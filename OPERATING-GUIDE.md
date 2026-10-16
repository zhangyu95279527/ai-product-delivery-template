# 运行指南（Operating Guide）

## 术语约定

本仓库正文使用中文，以下术语保留英文原词，全仓库统一使用：

- gate = 门：挂在制品上的质量检查点（G1-G5 / GA / GB）
- 门决策：go（放行）/ recycle（打回）/ hold（挂起）
- handoff = 交接：制品按门记录在角色之间移交，无需开会
- artifact = 制品：持久化文档，是项目记忆的唯一载体
- ungated artifact = 无门制品：不设门的辅助文档
- living = 活文档：持续演进、随证据更新的制品状态

PRD、PBI、Feature、Task、Sprint、Product Goal、Product Backlog、Sprint Goal、Sprint Backlog、Definition of Done 等行业标准词保持英文。

## 通用生命周期

```text
Discovery
  ↓
Product Brief
  ↓
Living PRD
  ↓
Roadmap / Backlog
  ↓
Architecture Discovery (when needed)
  ↓
Architecture Baseline
  ↓
Feature / PBI Refinement
  ↓
UX/UI + Technical Design
  ↓
Task DAG
  ↓
Implementation
  ↓
Verification / Convergence
  ↓
Release
  ↓
Operate / Feedback
  └────→ Product Backlog / PRD / Architecture
```

这是一个控制模型，不是瀑布模型。上游制品可以基于证据持续演进。

## Scrum 形态

```text
Product Goal
  ↓
Product Backlog
  ↓
Backlog Refinement
  ↓
Sprint Planning
  ↓
Sprint Goal + Sprint Backlog
  ↓
Task DAG / Execution
  ↓
Done Increment
  ↓
Sprint Review
  ↓
Retrospective
  ↓
Product Backlog
```

当前官方 Scrum Guide 为 2020 年 11 月版。它将 Product Goal、Product Backlog、Sprint Goal、Sprint Backlog 与 Definition of Done 定义为 Scrum 各制品所关联的承诺；refinement 是持续进行的，Sprint Planning 回答 Why、What、How 三个问题。

## 启动一个产品

用法本质：每个阶段开一个新会话，把对应提示词贴给 agent；agent 按提示词产出制品；制品过门后进入下一阶段。提示词在 `.agent/prompts/`，编号即阶段顺序；提示词主体是一段可以直接粘贴的指令。

首次使用前：

- 把 `AGENTS.md` 设为项目级常驻指令（IDE 规则区或会话开头引用）。
- 人通读本指南与 `.agent/constitution.md`。

通用路径（不选 Scrum）：

| 顺序 | 新会话提示词 | 产出制品 | 门（决策者） | 提交点 |
|---|---|---|---|---|
| 1 | [00-discovery](.agent/prompts/00-discovery.md) | `docs/product/product-brief.md` | G1（人） | 过门后 |
| 2 | [01-prd](.agent/prompts/01-prd.md) | `docs/product/prd/` 各分节 | G2（人） | 过门后 |
| 3 | [02-backlog](.agent/prompts/02-backlog.md) | PBI 草稿（`docs/features/`） | G3 输入 | 草稿落盘即提交 |
| 4 | [05-architecture](.agent/prompts/05-architecture.md)（按需） | `architecture-baseline.md` / ADR | GA / GB（人） | 过门后 |
| 5 | [03](.agent/prompts/03-feature-refinement.md) → [04](.agent/prompts/04-ux-ui.md) → [06](.agent/prompts/06-technical-design.md) | 精炼 PBI（验收标准 + UX/UI + 技术设计） | G3（PO+Architect） | 过门后 |
| 6 | [09-task-planning](.agent/prompts/09-task-planning.md) | Task DAG | G3 判据 | 随 PBI 一起 |
| 7 | [10](.agent/prompts/10-implementation.md) → [11](.agent/prompts/11-verification.md) | 代码增量 + 验证证据 | G4（QA+PO） | 见 Git 节 |
| 8 | 发布 | Release | G5（人） | 过门后 |

说明：

