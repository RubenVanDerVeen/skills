---
description: Take a feature request through brainstorm > spec > plan in one run, then hand execution to a clean session via /execute-plan. Never implements in the same session.
---

Run the design pipeline for `$ARGUMENTS` and stop at the execution boundary. This command produces an approved spec and plan; implementation happens in a fresh session with clean context (a plan written here is opened in a new session, or the session is compacted first). Do not start implementing here, even if asked to "walk through the whole process": for this command the whole process ends at the handoff.

Agent mapping: run this command as the `planner` agent when available (it pins the planning model and scopes file writes to `docs/`); fall back to the current agent otherwise.

1. **Brainstorm.** Load the `brainstorming` skill and explore intent, requirements, and design. Skip only when the request already states requirements explicitly enough to spec without guessing.
2. **Spec.** Write the design to `docs/artifacts/specs/<topic>/YYYY-MM-DD-<slug>-design.md` (today's date). Present it for approval.
3. **Plan.** Load the `writing-plans` skill. Write the implementation plan to `docs/artifacts/plans/<topic>/YYYY-MM-DD-<slug>-plan.md`, referencing the spec. Present it for approval.
4. **Hand off.** After plan approval, end with a short handoff block: the spec and plan paths, plus the exact line to paste in a fresh session: `/execute-plan docs/artifacts/plans/<topic>/<file>.md`. If the user insists on staying in this session, tell them to compact first, then run that command.

Gates: one approval after the spec, one after the plan. If the invocation says "at once" (or similar), collapse both gates and run brainstorm through handoff without stopping. Within a phase, never end the turn to ask whether to continue; turns end only at the two gates and the final handoff.
