#!/usr/bin/env python3
# 状态派生器: 扫描仓库内的制品与门记录, 生成 docs/delivery/status.md
# 原则: status.md 是派生的只读视图, 禁止手工编辑; 项目状态的唯一来源是制品本身
# 仅使用标准库; 解析只依赖本仓库模板的顶层标量字段, 不做通用 YAML 解析
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOC_STATES = ["draft", "in-review", "approved", "living", "superseded"]
EXEC_STATES = ["draft", "ready", "in-progress", "in-verification", "done"]
GATES = ["G1", "G2", "G3", "G4", "G5", "GA", "GB"]


def read_text(path):
    return path.read_text(encoding="utf-8")


def md_status_header(path):
    # 解析 Markdown 顶部的状态头: "Status: xxx"
    m = re.search(r"^Status:\s*([a-z-]+)", read_text(path), re.M)
    return m.group(1) if m else "unknown"


def adr_status(path):
    # 解析 ADR 模板 "## Status" 标题下第一个非空行的首个单词
    lines = read_text(path).splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "## Status":
            for rest in lines[i + 1:]:
                word = rest.strip().split(" ")[0] if rest.strip() else ""
                if word:
                    return re.sub(r"[^a-z-]", "", word) or "unknown"
            return "unknown"
    return "unknown"


def yaml_scalars(path, keys):
    # 提取 YAML 顶层标量字段, 值内联注释一并剥离
    found = {}
    for line in read_text(path).splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m and m.group(1) in keys and m.group(1) not in found:
            value = m.group(2).split(" #", 1)[0].strip().strip('"')
            found[m.group(1)] = value
    return found


def sprint_info(path):
    # 解析 sprint.yaml: 全部字段位于顶层 sprint: 块下, 缩进两格
    info = {}
    in_block = False
    for line in read_text(path).splitlines():
        if re.match(r"^sprint:", line):
            in_block = True
            continue
        if in_block:
            if re.match(r"^\S", line):
                break
            m = re.match(r"^\s{2}([a-z_]+):\s*(.*)$", line)
            if m and m.group(1) not in info:
                value = m.group(2).split(" #", 1)[0].strip().strip('"')
                info[m.group(1)] = value
    items = re.findall(r"^\s*-\s*(PBI-\S+)", read_text(path), re.M)
    info["pbi_count"] = str(len(items))
    return info


def gate_records(gates_dir):
    # 扫描门记录, 提取 gate/artifact/decision/date 四个顶层标量
    records = []
    for path in sorted(gates_dir.glob("*.yaml")):
        data = yaml_scalars(path, {"gate", "artifact", "decision", "date"})
        if data.get("gate") in GATES and data.get("artifact"):
            records.append({"file": path.name, **data})
    return records


def latest_by_gate_artifact(records):
    # 同一 (gate, artifact) 取最新一条: 先按记录日期, 再按文件名(YYYYMMDD 前缀可排序)
    latest = {}
    for r in records:
        key = (r["gate"], r["artifact"])
        rank = (r.get("date", ""), r["file"])
        if key not in latest or rank > latest[key][0]:
            latest[key] = (rank, r)
    return {key: r for key, (rank, r) in latest.items()}


def latest_decision(latest, gate, artifact):
    r = latest.get((gate, artifact))
    if not r:
        return "—"
    return "%s (%s)" % (r.get("decision", "?"), r.get("date", "?"))


def cell(value):
    # 表格单元格清洗: 空值占位, 去掉会破坏表格的字符
    value = (value or "").strip()
    return value.replace("|", "/") if value else "—"


