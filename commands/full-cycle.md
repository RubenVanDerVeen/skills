---
description: Take a request from prompt to shipped change in one run. Small fixes classify at intake into a quick path (one executor with an inline brief, no spec/plan/report artifacts); everything else runs brainstorm (optional) > spec > plan > dispatch the orchestrator to execute, then relay its report. Single-pass, no approval gates. Use `handoff` to print the /execute-plan line for a fresh session instead.
---

Run the full pipeline for `$ARGUMENTS` in a single pass. Agent mapping: run this command as the `planner` agent when available; fall back to the current agent otherwise.

Keywords in `$ARGUMENTS`:
- `no brainstorm`: skip the brainstorm phase (spec directly).
- `quick`: force the quick-fix fast path (one executor with an inline brief, no spec/plan/report artifacts) even when the request looks borderline.
- `full`: force the complete pipeline even when the request looks small.
- `handoff`: print the /execute-plan line for a fresh session instead of dispatching. Use for huge tasks where the planner's context should not carry into execution.

Steps:
1. Classify: quick fix or feature? Quick fix only when ALL hold: one task with one obvious fix; expected diff touches about 1-2 files; no design alternatives worth weighing, no new interface, API, behavior surface, or schema; one runnable verification check covers it; nothing that belongs in `docs/artifacts/choices/`. Any doubt means the full pipeline. Keywords `quick` and `full` override the classification either way. State the tier in one line so the user sees which path ran.
2. Quick-fix path: dispatch the `explore` subagent only when the target file or fix site is unknown; then dispatch ONE `executor` with an inline brief (branch name, target files, the fix, one verification command copied from the project's AGENTS.md). The executor commits once with Conventional Commits, adds a changelog `[Unreleased]` entry and patch version bump when the project's conventions require them, and stops and reports back on scope creep instead of expanding. No lazy-dev gate, orchestrator, reviewer, or documenter: git log plus changelog is the record. Relay the executor's report, then dispatch the `shipper` to finish the branch as in step 7. On scope creep, convert to the full pipeline starting at step 3.
3. Brainstorm (full path, unless `no brainstorm` is present, or the request is explicit enough to spec without it): load the `brainstorming` skill; explore intent, requirements, and design. Dispatch the `explore` subagent for codebase recon and web lookups.
4. Spec: write the design to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md` (today's date).
5. Plan: load the `writing-plans` skill; write the plan to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md`, referencing the spec.
6. Lean-plan gate: dispatch the `lazy-dev` subagent with the spec and plan paths; fold findings into the plan and re-dispatch until PASS (max 2 rounds), attaching leftovers to the execute dispatch as constraints.
7. Execute (default): dispatch the `orchestrator` subagent with the spec and plan paths; it branches, runs executor/reviewer in parallel waves (executors for all ready tasks at once, each reviewer pipelined as its own executor returns), escalates two-strike failures to `oracle`, then runs a structure review (`doc-standardizer` + `code-standardizer`, dispatched concurrently, with quick-fix `executor` passes) and a documentation phase (`documenter` writes the execution report to `docs/artifacts/features/` and updates catalogs, plus writes choices entries to `docs/artifacts/choices/`), commits at boundaries, and returns a final report. Relay that report, then dispatch the `shipper` to finish the branch (PR, merge question, tag and release). If `orchestrator` is unavailable, dispatch `general` with the same instructions; if no subagent dispatch is possible, fall back to step 8.
8. Handoff (only when `handoff` is present, or as the fallback): print the spec and plan paths plus `/execute-plan docs/artifacts/features/<topic>/<file>.md` for a fresh session.

No approval gates: the run goes straight through from prompt to final report. Do not end the turn between phases to ask whether to continue; end only at the final report (or the handoff block).

Requires `subagent_depth >= 2` in opencode config so the orchestrator can dispatch executor/reviewer; the quick-fix path needs only depth 1. If unset, a full-pipeline execute dispatch fails with "Subagent depth limit reached"; in that case fall back to step 8 for the full pipeline. On the quick path, report the dispatch failure instead (there are no spec/plan paths to hand off).
