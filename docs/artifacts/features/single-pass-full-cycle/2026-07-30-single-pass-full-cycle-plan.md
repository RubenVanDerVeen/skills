# Single-pass /full-cycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `/full-cycle` run prompt-to-report in one pass by having the planner dispatch the `orchestrator` as a subagent (which dispatches executor/reviewer/oracle) instead of stopping at a handoff line.

**Architecture:** Change the orchestrator from `mode: primary` to `mode: all` so the planner can dispatch it; add explicit `task` and `todowrite` permissions so the task tool does not auto-deny them when the orchestrator runs as a subagent; rewrite the planner body and `/full-cycle` command for single-pass with `no brainstorm` and `handoff` keywords; require machine-local `subagent_depth: 2`. The manual fresh-session handoff survives as a `handoff` opt-in.

**Tech Stack:** opencode agent config (YAML frontmatter + markdown bodies), markdown command files, opencode CLI (`opencode agent list`, `opencode debug agent`). No code, no build step.

**Spec:** `docs/artifacts/features/single-pass-full-cycle/2026-07-30-single-pass-full-cycle-design.md`

## Global Constraints

- No em-dashes (U+2014) anywhere. Verify after each task: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty for edited files. Also use ASCII arrows (`->`) or `>` in prose, never Unicode arrows.
- Frontmatter rules: `name` kebab-case matching folder; `description` under 1024 chars total; no top-level `## Skill` heading (use `## Overview`).
- Conventional Commits 1.0.0. Per-task commits are sanctioned by the plan-execution carve-out; do not pause to ask.
- Markdown only. Agent and command files are inert in this repo until synced to `~/.config/opencode/`; opencode loads config once at startup, so runtime verification needs a fresh opencode process.
- `~/.config/opencode/opencode.json` may contain secrets (homelab MCP keys). When editing it, add only the `subagent_depth` key. Never print, echo, log, or diff its contents; verify by checking only that the key exists, never by dumping the file.
- Today's date is 2026-07-30 for any dated artifact paths.
- The executing session cannot change its own running config mid-flight; runtime gate verification runs via a child `opencode run` process (reads fresh config) or is documented for a post-restart terminal.

## File Structure

Source-of-truth edits (committed):
- `agents/orchestrator.md`: mode + permissions + description.
- `agents/planner.md`: description + pipeline body.
- `commands/full-cycle.md`: rewrite for single-pass.
- `commands/execute-plan.md`: one-line note.
- `agents/README.md`: orchestrator row + single-pass note.
- `AGENTS.md`: two comment/text lines.
- `CHANGELOG.md`: Unreleased entries.

Machine-local (not committed):
- `~/.config/opencode/agents/*.md`: synced copies of the four agent/command-adjacent files.
- `~/.config/opencode/command/full-cycle.md`, `execute-plan.md`: synced copies.
- `~/.config/opencode/opencode.json`: add `subagent_depth: 2`.

---

### Task 1: Make the orchestrator dispatchable (mode + permissions)

**Files:**
- Modify: `agents/orchestrator.md`

**Depends on:** nothing. **Affects:** every later runtime gate; the planner dispatch in Task 8.

- [ ] **Step 1: Change `mode` and add `task` + `todowrite` permissions**

In `agents/orchestrator.md`, change line 3 from `mode: primary` to `mode: all`.

In the `permission:` block, after the `patch: deny` line (and before `skill:`), insert the `task` and `todowrite` entries. The resulting frontmatter `permission:` block must read exactly:

```yaml
permission:
  edit: deny
  write: deny
  patch: deny
  task:
    "executor": allow
    "reviewer": allow
    "oracle": allow
    "explore": allow
    "*": deny
  todowrite: allow
  skill:
    "*": allow
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
    "stop-slop": deny
    "synctool-sync": deny
    "test-driven-development": deny
```

Keep the rest of the existing skill-deny list as-is; the snippet above shows the full current `skill:` block for completeness, do not remove any existing entries.

- [ ] **Step 2: Update the frontmatter `description`**

Replace the current `description:` line with:

