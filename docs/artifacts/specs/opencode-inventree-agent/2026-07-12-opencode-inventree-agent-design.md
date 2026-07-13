# opencode InvenTree agent: port of the Claude Code inventree subagent

Date: 2026-07-12
Status: approved (design approved in session)

## Goal

One opencode primary agent, `inventree`, for inventory work against the homelab InvenTree instance: AliExpress order CSV import, part/stock/purchase-order management, and renaming parts to the naming convention. Straight port of the proven Claude Code agent at `~/.claude/agents/inventree.md`; no behaviour redesign.

## Context (current state, 2026-07-12)

- Claude Code agent exists: `~/.claude/agents/inventree.md` (~140 lines). Contains the supplier table (AliExpress pk=1), the full category map (38 categories with pks), the naming convention with per-category name formats, standard workflows (AliExpress CSV import, PO creation, pack quantities, renaming), and behaviour rules. Proven in use; it is the single source for the body content.
- Homelab MCP server: stdio Python server at `C:\Users\ruben\projects\hobby\homelab\mcp\server.py`, launched with `C:\Users\ruben\projects\hobby\homelab\mcp\.venv\Scripts\python.exe`. Env vars (values live in `~/.claude.json` under `mcpServers.homelab`): `PLANE_API_KEY`, `PLANE_BASE_URL`, `PLANE_WORKSPACE_SLUG`, `INVENTREE_BASE_URL`, plus any other keys present there. The server exposes ~25 `inventree_*` tools and ~18 `plane_*` tools.
- opencode global config `~/.config/opencode/opencode.json` has no `mcp` block today; the homelab server is not available to opencode at all.
- Existing roster in `agents/`: planner, orchestrator, writer, executor, reviewer, oracle (see `agents/README.md`). Convention: denylist over allowlist; per-agent skill denies keep startup context lean.
- InvenTree instance: `http://192.168.178.208:8000`.

## Design

### 1. Agent file: `agents/inventree.md`

Frontmatter, following `agents/executor.md` style:

- `description`: reuse the Claude Code agent description verbatim.
- `mode: primary` (user-driven sessions: "import this CSV", "rename these parts").
- `color: info`
- `model: minimax-coding-plan/MiniMax-M3` (tool-calling-heavy workload, flat quota; see Risks for the swap condition).
- `tools`: `write: false`, `edit: false`, `patch: false`, `task: false`, `webfetch: false`, `"homelab_plane*": false` (no file writes, no subagents, no web, no Plane tool schemas in its sessions).
- `permission`: denies matching the tools map, plus skill denylist: the executor's deny set (brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, multi-plan-orchestration, finishing-a-development-branch, requesting-code-review, skill-harvest, find-skills, deep-research, project-standardization) plus `typst-pro`, `drawio-pro`, `altium-pro` (doc/EDA domain, irrelevant to inventory CRUD).

Body: near-verbatim copy of the Claude Code agent body (suppliers, category map, naming convention with format table and examples, standard workflows, behaviour rules). One mechanical adjustment: tool references in prose change from Claude naming (`inventree_list_parts`) to the opencode-resolved names (`homelab_inventree_list_parts`), so the model calls what it reads.

### 2. MCP config (machine-local, never in repo)

Add to `~/.config/opencode/opencode.json`:

```json
"mcp": {
  "homelab": {
    "type": "local",
    "command": [
      "C:\\Users\\ruben\\projects\\hobby\\homelab\\mcp\\.venv\\Scripts\\python.exe",
      "C:\\Users\\ruben\\projects\\hobby\\homelab\\mcp\\server.py"
    ],
    "environment": { "<mirror all keys/values from ~/.claude.json mcpServers.homelab.env>": "" }
  }
}
```

API keys stay in machine-local config only. The repo never contains secrets; `agents/README.md` documents the required block with placeholder values.

### 3. Token hygiene: the other six agents

Blanket deny in each existing agent file (planner, orchestrator, writer, executor, reviewer, oracle): add `"homelab*": false` to `tools:`. Keeps all ~43 MCP tool schemas out of every non-inventree session. Without this, adding the MCP block globally would grow every session's startup context.

### 4. Catalog updates (same commit as the agent file)

- `agents/README.md`: roster table row, sync instructions, note that the agent requires the machine-local `mcp.homelab` block (with placeholder example).
- `AGENTS.md`: agent roster mentions (file layout comment and the Agent definitions section).
- `README.md`: roster mention.
- `CHANGELOG.md`: entry under Unreleased or dated release per Keep a Changelog.

### 5. Sync and verification

1. Copy `agents/inventree.md` to `~/.config/opencode/agents/`; add the `mcp` block to `~/.config/opencode/opencode.json`; restart opencode (config loads at startup).
2. `opencode agent list` parses; `opencode debug agent inventree` shows resolved config: `homelab_inventree_*` tools present, `homelab_plane*` absent.
3. `opencode debug agent build` (or any other agent): all `homelab*` tools absent.
4. Live smoke test: inventree agent session, "list the categories" returns the known category map; then one real AliExpress CSV import end to end (parts created or stock added, supplier parts linked, summary reported).
5. Optional: re-measure startup tokens per the `agents/README.md` maintenance note.

## Out of scope

- Datasheet fetching/attachment workflow: separate spec (#2 in the session's decomposition); needs a new MCP attachment-upload tool first.
- Plane agent port for opencode.
- Any change to the Claude Code agent; it stays as-is. Divergence between the two copies is accepted for now; whoever edits one updates the other by hand.

## Risks / notes

- Wildcard keys in the `tools:` map (`homelab*`, `homelab_plane*`): verify they resolve via `opencode debug agent inventree`. Fallback if unsupported: enumerate the tool names explicitly (mechanical, longer file).
- The `mode: subagent` standalone-run quirk in `agents/README.md` does not apply: this agent is `mode: primary`.
- MCP paths use lowercase `projects\hobby\homelab` exactly as in `~/.claude.json`; Windows is case-insensitive, keep verbatim.
- Model pin: naming-convention judgement is light reasoning, M3 should hold. If part names or descriptions degrade versus the Claude agent's output, swap the pin to `zai-coding-plan/glm-5.2` (one line).
