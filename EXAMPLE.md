# 最佳实践示例：MiniTodo 从 0 到 v0.1

本文用一个最简单的产品，端到端演示本体系的完整用法：从产品想法开始，每个阶段谁做什么、产出什么制品、过什么门、git 提交什么，直到发布上线与 CI/CD。

文中所有制品片段均按 `.agent/templates/` 与 `.agent/gates/gates.yaml` 的真实字段编写，可直接对照。本文属模板域，实例化后可自由删除；模板升级可能带回新版本。

## 案例设定

- **产品**：MiniTodo —— 纯静态待办事项网页应用，数据存浏览器 localStorage，无后端、无账号。
- **团队**：3 人 + agent 协作。角色是责任不是人头（见 `.agent/roles/role-catalog.md`），本例中：
  - 林岚：Product Owner（PO）
  - 陈实：Product Designer + Developer + Architect
  - 赵稳：QA + DevOps/Platform
  - agent：承担各角色的执行工作（起草制品、写代码、跑 git）；人只做两件事：审内容、做门决策
- **形态**：monorepo。单服务小产品，交付仓即代码仓（适用边界见 `OPERATING-GUIDE.md` 的 Git 与仓库结构章）。
- **交付方法**：通用路径，不选 Scrum。
- **平台**：GitHub。PR 评审承载人工门，Actions 跑 CI/CD，Pages 做 staging 环境。

## 全程概览

| 阶段 | 日期 | 主导角色 | 提示词 | 产出 | 门 | 结果 |
|---|---|---|---|---|---|---|
| 准备 | 10-09 | 全员 | — | 实例仓 + 平台配置 | — | — |
| Discovery | 10-09 | PO | 00-discovery | product-brief.md | G1 | go |
| PRD | 10-10 | PO | 01-prd | prd/ 七节 | G2 | go |
| Backlog | 10-11 | PO | 02-backlog | 3 个 PBI 草稿 | G3 输入 | — |
| 架构基线 | 10-12 | Architect | 05-architecture | architecture-baseline.md | GA | go |
| PBI 精炼 + 设计 | 10-13 ~ 10-14 | PO/Designer/Developer | 03 → 04 → 06 | 精炼 PBI + UX + 技术设计 | G3 ×3 | 2 go / 1 recycle 后 go |
| Task 分解 | 10-14 | Developer | 09-task-planning | Task DAG | G3 判据 | — |
| 实现 | 10-14 ~ 10-16 | Developer | 10-implementation | 代码增量 | G4 输入 | — |
| 验证 | 10-16 ~ 10-17 | QA | 11-verification | 验证证据 | G4 ×3 | go |
| 发布 | 10-18 | DevOps 执行 / PO 决策 | — | Release v0.1.0 | G5 | go |

## 0. 准备：实例化与平台配置

一次性工作，全员参与，约半天。

**林岚执行实例化**（命令由 agent 代劳，下同）：

```bash
git clone <template-url> minitodo
cd minitodo
git remote rename origin template
git remote add origin git@github.com:example/minitodo.git
git push -u origin main
```

`TEMPLATE-VERSION`（内容为 `v0.4`）随 clone 带过来，即为实例的模板基线版本。

**林岚建立项目上下文** `.agent/local/project-context.md`：

```markdown
# MiniTodo 项目上下文

- 产品：纯静态待办事项网页应用，无后端，数据存 localStorage
- 团队：林岚(PO)、陈实(Designer/Developer/Architect)、赵稳(QA/DevOps)
- 仓库：monorepo，本仓即代码仓，组件名 web-app
- 环境：staging = GitHub Pages（main 自动部署）；production = 静态托管（tag 触发，PO 审批）
- 约定：制品正文中文；提交信息中文一句话
```

**赵稳完成平台配置**（对应 `OPERATING-GUIDE.md` 实例化清单第 3-4 步）：

- main 分支保护：禁止直推，PR 需 1 人评审。
- required reviewers 映射人工门责任人：G1/G2/G5 → 林岚，GA/GB → 陈实。
- CI：push 时自动运行 `python scripts/build-status.py` 做体系自检（workflow 见第 9 节）。
- GitHub environments：`staging`（无保护）、`production`（required reviewers = 林岚）—— G5 的人工决策由此在平台上承载。

初始目录树（模板基线）：

