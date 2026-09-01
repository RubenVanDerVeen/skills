# skills: personal agent environment

## What this is

Personal agent environment monorepo for AI coding agents that follow the [agents.md](https://agents.md) convention (opencode, Claude Code, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.). Three kinds of content: skills (`skills/<name>/SKILL.md`), slash commands (`commands/`), and opencode agent definitions (`agents/`). Top-level `.md` files (`README.md`, `opencode-install.md`, `external-skills.md`) are repo docs, not skills.

The user adds, refines, and shares skills, commands, and agents over time. Auto-loaded for any agent that opens this repo.

## Stack

- **Content:** Markdown only. No build step, no tooling, no runtime.
- **Discovery:** `AGENTS.md` at the repo root; each `SKILL.md` uses YAML frontmatter (`name`, `description`).
- **Distribution:** Git remote `https://github.com/RubenVanDerVeen/skills.git`, branch `main`.

## Critical conventions

### File layout

```
skills/
├── README.md                                  <- catalog overview
├── opencode-install.md                        <- bootstrap doc
├── external-skills.md                         <- external skill catalog
├── AGENTS.md                                  <- this file
├── commands/                                  <- all slash commands live here
│   ├── goal.md                                <- /goal: iterate until verifier passes
│   ├── execute-plan.md                        <- /execute-plan: subagent-driven plan execution
│   ├── full-cycle.md                          <- /full-cycle: single-pass brainstorm > spec > plan > dispatch orchestrator (or handoff)
│   ├── iterate-skill.md                       <- /iterate-skill: refine a skill via subagent review loops
│   ├── harvest.md                             <- /harvest: mine sessions for skill improvements
│   ├── multi-plan.md                          <- /multi-plan: start multi-plan orchestration
│   ├── standardize.md                         <- /standardize: bootstrap or restructure a project
│   ├── standardize-code.md                    <- /standardize-code: audit code structure via code-standardization
│   └── standardize-migrate.md                 <- /standardize-migrate: migrate an older layout
├── agents/                                    <- opencode agent definitions (planner, orchestrator, writer, executor, reviewer, oracle, inventree)
└── skills/                                    <- all skill folders live here
    ├── drawio-pro/SKILL.md
    ├── typst-pro/SKILL.md
    └── rubens-project-standardization/
        ├── SKILL.md
        ├── references/
        └── templates/
```

A skill lives in a folder under the top-level `skills/` directory. A folder without `SKILL.md` is not a skill. Top-level `.md` files are repo docs, not skills, and they should not have frontmatter. Two exceptions exist because each doubles as a discoverable skill: `opencode-install.md` (install doc) and `external-skills.md` (external skill catalog). Keep both as-is.

All slash commands live at the top-level `commands/` directory, never inside a skill folder. The `.md` files become slash commands only after being copied to the agent's commands directory. See the Slash commands section below for the full pattern.

### Slash commands

Slash commands give a skill an explicit entry point for when the agent does not pick it up automatically from frontmatter description matching. All commands live as `.md` files in the top-level `commands/` directory, never inside a skill folder. Current examples: `commands/standardize.md` (`/standardize`), `commands/multi-plan.md` (`/multi-plan`), `commands/harvest.md` (`/harvest`), `commands/goal.md` (`/goal`), `commands/execute-plan.md` (`/execute-plan`), `commands/full-cycle.md` (`/full-cycle`), `commands/iterate-skill.md` (`/iterate-skill`), `commands/standardize-migrate.md` (`/standardize-migrate`), `commands/standardize-code.md` (`/standardize-code`).

#### File format

Each command is one `.md` file with YAML frontmatter and a short body:

```markdown
---
description: <one-line summary of what the command does>
---

<numbered or single-paragraph instructions telling the agent which skill to load and what to do>
```

- Frontmatter has `description` only (no `name` field; the file name is the command name).
- The body tells the agent to load the relevant skill and run specific steps. It does **not** reimplement the skill.
- Optional `$ARGUMENTS` placeholder for commands that take parameters (e.g. tier override). See `commands/standardize.md` for the pattern.

#### Sync pattern

The `commands/` directory is inactive inside the skills directory. Two-step sync per machine:

1. Copy each folder under `skills/` to the agent's skills directory (e.g. `~/.claude/skills/`, `~/.config/opencode/skills/`).
2. Copy `commands/*.md` to the agent's commands directory:

| Agent | Global | Per-project |
|-------|--------|-------------|
| OpenCode | `~/.config/opencode/command/` | `.opencode/command/` |
| Claude Code | `~/.claude/commands/` | `.claude/commands/` |

OpenCode uses the singular `command/` directory; Claude Code uses plural `commands/`. Do not normalise across agents.

#### Documenting commands in the skill

A skill that has an associated command must add a `## Commands` section near the end of `SKILL.md`:

- Table listing each command with its purpose.
- The source path in the top-level `commands/` directory (e.g. `commands/multi-plan.md`).
- Reminder that the file is dead weight inside the skills directory until step 2 of the sync.

#### When to add a command

Add a command when:
- The skill's description triggers on user signals that are easy to miss (e.g. multi-module requests get buried mid-brainstorm).
- The user benefits from an explicit entry point to bypass auto-discovery.

Do not add a command for every skill. If the frontmatter description reliably triggers loading, no command is needed. Commands are an escape hatch, not a default. A command without a parent skill (universal workflows, cross-cutting tools) lives in the same top-level `commands/` directory; no skill-folder wrapping is required.

### Agent definitions

Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `doc-standardizer`, `code-standardizer`, `documenter`, `oracle`) and `inventree` (InvenTree inventory sessions via the homelab MCP) live in the top-level `agents/` directory. Same pattern as `commands/`: source of truth here, inactive until copied to `~/.config/opencode/agents/`. They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult, post-implementation structure review goes to `doc-standardizer` then `code-standardizer`, and the documentation/report phase goes to `documenter`). opencode-only; do not copy to Claude Code. Format, sync, token measurements, and tuning rules: `agents/README.md`.

