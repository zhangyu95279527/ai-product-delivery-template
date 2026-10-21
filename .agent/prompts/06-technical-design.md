# Feature Technical Design Prompt

"Using the Feature/PBI contract, UX/UI, Architecture Baseline and Impact findings, design the smallest technical slice required. Define contracts, data changes, affected components/services, affected repositories, integrations, security, observability, failure behavior and test strategy as applicable. If the baseline is insufficient, trigger Architecture Evolution instead of silently changing it."

Gate context: input = Architecture Baseline approved at gate GA plus the refined PBI; output = Feature Technical Design feeding G3 criterion tech-design-ready. Baseline gaps route to gate GB, never silent change.

Git: G3 is a rolling gate; push the Feature Technical Design directly to main with commit anchor PBI-<id>; baseline gaps route to gate GB as an ADR PR, never silent change.

Context:
- Fixed read: `AGENTS.md`.
- On demand: `docs/delivery/status.md`, `docs/architecture/architecture-baseline.md`, the selected PBI in `docs/features/` and the paths in its `references`; ADRs in `docs/architecture/adr/` only when referenced.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.