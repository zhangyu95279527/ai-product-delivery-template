# Architecture Prompt

Mode: Discovery | Baseline | Impact | Evolution.

"Use only the selected mode. Discovery reduces material uncertainty. Baseline defines stable current boundaries. Impact identifies affected components/services/data/contracts for a Feature/PBI. Evolution evaluates a durable architectural change. Do not create components/services/repositories just to look enterprise-grade. Record trade-offs and stop for material human decisions."

Gate context: Discovery/Baseline modes produce architecture-baseline.md for gate GA (human decision); Evolution mode produces an ADR for gate GB (human decision); Impact mode feeds Feature Technical Design and G3 criterion tech-design-ready.

Git: GA and GB are human gates carried by PRs on branches ga-baseline and gb-<adr-slug>; commit anchor GA go / GA recycle or GB go / GB recycle with the gate record and regenerated status.md in the same commit; Impact-mode notes are rolling artifacts pushed directly to main.

Context:
- Fixed read: `AGENTS.md`.
- On demand: `docs/architecture/architecture-baseline.md`; Discovery mode adds `docs/product/product-brief.md`; Impact mode adds the selected PBI in `docs/features/`; Evolution mode adds the target ADR in `docs/architecture/adr/`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.