```text
minitodo/
├── AGENTS.md
├── OPERATING-GUIDE.md
├── TEMPLATE-VERSION
├── .agent/
│   ├── prompts/        # 14 个阶段提示词
│   ├── gates/          # 门定义
│   ├── roles/          # 角色目录
│   ├── skills/         # 3 个能力
│   ├── templates/      # 制品模板
│   └── local/          # 实例域：project-context.md
├── docs/
│   ├── product/        # product-brief.md + prd/ 骨架
│   ├── architecture/   # architecture-baseline.md 骨架
│   ├── features/       # PBI 将放这里
│   └── delivery/       # gates/ releases/ checkpoints/ sprints/ + status.md
└── scripts/
    └── build-status.py
```

## 1. Discovery：Product Brief 与 G1

**主导**：林岚（PO）。**咨询**：陈实（Architect/Designer 视角）。

林岚开新会话，粘贴 `.agent/prompts/00-discovery.md` 的指令段，附上想法："我想做一个打开浏览器就能用的极简待办工具，先验证身边同事愿不愿意用。"agent 起草 `docs/product/product-brief.md`，林岚改定后：

```markdown
# Product Brief（产品简报）

Status: in-review <!-- 文档生命周期: draft | in-review | approved | living | superseded -->

## 产品愿景
让记录待办这件事的成本趋近于零：打开页面就能记，无需注册无需安装。

## 问题
团队同学记临时待办散落在聊天消息、纸便签和脑子里，经常丢失。
现有待办应用要求注册登录，为记一件小事成本过高。

## 目标用户
本部门约 30 名同事（首批）；此后扩展到任何想"打开就记"的人。

## 价值主张
零账号、零安装、打开即用的待办列表；数据留在本机浏览器，无隐私顾虑。

## 证据 / 假设
- 事实：部门群近一个月有 12 条"提醒我一下……"的消息（林岚手工统计）。
- 假设：至少 10 名同事愿意把一个静态网页加入书签日常使用。
- 假设：localStorage 持久化对单人单设备场景足够。

## 初始边界
做：单个待办列表的增、完成/取消完成、删；浏览器本地持久化。
不做：多列表、标签、截止日期、云同步、账号体系、移动端 App。

## 成功信号
上线 4 周内：至少 10 名同事周活跃使用；收到至少 5 条自发反馈。

## 开放问题
- 同事换浏览器/设备后数据丢失是否会成为主要抱怨？（上线后收集）
```

**G1 评审**：agent 把制品放上短分支 `g1-product-brief` 并开 PR；林岚作为 required reviewer 逐条对照 G1 判据（问题/用户/背景已描述；事实与假设分离；已考虑替代方案与非目标；成果/风险/开放问题已列），评审通过、合并 PR。门记录由 agent 落盘：

`docs/delivery/gates/20261009-g1-product-brief.yaml`：

```yaml
id: GATE-RECORD-0001
gate: G1
artifact: docs/product/product-brief.md
decision: go
criteria_met: [problem-users-context, facts-separated, alternatives-considered, outcomes-risks-defined]
criteria_failed: []
decided_by: 林岚
role: product-owner
date: 2026-10-09
recycle_target: ""
follow_up: []
notes: 非目标明确（无账号无同步），首批用户定为本部门，风险可控。
```

**git**：PR 合并 = 一次提交，含制品 + 门记录 + 重新生成的 `status.md`（agent 运行 `python scripts/build-status.py`）。制品 Status 行在合并前改为 `approved`。

## 2. PRD 与 G2

**主导**：林岚（PO）。**咨询**：陈实（Designer/Architect）、赵稳（QA）。

新会话粘贴 `01-prd.md` 指令段，agent 读取 G1 已过门的 product-brief，把 `docs/product/prd/` 七节从骨架填成实质内容。最关键的两节：

`03-functional-requirements.md`（节选）：

```markdown
# PRD — 03-functional-requirements

- FR-1 添加待办：输入文本并确认后，列表新增一条未完成待办。
- FR-2 空白保护：输入为空或仅空白字符时不产生新待办。
- FR-3 完成切换：每条待办可在未完成/已完成之间切换，已完成有明确的视觉区分。
- FR-4 删除：每条待办可删除，删除后不可恢复（MVP 无回收站）。
- FR-5 本地持久化：列表内容在页面刷新、浏览器重启后保持。
```

`06-mvp-scope.md`：

```markdown
# PRD — 06-mvp-scope

## MVP 范围内
单个待办列表：添加（FR-1/FR-2）、完成切换（FR-3）、删除（FR-4）、localStorage 持久化（FR-5）。
桌面与手机浏览器可用（响应式单页）。

## 明确不做
多列表、编辑已有待办文本、截止日期与提醒、拖拽排序、云同步与账号、导入导出、回收站/撤销删除。

## 后续候选（不承诺）
编辑文本、撤销删除、多设备同步——视上线反馈从 Product Backlog 重新排队。
```