```yaml
description: Executes approved plans. Dispatches executor subagents per task, reviews results via the reviewer subagent, escalates two-strike failures to the oracle, manages the todo list, commits at boundaries. Cannot write, edit, or patch files; all implementation goes through subagents. Runs as a session agent for standalone /execute-plan, or dispatched by the planner for single-pass /full-cycle (mode: all).
```

- [ ] **Step 3: Content check**

Run: `(Get-ChildItem agents\orchestrator.md | Select-String -Pattern ([char]0x2014))`
Expected: no output (no em-dashes).

- [ ] **Step 4: Commit**

```bash
git add agents/orchestrator.md
git commit -m "feat(agents): make orchestrator dispatchable (mode: all) with explicit task/todowrite perms"
```

---

### Task 2: Planner dispatches instead of handing off

**Files:**
- Modify: `agents/planner.md`

**Depends on:** nothing. **Affects:** Task 8 (the dispatch uses this body).

- [ ] **Step 1: Replace the frontmatter `description`**

Replace the current `description:` line with:

```yaml
description: Designs specs and implementation plans, then dispatches the orchestrator to execute the plan in the same run. Brainstorms intent (skip with `no brainstorm`), writes the spec, writes the plan, dispatches the orchestrator subagent, relays its report. Use `handoff` to instead print the /execute-plan line for a fresh session. File writes limited to docs/; source code untouchable. Dispatches the explore subagent for codebase recon.
```

- [ ] **Step 2: Replace the body pipeline section**

Replace the entire body (everything after the closing `---` of frontmatter) with:

```
You are the planner: you turn a feature request into a spec and plan, then dispatch the orchestrator to execute it in the same run. You never implement; you dispatch and relay. Your file writes only land under docs/ (permissions enforce this).

Single-pass pipeline (default, no approval gates):
1. Parse the prompt for keywords: `no brainstorm` skips step 2; `handoff` switches the end of the pipeline to the manual handoff in step 6.
2. Brainstorm (unless skipped, or the request is explicit enough to spec without it): load the brainstorming skill; explore intent, requirements, and design. Dispatch the explore subagent for codebase recon instead of grepping in your own window.
3. Spec: write the design to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md.
4. Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md, referencing the spec.
5. Dispatch: dispatch the orchestrator subagent with the spec and plan paths, instructing it to execute the plan following the /execute-plan conventions (branch first, ponytail, per-task Conventional Commits, executor/reviewer per task, oracle on two-strike failures, final report). When it returns, relay its final report to the user. If the orchestrator agent is unavailable, dispatch the general subagent with the same instructions; if no subagent dispatch is possible, fall back to step 6.
6. Handoff (only when the `handoff` keyword is given, or as the fallback above): end with the spec and plan paths plus the exact line to paste in a fresh session: /execute-plan <plan-path>.

Within a phase, never end the turn to ask whether to continue; the run goes straight through from prompt to final report.

Scope discipline: YAGNI in every design; propose 2-3 approaches with a recommendation before locking one in. If the task outgrows one plan, load multi-plan-orchestration and split it.
```

- [ ] **Step 3: Content check**

Run: `(Get-ChildItem agents\planner.md | Select-String -Pattern ([char]0x2014))`
Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add agents/planner.md
git commit -m "feat(agents): planner dispatches orchestrator in single-pass; no brainstorm/handoff keywords"
```

---

### Task 3: Rewrite /full-cycle for single-pass

**Files:**
- Modify: `commands/full-cycle.md`

**Depends on:** Tasks 1 and 2 (the command references the orchestrator dispatch and the planner body).

- [ ] **Step 1: Replace the entire file contents**

Overwrite `commands/full-cycle.md` with exactly:

```markdown
---
description: Take a feature request from prompt to shipped change in one run - brainstorm (optional) > spec > plan > dispatch the orchestrator to execute, then relay its report. Single-pass, no approval gates. Use `handoff` to print the /execute-plan line for a fresh session instead.
---

Run the full pipeline for `$ARGUMENTS` in a single pass. Agent mapping: run this command as the `planner` agent when available; fall back to the current agent otherwise.

