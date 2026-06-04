# <Project Name> — Claude Context

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

This project follows the standards stack documented in `docs/research/<paper>.pdf`. For Claude operating notes on the stack, see the `rubens-project-standardization` skill, reference `standards-stack.md`. Do **not** inline the standards stack into this file — it lives in `README.md` and the paper.

## Git & Workflow

- Repo: <url>
- No commit/push unless user explicitly says to.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- Changelog: `CHANGELOG.md` grouped by sprint, Keep a Changelog 1.1.0.
- Naming: kebab-case ASCII paths, English structural paths, ISO 8601 date prefix for time-based filenames.
- <Branch model, hooks, signing rules.>

@claude/<auto-loaded-1>.md
@claude/<auto-loaded-2>.md

## On-demand Context

| File | Purpose |
|------|---------|
| `claude/todolist.md` | Pending tasks (also mirrored in Plane if configured) |
| `claude/<domain>.md` | <what it covers> |
| `claude/<domain>.md` | <what it covers> |
| `claude/<domain>/<sub>.md` | <what it covers> |

<!-- Load on demand (not auto-imported):
  - claude/<file>.md           — <purpose>
  - claude/<file>.md           — <purpose>
-->

## Sprint Workflow Reminders

- At sprint close: export `docs/source/<topic>/` → `docs/deliverables/sprint<N>-<topic>/`.
- Add retrospective note to `docs/project-management/retrospectives/` (ISO 8601 prefix).
- Update `CHANGELOG.md` with a `## [Sprint N] — YYYY-MM-DD` section.
- Update component test docs under `docs/components/<component>/test/`.
