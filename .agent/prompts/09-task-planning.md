# Task Planning Prompt

"Decompose the selected PBI into small, reviewable Tasks. Each Task states outcome, inputs, dependencies, allowed scope, affected repository/component references, verification and done evidence. Prefer independent tasks that can safely run in parallel. Do not create a Workstream layer."

Gate context: input = refined PBI (pre-G3); output = Task DAG feeding G3 criterion tasks-decomposed. New Tasks start at status: draft.

Skills: ../skills/decomposing-tasks.md