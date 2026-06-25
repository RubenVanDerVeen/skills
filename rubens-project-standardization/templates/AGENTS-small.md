# <Project Name>: Agent Notes

Context for AI coding agents that follow the agents.md convention (opencode, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.) working on this repo. Claude Code requires the `CLAUDE.md` shim at the repo root that imports this file — the skill `project-standardization` ships `templates/CLAUDE.md` for that. Loaded automatically each session. Start here.

## What this is

<2–3 sentences. What the project does, the stack, the user persona. Mention the primary OS / target if relevant.>

## Stack

- **<Framework>**: <one-line role>.
- **<Language>:** <version, key idioms / features used>.
- **<Build tool / package manager>**: <name + version pin if relevant>.

## Critical conventions

<The non-obvious things an agent will get wrong without being told. Examples:>

### <Convention area 1>

- <Rule>.
- <Rule>.

### <Convention area 2>

- <Rule>.

## Build environment

<Only if the build is non-standard. Most projects can skip this section. Otherwise: required tools, PATH gotchas, OS-specific notes.>

## Git & workflow

- Repo: <url>
- **No commit/push unless user explicitly says to.** Carve-out: during plan execution (e.g. GSD-style phase plans), commit-per-phase is the expected behaviour; the agent commits each phase as it lands.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- <Any other project-specific rules: branch model, hooks, signing.>
