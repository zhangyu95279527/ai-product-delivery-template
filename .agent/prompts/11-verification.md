# Verification Prompt

"Verify the selected PBI against acceptance criteria and Definition of Done. Use objective evidence from tests, UI validation, contracts, CI, security checks, AI evaluations and deployment status as applicable. Separate passed, failed, blocked and not-applicable checks. Do not mark Done without evidence."

Gate context: input = PBI in status in-verification with implementation evidence; output = verification results deciding gate G4 (done). A failed G4 recycles to implementation.

Git: G4 is a rolling gate; push verification evidence and gate records directly to main with commit anchor G4 go / G4 recycle, gate record and regenerated status.md in the same commit; a failed G4 recycles the Task on its existing branch.

Context:
- Fixed read: `AGENTS.md` and the skill file below.
- On demand: the selected PBI in `docs/features/`, the paths in its `references`, the linked verification evidence, `.agent/scrum/definition-of-done.md`, `.agent/gates/gates.yaml` (G4 criteria), `.agent/templates/gate-record.yaml`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.

Skills: ../skills/collecting-verification-evidence.md