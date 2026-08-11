# Versioning standard implementation report

## Summary

**Status: PASS.** The `project-standardization` skill gained a SemVer 2.0.0 versioning policy as a single new reference file (`references/versioning.md`) that nine existing files now point at: the SKILL body, the bootstrap checklist, all three AGENTS templates (small/medium/large), the CHANGELOG template, the STANDARDS template, and the two agents that act on the policy (`standardizer` audits it, `orchestrator` cuts releases against it). Eight commits on `feat/versioning-standard`, 10 files changed (+163/-6), zero em-dashes introduced, all six verification-sweep checks green. The standardizer returned PASS with two non-blocking observations (CHANGELOG recipe-comment wording drift and a missing trailing newline), both carried forward as recommendations rather than tagged `quick-fix`. No new skill or command was added, so no catalog row changes were required; the internal References table of `SKILL.md` got its new row as Task 2 scope, not a catalog update.

## Branch and commits

- **Branch:** `feat/versioning-standard` (checked out, branched from `main` at `4591816`).
- **Commit count:** 8 (excluding this report). Tasks 1 through 7 each produced one commit; Task 2 produced an implementation commit plus one follow-up fix; Task 8 was a read-only verification sweep with no commit per plan Step 6.
- **Diffstat (`4591816..HEAD`):** 10 files changed, 163 insertions(+), 6 deletions(-).

### Commit list (execution order, oldest first)

| # | Hash | Subject | Phase |
|---|------|---------|-------|
| 1 | `3a84f8a` | `feat(skills): add versioning reference to project-standardization` | Task 1 (versioning.md) |
| 2 | `f1a7b58` | `docs(skills): wire versioning reference into project-standardization SKILL and bootstrap` | Task 2 (SKILL.md + bootstrap.md) |
| 3 | `61a00b2` | `fix(skills): point bootstrap step 8.1 at versioning reference` | Task 2 follow-up fix |
| 4 | `ac4e6df` | `feat(skills): add Versioning subsection to project-standardization AGENTS templates` | Task 3 (3 AGENTS templates) |
| 5 | `cc5a46f` | `feat(skills): add SemVer header and release-cut recipe to CHANGELOG template` | Task 4 (CHANGELOG.md) |
| 6 | `f4023c0` | `feat(skills): add SemVer 2.0.0 to STANDARDS template stack, section, and references` | Task 5 (STANDARDS.md) |
| 7 | `33419f0` | `feat(agents): add versioning-policy audit to standardizer` | Task 6 (standardizer.md) |
| 8 | `fef0578` | `feat(agents): add release-cut branch to orchestrator` | Task 7 (orchestrator.md) |

## Files changed (diff stats)

### Added (Task 1)

| File | Delta | Why |
|------|-------|-----|
| `skills/rubens-project-standardization/references/versioning.md` | +87 | New reference: the single source of truth for the SemVer 2.0.0 policy. Eight sections (policy table, bump decision rule, trigger rule, source-of-truth declaration, release-cut recipe, the 3 standardizer checks, anti-patterns). |

### Edited (Tasks 2-7)

| File | Delta | Why |
|------|-------|-----|
| `skills/rubens-project-standardization/SKILL.md` | +6 -0 (net) | Floor bullet now names SemVer 2.0.0 alongside Conventional Commits and Keep a Changelog; References table gains the `versioning.md` row; Anti-patterns gains two bullets (Task 2). |
| `skills/rubens-project-standardization/references/bootstrap.md` | +1 | New sub-step 8.1 pointing version-shipping projects at the `### Versioning` subsection (Task 2, path corrected in follow-up `61a00b2`). |
| `skills/rubens-project-standardization/templates/AGENTS-small.md` | +14 | New `### Versioning` subsection under `## Git & workflow`, shipped inside an HTML comment so the small tier pays zero tokens when inactive (Task 3). |
| `skills/rubens-project-standardization/templates/AGENTS-medium.md` | +14 | Same Versioning block, placeholders visible (Task 3). |
| `skills/rubens-project-standardization/templates/AGENTS-large.md` | +14 | Same Versioning block, placeholders visible (Task 3). |
| `skills/rubens-project-standardization/templates/CHANGELOG.md` | +10 -1 | Header paragraph now names SemVer 2.0.0 alongside the other two conventions; new release-cut recipe comment block carrying the 5-step procedure, scoped to semver projects (Task 4). The original 3-mode grouping comment and the `[<First Version or Sprint>]` placeholder are preserved verbatim. |
| `skills/rubens-project-standardization/templates/STANDARDS.md` | +12 | Stack table gains the SemVer 2.0.0 row; new `## Versioning: SemVer 2.0.0` section between Changelog and Repository layout; References list gains the semver.org link (Task 5). |
| `agents/standardizer.md` | +4 -0 (net) | Frontmatter description widens to "version-source sync and SemVer 2.0.0 policy presence (shipped-software projects)"; body gains the three-check audit paragraph before the `code-standardization` load paragraph (Task 6). |
| `agents/orchestrator.md` | +7 -0 (net) | New numbered step 7 (Release-cut, user-invoked) inserted before the Documentation step, which is renumbered 7 -> 8 and the Finish step 8 -> 9; frontmatter description appends the release-cut responsibility (Task 7). |

