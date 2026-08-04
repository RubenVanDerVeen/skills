# agents: opencode agent definitions

Source of truth for the custom opencode agents. Like `commands/`, this directory is inactive inside the repo; copy each `.md` file to `~/.config/opencode/agents/` (global) or `.opencode/agents/` (per-project) to activate, then restart opencode (config loads once at startup). opencode-only: Claude Code subagents use a different frontmatter format, do not copy these to `~/.claude/agents/`.

## The set

| Agent | Mode | Model | Role | Denied |
|---|---|---|---|---|
| `planner` | primary | `zai-coding-plan/glm-5.2` | Brainstorm > spec > plan. Dispatches the `orchestrator` subagent in single-pass mode by default (commits at task boundaries), or prints the `/execute-plan` handoff block when `handoff` is requested. Dispatches `explore` for recon. | file writes outside `docs/**` (glob deny); execution-process skills |
| `orchestrator` | all | `minimax-coding-plan/MiniMax-M3` (`thinking` variant) | Executes approved plans: dispatches executor/reviewer per task, oracle on two-strike failures, commits at boundaries via bash. Session agent for standalone /execute-plan and dispatchable by the planner for single-pass /full-cycle. | edit/write/patch tools; implementation-domain skills |
| `writer` | primary | unpinned (session model) | Focused doc/Typst sessions: direct edits, compile-verify, no ceremony. | plan/execution suite and code-domain skills |
| `inventree` | primary | `minimax-coding-plan/MiniMax-M3` | InvenTree inventory sessions: AliExpress CSV import, parts/stock/POs, naming convention, datasheet fetch/attach. Needs the machine-local `mcp.homelab` block. | file writes; task/webfetch; `homelab_plane*` schemas; planning and doc-domain skills |
| `executor` | subagent | `minimax-coding-plan/MiniMax-M3` | Implements exactly one plan task: TDD, edit, verify, report. Keeps ponytail suite and `using-git-worktrees`. | task/webfetch tools; planning skills |
| `reviewer` | subagent | `zai-coding-plan/glm-5.2` | Spec-compliance and code-quality review of one task. Cross-model on purpose: a different family reviewing M3 diffs does not share the executor's blind spots. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |
| `oracle` | subagent | `zai-coding-plan/glm-5.2` | Read-only consult after two failed attempts: ranked hypotheses, one recommendation. Keeps bash + webfetch. | edit/write/patch/task tools; planning and review-workflow skills |
| `standardizer` | subagent | `zai-coding-plan/glm-5.2` | Repo-wide standardization audit after a plan's task loop: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows; plus code structure via `code-standardization` (formatter/linter presence, naming/module organization, architecture boundaries). Returns findings tagged quick-fix or recommendation. Read-only. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |
| `documenter` | subagent | `zai-coding-plan/glm-5.2` | Closes out a completed plan: writes the execution report to `docs/artifacts/reports/`, updates every catalog/doc touched (README, AGENTS, commands sections), commits as docs. Write-scoped to docs/** + root markdown. | task/webfetch tools; planning and review-workflow skills; writes outside docs/** + root markdown |

`/full-cycle` runs as `planner`. `/execute-plan` (see `commands/execute-plan.md`) dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, two-strike failures to `oracle`, post-implementation structure review to `standardizer`, and the documentation/report phase to `documenter`; the command itself runs as `orchestrator`. It falls back to the general subagent when a named one is missing, so the command stays portable to harnesses without these agents. The built-in `explore` subagent handles codebase recon for planner and orchestrator; no custom file needed. Single-pass `/full-cycle`: the planner dispatches the `orchestrator` as a subagent (mode `all`) instead of stopping at a handoff; this requires `subagent_depth >= 2` in opencode config so the orchestrator can dispatch executor/reviewer.

Model routing: GLM 5.2 carries planning, review, and consult (long-horizon reasoning); MiniMax M3 carries orchestration and implementation (near-par execution, faster and cheaper). Both are flat-quota coding plans, so crossmodel dispatch has no marginal token cost.

## Why: tokens and discipline

Skill descriptions, not tool schemas, dominate opencode startup context (~5k of ~17k with 37 skills registered). Per-agent `permission: skill: { "<name>": deny }` removes denied skills from the listing the model sees. Tool-schema removal (edit/write/patch) is only ~80 tokens per tool. The edit/write deny on the orchestrator is a guardrail, not a forcing function: bash can still write files (`Set-Content`, redirection, `git apply`), so a pragmatic model can bypass it. Real enforcement is the body's dispatch-first mandate plus the Dispatch Log that makes any self-implementation visible in the final report. Verified the hard way 2026-08-02: MiniMax-M3 ran two full plans with zero executor dispatches and produced green reports; the bypass was caught only by a later DB audit.

Measured 2026-07-05 (opencode 1.17.13, MiniMax-M3, this repo, input + cache-read):

| Session | Tokens |
|---|---|
| build (baseline) | 16,814 |
| orchestrator | 14,846 |
| executor via task dispatch | ~13,800 |
| everything denied (floor) | 11,763 |

Measurements predate the 2026-07-12 roster change (planner/writer/oracle, model pins); re-measure before quoting.

## Maintenance notes

- Denylist over allowlist: new skills surface in every agent by default; add a deny where a skill does not belong.
- `variant: thinking` is pinned on the orchestrator (not just inherited) so single-pass `/full-cycle` subagent dispatch matches the standalone `/execute-plan` model. Without an explicit `variant`, opencode uses the `default` variant when the orchestrator is dispatched as a subagent, even though standalone runs pick up `thinking` from the session default. Verified against session history (2026-07-31): standalone orchestrator ran `thinking`, planner-dispatched ran `default`.
- `tools:` is deprecated in the schema but still strips tool schemas from context; keep both `tools:` and the matching `permission:` entries.
- Permission rule order matters: opencode uses last-match-wins inside a patterned permission object, so put the broad rule (`"*"`) FIRST and narrow allows LAST. A trailing `"*": deny` matched the tool-capability probe and silently disabled the tool entirely (the orchestrator's `task:` block had `"*": deny` last and lost dispatch until reordered).
- `color:` accepts hex (`#rrggbb`) or theme tokens (`primary|secondary|accent|success|warning|error|info`) only.
- Quirk: running a `mode: subagent` agent standalone (`opencode run --agent executor`) skips its skill filtering; the task-dispatch path applies it. Do not benchmark subagents standalone.
- An empty body keeps opencode's default system prompt. A non-empty body replaces it entirely; only add one deliberately.
- Validate after editing: `opencode agent list` (parses), `opencode debug agent <name>` (resolved config).

The `inventree` agent requires the homelab MCP server registered machine-locally in `~/.config/opencode/opencode.json` (secrets entered directly, never committed):

    "mcp": { "homelab": { "type": "local", "command": ["<venv-python>", "<path>\\server.py"], "environment": { "INVENTREE_BASE_URL": "...", "INVENTREE_API_KEY": "<secret>" }, "enabled": true } }

All other agents deny `homelab*` in `tools:`; add that line to any future agent too.
