# skills

Personal agent environment for AI coding agents that follow the [agents.md](https://agents.md) convention (opencode, Claude Code, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.): skills, slash commands, and opencode agent definitions in one repo.

Skills live under `skills/` as `<name>/SKILL.md`, slash commands under `commands/`, agent definitions under `agents/`. The top level holds repo-level docs (this README and the install guide).

## Skills

| Skill | What it does |
|---|---|
| [`drawio-pro`](./skills/drawio-pro/SKILL.md) | Personal draw.io style. Pastel grouped containers, BPMN flowcharts, light-grey legend boxes. |
| [`typst-pro`](./skills/typst-pro/SKILL.md) | Typst helpers. Academic frontpage, IEEE templates, Dutch project layout, color tokens. |
| [`altium-pro`](./skills/altium-pro/SKILL.md) | Altium Designer knowledge base. PCB rooms, polygon pours, design rules, query snippets, troubleshooting log. |
| [`deep-research`](./skills/deep-research/SKILL.md) | End-to-end research pipeline: intake, parallel gather (arxiv + web + own vault), synthesized dossier with citations, then brainstorm or Typst draft. Hermes research profile. |
| [`rubens-project-standardization`](./skills/rubens-project-standardization/SKILL.md) | Universal project bootstrap. `AGENTS.md` convention, kebab-case paths, ISO 8601 dates, Conventional Commits, Keep a Changelog. Three tiers (small/medium/large). |
| [`synctool-sync`](./skills/synctool-sync/SKILL.md) | Drive the `synctool` CLI to run saved NAS sync jobs (push/pull, copy/update). Dry-run first, hard rails, never auto-runs destructive mirror. |
| [`multi-plan-orchestration`](./skills/multi-plan-orchestration/SKILL.md) | Coordinator skill for too-large tasks: splits a brainstorm into foundation + N parallel sub-plans. Decomposition outline, scope-slip handling, manifest with per-agent dispatch prompts. Delegates to `brainstorming` + `writing-plans`. Slash command: `/multi-plan`. |
| [`skill-harvest`](./skills/skill-harvest/SKILL.md) | Mines recent opencode sessions for repeated corrections and skill gaps; report, approve, apply. Slash command: `/harvest`. |

## Agents

Custom opencode agents for the plan/execute/review split: `orchestrator` (`mode: all`, denies edit/write/patch), `executor` (implements one task), `reviewer` (read-only review), `inventree` (InvenTree inventory sessions via the homelab MCP). Per-agent skill denylists cut startup context ~2-4k tokens per session. Source of truth in [`agents/`](./agents/README.md); copy to `~/.config/opencode/agents/` to activate.

## External skills

Beyond the personal skills in this repo, several external sources are installed in the same environment. See [`external-skills.md`](./external-skills.md) for what each does and when to reach for it; install commands live in [`opencode-install.md`](./opencode-install.md).

- **superpowers** - process discipline skills (TDD, debugging, brainstorming, ...)
- **caveman** - terse, low-token output style
- **graphify** - codebase knowledge graph builder
- **vercel-labs/agent-skills** - React / Next.js / React Native / web-design pack
- **stop-slop** - removes AI writing patterns from prose

## Install

See [`opencode-install.md`](./opencode-install.md) for the full 8-step bootstrap.

Quick version:

```
# 1. Superpowers - fetch and follow:
https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md

# 2. Caveman
npx -y github:JuliusBrussee/caveman -- --only opencode

# 3. Copy the skill folders under skills/ to the agent's skills dir
```


## Layout

```
skills/
├── README.md                                    <- you are here
├── opencode-install.md                          <- install / bootstrap
├── external-skills.md                           <- external skill catalog
├── commands/                                    <- all slash commands live here
│   ├── goal.md                                  <- /goal: iterate until verifier passes
│   ├── execute-plan.md                          <- /execute-plan: subagent-driven plan execution
│   ├── full-cycle.md                          <- /full-cycle: single-pass brainstorm > spec > plan > dispatch orchestrator (or handoff)
│   ├── iterate-skill.md                         <- /iterate-skill: refine a skill via subagent review loops
│   ├── harvest.md                               <- /harvest: mine sessions for skill improvements
│   ├── multi-plan.md                            <- /multi-plan: start multi-plan orchestration
│   ├── standardize.md                           <- /standardize: bootstrap or restructure a project
│   └── standardize-migrate.md                   <- /standardize-migrate: migrate an older layout
├── agents/                                      <- opencode agent definitions (orchestrator, executor, reviewer)
└── skills/                                      <- all skill folders live here
    ├── drawio-pro/SKILL.md
    ├── typst-pro/SKILL.md
    ├── altium-pro/SKILL.md
    ├── deep-research/
    │   ├── SKILL.md
    │   ├── references/
    │   ├── scripts/
    │   └── templates/
    ├── rubens-project-standardization/SKILL.md
    ├── synctool-sync/SKILL.md
    ├── multi-plan-orchestration/SKILL.md
    └── skill-harvest/
        ├── SKILL.md
        └── references/extraction.md
```

## Adding a skill

See `AGENTS.md` for the full rule, in the section "Adding or modifying a skill" (catalogs, frontmatter checks, red flags). Short version:

1. `mkdir skills/<skill-name>`, add `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`).
2. (Optional) Add a command file to the top-level `commands/` directory and a `## Commands` section to the `SKILL.md`. See AGENTS.md "Slash commands" section for format and sync.
3. Add a row to the table above and to the matching `## Current skills` table in `AGENTS.md`. Update the Layout block if you added a command.
4. Commit.
