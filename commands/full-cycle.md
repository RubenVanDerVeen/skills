---
description: Take a feature request from prompt to shipped change in one run - brainstorm (optional) > spec > plan > dispatch the orchestrator to execute, then relay its report. Single-pass, no approval gates. Use `handoff` to print the /execute-plan line for a fresh session instead.
---

Run the full pipeline for `$ARGUMENTS` in a single pass. Agent mapping: run this command as the `planner` agent when available; fall back to the current agent otherwise.

Keywords in `$ARGUMENTS`:
- `no brainstorm`: skip the brainstorm phase (spec directly).
- `handoff`: print the /execute-plan line for a fresh session instead of dispatching. Use for huge tasks where the planner's context should not carry into execution.

Steps:
1. Brainstorm (unless `no brainstorm` is present, or the request is explicit enough to spec without it): load the `brainstorming` skill; explore intent, requirements, and design. Dispatch the `explore` subagent for codebase recon.
2. Spec: write the design to `docs/artifacts/specs/<topic>/YYYY-MM-DD-<slug>-design.md` (today's date).
3. Plan: load the `writing-plans` skill; write the plan to `docs/artifacts/plans/<topic>/YYYY-MM-DD-<slug>-plan.md`, referencing the spec.
4. Execute (default): dispatch the `orchestrator` subagent with the spec and plan paths; it branches, runs executor/reviewer per task, escalates two-strike failures to `oracle`, commits at boundaries, and returns a final report. Relay that report. If `orchestrator` is unavailable, dispatch `general` with the same instructions; if no subagent dispatch is possible, fall back to step 5.
5. Handoff (only when `handoff` is present, or as the fallback): print the spec and plan paths plus `/execute-plan docs/artifacts/plans/<topic>/<file>.md` for a fresh session.

No approval gates: the run goes straight through from prompt to final report. Do not end the turn between phases to ask whether to continue; end only at the final report (or the handoff block).

Requires `subagent_depth >= 2` in opencode config so the orchestrator can dispatch executor/reviewer. If unset, the dispatch fails with "Subagent depth limit reached"; in that case fall back to step 5.
