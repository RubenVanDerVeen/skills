# Commit race hardening: execution report

Date: 2026-09-24
Branch: `feat/parallel-plan-execution` (follow-up on the base feature's branch)
Plan: `docs/artifacts/features/parallel-plan-execution/2026-09-24-commit-race-hardening-plan.md`
Spec: `docs/artifacts/features/parallel-plan-execution/2026-09-24-commit-race-hardening-design.md`
Base report: `docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-report.md`

## Summary

One-task follow-up to the parallel-plan-execution run. Closes the sibling-stage race documented in the base report's Discipline note: every executor commit is now a pathspec commit (race closed by construction), and the orchestrator gained a commit-integrity check as the detection backstop. Commit `8f2cfd5` was itself a pathspec commit, dogfooding the discipline it ships.

## Branch and commits

| Hash | Subject | Role |
|---|---|---|
| `6d16b6b` | `docs: add race-hardening plan and spec` | orchestrator bootstrap (spec + plan) |
| `8f2cfd5` | `fix(agents): pathspec commits close the sibling-stage race in parallel waves` | Task 1 (executor) |

## What changed

`8f2cfd5`, 3 files, +3/-3:

```
 agents/executor.md       | 2 +-
 agents/orchestrator.md   | 2 +-
 commands/execute-plan.md | 2 +-
```

- `agents/executor.md` (Parallel safety): "Exactly one commit per task" now reads "Exactly one commit per task, and always a pathspec commit (`git commit <message> -- <exact files from the task's Files block>`)", with the shared-index rationale inline.
- `agents/orchestrator.md` (Per wave): new `Commit integrity` sentence directly after the Pipelined review rule: before accepting a review pass, confirm `git show --name-only <hash>` touches exactly the task's `**Files:**` paths; a commit carrying sibling paths is a verification failure, re-dispatch that executor to split it (`git reset --soft HEAD~1`, re-stage its own paths, commit again with its pathspec).
- `commands/execute-plan.md` (per-task commit bullet): appends the same pathspec-commit rule so every implementer dispatch carries it.

## Why it works

A plain `git commit` takes the whole shared index. With a pathspec, git defaults to `--only` semantics: the commit takes exactly the named paths and leaves every other staged entry staged, so a sibling's in-flight staging cannot enter your commit and survives for its own commit. The race closes by construction, no stage-to-commit window and no check-then-fix TOCTOU gap (spec approach A over rejected approach B). The orchestrator's commit-integrity check is the backstop: it encodes the exact `git reset --soft HEAD~1` split recipe the base run improvised, so the repair is codified in the agent definition instead of session folklore.

## Verification evidence

Executor Step 4, all as expected:

- `Select-String -Path agents/executor.md,agents/orchestrator.md,commands/execute-plan.md -Pattern 'pathspec'`: hits at `agents/executor.md:37`, `agents/orchestrator.md:47`, `commands/execute-plan.md:17`.
- `Select-String -Path agents/orchestrator.md -Pattern 'Commit integrity'`: hit at `agents/orchestrator.md:47`.
- Em-dash scan `([char]0x2014)` across all three files: no output.

## Reviewer and standardizers

- Reviewer: PASS, character-for-character match with plan Steps 1-3; commit touches exactly the three Files-block paths; Conventional Commits compliant.
- doc-standardizer: PASS, no findings.
- code-standardizer: PASS, no findings.
- Quick-fix pass: not needed.

## Close-out

No `ponytail:` deferrals. No unverified items. No catalog edits (no skill, agent, or command added or renamed; spec's Docs section required only this report and the base-report note). Versioning: root `AGENTS.md` declares no `### Versioning` subsection, unversioned, no bump.

## Dispatch Log

| Step | Dispatched | Outcome |
|---|---|---|
| Bootstrap (spec + plan) | orchestrator, self-implemented: docs placement, not implementation logic | `6d16b6b` |
| Task 1 (pathspec discipline, three mirror sites) | executor + reviewer | `8f2cfd5`, PASS |
| Structure review | doc-standardizer + code-standardizer, concurrent | both PASS, no findings |
| Quick-fix pass | not needed | none |
| Documentation | documenter (this report + base-report discipline-note append) | this commit |
