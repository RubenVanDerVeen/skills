# Single-pass /full-cycle: planner dispatches the orchestrator in one run

Date: 2026-07-30
Status: draft (awaiting approval)

## Goal

Collapse `/full-cycle` into one fully-autonomous run. The planner brainstorms (optional), writes the spec, writes the plan, then dispatches the `orchestrator` as a subagent to execute the plan in the same run. The orchestrator runs its existing executor/reviewer/oracle loop with a fresh context and returns a final report, which the planner relays to the user. No approval gates, no manual session switch. Prompt in, final report out.

The manual fresh-session handoff survives as an explicit opt-in for huge tasks.

## Context (current state, 2026-07-30)

- `/full-cycle` (`commands/full-cycle.md`) runs as the `planner` (primary): brainstorm > spec > plan > stop at a handoff line. Two approval gates (spec, plan). The user then pastes `/execute-plan <path>` in a fresh session that runs as `orchestrator`.
- The `orchestrator` is `mode: primary` (`agents/orchestrator.md`), so it is NOT dispatchable by the planner. Primary agents are session drivers; only `subagent` and `all` agents appear in the task tool's dispatch list.
- opencode agent modes, verified in `packages/opencode/src/agent/agent.ts`: `mode: Schema.Literals(["subagent", "primary", "all"])`. `all` means both a session driver and dispatchable. It is the DEFAULT for custom agents when `mode` is omitted.
- Nested subagent dispatch is supported but gated by config, verified in `packages/opencode/src/tool/task.ts`: a depth check `if (depth >= cfg.subagent_depth ?? 1)` fails the dispatch. Default `subagent_depth` is 1, which allows planner (depth 0) to orchestrator (depth 1) but BLOCKS orchestrator to executor (depth 2). Single-pass needs `subagent_depth >= 2`.
- The task tool auto-denies `task` and `todowrite` for any dispatched subagent that does not explicitly declare those permissions (`packages/opencode/src/agent/subagent-permissions.ts`, `deriveSubagentSessionPermission`). Today's `orchestrator.md` declares neither. That is fine while it runs as a primary session (the auto-deny applies only to task-spawned sessions), but it would strip both the moment the orchestrator runs as a subagent.
- Subagent capabilities are governed by the subagent's own permission, not the parent's (`subagent-permissions.ts` doc: "the subagent's own permissions determine its capabilities"). Inherited parent rules contribute directory containment (`external_directory`) and deny rules. Current evidence: the primary orchestrator (edit/write/patch denied) dispatches executor (edit/write allowed) and executor edits successfully today, so the executor child's own permissions hold. The two-level chain (planner to orchestrator to executor) should behave the same, but must be verified empirically (see Verification gates).

## Decisions (locked with user)

1. Gates: removed. Single-pass runs straight through: brainstorm (if on) > spec > plan > dispatch > report.
2. Brainstorm: ON by default. Skip when the request is explicit enough to spec without it, OR when the prompt contains the keyword `no brainstorm`.
3. Manual handoff: retained as an explicit opt-in. The keyword `handoff` in the prompt makes `/full-cycle` print the `/execute-plan <path>` line for a fresh session instead of dispatching.

## Design

### Flow

1. `/full-cycle <task>` runs as `planner`. Parse `$ARGUMENTS` for the keywords `no brainstorm` and `handoff`.
2. If brainstorm is on (default) and the request is not explicit enough, load the `brainstorming` skill and explore intent, requirements, and design. Dispatch `explore` for recon.
3. Write the spec to `docs/artifacts/specs/<topic>/YYYY-MM-DD-<slug>-design.md`. No approval pause.
4. Load `writing-plans`, write the plan to `docs/artifacts/plans/<topic>/YYYY-MM-DD-<slug>-plan.md`, referencing the spec. No approval pause.
5. If the `handoff` keyword is present: print the handoff block (spec + plan paths, the `/execute-plan <path>` line) and stop. Old behavior.
6. Otherwise (default): dispatch the `orchestrator` subagent with the plan path and spec path, instructing it to execute the plan following the `/execute-plan` conventions (branch first, ponytail, per-task Conventional Commits, executor/reviewer per task, oracle on two-strike failures, final report). The orchestrator runs with a fresh context.
7. When the orchestrator returns, relay its final report to the user (branch, commits, files changed, verifier output, deferrals, anything Unverified). End.

The orchestrator's internal loop, git operations (bash), and report format are unchanged. The planner does not implement; it dispatches and relays.

### Why this preserves the old design's benefits

- Context hygiene: the orchestrator subagent starts with a fresh context (task tool contract: each agent invocation starts with a fresh context). The manual fresh-session handoff existed to reset context before execution; the subagent boundary delivers that reset automatically.
- Role separation: the planner still cannot write outside `docs/**` (dispatch is a `task` call, not a file write) and still denies the execution-skill suite. The orchestrator still denies edit/write/patch and implements only through executor subagents. No role boundary is weakened.
- Standalone `/execute-plan` in a fresh session still works: an `all` agent is still primary-eligible, so the existing two-step workflow and the `handoff` opt-in path are both intact.

## Required changes

