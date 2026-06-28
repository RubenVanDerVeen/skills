# <Project Name>: Agent Context

## Overview

<2–3 sentences: what this project is, the stack, the user persona.>

## Key Facts

<Bullets of non-obvious facts an agent needs as baseline. IPs, URLs, conventions, constraints, version pins.>

- **<Fact>:** <value>
- **<Fact>:** <value>
- **<Fact>:** <value>

## Git & Workflow

- Repo: <url>
- **No commit/push without explicit user instruction.** Default: every commit waits for the user.
- **Carve-out: spec/plan-driven development and execution.** When the user has approved both a spec (in `docs/artifacts/specs/`) and a plan that references it (in `docs/artifacts/plans/`), and the agent is currently executing that plan, the agent commits on its own volition at the boundaries the plan specifies (typically per task or per phase). Outside an approved plan, the default rule applies.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- Changelog: Keep a Changelog 1.1.0, grouped by release / milestone.
- <Any project-specific git rules.>

## <Central Reference Table>

<One table: services, endpoints, components, VMs, modules. Slim version only; full detail in the on-demand subdirectory.>

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| <row>    | <row>    | <row>    |

## Auto-loaded on-demand files

<!--
List the few on-demand files that should be loaded every session. Tool-specific syntax varies; substitute the syntax your active agent recognises (some agents use `@path`, some auto-load by reference). The goal is "few enough to stay in budget, important enough to be present".
-->

@.agents/<auto-loaded-file>.md
@.agents/<auto-loaded-file>.md

## On-demand Context

<!-- Read on demand (not auto-imported). Tool-specific path: most tools read .agents/<file>.md automatically when mentioned; some agents need an explicit @path import. -->

| File | Purpose |
|------|---------|
| `.agents/todolist.md` | Pending improvements / task list |
| `.agents/<topic>.md` | <what it covers> |
| `.agents/<topic>.md` | <what it covers> |
| `.agents/<domain>/<sub>.md` | <what it covers> |

<!--
Additional on-demand files (one-line purposes):
  - .agents/<file>.md: <purpose>
  - .agents/<file>.md: <purpose>
-->

## Adding features, modules, or components

When you add a new feature, module, component, or skill, update every catalog or table that lists the existing set in the same commit. Fill the list below at bootstrap with the actual catalogs in this project.

- `<catalog-file>`: <what it lists>
- `<catalog-file>`: <what it lists>

Red flags (any one = stop and fix before committing):

- The new item is in the source tree but not in any catalog above.
- The user had to remind you to update a doc.
- Two catalogs disagree (one has the new entry, another does not).