## Per-task outcome

| Task | Outcome |
|------|---------|
| Task 1 (versioning.md) | PASS. Reviewer approved; 8 sections, both bump tables render, SemVer link present, no em-dashes. Commit `3a84f8a`. |
| Task 2 (SKILL.md + bootstrap.md) | PASS-with-finding. Reviewer flagged that bootstrap step 8.1 referenced "the versioning reference" rather than the exact path `references/versioning.md`. Folded into the follow-up fix. Commit `f1a7b58`. |
| Task 2 fix (bootstrap path) | PASS. Single 6-word edit landed the exact path. Commit `61a00b2`. |
| Task 3 (3 AGENTS templates) | PASS. All three templates carry the Versioning block; small tier ships it inside an HTML comment (zero active tokens). Commit `ac4e6df`. |
| Task 4 (CHANGELOG template) | PASS. SemVer line in header, recipe comment block added, original grouping comment and placeholder preserved. Commit `cc5a46f`. |
| Task 5 (STANDARDS template) | PASS. Stack row, new section, and References link all landed. Commit `f4023c0`. |
| Task 6 (standardizer agent) | PASS. Frontmatter parses; audit paragraph sits before the `code-standardization` load paragraph; agent stays read-only. Commit `33419f0`. |
| Task 7 (orchestrator agent) | PASS. Step numbering runs 1-9 with no gaps; release-cut step at position 7, Documentation at 8, Finish at 9. Commit `fef0578`. |
| Task 8 (whole-plan verification) | PASS, read-only. Six checks, all green. No commit per plan Step 6. |

## Standardization review

The standardizer audited the full branch diff (`4591816..HEAD`) against `project-standardization`. Final state: **PASS**. Zero `quick-fix` items. Two non-blocking observations, both carried forward as recommendations:

