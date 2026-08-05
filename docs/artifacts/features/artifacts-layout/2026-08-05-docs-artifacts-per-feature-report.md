# docs/artifacts per-feature layout migration report

## Summary

**Status: PASS.** The `docs/artifacts/` tree was reorganized from a type-bucket split (`specs/`, `plans/`, `multi-plans/`, `reports/`) into a per-feature split: one flat `features/<feature>/` container per piece of work, plus `reviews/` kept flat at the top. Every artifact file (33 total) moved via `git mv` with basenames preserved exactly; every active reference (generators, layout docs, templates, cross-references) was rewritten; the verification grep returns zero hits outside the four intentional historical categories. The standardizer review returned two quick-fix items (both fixed) and zero recommendations. The only leftover is an empty phantom `docs/artifacts/reports/` directory that the Nextcloud sync client holds open and that git no longer tracks.

## Branch and commits

- **Branch:** `feat/docs-artifacts-per-feature` (branched from `main`).
- **Commit count:** 10 (excluding this report).
- **Diffstat (`main..HEAD`):** 56 files changed, 545 insertions(+), 230 deletions(-).
- **Renames:** 33 pure directory moves (rename scores R069 to R100); every basename is byte-identical to its pre-migration name.

### Commit list (execution order, oldest first)

| # | Hash | Subject | Phase |
|---|------|---------|-------|
| 1 | `f4fa6d7` | `docs: add plan and spec for docs/artifacts per-feature layout` | Preflight |
| 2 | `9e8be2e` | `docs(artifacts): reorganize docs/artifacts into per-feature layout` | Task 1 (move) |
| 3 | `c99331a` | `docs(skills): point generators at docs/artifacts/features/ layout` | Task 2 (generators) |
| 4 | `75df96c` | `docs: update layout documentation for docs/artifacts/features/` | Task 3 (layout docs) |
| 5 | `1a8fde5` | `docs(skills): update project-standardization references and templates to per-feature layout` | Task 3 follow-up |
| 6 | `ff89358` | `docs(artifacts): update cross-references for per-feature layout` | Task 4 (cross-refs) |
| 7 | `762a8a3` | `docs(artifacts): complete forward-looking plans/ refs and restore historical prose` | Task 4 follow-up |
| 8 | `04ef3bc` | `docs(artifacts): finish stale docs/artifacts cross-references in moved plans` | Task 5 follow-up |
| 9 | `9349d64` | `docs(artifacts): restore verbatim CHANGELOG quote anchor in commitlint plan` | Task 5 anchor fix |
| 10 | `2257285` | `docs: add unreleased changelog entry for per-feature docs/artifacts migration` | Standardizer fixes |

## Files changed (diff stats)

### Moved (33 renames across 10 existing features, all into `docs/artifacts/features/<feature>/`)

Each feature folder now holds its full artifact set (spec, plan, and where applicable outline, manifest, report) flat in one place. Example baselines (rename score in parentheses):

| Feature | Files moved | Notable scores |
|---------|-------------|----------------|
| `agent-roster` | design + plan | R095, R097 |
| `code-standardization` | 11 files (foundation, SP-1..SP-5, outline, manifest, report) | R069 to R100 |
| `commitlint` | design + plan | R100, R096 |
| `multi-plan-orchestration` | design + plan | R080, R085 |
| `orchestrator-standardization-documentation` | design + plan | R080, R078 |
| `single-pass-full-cycle` | design + plan | R098, R090 |
| `skill-harvest` | design + plan | R100, R092 |
| `standardization-commit-hook` | design + plan | R098, R098 |
| `opencode-inventree-agent`, `inventree-datasheet-autopilot` | design + plan each | R100 across |

Lower scores (R069, R078, R080) reflect content edits made in the same change window (cross-reference and prose updates inside the moved files), not filename churn. Basenames are preserved exactly.

### Edited (active code)

| File | Delta | Why |
|------|-------|-----|
| `agents/planner.md` | +2 -2 | spec + plan paths to `features/` (Task 2). |
| `agents/documenter.md` | +2 -2 | report path (twice) + bare `reports/` to `features/` (Task 2). |
| `agents/orchestrator.md` | +1 -1 | bare `reports/` to `features/` (Task 2). |
| `commands/full-cycle.md` | +4 -4 | spec + plan + handoff + bare `reports/` (Task 2). |
| `commands/execute-plan.md` | +2 -2 | spec dir + report path (Task 2). |
| `commands/multi-plan.md` | +1 -1 | outline path (Task 2). |
| `skills/multi-plan-orchestration/SKILL.md` | +8 -8 | all `{multi-plans,specs,plans}/` patterns to `features/` (Task 2). |