### `agents/orchestrator.md`
- `mode: primary` to `mode: all`. One line. Keeps it a valid session agent and makes it dispatchable.
- Add an explicit `task` permission allowing the agents it must spawn: `executor`, `reviewer`, `oracle`, `explore` (and `*`: deny, or allow per preference). Without this, the task tool auto-denies `task` when the orchestrator runs as a subagent.
- Add `todowrite: allow`. The orchestrator maintains a live todo list; without an explicit rule the task tool auto-denies it for subagents.
- Description: note it is now also dispatchable by the planner for single-pass `/full-cycle`.

### `agents/planner.md`
- Frontmatter description: replace "stops at the /execute-plan handoff" with "dispatches the orchestrator to execute the plan in the same run (single-pass), unless the `handoff` keyword is given".
- Body: replace step 4 (hand off) with the dispatch step and the keyword rules (`no brainstorm`, `handoff`). Keep the docs-only write deny and the execution-skill denies. Add: after writing the plan, dispatch the `orchestrator` subagent with the plan/spec paths and the `/execute-plan` conventions folded into the dispatch prompt; relay its final report. Note the `handoff` opt-in. The `explore` recon dispatch stays as-is.
- No permission change needed: dispatch uses `task`, which the planner already has; file writes stay docs-only.

### `commands/full-cycle.md`
Rewrite the body for single-pass:
- Default: straight through, no gates, auto-dispatch the orchestrator at the end.
- `no brainstorm` keyword: skip the brainstorm phase.
- `handoff` keyword: print the handoff line instead of dispatching (old behavior).
- Remove the `at once` special-case: it existed to collapse the gates, and gates are gone, so it is now equivalent to the default. Drop the special-case text; the keyword can be tolerated as a no-op for muscle memory.
- Fallback: if the `orchestrator` agent is unavailable, dispatch the `general` subagent with the `/execute-plan` instructions (single-pass preserved); if subagent dispatch is unavailable, fall back to printing the handoff line.

### `commands/execute-plan.md`
No structural change. Add one line noting the command also runs unchanged when the orchestrator is dispatched as a subagent by the planner; the conventions it lists (branch, ponytail, per-task commits, graphify, report) are the same conventions the planner folds into the orchestrator dispatch prompt. The plan decides whether to keep these conventions only in the command or also mirror them into `orchestrator.md` so both paths share one source of truth.

### `agents/README.md`
- Orchestrator row: `Mode` primary to all; note it is now dispatchable for single-pass `/full-cycle` while remaining a session agent for standalone `/execute-plan`.
- Add a short note on single-pass `/full-cycle` and the `subagent_depth` requirement.

### Machine-local opencode config (not committed)
Set `"subagent_depth": 2` in `~/.config/opencode/opencode.json`. This is the minimum for planner to orchestrator to executor. Without it the orchestrator subagent cannot dispatch executor/reviewer and the run fails with "Subagent depth limit reached". Document this as a required one-time local config step in `agents/README.md`.

### Catalog and changelog
- `AGENTS.md`: update any text describing the planner as handoff-only and the orchestrator as primary-only.
- `CHANGELOG.md`: entry under the current unreleased section.
- Sync: copy `agents/*.md` and `commands/*.md` to `~/.config/opencode/`, set `subagent_depth: 2`, restart opencode, validate.

## Verification gates (must pass before declaring done)

These are empirical because they depend on the installed opencode build:

1. Depth: with `subagent_depth: 2`, a planner dispatch of the orchestrator that itself dispatches executor succeeds; with the default 1 it fails with the depth-limit error. Confirm both directions.
2. Auto-deny: with the new explicit `task` and `todowrite` permissions on the orchestrator, the orchestrator subagent can dispatch executor/reviewer and update its todo list. Without them, it cannot. Confirm.
3. Inherited writes: in the two-level chain, the executor grandchild can still write a source file outside `docs/` (its own `edit/write: allow` holds despite the planner ancestor's docs-only restriction). This is the load-bearing check; if it fails, single-pass falls back to the handoff path.
4. Standalone regression: `/execute-plan <path>` in a fresh session still runs as orchestrator and still dispatches executor/reviewer (the `all` change did not break the primary path).

## Risks and fallbacks

- If verification 3 fails (executor grandchild cannot write): single-pass is not viable on this opencode build. Fallback: keep `handoff` as the default and make single-pass opt-in, or stay on the two-step workflow. The required config changes (mode: all, explicit task/todowrite, subagent_depth) are still worth landing because they unblock future use.
- No approval gates means a misread task executes without a checkpoint. Mitigation: brainstorm is on by default (surfaces intent early); the spec and plan are still written to `docs/artifacts/` and are visible and interruptible mid-run; the `handoff` opt-in remains for tasks that need a checkpoint.
- Planner context budget: single-pass holds brainstorm + spec + plan output in the planner's context before dispatch. For huge tasks this risks filling the context. Mitigation: the `handoff` opt-in; optionally the planner switches to handoff if it detects context pressure (nice-to-have, not required).
- `subagent_depth: 2` lets executor attempt one further dispatch (depth 2 to 3 is blocked), which is the intended ceiling. No runaway recursion.

## Out of scope (deliberately skipped)

- Re-adding approval gates or a mid-run review checkpoint (the `handoff` opt-in covers the checkpoint need; YAGNI).
- Changes to executor/reviewer/oracle definitions (unchanged).
- Multi-plan orchestration changes (unchanged; if a task outgrows one plan the planner still loads it).
- A new reporting agent or richer final reports (the orchestrator's existing report suffices).
- Whether to mirror `/execute-plan` conventions into `orchestrator.md`: decided in the plan, not the spec.
