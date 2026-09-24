# Parallel plan execution: execution report

Date: 2026-09-24
Branch: `feat/parallel-plan-execution` (from `main` at `f28316c`)
Plan: `docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-plan.md`
Spec: `docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-design.md`

## Summary

Plan execution was serial end to end: the orchestrator dispatched one executor, waited, dispatched one reviewer, waited, repeated, so wall-clock time was the sum of all task and review durations even when tasks were independent. The dispatch infrastructure already supports concurrent `task` calls; the serial constraint was pure convention in the agent and command definitions.

This feature makes execution parallel on the shared branch (spec approach A, wave dispatch with plan-declared dependencies):

- The planner (`agents/planner.md`) marks every plan task with a `**Depends:**` line and guarantees mutually disjoint `**Files:**` sets among `Depends: none` tasks.
- The orchestrator (`agents/orchestrator.md`) computes a ready set each turn, dispatches one executor per ready task concurrently, pipelines each task's reviewer the moment its own executor returns (reviewing that task's commit hash via `git show <hash>`, never a range), guards against file overlap, and runs the two structure reviewers concurrently.
- The executor (`agents/executor.md`) stages explicit paths only, commits exactly once per task, retries once on `index.lock`, and reports its commit hash.
- `/execute-plan` (`commands/execute-plan.md`) mirrors the rules and explicitly overrides the superpowers `subagent-driven-development` skill's serial-momentum red flags.
- Plans without `**Depends:**` lines keep the old serial loop: backwards compatible.

Content-only change: five agent/command definitions plus two doc files, no tooling, no new branches. The run dogfooded the feature: Tasks 1-4 were dispatched in one parallel wave per the new rules.

### Approaches considered and rejected

- **B. Per-executor worktrees in-run.** True isolation, but per-worktree dependency installs, merge ceremony, and N branches per plan. The code-standardization postmortem says switch to worktrees only when parallelism is worth the git ceremony; heavy for a markdown/content repo. The multi-plan model stays cross-session. Rejected.
- **C. Inference only (no plan format change).** The orchestrator would derive parallel groups from `**Files:**` overlap and Interfaces prose. Dependency inference from prose is exactly where a smaller executor-model planner errs, and a wrong inference means cross-contaminated commits. One explicit `**Depends:**` line per task is cheaper than debugging silent corruption. Rejected.

## Branch and commits

| Hash | Subject | Task |
|---|---|---|
| `95f0d9c` | `docs: add plan and spec for parallel-plan-execution` | orchestrator bootstrap (documents, plan, spec) |
| `281b5b6` | `feat(commands): execute-plan dispatches ready tasks in parallel waves` | Task 4 |
| `9aa93c7` | `feat(agents): orchestrator dispatches ready executors in parallel waves` | Task 2 |
| `f163533` | `feat(agents): planner marks plan tasks with Depends for parallel waves` | Task 1 |
| `00d6b03` | `feat(agents): executor stages explicit paths and reports commit hash for parallel waves` | Task 3 |
| `efde9c7` | `docs: sync agent catalogs and workflow doc for parallel plan execution` | Task 5 |
| `49a6939` | `fix(agents): drop momentum elision marker and sync stale serial dispatch wording` | post-task quick-fix (code-standardizer findings) |

Chronology note: Tasks 1-4 all ran in one parallel wave, so their commits interleave in non-numeric order. A race in that wave bundled Task 2's and Task 4's changes into a single commit; the orchestrator split it before Task 5 landed (see Discipline note), which is why Task 4's commit (`281b5b6`) precedes Task 2's (`9aa93c7`) in history. The plan file lists tasks in numeric order.

## Files changed

10 files, +403/-14 (`git diff main...feat/parallel-plan-execution --stat`):

```
 AGENTS.md                                        |   2 +-
 agents/README.md                                 |   4 +-
 agents/executor.md                               |   1 +
 agents/orchestrator.md                           |   6 +-
 agents/planner.md                                |   2 +-
 commands/execute-plan.md                         |   6 +-
 commands/full-cycle.md                           |   2 +-
 docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-design.md | 102 +
 docs/artifacts/features/parallel-plan-execution/2026-09-24-parallel-plan-execution-plan.md   | 286 +
 docs/workflows/workflow.md                       |   6 +-
 10 files changed, 403 insertions(+), 14 deletions(-)
```

