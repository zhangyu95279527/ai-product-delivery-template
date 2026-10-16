# Implementation Prompt

"Execute TASK-ID. Read AGENTS.md plus only the Task's referenced PBI, design, architecture, contracts, relevant code and tests. Check dependencies. Make the smallest reviewable change. Do not change product scope or architecture silently. Run relevant tests. Before completion report changed files, evidence, acceptance status and risks."

Gate context: input = Task of a G3-passed PBI (status: ready); the Task moves in-progress → in-verification and its evidence feeds gate G4.

Skills: ../skills/collecting-verification-evidence.md