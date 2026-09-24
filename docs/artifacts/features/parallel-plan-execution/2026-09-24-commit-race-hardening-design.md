# Design: Commit race hardening for parallel waves

- Date: 2026-09-24
- Status: approved (single-pass /full-cycle, no approval gates)
- Feature folder: `docs/artifacts/features/parallel-plan-execution/` (follow-up to `2026-09-24-parallel-plan-execution-design.md`)
- Plan: `2026-09-24-commit-race-hardening-plan.md` (same folder)
- Branch: continues on `feat/parallel-plan-execution` (clean, same topic, unmerged)

## Problem

The wave-1 dogfood run hit the sibling-stage race the first plan predicted: two executors in one parallel wave share one git index. The existing rule "stage explicit paths only, never `git add -A`" was followed, but the window between an executor's `git add` and its `git commit` let a sibling's staged entries get swept into the first commit that landed (observed as bundled commit `9802f08`, repaired by hand via `git reset --soft` + re-stage + sequential commits; documented in the execution report's "Discipline note: the bundled-commit race").

Root cause: a plain `git commit` commits the entire index, and the index is shared by all concurrent executors in one worktree. Explicit staging controls what *you* put in; nothing controls what the commit *takes*.

## Goals

1. Close the race by construction, not by check-then-fix: a commit can only ever contain its own task's paths, no matter what siblings staged.
2. Add a detection backstop so a bundled commit, if it ever happens anyway, is caught and split per the recipe already proven in the dogfood run.
3. Mirror the discipline everywhere executor commit conventions are stated.

## Non-goals

- Orchestrator-owned commits (executors stop committing): changes commit ownership across five definitions for the same guarantee.
- Per-executor worktrees: already rejected in the base design.
- Changes to planner/reviewer/documenter definitions: no commit mechanics there.

## Approaches considered

**A. Pathspec commit (recommended).** Executors commit with a pathspec: `git commit <message> -- <exact files>`. Git's default mode with a pathspec is `--only`: the commit takes exactly those paths from the working tree, disregards all other staged entries, and leaves them staged. A sibling staging mid-flight is now harmless by construction: its entries cannot enter your commit and remain staged for its own pathspec commit. Zero extra commands; one sentence changed per site. No window at all, unlike check-then-fix.

**B. Check-and-unstage before commit.** Immediately before committing: list the index (`git diff --cached --name-only`), unstage sibling paths (`git restore --staged <paths>`, the report's original candidate), then commit. Works, but it is a check-then-fix loop with a residual TOCTOU window between the unstage and the commit (a sibling can stage in between). Strictly weaker than A and more text. Rejected.

**C. Detection only.** Keep plain commits, have the orchestrator detect bundles in `git show --name-only <hash>` and split. Keeps the race; only cleans up after. Rejected as the sole measure, but kept as the backstop (see design).

## Design

Three edits, one concern: commit isolation. All three sites are disjoint files.

### 1. Executor commit discipline (`agents/executor.md`, Parallel safety paragraph, line 37)

Amend the paragraph: after the existing "stage explicit paths only" sentence, commit with a pathspec, `git commit <message> -- <exact files from the task's Files block>`. Git then commits only those paths even if a sibling task's staged entries sit in the shared index, and leaves those entries staged for the sibling's own commit. Existing rules unchanged: one commit per task, index.lock retry, commit hash reported in the result. The preceding `git add <exact files>` stays: it is what makes the pathspec match for newly created files.

### 2. Orchestrator commit-integrity check (`agents/orchestrator.md`, "Per wave:" paragraph, line 47)

New sentence directly after the Pipelined review sentence: commit integrity. Before accepting a review pass, confirm `git show --name-only <hash>` touches exactly the task's `**Files:**` paths. A commit carrying sibling paths is a verification failure: re-dispatch that task's executor to split it (`git reset --soft HEAD~1`, re-stage its own paths, commit again with its pathspec). This encodes the repair the wave-1 run improvised, so it is no longer folklore.

### 3. Command mirror (`commands/execute-plan.md`, commit convention bullet, line 17)

Append to the per-task commit bullet (the one folded into every implementer dispatch): commit with a pathspec, `git commit <message> -- <exact files from the task's Files block>`; a plain `git commit` can sweep a parallel sibling's staged files into your commit.

### Docs

No catalog or workflow-doc changes: none of them state commit invocation mechanics. The documenter adds one line to the existing execution report's discipline note recording that the hardening candidate landed (with the commit hash).

## Risks

| Risk | Mitigation |
|---|---|
| Pathspec commit fails on untracked-only files | prevented: `git add <exact files>` precedes every commit (existing rule); staged paths always match |
| Reviewer flags a commit touching a file absent from the task's `**Files:**` block | that is a plan-accuracy defect; flagging it is correct behavior, not a false positive |
| Pathspec semantics surprise on merge/conflict states | out of scope: plan execution commits onto a linear task branch, never mid-merge |

## Success criteria

- The pathspec-commit discipline appears at all three sites (grepable).
- The orchestrator's commit-integrity check and split recipe are in `agents/orchestrator.md` (grepable).
- A future parallel wave cannot bundle sibling changes into one commit by construction.

## Versioning

Root `AGENTS.md` declares no `### Versioning` subsection: unversioned, no bump.
