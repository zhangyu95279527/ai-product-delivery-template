# Skills

Skills are reusable capability handbooks. Prompts in `../prompts/` are per-stage session protocols; a prompt names the skills it uses on its `Skills:` line, and a skill may also be applied on its own outside any standard stage. Skills are added by capability, not by pipeline stage — do not create one skill per prompt.

Implemented:

- `writing-acceptance-criteria.md` — verifiable acceptance criteria; feeds G3 criterion `ac-verifiable`
- `decomposing-tasks.md` — Task DAG decomposition from acceptance criteria; feeds G3 criteria `tasks-decomposed` and `dependencies-confirmed`
- `collecting-verification-evidence.md` — durable per-criterion verification evidence; feeds G4 criteria `ac-verified` and `evidence-recorded`

Add further skills when a real project needs them and the capability is reusable across stages (e.g. splitting oversized PBIs, UX/UI specification, technical-design authoring). Keep each skill small and task-oriented.
