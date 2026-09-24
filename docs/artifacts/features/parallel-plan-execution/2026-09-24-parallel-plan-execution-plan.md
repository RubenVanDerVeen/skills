# Parallel Plan Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This repo's parallel-dispatch rules (agents/orchestrator.md after Task 2 of this plan) supersede the skill's serial-momentum red flags; execute this plan's tasks as parallel waves per its `**Depends:**` markers.

**Goal:** Make plan execution parallel: plans declare task dependencies, the orchestrator dispatches ready executors in waves with pipelined reviews, and structure reviews run concurrently.

**Architecture:** Content-only change to five markdown definitions. The planner gains a `**Depends:**` plan-format rule; the orchestrator's step 3 and momentum rule switch from a serial loop to ready-set wave dispatch with per-task pipelined reviews and a serial fallback; the executor gains explicit-path staging, one-commit-per-task with hash reporting, and an index.lock retry; the `/execute-plan` command mirrors the rules and explicitly overrides the superpowers skill's serial red flags; catalog and workflow docs stay truthful.

**Tech Stack:** Markdown only. No build step. Git hooks (`.githooks/`) enforce Conventional Commits, em-dash ban, and SKILL.md frontmatter rules.

**Spec:** `docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-design.md`

## Global Constraints

- No em-dashes (U+2014, `-`) in any edited file. Verify per file with `Select-String -Path <file> -Pattern ([char]0x2014)`; expected: no output.
- Do not touch YAML frontmatter of any agent file except where a task below says so explicitly (no task does).
- Canonical strings (use verbatim wherever referenced): marker line `**Depends:** none` / `**Depends:** Task N`; terms `ready set`, `parallel waves`, `Pipelined review`, `File-conflict guard`.
- Conventional Commits 1.0.0, one commit per task. Stage explicit paths only; never `git add -A`.
- Shell is Windows PowerShell 5.1.
- Versioning: root AGENTS.md declares no `### Versioning` subsection. Unversioned, no bump.

---

### Task 1: Planner writes dependency-ready plans

**Files:**
- Modify: `agents/planner.md` (step 4, the "Plan:" paragraph, around line 47)

**Depends:** none

**Interfaces:**
- Consumes: none
- Produces: the plan-format rule other tasks and the orchestrator rely on: every plan task carries a `**Depends:**` line after its `**Files:**` block; `Depends: none` tasks have disjoint file sets.

- [ ] **Step 1: Read the target paragraph**

Read `agents/planner.md`. Locate the step 4 line beginning `Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/...`.

- [ ] **Step 2: Append the parallel-readiness rule to step 4**

Do not insert a new numbered step and do not renumber anything: appending to step 4 avoids stranding the live cross-references to "step 7" elsewhere in the file (lines mentioning "manual handoff in step 7" and "fall back to step 7"). Directly append to the end of the step 4 line, after "...records 'unversioned, no bump'.":

```markdown
Parallel readiness: every task in the plan carries a `**Depends:**` line (e.g. `**Depends:** none` or `**Depends:** Task 2, Task 3`) directly after its `**Files:**` block. Default to `none`; list a dependency only when the task's Interfaces `Consumes:` block cites an earlier task's output. All `Depends: none` tasks must have mutually disjoint `**Files:**` sets: merge overlapping tasks or add a dependency edge. When the domain forces a serial chain, maximize independent branches around it. The orchestrator dispatches ready tasks in parallel waves (see agents/orchestrator.md).
```

- [ ] **Step 3: Verify**

```powershell
Select-String -Path agents/planner.md -Pattern 'Parallel readiness'
Select-String -Path agents/planner.md -Pattern ([char]0x2014)
```

Expected: first command finds the new line; second returns nothing.

- [ ] **Step 4: Commit**

```powershell
git add agents/planner.md
git commit -m "feat(agents): planner marks plan tasks with Depends for parallel waves"
```

---

### Task 2: Orchestrator wave dispatch with pipelined reviews

**Files:**
- Modify: `agents/orchestrator.md` (step 3 paragraph around line 47, momentum rule line 49, structure-review step line 50)

**Depends:** none

**Interfaces:**
- Consumes: the `**Depends:**` plan marker and disjoint-files guarantee produced by Task 1's planner rule.
- Produces: the ready-set/wave execution model that `commands/execute-plan.md` (Task 4) mirrors and the docs (Task 5) describe.

- [ ] **Step 1: Read the current step 3, momentum, and structure-review lines**

Read `agents/orchestrator.md`. Locate: the "Per task:" paragraph (step 3), the "Momentum:" paragraph (step 5), and the "Structure review" paragraph (step 6).

- [ ] **Step 2: Replace the step 3 paragraph**

