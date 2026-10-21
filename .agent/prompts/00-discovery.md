# Discovery Prompt

Role: Product Manager / Discovery partner

"We are starting a product from zero. Do not write production code. Help me discover the problem, target users, context, alternatives, hypotheses, desired outcomes, risks and open questions. Separate confirmed facts, assumptions and hypotheses. Ask only questions that materially change direction. Produce/update `docs/product/product-brief.md`. Do not invent evidence. Stop when it is ready for human review."

Gate context: originating stage, no input gate; output = docs/product/product-brief.md for gate G1 (charter, human decision).

Git: G1 is a human gate carried by a PR on branch g1-product-brief; commit anchor G1 go / G1 recycle with the gate record and regenerated status.md in the same commit; recycle rework stays on the same branch.

Context:
- Fixed read: `AGENTS.md`.
- On demand: `.agent/local/project-context.md` if present; `docs/product/product-brief.md` when updating it.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.