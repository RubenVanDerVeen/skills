# AI-provenance disclosure: execution report

Date: 2026-08-29
Plan: `docs/artifacts/features/ai-provenance-disclosure/2026-08-29-ai-provenance-disclosure-plan.md`
Spec: `docs/artifacts/features/ai-provenance-disclosure/2026-08-29-ai-provenance-disclosure-design.md`

## Summary

Shipped AI-provenance disclosure for the `project-standardization` skill on branch `feat/ai-provenance-disclosure` (7 commits from `main` at `db0252b`, 11 files, +447/-8). Every project bootstrapped or restructured with the skill now gets a `## AI assistance` section in its README (involvement level from a 4-level vocabulary, links to the skills repo and the workflow doc) via new bootstrap sub-step 9.1 stamping `templates/README-ai-assistance.md`, and STANDARDS.md carries the research-paper URL as its default rationale link (the URL constant lives in exactly two skill files). Retro-fit needs no new tooling: the restructure flow re-runs the same predicates. All five task verification suites passed, including the end-to-end smoke test; the standardizer's two quick-fix findings and one latent em-dash were fixed in `b8076d6`.

## Branch and commits

Branch `feat/ai-provenance-disclosure`, created from `main` at `db0252b`.

| Hash | Subject | Task |
|---|---|---|
| `fce5d16` | `docs: add plan and spec for ai-provenance-disclosure` | docs-first branch commit (per `/execute-plan` setup) |
| `6865286` | `feat(skills): add README AI-assistance snippet template to project-standardization` | Task 1: template + SKILL.md Templates row (2 files, +9) |
| `4f12f28` | `feat(skills): default research-paper link in STANDARDS.md and standards-stack reference` | Task 2: paper URL in its two homes, double-colon typo fix (2 files, +2/-2) |
| `5bc6a14` | `feat(skills): bootstrap step 9.1 stamps AI-assistance section into README` | Task 3: sub-step 9.1, step 9 predicate extension, SKILL.md summary row (2 files, +4/-2) |
| `241b8fb` | `fix(skills): indent bootstrap sub-step 9.1 to match 8.1 pattern` | Task 3 fixup after CHANGES_REQUESTED: 4-space indent restored the step count to 12 (1 file, +1/-1) |
| `e447e98` | `docs(skills): note README AI-assistance section in tier layout trees` | Task 4: `small.md`, `medium.md`, `large.md` tree annotations (3 files, +3/-3) |
| `b8076d6` | `docs(skills): changelog entry and bootstrap prose fix` | Standardizer quick-fixes + latent em-dash (2 files, +3/-2) |

Task 5 (smoke test + sweeps) modified no repo files; no commit, results below.

## Files changed

`git diff db0252b..HEAD --stat`:

```text
 CHANGELOG.md                                                       |   3 +-
 docs/artifacts/features/ai-provenance-disclosure/...-design.md     | 114 ++++++++
 docs/artifacts/features/ai-provenance-disclosure/...-plan.md       | 313 +++++++++++++++++++++
 skills/rubens-project-standardization/SKILL.md                     |   3 +-
 skills/rubens-project-standardization/references/bootstrap.md      |   4 +-
 skills/rubens-project-standardization/references/large.md          |   2 +-
 skills/rubens-project-standardization/references/medium.md         |   2 +-
 skills/rubens-project-standardization/references/small.md          |   2 +-
 skills/rubens-project-standardization/references/standards-stack.md|   2 +-
 skills/rubens-project-standardization/templates/README-ai-assistance.md |   8 +
 skills/rubens-project-standardization/templates/STANDARDS.md       |   2 +-
 11 files changed, 447 insertions(+), 8 deletions(-)
```

Added files (3): the spec, the plan, `templates/README-ai-assistance.md`. Deleted files: none. `commands/`, `agents/`, and all other `skills/` folders untouched (verified via `git diff --diff-filter=A/D --name-only`).

## Standardization review

The standardizer pass (1 dispatch) returned 2 quick-fix findings, 0 recommendations:

1. Missing `CHANGELOG.md` entry for the feature. Fixed in `b8076d6`: `[Unreleased] ### Added` bullet describing step 9.1, the template, the vocabulary, the paper links, and the tier-tree notes.
2. Garbled prose in `references/bootstrap.md:34`: "with the user, vocabulary:" became "with the user's vocabulary:". Fixed in `b8076d6`.

Plus one latent defect fixed in the same commit: a pre-existing em-dash on `CHANGELOG.md:26` (workflow-diagrams bullet). The repo's no-em-dash rule applies to every touched file, so the exemption for pre-existing hits ended the moment this run edited CHANGELOG.md; the em-dash became a colon.

Nothing remains open from the standardizer. Pre-existing em-dashes in files this run never touched are out of scope (see Verifier output).

## Documentation updates

Catalogs and docs touched by the run, and why:

