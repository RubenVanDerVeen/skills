# Execution Report: Standardization Git Hooks

Date: 2026-09-01
Feature folder: `docs/artifacts/features/standardization-githooks/`
Spec: `2026-09-01-standardization-githooks-design.md`
Plan: `2026-09-01-standardization-githooks-plan.md`
Branch: `plan-standardization-githooks` (off `main`, not pushed)
Status: Complete. All 5 plan tasks executed, all 10 verification matrix rows PASS, hook active.

## Summary

The repo now enforces the machine-checkable subset of its doc standards at commit time via a new POSIX-sh `.githooks/pre-commit` hook (checks P1..P7: em-dash ban, SKILL.md frontmatter name/description/size rules, body headings, catalog sync for new skills, forbidden paths), with zero new dependencies. The day-one scrub removed all 24 em-dashes from tracked markdown and added the missing `## Overview` heading to `skills/rubens-project-standardization/SKILL.md`, so the hook never fails on untouched files. Documentation (AGENTS.md, STANDARDS.md, opencode-install.md, CHANGELOG.md) now names the full hook set, activation, and bypass. The verification matrix passed 10/10 in a scratch clone, independently re-confirmed by the reviewer.

## Branch and commits

Six commits on `plan-standardization-githooks`, oldest first:

| Hash | Subject | Plan task |
|---|---|---|
| `f250946` | `docs(standardization-githooks): add design and plan` | Spec + plan (pre-work) |
| `5088120` | `docs: scrub em-dashes from markdown files` | Task 1 |
| `e462d37` | `docs(skills): add Overview heading to project-standardization` | Task 2 |
| `9e89297` | `feat(githooks): enforce doc standards in pre-commit hook` | Task 3 |
| `afd4146` | `docs: wire standardization git hooks into repo documentation` | Task 5 |
| `c155e52` | `fix(docs): sync standardization-githooks tree and changelog spec link` | Review quick-fixes |

Task 4 (verification matrix) was verification-only and produced no commit, as the plan specifies.

## Files changed

12 files, 659 insertions, 29 deletions (`git diff --stat main...HEAD`):

| File | Change |
|---|---|
| `.githooks/pre-commit` | New, 113 lines, mode 100755. Checks P1..P7 against staged index content. |
| `skills/deep-research/SKILL.md` | 16 em-dash removals (Task 1) |
| `skills/deep-research/templates/dossier-template.md` | 1 em-dash removal (Task 1) |
| `docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-skill-artifacts-per-feature-cleanup-plan.md` | 6 em-dash removals (Task 1) |
| `docs/artifacts/reviews/2026-07-12-harvest.md` | 1 em-dash removal (Task 1) |
| `skills/rubens-project-standardization/SKILL.md` | H1 converted to `## Overview` (Task 2) |
| `AGENTS.md` | Enforcement sentence now names both hooks and their checks (Task 5) |
| `STANDARDS.md` | Enforcement line names both hooks (Task 5) |
| `opencode-install.md` | Step 10 retitled "Enable the git hooks", describes the full set (Task 5) |
| `CHANGELOG.md` | Keep a Changelog Added entry with spec link (Task 5 + quick-fix) |
| `docs/artifacts/features/standardization-githooks/2026-09-01-standardization-githooks-design.md` | New spec |
| `docs/artifacts/features/standardization-githooks/2026-09-01-standardization-githooks-plan.md` | New plan |

## Verification matrix (Task 4, scratch clone)

| Case | Expected | Actual | Verdict |
|---|---|---|---|
| M0 baseline clean | exit 0 | exit 0 | PASS |
| M1 em-dash (`*.md` with U+2014) | exit 1, `P1 em-dash` | exit 1, `P1 em-dash` | PASS |
| M2 name mismatch | exit 1, `P2 name` | exit 1, `P2 name` | PASS |
| M3 description not starting with "Use when" | exit 1, `P3 description` | exit 1, `P3 description` | PASS |
| M4 frontmatter > 1024 bytes | exit 1, `P4 frontmatter-size` | exit 1, `P4 frontmatter-size` | PASS |
| M5a `## Skill` heading | exit 1, `P5 skill-heading` | exit 1, `P5 skill-heading` | PASS |
| M5b missing `## Overview` | exit 1, `P5 overview` | exit 1, `P5 overview` | PASS |
| M6 new skill, no catalog rows | exit 1, two `P6 catalog-sync` | exit 1, two `P6 catalog-sync` | PASS |
| M6-pass same skill with rows added | exit 0 | exit 0 | PASS |
| M7 forbidden dir `docs/superpowers/` | exit 1, `P7 forbidden-path` | exit 1, `P7 forbidden-path` | PASS |

