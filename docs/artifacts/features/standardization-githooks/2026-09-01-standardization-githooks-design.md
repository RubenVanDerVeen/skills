# Design: Standardization Git Hooks (pre-commit + commit-msg extension)

Date: 2026-09-01
Status: Approved (single-pass full-cycle)
Feature folder: `docs/artifacts/features/standardization-githooks/`

## Problem

The repo has exactly one tracked git hook (`.githooks/commit-msg`, Conventional Commits subject check). Every other convention in `AGENTS.md` and `STANDARDS.md` relies on the agent choosing to comply. The user wants more hooks so an agent physically cannot commit wrong docs: bad skill frontmatter, skills missing from catalogs, em-dashes, forbidden directories, or mis-typed commit messages.

## Goal

Extend `.githooks/` with a `pre-commit` hook so the machine-checkable subset of the standardization rules is enforced at commit time, with zero new dependencies. The existing `commit-msg` hook stays untouched.

## Non-goals (explicitly out of scope)

- Token/word budgets for SKILL.md bodies ("frequently-loaded" is a judgment call; 9 of 10 current skills would fail; not hookable without fixing content first).
- Filename-suffix validation under `docs/artifacts/` (the convention itself is internally inconsistent today: `commands/harvest.md` mandates `-harvest.md`, AGENTS.md says `-review.md`).
- Secrets regex scanning (`.gitignore` already excludes `opencode.json`; a noisy scanner adds false positives for no real coverage).
- Alphabetical-order enforcement in catalog tables (both tables violate their own ordering rule today).
- Repo-wide kebab-case path enforcement (overlaps the forbidden-dir and top-level-md checks; marginal gain, more allowlist code).
- CI-side checks (the `commitlint` feature already rejected remote enforcement; local hooks cover the stated goal).
- Fixing stale CHANGELOG paths / README step-count drift (unrelated doc drift, not hook-blocking).

## Approaches considered

1. **One new POSIX-sh `pre-commit` file + extend existing `commit-msg` (chosen).** Matches the established `commitlint` feature pattern: `sh` + `grep` only, `ponytail:` ceiling comment, LF pin via existing `.gitattributes` glob, `update-index --chmod=+x` for the executable bit. All checks live in one file as small functions; failure output names the rule and the bypass.
2. Split checks into a shared `checks/` library with thin hooks. More files, zero benefit at ~7 checks. Rejected.
3. pre-commit framework / husky / commitlint npm tooling. Adds node_modules to a markdown-only repo. Rejected (same rationale as the `commitlint` feature spec).

## Recommended checks (what the hooks grab)

Ranked during exploration; every rule below is verified machine-checkable and passes (or is scrubbed by this feature) on day one.

### New `.githooks/pre-commit` (POSIX sh)

Runs only against staged, changed files (`git diff --cached --name-only --diff-filter=ACMR`), never the whole repo.

| # | Check | Rule source | Notes |
|---|---|---|---|
| P1 | Em-dash ban: reject any staged `*.md` containing U+2014 | AGENTS.md body rules | Byte-level scan against index content; the byte sequence is built with POSIX printf octal escapes (`printf '\342\200\224'`), so the script never contains the literal character. Safe after the day-one scrub (below). |
| P2 | SKILL.md frontmatter: `name` is kebab-case (`^[a-z0-9-]+$`) and matches the folder name, except the sanctioned allowlist entry `skills/rubens-project-standardization` -> `project-standardization` | AGENTS.md frontmatter rules | Allowlist is a two-line `case` statement. |
| P3 | SKILL.md frontmatter: `description` starts with `Use when` | AGENTS.md frontmatter rules | Prefix match only. |
| P4 | SKILL.md frontmatter: total frontmatter block <= 1024 characters | AGENTS.md frontmatter rules | Char count between the first two `---` lines. |
| P5 | SKILL.md body: no `^## Skill` heading; must contain an `## Overview` heading somewhere in the body | AGENTS.md body rules | Presence-only (position is not enforced; 6 existing skills have an H1 above `## Overview` and pass). |
| P6 | Catalog sync: any staged `skills/<x>/SKILL.md` (new or modified path not previously tracked) must be referenced in BOTH the `README.md` `## Skills` table and the `AGENTS.md` `## Current skills` table | AGENTS.md "Adding or modifying a skill" | Presence check via `grep` for the folder path in each file (search README for `skills/<x>/`, AGENTS for `<x>` row / path). Trigger: staged SKILL.md whose folder is not yet in HEAD (`git ls-tree HEAD -- skills/<x>/` empty) OR the commit touches the skill folder at all and the catalogs are also being touched; simplest correct rule: if `skills/<x>/SKILL.md` is staged and `git cat-file -e HEAD:skills/<x>/SKILL.md` fails (new skill), both tables must contain the path. Modified existing skills do not re-trigger (rows already exist). |
| P7 | Forbidden staged paths: anything under `temp/`, `old/`, `archive/` (any depth), or `docs/superpowers/`, `.planning/` | AGENTS.md Git & workflow + Artifacts sections | Path-prefix `case` match. |