| # | Finding | Tag | Disposition |
|---|---------|-----|-------------|
| 1 | `templates/CHANGELOG.md:14` release-cut comment header reads "semver projects only", while the other 7 locations in the diff use the canonical "shipped-software projects (Tauri apps, CLIs, libraries, installers)" + explicit "Skip for sub-projects versioned through a parent" wording. Semantically equivalent (sub-projects don't cut releases). The executor followed the plan's Task 4 Step 2 verbatim text; the wording drift originates in the plan, not the execution. | recommendation | Carried forward. Cosmetic wording drift, not policy drift. A future touch-up commit can normalize the CHANGELOG recipe comment header to the canonical phrasing; no behavior change. |
| 2 | `references/versioning.md` ends with no trailing newline (last byte is `.` = 0x2E, not `\n`). | recommendation | Carried forward. Cosmetic only; POSIX text-file convention. A future `style:` commit can append the newline. |

Recommendations are the standardizer's term for non-blocking findings that do not gate merge. Both are safe to defer.

## Documentation updates

Catalogs audited at documentation time against the repo `AGENTS.md` "Adding or modifying a skill" rule. **No catalog updates required.** This plan adds no new skill and no new command; it extends an existing skill (`project-standardization`) and edits two existing agents (`standardizer`, `orchestrator`) already listed in every roster.

| Catalog | Required change | Reason |
|---------|-----------------|--------|
| `README.md` (`## Skills` table) | none | No new skill folder. `project-standardization` row already present and correct. |
| `AGENTS.md` (`## Current skills` table) | none | Same as above. The repo-root `AGENTS.md` is also untouched by the branch (confirmed via `git diff`). |
| `agents/README.md` (roster) | none | `standardizer` and `orchestrator` rows already exist. Neither agent's Mode, Model, Role, or Denied columns changed in a way the roster tracks; the edits were body and frontmatter-description refinements within scope of the existing Role text. |
| `opencode-install.md` | none | The `## Verify` section does not list `project-standardization`, `standardizer`, or `orchestrator` by name. Per the catalog rule, skipped. |
| `external-skills.md` | none | External skills catalog; this work is internal. |
| `skills/rubens-project-standardization/SKILL.md` References table | already landed (Task 2) | The new `references/versioning.md` row was added in commit `f1a7b58` as Task 2 scope. This is the skill's internal reference index, not a repo-level catalog; no separate documentation-phase commit is warranted. |

Cross-check (the "exists in one catalog but not another" rule): the `skills/rubens-project-standardization/` folder, the `project-standardization` frontmatter `name`, the README row, and the AGENTS row remain byte-identical to their pre-branch state. No drift. **Net result: the report itself is the sole new file this phase adds.**

## Verifier output

Task 8 ran six read-only checks across the 10 touched files. All passed:

1. **Em-dash scan (U+2014):** 0 matches across all 10 files. Clean.
2. **Cross-reference consistency (`versioning.md` path):** 11 matches across 9 files (versioning.md itself is the source, so it does not self-match). Distribution: SKILL.md 3 (floor bullet + References row + anti-pattern bullet), bootstrap.md 1, AGENTS-small/medium/large 1 each, CHANGELOG.md 1 (inside the recipe comment), STANDARDS.md 1, standardizer.md 1, orchestrator.md 1. The plan's Task 8 Step 2 expected 2 matches in SKILL.md; the actual 3rd match comes from the anti-pattern bullet added in Task 2 Step 3, which is in-plan scope. No drift; the plan's own expectation slightly under-counted.
3. **SemVer 2.0.0 mention sweep:** 21 matches across 10 files. Met or exceeded the plan's per-file expectations (versioning.md multiple, SKILL.md >=2, CHANGELOG.md 1, STANDARDS.md >=4, standardizer.md >=2, orchestrator.md 1, AGENTS templates 1 each inside the commented block).
4. **CHANGELOG heading format:** the canonical `## [X.Y.Z] - YYYY-MM-DD` format is present in the CHANGELOG recipe comment (line 18) and in the new `references/versioning.md`. The original `[<First Version or Sprint>]` placeholder is preserved verbatim.
5. **No accidental catalog edits:** `git status --porcelain` clean. `README.md`, repo-root `AGENTS.md`, `opencode-install.md`, `external-skills.md`, `agents/README.md`, and `commands/` are all untouched by the branch (confirmed via `git diff 4591816..HEAD --stat` against those paths returning empty).
6. **Working tree clean:** `git status --porcelain` returns empty at the time of this report.

## Skills loaded

- The orchestrator ran this plan on its standard orchestration tooling (system prompt); no explicit skill loads in the orchestration run.
- Each executor and reviewer subagent read the plan and spec directly; no explicit skill loads recorded in the dispatch log.
- The standardizer consults `project-standardization` and `code-standardization` per its agent definition; the versioning audit added in Task 6 is part of the `project-standardization` scope.
- The documenter (this dispatch) consulted the repo `AGENTS.md` "Adding or modifying a skill" rule and the existing reports (`artifacts-layout`, `code-standardization`) for format consistency, plus `agents/README.md` for the roster rules.

## ponytail: deferrals

None. Every simplification in the plan was a deliberate YAGNI choice approved at brainstorming and recorded in the spec's "Non-goals" section:

- No bump scripts. Manual multi-file edit at release-cut. (Spec non-goal 1.)
- No release-automation tooling (`release-please`, `semantic-release`, `git-cliff`). (Spec non-goal 2.)
- No library-sub-project coverage. (Spec non-goal 4.)
- No migration of existing `klad`/`synctool` CHANGELOG drift. (Spec non-goal 3.)

These are scope decisions, not shortcuts with a ceiling to track. No `ponytail:` comments were introduced by this branch.

## Unverified items

None. All six Task 8 checks passed. The two standardizer observations are recommendations, not unverified items; they are documented above as carried forward.

One mechanical-verification gap worth naming: `opencode agent list` and `opencode debug agent standardizer` / `opencode debug agent orchestrator` were not run in this environment (no opencode CLI verification step is in the plan). The edited frontmatter and bodies were validated by eye against the schema documented in `agents/README.md`, and the YAML frontmatter blocks were confirmed intact (single-line `description:`, `---` fences preserved). This matches the verification posture of prior reports on this repo.

## Dispatch Log

Concise record of how the orchestrator ran the plan on `feat/versioning-standard`.

| Task | Dispatch | Reviewer |
|------|----------|----------|
| Task 1 (write versioning.md) | dispatched: executor + reviewer | PASS |
| Task 2 (SKILL.md + bootstrap.md) | dispatched: executor + reviewer | PASS-with-finding (bootstrap path missing) |
| Task 2 fix (bootstrap path) | dispatched: executor (single edit, 6 words) | folded into reviewer's recommended fix text |
| Task 3 (3 AGENTS templates) | dispatched: executor + reviewer | PASS |
| Task 4 (CHANGELOG template) | dispatched: executor + reviewer | PASS |
| Task 5 (STANDARDS template) | dispatched: executor + reviewer | PASS |
| Task 6 (standardizer agent) | dispatched: executor + reviewer | PASS |
| Task 7 (orchestrator agent) | dispatched: executor + reviewer | PASS |
| Task 8 (whole-plan verification) | self-implemented: read-only sweep, no commit | n/a (no diff to review) |
| Standardizer | dispatched: standardizer | PASS, 2 non-blocking observations |
| Documenter | dispatched: documenter (this commit) | n/a |

Totals: 8 executor dispatches (Tasks 1, 2, 2-fix, 3, 4, 5, 6, 7), 7 reviewer dispatches (Tasks 1, 2, 3, 4, 5, 6, 7), 1 standardizer dispatch, 1 documenter dispatch. Two-strike failures and oracle consults: none.

## Spec coverage map

Every spec component (A-H from the design doc) maps to exactly one task, except B + F (folded into Task 2) and the split of D + E across Tasks 4 + 5 for reviewability. Confirmed 1:1 coverage; no spec component is unimplemented.

| Spec component | Task | Evidence |
|----------------|------|----------|
| A. New reference `references/versioning.md` | Task 1 | File created, 8 sections, both bump tables, commit `3a84f8a`. |
| B. `SKILL.md` updates (floor bullet, References row, anti-pattern) | Task 2 | All three edits landed, commit `f1a7b58`. |
| C. AGENTS.md templates (small/medium/large Versioning subsection) | Task 3 | All three carry the block; small tier commented out, commit `ac4e6df`. |
| D. CHANGELOG template (SemVer header + release-cut recipe) | Task 4 | Header line + recipe comment added, commit `cc5a46f`. |
| E. STANDARDS template (stack row + section + References link) | Task 5 | All three edits landed, commit `f4023c0`. |
| F. Bootstrap checklist sub-step 8.1 | Task 2 | Sub-step added; path corrected in follow-up `61a00b2`. |
| G. `agents/standardizer.md` audit + frontmatter | Task 6 | Description widened + audit paragraph added, commit `33419f0`. |
| H. `agents/orchestrator.md` release-cut branch | Task 7 | New step 7 inserted; downstream steps renumbered; description updated, commit `fef0578`. |
| (verification) | Task 8 | Read-only sweep, 6 checks green, no commit. |

## Out of scope / outstanding

- The two standardizer recommendations (CHANGELOG recipe-comment wording normalization; trailing newline on `versioning.md`). Both cosmetic; safe to defer to a future `style:` touch-up.
- The spec's recorded non-goals (bump scripts, release-automation tools, library-sub-project coverage, `klad`/`synctool` CHANGELOG migration). All remain intentionally unimplemented.

The branch is clean, all planned files exist, all cross-references resolve, all catalogs are in sync, and the standardizer returned PASS. `feat/versioning-standard` is ready for the user to merge to `main`.