### Edited (layout docs, Task 3)

| File | Delta | Why |
|------|-------|-----|
| `STANDARDS.md` | +1 -1 | `{specs,plans,reviews,reports}/` to `{features,reviews}/` (line 168). |
| `AGENTS.md` | +1 -1 | carve-out spec/plan path to `features/` (line 181). |
| `agents/README.md` | +1 -1 | roster path reference. |
| `docs/workflows/workflow.md` | +5 -5 | multiple path refs. |
| `docs/workflows/plan-flow.drawio` | +3 -3 | path text in `<mxCell>` labels. |
| `docs/workflows/multi-plan-flow.drawio` | +2 -2 | path text in `<mxCell>` labels. |

### Edited (project-standardization templates + references, Task 3 follow-up)

| File | Delta | Why |
|------|-------|-----|
| `skills/rubens-project-standardization/references/artifacts.md` | +80 -79 | full rewrite of artifact-path guidance to per-feature layout. |
| `skills/rubens-project-standardization/references/memory.md` | +4 -4 | path refs. |
| `skills/rubens-project-standardization/references/todolist.md` | +2 -2 | path refs. |
| `skills/rubens-project-standardization/templates/AGENTS-large.md` | +2 -2 | layout tree block. |
| `skills/rubens-project-standardization/templates/AGENTS-medium.md` | +2 -2 | layout tree block. |
| `skills/rubens-project-standardization/templates/AGENTS-small.md` | +2 -2 | layout tree block. |
| `skills/rubens-project-standardization/templates/STANDARDS.md` | +16 -16 | layout tree + path guidance. |

### Edited (moved artifacts, cross-reference updates, Tasks 4 + 5 follow-ups)

| File | Delta | Why |
|------|-------|-----|
| `features/agent-roster/...-plan.md` | +5 -5 | spec path cross-ref. |
| `features/code-standardization/...-manifest.md` | +9 -9 | spec + plan cross-refs. |
| `features/code-standardization/...-foundation-plan.md` | +2 -2 | spec cross-ref. |
| `features/code-standardization/...-sp{1,2,3,4,5}-plan.md` | +1 -1 each | spec cross-refs. |
| `features/commitlint/2026-08-01-commit-msg-hook-plan.md` | +2 -2 | spec cross-ref + restored verbatim CHANGELOG quote anchor (Task 5 fix). |
| `features/multi-plan-orchestration/...-design.md` | +8 -8 | prose + path refs. |
| `features/multi-plan-orchestration/...-plan.md` | +15 -15 | prose + path refs. |
| `features/orchestrator-standardization-documentation/...-{design,plan}.md` | +8 -8, +22 -22 | forward-looking `plans/` refs + historical prose restored (Task 4 follow-up). |
| `features/single-pass-full-cycle/...-{design,plan}.md` | +2 -2, +7 -7 | cross-refs. |
| `features/skill-harvest/...-plan.md` | +4 -4 | spec cross-ref. |
| `features/standardization-commit-hook/...-{design,plan}.md` | +1 -1 each | spec cross-refs. |
| `features/inventree-datasheet-autopilot/...-plan.md` | +1 -1 | spec cross-ref. |
| `features/opencode-inventree-agent/...-plan.md` | +1 -1 | spec cross-ref. |

### Added (this migration's own spec + plan)

| File | Lines | Why |
|------|-------|-----|
| `features/artifacts-layout/2026-08-05-docs-artifacts-per-feature-design.md` | +121 | the spec. |
| `features/artifacts-layout/2026-08-05-docs-artifacts-per-feature-plan.md` | +182 | the plan. |

### Added (CHANGELOG)

| File | Delta | Why |
|------|-------|-----|
| `CHANGELOG.md` | +1 | `### Changed` bullet under `## [Unreleased]` (standardizer fix). |

## Standardization review

The standardizer audited the full branch diff (`main..HEAD`) against `project-standardization` (repo structure). Final state: **PASS**.

Two quick-fix items, both addressed in commit `2257285`:

