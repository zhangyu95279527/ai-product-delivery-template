# Scrum Backlog Refinement Prompt

"Refine the selected PBIs for possible Sprint selection. Clarify value, acceptance criteria, dependencies, UX/UI needs, technical uncertainty and forecasting information used by the team. Split oversized items. Do not turn every PBI into detailed engineering tasks before Sprint Planning."

Gate context: rolling preparation toward gate G3 (ready); output = PBIs approaching ready state. Sprint Planning realizes G3 as a batch decision.

Git: G3 is a rolling gate; push refined PBIs directly to main with commit anchor PBI-<id>; gate events use anchor G3 go / G3 recycle.

Context:
- Fixed read: `AGENTS.md` and the skill file below.
- On demand: the selected PBIs in `docs/features/`, the paths in their `references`, and only the PRD section files relevant to them.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.

Skills: ../skills/writing-acceptance-criteria.md