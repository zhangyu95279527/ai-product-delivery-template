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


def yaml_list_items(text, key):
    # 解析 YAML 顶层键的列表值: 支持 "key: [a, b]" 内联与 "key:\n  - a" 块两种写法
    m = re.search(r"^%s:\s*\[(.*?)\]" % key, text, re.M)
    if m:
        return [x.strip().strip('"') for x in m.group(1).split(",") if x.strip()]
    items = []
    in_block = False
    for line in text.splitlines():
        if re.match(r"^%s:\s*$" % key, line):
            in_block = True
            continue
        if in_block:
            item = re.match(r"^\s+-\s*(\S+)", line)
            if item:
                items.append(item.group(1).strip('"'))
            elif re.match(r"^\S", line):
                break
    return items


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
    # 扫描门记录, 提取 gate/artifact/decision/date 等顶层标量与 criteria_failed 列表
    records = []
    for path in sorted(gates_dir.glob("*.yaml")):
        data = yaml_scalars(path, {"gate", "artifact", "decision", "date", "role", "recycle_target"})
        if data.get("gate") in GATES and data.get("artifact"):
            data["criteria_failed"] = yaml_list_items(read_text(path), "criteria_failed")
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


# 角色显示顺序: 与 .agent/roles/role-catalog.md 一致, 组合角色(如 "PO + Architect")排在其后
ROLE_ORDER = ["PO", "Designer", "Architect", "Developer", "QA", "DevOps"]


def pbi_instances(features_dir):
    # 扫描 PBI 实例, 提取顶层标量与 dependencies 列表
    pbis = []
    for path in sorted(features_dir.glob("*.yaml")):
        data = yaml_scalars(path, {"id", "type", "feature_id", "status", "title", "owner_role"})
        if data.get("id"):
            data["dependencies"] = yaml_list_items(read_text(path), "dependencies")
            pbis.append(data)
    return pbis


def gate_go(latest, gate, artifact):
    # 指定 (门, 制品) 的最新决策是否为 go
    r = latest.get((gate, artifact))
    return bool(r and r.get("decision") == "go")


def stage_progress(latest, pbis, records):
    # 阶段进度: done = 门已放行; active = 有门记录(返工/挂起中)或上游门已放行; pending = 未开始
    stages = []

    g1 = latest.get(("G1", "product-brief"))
    g1_decision = g1.get("decision") if g1 else None
    stages.append(("Discovery (G1)",
                   "done" if g1_decision == "go" else ("active" if g1_decision else "pending"),
                   latest_decision(latest, "G1", "product-brief")))

    g2 = latest.get(("G2", "prd"))
    g2_decision = g2.get("decision") if g2 else None
    stages.append(("PRD (G2)",
                   "done" if g2_decision == "go" else (
                       "active" if g2_decision or g1_decision == "go" else "pending"),
                   latest_decision(latest, "G2", "prd")))

    ga = latest.get(("GA", "architecture-baseline"))
    ga_decision = ga.get("decision") if ga else None
    stages.append(("Architecture baseline (GA)",
                   "done" if ga_decision == "go" else ("active" if ga_decision else "pending"),
                   latest_decision(latest, "GA", "architecture-baseline") if ga else "on-demand"))

    if pbis:
        counts = {}
        g3_passed = 0
        for p in pbis:
            counts[p.get("status", "?")] = counts.get(p.get("status", "?"), 0) + 1
            if gate_go(latest, "G3", p["id"]):
                g3_passed += 1
        detail = "%d PBIs (%s); G3 passed: %d" % (
            len(pbis),
            ", ".join("%s: %d" % (s, counts[s]) for s in EXEC_STATES if s in counts),
            g3_passed)
        stages.append(("Backlog & refinement (G3)", "active", detail))
    else:
        stages.append(("Backlog & refinement (G3)",
                       "active" if g2_decision == "go" else "pending", "no PBIs yet"))

    started = [p for p in pbis if gate_go(latest, "G3", p["id"])]
    done_pbis = [p for p in pbis if p.get("status") == "done"]
    if started:
        g4_passed = sum(1 for p in started if gate_go(latest, "G4", p["id"]))
        state = "done" if len(done_pbis) == len(pbis) else "active"
        stages.append(("Implementation & verification (G4)", state,
                       "executable: %d; done: %d; G4 passed: %d" % (len(started), len(done_pbis), g4_passed)))
    else:
        stages.append(("Implementation & verification (G4)", "pending", "no PBI passed G3 yet"))

    g5_records = [r for r in records if r.get("gate") == "G5"]
    g5_go_count = sum(1 for r in g5_records if r.get("decision") == "go")
    if g5_go_count:
        stages.append(("Release (G5)", "done", "%d release(s) passed G5" % g5_go_count))
    elif g5_records:
        stages.append(("Release (G5)", "active", "gating in progress"))
    elif done_pbis:
        stages.append(("Release (G5)", "pending", "%d PBI(s) done, release not gated" % len(done_pbis)))
    else:
        stages.append(("Release (G5)", "pending", "no release yet"))

    return stages


