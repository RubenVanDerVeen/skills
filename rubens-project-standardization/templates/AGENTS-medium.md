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
- No commit/push unless user explicitly says to.
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
List the few on-demand files that should be loaded every session. Tool-specific syntax:
- Claude Code: @agents/<file>.md
- opencode: agents/<file>.md is honoured automatically (AGENTS.md is read at any depth)
- Codex / Cursor: include in this file's "On-demand context" table and load on reference
Substitute the syntax your tool recognises. The goal is "few enough to stay in budget, important enough to be present".
-->

@agents/<auto-loaded-file>.md
@agents/<auto-loaded-file>.md

## On-demand Context

<!-- Read on demand (not auto-imported). Tool-specific path: most tools read agents/<file>.md automatically when mentioned; Claude Code needs the explicit @path syntax. -->

| File | Purpose |
|------|---------|
| `agents/todolist.md` | Pending improvements / task list |
| `agents/<topic>.md` | <what it covers> |
| `agents/<topic>.md` | <what it covers> |
| `agents/<domain>/<sub>.md` | <what it covers> |

<!--
Additional on-demand files (one-line purposes):
  - agents/<file>.md: <purpose>
  - agents/<file>.md: <purpose>
-->