Per task:

- Task 1: appended the `Parallel readiness:` rule to step 4 of `agents/planner.md` (no new numbered step, so live cross-references to step 7 stay valid).
- Task 2: replaced `agents/orchestrator.md` step 3 (ready-set wave dispatch, `Pipelined review`, `File-conflict guard`, serial fallback; the self-dispatch guard sentence survived), the momentum rule, and the structure-review step (concurrent dispatch).
- Task 3: appended the `Parallel safety:` paragraph to `agents/executor.md` after the Conventional Commits line.
- Task 4: added the `Execution-order override` note, replaced the momentum paragraph, and parallelized the structure-review end step in `commands/execute-plan.md`.
- Task 5: synced `agents/README.md` (orchestrator roster row + workflow paragraph) and `docs/workflows/workflow.md` (wave wording in the 8-step loop sentence, concurrent structure review).
- Quick-fix (`49a6939`): removed a literal `...` elision marker shipped verbatim from the plan's momentum replacement in `agents/orchestrator.md`, and swept the two live dispatch-site docs the plan's verify step missed (`AGENTS.md`, `commands/full-cycle.md`).

## Standardization review

Both audits dispatched concurrently against the branch diff:

- **doc-standardizer**: PASS, zero findings.
- **code-standardizer**: 2 quick-fix findings, both fixed in `49a6939`:
  1. `agents/orchestrator.md` shipped a literal `...` elision marker copied verbatim from the plan's replacement text for the momentum paragraph.
  2. Two live dispatch-site docs (root `AGENTS.md`, `commands/full-cycle.md`) still carried serial structure-review wording; the plan's verify step swept only four of the six dispatch-site docs.

Nothing remains open from either audit. One out-of-scope hardening candidate is recorded in the Discipline note below.

## Documentation updates

- `agents/README.md`, `docs/workflows/workflow.md`: Task 5 (`efde9c7`), catalog and workflow sync for wave dispatch.
- `AGENTS.md`, `commands/full-cycle.md`: quick-fix (`49a6939`), serial-residue sweep.
- Root `README.md`: checked by the documenter. It is a skill listing plus a generic agent paragraph; it carries no per-task dispatch workflow wording, so it needs no parallel-waves sync. Left unchanged.
- No skill, command file, or agent was added, removed, or renamed by this feature, so no catalog rows were required (`README.md` / `AGENTS.md` skills tables, `opencode-install.md` name references, `external-skills.md` rows all untouched by design).
- Versioning: root `AGENTS.md` declares no `### Versioning` subsection. Unversioned, no bump.

## Verifier output

All checks run from the branch head, all PASS:

- Em-dash scan across the branch diff: empty.
- `agents/orchestrator.md` contains `ready set`, `Pipelined review`, `File-conflict guard`, `concurrently`.
- `commands/execute-plan.md` contains `Execution-order override`, `Depends`, `concurrently`.
- `agents/README.md` and `docs/workflows/workflow.md` contain `parallel waves`, `concurrently`.
- Serial residue scan for `then `code-standardizer.`` across all six live dispatch-site docs (`agents/orchestrator.md`, `commands/execute-plan.md`, `agents/README.md`, `docs/workflows/workflow.md`, `AGENTS.md`, `commands/full-cycle.md`): empty.
- Elision marker `... Your last message` removed from `agents/orchestrator.md`.
- Every commit on the branch uses a Conventional Commits 1.0.0 message.

## Skills loaded

Across the run: `ponytail` (level full, active throughout), `using-superpowers`, `executing-plans`, `subagent-driven-development`. The last one's serial-momentum red flags were explicitly overridden by this repo's new parallel rules, exactly the override Task 4 codified in `commands/execute-plan.md`.

## Success criteria (spec, all met)