### `SKILL.md` frontmatter rules

```markdown
---
name: <kebab-case>
description: <triggering conditions only>
---
```

- `name`: letters, numbers, hyphens only. No parentheses, no special characters. Must match the folder name.
- `description`: starts with "Use when..." and describes **only** when to load the skill. Never summarises the skill's workflow; the body is the source of truth. Third person. Under ~500 characters if possible.
- Max 1024 characters per skill's frontmatter (the agents.md spec limit).
- The `description` is what the agent uses to decide whether to load the skill. Optimise for retrieval, not summary.

### `SKILL.md` body rules

- No em-dashes (U+2014, `-`). Use commas, colons, periods, parentheses, or hyphens. The rule applies to every file in this repo AND to chat output. Verify with `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty.
- Token efficiency: lean skills under 200 words, frequently-loaded under 500. Move heavy reference to `references/<file>.md` and link from the body.
- Body starts with `## Overview`. Then `## When to use` (or similar). Then the actual content.
- One excellent example beats many mediocre ones. TypeScript or shell is fine, porting is cheap.
- Flowcharts only for non-obvious decisions. Tables for reference. Code in markdown blocks.

### Discovery helpers

- Keywords in the description that an agent would actually search for: tool names, error messages, symptoms, file extensions.
- Keep descriptions stable. Renaming a description is a breaking change for any agent that has memorised the trigger.

## Current skills

| Folder | `name` in frontmatter | What it does |
|---|---|---|
| `skills/drawio-pro/` | `drawio-pro` | Personal draw.io style. Pastel grouped containers, BPMN flowcharts, light-grey legend boxes. |
| `skills/typst-pro/` | `typst-pro` | Typst helpers. Academic frontpage, IEEE templates, Dutch project layout, color tokens. |
| `skills/altium-pro/` | `altium-pro` | Altium Designer knowledge base. PCB rooms, polygon pours, design rules, query snippets, troubleshooting log. |
| `skills/code-standardization/` | `code-standardization` | Source-code structure standard. Formatter/linter/hooks per language, naming, module organization, architecture/dependency boundaries. Multi-language (Python, TS/JS, C/C++, Go, Rust), flat (one standard). Sister to `project-standardization`. |
| `skills/deep-research/` | `deep-research` | End-to-end research pipeline: intake, parallel gather (arxiv + web + own vault), synthesized dossier with citations, then brainstorm or Typst draft. Hermes research profile. |
| `skills/inventree-naming/` | `inventree-naming` | InvenTree part naming convention: dash-separated names, description structure, per-category formats. Source of truth for the convention; the inventree agents embed a condensed copy. |
| `skills/synctool-sync/` | `synctool-sync` | Drive the `synctool` CLI for saved NAS sync jobs (push/pull, copy/update). Dry-run first, hard rails, never auto-runs destructive mirror. |
| `skills/rubens-project-standardization/` | `project-standardization` | Universal project bootstrap. `AGENTS.md` convention, kebab-case paths, ISO 8601 dates, Conventional Commits, Keep a Changelog. Three tiers (small/medium/large). |
| `skills/multi-plan-orchestration/` | `multi-plan-orchestration` | Splits large tasks into foundation + N parallel sub-plans during brainstorming. Decomposition outline, scope-slip handling, manifest with per-agent dispatch prompts. Delegates to existing brainstorming + writing-plans skills. |
| `skills/skill-harvest/` | `skill-harvest` | Mines recent opencode sessions for repeated corrections and skill gaps. Report, approve, apply loop with incremental state. Slash command: `/harvest`. |
| `opencode-install.md` (top-level doc) | `opencode-install` | Bootstrap doc: install commands for superpowers, caveman, graphify, plus the personal skills repo path. |
| `external-skills.md` (top-level doc) | `external-skills` | Catalog of external skills/tools (superpowers, caveman, graphify): what each does, when to use, install pointers. |

