# Writing Acceptance Criteria Skill

Use this skill when writing or refining acceptance criteria for a backlog item or PBI. Used by prompts: `../prompts/02-backlog.md`, `../prompts/03-feature-refinement.md`, `../prompts/07-scrum-refinement.md`.

Input: a backlog item or PBI draft with stated value/outcome.
Output: acceptance criteria recorded in the PBI (`acceptance_criteria` in `../templates/pbi.yaml`), feeding gate G3 criterion `ac-verifiable`.

## Procedure

1. Start from the user outcome, not the implementation. Each criterion describes observable behavior or a checkable property of the product, never internal structure.
2. Make every criterion objectively verifiable: a third party given the same input must reach the same pass/fail judgment without asking the author. A criterion passes this test only if it answers three questions — what action or input triggers it, what is observed, and where the pass/fail boundary lies.
3. Cover the normal path, boundary values and error handling. If an error case is out of scope, record that exclusion in the PBI; do not omit it silently.
4. Remove subjective wording. Words like "reasonable", "fast", "friendly" or "works correctly" fail verifiability; replace them with measurable statements (e.g. "responds within 2 s at p95 under the stated load").
5. Write each criterion so that G4 evidence can be attached later: for every criterion, name at least one conceivable piece of evidence (test output, UI check, API response, metric). If no evidence is conceivable, the criterion is not verifiable — rewrite it.
6. Keep criteria independent and minimal. Split any criterion that needs "and" to join two separate checks.

## Quality bar

- Every criterion passes the three-question test (trigger, observation, pass/fail boundary).
- No subjective or implementation-internal wording remains.
- Normal path, boundaries and error handling are covered or explicitly excluded.
- Each criterion has at least one named, durable evidence option ready for G4.