def next_actions(latest, pbis, records, baseline, adrs):
    # 角色待办: 从门状态与 PBI 执行态派生; owner_role 优先, 缺省按状态归属角色
    # 派生依据: .agent/roles/role-catalog.md 的角色x制品矩阵与 gates.yaml 的 decision_maker
    actions = {}

    def add(role, text):
        actions.setdefault(role, []).append(text)

    # 产品侧: G1/G2 人工门是流程起点
    g1 = latest.get(("G1", "product-brief"))
    if not gate_go(latest, "G1", "product-brief"):
        if g1 and g1.get("decision") == "recycle":
            add("PO", "返工 Product Brief（G1 recycle %s）后重提 G1" % g1.get("date", "?"))
        elif g1 and g1.get("decision") == "hold":
            add("PO", "Product Brief 处于 hold（%s），解除挂起条件后重提 G1" % g1.get("date", "?"))
        else:
            add("PO", "完成 Product Brief 并提交 G1 评审（00-discovery）")
    elif not gate_go(latest, "G2", "prd"):
        g2 = latest.get(("G2", "prd"))
        if g2 and g2.get("decision") == "recycle":
            add("PO", "返工 PRD（G2 recycle %s）后重提 G2" % g2.get("date", "?"))
        elif g2 and g2.get("decision") == "hold":
            add("PO", "PRD 处于 hold（%s），解除挂起条件后重提 G2" % g2.get("date", "?"))
        else:
            add("PO", "推进 PRD 并提交 G2 评审（01-prd）")
    elif not pbis:
        add("PO", "拆分 Backlog 并起草 PBI（02-backlog）")

    # 架构侧: GA/GB 人工门
    ga = latest.get(("GA", "architecture-baseline"))
    if ga and ga.get("decision") == "recycle":
        add("Architect", "返工 Architecture Baseline（GA recycle %s）" % ga.get("date", "?"))
    elif ga and ga.get("decision") == "hold":
        add("Architect", "Architecture Baseline 处于 hold（%s）" % ga.get("date", "?"))
    elif md_status_header(baseline) == "in-review" and not gate_go(latest, "GA", "architecture-baseline"):
        add("Architect", "Architecture Baseline 待 GA 评审")
    for adr in adrs:
        gb = latest.get(("GB", adr.stem))
        if gb and gb.get("decision") == "recycle":
            add("Architect", "返工 %s（GB recycle %s）" % (adr.stem, gb.get("date", "?")))
        elif adr_status(adr) == "proposed" and not gate_go(latest, "GB", adr.stem):
            add("Architect", "%s 待 GB 评审" % adr.stem)

    # PBI 侧: 按执行态归派, dependencies 中有未 done 的标 blocked
    status_by_id = {p["id"]: p.get("status") for p in pbis}
    for p in pbis:
        pid = p["id"]
        st = p.get("status")
        owner = p.get("owner_role") or None
        blocked_by = [d for d in p.get("dependencies", []) if status_by_id.get(d) != "done"]
        suffix = "（blocked by %s）" % ", ".join(blocked_by) if blocked_by else ""
        if st == "done":
            continue
        g3 = latest.get(("G3", pid))
        g4 = latest.get(("G4", pid))
        if st == "draft":
            if g3 and g3.get("decision") == "recycle":
                failed = ", ".join(g3.get("criteria_failed", [])) or "见门记录"
                add(owner or "PO", "%s 被 G3 打回（%s），返工后重提" % (pid, failed))
            else:
                add(owner or "PO", "%s 精炼中：补齐验收标准/设计/技术设计，备齐 G3 输入" % pid)
        elif st == "ready":
            if not gate_go(latest, "G3", pid):
                add("PO + Architect", "%s 待 G3 评审" % pid)
            else:
                add(owner or "Developer", "%s 已过 G3，可启动实现%s" % (pid, suffix))
        elif st == "in-progress":
            add(owner or "Developer", "%s 实现中%s" % (pid, suffix))
        elif st == "in-verification":
            if g4 and g4.get("decision") == "recycle":
                add(owner or "Developer", "%s 被 G4 打回，修复后重交验证" % pid)
            else:
                add("QA + PO", "%s 待 G4 验证评审" % pid)

    # 发布侧: done 且 G4 go 晚于最近一次 G5 go 的 PBI, 提示可筹划发布
    last_g5_go = max((r.get("date", "") for r in records
                      if r.get("gate") == "G5" and r.get("decision") == "go"), default="")
    releasable = []
    for p in pbis:
        if p.get("status") != "done":
            continue
        g4 = latest.get(("G4", p["id"]))
        if g4 and g4.get("decision") == "go" and g4.get("date", "") > last_g5_go:
            releasable.append(p["id"])
    if releasable:
        add("PO", "%d 个 PBI 已 done（%s），可筹划发布并提交 G5 评审" % (
            len(releasable), ", ".join(releasable)))

    return actions


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
    pbis = pbi_instances(root / "docs" / "features")
    baseline = root / "docs" / "architecture" / "architecture-baseline.md"
    adrs = sorted((root / "docs" / "architecture" / "adr").glob("*.md"))

    # 阶段进度: 回答"项目到哪了"; 各阶段状态由门记录与制品状态派生
    add("## Stage progress")
    add("")
    add("| Stage | State | Detail |")
    add("|---|---|---|")
    for name, state, detail in stage_progress(latest, pbis, records):
        add("| %s | %s | %s |" % (name, state, cell(detail)))
    add("")

    # 角色待办: 回答"接下来谁做什么"; 依赖未满足项标 blocked
    add("## Next actions by role")
    add("")
    actions = next_actions(latest, pbis, records, baseline, adrs)
    if actions:
        ordered = [r for r in ROLE_ORDER if r in actions]
        ordered += sorted(r for r in actions if r not in ROLE_ORDER)
        for role in ordered:
            add("### %s" % role)
            for item in actions[role]:
                add("- %s" % item)
            add("")
    else:
        add("No pending actions derived.")
        add("")

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
    add("| Artifact | Status | Gate | Latest decision |")
    add("|---|---|---|---|")
    add("| Architecture Baseline | %s | GA | %s |" % (
        md_status_header(baseline), latest_decision(latest, "GA", "architecture-baseline")))
    for adr in adrs:
        add("| ADR %s | %s | GB | %s |" % (
            adr.stem, adr_status(adr), latest_decision(latest, "GB", adr.stem)))
    if not adrs:
        add("| ADR | — | GB | — |")
    add("")

    # PBI 列表与执行态计数, PBI 实例存放于 docs/features/
    add("## PBIs")
    add("")
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
