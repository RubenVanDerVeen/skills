# AI Workflow

How Ruben works with AI coding agents: the harnesses, the skill stack, the plugins and hooks around them, and the flow a task follows from idea to commit. Snapshot date: 2026-07-04.

## Harnesses

Two harnesses share one skill catalog through the [agents.md](https://agents.md) convention:

| Harness | Role | Config |
|---|---|---|
| Claude Code | Primary daily driver | Model `claude-fable-5[1m]`, effort `xhigh`, plugins + hooks in `~/.claude/settings.json` |
| opencode | Secondary harness, same skills | `~/.config/opencode/` + `~/.opencode/opencode.json`, install steps in `opencode-install.md` |

Personal skills live in this repo (`C:\Users\ruben\projects\tools\skills`) and are synced to `~/.claude/skills/`. opencode picks them up from that same directory; the `~/.config/opencode/skills/` folder only holds `graphify` (no separate copy of the personal skills is maintained there). Slash commands do sync per harness: `~/.claude/commands/` (Claude Code) and `~/.config/opencode/command/` singular (opencode).

## Skill stack

Four layers, from personal to generic.

### 1. Personal skills (this repo)

| Skill | Covers |
|---|---|
| `altium-pro` | Altium Designer: PCB rooms, polygon pours, design rules, troubleshooting log |
| `drawio-pro` | Personal draw.io style: pastel grouped containers, BPMN flowcharts, legend boxes |
| `typst-pro` | Typst documents: NHL Stenden reports, IEEE templates, Dutch project layout |
| `synctool-sync` | NAS sync jobs via the `synctool` CLI, dry-run first |
| `project-standardization` | Bootstraps any repo for AI agents: AGENTS.md, `docs/artifacts/`, standards stack. Commands: `/standardize`, `/standardize-migrate` |
| `multi-plan-orchestration` | Splits oversized tasks into foundation + N parallel sub-plans. Command: `/multi-plan` |
| `commands/goal.md` | Orphan `/goal` command: iterate a build loop until a verifier passes |

### 2. Process discipline: superpowers (plugin, v5.1.0)

The gatekeeper layer. `using-superpowers` loads at session start and forces a skill check before any action. The skills used most:

- `brainstorming` before any creative work (features, components, new skills)
- `writing-plans` and `executing-plans` for multi-step work
- `test-driven-development` and `systematic-debugging` during implementation
- `requesting-code-review`, `receiving-code-review`, `verification-before-completion` before claiming done
- `writing-skills` when authoring skills for this repo
- `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees` for parallel or isolated work

### 3. Output style

- **caveman** (plugin, Claude Code only): terse chat register, roughly 75% fewer output tokens. Forced to ULTRA via SessionStart and UserPromptSubmit hooks in `~/.claude/settings.json`. Also ships `/caveman-commit` and `/caveman-review`. Chat only; code, commits, and docs stay normal. Not installed on opencode.
- **stop-slop** (skill): strips AI tells from prose (banned phrases, structural cliches, no em-dashes). Loaded whenever drafting or editing text. Reinforces the repo-wide no-em-dash rule.
- **ponytail** (opencode only): YAGNI-first "lazy senior dev" mode plus over-engineering review/audit skills. Governs what gets built; caveman governs how the agent talks.

### 4. Domain packs and utilities

- **vercel-labs/agent-skills**: `vercel-react-best-practices`, `vercel-composition-patterns`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`
- **find-skills**: discovers and installs new skills on demand
- **markitdown** (CLI): converts PDF/Office/EPUB/images/audio to Markdown so the agent can read them
- **graphify** (CLI): builds a queryable knowledge graph per repo (`graphify-out/`). Economics: a ~1-2K-token `graphify query` replaces a 10-40K-token grep/read exploration whose residue gets re-billed on every later prompt; phrase queries with concrete filenames/symbols, since abstract questions anchor on doc headings instead of code. Harness-agnostic via a "Knowledge graph" section in each graphed repo's AGENTS.md (wired by `/standardize` step 10 at medium/large tiers). Freshness needs no LLM: `graphify update .` is pure AST (~30 s), run by a debounced post-commit hook (`templates/post-commit-graphify` in the standardization skill) and as an end step of `/execute-plan`. opencode additionally has a `/graphify` skill + one-shot bash nudge plugin; Claude Code relies on the AGENTS.md section alone.
- **claude-mem**: cross-session memory. Currently disabled on opencode (plugin renamed to `claude-mem.js.bak`); Claude Code uses its native file-based memory instead.

## Plugins (Claude Code)

| Plugin | Scope | Purpose |
|---|---|---|
| `superpowers@claude-plugins-official` | user | Process-discipline skills |
| `caveman@caveman` | user | Terse output mode + commit/review commands |
| `rust-analyzer-lsp@claude-plugins-official` | user | Rust LSP support |
| `frontend-design`, `github`, `commit-commands` | project (homelab repo only) | Frontend design, GitHub, and commit helpers |

## Hooks

Claude Code only, all in `~/.claude/settings.json`. opencode has no hooks configured (plugins handle everything; `~/.config/opencode/hooks/` is empty).

- **Caveman**: SessionStart + UserPromptSubmit inject the ULTRA style contract.
- **Terax notify**: terminal escape sequences signal working/attention/finished states to the Terax terminal.

## Subagents

Claude Code only. opencode has no subagents configured (`~/.config/opencode/agents/` is empty).

`code-reviewer` (personal review style), `inventree` (parts inventory, pre-loaded category map), `plane` (project management, pre-loaded workspace context), `scrum-master`.

## MCP

Claude Code only. None of these are registered in the opencode configs (`~/.opencode/opencode.json` and `~/.config/opencode/opencode.jsonc` list only graphify, ponytail, and superpowers).

- **homelab** (stdio, Python): self-hosted services on the home server. Tools for InvenTree (inventory), Plane (project management), and Nextcloud. The `inventree` and `plane` agents wrap these tools with pre-loaded context.
- **claude.ai connectors**: Gmail, Google Calendar, Google Drive.

## Flow

Which path a task takes depends on size.

### Small task (bugfix, doc edit, one-file change)

1. Ask in chat; caveman keeps the exchange short.
2. Relevant skills auto-trigger on their frontmatter descriptions (`using-superpowers` enforces the check).
3. Bugs go through `systematic-debugging`; features through `brainstorming`, then TDD.
4. `verification-before-completion` before any "done" claim. Commits wait for explicit instruction, Conventional Commits format.

### Medium feature (one plan)

1. `brainstorming` produces a design doc in `docs/artifacts/specs/<topic>/YYYY-MM-DD-<topic>-design.md`.
2. `writing-plans` turns it into `docs/artifacts/plans/<topic>/YYYY-MM-DD-<topic>-plan.md`.
3. Execution via `executing-plans` or `subagent-driven-development`, often in a git worktree.
4. Once spec and plan are approved, the agent commits on its own at plan-defined boundaries (the one carve-out from the no-unprompted-commit rule).
5. Code review skills close the loop before merge.

### Large feature (multiple modules)

`/multi-plan` decomposes the work into a foundation plan plus N independent sub-plans with per-agent dispatch prompts, then parallel agents execute them.

### New repo

`/standardize` bootstraps AGENTS.md + CLAUDE.md shim, `docs/artifacts/`, and the standards stack (Conventional Commits, Keep a Changelog, ISO 8601 dates, kebab-case paths) at one of three size tiers. At medium/large tiers it also wires the graphify knowledge graph: gitignored `graphify-out/`, initial `graphify update .` build, debounced post-commit refresh hook, and the query-before-grep section in AGENTS.md.

## House conventions

- AGENTS.md is the single source of project context; CLAUDE.md is a one-line shim pointing at it.
- Specs, plans, and reviews from any framework land in `docs/artifacts/`.
- No em-dashes anywhere: repo files or chat.
- Skill descriptions are a public interface; changing one breaks description-match loading.
- New skills update every catalog (README.md, AGENTS.md) in the same commit.

## Related

- `AGENTS.md`: repo conventions and skill-authoring rules
- `external-skills.md`: full catalog of external sources with triggers
- `opencode-install.md`: install order for the opencode side
