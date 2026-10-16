# 阶段门（Stage Gates）

阶段门是本交付系统的运行时内核。核心流程
（`Product → PRD → Feature/PBI → Task → Verification → Release`）定义*做什么*；
门定义*制品何时可以前进*以及*由谁决定*。

门挂在制品上，不挂在日历时间上。每个门守卫一个特定制品在制品生命周期中的晋级。
这使模型保持迭代：不同的门以不同的粒度和节奏运行，`recycle`（打回）是正常结果，不是失败。

## 制品生命周期

文档类制品（Product Brief、PRD、Architecture Baseline、ADR、设计文档）：

```text
draft → in-review → approved → living → superseded
```

`living`（活文档）适用于持续演进的文档（PRD、Architecture Baseline）：批准一次，
随后通过受控变更持续更新。`superseded` 标记一份已被新决策取代的文档。

执行类制品（PBI、Task）：

```text
draft → ready → in-progress → in-verification → done
```

门决策推动制品在这些状态间迁移，且必须记录。
日常执行工作（例如 `in-progress` 中的编码）不记录为门事件。

## 门模型

每个门包含：范围、守卫的制品类型、准入判据、决策者、是否强制人工决策。
完整的机器可读定义见 `gates.yaml`。

决策取值：

- `go` —— 制品晋级；下游环节可以消费它。
- `recycle` —— 制品带着后续行动项打回到指定的上游环节。
- `hold` —— 因外部条件暂停晋级；后续记录写明什么条件解除它。

每次决策生成一份仅可追加的记录，模板为 `../templates/gate-record.yaml`，
存放于 `docs/delivery/gates/`，命名 `YYYYMMDD-<gate>-<artifact>.yaml`。
记录事后绝不修改；决策变更就是一条新记录。

## 门清单

| 门 | 名称 | 守卫对象 | 节奏 | 决策者 | 强制人工 |
|------|------|--------|---------|----------------|----------------|
| G1 | Charter | Product Brief | 每个产品一次，可重开 | Product Owner | yes |
| G2 | PRD | PRD + MVP 范围 | 每个产品版本 | Product Owner | yes |
| G3 | Ready (DoR) | 每个 PBI | 滚动 | PO + Architect | no |
| G4 | Done (DoD) | 每个 PBI | 滚动 | QA + PO | no |
| G5 | Release | 每个 Release | 按需 | Product Owner | yes |
| GA | Architecture Baseline | 基线 | 基线变更时 | Architect | yes |
| GB | Architecture Evolution | 每个 ADR | 每个 ADR | Architect | yes |

G3 与 G4 按 PBI 持续滚动：团队一天之内可以让多个 PBI 通过这些门，没有批量等待。
G3/G4 决策可由承担相应角色的 agent 按项目策略执行；被问责的角色仍对决策负责。

## 人工决策点

强制人工决策：G1、G2、G5、GA、GB，以及任何涉及安全或重大成本的 ADR。
这份清单是章程第 8 条的具体化。其余一切可以由 agent 自主流转。

## 交接规则

角色之间唯一合法的交接形式，是已经通过其门的上游制品。下游角色收到未过门的输入时，
通过在相关门上记录 `recycle` 来拒绝它 —— 不需要协商层。

操作细节 —— 有效输入定义、拒绝程序、打回路由与升级 —— 见 `../roles/role-catalog.md`。

## 与 Scrum 事件的关系

当 `delivery.method: scrum` 时，Scrum 事件*实现*门，而不是增加一个平行的治理层：

- Sprint Planning ≈ 对入选 PBI 的批量 G3，外加 Sprint Goal 承诺。
- Sprint Review ≈ 批量 G4，外加与干系人一起检视增量。
- Retrospective 检视门判据本身：太松、太严、缺失。
