# Plan: quick-fix fast path in the planner pipeline

Date: 2026-11-13
Spec: docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-design.md
Branch: feat/quick-fix-path
Versioning: unversioned, no bump (repo AGENTS.md has no `### Versioning` subsection)

## File structure

Four tasks, all `Depends: none`, mutually disjoint files, one parallel wave:

| Task | Files | Commit |
|---|---|---|
| 1 | `agents/planner.md` | `feat(agents): add quick-fix fast path to planner intake` |
| 2 | `commands/full-cycle.md` | `feat(commands): add quick-fix branch to full-cycle` |
| 3 | `agents/executor.md` | `feat(agents): teach executor quick-fix dispatch without a plan` |
| 4 | `agents/README.md`, `README.md`, `AGENTS.md` | `docs(agents): sync catalogs for the quick-fix fast path` |

Wording contract shared verbatim by all tasks (do not paraphrase): keywords `quick` and `full`; criteria "one task with one obvious fix; expected diff touches about 1-2 files; no design alternatives worth weighing, no new interface, API, behavior surface, or schema; one runnable verification check covers it; nothing that belongs in `docs/artifacts/choices/`"; the scope-creep stop ("more files than the brief names, new logic branches, a new interface, a second task emerging"). No em-dashes anywhere (pre-commit hook rejects them).

All tasks: after editing, verify with the exact greps in the task, then make the pathspec commit. Working directory is the repo root.

### Task 1: planner intake classification and quick-fix path

**Files:**
- Modify: `agents/planner.md` (frontmatter description line 2; body pipeline list lines 43-50)

**Depends:** none

**Interfaces:**
- Consumes: none
- Produces: the quick-path process definition referenced by Tasks 2 and 4 (they embed their own verbatim copies; no file-level consumption)

- [ ] **Step 1: Update the frontmatter description**

Replace the description value (line 2) with:

```
Classifies each request at intake: a small fix (one obvious fix, about 1-2 files, no design alternatives) takes a quick path, one executor with an inline brief and no spec/plan/report artifacts; `quick` forces it, `full` forces the complete pipeline. Everything else: designs specs and implementation plans, then dispatches the orchestrator to execute the plan in the same run. Brainstorms intent (skip with `no brainstorm`), writes the spec, writes the plan, dispatches the orchestrator subagent, relays its report, then dispatches the shipper for PR and release. Gates every plan through the lazy-dev subagent (lean-plan review, loop to PASS capped at 2 rounds) before dispatching. Use `handoff` to instead print the /execute-plan line for a fresh session. File writes limited to docs/; source code untouchable. Delegates all recon (codebase reading and web lookup) to the explore subagent.
```

- [ ] **Step 2: Replace the pipeline list (lines 43-50)**

Replace the entire block from `Single-pass pipeline (default, no approval gates):` through step `7. Handoff (only when the ...)` (lines 43-50, ending before the blank line and `Within a phase`) with:

