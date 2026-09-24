# Choices registry: execution report

> Closes out the choices-registry plan. Plan: `docs/artifacts/features/choices-registry/2026-09-24-choices-registry-plan.md`. Spec: `docs/artifacts/features/choices-registry/2026-09-24-choices-registry-design.md`.

## Summary

The choices-registry plan landed a cross-feature decision registry at `docs/artifacts/choices/` and wired it into the planning flow (planner lookup, lazy-dev contradiction check), the orchestration flow (raw-material list), the documenter (writes entries at close-out), the slash commands (note destination), and PR descriptions (new `## Choices` section). Six Conventional Commits, no em-dashes, no hook bypasses, no forbidden paths.

## Branch and commits

- Branch: `feat/choices-registry` (off `main`).
- Commits since main (6, oldest first):
  - `17f864e` docs: add plan and spec for choices-registry
  - `96afcb7` feat(conventions): add choices registry convention and seed index
  - `ae7c5b0` feat(agents): wire choices registry into planner, lazy-dev, orchestrator, documenter
  - `b64c5ea` fix(agents): drop out-of-scope orchestrator step 9 choices report clause
  - `a415b16` feat(commands): route choice notes to registry and add PR Choices section
  - `2d73022` docs: log choices registry and sync PR Choices mentions in catalogs

## Files changed

`git diff main..feat/choices-registry --stat`:

```
 AGENTS.md                                          |   5 +-
 CHANGELOG.md                                       |   1 +
 README.md                                          |   2 +-
 agents/documenter.md                               |  15 +-
 agents/lazy-dev.md                                 |   1 +
 agents/orchestrator.md                             |   2 +-
 agents/planner.md                                  |   2 +-
 commands/execute-plan.md                           |   2 +-
 commands/full-cycle.md                             |   2 +-
 docs/artifacts/choices/index.md                    |   6 +
 .../2026-09-24-choices-registry-design.md          | 100 +++++++
 .../2026-09-24-choices-registry-plan.md            | 287 +++++++++++++++++
 skills/pr-description/SKILL.md                     |   3 +
 skills/rubens-project-standardization/SKILL.md     |   2 +-
 .../references/artifacts.md                        |  42 ++-
 15 files changed, 453 insertions(+), 19 deletions(-)
```

Grouped by intent:

- Convention source of truth: `skills/rubens-project-standardization/references/artifacts.md`, `skills/rubens-project-standardization/SKILL.md` (Step 5 conditional), `AGENTS.md`, `docs/artifacts/choices/index.md` (new).
- Flow wiring: `agents/planner.md`, `agents/lazy-dev.md`, `agents/orchestrator.md`, `agents/documenter.md`.
- Command wiring: `commands/execute-plan.md`, `commands/full-cycle.md`.
- PR template: `skills/pr-description/SKILL.md` (new `## Choices` section).
- Catalog sync: `README.md`, `AGENTS.md` (pr-description row in Current skills table).
- Changelog: `CHANGELOG.md` (Unreleased Added bullet).
- Artifacts: `docs/artifacts/features/choices-registry/2026-09-24-choices-registry-{design,plan}.md`.

## Standardization review

### doc-standardizer findings (3 quick-fix, all applied in `2d73022`)

1. CHANGELOG.md Unreleased entry: added.
2. `agents/documenter.md` step 4 stale PR section list: updated to include Choices.
3. `AGENTS.md` and `README.md` pr-description catalog rows stale section list: updated.

No recommendation findings.

### code-standardizer findings

PASS (markdown-only branch, no source code touched).

## Verifier output

- Em-dash check on all touched files: empty.
- Hook active at `.githooks`. All 6 commits passed `pre-commit` and `commit-msg` without `--no-verify`.
- Forbidden paths check: clean (no `docs/superpowers/`, `.planning/`, `temp/`, `old/`, `archive/`).
- Conventional Commits 1.0.0 subjects: all 6 compliant.
- Frontmatter description length: `agents/documenter.md` description = 625 chars (under 1024).
- `docs/artifacts/choices/index.md` seeded with header row + zero data rows.

