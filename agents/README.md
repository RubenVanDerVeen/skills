# agents: opencode agent definitions

Source of truth for the custom opencode agents. Like `commands/`, this directory is inactive inside the repo; copy each `.md` file to `~/.config/opencode/agents/` (global) or `.opencode/agents/` (per-project) to activate, then restart opencode (config loads once at startup). opencode-only: Claude Code subagents use a different frontmatter format, do not copy these to `~/.claude/agents/`.

## The set

| Agent | Mode | Role | Denied |
|---|---|---|---|
| `orchestrator` | primary | Plans, dispatches executor/reviewer per task, reviews results, commits at boundaries via bash. | edit/write/patch tools; implementation-domain skills |
| `executor` | subagent | Implements exactly one plan task: TDD, edit, verify, report. Keeps ponytail suite and `using-git-worktrees`. | task/webfetch tools; planning skills |
| `reviewer` | subagent | Spec-compliance and code-quality review of one task. Read-only plus bash for running tests. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |

`/execute-plan` (see `commands/execute-plan.md`) dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, the command itself runs as `orchestrator`. It falls back to the general subagent when a named one is missing, so the command stays portable to harnesses without these agents.

## Why: tokens and discipline

Skill descriptions, not tool schemas, dominate opencode startup context (~5k of ~17k with 37 skills registered). Per-agent `permission: skill: { "<name>": deny }` removes denied skills from the listing the model sees. Tool-schema removal (edit/write/patch) is only ~80 tokens per tool. The edit/write deny on the orchestrator also enforces the subagent-driven-development rule "the orchestrator never implements" mechanically instead of by prose.

Measured 2026-07-05 (opencode 1.17.13, MiniMax-M3, this repo, input + cache-read):

| Session | Tokens |
|---|---|
| build (baseline) | 16,814 |
| orchestrator | 14,846 |
| executor via task dispatch | ~13,800 |
| everything denied (floor) | 11,763 |

## Maintenance notes

- Denylist over allowlist: new skills surface in every agent by default; add a deny where a skill does not belong.
- `tools:` is deprecated in the schema but still strips tool schemas from context; keep both `tools:` and the matching `permission:` entries.
- `color:` accepts hex (`#rrggbb`) or theme tokens (`primary|secondary|accent|success|warning|error|info`) only.
- Quirk: running a `mode: subagent` agent standalone (`opencode run --agent executor`) skips its skill filtering; the task-dispatch path applies it. Do not benchmark subagents standalone.
- An empty body keeps opencode's default system prompt. A non-empty body replaces it entirely; only add one deliberately.
- Validate after editing: `opencode agent list` (parses), `opencode debug agent <name>` (resolved config).