def build(root):
    lines = []
    add = lines.append

    add("# Delivery Status")
    add("")
    add("Derived from repository artifacts by `scripts/build-status.py`. Do not edit by hand; regenerate instead.")
    add("")
    add("Generated: %s" % date.today().isoformat())
    add("")

    records = gate_records(root / "docs" / "delivery" / "gates")
    latest = latest_by_gate_artifact(records)

    # 产品侧: Product Brief (G1) 与 PRD (G2), 状态头来自文件本身
    add("## Product")
    add("")
    add("| Artifact | Status | Gate | Latest decision |")
    add("|---|---|---|---|")
    brief = root / "docs" / "product" / "product-brief.md"
    prd = root / "docs" / "product" / "prd" / "00-overview.md"
    add("| Product Brief | %s | G1 | %s |" % (
        md_status_header(brief), latest_decision(latest, "G1", "product-brief")))
    add("| PRD (00-overview) | %s | G2 | %s |" % (
        md_status_header(prd), latest_decision(latest, "G2", "prd")))
    add("")

    # 架构侧: Baseline (GA) 与全部 ADR (GB)
    add("## Architecture")
    add("")
    baseline = root / "docs" / "architecture" / "architecture-baseline.md"
    add("| Artifact | Status | Gate | Latest decision |")
    add("|---|---|---|---|")
    add("| Architecture Baseline | %s | GA | %s |" % (
        md_status_header(baseline), latest_decision(latest, "GA", "architecture-baseline")))
    adr_dir = root / "docs" / "architecture" / "adr"
    adrs = sorted(adr_dir.glob("*.md"))
    for adr in adrs:
        add("| ADR %s | %s | GB | %s |" % (
            adr.stem, adr_status(adr), latest_decision(latest, "GB", adr.stem)))
    if not adrs:
        add("| ADR | — | GB | — |")
    add("")

    # PBI 列表与执行态计数, PBI 实例存放于 docs/features/
    add("## PBIs")
    add("")
    features_dir = root / "docs" / "features"
    pbis = []
    for path in sorted(features_dir.glob("*.yaml")):
        data = yaml_scalars(path, {"id", "type", "feature_id", "status", "title"})
        if data.get("id"):
            pbis.append(data)
    if pbis:
        counts = {}
        for p in pbis:
            counts[p.get("status", "?")] = counts.get(p.get("status", "?"), 0) + 1
        add("Total: %d — %s" % (len(pbis), ", ".join(
            "%s: %d" % (s, counts[s]) for s in EXEC_STATES if s in counts)))
        add("")
        add("| PBI | Type | Feature | Status | Latest gate decision |")
        add("|---|---|---|---|---|")
        for p in pbis:
            decision = latest_decision(latest, "G4", p["id"])
            if decision == "—":
                decision = latest_decision(latest, "G3", p["id"])
            add("| %s | %s | %s | %s | %s |" % (
                cell(p.get("id")), cell(p.get("type")), cell(p.get("feature_id")),
                cell(p.get("status")), decision))
    else:
        add("No PBI instances yet.")
    add("")

    # Sprint 列表 (仅当 delivery.method: scrum 时使用)
    add("## Sprints")
    add("")
    sprints_dir = root / "docs" / "delivery" / "sprints"
    sprints = [sprint_info(p) for p in sorted(sprints_dir.glob("*.yaml"))]
    sprints = [s for s in sprints if s.get("id")]
    if sprints:
        add("| Sprint | Status | Goal | Start | End | PBIs |")
        add("|---|---|---|---|---|---|")
        for s in sprints:
            add("| %s | %s | %s | %s | %s | %s |" % (
                cell(s.get("id")), cell(s.get("status")), cell(s.get("goal")),
                cell(s.get("start")), cell(s.get("end")), cell(s.get("pbi_count"))))
    else:
        add("No sprints yet.")
    add("")

    # 最近门记录, 按日期与文件名倒序取 10 条
    add("## Recent gate records")
    add("")
    if records:
        add("| Date | Gate | Artifact | Decision | Record |")
        add("|---|---|---|---|---|")
        recent = sorted(records, key=lambda r: (r.get("date", ""), r["file"]), reverse=True)[:10]
        for r in recent:
            add("| %s | %s | %s | %s | %s |" % (
                cell(r.get("date")), cell(r.get("gate")), cell(r.get("artifact")),
                cell(r.get("decision")), r["file"]))
    else:
        add("No gate records yet.")
    add("")

    return "\n".join(lines)


def main():
    out = ROOT / "docs" / "delivery" / "status.md"
    out.write_text(build(ROOT), encoding="utf-8", newline="\n")
    print("wrote %s" % out)


if __name__ == "__main__":
    sys.exit(main())