其余五节（overview/users/user-journeys/business-rules/nfr）各 5-15 行实质内容，例如 NFR 写明"首屏加载小于 2 秒（办公网络）、支持最近两个版本的 Chrome/Edge/Safari"。

**G2 评审**：短分支 `g2-prd` + PR，林岚对照 G2 判据（七节有实质内容；MVP 边界双向明确；无方向性开放问题；需求可被 PBI 追溯）。发现 NFR 节初稿写了"性能要好"这类不可测表述，PR 评论后 agent 修订为可测量口径，随后通过。

`docs/delivery/gates/20261010-g2-prd.yaml`：

```yaml
id: GATE-RECORD-0002
gate: G2
artifact: docs/product/prd/
decision: go
criteria_met: [sections-complete, mvp-scope-explicit, no-material-open-questions, requirements-traceable]
criteria_failed: []
decided_by: 林岚
role: product-owner
date: 2026-10-10
recycle_target: ""
follow_up: []
notes: NFR 节的不可测表述已在 PR 评审中修订；FR 编号供 PBI 追溯。
```

**git**：同上，PR 合并一次提交（prd 七节 + 门记录 + status.md）。PRD 各节 Status 行改为 `living` —— PRD 是活文档，此后随证据受控演进。

## 3. Product Backlog：PBI 草稿

**主导**：林岚（PO）。

新会话粘贴 `02-backlog.md` 指令段（agent 自动加载 `writing-acceptance-criteria` skill），把 PRD 转成排好序的 Backlog：一个 Feature（FEAT-001 待办列表管理）下 3 个 PBI 草稿，落盘 `docs/features/`。PBI 草稿是**无门制品**（G3 的输入），落盘即提交，不需要 PR。

`docs/features/PBI-0001.yaml`（草稿）：

```yaml
id: PBI-0001
type: user-story
feature_id: FEAT-001
status: draft
title: 添加待办
value: 用户能记录新待办，这是产品的存在理由（FR-1/FR-2/FR-5）
user_story:
  as_a: 打开页面的访客
  i_want: 输入一条待办并添加
  so_that: 它不会丢，之后随时能看到
acceptance_criteria: []   # 草稿阶段可空，精炼时补全
dependencies: []
references: [docs/product/prd/03-functional-requirements.md]
```

PBI-0002（完成切换，FR-3）、PBI-0003（删除，FR-4）结构相同，排序依次在后。

**git**：agent 直推 main：`PBI 草稿：FEAT-001 下 PBI-0001~0003`。

## 4. 架构基线与 GA

**主导**：陈实（Architect）。**咨询**：林岚（PO）、赵稳（DevOps）。

产品简单，但基线不能省 —— 它回答"边界在哪"，此后的技术设计不许静默越界。新会话粘贴 `05-architecture.md` 指令段，产出**薄基线**（每节一两句，但节节有实质内容）：

```markdown
# Architecture Baseline（架构基线）

Status: in-review

## 当前视界
单页静态 Web 应用，无后端，无构建管线（原生 HTML/CSS/JS，免打包）。

## 系统上下文
用户浏览器 ↔ 静态文件托管。无任何外部服务调用。

## 主要组件/服务
- web-app（本仓）：index.html + app.js + style.css，仓库即组件，无外部代码仓。

## 数据
唯一数据：待办列表，存浏览器 localStorage，键 minitodo.items，
结构为 [{ id, text, done }]。无服务端数据，无跨设备同步。

## 集成
无。

## 身份/安全
无账号体系。XSS 是唯一实质风险：渲染待办文本一律走 textContent，禁止 innerHTML 拼接。

## 运行时/部署
staging：GitHub Pages（main 自动部署）；production：静态托管（tag 触发部署）。

## 可观测性
无服务端可观测性。前端不采集数据（MVP 明示）；使用反馈走群内人工收集。

## 重要约束/NFR
首屏 < 2s；支持最近两个版本 Chrome/Edge/Safari；无任何运行时依赖与 CDN 引用。

## 开放架构问题
- 多设备同步若进入 Backlog，将触发架构演进（GB/ADR），不在本次基线内。
```

**GA 评审**：短分支 `ga-baseline` + PR，陈实作为 Architect 角色人工决策（required reviewer）。对照判据：节节有实质内容、关键权衡已记录（无构建管线、localStorage 选型、XSS 约束）、开放问题已列。通过。

