# skills

Personal opencode / Claude Code skills by Ruben.

Skills live in folders as `SKILL.md`. The top level holds repo-level docs (this README and the install guide).

## Skills

| Skill | What it does |
|---|---|
| [`drawio-pro`](./drawio-pro/SKILL.md) | Personal draw.io style — pastel grouped containers, BPMN flowcharts, light-grey legend boxes. |
| [`typst-pro`](./typst-pro/SKILL.md) | Typst helpers — academic frontpage, IEEE templates, Dutch project layout, color tokens. |
| [`rubens-project-standardization`](./rubens-project-standardization/SKILL.md) | Bootstraps a Claude Code project — `CLAUDE.md`, `claude/` scaffold, ISO/IEC/IEEE + Conventional Commits + Keep a Changelog stack. |

## Install

See [`opencode-install.md`](./opencode-install.md) for the full bootstrap (superpowers + caveman + this repo).

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
├── drawio-pro/SKILL.md
├── typst-pro/SKILL.md
└── rubens-project-standardization/SKILL.md
```

## Adding a skill

1. `mkdir <skill-name>`, add `<skill-name>/SKILL.md` with frontmatter (`name`, `description`).
2. Add a row to the table above.
3. Commit.
