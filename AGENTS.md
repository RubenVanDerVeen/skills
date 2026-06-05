# skills: personal agent skills

## What this is

Personal skills catalog for AI coding agents (opencode, Claude Code, Codex, Cursor, Aider, GitHub Copilot). Each skill lives in its own folder as `<name>/SKILL.md`. Top-level `.md` files (`README.md`, `opencode-install.md`) are repo docs, not skills.

The user adds, refines, and shares skills over time. Auto-loaded for any agent that opens this repo.

## Stack

- **Content:** Markdown only. No build step, no tooling, no runtime.
- **Discovery:** `AGENTS.md` at the repo root; each `SKILL.md` uses YAML frontmatter (`name`, `description`).
- **Distribution:** Git remote `https://github.com/RubenVanDerVeen/skills.git`, branch `master`.

## Critical conventions

### File layout

```
skills/
├── README.md                                  <- catalog overview
├── opencode-install.md                        <- bootstrap doc
├── AGENTS.md                                  <- this file
├── drawio-pro/SKILL.md
├── typst-pro/SKILL.md
└── rubens-project-standardization/
    ├── SKILL.md
    ├── references/
    └── templates/
```

A skill lives in a folder. A folder without `SKILL.md` is not a skill. Top-level `.md` files are repo docs, not skills, and they should not have frontmatter (the `opencode-install.md` exception exists because it doubles as a discoverable skill; keep it as-is).

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

- No em-dashes (U+2014, `—`). Use commas, colons, periods, parentheses, or hyphens. The rule applies to every file in this repo AND to chat output. Verify with `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty.
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
| `drawio-pro/` | `drawio-pro` | Personal draw.io style. Pastel grouped containers, BPMN flowcharts, light-grey legend boxes. |
| `typst-pro/` | `typst-pro` | Typst helpers. Academic frontpage, IEEE templates, Dutch project layout, color tokens. |
| `rubens-project-standardization/` | `project-standardization` | Universal project bootstrap. `AGENTS.md` convention, kebab-case paths, ISO 8601 dates, Conventional Commits, Keep a Changelog. Three tiers (small/medium/large). |
| `opencode-install.md` (top-level doc) | `opencode-install` | Bootstrap doc: superpowers + caveman + this repo's path. |

The `rubens-project-standardization/` directory keeps the old name for backwards compatibility. The skill's identity is `project-standardization`. Renaming the folder is a future chore.

## Adding or modifying a skill

To add a new skill:

1. `mkdir <name>`, create `<name>/SKILL.md` with frontmatter.
2. Add a row to the "Current skills" table above.
3. Verify the frontmatter passes: `name` in kebab-case, `description` starts with "Use when...", description does not summarise the workflow, under 1024 chars total.
4. Verify the body: no em-dashes, no top-level `## Skill` heading (use `## Overview` instead), under the token budget for the skill type.
5. Commit. Conventional Commits 1.0.0.

To modify an existing skill, edit the `SKILL.md` in place. Skill descriptions are part of the public interface; changing them is a breaking change for any agent that loads by description-match.

## Git & workflow

- Repo: `https://github.com/RubenVanDerVeen/skills.git`
- No commit/push unless the user explicitly says to.
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`). `chore:`, `docs:`, `feat:`, `fix:`, `refactor:` are the common types.
- Branch model: `master` (rename to `main` when convenient; ask before rewriting history).
- No secrets in tracked files. No `temp/`, no `old/`, no `archive/`. Git history is the archive.

## Related

- The `project-standardization` skill (in this repo) is the source of truth for bootstrapping any other project. Use it to scaffold a new project that itself needs agent context.
- The `AGENTS.md` spec: <https://agents.md>
- The `writing-skills` skill (from superpowers) is the meta-skill for authoring new skills well.