`docs/delivery/gates/20261012-ga-architecture-baseline.yaml`：

```yaml
id: GATE-RECORD-0003
gate: GA
artifact: docs/architecture/architecture-baseline.md
decision: go
criteria_met: [baseline-substantive, tradeoffs-recorded, open-questions-listed]
criteria_failed: []
decided_by: 陈实
role: architect
date: 2026-10-12
recycle_target: ""
follow_up: []
notes: 薄基线，与产品复杂度匹配；多设备同步明确留待 GB/ADR。
```

**git**：PR 合并（基线 + 门记录 + status.md），Status 行改 `living`。

## 5. PBI 精炼、UX/UI、技术设计与 G3

**主导**：林岚（PO，精炼）→ 陈实（Designer，UX/UI）→ 陈实（Developer，技术设计）。**决策**：PO + Architect 共同（G3 非强制人工门，agent 可按角色执行，本例中林岚和陈实选择让 agent 执行、自己抽查）。

三个 PBI 逐个走 03 → 04 → 06（可交叉进行）。以 PBI-0001 为例。

### 5.1 精炼（03-feature-refinement）

agent 加载 `writing-acceptance-criteria` skill，把 AC 补全到 PBI。每条 AC 通过三问测试（什么触发、观察什么、通过/失败边界在哪）且可附证据：

`docs/features/PBI-0001.yaml`（精炼后）：

```yaml
id: PBI-0001
type: user-story
feature_id: FEAT-001
status: ready
title: 添加待办
value: 用户能记录新待办，这是产品的存在理由（FR-1/FR-2/FR-5）
user_story:
  as_a: 打开页面的访客
  i_want: 输入一条待办并添加
  so_that: 它不会丢，之后随时能看到
acceptance_criteria:
  - 在输入框键入"买牛奶"并点击"添加"按钮后，待办列表中出现一条文字为"买牛奶"的未完成待办
  - 添加成功后，输入框内容被清空
  - 输入框为空或仅含空白字符时点击"添加"，列表不产生新待办
  - 添加待办后刷新页面，该待办仍以原有状态出现在列表中
dependencies: []
references:
  - docs/product/prd/03-functional-requirements.md
  - docs/features/PBI-0001-ux.md
  - docs/features/PBI-0001-tech-design.md
```

### 5.2 UX/UI（04-ux-ui）

PBI 有用户界面，需要 `design-ready` 输入。陈实（Designer）与 agent 产出 `docs/features/PBI-0001-ux.md` —— 无门制品，被 PBI `references` 引用后有效。线框用 ASCII 即可，视觉稿若有 Figma 源文件则按制品形态规则存外部、仓内放指针：

```markdown
# PBI-0001 UX

## 线框

  +--------------------------------------+
  |  MiniTodo                            |
  |  +----------------------+ +--------+ |
  |  | 输入待办……           | |  添加  | |
  |  +----------------------+ +--------+ |
  |  [ ] 买牛奶                      (删) |
  |  [x] 写周报                        (删) |
  +--------------------------------------+

## 交互约定
- 输入框自动聚焦；回车等同点击"添加"
- 空白输入点击"添加"：无新增，无报错提示，输入框内容保留
- 已完成项：复选框勾选 + 文字删除线，颜色降为灰
- (删) 按钮本 PBI 仅占位，行为归 PBI-0003
```

### 5.3 技术设计（06-technical-design）

agent 读取已过 GA 的基线 + 精炼 PBI + UX，产出 `docs/features/PBI-0001-tech-design.md`（节选）：

```markdown
# PBI-0001 技术设计

## 最小切片
index.html：输入框 #new-item、按钮 #add-btn、列表容器 #list。
app.js：load() 从 localStorage['minitodo.items'] 读数组渲染；
add() 校验空白 → push { id, text, done:false } → save() → 重渲染。

## 契约与数据
localStorage 键与结构遵从基线；id 用 Date.now() 加随机后缀。

## 安全
渲染一律 element.textContent = item.text（基线 XSS 约束）。

## 失败行为
localStorage 不可用（隐私模式）：页面顶部固定提示"当前浏览器不保存数据"，添加功能仍可用（仅内存）。

## 测试策略
CI：node --check 语法检查 + 体系自检；AC 由 QA 在实现分支预览环境手工验证（第 8 节）。
```

### 5.4 G3 评审（含一次 recycle）

G3 是滚动门，三个 PBI 各评一次。判据五条：ac-verifiable / design-ready / tech-design-ready / tasks-decomposed / dependencies-confirmed（Task 分解见第 6 节，与 PBI 一起过门）。

