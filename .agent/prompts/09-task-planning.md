# Task Planning Prompt

"Decompose the selected PBI into small, reviewable Tasks. Each Task states outcome, inputs, dependencies, allowed scope, affected repository/component references, verification and done evidence. Write the exact file paths needed to execute each Task into its `inputs`; the executor reads only those. Prefer independent tasks that can safely run in parallel. Do not create a Workstream layer."

Gate context: input = refined PBI (pre-G3); output = Task DAG feeding G3 criterion tasks-decomposed. New Tasks start at status: draft.

Context:
- Fixed read: `AGENTS.md` and the skill file below.
- On demand: the selected PBI in `docs/features/`, the paths in its `references` (UX/UI, technical design), `.agent/templates/task.yaml`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.

Skills: ../skills/decomposing-tasks.md