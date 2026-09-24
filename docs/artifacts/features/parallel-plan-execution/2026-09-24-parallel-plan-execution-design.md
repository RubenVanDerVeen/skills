# Design: Parallel plan execution

- Date: 2026-09-24
- Status: approved (single-pass /full-cycle, no approval gates)
- Feature folder: `docs/artifacts/features/parallel-plan-execution/`
- Plan: `2026-09-24-parallel-plan-execution-plan.md` (same folder)

## Problem

Feature shipping through `/full-cycle` and `/execute-plan` is serial end to end. The orchestrator dispatches one executor, waits, dispatches one reviewer, waits, then moves to the next task. Wall-clock time is the sum of all task durations plus all review durations. The subagent dispatch infrastructure already supports multiple concurrent `task` calls in one turn; the serial constraint is pure convention in the agent and command definitions, not a platform limit.

## Goals

1. Plans express task independence so maximal parallelism is possible. The planner optimizes for decomposing work into independent tasks.
2. Orchestrator dispatches all ready executors in parallel; each task's reviewer starts as soon as that task's own executor returns (pipelined, overlapping sibling executors).
3. Structure reviews (`doc-standardizer`, `code-standardizer`) run in parallel.
4. No git corruption: disjoint file sets per parallel wave, explicit path staging, commit-hash-based review packages.
5. Serial fallback for plans without dependency markers (backwards compatible).

## Non-goals

- Per-executor git worktrees (the multi-plan model stays cross-session; too much ceremony per task in-run).
- Changes to executor/reviewer internals beyond staging discipline and commit-hash reporting.
- Parallelizing steps inside a single task (TDD cycle stays ordered).
- opencode config changes (`subagent_depth` is unchanged: one orchestrator-to-executor level, just several at once).

## Approaches considered

**A. Wave dispatch on the shared branch, plan-declared dependencies plus disjoint file groups (recommended).**
Each task gains a `**Depends:**` line; the orchestrator computes a ready set each turn and dispatches executors concurrently. Reviews are pipelined per task. Git safety comes from the plan guaranteeing disjoint `**Files:**` sets within a wave and executors staging explicit paths. Smallest change surface: edits to five markdown definitions, no new tooling, no new branches.

**B. Per-executor worktrees in-run.** Each parallel executor gets its own worktree and branch; the orchestrator merges back per task. True isolation, but per-worktree dependency installs, merge ceremony, and N branches per plan. The repo's own postmortem (`docs/artifacts/features/code-standardization/2026-08-04-code-standardization-report.md`) says switch to per-executor worktrees only when parallelism is worth the git ceremony. Rejected: heavy for typical plans in a markdown/content repo.

**C. Inference only: no plan format change, orchestrator derives parallel groups from `**Files:**` overlap and Interfaces prose.** Zero planner change, but dependency inference from prose is exactly where a smaller executor-model planner errs, and a wrong inference means cross-contaminated commits. One explicit line per task is cheaper than debugging silent corruption. Rejected.

## Design

### 1. Plan format (planner; `agents/planner.md`)

Every task in a plan carries one line directly after the `**Files:**` block:

```
**Depends:** none
```
or
```
**Depends:** Task 2, Task 3
```

Rules:

- Default to `none`. A task lists a dependency only when it truly consumes an earlier task's output (the Interfaces `Consumes:` block is the litmus test).
- All tasks with `Depends: none` must have mutually disjoint `**Files:**` sets. The planner resolves any overlap either by merging the tasks or by adding a dependency edge.
- When the domain forces a serial chain, the planner maximizes independent branches around the chain (the "as many steps as possible in parallel" requirement).
- Backwards compatibility: a plan with no `Depends:` lines anywhere executes exactly as today, fully serial.

### 2. Orchestrator scheduling (`agents/orchestrator.md`, step 3 and momentum rule)

- **Ready set:** incomplete tasks whose `Depends:` entries are all complete (reviewer-passed).
- **Wave dispatch:** in the same turn, one `task` call per ready task, all concurrent.
- **Pipelined review:** when an executor returns, dispatch its reviewer in that same turn even if sibling executors are still running. The reviewer receives the executor's commit hash and reviews that commit (`git show <hash>`), not a BASE..HEAD range, so interleaved commits from sibling tasks cannot mix into the review package.
- **On reviewer pass:** mark the task complete, recompute the ready set, and dispatch any newly ready executors in the same turn.
- **File-conflict guard:** if two ready tasks have overlapping `**Files:**` sets, run them sequentially regardless of dependencies (files win over plan metadata).
- **Escalation:** unchanged; oracle per task on two strikes.
- **Structure review:** dispatch `doc-standardizer` and `code-standardizer` concurrently (both are read-only against the same branch diff, so there is no conflict). Supersedes the earlier "rejected for sequential simplicity" decision in `docs/artifacts/features/standardizer-split/2026-08-29-standardizer-split-design.md` now that a parallel dispatch mechanism exists anyway. Then one quick-fix `executor` pass and `reviewer` recheck, as today.
- **Fallback:** if the plan contains no `Depends:` lines, execute with the current serial loop.

### 3. Git safety (`agents/executor.md`)

- Stage explicit paths only (`git add <exact files>`); never `git add -A` (lesson from the code-standardization shared-worktree race).
- Exactly one commit per task; the executor reports the commit hash in its result.
- On a git `index.lock` failure (concurrent commit), wait briefly and retry once; if it still fails, report the failure for the orchestrator to re-dispatch. Lock windows are milliseconds, so collisions are rare and retries cheap.

### 4. Command and docs sync

- `commands/execute-plan.md`: rewrite the momentum paragraph to ready-set dispatch (including the serial fallback for plans without `**Depends:**` lines), make its structure-review end step dispatch `doc-standardizer` and `code-standardizer` concurrently (mirroring the orchestrator), and add an explicit override note: this repo's parallel rules supersede the superpowers `subagent-driven-development` skill's serial momentum and its "never dispatch multiple implementation subagents in parallel" red flag, under the disjoint-files guard. The repo-side conventions in `agents/orchestrator.md` are the process of record for execution order.
- `agents/README.md`: workflow paragraph and the orchestrator roster row mention parallel waves.
- `docs/workflows/workflow.md`: update the flow sentence (executor per task, reviewer per task, dispatched in parallel waves when the plan marks tasks independent).

Reviewer, lazy-dev, oracle, documenter, and both standardizer definitions need no changes: reviewer gets its diff via the dispatch prompt anyway (now a hash), and the standardizers already accept "the branch diff".

## Risks

| Risk | Mitigation |
|---|---|
| `index.lock` contention on concurrent commits | retry once; lock windows are milliseconds, collisions rare |
| Executor stages a sibling task's in-flight file | disjoint `**Files:**` per wave (plan guarantee) plus explicit path staging |
| Reviewer mixes tasks' diffs | commit-hash review package instead of ranges |
| Old plans without `Depends:` lines | serial fallback, unchanged behavior |
| Over-parallelizing genuinely coupled tasks | planner rule: dependency required whenever `Consumes:` cites an earlier task; the lazy-dev gate checks the plan |

## Success criteria

- Plans written by the planner carry `**Depends:**` on every task; independent tasks dominate.
- The orchestrator dispatches more than one executor concurrently whenever the ready set has more than one task.
- Reviews overlap with sibling executors rather than waiting for the whole wave.
- Structure reviews run concurrently.
- A plan without dependency markers still executes serially without error.

## Versioning

Root `AGENTS.md` declares no `### Versioning` subsection: unversioned, no bump.