- **PBI-0001：go**。五条全过。
- **PBI-0002：recycle**。初稿 AC 第一条写"已完成待办在视觉上明显区别于未完成待办" —— 不可客观验证（"明显"没有通过/失败边界）。G3 打回，按路由表 ac-verifiable → feature-refinement → PO：

`docs/delivery/gates/20261013-g3-pbi-0002.yaml`：

```yaml
id: GATE-RECORD-0005
gate: G3
artifact: PBI-0002
decision: recycle
criteria_met: [design-ready, tech-design-ready, tasks-decomposed, dependencies-confirmed]
criteria_failed: [ac-verifiable]
decided_by: ""
role: product-owner + architect（agent 按角色执行）
date: 2026-10-13
recycle_target: feature-refinement
follow_up: [PO 把 AC-1 改写为可客观判定的表述（明确勾选态与删除线样式）]
notes: "明显区别于"无通过/失败边界，违反 ac-verifiable。
```

林岚修订 AC-1 为"点击未完成待办的复选框后，该条复选框呈勾选状态且文字带删除线"。次日 G3 重评，五条全过，新落一条 go 记录（门记录只追加不修改）。**这次 recycle 是有价值的信号，不是过错** —— 它发生在文档阶段，成本是一次改写；若漏到 G4，成本是返工。

- **PBI-0003：go**。

`docs/delivery/gates/20261013-g3-pbi-0001.yaml`（PBI-0001 的 go 记录）：

```yaml
id: GATE-RECORD-0004
gate: G3
artifact: PBI-0001
decision: go
criteria_met: [ac-verifiable, design-ready, tech-design-ready, tasks-decomposed, dependencies-confirmed]
criteria_failed: []
decided_by: ""
role: product-owner + architect（agent 按角色执行）
date: 2026-10-13
recycle_target: ""
follow_up: []
notes: ""
```

**git**：G3/G4 滚动门由 agent 直推 main：精炼 PBI + UX + 技术设计 + Task + 门记录 + status.md，按 PBI 分次提交。

## 6. Task 分解

**主导**：陈实（Developer）。新会话粘贴 `09-task-planning.md` 指令段（agent 自动加载 `decomposing-tasks` skill），为每个 PBI 分解 Task。PBI-0001 的 DAG：

`docs/features/TASK-0001.yaml`：

```yaml
id: TASK-0001
pbi_id: PBI-0001
status: draft
objective: 页面骨架：index.html（输入框、添加按钮、列表容器）+ style.css 基础布局，按 UX 线框
depends_on: []
inputs: [docs/features/PBI-0001.yaml, docs/features/PBI-0001-ux.md]
affected_repositories: [minitodo]
affected_components: [web-app]
allowed_scope: [index.html, style.css]
verification: [页面在浏览器打开后呈现线框布局，输入框自动聚焦]
executor:
  mode: agent
  adapter: codex
```

`TASK-0002`（添加与持久化逻辑，`allowed_scope: [app.js]`，`depends_on: [TASK-0001]`）与 `TASK-0003`（视觉样式完善，`allowed_scope: [style.css]`，`depends_on: [TASK-0001]`）依赖同一前置，**彼此无依赖、可并行** —— 并行来自 Task 依赖，不需要 Workstream 层。

Task 分解是 G3 的 `tasks-decomposed` 判据（DAG 覆盖全部 AC 且依赖已声明），随所属 PBI 一起过门，不单独设门。

## 7. 实现

**主导**：陈实（Developer，agent 执行）。新会话粘贴 `10-implementation.md` 指令段。

按 Task 粒度开短分支、小步提交；Task 状态沿 `draft → ready → in-progress → in-verification → done` 流转：

```bash
git checkout -b task-0001-page-skeleton
# agent 产出 index.html / style.css
git commit -m "TASK-0001 页面骨架：输入区与列表容器"
git checkout -b task-0002-add-logic
# agent 产出 app.js
git commit -m "TASK-0002 添加与 localStorage 持久化"
```

此时目录树出现代码（monorepo：代码与制品同仓）：

```text
minitodo/
├── index.html          # TASK-0001
├── app.js              # TASK-0002
├── style.css           # TASK-0001 / TASK-0003
├── docs/features/      # PBI + Task + UX + 技术设计
└── .github/workflows/  # 第 9 节
```

**合并规则**（来自提交节奏表）：Task 分支带齐 G4 证据后合并回 main —— 即实现分支不急着合，先走第 8 节验证；三个 PBI 的实现分支依次走"实现 → 分支预览验证 → G4 go → 合并"。

