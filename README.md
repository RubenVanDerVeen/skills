# skills

Personal skills for AI coding agents that follow the [agents.md](https://agents.md) convention (opencode, Claude Code, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.).

Skills live in folders as `SKILL.md`. The top level holds repo-level docs (this README and the install guide).

## Skills

| Skill | What it does |
|---|---|
| [`drawio-pro`](./drawio-pro/SKILL.md) | Personal draw.io style. Pastel grouped containers, BPMN flowcharts, light-grey legend boxes. |
| [`typst-pro`](./typst-pro/SKILL.md) | Typst helpers. Academic frontpage, IEEE templates, Dutch project layout, color tokens. |
| [`altium-pro`](./altium-pro/SKILL.md) | Altium Designer knowledge base. PCB rooms, polygon pours, design rules, query snippets, troubleshooting log. |
| [`rubens-project-standardization`](./rubens-project-standardization/SKILL.md) | Universal project bootstrap. `AGENTS.md` convention, kebab-case paths, ISO 8601 dates, Conventional Commits, Keep a Changelog. Three tiers (small/medium/large). |
| [`synctool-sync`](./synctool-sync/SKILL.md) | Drive the `synctool` CLI to run saved NAS sync jobs (push/pull, copy/update). Dry-run first, hard rails, never auto-runs destructive mirror. |

## External skills

Beyond the personal skills in this repo, several external sources are installed in the same environment. See [`external-skills.md`](./external-skills.md) for what each does and when to reach for it; install commands live in [`opencode-install.md`](./opencode-install.md).

- **superpowers** - process discipline skills (TDD, debugging, brainstorming, ...)
- **caveman** - terse, low-token output style
- **claude-mem** - persistent cross-session memory
- **graphify** - codebase knowledge graph builder
- **vercel-labs/agent-skills** - React / Next.js / React Native / web-design pack
- **stop-slop** - removes AI writing patterns from prose
- **gsd-core** - spec-driven phase-loop framework

## Install

See [`opencode-install.md`](./opencode-install.md) for the full 8-step bootstrap.

Quick version:

```
# 1. Superpowers — fetch and follow:
https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md

# 2. Caveman
npx -y github:JuliusBrussee/caveman -- --only opencode

# 3. Point opencode at this folder for the personal skills
```

On Windows, step 3 means adding `C:\Users\ruben\Projects\Tools\skills` to opencode's skills discovery path.

## Layout

```
skills/
├── README.md                                    <- you are here
├── opencode-install.md                          <- install / bootstrap
├── external-skills.md                           <- external skill catalog
├── drawio-pro/SKILL.md
├── typst-pro/SKILL.md
├── altium-pro/SKILL.md
├── rubens-project-standardization/SKILL.md
└── synctool-sync/SKILL.md
```

## Adding a skill

1. `mkdir <skill-name>`, add `<skill-name>/SKILL.md` with frontmatter (`name`, `description`).
2. Add a row to the table above.
3. Commit.
