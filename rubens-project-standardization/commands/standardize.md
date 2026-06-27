---
description: Bootstrap or restructure a project for AI coding agents: triage tier, then apply AGENTS.md, .agents/, docs/artifacts/, memory, CHANGELOG, STANDARDS
---

Load the `project-standardization` skill and run the full bootstrap from `references/bootstrap.md`.

1. Triage the tier (small / medium / large) from README + top-level layout. State the choice with reasoning; ask if unsure.
2. Read `references/<tier>.md` for the tier-specific layout.
3. Apply the standards stack per `references/standards-stack.md`.
4. Scaffold `AGENTS.md` from `templates/AGENTS-<tier>.md` and `CLAUDE.md` shim from `templates/CLAUDE.md`.
5. Scaffold `.agents/`, `docs/artifacts/`, memory, CHANGELOG, STANDARDS per tier.
6. Verify the auto-loaded token budget.

Stop and confirm before each destructive step.

Optional tier override: `$ARGUMENTS` (for example `small`, `medium`, `large`).