- 第 5 步的三个提示词按 PBI 逐个进行，可交叉可并行，G3 统一评判；写验收标准、任务分解、证据收集时 agent 会自动加载 `.agent/skills/` 下对应能力。
- 第 4 步在需要降低不确定性时随时插入；基线变更走 GA，持久架构演进走 GB（ADR）。
- 强制人工门：G1、G2、G5、GA、GB；G3/G4 可由 agent 按角色滚动执行，一天可过多个 PBI。

选 Scrum 时：第 3 步之后改走 [07-scrum-refinement](.agent/prompts/07-scrum-refinement.md) → [08-sprint-planning](.agent/prompts/08-sprint-planning.md)（≈ 批量 G3）→ 09-11 → [12-sprint-review](.agent/prompts/12-sprint-review.md)（≈ 批量 G4）→ [13-retrospective](.agent/prompts/13-retrospective.md)。Scrum 事件实现门，不是平行治理层；PBI 格式见 `.agent/scrum/pbi-model.md`。

最小第一步：开新会话，粘贴 `00-discovery.md` 的指令段，附上你的产品想法；agent 产出 Product Brief 草稿，人审后做 G1 决策，体系即开始运转。

完整走查示例：[EXAMPLE.md](EXAMPLE.md) 用 MiniTodo（纯静态待办应用，monorepo，10 天）演示从产品想法到 v0.1 发布的全过程：每阶段谁做什么、制品实例、门记录、git 提交与 CI/CD。实例化后可删除该文件。

## 运转规则

1. **一个提示词 = 一个会话。** 不跨阶段携带聊天记录；会话上下文只从提示词 `Gate context:` 指定的制品读取。制品是项目记忆，聊天不是。
2. **长会话落 checkpoint。** 按 `.agent/templates/checkpoint.md` 写入中断点，存 `docs/delivery/checkpoints/`；续接从 checkpoint + 制品恢复，不回翻聊天记录。
3. **门决策必须落记录。** 用 `.agent/templates/gate-record.yaml`，存 `docs/delivery/gates/`，命名 `YYYYMMDD-<gate>-<artifact>.yaml`；只追加不修改，改决策就是一条新记录。下游角色只认过门记录，聊天承诺不算数。
4. **recycle 是正常迭代。** 同一制品在同一门以同一判据被打回两次或以上，是系统性问题信号（判据、提示词或上游制品质量），成为 Retrospective 输入，任何角色都可以提出。
5. **状态永远自动生成。** 每次门事件后运行 `python scripts/build-status.py` 重新生成 `docs/delivery/status.md`（由制品状态与门记录派生的只读视图）；不手工维护任何状态看板。

## Git 与仓库结构

原则（详见 `AGENTS.md`）：main 保持可发布；有意义的变更用短生命周期分支；提交持久制品与完成的增量；绝不提交秘密或私有数据。

### 仓库结构

多组件、多团队产品采用三层结构：

- **模板仓**：本仓库，承载方法论，持续迭代并打版本 tag（版本见 `TEMPLATE-VERSION`）。
- **产品交付仓**：每个产品一个，含 `AGENTS.md`、`.agent/`、`docs/`，是项目记忆唯一真源，不放代码。
- **组件代码仓 × N**：各角色团队自有仓库，独立分支策略与 CI/CD。

适用边界：单服务、小团队的小产品直接用 monorepo —— 模板实例化后代码与制品同仓，交付仓即代码仓。存在跨组件 PBI、多团队协作时才拆三层。

### 目录所有权

| 域 | 内容 | 模板升级时 |
|---|---|---|
| 模板域 | `.agent/`（除 `local/`）、`AGENTS.md`、`OPERATING-GUIDE.md`、`EXAMPLE.md`、`TEMPLATE-VERSION` | 接受模板侧新版 |
| 实例域 | `docs/`、`.agent/local/`、代码 | 模板永不覆盖 |

实例级约定与策略（项目上下文、附加门判据）一律放 `.agent/local/`，不要修改模板域文件，模板升级冲突由此趋零。

### 实例化

建仓命令（平台无关）：

```bash
git clone <template-url> my-product-delivery
cd my-product-delivery
git remote rename origin template
git remote add origin <实例仓URL>
git push -u origin main
```

实例化清单：

