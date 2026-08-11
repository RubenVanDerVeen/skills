# <Project Name>: Agent Context

## Overview

<2–3 sentences: what the project is, who the team is, who the client / customer is.>

## Team

| Field      | Value |
|------------|-------|
| Group / org | <value> |
| Tutor / lead | <value> |
| Team size  | <value> |
| Disciplines | <value> |

## Milestones

| Date     | Milestone |
|----------|-----------|
| <date>   | <event>   |
| <date>   | <event>   |
| <date>   | <event>   |

## Key Constraints

<Hard rules: regulatory, physical, deadline. The things that change architecture if violated.>

- **<Constraint>:** <value>
- **<Constraint>:** <value>

## Discipline Boundaries

| Top-level dir | Owner | Scope |
|---------------|-------|-------|
| `mechanical/` | <discipline> | <what lives here> |
| `electrical/` | <discipline> | <what lives here> |
| `software/`   | <discipline> | <what lives here> |

## Standards Stack

This project follows the standards stack documented in `docs/research/<paper>.pdf`. For agent operating notes on the stack, see the `project-standardization` skill, reference `standards-stack.md`. Do **not** inline the standards stack into this file; it lives in `README.md` and the paper.

## Git & Workflow

- Repo: <url>
- **No commit/push without explicit user instruction.** Default: every commit waits for the user.
- **Carve-out: spec/plan-driven development and execution.** When the user has approved both a spec and a plan that references it (both under `docs/artifacts/features/<feature>/`), and the agent is currently executing that plan, the agent commits on its own volition at the boundaries the plan specifies (typically per task or per phase). Outside an approved plan, the default rule applies.
- **Default to a feature branch for features.** Use `feat/<scope>` (or a per-plan `plan-<name>`) for features, modules, and non-trivial changes. Small fixes (typos, single-line tweaks, dep bumps, docs-only edits) can land directly on the default branch. Plan execution follows the same default: each plan runs in its own branch, cut from the latest default branch at plan start. The user can always say otherwise.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- Commits are enforced by a tracked `commit-msg` hook (`.githooks/commit-msg`); activate per clone with `git config core.hooksPath .githooks`. Bypass: `git commit --no-verify`.
- **Bundle related changes into a single commit.** One logical change = one commit; never commit/push per tweak.
- Changelog: `CHANGELOG.md` grouped by sprint, Keep a Changelog 1.1.0.
- Naming: kebab-case ASCII paths, English structural paths, ISO 8601 date prefix for time-based filenames.
- <Branch model, hooks, signing rules.>

### Versioning

<!--
For shipped-software projects (Tauri apps, CLIs, libraries, installers): uncomment the block below and fill it in. Skip for sub-projects versioned through a parent. During 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only.
-->

<!--
- **Canonical source:** <one file + field, e.g. `src-tauri/tauri.conf.json` -> `version`>
- **Sync targets** (must mirror canonical source in every release commit): <e.g. `src-tauri/Cargo.toml`, `package.json`>
- **Policy:** SemVer 2.0.0. Decision table + release-cut recipe: `references/versioning.md` in the `project-standardization` skill.
- **Trigger:** plan execution appends to `[Unreleased]` in `CHANGELOG.md`. Cutting a version is deliberate, user-invoked.
- **Last release:** <tag + date, e.g. `v0.3.0` - `2026-08-02`>
-->

## Artifacts

Specs, plans, multi-plan outlines/manifests, and reports live under `docs/artifacts/features/<feature>/`; reviews live in `docs/artifacts/reviews/` (flat log). Filename: `YYYY-MM-DD-<topic>-<type>.md`, suffix signals type (`-design` spec, `-plan`, `-outline`, `-manifest`, `-report`, `-review`, `-audit`). When delegating to superpowers (`brainstorming`, `writing-plans`) or GSD, name the canonical path (`docs/artifacts/features/<feature>/...`) instead of the framework default (`docs/superpowers/...`, `.planning/...`); both frameworks accept the override. A `docs/superpowers/`, `.planning/`, or other framework-native directory should never land in this repo. If one does, `git rm` it.

## Knowledge graph (graphify)

<!-- Keep this section whenever `graphify-out/graph.json` exists (any tier). Delete only when there is no graph. -->

`graphify-out/` holds a queryable code graph (refreshed by a post-commit hook; AST-only, no LLM).
**If `graphify-out/graph.json` exists, query it BEFORE grep/glob/Read** for any architecture,
cross-file, "what touches X", or "how does X work" question: `graphify query "<question>"`
(~1–2K tokens, budget-capped; grep output gets re-billed on every later prompt). Name a concrete
file or symbol. `graphify explain "<Node>"` for one symbol; `GRAPH_REPORT.md` = overview only.
Stale graph → `graphify update .` (~30 s, no LLM). If the `graphify` skill is available, load it
for the query/path/explain flow.

## Auto-loaded on-demand files

<!--
List the few on-demand files that should be loaded every session. Tool-specific syntax varies; substitute the syntax your active agent recognises (some agents use `@path`, some auto-load by reference).
-->

@.agents/<auto-loaded-1>.md
@.agents/<auto-loaded-2>.md

## On-demand Context

| File | Purpose |
|------|---------|
| `.agents/todolist.md` | Pending tasks (also mirrored in Plane if configured) |
| `.agents/<domain>.md` | <what it covers> |
| `.agents/<domain>.md` | <what it covers> |
| `.agents/<domain>/<sub>.md` | <what it covers> |

<!--
Additional on-demand files (one-line purposes):
  - .agents/<file>.md: <purpose>
  - .agents/<file>.md: <purpose>
-->

## Sprint Workflow Reminders

- At sprint close: export `docs/source/<topic>/` to `docs/deliverables/sprint<N>-<topic>/`.
- Add retrospective note to `docs/project-management/retrospectives/` (ISO 8601 prefix).
- Update `CHANGELOG.md` with a `## [Sprint N]: YYYY-MM-DD` section.
- Update component test docs under `docs/components/<component>/test/`.

## Adding features, modules, or components

When you add a new feature, module, component, or skill, update every catalog or table that lists the existing set in the same commit. Fill the list below at bootstrap with the actual catalogs in this project (typical large project: discipline-boundary table, services/components table, `CHANGELOG.md`, `README.md` feature index).

- `<catalog-file>`: <what it lists>
- `<catalog-file>`: <what it lists>

Red flags (any one = stop and fix before committing):

- The new item is in the source tree but not in any catalog above.
- The user had to remind you to update a doc.
- Two catalogs disagree (one has the new entry, another does not).