```
Single-pass pipeline (default, no approval gates):
1. Parse the prompt for keywords: `no brainstorm` skips the brainstorm step; `handoff` switches the end of the pipeline to the manual handoff in step 9; `quick` forces the quick-fix path (step 3); `full` forces the complete pipeline (steps 4-8).
2. Classify: quick fix or feature? Quick fix only when ALL hold: one task with one obvious fix; expected diff touches about 1-2 files; no design alternatives worth weighing, no new interface, API, behavior surface, or schema; one runnable verification check covers it; nothing that belongs in `docs/artifacts/choices/`. Any doubt means the full pipeline. Keywords `quick` and `full` override the classification either way. State the tier in one line ("Quick path: single executor, no spec/plan artifacts") so the user sees which path ran.
3. Quick-fix path: dispatch the `explore` subagent only when the target file or fix site is unknown. Then dispatch ONE executor with an inline task brief (no plan file, no spec): branch name (`fix/<scope>` or `chore/<scope>`), target files and the fix, the one verification command (copied from the target project's AGENTS.md), and a pointer to the executor's quick-fix rules (single Conventional Commit; changelog `[Unreleased]` entry when the project keeps one; patch bump when its AGENTS.md declares a version source; scope-creep stop). No lazy-dev gate (nothing to gate), no orchestrator, no reviewer, no documenter report: git log plus changelog is the record, and a fix that deserves a choices entry was never a quick fix. Relay the executor's report, then run the shipper tail described in step 8. If the executor stopped on scope creep, convert: continue at step 4 with the executor's findings as recon input.
4. Brainstorm (unless skipped, or the request is explicit enough to spec without it): load the brainstorming skill; explore intent, requirements, and design. Dispatch the explore subagent for codebase recon instead of grepping in your own window.
5. Spec: before locking the spec, grep `docs/artifacts/choices/` (all files, full text) for the task's topics and likely dependency or plugin names. Read every hit: carried constraints go into the spec; contradictions note the old entry as superseded (the documenter flips its status line at close-out). Then write the design to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md.
6. Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md, referencing the spec. Check the project's AGENTS.md for a `### Versioning` subsection: if it declares a canonical version source, the plan states the expected bump type for the shipped work; if not, the plan records "unversioned, no bump". Parallel readiness: every task in the plan carries a `**Depends:**` line (e.g. `**Depends:** none` or `**Depends:** Task 2, Task 3`) directly after its `**Files:**` block. Default to `none`; list a dependency only when the task's Interfaces `Consumes:` block cites an earlier task's output. All `Depends: none` tasks must have mutually disjoint `**Files:**` sets: merge overlapping tasks or add a dependency edge. When the domain forces a serial chain, maximize independent branches around it. The orchestrator dispatches ready tasks in parallel waves (see agents/orchestrator.md).
7. Lean-plan gate: dispatch the lazy-dev subagent with the spec and plan paths. On findings, fold the corrections into the plan (edit the spec too when a finding is prefixed "spec:") and re-dispatch. PASS is required before dispatching the orchestrator; cap the loop at 2 review rounds, and on a cap without PASS attach the remaining findings to the orchestrator dispatch as constraints. If the lazy-dev agent is unavailable, dispatch the general subagent instructed to review the plan with the ponytail skill and return PASS or findings in the same format.
8. Dispatch: dispatch the orchestrator subagent with the spec and plan paths, instructing it to execute the plan following the /execute-plan conventions (branch first, ponytail, per-task Conventional Commits, executor/reviewer per task, oracle on two-strike failures, documenter ship-bumps the version when the project is versioned, final report). When it returns, relay its final report to the user. If the orchestrator agent is unavailable, dispatch the general subagent with the same instructions; if no subagent dispatch is possible, fall back to step 9. After the relay, dispatch the shipper subagent to finish the branch: open the PR from the report, ask the user merged/tag-and-release vs merged/pull-locally vs abort, and cut the tag and release on a merged answer. Skip this only when the branch carries nothing shippable (docs-only run the user does not want a PR for).
9. Handoff (only when the `handoff` keyword is given, or as the fallback above): end with the spec and plan paths plus the exact line to paste in a fresh session: /execute-plan <plan-path>.
```

- [ ] **Step 3: Verify**

```bash
grep -c '^---$' agents/planner.md          # expect: 2
grep -n 'quick' agents/planner.md          # expect hits in description + steps 1,2,3
grep -n 'fall back to step 9' agents/planner.md   # expect: one hit in step 8
grep -nP '\x{2014}' agents/planner.md      # expect: no output (no em-dashes)
```

- [ ] **Step 4: Commit**

```bash
git add agents/planner.md
git commit -m "feat(agents): add quick-fix fast path to planner intake" -- agents/planner.md
```

### Task 2: full-cycle command quick-path branch

**Files:**
- Modify: `commands/full-cycle.md` (whole body rewrite, 21 to ~30 lines)

**Depends:** none

**Interfaces:**
- Consumes: none
- Produces: `/full-cycle` behavior matching the planner definition from Task 1 (text embedded verbatim; no file-level consumption)

- [ ] **Step 1: Replace the file content**

Replace everything after the frontmatter (keep the `---` fences intact) with:

```
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
```

Also update the frontmatter description (line 2) to:

```
description: Take a request from prompt to shipped change in one run. Small fixes classify at intake into a quick path (one executor with an inline brief, no spec/plan/report artifacts); everything else runs brainstorm (optional) > spec > plan > dispatch the orchestrator to execute, then relay its report. Single-pass, no approval gates. Use `handoff` to print the /execute-plan line for a fresh session instead.
```

- [ ] **Step 2: Verify**

```bash
grep -c '^---$' commands/full-cycle.md      # expect: 2
grep -n '`quick`\|`full`' commands/full-cycle.md   # expect: keyword list + step 1
grep -n 'fall back to step 8' commands/full-cycle.md  # expect: steps 7 and the last paragraph
grep -nP '\x{2014}' commands/full-cycle.md  # expect: no output
```

- [ ] **Step 3: Commit**

```bash
git add commands/full-cycle.md
git commit -m "feat(commands): add quick-fix branch to full-cycle" -- commands/full-cycle.md
```

### Task 3: executor quick-fix dispatch rules

**Files:**
- Modify: `agents/executor.md` (description line 2; intro line 29; new paragraph after line 29)

**Depends:** none

**Interfaces:**
- Consumes: none (the quick-fix rules the planner brief points at, defined here)
- Produces: executor-side rules referenced by the planner (Task 1) and full-cycle (Task 2)

- [ ] **Step 1: Update the description (line 2)**

Replace with:

```
Implements exactly one delegated task from an approved plan, or one quick-fix brief dispatched directly by the planner without a plan file. Reads the relevant files, follows TDD where applicable, edits code, runs verification, and reports what changed and what was verified. Dispatch one executor per plan task, or one per quick fix. Cannot dispatch further subagents.
```

- [ ] **Step 2: Update the intro (line 29) and insert the quick-fix paragraph**

Replace line 29 with:

```
You are an executor: you implement exactly one delegated task from an approved plan, or one quick-fix brief from the planner, then return. You do not dispatch further subagents (the subagent tool is denied) and you do not redesign scope.