1. 执行上述命令；`TEMPLATE-VERSION` 随 clone 带过来，即为实例的模板基线版本。
2. 在 `.agent/local/` 建 `project-context.md`，写项目约定与背景。
3. 平台配置：main 分支保护；required reviewers 映射 G1/G2/G5/GA/GB 的责任人（人工门由 PR 评审承载）；按团队划分交付仓与代码仓权限（PRD 可能商业敏感）。
4. 配置 CI（推荐）：push 时自动运行 `python scripts/build-status.py` 做体系自检，不依赖人记得跑脚本。
5. 组件代码仓 URL 登记到 `architecture-baseline.md` 的"主要组件/服务"节，作为组件注册表单真源。

### 操作规则

- git 操作一律由 agent 代劳（提交、分支、PR、合并）；人只做两件事：审内容、做门决策（go / recycle / hold）。
- 人工门（G1/G2/G5/GA/GB）由交付仓短分支 + PR 评审承载，制品与门记录随 PR 落盘，评审痕迹即平台级审计；G3/G4 滚动门由 agent 直推 main。
- 制品形态：交付仓只放文本制品；二进制与外部资产（Figma、设计源文件、截图、录屏、大文件）存外部存储，仓内放指针（链接 + 一句话说明）。
- 门评审设时间盒（建议 48 小时），超时由责任人升级处理，避免门成为迭代瓶颈。
- 本地布局：交付仓与代码仓 checkout 在同一父目录下，IDE 用多根工作区同时挂载，实现会话可同屏读交付仓制品、写代码仓代码。

### 提交节奏

| 时机 | 提交内容 |
|---|---|
| 仓库初始化 | 模板基线（首次提交建立运行基线，见实例化） |
| 门决策后 | 制品 + 门记录 + 重新生成的 `status.md` 一并提交；recycle 同样提交（记录即沟通） |
| 无门制品完成时 | PBI 草稿、验收标准、UX/UI、技术设计、Task DAG 落盘即提交 |
| 实现期间 | 按 Task 粒度在代码仓短分支提交；带齐 G4 证据后合并回 main |
| 会话中断前 | checkpoint |
| Sprint 边界（选 Scrum 时） | Sprint 实例（`docs/delivery/sprints/`，模板为 `.agent/templates/sprint.yaml`）与 Sprint 门记录 |
| 模板升级后 | merge 提交（含 `TEMPLATE-VERSION` 更新） |

### 模板升级

低频执行，先审视后合并：

```bash
git fetch template
git diff template/<基线tag>..template/main -- .agent/ AGENTS.md OPERATING-GUIDE.md
git merge template/main
```

冲突只会出现在实例改过的模板域文件；遵守目录所有权规则后冲突趋零。升级后按提交节奏表提交 merge。

模板演进纪律（模板侧承诺）：

- 以只增不改为原则；修改既有文件时在提交说明中写清迁移要点。
- 每次发布更新 `TEMPLATE-VERSION` 并打同名 tag。
- 永不写入 `.agent/local/`；`docs/` 骨架变更不假设实例未填内容。

### 多仓语义

- Task 用 `affected_repositories` / `affected_components` 字段点名受影响仓库与组件；G4 的 `ac-verified` 语义为"该 PBI 所有受影响仓库的变更全部合并且证据齐备"，任一仓未完成则 PBI 不进 done。
- 不存在跨仓事务；合并顺序由 Task DAG 依赖驱动，门检查是唯一一致性保障。
- Release BOM：G5 过门时，`docs/delivery/releases/` 的发布记录钉住各组件仓的 tag/commit，多仓产品的发布内容由此可追。

### 已知限制

跨产品组合视图缺失：一人管多个产品时需分别查看各交付仓的 `status.md`；面向管理层的聚合展示属 P5 工具适配器范围。

## 重要区分

- Product Brief = 产品为什么应该存在。
- Living PRD = 产品需要达成什么，及其当前边界。
- Product Backlog = 排好序的工作。
- Feature = 产品能力。
- PBI/User Story = 一个具体的待办结果。User Story 是常用表达，不是普遍强制要求。
- Task = 可执行的工程/设计工作。

## 架构区分

- Architecture Discovery：降低不确定性。
- Architecture Baseline：稳定的当前架构边界。
- Feature Technical Design：当前 Feature/PBI 的实现设计。
- Architecture Evolution：显式的、持久的架构变更。

## 并行工作

并行来自 Task 依赖。不要引入 Workstream 层。输入稳定且无实质依赖的 Task 可以并行执行。
