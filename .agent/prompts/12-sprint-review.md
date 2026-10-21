# Sprint Review Prompt

"Prepare a Sprint Review pack from completed Increment evidence. Summarize Sprint Goal, completed PBIs, acceptance evidence, known gaps, product metrics and stakeholder/user feedback. Suggest backlog updates from evidence, but do not make product-priority decisions for humans."

Gate context: this event realizes gate G4 as a batch review of completed PBIs and the Increment; the review pack is the evidence input for release gate G5 (human decision).

Git: G4 is realized here as a batch rolling gate; push the review pack and gate records directly to main with commit anchor G4 go; a passed G5 tags main with the release semver and lands a release record in docs/delivery/releases/.

Context:
- Fixed read: `AGENTS.md`.
- On demand: the sprint file in `docs/delivery/sprints/`, its PBIs in `docs/features/` and their evidence links, `.agent/scrum/definition-of-done.md`, `.agent/gates/gates.yaml` (G4 criteria), `.agent/templates/gate-record.yaml`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.