| Criterion | Status |
|---|---|
| Plans written by the planner carry `**Depends:**` on every task; independent tasks dominate | Met: rule shipped in `f163533`; this plan itself already carries `**Depends:**` on every task (dogfooded) |
| Orchestrator dispatches more than one executor concurrently whenever the ready set has more than one task | Met: Tasks 1-4 dispatched in one wave during this very run |
| Reviews overlap with sibling executors rather than waiting for the whole wave | Met: pipelined reviewer dispatch per returning executor, review package pinned to that executor's commit hash |
| Structure reviews run concurrently | Met: `doc-standardizer` + `code-standardizer` dispatched concurrently for this run |
| A plan without dependency markers still executes serially without error | Met: the serial fallback preserves the previous loop verbatim for marker-less plans; it is a zero-behavior-change path, so the shipped wording is the guarantee |

## Risks, retroactively evaluated

| Spec risk | Observed |
|---|---|
| `index.lock` contention on concurrent commits | Not observed. No lock failures fired during the wave; the retry-once rule shipped but was not exercised. |
| Executor stages a sibling task's in-flight file | Partially observed, different vector than predicted: see Discipline note. Explicit-path staging was followed, but the stage-to-commit race window bundled a sibling's staged file into the first-landing commit (`9802f08`). Resolved by the orchestrator's commit split. |
| Reviewer mixes tasks' diffs | Not observed; hash-based review packages were used throughout. |
| Old plans without `Depends:` lines | Covered by the serial fallback; not exercised in-run because this plan uses markers. |
| Over-parallelizing genuinely coupled tasks | Not observed; the disjoint-files guarantee held for the wave; the lazy-dev gate is unchanged. |

## Discipline note: the bundled-commit race

Tasks 1-4 were dispatched in one parallel wave, dogfooding the feature being built. During that wave a race produced commit `9802f08`: Task 2's `agents/orchestrator.md` edits (staged, not yet committed by its executor) were swept into Task 4's commit, which landed first and carried Task 4's message with both tasks' changes. The orchestrator detected this while reviewing the wave's git log and split the bundled commit into the plan-prescribed per-task commits (`281b5b6` and `9aa93c7`) via `git reset --soft` plus `git restore --staged` plus sequential explicit-path commits. File content was preserved byte-for-byte; only commit boundaries changed.

This is the exact sibling-stage race the Task 3 parallel-safety paragraph warns about. The new rule "stage explicit paths only, never `git add -A`" was followed, but the window between one executor staging and committing still allowed the bundle. Follow-up hardening candidate, out of scope for this plan: add `git restore --staged <sibling paths>` to the executor's race-avoidance guidance so an executor unstages anything it did not stage itself immediately before committing.

Update 2026-09-24: the hardening candidate landed via commit `8f2cfd5`, superseded by a stronger fix than the unstage suggestion above. Every executor commit is now a pathspec commit (`git commit <message> -- <exact files>`): git's `--only` semantics mean a sibling's staged entries cannot enter your commit and stay staged for the sibling, closing the race by construction rather than check-then-fix. The orchestrator now performs the commit-integrity check as the backstop, encoding the same `git reset --soft HEAD~1` split recipe this run improvised. Details: `2026-09-24-commit-race-hardening-report.md`.

## `ponytail:` deferrals

None. Shortest working diff throughout (six edited lines per file at most); no `ponytail:` comments added.

## Unverified items

None.

## Dispatch Log

| Step | Dispatched | Outcome |
|---|---|---|
| Branch setup + docs commit | orchestrator | `95f0d9c` |
| Task 1 (planner rule) | executor + reviewer (pipelined) | `f163533`, PASS |
| Task 2 (orchestrator waves) | executor + reviewer (pipelined) | `9aa93c7`, PASS (landed after the race-bundled commit split, see Discipline note) |
| Task 3 (executor git safety) | executor + reviewer (pipelined) | `00d6b03`, PASS |
| Task 4 (/execute-plan parity) | executor + reviewer (pipelined) | `281b5b6`, PASS (landed after the same split) |
| Race-bundled commit split | orchestrator, self-implemented: pure git plumbing (`git reset --soft` + `git restore --staged` + sequential explicit-path commits), no file content changes, diff preserved exactly | `9802f08` split into `281b5b6` + `9aa93c7` |
| Task 5 (docs sync) | executor + reviewer (pipelined) | `efde9c7`, PASS |
| Structure review | doc-standardizer + code-standardizer, dispatched concurrently | doc-standardizer PASS; code-standardizer 2 quick-fix findings |
| Quick-fix pass | executor + reviewer | `49a6939`, PASS |
| Documentation | documenter (this report) | this commit |