Quick-fix brief (no plan file): the brief names the branch, the target files, the fix, and one verification command. Create the branch, implement, verify, and make exactly one Conventional Commit. In the same run: add a changelog `[Unreleased]` entry when the project keeps a `CHANGELOG.md`, and apply the patch version bump when the project's AGENTS.md declares a canonical version source. Scope-creep stop: when the real fix exceeds the brief (more files than the brief names, new logic branches, a new interface, a second task emerging), stop before committing the expanded scope and report back what you found; the planner converts the run to the full pipeline. Never silently expand a quick fix.
```

The inserted paragraph sits between the intro and `For your one task:`.

- [ ] **Step 3: Verify**

```bash
grep -c '^---$' agents/executor.md          # expect: 2
grep -n 'Quick-fix brief' agents/executor.md  # expect: one hit
grep -n 'scope-creep\|Scope-creep' agents/executor.md  # expect: one hit
grep -nP '\x{2014}' agents/executor.md      # expect: no output
```

- [ ] **Step 4: Commit**

```bash
git add agents/executor.md
git commit -m "feat(agents): teach executor quick-fix dispatch without a plan" -- agents/executor.md
```

### Task 4: catalog and roster sync

**Files:**
- Modify: `agents/README.md` (planner row line 9, executor row line 14, paragraph line 23)
- Modify: `README.md` (agents paragraph, line 38)
- Modify: `AGENTS.md` (Agent definitions paragraph, line 112)

**Depends:** none

**Interfaces:**
- Consumes: none (final wording embedded below)
- Produces: catalog consistency required by the repo's doc rules

- [ ] **Step 1: agents/README.md roster rows and paragraph**

In the table row for `planner` (line 9), in the Role cell, append after "Dispatches `explore` for recon.":

```
Classifies small fixes at intake (one obvious fix, about 1-2 files, no design alternatives; `quick`/`full` keywords override) and routes them to a quick path: one executor with an inline brief, no spec/plan/report artifacts.
```

In the table row for `executor` (line 14), in the Role cell, append after "Keeps ponytail suite and `using-git-worktrees`.":

```
Also takes planner-dispatched quick-fix briefs without a plan file: branch, one commit, changelog and patch bump per project conventions, scope-creep stop.
```

In the paragraph (line 23), append one sentence right after "The `planner` gates every plan through `lazy-dev` (lean-plan review, PASS or findings, 2-round cap) before any orchestration starts.":

```
Small fixes skip that machinery: the planner classifies them at intake (`quick` forces the fast path, `full` forces the pipeline) and dispatches a single executor with an inline brief, no spec/plan/report artifacts.
```

- [ ] **Step 2: README.md agents paragraph**

In line 38, append one sentence after "Source of truth in `agents/`; copy each `agents/*.md` to `~/.config/opencode/agents/` to activate.":

```
The planner classifies small fixes at intake and routes them to a quick path: one executor with an inline brief, no spec/plan/report artifacts.
```

- [ ] **Step 3: AGENTS.md Agent definitions paragraph**

In line 112, change "They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run) and `/execute-plan`" to:

```
They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run; small fixes classify at intake into a quick path, one executor with an inline brief and no spec/plan/report artifacts) and `/execute-plan`
```

- [ ] **Step 4: Verify**

```bash
grep -n 'quick path' agents/README.md README.md AGENTS.md   # expect: hits in all three
bin/skillctl check                                          # expect: pass, no new violations
grep -nP '\x{2014}' agents/README.md README.md AGENTS.md    # expect: no output
```

- [ ] **Step 5: Commit**

```bash
git add agents/README.md README.md AGENTS.md
git commit -m "docs(agents): sync catalogs for the quick-fix fast path" -- agents/README.md README.md AGENTS.md
```

## Post-task checks (orchestrator)

- `bin/skillctl check` green.
- `bin/skillctl sync --check` will report the agent/command files STALE for the global config dir; expected, the report tells the user to run `bin/skillctl sync` to activate.
- Documenter writes the execution report and a choices entry for the quick-path decision (this run is itself a full-pipeline feature).
