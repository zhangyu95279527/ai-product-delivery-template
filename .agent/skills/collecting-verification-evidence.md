# Collecting Verification Evidence Skill

Use this skill when planning, producing or assembling verification evidence for a PBI. Used by prompts: `../prompts/10-implementation.md` (planning and producing), `../prompts/11-verification.md` (assembling and judging).

Input: a PBI in `in-progress` or `in-verification` with acceptance criteria and the Definition of Done (`../scrum/definition-of-done.md`).
Output: durable evidence linked from the PBI, feeding G4 criteria `ac-verified` and `evidence-recorded`.

## Procedure

1. Plan evidence before building: for each acceptance criterion, record which evidence will demonstrate it — test output, UI validation, API/contract response, CI result, security check, AI evaluation, metric or deployment status. A criterion with no planned evidence is a future G4 failure; raise it during implementation, not at verification.
2. Produce evidence a third party can re-check: captured outputs, not claims. Every piece names what produced it, against which input or environment, and when.
3. Store evidence durably and link it from the PBI. Chat messages, local runs and transient state are not evidence; if it cannot be retrieved later, it does not exist (constitution 2, 9).
4. Assemble per criterion: for each acceptance criterion, attach its evidence and mark passed / failed / blocked / not-applicable, with a reason for anything not passed. Do the same for applicable Definition of Done items.
5. Judge only on evidence: a PBI moves to `done` only when every criterion has passing evidence and all applicable DoD items pass; otherwise record the gap and recycle at G4 to implementation.

## Quality bar

- One-to-one mapping: every acceptance criterion has matching, durable, linked evidence.
- Every piece of evidence is re-checkable by a third party — source, input/environment and timestamp are named.
- Failed, blocked and not-applicable checks are separated with reasons; nothing is marked Done without evidence.