## 8. 验证与 G4

**主导**：赵稳（QA）。**决策**：QA + PO 共同（G4 非强制人工门，agent 按角色执行）。

新会话粘贴 `11-verification.md` 指令段（agent 自动加载 `collecting-verification-evidence` skill）。验证环境按门分层：G4 按 PBI 在实现分支的本地预览环境验证（agent 启动本地静态服务器）——因为合并规则要求"带齐 G4 证据后合并回 main"，而 staging 只部署 main；合并后 staging 再承接 G5 的集成增量复验（第 9 节）。

agent 起好分支预览后，赵稳逐条 AC 验证，证据落 `docs/features/PBI-0001-evidence.md`：

```markdown
# PBI-0001 验证证据

环境：实现分支本地预览（agent 启动的静态服务器，分支 task-0001~0003 合并态，commit a1b2c3d）
日期：2026-10-16  验证人：赵稳（QA）

| AC | 结果 | 证据 |
|---|---|---|
| 添加"买牛奶"后列表出现该条未完成待办 | pass | 截图 evidence/pbi-0001-ac1.png（外部网盘链接） |
| 添加成功后输入框清空 | pass | 同上录屏 |
| 空白输入点击"添加"不产生新待办 | pass | 空白/纯空格各一次，列表计数不变（文本记录） |
| 刷新后待办仍在 | pass | 刷新前后对比截图 |

DoD 适配勾选（按 .agent/scrum/definition-of-done.md 裁剪）：
- [x] acceptance criteria verified
- [x] code review completed（陈实 PR 评审）
- [x] automated checks passed（CI：build-status.py + node --check；本项目无单元测试，已裁剪并在此注明）
- [x] deployable artifact produced（纯静态文件，分支即可部署预览；合并后 staging 自动部署）
- [N/A] integration/E2E、security scans、observability、AI 检查 —— 无对应面，裁剪理由：纯静态无后端
```

注意两条体系规则的实况演示：**截图是二进制，按制品形态规则存外部、仓内放指针**；**DoD 按产品裁剪并显式注明 N/A 理由**，而不是假装执行。

`docs/delivery/gates/20261016-g4-pbi-0001.yaml`：

```yaml
id: GATE-RECORD-0008
gate: G4
artifact: PBI-0001
decision: go
criteria_met: [ac-verified, dod-passed, evidence-recorded]
criteria_failed: []
decided_by: ""
role: qa + product-owner（agent 按角色执行）
date: 2026-10-16
recycle_target: ""
follow_up: []
notes: 四条 AC 全过；证据含外部指针与文本记录。
```

G4 go 后 agent 合并实现分支回 main，PBI status 改 `done`。PBI-0002、PBI-0003 同法各过一次（10-17 全部 done）。

## 9. CI/CD 与发布（G5）

**执行**：赵稳（DevOps）。**决策**：林岚（PO，G5 强制人工）。

### 9.1 三个 workflow

`.github/workflows/ci.yml` —— 每次 push/PR 的体系与代码自检：

```yaml
name: ci
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.x" }
      - run: python scripts/build-status.py   # 体系自检：状态视图可从制品派生
      - run: node --check app.js              # 前端语法检查
```

`.github/workflows/deploy-staging.yml` —— main 更新自动部署 staging（每次 G4 合并后即可在类生产环境验证）：

```yaml
name: deploy-staging
on:
  push: { branches: [main] }
permissions:
  pages: write
  id-token: write
jobs:
  deploy:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: "." }
      - uses: actions/deploy-pages@v4
```

`.github/workflows/deploy-production.yml` —— tag 触发生产部署；`environment: production` 配了 required reviewers（林岚），**G5 的人工决策直接由平台承载**：

```yaml
name: deploy-production
on:
  push: { tags: ["v*"] }
jobs:
  release:
    environment: production        # 林岚在 GitHub 上 approve 才执行 = G5 决策动作
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: tar -czf minitodo-${{ github.ref_name }}.tar.gz index.html app.js style.css
      # 同步到生产静态托管（示例命令，替换为实际托管方式）：
      # aws s3 sync . s3://minitodo-prod --exclude "*" --include "*.html" --include "*.js" --include "*.css"
      - uses: softprops/action-gh-release@v2
        with:
          files: minitodo-${{ github.ref_name }}.tar.gz
          body: 发布记录见 docs/delivery/releases/
```

