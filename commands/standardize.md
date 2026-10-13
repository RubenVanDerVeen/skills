---
description: Bootstrap or restructure a project for AI coding agents: triage tier, then apply AGENTS.md, .agents/, docs/artifacts/, CHANGELOG, STANDARDS
---

Load the `project-standardization` skill and run the full bootstrap from `references/bootstrap.md`.

1. Triage: pick the tier (small / medium / large) from README + top-level layout, AND detect the branch. State both with reasoning; ask if unsure.
   - Fresh (`AGENTS.md` absent): run as `orchestrator` and dispatch the explore-patch-verify flow from `references/bootstrap-flow.md` (explore reads the tier reference and recon's the project, one executor per scaffold cluster, reviewer re-runs every predicate with fresh context). Steps 1 and 11 stay inline.
   - Restructure (`AGENTS.md` present): dispatch the explore-patch-verify flow from `references/restructure-flow.md` (explore audits state, executor patches gaps, reviewer re-verifies with fresh context).
2. Stop and confirm before each destructive step.

Optional tier override: `$ARGUMENTS` (for example `small`, `medium`, `large`).