# Execution report: `/standardize` explore-patch-verify flow + grep-gated bootstrap

- **Date:** 2026-08-14
- **Status:** complete
- **Branch:** `feat/standardize-flow` (skills repo)
- **Spec:** [2026-08-12-standardize-flow-design.md](./2026-08-12-standardize-flow-design.md)
- **Plan:** [2026-08-12-standardize-flow-plan.md](./2026-08-12-standardize-flow-plan.md)

## Overview

The `project-standardization` skill now gates every bootstrap step on a literal-grep verification predicate, `/standardize` auto-branches between fresh bootstrap (linear, unchanged) and restructure (three-subagent explore-patch-verify flow), and the new flow was proven end-to-end against the klad repo. Two predicate defects found during the klad exercise were fixed on the feature branch (`e835559`); one minor predicate brittleness is recorded as a follow-up. The plan said `2026-08-12-<slug>-report.md`; this file is dated `2026-08-14` per the actual run date, at the user's direction.

## Branch and commits

Skills repo, `feat/standardize-flow`, oldest first:

| Commit | Description |
|--------|-------------|
| `94bf4e3` | `docs(agents): add Artifacts and Git workflow sections to repo AGENTS.md` (pre-existing in-flight `AGENTS.md` change on `main`, committed separately before the first task per the plan's staging note; not part of any task) |
| `000df87` | `docs: add plan and spec for standardize-flow` |
| `6cd7ac6` | `feat(standardization): gate each bootstrap step on a literal-grep verification predicate` (Task 1) |
| `eb43d20` | `feat(standardization): add restructure-flow reference for explore-patch-verify dispatch` (Task 2) |
| `f47c8ec` | `feat(standardization): branch /standardize on fresh vs restructure detection` (Task 3) |
| `e835559` | `fix(standardization): correct step 5 tier-assertion and step 9 header-? predicate` (Task 4 predicate fix loop) |

`git diff --stat main..HEAD`:

```
 AGENTS.md                                                                      |  11 +
 commands/standardize.md                                                        |  13 +-
 docs/artifacts/features/standardize-flow/2026-08-12-standardize-flow-design.md | 121 ++++++++
 docs/artifacts/features/standardize-flow/2026-08-12-standardize-flow-plan.md   | 341 +++++++++++++++++++++
 skills/rubens-project-standardization/SKILL.md                                 |   1 +
 skills/rubens-project-standardization/references/bootstrap.md                  |  22 ++
 skills/rubens-project-standardization/references/restructure-flow.md           |  33 ++
 7 files changed, 533 insertions(+), 9 deletions(-)
```

No new skill was added, so no catalog rows changed (per the spec's files-touched table: README.md and AGENTS.md current-skills unchanged).

klad repo (`C:\Users\ruben\Projects\Tools\klad`, branch `feat/typst-preview`), pre-flight base `8e37895`:

| Commit | Description |
|--------|-------------|
| `8e37895` | `docs(standards): wire SemVer 2.0.0 into changelog, standards, agents` (pre-flight SemVer commit sanctioned by the plan) |
| `6b0dc6b` | `docs(agents): declare tier in klad AGENTS.md Overview` (patch phase, closes step 5) |
| `350dbb3` | `feat(memory): seed klad MEMORY.md with user and project-typst-preview entries` (patch phase, closes step 7) |

`git diff --name-only 8e37895..HEAD` (klad): `AGENTS.md`, `MEMORY.md`. Both within the gap-list paths. klad was not pushed.

## Per-task summary

### Task 1: grep-gate predicates in `bootstrap.md`

- Added the `## Branch: fresh vs restructure` note after the title (fresh = linear walk with inline predicates; restructure = dispatch `references/restructure-flow.md`; rule: a requirement edit and its `Verification:` predicate land in the same edit).
- Added a `Verification:` sub-bullet to each of the 12 numbered steps (including 8.1), using the exact predicate text from the plan table. `bootstrap.md` grew from 34 to 56 lines.
- Structural self-check: 12 numbered top-level steps, 15 `Verification:` lines (12 steps + step 8.1 + two textual mentions in the branch note), em-dash scan empty.
- Committed alone as `6cd7ac6`; staged set verified to contain only `bootstrap.md`.

### Task 2: `references/restructure-flow.md` + `SKILL.md` wiring

- Created `references/restructure-flow.md` (33 lines): why three agents (the klad skip report's memory-shortcut failure mode), explore (read-only gap report), patch (executor, per-gap-cluster commits, no inline file moves), verify (reviewer re-runs predicates with fresh context), two-strike oracle escalation, filesystem-move exclusion (flag, not fail; `/standardize-migrate` owns moves), and the POSIX translation note for the PowerShell predicates.
- Added one row to the `SKILL.md` References table in alphabetical position between `migration.md` and `small.md`.
- `Test-Path` on the new file returns True; `Select-String 'restructure-flow' SKILL.md` returns one hit in the References table.
- Committed as the two files only, `eb43d20`. The fresh-bootstrap path never loads the new reference (token budget constraint held).

### Task 3: `commands/standardize.md` branch body

- Replaced the 7-step linear list with the branch-aware body: triage states tier AND branch; fresh walks `references/bootstrap.md` linearly with inline predicates; restructure dispatches the explore-patch-verify flow from `references/restructure-flow.md`. Frontmatter description unchanged (already says "Bootstrap or restructure"); `$ARGUMENTS` tier override preserved.
- Line count after edit: 12 lines, under the 25-line cap.
- Committed alone as `f47c8ec`.

### Task 4: klad end-to-end validation

- Pre-flight: klad status matched the skip-report shape; the pending SemVer fix set committed as one sanctioned commit (`8e37895`); pre-flight base recorded. klad's pre-existing modified `.gitignore` was left untouched per the plan.
- Explore (read-only): produced the 12-step gap report below, every non-reasoning step with literal command output. Two fails found: step 5 (tier not declared in AGENTS.md, surfaced after the predicate fix; original predicate falsely passed) and step 7 (MEMORY.md absent).
- Patch (executor): two commits in klad, `6b0dc6b` (tier line in AGENTS.md Overview, un-bolded `- Tier: medium.` so the predicate matches) and `350dbb3` (seed MEMORY.md, 7 lines).
- Verify (reviewer, read-only): step 5 closed (`Select-String -Path AGENTS.md -Pattern 'Tier:\s*(small|medium|large)'` hit at line 4); step 7 closed (`Test-Path MEMORY.md` True, 7 non-empty lines); steps 4, 6, 8, 8.1, 9, 10, 11 re-confirmed pass. No still-fails, no oracle escalation.
- Predicate fix loop fired once (two defects, one commit `e835559`), see next section.
- Closure criteria all hold: 12 steps accounted for with literal outputs; every explore fail closed in verify; legacy buckets flagged, not moved; klad log shows only Conventional Commits; klad diff stays within gap-list paths.

## klad gap report (explore phase, with final state)

| Step | Explore (pre-patch) | Final (post-patch, post-verify) |
|------|---------------------|--------------------------------|
| 1. Triage | reasoning step, skipped (tier-not-stated flag) | closed via `6b0dc6b` (tier now declared) |
| 2. Read tier reference | reasoning step, skipped | n/a (agent-internal) |
| 3. Apply standards | decision step (verified via step 9) | pass (via step 9) |
| 4. AGENTS.md + CLAUDE.md shim | pass | pass (re-confirmed) |
| 5. `.agents/` | fail (after predicate fix; original explore showed pass) | closed (`6b0dc6b`) |
| 6. `docs/artifacts/` | pass (legacy bucket flags) | pass (flagged, not moved) |
| 7. Memory | fail | closed (`350dbb3`) |
| 8. CHANGELOG.md | pass | pass (re-confirmed) |
| 8.1 Versioning | pass | pass (re-confirmed) |
| 9. STANDARDS.md | pass (under original predicate; new predicate also passes) | pass |
| 10. commit-msg hook | pass | pass (re-confirmed) |
| 11. graphify | pass | pass (re-confirmed) |
| 12. Token budget | not verified (no context indicator in shell) | not verified; on-disk AGENTS.md is 60 lines, under the 80-line cap |

klad flags (flags, not fails): legacy artifact buckets `docs/artifacts/{specs,plans,multi-plans}` still present (resolution is `/standardize-migrate`); stray historical checklists under `docs/artifacts/reviews/` flagged for the same reason; `command -v graphify` empty in the verify shell but `graphify-out/graph.json` exists, so the conditional step 11 predicate still applies and passes.

## Predicate fixes

Committed in `e835559` (both in one commit):

1. **Step 5 tier assertion (missing).** The original predicate only checked `.agents/` existence and contents; it never asserted the tier is declared in AGENTS.md, so klad's missing tier line falsely passed. Tightened to also require `Select-String -Pattern 'Tier:\s*(small|medium|large)' AGENTS.md` to return a hit. This flipped klad's step 5 to fail and added patch commit `6b0dc6b`.
2. **Step 9 header-`?` false positive.** The original row-scan matched the markdown table's header and separator rows, which contain no data cells, so a header-only or separator-adjacent `?`/blank could be miscounted. Tightened to skip header + separator via `Select-String -Pattern '^\|' | Select-Object -Skip 2`. Klad still passes (no data-row blanks or `?` cells).

Noted but NOT fixed (follow-ups):

- **Step 5 bold-marker brittleness:** `Tier:\s*(small|medium|large)` does not match `**Tier:** medium.` because `**` intervenes between colon and whitespace. The patch executor worked around it by committing the un-bolded form in klad. Candidate fix: allow optional emphasis (`Tier:\*{0,2}\s*(small|medium|large)`). Deferred to avoid further klad commit churn.
- **Step 4 line-cap unenforced:** the body requires AGENTS.md under 80 lines (small/medium) or 200 (large); the predicate checks presence + shim line only. Soft target, not a defect.
- **Step 5 tier-template check missing:** predicate does not assert `.agents/` contents match tier expectations (medium: `todolist.md`; large: per-domain files). Out of scope for this fix loop.

## Em-dash scan results

Commands run (literal):

```powershell
(Get-ChildItem -Recurse -Include *.md -Path skills\rubens-project-standardization | Select-String -Pattern ([char]0x2014))
(Get-ChildItem -Recurse -Include *.md -Path commands | Select-String -Pattern ([char]0x2014))
```

Output: empty (both). klad's two touched files (`AGENTS.md`, `MEMORY.md`) also scanned clean.

## Structural verification outputs

| Check | Command (equiv.) | Result |
|-------|------------------|--------|
| Task 1: numbered steps | `Select-String -Pattern '^\d+\.' bootstrap.md` count | 12 |
| Task 1: verification lines | `Select-String -Pattern 'Verification:' bootstrap.md` count | 15 (>= 12 required) |
| Task 1: bootstrap.md length | `(Get-Content bootstrap.md).Count` | 56 lines (was 34) |
| Task 2: file exists | `Test-Path references/restructure-flow.md` | True |
| Task 2: SKILL.md wiring | `Select-String 'restructure-flow' SKILL.md` | 1 hit (References table) |
| Task 3: command length | `(Get-Content commands/standardize.md).Count` | 12 lines (cap 25) |
| Em-dash scans | see above | empty |

## Skills loaded

- `using-superpowers`: auto-loaded; establishes the skill-first workflow.
- `subagent-driven-development`: per the plan's required sub-skill header; drove the task-by-task dispatch pattern.
- `ponytail` (full mode): per the plan and repo convention; shortest working diffs, explicit deferral notes.
- `using-git-worktrees`: referenced by `commands/execute-plan.md`; loaded but not needed (plain feature branch used).
- `project-standardization`: the skill being modified; referenced by the plan and `commands/standardize.md`.

## ponytail: deferrals

- Standardizer dispatch skipped: the plan marked it optional ("most of this plan is markdown; full standardizer pass may be skipped"). The plan's override of the orchestrator default was honored.
- Step 5 bold-marker predicate defect left unfixed: the un-bolded tier line works; fixing the regex now would force another klad commit round. Future predicate-fix candidate.
- Step 4 line-cap and step 5 tier-template predicates not added: soft targets and out of scope for this fix loop; noted above.

## Unverified

- Step 12 token budget: no `/context` indicator available in the verification shell. On-disk klad AGENTS.md is 60 lines, well under the 80-line cap; actual session token count unknown.
- POSIX translation of the predicates: `restructure-flow.md` documents the `grep` / `test -f` / `find` equivalents, but they were not exercised; the active shell is Windows PowerShell.
- klad's modified `.gitignore`: pre-existing dirty state, not in the gap list, left untouched per the plan ("Any OTHER dirty files in klad: leave untouched, list them in the report").
- Legacy bucket moves: intentionally not performed or verified beyond flagging; `/standardize-migrate` owns that flow (per the plan's closure criterion, flagged-to-user was the requirement, and it was met).

## Dispatch log

| Task | Dispatch |
|------|----------|
| Task 1 (bootstrap.md predicates) | dispatched: executor + reviewer |
| Task 2 (restructure-flow.md + SKILL.md) | dispatched: executor + reviewer |
| Task 3 (standardize.md branch body) | dispatched: executor + reviewer |
| Task 4 pre-flight (klad SemVer commit) | self-implemented by orchestrator (single sanctioned commit) |
| Task 4 explore phase | dispatched: explore (read-only, workdir klad) |
| Task 4 patch phase | dispatched: executor (workdir klad) |
| Task 4 verify phase | dispatched: reviewer (read-only, workdir klad) |
| Task 4 predicate fix loop | self-implemented by orchestrator (two predicate corrections, commit `e835559`, re-run against klad) |
| Standardizer (optional structure pass) | skipped per plan option |
| Documentation/report | dispatched: documenter (this report) |