Keywords in `$ARGUMENTS`:
- `no brainstorm`: skip the brainstorm phase (spec directly).
- `handoff`: print the /execute-plan line for a fresh session instead of dispatching. Use for huge tasks where the planner's context should not carry into execution.

Steps:
1. Brainstorm (unless `no brainstorm` is present, or the request is explicit enough to spec without it): load the `brainstorming` skill; explore intent, requirements, and design. Dispatch the `explore` subagent for codebase recon.
2. Spec: write the design to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md` (today's date).
3. Plan: load the `writing-plans` skill; write the plan to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md`, referencing the spec.
4. Execute (default): dispatch the `orchestrator` subagent with the spec and plan paths; it branches, runs executor/reviewer per task, escalates two-strike failures to `oracle`, commits at boundaries, and returns a final report. Relay that report. If `orchestrator` is unavailable, dispatch `general` with the same instructions; if no subagent dispatch is possible, fall back to step 5.
5. Handoff (only when `handoff` is present, or as the fallback): print the spec and plan paths plus `/execute-plan docs/artifacts/features/<topic>/<file>.md` for a fresh session.

No approval gates: the run goes straight through from prompt to final report. Do not end the turn between phases to ask whether to continue; end only at the final report (or the handoff block).

Requires `subagent_depth >= 2` in opencode config so the orchestrator can dispatch executor/reviewer. If unset, the dispatch fails with "Subagent depth limit reached"; in that case fall back to step 5.
```

- [ ] **Step 2: Content check**

Run: `(Get-ChildItem commands\full-cycle.md | Select-String -Pattern ([char]0x2014))`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add commands/full-cycle.md
git commit -m "feat(commands): single-pass /full-cycle with no brainstorm and handoff keywords"
```

---

### Task 4: Note the subagent path in /execute-plan

**Files:**
- Modify: `commands/execute-plan.md`

**Depends on:** Task 1.

- [ ] **Step 1: Append one sentence to the agent-mapping paragraph**

In `commands/execute-plan.md`, the agent-mapping paragraph (the one beginning "Agent mapping: if named subagents exist...") ends with "...when `oracle` is missing, decide yourself." Append immediately after that sentence:

```
 The planner can also dispatch the orchestrator as a subagent to run this command's flow in single-pass `/full-cycle`; the conventions below are identical either way.
```

- [ ] **Step 2: Content check**

Run: `(Get-ChildItem commands\execute-plan.md | Select-String -Pattern ([char]0x2014))`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add commands/execute-plan.md
git commit -m "docs(commands): note single-pass subagent path in /execute-plan"
```

---

### Task 5: Update agents/README.md and AGENTS.md

**Files:**
- Modify: `agents/README.md`
- Modify: `AGENTS.md`

**Depends on:** Tasks 1 and 2.

- [ ] **Step 1: Update the orchestrator row in `agents/README.md`**

In the set table, change the orchestrator row. Replace:

```
| `orchestrator` | primary | `minimax-coding-plan/MiniMax-M3` | Executes approved plans: dispatches executor/reviewer per task, oracle on two-strike failures, commits at boundaries via bash. | edit/write/patch tools; implementation-domain skills |
```

with:

```
| `orchestrator` | all | `minimax-coding-plan/MiniMax-M3` | Executes approved plans: dispatches executor/reviewer per task, oracle on two-strike failures, commits at boundaries via bash. Session agent for standalone /execute-plan and dispatchable by the planner for single-pass /full-cycle. | edit/write/patch tools; implementation-domain skills |
```

- [ ] **Step 2: Add a single-pass note in `agents/README.md`**

After the paragraph that ends "...no custom file needed." (the one describing `/full-cycle` runs as `planner` and `/execute-plan` dispatch by name), append one sentence:

```
 Single-pass `/full-cycle`: the planner dispatches the `orchestrator` as a subagent (mode `all`) instead of stopping at a handoff; this requires `subagent_depth >= 2` in opencode config so the orchestrator can dispatch executor/reviewer.
