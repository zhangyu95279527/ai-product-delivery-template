# Instantiate Prompt

Role: Project setup assistant

"This repository is a fresh copy of the AI Product Delivery Template. Instantiate it for one product. Protocol:

1. Collect the minimum setup facts in ONE batch of questions, nothing else:
   - Product name and a one-line description.
   - Product type: internet product / internal tool / platform service.
   - Delivery method: generic iterative (default) or Scrum.
   - Team roster: each member's name and role(s) from PO | Designer | Architect | Developer | QA | DevOps | Scrum Master.
   - Repository layout: monorepo (default) or separate delivery repo + component repos.
2. Apply defaults for anything the user skips, and state the defaults you applied.
3. Write the instance files:
   - Fill `PROJECT-PROFILE.yaml`: product name, type, delivery method.
   - Create `.agent/local/project-context.md`: product background, conventions and terminology gathered above.
   - Copy `.agent/templates/team.yaml` to `.agent/local/team.yaml` and fill in the roster.
   - Run `python scripts/build-status.py` to generate the first `docs/delivery/status.md`.
4. List the platform steps the user must do by hand, since you cannot: create and push the remote repository, protect the main branch, map required reviewers to the human gates G1/G2/G5/GA/GB, set up CI to run `python scripts/build-status.py` on push.
5. Do not modify anything under `.agent/` except `.agent/local/`. Do not start discovery in this session.
6. Finish by telling the user: open a new session, paste `.agent/prompts/00-discovery.md`, and bring the product idea.

Gate context: originating session, no input gate; outputs = `PROJECT-PROFILE.yaml`, `.agent/local/project-context.md`, `.agent/local/team.yaml`, `docs/delivery/status.md`."

Context:
- Fixed read: `AGENTS.md`.
- On demand: `PROJECT-PROFILE.yaml`, `.agent/templates/team.yaml`, `.agent/local/README.md`.
- Do not read: `EXAMPLE.md` or `OPERATING-GUIDE.md`; never sweep `docs/` wholesale, search to locate anything not listed.
