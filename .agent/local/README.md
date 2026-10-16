# .agent/local/

本目录归产品实例所有。模板承诺永不在此目录放置文件，模板升级不会与本目录产生冲突。

实例可在此放置：

- `project-context.md`：项目级约定、背景、术语，作为 agent 会话的项目上下文
- `gate-criteria.md`：项目级附加门判据，对 `.agent/gates/gates.yaml` 的补充，由 agent 在门评审时一并执行
- 其他实例专属配置

原则：实例级定制只放本目录与 `docs/`，不要修改模板域文件（`.agent/` 其余部分、`AGENTS.md`、`OPERATING-GUIDE.md`、`TEMPLATE-VERSION`），这样模板升级冲突趋零。
