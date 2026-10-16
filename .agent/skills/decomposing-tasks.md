# Decomposing Tasks Skill

Use this skill when decomposing a refined PBI into an executable Task DAG. Used by prompts: `../prompts/09-task-planning.md` (applies wherever Tasks are created).

Input: a refined PBI with verifiable acceptance criteria (pre-G3).
Output: Task drafts (`status: draft`) on `../templates/task.yaml`, together forming the Task DAG that feeds G3 criteria `tasks-decomposed` and `dependencies-confirmed`.

## Procedure

1. Work backwards from the acceptance criteria: enumerate what must change for each criterion to hold, then group changes into Tasks. Every Task traces to at least one acceptance criterion, and every criterion is covered by at least one Task (traceability, AGENTS.md).
2. Size each Task as the smallest reviewable change: one reviewer can judge it in one sitting, and its verification evidence is self-contained.
3. Declare only substantive dependencies: Task B depends on Task A only when B consumes an output of A. Never declare ordering preferences, team convenience or "logical flow" as dependencies — parallelism comes from Task dependencies alone (OPERATING-GUIDE, Parallel work). Do not introduce a Workstream layer.
4. Fill each Task per the template: outcome, inputs, dependencies, allowed scope, affected repository/component references (when known), verification and done evidence. Record the planned evidence now, not during verification.
5. Confirm dependencies before G3: every external dependency (third-party API, another team, an environment, a dataset) is confirmed available and the confirmation is recorded; "should be fine" fails `dependencies-confirmed`. Internal dependencies are satisfied by the DAG itself.
6. State scope limits explicitly: each Task names what it must not change. Product scope and architecture are fixed by the PBI and its design; a Task never extends them silently.

## Quality bar

- Full two-way traceability between Tasks and acceptance criteria, with no orphans on either side.
- Every dependency edge is substantive and confirmed; no convenience edges; no cycles.
- Each Task is independently reviewable and carries its planned verification evidence.
- Affected repositories/components are named where known.