- `skills/rubens-project-standardization/SKILL.md`: `templates/README-ai-assistance.md` row in the `## Templates` table (`6865286`); bootstrap summary row now says "STANDARDS + README AI section" (`5bc6a14`).
- `CHANGELOG.md`: `[Unreleased] ### Added` bullet (`b8076d6`).
- Tier references `small.md` / `medium.md` / `large.md`: README tree entries annotated "carries the AI assistance section" so the restructure flow's template comparison treats a missing section as a gap (`e447e98`).

Repo-level catalog sync: **no updates needed, verified.** This feature modifies an existing skill; it adds no skill, command, or agent, so:

- `README.md` `## Skills` table: unchanged, no row needed (existing `rubens-project-standardization` row at line 17 still correct).
- `AGENTS.md` `## Current skills` table: unchanged, no row needed.
- `opencode-install.md`: no skill-name references; grep for `project-standardization|README-ai-assistance|ai-provenance` returns nothing.
- `commands/`, `agents/`, `external-skills.md`: no new command or agent, nothing to sync.

Per the plan's own constraint (line 21), the catalog rule applied only to the SKILL.md Templates table. No catalog was found missing an entry.

## Verifier output

All five task verification suites passed; every predicate in the plan was actually run:

- Task 1: template `Test-Path` True; workflow deep link 1 hit in the template; `README-ai-assistance` 1 hit in SKILL.md.
- Task 2: `portfolio.rvdv-lab.nl` present in exactly the two intended skill files (`templates/STANDARDS.md`, `references/standards-stack.md`); process docs (spec/plan) mention it too, as the plan allows.
- Task 3: `README AI section` 1 hit in SKILL.md; step-count predicate `(Select-String '^\d+\.' bootstrap.md).Count` = 12 after the `241b8fb` indent fixup (the executor's first attempt had the 9.1 block at column 0, yielding 13; the reviewer caught it).
- Task 4: `carries the AI assistance section` exactly 1 hit per tier file; the later example trees in `small.md` untouched.
- Task 5 smoke test: scratch project without a README in `C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke\`; minimal README created, template appended; both step 9.1 predicates (`^## AI assistance`, `RubenVanDerVeen/skills`) hit. Scratch dir deleted afterwards (confirmed gone).

Em-dash sweeps (re-run by the documenter from `main` worktree state on the branch):

- Targeted re-sweep of all 11 touched files: zero hits.
- Repo-wide: pre-existing hits remain in 4 untouched files, out of scope per the plan (blocker only in touched files): `docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-skill-artifacts-per-feature-cleanup-plan.md`, `docs/artifacts/reviews/2026-07-12-harvest.md`, `skills/deep-research/templates/dossier-template.md`, `skills/deep-research/SKILL.md`.

Working tree clean; no scratch residue.

## Skills loaded

- `executing-plans` (loaded by the orchestrator).
- `using-git-worktrees` baseline considered (single-branch work chosen).
- Subagent dispatches: executor (7x), reviewer (5x), standardizer (1x), documenter (1x, this report).

## `ponytail:` deferrals

None. The plan was already minimal (template-stamping, no new tooling); no shortcuts were taken or marked.

## Unverified items

None. Every verification predicate ran and produced its expected output. Two plan-predicate defects were found during the Task 3 review and deliberately kept as-is (they are defects in the plan's verification text, not in shipped skill files):

1. The `^9\.1\.` anchor predicate cannot match the correctly indented sub-step (the line starts with 4 spaces per the 8.1 pattern the spec D4 mandates).
2. The simple grep against `\.` matches the literal backslash-dot sequence in the markdown, not the rendered text.

Neither affects shipped behavior; both are documented in the Task 3 review exchange.

## Dispatch log

| Step | Dispatched | Outcome |
|---|---|---|
| Branch setup + docs commit | orchestrator | `fce5d16` |
| Task 1 | executor, then reviewer | `6865286`, PASS |
| Task 2 | executor, then reviewer | `4f12f28`, PASS |
| Task 3 | executor, reviewer (CHANGES_REQUESTED: indent defect), executor fixup, reviewer | `5bc6a14` + `241b8fb`, PASS |
| Task 4 | executor, then reviewer | `e447e98`, PASS |
| Task 5 | executor (verification only) | no commit, all predicates pass |
| Standardization | standardizer (2 quick-fixes, 0 recommendations), executor for fixes, reviewer | `b8076d6`, PASS |
| Documentation | documenter | this report |

## Notes for future runs

- Plans that verify indented sub-steps should not use `^N.N\.` anchors: the spec-correct indent (matching 8.1) defeats the anchor. Prefer a pattern without the line-start anchor, or assert the step count instead (the count predicate is what actually caught the defect).
- The no-em-dash rule reaches pre-existing hits the moment a file is touched. Runs that must edit old files (CHANGELOG.md was the case here) inherit a scrub of every em-dash in that file; budget for it.
- Markdown code fences preserve `\.` escapes literally. Predicates that grep fenced content should account for that or grep for escape-free substrings.