**CI/CD 不替代门**：自动化负责"检查与搬运"，门负责"能不能走"的决策；G1/G2/GA 由 PR 评审承载，G5 由 environment 审批承载，所有决策另有门记录落仓。

### 9.2 G5 与 Release BOM

三个 PBI 全部 done 后，staging 上的集成增量已验证。赵稳起草发布记录 `docs/delivery/releases/20261018-v0.1.0.md`（Release BOM：monorepo 只有本仓，钉住 tag 与 commit）：

```markdown
# Release v0.1.0 — 2026-10-18

## 内容
- PBI-0001 添加待办 / PBI-0002 完成切换 / PBI-0003 删除待办（G4 均已 go）

## BOM
- minitodo（本仓）: tag v0.1.0, commit f4e5d6c

## 类生产验证
staging（main@f4e5d6c）全量回归通过：三个 PBI 的 9 条 AC 抽查复验 pass（赵稳，10-18）。

## 发布说明（用户可见）
MiniTodo 首个版本：打开即用记录待办，支持添加、完成切换、删除，数据保存在本机浏览器。

## 回滚方案
重新执行上一稳定 tag 的 deploy-production workflow（本版本为首版，兜底为下线静态文件）；
或 git revert 后打 v0.1.1。静态站点多版本共存成本低，回滚耗时可忽略。
```

林岚对照 G5 判据（集成增量已在类生产环境验证；发布说明已写；回滚方案已录；持久制品已提交）做决策。门记录落盘：

`docs/delivery/gates/20261018-g5-release-v0.1.0.yaml`：

```yaml
id: GATE-RECORD-0012
gate: G5
artifact: docs/delivery/releases/20261018-v0.1.0.md
decision: go
criteria_met: [increment-verified, release-notes, rollback-plan, durable-artifacts-committed]
criteria_failed: []
decided_by: 林岚
role: product-owner
date: 2026-10-18
recycle_target: ""
follow_up: []
notes: 首版发布；4 周后按 Product Brief 成功信号复盘使用数据。
```

**发布动作**：agent 直推 main 提交发布记录与门记录 → 赵稳确认后由 agent 打 tag：

```bash
git tag v0.1.0 && git push origin v0.1.0
```

tag 触发 deploy-production workflow，停在 environment 审批；林岚在 GitHub 上 approve（与门记录互为印证），生产部署执行，Release 页生成制品包。**v0.1.0 上线，全程 10 天。**

## 10. 角色 × 阶段速查

| 角色 | 本案例中实际做了什么 |
|---|---|
| PO（林岚） | 主导 Discovery/PRD/Backlog/精炼；决策 G1、G2、G5（人工门）；修订 PBI-0002 被 G3 打回的 AC；approve production deployment |
| Designer（陈实兼） | 产出 3 个 PBI 的 UX 线框与交互约定（G3 design-ready 输入） |
| Architect（陈实兼） | 产出薄架构基线；决策 GA（人工门）；参与 G3 共同决策 |
| Developer（陈实兼） | 产出技术设计与 Task DAG；实现 9 个 Task；代码评审 |
| QA（赵稳兼） | 分支预览环境逐条验证 9 条 AC、staging 集成复验；产出证据文件；参与 G4 共同决策；裁剪并勾选 DoD |
| DevOps（赵稳兼） | 平台配置（分支保护/environments）；三个 workflow；staging/production 部署与 tag 发布 |
| Scrum Master | 本案例未选 Scrum，无此角色 |
| agent | 起草全部制品与代码、执行全部 git 操作、跑 build-status.py、按角色执行 G3/G4 决策 |

## 11. Git 分支与提交规范

本节把前 10 节实际使用的命名法固化为规范。规则层（什么时候必须提交）见 `OPERATING-GUIDE.md` 提交节奏表；本节的命名模式是 monorepo 实例的推荐默认，实例可在 `.agent/local/project-context.md` 中改写。

### 分支命名

模式：`<类型>-<标识>[-<简述>]`；小写字母、数字、连字符（跨平台与工具链安全）。

| 分支 | 模式 | 本案例实例 | 生命周期 |
|---|---|---|---|
| main | 常驻唯一主干 | `main` | 保持可发布；受保护 |
| 门评审分支 | `<gate>-<制品>` | `g1-product-brief`、`g2-prd`、`ga-baseline` | 随 PR 合并删除 |
| Task 分支 | `task-<id>-<slug>` | `task-0001-page-skeleton`、`task-0002-add-logic` | G4 go 合并后删除 |
| 返工 | 不开新分支 | G4 recycle 后回到原 Task 分支继续提交 | 随原分支 |
| 发布分支 | 本案例无：发布记录直推 main，G5 由 environment 审批承载；若改用 PR 承载 G5，则 `g5-release-v<x.y.z>` | — | — |
| 模板升级分支 | `template-upgrade-<version>` | `template-upgrade-v0.5`（场景见第 13 节） | merge 后删除；PR 正好承载升级前的 diff 审视 |

