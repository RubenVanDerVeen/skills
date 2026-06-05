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
- No commit/push unless user explicitly says to.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- Changelog: `CHANGELOG.md` grouped by sprint, Keep a Changelog 1.1.0.
- Naming: kebab-case ASCII paths, English structural paths, ISO 8601 date prefix for time-based filenames.
- <Branch model, hooks, signing rules.>

## Auto-loaded on-demand files

<!--
List the few on-demand files that should be loaded every session. Tool-specific syntax:
- Claude Code: @agents/<file>.md
- opencode: agents/<file>.md is honoured automatically
- Codex / Cursor: include in the on-demand table below and load on reference
-->

@agents/<auto-loaded-1>.md
@agents/<auto-loaded-2>.md

## On-demand Context

| File | Purpose |
|------|---------|
| `agents/todolist.md` | Pending tasks (also mirrored in Plane if configured) |
| `agents/<domain>.md` | <what it covers> |
| `agents/<domain>.md` | <what it covers> |
| `agents/<domain>/<sub>.md` | <what it covers> |

<!--
Additional on-demand files (one-line purposes):
  - agents/<file>.md: <purpose>
  - agents/<file>.md: <purpose>
-->

## Sprint Workflow Reminders

- At sprint close: export `docs/source/<topic>/` to `docs/deliverables/sprint<N>-<topic>/`.
- Add retrospective note to `docs/project-management/retrospectives/` (ISO 8601 prefix).
- Update `CHANGELOG.md` with a `## [Sprint N]: YYYY-MM-DD` section.
- Update component test docs under `docs/components/<component>/test/`.
