# 角色目录（Role Catalog）

角色描述的是责任，不是某个具体的人或 agent。

## 角色

- Product Manager / Product Owner（PO）：产品价值、Product Goal、PRD 与 backlog 排序。决定门 G1、G2、G5（强制人工）；与 Architect 共同决定 G3，与 QA 共同决定 G4。
- Product Designer：UX/UI 探索、交互与视觉设计。负责 G3 的 `design-ready` 输入。
- Architect：架构边界与重大技术权衡。决定门 GA、GB（强制人工）；共同决定 G3。
- Developer：实现与工程质量。负责产出 Feature Technical Design、Task DAG 与增量。
- QA/Quality Engineer：验证策略与证据。共同决定 G4。
- DevOps/Platform：交付平台、环境与运行时。执行发布。
- Scrum Master（选用 Scrum 时）：帮助团队实施 Scrum 并移除流程/系统性障碍；不拥有任何制品门，也不成为指挥团队的项目经理。

任何角色都可以由人、agent 或人+agent 承担，取决于项目策略，且重大决策由人担责（章程第 8 条）。
当 agent 承担某角色时，门记录写明该角色，被问责的人仍然负责。
强制人工门（G1、G2、G5、GA、GB）定义在 `../gates/gates.yaml`；G3/G4 决策可由承担相应角色的 agent 执行。

## 角色 × 制品矩阵

A = 对该制品负责的唯一角色；R = 产出它；C = 在其被视为完成前被咨询。
门判据与门决策者定义在 `../gates/gates.yaml`；本矩阵是责任视图，不是门判据的第二真源。

| 制品 | 门 | A | R | C |
|---|---|---|---|---|
| Product Brief | G1 | PO | PO | Architect, Designer |
| PRD + MVP scope | G2 | PO | PO | Designer, Architect, QA |
| Architecture Baseline | GA | Architect | Architect | PO, Developer, DevOps |
| ADR | GB | Architect | Architect | 受影响的 Developer, DevOps |
| Backlog order / PBI drafts | G3 输入 | PO | PO | Designer, QA, Architect |
| Acceptance criteria | G3: ac-verifiable | PO | PO | QA, Designer, Developer |
| UX/UI artifacts | G3: design-ready | Designer | Designer | PO, Developer |
| Feature Technical Design | G3: tech-design-ready | Architect | Developer | QA, DevOps |
| Task DAG | G3: tasks-decomposed | Developer | Developer | QA, PO |
| Increment (code) | G4 输入 | Developer | Developer | QA |
| Verification evidence | G4 | QA | QA | PO, Developer |
| Release | G5 | PO | DevOps | QA, Developer |
| Gate records | 全部 | 决策角色 | 决策角色 | — |

标记为 "G3/G4 输入" 或 "G3: \<判据\>" 的行是无门制品：它们没有自己的门，只作为消费方门的判据被评判。
Scrum Master 不拥有上表任何行；该角色的贡献是促成实现门的事件（Sprint Planning ≈ 批量 G3，Sprint Review ≈ 批量 G4）并移除障碍。

## 交接与拒绝规则

1. **有效输入。** 一个环节只能基于有效输入开始工作：
   - 有门制品在 `docs/delivery/gates/` 中相关门上存在 `go` 记录时有效；
   - 无门制品（验收标准、UX/UI、技术设计、Task DAG、验证证据）在被父 PBI 引用、且对照消费方门的判据实质完整时有效；其充分性只在该门被评判。
2. **拒绝即门记录。** 收到无效输入的角色不静默修复，也不在聊天中协商。它在相关门上记录 `recycle` —— `criteria_failed`、`recycle_target`、`follow_up` —— 工作回到上游角色。记录即沟通（章程第 2 条）。
3. **打回路由。** `../gates/gates.yaml` 定义每个门的 `recycle_target`。对 G3，失败的判据选择返回环节：

   | 失败判据 | 返回到 | 接收角色 |
   |---|---|---|
   | ac-verifiable | feature-refinement | PO |
   | design-ready | ux-ui | Designer |
   | tech-design-ready | technical-design | Developer / Architect |
   | tasks-decomposed | task-planning | Developer |
   | dependencies-confirmed | 依赖所属环节，在 `follow_up` 中指名 | 按 `follow_up` |

4. **打回是常态。** 打回是迭代，不是过错。同一制品在同一门以同一判据被打回两次或以上，说明存在系统性问题 —— 判据、提示词或上游制品的质量 —— 并成为 Retrospective 输入；任何角色都可以提出。
5. **hold 仅限外部。** `hold` 只用于团队控制之外的条件；`follow_up` 写明解除条件及其负责人，条件解除后由门的决策者重新召集该门。
6. **交接无需开会。** 制品加其门记录就是交接。讨论可以发生，但任何影响制品的结论必须落到该制品中（章程第 2、10 条）。
7. **禁止静默修复。** 下游绝不静默修复实质不充分的输入；那样做会掩盖打回记录本来要暴露的上游质量信号。
