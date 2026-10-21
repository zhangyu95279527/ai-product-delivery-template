# PRD Prompt

"Using the confirmed Product Brief and discovery evidence, help me create the Living PRD. Define goals, users, journeys, functional requirements, business rules, product-relevant NFRs, MVP boundaries, out-of-scope, success metrics and open questions. Do not design APIs or databases. Mark unresolved product decisions explicitly. Stop for material product decisions."

Gate context: input = Product Brief approved at gate G1; output = Living PRD for gate G2 (human decision). Unresolved material questions block G2.

Git: G2 is a human gate carried by a PR on branch g2-prd; commit anchor G2 go / G2 recycle with the gate record and regenerated status.md in the same commit; recycle rework stays on the same branch.

Context:
- Fixed read: `AGENTS.md`.
- On demand: `docs/delivery/status.md`, `docs/product/product-brief.md`, the section files under `docs/product/prd/`, `.agent/local/project-context.md` if present.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.