注：main 分支保护对人工门 PR 生效；agent 执行 G3/G4 滚动门直推时，平台侧需给 agent 账号配置 bypass 权限（或允许指定 actor 直推），规则本身不变。

### 提交信息

模式：`<锚点> <动作>：<内容>`；中文一句话，不超过 72 字符。锚点前置，使 `git log --grep` 可按 Task/PBI/门追溯 —— 锚点是追溯链的一环：提交 ↔ Task ↔ PBI ↔ 门记录互相定位。

| 场景 | 模式 | 本案例实例 |
|---|---|---|
| Task 实现 | `TASK-<id> <内容>` | `TASK-0001 页面骨架：输入区与列表容器` |
| PBI 制品 | `PBI-<id> <动作>：<内容>` | `PBI-0001 精炼：补全验收标准与技术设计引用` |
| 门放行 | `<GATE> go：<制品> + 门记录 + status.md` | `G1 go：product-brief + 门记录 + status.md` |
| 门打回 | `<GATE> recycle：<制品> <未过判据>` | `G3 recycle：PBI-0002 ac-verifiable 未过` |
| 发布 | `Release v<x.y.z>：<内容>` | `Release v0.1.0：发布记录 + G5 门记录 + status.md` |
| 杂项 | `chore：<内容>` | `chore：实例化模板基线 v0.4`、`chore：模板升级 v0.4 → v0.5` |

硬规则：

1. 门事件提交必须同包门记录与重新生成的 `status.md`（运转规则第 3、5 条）。
2. 一个提交一个意图；实现按 Task 粒度提交（提交节奏表）。
3. recycle 与 go 同样提交 —— 打回历史是 Retrospective 的输入，不是该隐藏的东西。

## 12. 全程 git 历史

```text
f4e5d6c  Release v0.1.0：发布记录 + G5 门记录 + status.md
9c8b7a6  PBI-0003 done：G4 门记录 + 合并 task-0007~0009（证据齐备）
8d7c6b5  PBI-0002 done：G4 门记录 + 合并 task-0004~0006
7a6b5c4  PBI-0001 done：G4 门记录 + 合并 task-0001~0003
6b5a493  TASK-0008/0009 删除逻辑与样式（task-0007~0009 分支提交略）
5a49382  PBI-0002 G3 go（修订后重评）+ PBI-0003 G3 go + Task DAG
4a38271  PBI-0001 G3 go：精炼 PBI + UX + 技术设计 + Task DAG
3b27160  PBI-0002 G3 recycle：ac-verifiable 未过，打回 feature-refinement
2a16059  PBI-0001~0003 草稿：FEAT-001 待办列表管理
1f05e48  GA go：架构基线 + 门记录 + status.md（PR #3）
0e59d37  G2 go：PRD 七节 + 门记录 + status.md（PR #2）
d48c426  G1 go：product-brief + 门记录 + status.md（PR #1）
c37b315  实例化：模板基线 v0.4 + project-context.md + workflows
```

对照提交节奏表：门决策后必提交（含 recycle）；无门制品落盘即提交；实现按 Task 粒度在短分支提交；每次门事件后 status.md 一并重生成。

## 13. 本案例未演示的部分

- **Scrum 形态**：第 3 节后改走 07-scrum-refinement → 08-sprint-planning（≈ 批量 G3）→ 12-sprint-review（≈ 批量 G4）→ 13-retrospective；Sprint 实例存 `docs/delivery/sprints/`（模板 `.agent/templates/sprint.yaml`）。详见 `OPERATING-GUIDE.md` Scrum 形态节。
- **三层多仓**：存在跨组件 PBI、多团队协作时拆交付仓/组件代码仓；Task 用 `affected_repositories` 点名仓库，Release BOM 钉住各仓 tag/commit。详见多仓语义节。
- **模板升级**：`git fetch template` → diff 审视 → merge，冲突趋零机制见模板升级节。
- **hold / GB(ADR) / checkpoint**：外部条件挂起、架构演进决策、长会话中断恢复，分别见 `.agent/gates/gates.yaml`、`.agent/templates/adr.md`、`.agent/templates/checkpoint.md` 与运转规则节。
