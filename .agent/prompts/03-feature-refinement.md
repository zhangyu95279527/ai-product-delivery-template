# Feature/PBI Refinement Prompt

"Refine the selected Feature/PBI. Confirm user outcome, scope, non-scope, acceptance criteria, dependencies, UX/UI needs, architecture impact, technical unknowns and risks. Identify whether it should be split. Produce/update the Feature/PBI artifact and stop when ready for design/planning or blocked by a material decision."

Gate context: input = Feature/PBI draft from the backlog; output = refined PBI with verifiable acceptance criteria, feeding G3 criterion ac-verifiable. G3 may recycle back to this stage.

Context:
- Fixed read: `AGENTS.md` and the skill file below.
- On demand: the selected PBI file in `docs/features/`, the paths in its `references`, and only the PRD section files relevant to it.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.

Skills: ../skills/writing-acceptance-criteria.md