Dropped during review (user decision, 2026-09-01):

- **P8 top-level `.md` allowlist**: dropped; more root `.md` files are allowed than the STANDARDS.md list.
- **C2 catalog-only `feat:` rejection**: dropped; the existing `commit-msg` hook is left untouched (it only validates the subject format). The AGENTS.md red flag "feat: on catalog-only commits" remains convention-only.

### Bypass and failure UX

- All failures print: which check failed, the offending file/value, the rule source, and `Bypass (emergencies only): git commit --no-verify`.
- No check may scan non-staged content. Merge/revert/fixup commits keep the existing skip behavior in commit-msg; pre-commit also skips during `git commit --amend` message-only edits naturally (nothing new staged).

## Day-one scrub (required before P1/P5 go live)

Exploration found violations that would make the hooks fail on untouched files if scoped repo-wide, or trip the next time these files are edited. This feature scrubs them first:

1. **Em-dashes (U+2014): 24 hits in 4 files.** Replace the em-dash character with a compliant separator (comma, colon, parentheses, or hyphen) preserving meaning:
   - `skills/deep-research/SKILL.md` (16 hits)
   - `skills/deep-research/templates/dossier-template.md` (1 hit)
   - `docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-...-plan.md` (6 hits; only replace the actual U+2014 bytes, never ASCII hyphens)
   - `docs/artifacts/reviews/2026-07-12-harvest.md` (1 hit)
2. **`skills/rubens-project-standardization/SKILL.md` has no `## Overview` heading.** Add one (convert the opening `# Project standardization skill` H1 plus intro paragraph into an `## Overview` section start, keeping content identical).

After the scrub, repo-wide verification must show zero U+2014 bytes in tracked `*.md` (matches the AGENTS.md verification command returning empty).

## Architecture

- `.githooks/pre-commit`: new file, `#!/bin/sh`, checks P1..P7 as sequential functions; every violation is reported (no early exit) and the hook exits 1 if any check failed, so an agent sees all failures in one pass. Shared helpers: `reject <check> <file> <message>`, cached `staged` list.
- `.githooks/commit-msg`: unchanged (Conventional Commits subject check only).
- Constants at the top of each file (allowlists, forbidden dirs) so future edits are one-line changes.
- `.gitattributes` already covers `.githooks/**` (LF pin); no change needed.
- Both files get `git update-index --chmod=+x` before commit.

## Error handling

Every rejection is a hard exit 1 with a human-readable block. No warnings-only mode: a rule that merely warns trains agents to ignore it. If a rule proves too strict in practice, the fix is editing the hook (or the convention), not bypassing it.

## Testing strategy

Verification matrix executed in a scratch clone (`git clone . <tempdir>`) so the real repo index is never polluted; hooks run via real `git commit` invocations so git's bundled sh executes them exactly as in production:

| Case | Expected |
|---|---|
| Commit a clean `*.md` edit | PASS |
| Stage a `*.md` containing U+2014 | REJECT (P1) |
| Stage `skills/bad-skill/SKILL.md` with name mismatching folder | REJECT (P2) |
| Stage a SKILL.md whose description lacks `Use when` | REJECT (P3) |
| Stage a SKILL.md with >1024-char frontmatter | REJECT (P4) |
| Stage a SKILL.md containing `## Skill` heading / missing `## Overview` | REJECT (P5) |
| Stage a brand-new `skills/<x>/SKILL.md` without catalog rows | REJECT (P6); add rows -> PASS |
| Stage `temp/x.md` (or `docs/superpowers/x.md`) | REJECT (P7) |
| Baseline: current repo HEAD commits cleanly after scrub | PASS (all) |

## Documentation wiring (same feature, same commits)

- `AGENTS.md`: Git & workflow section, enforcement sentence now covers the hook set (existing `commit-msg` plus the new `pre-commit`) and the checked rules; the em-dash rule's "verify with" note can mention the hook enforces it.
- `STANDARDS.md`: enforcement line updated to name both hooks.
- `opencode-install.md` step 10: retitle to "Enable the git hooks", describe the full set.
- `CHANGELOG.md`: Added entry under Unreleased/keep-a-changelog format.
- `README.md`: no structural change needed (no new skill/command); only touched if P6 requires catalog rows (it does not; no new skill here).

## Rollout

Single feature branch `plan-standardization-githooks`, per-task Conventional Commits, task order: (1) scrub em-dashes, (2) add `## Overview` to rubens skill, (3) write `pre-commit`, (4) verification matrix in scratch clone, (5) docs wiring. Hooks activate automatically for clones that already ran `git config core.hooksPath .githooks`; fresh clones follow step 10 as before.