Replace the entire "Per task:" paragraph, from "Per task: FIRST action is `task` with `subagent_type: executor`" through "...Self-implementing a task with real logic, branches, or multi-file scope is a process failure - dispatch instead." (that final guard sentence must survive; the repo's documented 2026-08-02 zero-dispatch bypass incident is why it exists), with:

```markdown
Per wave: compute the ready set, meaning all incomplete tasks whose `**Depends:**` entries are complete (reviewer-passed). In the same turn, dispatch one `task` call per ready task with `subagent_type: executor`, each with its task's context folded in. Do not read the task and start editing - dispatch first. Pipelined review: the moment an executor returns, dispatch the reviewer subagent for that task in the same turn, even while sibling executors still run; pass the executor's commit hash and have the reviewer review that commit (`git show <hash>`), not a range. On review pass, mark the task complete, recompute the ready set, and dispatch newly ready executors in the same turn. On changes-requested, re-dispatch that task's executor with the findings. File-conflict guard: if two ready tasks have overlapping `**Files:**` sets, run them sequentially regardless of dependencies; files win over plan metadata. Fallback: if the plan carries no `**Depends:**` lines, execute one task at a time in plan order, reviewer between tasks, as before. Trivial-task fallback unchanged: you may self-implement a one-line fix, but still dispatch the reviewer against your own change and log it as self-implemented in the final report. Self-implementing a task with real logic, branches, or multi-file scope is a process failure - dispatch instead.
```

- [ ] **Step 3: Replace the momentum paragraph**

Replace the "Momentum: dispatch the next task in the same turn a subagent returns. ..." paragraph with:

```markdown
Momentum: dispatch every ready task's executor in the same turn; as subagents return, dispatch their reviewers or the next wave's executors without ending the turn. End the turn only when the plan is done, a verifier failure needs a user decision, or a blocker question cannot be defaulted. ... Your last message in any turn is either the step-9 completion report or a specific decision/blocker request.
```

- [ ] **Step 4: Parallelize the structure review**

In the "Structure review (after the task loop is complete):" paragraph, replace `dispatch the `doc-standardizer` subagent against the branch diff, then the `code-standardizer` subagent against the same diff.` with:

```markdown
dispatch the `doc-standardizer` and `code-standardizer` subagents concurrently (both are read-only against the same branch diff).
```

- [ ] **Step 5: Verify**

```powershell
Select-String -Path agents/orchestrator.md -Pattern 'ready set','Pipelined review','File-conflict guard','concurrently'
Select-String -Path agents/orchestrator.md -Pattern ([char]0x2014)
```

Expected: all four phrases found; second command returns nothing.

- [ ] **Step 6: Commit**

```powershell
git add agents/orchestrator.md
git commit -m "feat(agents): orchestrator dispatches ready executors in parallel waves"
```

---

### Task 3: Executor git safety for concurrent tasks

**Files:**
- Modify: `agents/executor.md` (the commit instructions around line 36)

**Depends:** none

**Interfaces:**
- Consumes: the disjoint-files-per-wave guarantee from the plan format (Task 1).
- Produces: executor result contract used by the orchestrator's pipelined review (Task 2): one commit per task, commit hash reported in the result.

- [ ] **Step 1: Read the commit section**

Read `agents/executor.md`. Locate the line "Commit with Conventional Commits 1.0.0 when the task is green."

- [ ] **Step 2: Extend the commit instructions**

Directly after that line, add:

```markdown
Parallel safety: stage explicit paths only (`git add <exact files from the task's Files block>`); never `git add -A`, because sibling tasks may be running concurrently in the same tree. Exactly one commit per task. If git reports an index.lock failure, wait about two seconds and retry once; if it still fails, stop and report the failure. Report the commit hash in your result so the reviewer can review exactly that commit.
```

- [ ] **Step 3: Verify**

```powershell
Select-String -Path agents/executor.md -Pattern 'index.lock','commit hash'
Select-String -Path agents/executor.md -Pattern ([char]0x2014)
```

Expected: both phrases found; second command returns nothing.

- [ ] **Step 4: Commit**

```powershell
git add agents/executor.md
git commit -m "feat(agents): executor stages explicit paths and reports commit hash for parallel waves"
```

---

### Task 4: /execute-plan mirrors the parallel rules

**Files:**
- Modify: `commands/execute-plan.md` (process sentence near line 5, momentum paragraph at line 19, structure-review end step around line 22)

**Depends:** none

**Interfaces:**
- Consumes: the orchestrator rules from Task 2 (ready set, Pipelined review, File-conflict guard, concurrent structure review) and the executor contract from Task 3.
- Produces: standalone-command parity; the explicit override of the superpowers skill's serial red flags.

- [ ] **Step 1: Read the current text**

Read `commands/execute-plan.md` in full.

- [ ] **Step 2: Add the override note**

In the first body paragraph, directly after "the items below are project-specific defaults and conventions the skill does not cover.", append a new sentence:

```markdown
Execution-order override: this repo runs executor/reviewer work in parallel waves per `agents/orchestrator.md` (ready-set dispatch, disjoint `**Files:**` per wave, hash-based reviews). Where the `subagent-driven-development` skill mandates serial momentum or forbids dispatching multiple implementation subagents in parallel, those repo rules supersede it; tasks whose `**Files:**` overlap still run sequentially.
```

- [ ] **Step 3: Replace the momentum paragraph**

Replace the paragraph beginning "Momentum: when a subagent returns, dispatch the next task's subagent in the same turn." with:

```markdown
Momentum: a task is ready when every task listed in its `**Depends:**` line is reviewer-passed. Dispatch every ready task's executor concurrently in the same turn; as each executor returns, dispatch its reviewer in the same turn so reviews overlap sibling executors. When a reviewer passes, mark the task complete and dispatch newly ready executors immediately. Fallback: if the plan carries no `**Depends:**` lines, execute one task at a time in plan order, reviewer between tasks, as before. Never end the turn to report intermediate progress or wait for a 'continue'; end the turn only when the plan is complete, a verifier failure needs a user decision, or a genuine scope question blocks every remaining task.
```

- [ ] **Step 4: Parallelize the structure-review end step**

In the end-step sentence "...then `code-standardizer` against the same diff" (line 22; note: no "the" and no "subagent" before `code-standardizer`, unlike the orchestrator's wording), replace the fragment "then `code-standardizer` against the same diff" with:

```markdown
and `code-standardizer` concurrently (both are read-only against the same branch diff) against the same diff
```

- [ ] **Step 5: Verify**

```powershell
Select-String -Path commands/execute-plan.md -Pattern 'Execution-order override','Depends','concurrently'
Select-String -Path commands/execute-plan.md -Pattern 'then .code-standardizer.'
Select-String -Path commands/execute-plan.md -Pattern ([char]0x2014)
```

Expected: first command finds all three phrases; second returns nothing (serial residue gone); third returns nothing.

- [ ] **Step 6: Commit**

```powershell
git add commands/execute-plan.md
git commit -m "feat(commands): execute-plan dispatches ready tasks in parallel waves"
```

---

### Task 5: Docs and catalogs stay truthful

**Files:**
- Modify: `agents/README.md` (orchestrator roster row around line 11, workflow paragraph around line 22)
- Modify: `docs/workflows/workflow.md` (orchestrator flow sentence around line 117)

**Depends:** Task 2, Task 4

**Interfaces:**
- Consumes: the final wording shipped by Tasks 2 and 4 (wave dispatch, pipelined reviews, concurrent structure review); its verify step greps those files' post-edit state, so it runs after them (wave 2).
- Produces: catalog entries matching the new behavior.

- [ ] **Step 1: Read both targets**

Read `agents/README.md` and `docs/workflows/workflow.md`. Locate the orchestrator roster row, the workflow paragraph mentioning `/execute-plan` dispatch, and the workflow.md sentence beginning "...then runs its 8-step loop: `executor` per task, `reviewer` after each...".

- [ ] **Step 2: Update the orchestrator roster row**

In `agents/README.md`, change the orchestrator row's description (keep the row's existing usage sentence about standalone `/execute-plan` and planner-dispatched single-pass `/full-cycle`) so the description reads:

```markdown
Executes approved plans: dispatches executor/reviewer work in parallel waves (ready-set dispatch), pipelines each reviewer against its own task's commit, escalates two-strike failures to oracle, commits at boundaries via bash. Session agent for standalone /execute-plan and dispatchable by the planner for single-pass /full-cycle.
```

- [ ] **Step 3: Update the workflow paragraph**

In the same file's workflow paragraph, inside the sentence describing `/execute-plan` dispatch ("...dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, ..."):

1. After "reviews to `reviewer`", insert:

```markdown
(dispatched in parallel waves: executors for all ready tasks at once, each reviewer pipelined as its own executor returns)
```

2. In the same sentence, flip the serial residue "post-implementation structure review to `doc-standardizer` then `code-standardizer`" to "post-implementation structure review to `doc-standardizer` + `code-standardizer`, dispatched concurrently".

- [ ] **Step 4: Update workflow.md**

In `docs/workflows/workflow.md`:

1. Replace the sentence fragment "`executor` per task, `reviewer` after each," with:

```markdown
parallel waves of `executor` tasks (plans carry `**Depends:**` markers; tasks without them run serially) with a `reviewer` pipelined per task as each executor returns,
```

2. In the same sentence, replace "`doc-standardizer` then `code-standardizer` structure review (repo structure first, then code structure)" with "`doc-standardizer` + `code-standardizer` structure review run concurrently".

3. Sweep the remaining serial-dispatch wording in the same file (around lines 87 and 97): find any other occurrences of "`executor` per task" / "`reviewer` after each"-style fragments and apply the same wave wording as in item 1.

- [ ] **Step 5: Verify**

```powershell
Select-String -Path agents/README.md,docs/workflows/workflow.md -Pattern 'parallel waves','concurrently'
Select-String -Path agents/README.md,docs/workflows/workflow.md,agents/orchestrator.md,commands/execute-plan.md -Pattern 'then .code-standardizer.'
Select-String -Path agents/README.md,docs/workflows/workflow.md -Pattern ([char]0x2014)
```

Expected: first command finds the phrases in both files; second returns nothing across all four files (no serial residue left); third returns nothing.

- [ ] **Step 6: Commit**

```powershell
git add agents/README.md docs/workflows/workflow.md
git commit -m "docs: sync agent catalogs and workflow doc for parallel plan execution"
```