```

- [ ] **Step 3: Update the two `AGENTS.md` spots**

In `AGENTS.md`, replace the line:

```
│   ├── full-cycle.md                          <- /full-cycle: brainstorm > spec > plan, hand off execution
```

with:

```
│   ├── full-cycle.md                          <- /full-cycle: single-pass brainstorm > spec > plan > dispatch orchestrator (or handoff)
```

In `AGENTS.md`, replace the sentence:

```
They pair with `/full-cycle` (runs as `planner`) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult).
```

with:

```
They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult).
```

- [ ] **Step 4: Content check**

Run: `(Get-ChildItem agents\README.md,AGENTS.md | Select-String -Pattern ([char]0x2014))`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add agents/README.md AGENTS.md
git commit -m "docs(agents): record orchestrator mode:all and single-pass /full-cycle"
```

---

### Task 6: CHANGELOG entry

**Files:**
- Modify: `CHANGELOG.md`

**Depends on:** Tasks 1 through 5 (summarizes them).

- [ ] **Step 1: Add entries under `[Unreleased]`**

In `CHANGELOG.md`, under `## [Unreleased]`, in the `### Added` subsection, append:

```
- Single-pass `/full-cycle`: the planner dispatches the `orchestrator` subagent to execute the plan in the same run (prompt to final report, no approval gates). `no brainstorm` skips brainstorming; `handoff` keeps the old fresh-session handoff. Requires machine-local `subagent_depth: 2`. Spec: `docs/artifacts/features/single-pass-full-cycle/2026-07-30-single-pass-full-cycle-design.md`.
```

In the `### Changed` subsection, append:

```
- `agents/orchestrator.md`: `mode: primary` to `mode: all` (now dispatchable by the planner); added explicit `task` (executor/reviewer/oracle/explore) and `todowrite` permissions so the task tool does not auto-deny them when the orchestrator runs as a subagent.
- `agents/planner.md`: end of pipeline dispatches the orchestrator instead of handing off; single-pass, no gates; `no brainstorm` and `handoff` keywords.
- `commands/full-cycle.md`: rewritten for single-pass; removed the `at once` gate-collapse special-case (gates are gone, so it was equivalent to the new default).
```

- [ ] **Step 2: Content check**