| # | Finding | Tag | Fix |
|---|---------|-----|-----|
| 1 | `CHANGELOG.md` had no entry under `## [Unreleased]` describing the per-feature migration. | quick-fix | Added a `### Changed` bullet (now line 46) summarizing the layout change, the filename-preservation, the scope of updates, and the phantom `reports/` directory caveat. |
| 2 | The now-empty `docs/artifacts/reports/` directory remained on disk after `git rm -r`; git no longer tracks it but the working tree still shows it. | quick-fix | Attempted removal; the Nextcloud sync client holds a handle on the directory and blocks deletion. Documented the leftover in the CHANGELOG bullet (see `ponytail:` deferrals below) rather than left silent. |

Recommendations: **none.** No items rolled forward.

## Documentation updates

Catalogs were audited at documentation time. The Task 3 commit already landed the layout-doc updates; the Task 3 follow-up already landed the template + reference updates. Cross-check against the repo `AGENTS.md` catalog rule (a skill or doc that exists but is missing from one of its catalogs is a process failure):

- **`README.md`** (`## Skills` table): no change required. No new skill was added or removed by this migration; the skills table lists skill folders, not artifact paths. The layout block (if any) under it was already correct after Task 3.
- **`AGENTS.md`** (`## Current skills` table + carve-out prose): already updated in Task 3 (line 181, spec/plan path now `docs/artifacts/features/`). No skill row changes needed. Confirmed clean.
- **`STANDARDS.md`**: already updated in Task 3 (line 168, brace-glob now `{features,reviews}/`). Confirmed clean.
- **`agents/README.md`**: already updated in Task 3 (roster path reference). Confirmed clean.
- **`opencode-install.md`**: no change required. The `## Verify` section does not reference the `docs/artifacts/` layout or any path that moved; per the catalog rule, skipped.
- **`external-skills.md`**: no change required. External skills catalog; does not reference internal artifact paths.
- **`CHANGELOG.md`**: `### Changed` bullet added under `## [Unreleased]` in the standardizer fix (`2257285`).
- **`docs/workflows/workflow.md` + `*.drawio`**: already updated in Task 3.
- **`skills/rubens-project-standardization/` templates + references**: already updated in Task 3 follow-up.

Cross-check (the "exists in one catalog but not another" rule): this migration added no skill, no agent, no command. The only catalog row that moved is the layout prose in `STANDARDS.md` and `AGENTS.md`, both updated. No drift.

**Net result: no further catalog updates were needed at documentation time.** The report itself is the sole new file this phase adds.

## Verifier output

- **Active-code grep (Task 5 Step 1):** `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/' -- ':!CHANGELOG.md' ':!docs/artifacts/reviews/*' ':!docs/artifacts/features/artifacts-layout/*' ':!docs/artifacts/features/commitlint/2026-08-01-commit-msg-hook-plan.md'` returns **zero hits** (exit 1). Clean.
- **Widened audit (no exclusions):** the only remaining hits fall into four intentional categories:
  1. `CHANGELOG.md` lines 23, 26, 27: historical `## [Unreleased]` entries that quote the spec path as it was at write time (immutable history).
  2. `docs/artifacts/reviews/2026-07-07-harvest.md` line 42: a historical harvest review referencing pre-migration paths (immutable history).
  3. `docs/artifacts/features/artifacts-layout/*.md`: this migration's own spec and plan, which describe the source paths as part of the migration mapping.
  4. `docs/artifacts/features/commitlint/2026-08-01-commit-msg-hook-plan.md` line 250: a verbatim quote anchor of `CHANGELOG.md` content kept so the commitlint plan's "add the entry" step can be re-executed byte-for-byte.
- **Directory tree sanity:** `Get-ChildItem docs/artifacts -Directory` returns `features`, `reviews`, and (working-tree-only) `reports`. Tracked content lives only under `features/` and `reviews/`; `reports/` is an untracked empty phantom (see deferrals).
- **New path reachable:** `docs/artifacts/features/` references appear in `agents/planner.md`, `agents/documenter.md`, `agents/orchestrator.md`, `commands/full-cycle.md`, `commands/execute-plan.md`, `commands/multi-plan.md`, `skills/multi-plan-orchestration/SKILL.md`, `STANDARDS.md`, `AGENTS.md`, `agents/README.md`, the three workflow docs, and the project-standardization templates + references. Count matches the spec's "Active generators" + "Layout documentation" lists.
- **Reviews unchanged:** the `docs/artifacts/reviews/` tree was not edited by this branch (flat log, immutable history).
- **Filename preservation:** 33 renames, every basename byte-identical pre- and post-move (git `{old => new}` notation confirms only the parent directory changed).
- **Em-dash scan (U+2014):** no new em-dashes introduced. The migration edits are path swaps and prose tweaks that preserved the existing punctuation.
- **Conventional Commits on branch:** `git log main..HEAD --oneline` shows 10 commits, all `docs:` or `docs(<scope>):` subjects, matching the plan's per-task messages plus the standardizer fix.