All 10 rows PASS. The Task 4 reviewer independently re-ran M0, M1, M6, and M7 in a fresh scratch clone and confirmed correct behavior.

## Standardization review

### Doc-standardizer findings (3)

1. STANDARDS.md layout tree missing `pre-commit`. Fixed in `c155e52`.
2. CHANGELOG entry missing spec reference. Fixed in `c155e52`.
3. Pre-existing drift in the STANDARDS.md tree for `commands/` and `agents/` listings. Recommendation only, not this branch's scope (plan constraint: do not fix unrelated drift). Remains open.

### Code review on hook script

Verdict: PASS. No critical or important findings. 12 minor nits, all documented as known ceilings (see `ponytail:` deferrals below); none warrant changes now.

## Documentation updates

- `AGENTS.md`: enforcement sentence in Git & workflow names `commit-msg` + `pre-commit`, the checked rules, activation, and bypass. No catalog changes needed: no new skill, command, or agent shipped, so the README skills table, agents/README.md roster, `opencode-install.md` name references, and `external-skills.md` rows are unaffected (verified against the "Adding or modifying a skill" rules).
- `STANDARDS.md`: enforcement line names both hooks; layout tree now includes `pre-commit` (quick-fix).
- `opencode-install.md`: step 10 covers the full hook set.
- `CHANGELOG.md`: Keep a Changelog Added entry, spec link included after quick-fix.
- This report closes out the feature folder's artifact set (design, plan, report).

## Verifier output

- `sh -n .githooks/pre-commit`: exit 0.
- `git ls-files -s .githooks/pre-commit`: `100755`.
- Repo-wide em-dash scan (`Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014)`): 0 hits, stable from Task 1 through every subsequent commit and this report.
- All commit subjects accepted by the `commit-msg` hook (Conventional Commits).
- The `pre-commit` hook accepted every commit on the branch, including its own landing commit (staged content non-`.md`, non-SKILL.md, non-forbidden) and the doc-only commits after it.
- Full matrix: 10/10 PASS (above).
- Completion checklist from the plan: all items ticked.

## Skills loaded

- `executing-plans` (orchestrator)

## `ponytail:` deferrals (known ceilings)

Documented in the hook's own `ponytail:` header comment and confirmed as intentional by code review:

1. Word-splits path lists. Safe because the kebab-case rule bans spaces in paths.
2. Treats a repo's very first commit as a new-skill commit (P6 demands catalog rows). No upgrade path needed for this repo (initial commit already exists).
3. UTF-8 BOM and CRLF in a staged SKILL.md are rejected by the P2 frontmatter check; not addressed by `.gitattributes` (only `.githooks/**` is LF-pinned).
4. P4 counts bytes, not characters; multi-byte frontmatter hits the 1024 cap sooner than a char count would.
5. P1 scans all `*.md` including fenced code blocks; an em-dash inside a code example trips P1.
6. P6 greps `skills/<folder>/` anywhere in README/AGENTS, not just the catalog table rows.

Upgrade path for any ceiling that bites: edit the hook and re-run the plan's verification matrix (noted in the hook header).

## Unverified items

- The 12 code-review nits beyond the 6 ceilings listed above were not individually re-verified after review; the review verdict (PASS, no critical/important findings) is accepted as-is.
- Hook behavior on clones that never run `git config core.hooksPath .githooks` is by definition unenforced; documented in `opencode-install.md` step 10, not machine-verified.

## Out-of-scope observations

- `skills/deep-research/scripts/verify-multi-lens.sh:2` contains one U+2014 in a comment. Check P1 only applies to `*.md`, so the hook does not trip. The plan's global constraint (line 16) says "No literal U+2014 byte may appear in ANY tracked file, ever"; the shipped hook's scope is narrower than that constraint. This gap is documented here, not fixed: scrubbing a `.sh` file and widening P1 to non-markdown files is a rule-scope decision for the user, not a report-phase edit.
- Doc-standardizer finding 3 (STANDARDS.md tree drift for `commands/` and `agents/` listings) remains a recommendation outside this branch.

## Dispatch Log

- Every plan task went through `executor` + `reviewer` dispatch (Tasks 1-5).
- Task 4's reviewer independently re-ran M0, M1, M6, M7 in a fresh scratch clone: confirmed.
- Doc-standardizer review fired once (post-implementation); 2 quick-fixes applied in `c155e52`, 1 recommendation deferred.
- Code review on the hook script fired once: PASS, 12 minor nits documented as ceilings, no critical issues.
- Documenter (this agent) wrote this report and committed it; no other files touched.