Run: `(Get-ChildItem CHANGELOG.md | Select-String -Pattern ([char]0x2014))`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog for single-pass /full-cycle"
```

---

### Task 7: Sync to machine-local opencode config (not committed)

**Files:**
- Modify (machine-local, not in repo): `~/.config/opencode/agents/orchestrator.md`, `~/.config/opencode/agents/planner.md`, `~/.config/opencode/command/full-cycle.md`, `~/.config/opencode/command/execute-plan.md`, `~/.config/opencode/opencode.json`

**Depends on:** Tasks 1 through 6. **Affects:** Task 8 (verification reads the synced config).

- [ ] **Step 1: Copy the four changed files into the opencode config**

Run:

```bash
Copy-Item agents\orchestrator.md "$env:USERPROFILE\.config\opencode\agents\orchestrator.md" -Force
Copy-Item agents\planner.md "$env:USERPROFILE\.config\opencode\agents\planner.md" -Force
Copy-Item commands\full-cycle.md "$env:USERPROFILE\.config\opencode\command\full-cycle.md" -Force
Copy-Item commands\execute-plan.md "$env:USERPROFILE\.config\opencode\command\execute-plan.md" -Force
```

Expected: four `Copy-Item` commands succeed silently.

- [ ] **Step 2: Add `subagent_depth: 2` to `opencode.json` WITHOUT printing the file**

`~/.config/opencode/opencode.json` may contain secrets. Edit it programmatically, adding only the top-level `subagent_depth` key if absent, and verify only that the key now exists. Never dump the file. Run:

```powershell
$path = "$env:USERPROFILE\.config\opencode\opencode.json"
$json = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
if ($null -eq $json.PSObject.Properties['subagent_depth']) {
    $json | Add-Member -NotePropertyName 'subagent_depth' -NotePropertyValue 2
    $json | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $path -NoNewline
}
# Verify ONLY that the key exists; do not print file contents.
$check = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
"subagent_depth present = $($null -ne $check.PSObject.Properties['subagent_depth']) value = $($check.subagent_depth)"
```

Expected: `subagent_depth present = True value = 2`.

If `ConvertTo-Json` reformats the file in a way that drops comments or reorders keys, that is acceptable; JSON has no comments. If the file is `.jsonc` or fails to parse, stop and report rather than risking corruption.

- [ ] **Step 3: No commit (machine-local change)**

Nothing to commit; these files are outside the repo. Note in the final report that the sync was performed.

---

### Task 8: Verification (deterministic config checks + runtime smoke test)

**Files:** none modified. Verification only.

**Depends on:** Task 7. This task validates the spec's four verification gates.

The executing session cannot change its own running config, so config-parse checks run against the synced config via the opencode CLI in a child process; the runtime write test (gate 3) runs via a child `opencode run` process or, if a server/lock conflict occurs, is documented for a post-restart terminal.

- [ ] **Step 1: Deterministic config checks (gates 1-config, 2-config, 4)**

Run each and record output:

```bash
opencode agent list
```
Expected: `orchestrator` and `planner` both present; no parse error.

```bash
opencode debug agent orchestrator
```
Expected: resolved config shows `mode: all`; `task` permission has executor/reviewer/oracle/explore allow and `*` deny; `todowrite` allow; edit/write/patch still denied.

```bash
opencode debug agent planner
```
Expected: `mode: primary`; edit/write/patch glob `docs/**` allow; `task` still allowed (unchanged).

- [ ] **Step 2: Runtime smoke test for gate 3 (executor grandchild can write outside docs)**

Create an isolated scratch repo and run a child `opencode run` that exercises the full chain: planner dispatches orchestrator, orchestrator dispatches executor, executor writes a file in the scratch root (outside any `docs/`).

```bash
$scratch = Join-Path $env:TEMP "opencode-singlepass-smoke"
Remove-Item $scratch -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $scratch -Force | Out-Null
git init $scratch | Out-Null
opencode run --cwd $scratch --agent planner "Dispatch the orchestrator subagent to execute a one-task plan: have the executor create a file named smoke.txt at the repo root containing the single word ok. Then report whether smoke.txt exists."
Test-Path (Join-Path $scratch "smoke.txt")
Get-Content (Join-Path $scratch "smoke.txt") -ErrorAction SilentlyContinue
```

Expected: `Test-Path` returns `True`; file content is `ok`.

Interpretation:
- If it succeeds: gates 1 (depth), 2 (auto-deny bypassed), and 3 (inherited writes) all pass. Single-pass is viable.
- If output contains `Subagent depth limit reached`: gate 1 failed; `subagent_depth` is not 2. Re-check Task 7 step 2.
- If the orchestrator/orchestrator's executor reports a permission denial writing `smoke.txt`: gate 3 failed. Apply the spec fallback (flip the `/full-cycle` default to `handoff`) and report; do not claim single-pass works.
- If `opencode run` fails with a server/lock conflict because opencode is already running: mark gate 3 as `Unverified - post-restart` and document the exact command above for the user to run in a fresh terminal after restarting opencode.
- If `opencode run` is not available non-interactively in this build: mark gate 3 as `Unverified - post-restart` with the command above.

- [ ] **Step 3: Standalone regression check (gate 4)**

Confirm the `all` change did not break standalone execution. Run:

```bash
opencode debug agent orchestrator
```
Expected: `mode: all` is primary-eligible (the debug output lists it as a usable session agent). No further action; this is the same command as step 1, read for primary-eligibility. The real regression proof is running `/execute-plan <some-plan>` in a fresh session after restart; if that cannot be done here, list it as `Unverified - post-restart`.

- [ ] **Step 4: No commit; produce the verification section of the final report**

Record, for each gate (1 depth, 2 auto-deny, 3 inherited writes, 4 standalone regression): PASS / FAIL / Unverified, with the command output that supports the claim. Anything Unverified lists the exact post-restart command to run.

---

## Self-Review

Spec coverage check against `2026-07-30-single-pass-full-cycle-design.md`:

- "mode: primary to mode: all" -> Task 1 step 1. Covered.
- "Add explicit task permission (executor/reviewer/oracle/explore)" -> Task 1 step 1. Covered.
- "Add todowrite: allow" -> Task 1 step 1. Covered.
- "orchestrator description update" -> Task 1 step 2. Covered.
- "planner frontmatter description" -> Task 2 step 1. Covered.
- "planner body dispatch step + keyword rules" -> Task 2 step 2. Covered.
- "full-cycle rewrite, single-pass, no gates, no brainstorm, handoff, remove at once, fallback to general" -> Task 3 step 1. Covered.
- "execute-plan one-line note" -> Task 4 step 1. Covered.
- "agents/README orchestrator row + single-pass note" -> Task 5 steps 1 and 2. Covered.
- "AGENTS.md text updates" -> Task 5 step 3. Covered.
- "CHANGELOG entry" -> Task 6. Covered.
- "machine-local subagent_depth: 2" -> Task 7 step 2. Covered.
- "sync copies" -> Task 7 step 1. Covered.
- "Verification gates 1 to 4" -> Task 8. Covered.
- "handoff opt-in survives" -> Task 2 step 2 (step 6) and Task 3 step 1 (step 5). Covered.
- "fallback if orchestrator unavailable -> general -> handoff" -> Task 2 step 2 and Task 3 step 1. Covered.

Placeholder scan: no TBD/TODO/`implement later`; every step carries exact content or an exact command. Type/name consistency: `subagent_depth`, `mode: all`, `task`/`todowrite` permission keys, and the `no brainstorm`/`handoff` keywords are spelled identically across tasks 1, 2, 3, 5, 6, 7, 8.

One spec item intentionally deferred to execution judgment, not a placeholder: the spec left open "whether to mirror /execute-plan conventions into orchestrator.md." This plan keeps a single source of truth in `commands/execute-plan.md` and has the planner fold those conventions into the dispatch prompt (Task 2 step 2, step 5). No file duplication. This is the ponytail choice; noted here so it is visible.

## Follow-up (out of this plan's scope)

User decision 2026-07-30: the `.drawio` diagrams go in a separate follow-up (tiny plan, or by hand in the draw.io GUI). Recorded here so the work is not lost. This plan does not touch them; `plan-flow.drawio` and `stack.drawio` will be stale at rev C until the follow-up lands.

`docs/plan-flow.drawio` (substantive):
- Title node `title`: change "/full-cycle (planner) to /execute-plan (orchestrator) (rev C)" to a single-pass title; bump rev C to D.
- Remove the two approval decision diamonds `n4` (Spec approved?) and `n6` (Plan approved?) and their revise-loop edges `e_n4no`, `e_n6no` and the Yes-labelled edges `e_n4n5`, `e_n6n7`.
- Reroute the planner lane to straight-through: `n3` (spec) -> `n5` (plan) -> `n7` (dispatch) directly.
- Rewrite node `n7` from "Handoff: /execute-plan <plan-path> (fresh session; planner never implements)" to a dispatch step: planner dispatches the orchestrator subagent (mode: all) with spec+plan paths; orchestrator executes (branch, executor/reviewer/oracle, commits) and returns a report the planner relays; `handoff` keyword switches to the fresh-session `/execute-plan` path.
- Relabel edge `e_handoff` from "fresh session" to "same run (subagent, fresh context)".
- Rewrite the `legend` node: drop gate language; state single-pass (no approval gates), the `no brainstorm` and `handoff` keywords, the `subagent_depth >= 2` requirement, orchestrator `mode: all`, and that the planner dispatches (does not implement).
- Phase header `ph1hdr` may append "(single-pass: then dispatches orchestrator)".

`docs/stack.drawio` (small):
- Node `aOrch`: "orchestrator (primary)" -> "orchestrator (all)".
- Usage chip `f2`: entry point "/execute-plan" -> "/full-cycle" (single-pass: brainstorm, spec, plan, dispatch, review).
- Optionally bump rev C -> D and the snapshot date.

`docs/multi-plan-flow.drawio`: no change. It is the parallel sub-plan flow (`/multi-plan`), which deliberately uses fresh user-dispatched sessions; single-pass does not apply (spec excludes multi-plan).