The `skills/rubens-project-standardization/` directory keeps the old name for backwards compatibility. The skill's identity is `project-standardization`. Renaming the folder is a future chore.

## Adding or modifying a skill

When you add a new skill to this repo, the work is incomplete unless every catalog that lists existing skills has been updated in the same commit. A skill that isn't discoverable doesn't exist for an agent.

Catalogs to update (in the same commit as the new skill):

- `README.md`: the `## Skills` table (one row per skill, alphabetical).
- `AGENTS.md`: the `## Current skills` table in this file (one row per skill, alphabetical).
- `opencode-install.md`: only if the `## Verify` section lists this skill by name. Currently it does not; skip if no name reference exists.

Steps:

1. `mkdir skills/<name>`, create `skills/<name>/SKILL.md` with frontmatter.
2. (Optional) Add a command file to the top-level `commands/` directory and a `## Commands` section to the `SKILL.md`. See the Slash commands section below for format and sync.
3. Update the catalogs above in the same commit. The folder name, frontmatter `name`, and table entries must match exactly.
4. Verify the frontmatter passes: `name` in kebab-case, `description` starts with "Use when...", description does not summarise the workflow, under 1024 chars total.
5. Verify the body: no em-dashes, no top-level `## Skill` heading (use `## Overview` instead), under the token budget for the skill type.
6. Commit. Conventional Commits 1.0.0. Use `feat(skills):` for a new skill, `docs(skills):` if the commit only adds the catalog entries.

Red flags (any one = stop and fix before commit):

- The skill exists in `skills/<name>/` but is not in the `README.md` `## Skills` table.
- The skill is in one catalog but not another (e.g. `README.md` has it, `AGENTS.md` does not).
- The skill has a command in `commands/` but `SKILL.md` has no `## Commands` section.
- The user has to remind you to update a doc. If they did, this section wasn't strong enough; tighten it.
- The commit message says `feat:` but only adds catalog rows. Use `docs:` for catalog-only commits.

To modify an existing skill, edit the `SKILL.md` in place. Skill descriptions are part of the public interface; changing them is a breaking change for any agent that loads by description-match.

## Artifacts

Process meta-documents (specs, plans, multi-plan outlines/manifests, execution reports, reviews) live in `docs/artifacts/`, not next to the code:

- `docs/artifacts/features/<feature>/`: one folder per feature. Holds its `YYYY-MM-DD-<topic>-design.md` (spec), `-plan.md`, `-outline.md`, `-manifest.md`, `-report.md`. Filename suffix signals type.
- `docs/artifacts/reviews/`: flat chronological log of committed audits (`YYYY-MM-DD-<topic>-review.md`).

When delegating to `brainstorming` or `writing-plans` (superpowers) or any GSD-style flow, name the canonical path (`docs/artifacts/features/<feature>/...`) instead of the framework default (`docs/superpowers/...`, `.planning/...`). A `docs/superpowers/` or `.planning/` directory should never land in this repo; if one does, `git mv` its contents into `docs/artifacts/` and remove the emptied dir. See `references/artifacts.md` in the `project-standardization` skill for the full convention.

## Git & workflow

- Repo: `https://github.com/RubenVanDerVeen/skills.git`
- **No commit/push without explicit user instruction.** Default: every commit waits for the user.
- **Carve-out: spec/plan-driven development and execution.** When the user has approved both a spec (in `docs/artifacts/features/`) and a plan that references it (in `docs/artifacts/features/`), and the agent is currently executing that plan, the agent commits on its own volition at the boundaries the plan specifies (typically per task or per phase). Specs, plans, reviews, and the code they describe ship together. Outside an approved plan, the default rule applies.
- **Default to a feature branch for non-trivial work.** Use `feat/<scope>` (or a per-plan `plan-<name>`) for features, new skills, and multi-step changes. Typos, single-line tweaks, and catalog-row syncs can land directly on `main`.
- **Bundle related changes into a single commit.** One logical change = one commit; never commit per tweak. A new skill ships with its catalog rows and any command file in one commit.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Enforced by tracked git hooks (`.githooks/`): `commit-msg` rejects non-Conventional-Commits messages; `pre-commit` rejects em-dashes in markdown, bad SKILL.md frontmatter (name, description, size, headings), new skills missing from the README/AGENTS catalogs, and forbidden paths (`temp/`, `old/`, `archive/`, `docs/superpowers/`, `.planning/`). Activate once per clone with `git config core.hooksPath .githooks` (see `opencode-install.md` step 10). Bypass: `git commit --no-verify`.
- Branch model: `main`.
- No secrets in tracked files. No `temp/`, no `old/`, no `archive/`. Git history is the archive.

## Related

- The `project-standardization` skill (in this repo) is the source of truth for bootstrapping any other project. Use it to scaffold a new project that itself needs agent context.
- The `AGENTS.md` spec: <https://agents.md>
- The `writing-skills` skill (from superpowers) is the meta-skill for authoring new skills well.
