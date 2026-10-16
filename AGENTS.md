# AI Product Delivery Project Instructions

This system exists for one purpose: agents help each role do its own job and deliver. Every mechanism here serves that purpose; anything that does not is removed.

## Core model
This repository uses a universal delivery model. Scrum is a selectable delivery method, not the universal process. Coding agents are executors, not the methodology.

Canonical core flow:
`Product → PRD → Feature/PBI → Task → Verification → Release`

Do not introduce artificial workflow layers merely to organize people.

## Architecture
Architecture Discovery reduces material uncertainty. Architecture Baseline defines stable current boundaries. Feature Technical Design applies that baseline to a current Feature/PBI. Architecture Evolution changes stable architecture explicitly through review/ADR.

Component/Service/Repository are engineering references, not mandatory workflow stages.

## Agile
The model is iterative. Discovery, PRD, design and architecture may be revisited when evidence changes the product or technical understanding.

If Scrum is selected, use `.agent/scrum/` for Product Goal, Product Backlog, PBI/User Story, Sprint Goal, Sprint Backlog, Daily Scrum, Review, Retrospective and Definition of Done.

## Agent behavior
Before acting: identify stage/artifact/task; read only required context; separate confirmed facts, assumptions, options and open questions; state intended outputs and stop conditions.

During work: ask only material blocking questions; keep assumptions explicit; avoid unrelated refactors; keep changes reviewable.

Before completion: report changed artifacts/files, verification evidence, unmet acceptance criteria, unresolved risks/questions, and checkpoint state for long-running work.

Context discipline:
- One prompt scopes one session; do not carry one stage's chat into another stage.
- Read only the artifacts named by the prompt's gate context and the task at hand. Artifacts, not chat history, are project memory.
- When work outgrows one session, write a checkpoint from `.agent/templates/checkpoint.md`; resume from the checkpoint plus the artifacts, never by re-reading chat scrollback.

## Traceability
Every implementation Task must trace to a Feature/PBI and Acceptance Criteria. A Feature may affect multiple repositories/components and one repository/component may support many Features. Record affected repositories/components on the Task when known.

## Git
- `main` stays releasable.
- Use short-lived branches for meaningful changes.
- Commit durable artifacts and completed increments.
- Never commit secrets or private data.
- Instance-specific conventions and policies live in `.agent/local/`; that directory and `docs/` belong to the product instance and are never overwritten by template updates.
