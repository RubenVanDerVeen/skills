# <Project Name>: Agent Notes

Context for AI coding agents that follow the agents.md convention (opencode, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.) working on this repo. Claude Code requires the `CLAUDE.md` shim at the repo root that imports this file; the skill `project-standardization` ships `templates/CLAUDE.md` for that. Loaded automatically each session. Start here.

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

## Adding features, modules, or components

When you add a new feature, module, component, or skill, update every catalog or table that lists the existing set in the same commit. Fill the list below at bootstrap with the actual catalogs in this project.

- `<catalog-file>`: <what it lists>
- `<catalog-file>`: <what it lists>

Red flags (any one = stop and fix before committing):

- The new item is in the source tree but not in any catalog above.
- The user had to remind you to update a doc.
- Two catalogs disagree (one has the new entry, another does not).

## Build environment

<Only if the build is non-standard. Most projects can skip this section. Otherwise: required tools, PATH gotchas, OS-specific notes.>

## Git & workflow

- Repo: <url>
- **No commit/push without explicit user instruction.** Default: every commit waits for the user.
- **Carve-out: spec/plan-driven development and execution.** When the user has approved both a spec (in `docs/artifacts/specs/`) and a plan that references it (in `docs/artifacts/plans/`), and the agent is currently executing that plan, the agent commits on its own volition at the boundaries the plan specifies (typically per task or per phase). Outside an approved plan, the default rule applies.
- **Default to a feature branch for features.** Use `feat/<scope>` (or a per-plan `plan-<name>`) for features, modules, and non-trivial changes. Small fixes (typos, single-line tweaks, dep bumps, docs-only edits) can land directly on the default branch. Plan execution follows the same default: each plan runs in its own branch, cut from the latest default branch at plan start. The user can always say otherwise.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
- **Bundle related changes into a single commit.** One logical change = one commit; never commit/push per tweak.
- <Any other project-specific rules: branch model, hooks, signing.>

## Artifacts

Specs, plans, and reviews live in `docs/artifacts/{specs,plans,reviews}/` (filename: `YYYY-MM-DD-<topic>-<type>.md`). When delegating to superpowers (`brainstorming`, `writing-plans`) or GSD, name the canonical path (`docs/artifacts/specs/...` or `docs/artifacts/plans/...`) instead of the framework default (`docs/superpowers/...`, `.planning/...`); both frameworks accept the override. A `docs/superpowers/`, `.planning/`, or other framework-native directory should never land in this repo. If one does, `git rm` it.

## Knowledge graph (graphify)

<!-- Keep this section whenever `graphify-out/graph.json` exists (any tier, including small). Delete only when there is no graph. -->

`graphify-out/` holds a queryable code graph (refreshed by a post-commit hook; AST-only, no LLM).
**If `graphify-out/graph.json` exists, query it BEFORE grep/glob/Read** for any architecture,
cross-file, "what touches X", or "how does X work" question: `graphify query "<question>"`
(~1–2K tokens, budget-capped; grep output gets re-billed on every later prompt). Name a concrete
file or symbol. `graphify explain "<Node>"` for one symbol; `GRAPH_REPORT.md` = overview only.
Stale graph → `graphify update .` (~30 s, no LLM). If the `graphify` skill is available, load it
for the query/path/explain flow.
