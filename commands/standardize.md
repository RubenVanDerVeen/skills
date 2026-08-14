---
description: Bootstrap or restructure a project for AI coding agents: triage tier, then apply AGENTS.md, .agents/, docs/artifacts/, memory, CHANGELOG, STANDARDS
---

Load the `project-standardization` skill and run the full bootstrap from `references/bootstrap.md`.

1. Triage: pick the tier (small / medium / large) from README + top-level layout, AND detect the branch. State both with reasoning; ask if unsure.
   - Fresh (`AGENTS.md` absent): walk the 12 steps in `references/bootstrap.md` linearly. Run each step's `Verification:` predicate inline before moving on.
   - Restructure (`AGENTS.md` present): dispatch the explore-patch-verify flow from `references/restructure-flow.md` (explore audits state, executor patches gaps, reviewer re-verifies with fresh context).
2. Stop and confirm before each destructive step.

Optional tier override: `$ARGUMENTS` (for example `small`, `medium`, `large`).