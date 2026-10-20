# Implementation Prompt

"Execute TASK-ID. Read AGENTS.md, then only the files listed in the Task's `inputs`; change code and tests only within the Task's `allowed_scope`. Check dependencies. Make the smallest reviewable change. Do not change product scope or architecture silently. Run relevant tests. Before completion report changed files, evidence, acceptance status and risks."

Gate context: input = Task of a G3-passed PBI (status: ready); the Task moves in-progress → in-verification and its evidence feeds gate G4.

Context:
- Fixed read: `AGENTS.md` and the skill file below.
- On demand: only the files listed in the Task's `inputs`; code and tests within the Task's `allowed_scope`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.

Skills: ../skills/collecting-verification-evidence.md