## Skills loaded

- `executing-plans` (orchestrator, this run).
- `writing-skills` / `writing-plans` (loaded during the planning phase that produced the spec and plan, prior to this execution run).
- `project-standardization` (catalog rules, em-dash rule, artifact layout convention; consulted at documentation time).
- `verification-before-completion` (evidence before claims; drove the rename-score and grep re-checks).
- `ponytail` (full, active session-wide: kept the catalog audit to the four real candidates, no speculative doc churn).

## ponytail: deferrals

- **Phantom `docs/artifacts/reports/` directory.** Empty, untracked by git, but still present on disk because the Nextcloud sync client holds an open handle on it and blocks `Remove-Item`. Documented in the CHANGELOG `### Changed` bullet. The user should restart or force-sync the Nextcloud client to release the handle, then delete the directory. Ceiling: cosmetic only (git already ignores it; no agent path points at it). Upgrade path: none beyond the client restart.
- **Drawio path text not visually verified.** The `plan-flow.drawio` and `multi-plan-flow.drawio` label strings were updated in the XML, but the diagrams were not opened in the drawio editor to confirm they render correctly with the new path text. The XML edits preserve all attributes other than the `value` string.

## Unverified items

- Whether the persistent phantom `docs/artifacts/reports/` directory clears after a Nextcloud client restart or force-sync. Not testable from this run (would require action outside the repo).
- Whether the two drawio files render correctly with the updated path text in their labels. Would require opening them in the drawio editor; out of scope for a docs/migration run.
- Whether downstream consumers (agent harnesses on other machines) pick up the new layout. They sync the repo via `git pull`; no migration hook is needed, but live verification happens on the next session, not here.

## Dispatch Log

Concise record of how the orchestrator ran the plan on `feat/docs-artifacts-per-feature`.

- **Preflight:** self-implemented (branch creation + spec/plan commit `f4fa6d7`).
- **Task 1 (move files):** dispatched executor + reviewer. Pass. Commit `9e8be2e`.
- **Task 2 (update generators):** dispatched executor + reviewer. Pass. Commit `c99331a`.
- **Task 3 (layout documentation):** dispatched executor + reviewer. Pass. Commit `75df96c`.
- **Task 3 follow-up (project-standardization templates + references):** dispatched executor (single, treated as a small extension to Task 3; no separate reviewer pass). Commit `1a8fde5`.
- **Task 4 (cross-references in moved artifacts):** dispatched executor + reviewer. Reviewer CHANGES_REQUESTED on 5 forward-looking `plans/` references and 2 prose rewrites that had been over-simplified. Re-dispatched executor for fixes + reviewer re-check. Pass. Commits `ff89358` (initial) + `762a8a3` (follow-up).
- **Task 5 (verification):** dispatched executor + reviewer. Follow-up commit `04ef3bc` completed the last stale cross-references inside moved plans. Reviewer CHANGES_REQUESTED on the follow-up overwriting a protected verbatim CHANGELOG quote anchor in the commitlint plan (line 250). Re-dispatched executor for the anchor fix; orchestrator self-verified the clean state. Pass. Commits `04ef3bc` (follow-up) + `9349d64` (anchor restore).
- **Standardizer:** dispatched standardizer. Returned 2 quick-fix items, 0 recommendations. Dispatched executor for both (CHANGELOG `### Changed` bullet + phantom-dir removal attempt). Self-reviewed. Commit `2257285`.
- **Documentation (this report):** dispatched documenter. This commit.

Totals: 9 executor dispatches (Tasks 1, 2, 3, 3-follow-up, 4, 4-follow-up, 5-follow-up, 5-anchor-fix, standardizer-quick-fixes), 6 reviewer dispatches (Tasks 1, 2, 3, 4, 4-follow-up, 5), 1 standardizer dispatch, 1 documenter dispatch. Two-strike failures and oracle consults: none.

## Out of scope / outstanding

None beyond the two `ponytail:` deferrals above. The branch is clean, all planned files moved and re-referenced, all catalogs are in sync, and the standardizer returned PASS. `feat/docs-artifacts-per-feature` is ready for the user to merge to `main`.
