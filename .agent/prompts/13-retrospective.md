# Retrospective Prompt

"Analyze Sprint evidence: cycle time, blocked work, rework, CI failures, defects, context problems, agent retries and collaboration friction. Separate facts from hypotheses. Propose a small set of experiments for the next Sprint. The team decides which improvements to adopt."

Gate context: no artifact gate; this event inspects the gate system itself (criteria too lax or strict, recycle patterns) using gate records in docs/delivery/gates/ as evidence.

Context:
- Fixed read: `AGENTS.md`.
- On demand: `docs/delivery/status.md`, all gate records in `docs/delivery/gates/`, all sprints in `docs/delivery/sprints/` (this stage's evidence base is delivery data).
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.