## Skills loaded

- `project-standardization` (source of truth for artifacts convention, applied by Task 1 and the doc-standardizer pass).
- `code-standardization` (source of truth for code rules, applied by code-standardizer pass - N/A on this markdown-only branch).
- `subagent-driven-development` (run structure: executor per task, reviewer per task).
- `executing-plans` (plan reading, branch-first, per-task commits).
- `pr-description` (PR template updated in Task 3).
- `brainstorming` (used during spec production; not in the execution run itself).
- `writing-plans` (used during plan production; not in the execution run itself).
- `using-superpowers` (always-on process layer).

## `ponytail:` deferrals

None. Every commit is the minimum the plan specified.

## Unverified

None. All checks listed in the plan ran and passed.

## Dispatch Log

| Task | Dispatch |
|---|---|
| Task 1 (convention source of truth + seed index) | executor + reviewer (PASS) |
| Task 2 (flow wiring in agent definitions) | executor + reviewer (rejected: orchestrator step 9 scope creep) + executor (revert in `b64c5ea`) + inline verify |
| Task 3 (commands and PR template) | executor + reviewer (PASS) |
| Structure review | doc-standardizer (3 quick-fix) + code-standardizer (PASS) |
| Quick-fix pass | executor + reviewer (PASS) |
| Documentation | documenter (this report + choices entries) |

## PR description (ready for when the user wants to cut the PR)

First line (PR title, Conventional Commits subject):

```
feat(conventions): add choices registry for cross-feature decision records
```

Body:

```markdown
## Problem
The repo has no durable record of why constraining decisions were made. Specs capture run-local detail; commit messages get scattered; chat history does not survive sessions. When later work wants to remove or change one of these things, there is no place to look up why it exists.

## What changed and why
Added a cross-feature choices registry at `docs/artifacts/choices/` (one file per decision, plus `index.md`). Convention lives in `skills/rubens-project-standardization/references/artifacts.md` (new `## Choices` section). Wired the flow: planner greps the registry before locking spec decisions; lazy-dev has a contradiction check; orchestrator passes rejected approaches and defaults to the documenter; documenter writes entries at close-out (and skips silently when nothing qualifies); commands route note destinations accordingly. PR descriptions gain a `## Choices` section between Verification and Docs.

Committed as six Conventional Commits across the convention, agents, commands, and catalog sync. See commit list in the report's Branch and commits section.

## Verification
- Em-dash check on all touched files: empty.
- Hook active at `.githooks`; all six commits pass pre-commit and commit-msg without `--no-verify`.
- doc-standardizer: 3 quick-fix findings, all applied.
- code-standardizer: PASS (markdown-only branch).
- Forbidden paths check: clean.

## Choices
- `docs/artifacts/choices/2026-09-24-registry-location-decision.md`: registry lives in `docs/artifacts/choices/` alongside `reviews/`, not under `features/` (cross-feature scope).
- `docs/artifacts/choices/2026-09-24-documenter-single-writer-decision.md`: the documenter is the only registry writer; no new writers introduced.
- `docs/artifacts/choices/2026-09-24-planner-full-text-lookup-decision.md`: planner lookup greps the directory full-text; correctness does not depend on `index.md` staying fresh.
- `docs/artifacts/choices/2026-09-24-pr-choices-section-decision.md`: PR descriptions gain a `## Choices` section between `## Verification` and `## Docs`; documenter populates it from run material.

## Docs
- `README.md`, `AGENTS.md` pr-description catalog rows updated.
- `CHANGELOG.md` `[Unreleased]` Added bullet.
- New `docs/artifacts/choices/index.md` (seeded).
- `skills/rubens-project-standardization/references/artifacts.md` new `## Choices` section + tree + grammar + redirect + memory-clause updates.
- `skills/pr-description/SKILL.md` new template section.
```
