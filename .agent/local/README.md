# .agent/local/

本目录归产品实例所有。模板承诺永不在此目录放置文件，模板升级不会与本目录产生冲突。

实例可在此放置：

- `project-context.md`：项目级约定、背景、术语，作为 agent 会话的项目上下文
- `team.yaml`：团队名册（人名 → 角色映射），由实例化会话从 `.agent/templates/team.yaml` 复制并填写
- `gate-criteria.md`：项目级附加门判据，对 `.agent/gates/gates.yaml` 的补充，由 agent 在门评审时一并执行
- `git-policy.yaml`：实例的平台侧 git 事实与核对清单——平台类型、远程仓、main 保护 / reviewer 映射 / CI 的确认位、允许直推 main 的账号；实例化时从 `.agent/templates/git-policy.yaml` 复制填写，须与平台实际配置保持一致
- 其他实例专属配置

原则：实例级定制只放本目录与 `docs/`，不要修改模板域文件（`.agent/` 其余部分、`AGENTS.md`、`OPERATING-GUIDE.md`、`TEMPLATE-VERSION`），这样模板升级冲突趋零。
