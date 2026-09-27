# Execution report: release-description

- **Date:** 2026-09-27
- **Branch:** `feat/release-description` (base: `main` at `4309b95^`)
- **Plan:** `docs/artifacts/features/release-description/2026-09-27-release-description-plan.md`
- **Spec:** `docs/artifacts/features/release-description/2026-09-27-release-description-design.md`
- **Versioning:** unversioned/no bump (repo `AGENTS.md` declares no `### Versioning` subsection)

## Summary

Two commits. The new `release-description` skill shipped (`skills/release-description/SKILL.md`: one five-section template, Summary / Highlights / Breaking changes / Internal / Full changelog) together with its catalog rows (README Skills table + Layout block, AGENTS.md Current skills table), the CHANGELOG bullet, and pipeline wiring in three sites: `references/versioning.md` (policy pointer + step 5 tag command now reads the skill's `.release-notes.md` body), `agents/documenter.md` (new step 6.1: write the body, copy character-for-character to commit body, tag annotation, Release page), and `agents/orchestrator.md` (step 8 dispatch clause). Spec and plan landed in their own docs commit ahead of the feat commit, per the plan's two-commit shape (the plan's Task 3 single-commit boundary covers the code side; the spec/plan pair shipped first as `4309b95`). Standardization review produced one shared finding (missing trailing newline at EOF in the new `SKILL.md`), quick-fixed and re-reviewed. Markdown-only change; no command file, no `references/` folder, no backfill of past releases (spec non-goals).

## Branch and commits

| Hash | Type | Message | Description |
|---|---|---|---|
| `4309b95` | docs | `docs: add plan and spec for release-description` | Spec (165 lines) + plan (292 lines) under `docs/artifacts/features/release-description/`. |
| `901d4fc` | feat | `feat(skills): add release-description standard for releases, tags, and changelog headings` | Single feat commit per plan Task 3: new SKILL.md, versioning.md pointer + step 5, documenter.md step 6.1, orchestrator.md step 8 clause, README row + Layout line, AGENTS.md row, CHANGELOG bullet. Exactly 7 files. |

## Files changed

Aggregate diff (`git diff main..901d4fc`): 9 files, +533 / −3.

| Path | +/− | Why |
|---|---|---|
| `skills/release-description/SKILL.md` | +66 | New skill: Overview, When to use, Template (4-space indented block), Rules, Audience and tone, Related. |
| `skills/rubens-project-standardization/references/versioning.md` | +3/−1 | Policy pointer line near the top; step 5 tag command now `git tag -a vX.Y.Z -m "$(cat .release-notes.md)"` per the skill. |
| `agents/documenter.md` | +1 | New step 6.1 between ship bump (6) and report commit (7): write `.release-notes.md`, copy verbatim to all surfaces, delete scratch file. |
| `agents/orchestrator.md` | +1/−1 | Step 8 dispatch clause: release tasks carry the release-description requirement. |
| `README.md` | +3/−1 | Skills table row (alphabetical, between `pr-description` and `rubens-project-standardization`) + Layout block entry as last skills-tree line. |
| `AGENTS.md` | +1 | `## Current skills` row, same alphabetical position. |
| `CHANGELOG.md` | +1 | `[Unreleased]` / `### Added` bullet with spec path. |
| `docs/artifacts/features/release-description/2026-09-27-release-description-design.md` | +165 | Spec (new). |
| `docs/artifacts/features/release-description/2026-09-27-release-description-plan.md` | +292 | Plan (new). |

Per-commit breakdown:

- `4309b95`: 2 files, +457/−0 (spec + plan).
- `901d4fc`: 7 files, +76/−3.

## Standardization review

### doc-standardizer

PASS with one finding, tagged quick-fix: missing trailing newline at EOF in `skills/release-description/SKILL.md`. Fixed in the working tree, re-reviewed: PASS. Nothing remains from this branch. No pre-existing out-of-scope findings were raised.

### code-standardizer

PASS with the same single finding (trailing newline). Same quick-fix satisfies it; re-reviewed: PASS. Nothing remains.

Both audits' finding is applied in close-out commit (see Dispatch Log); the `901d4fc` feature commit itself is untouched, as required.

## Documentation updates

- `skills/release-description/SKILL.md` (new): the standard itself, 388-word body.
- `README.md`: Skills table row + Layout block entry, landed in `901d4fc`.
- `AGENTS.md`: Current skills table row, landed in `901d4fc`.
- `CHANGELOG.md`: `[Unreleased]` / `### Added` bullet, landed in `901d4fc`.
- `opencode-install.md`: deliberately untouched. Per AGENTS.md "Adding or modifying a skill", it changes only if its Verify section names the skill by name; it does not name `release-description`. Re-checked at close-out: no reference exists, none needed.
- `external-skills.md`: untouched; personal skill, not external.
- No `## Commands` section and no `commands/` file: the spec rules out a slash command (close-out internal step, discovered by frontmatter description-match).
- `agents/README.md` roster: untouched; no new agent, no agent rename.

Catalog correctness re-checked by the documenter at close-out: folder `skills/release-description/`, frontmatter `name: release-description`, README row (line 23), Layout line (line 95), and AGENTS.md row (line 146) all agree. No further catalog updates required.

## Verifier output

Per-task and close-out verification results:

- Task 1: frontmatter block 368 chars (< 1024); body word count 388 (< 400); `description` starts with `Use when`; `name` kebab-case matches folder; em-dash scan over `skills/release-description/` CLEAN.
- Task 2: `opencode agent list` parses cleanly, `documenter` and `orchestrator` listed; `release-description` referenced in all three wired sites (`agents/documenter.md`, `agents/orchestrator.md`, `references/versioning.md`); consistency read passes: `git tag -a vX.Y.Z -m "$(cat .release-notes.md)"` appears with identical wording, count 1, in both `agents/documenter.md` and `references/versioning.md`.
- Task 3: hooks active (`git config core.hooksPath` = `.githooks`); pre-commit + commit-msg passed first attempt; `git show --stat` confirms exactly 7 files in `901d4fc`, subject `feat(skills): add release-description standard for releases, tags, and changelog headings`, no body, no trailers; catalog agreement `grep -c release-description` hits README.md (2), AGENTS.md (1), CHANGELOG.md (1); em-dash scan CLEAN across all touched markdown.

## Skills loaded

- `project-standardization` (by doc-standardizer, per its agent definition).
- `code-standardization` (by code-standardizer, per its agent definition).

## `ponytail:` deferrals

None. The executor reported no shortcuts; no `ponytail:` comments landed in the diff.

## Unverified items

- Behavioral acceptance is deferred to the next real release cut: an agent told to cut a release produces the `chore(release): vX.Y.Z` subject, a five-section body with `None` where empty, and a tag annotation identical to the commit body character-for-character. The wiring and template are verified; the behavior only proves itself at first use.
- The skill's Template block uses a 4-space indented block instead of the design's fenced sketch. Deliberate deviation, documented in plan Global Constraints and Task 2 Step 3 rationale: sibling consistency with `pr-description/SKILL.md` and heading-scanner safety in the pre-commit hook. Recorded here so the deviation is visible, not silent.

## Dispatch Log

| Phase | Agent | Result |
|---|---|---|
| Task 1: create `skills/release-description/SKILL.md` | dispatched: executor + reviewer | PASS; worked from working-tree diff, no commit (plan's single-commit boundary). |
| Task 2: wire versioning.md, documenter.md, orchestrator.md | dispatched: executor + reviewer | PASS; worked from working-tree diff, no commit. |
| Task 3: catalogs, CHANGELOG, single commit | dispatched: executor + reviewer | PASS; commit `901d4fc`, reviewed against the commit. |
| Closing structure review | doc-standardizer | PASS, 1 quick-fix finding (trailing newline EOF). |
| Closing code review | code-standardizer | PASS, same finding. |
| Quick-fix | executor (in-run) | Trailing newline applied to working tree; re-reviewed, PASS. |
| Choices registry + report + quick-fix commit | dispatched: documenter | Decision record `2026-09-27-release-description-template-decision.md` + index row; this report; trailing-newline fix committed as `style(skills)`. |
