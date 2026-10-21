# Sprint Planning Prompt

"Help the Scrum Team prepare Sprint Planning around Why, What and How. Propose a Sprint Goal and candidate PBIs based on the ordered backlog, capacity and evidence. Then help create a Sprint Backlog and initial Task DAG. Do not claim a human commitment."

Gate context: input = refined PBIs; output = Sprint Backlog with initial Task DAG. This event realizes gate G3 as a batch decision for the selected PBIs; record gate results in docs/delivery/gates/.

Git: G3 is realized here as a batch rolling gate; push the sprint backlog and gate records directly to main with commit anchor G3 go / G3 recycle, gate record and regenerated status.md in the same commit.

Context:
- Fixed read: `AGENTS.md`.
- On demand: candidate PBIs in `docs/features/`, `.agent/scrum/sprint.md`, `.agent/templates/sprint.yaml`, `.agent/gates/gates.yaml` (G3 criteria), `.agent/templates/gate-record.yaml`, past sprints in `docs/delivery/sprints/`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.