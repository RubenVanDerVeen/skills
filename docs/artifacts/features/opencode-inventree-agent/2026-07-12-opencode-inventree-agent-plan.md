# opencode InvenTree Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the Claude Code `inventree` agent to opencode: agent file in this repo, homelab MCP wired into opencode, MCP schemas kept out of every other agent.

**Architecture:** One new `mode: primary` opencode agent (`agents/inventree.md`) whose body is copied from the proven Claude Code agent. The homelab MCP server (stdio Python) gets registered machine-locally in `~/.config/opencode/opencode.json`; the six existing agents blanket-deny `homelab*` tools so only inventree sessions pay the schema cost.

**Tech Stack:** opencode agent markdown (frontmatter + body), opencode JSON config, no code.

**Spec:** `docs/artifacts/specs/opencode-inventree-agent/2026-07-12-opencode-inventree-agent-design.md`

## Global Constraints

- No em-dashes (U+2014) in any repo file. Replace with comma, colon, or hyphen.
- Conventional Commits 1.0.0. Repo: `C:\Users\ruben\projects\Tools\skills` (branch `main`).
- No secrets in repo files. API keys exist only in `~/.claude.json` and `~/.config/opencode/opencode.json`.
- opencode loads config at startup: after machine-local changes, restart opencode before validating.
- Keep both `tools:` and matching `permission:` entries for denied built-in tools (repo convention, `agents/README.md`).

---

### Task 1: Create `agents/inventree.md`

**Files:**
- Create: `agents/inventree.md`
- Source (read-only): `C:\Users\ruben\.claude\agents\inventree.md` (body lines 7-145)

**Interfaces:**
- Produces: agent name `inventree` (primary). Tool names later tasks rely on: `homelab_inventree_*` (e.g. `homelab_inventree_list_parts`).

- [ ] **Step 1: Write the frontmatter** (exact content):

```markdown
---
description: Purpose-built agent for managing the InvenTree parts inventory. Use this agent for: importing AliExpress order CSVs, creating parts/categories/locations, updating stock, managing purchase orders, linking supplier parts, and renaming/redescribing parts to match the naming convention. This agent starts pre-loaded with the full category map, supplier IDs, and naming convention, no re-derivation needed.
mode: primary
color: info
model: minimax-coding-plan/MiniMax-M3
tools:
  write: false
  edit: false
  patch: false
  task: false
  webfetch: false
  "homelab_plane*": false
permission:
  write: deny
  edit: deny
  patch: deny
  task: deny
  webfetch: deny
  skill:
    "*": allow
    "brainstorming": deny
    "writing-plans": deny
    "executing-plans": deny
    "subagent-driven-development": deny
    "dispatching-parallel-agents": deny
    "multi-plan-orchestration": deny
    "finishing-a-development-branch": deny
    "requesting-code-review": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
---
```

- [ ] **Step 2: Copy the body** from `C:\Users\ruben\.claude\agents\inventree.md` lines 7-145 (everything after its frontmatter) below the new frontmatter, then apply exactly these transforms:
  1. Tool-name prefix: every `inventree_...` tool reference in prose becomes `homelab_inventree_...`. Occurrences: `inventree_list_parts`, `inventree_create_purchase_order`, `inventree_list_supplier_parts(part_id)`, `inventree_add_po_line`. Bash check afterwards: `grep -n '`inventree_' agents/inventree.md` returns nothing.
  2. Em-dash removal: replace every U+2014 with a comma or colon that reads naturally. The source body contains several; e.g. source line 7 becomes "...naming convention: use this context directly...". Find them with `grep -nP '\x{2014}'` on the copied body.
  3. Keep the `×` (U+00D7) and `⌀` characters untouched; they are part of the naming convention.

- [ ] **Step 3: Verify**

Run: `grep -cP '\x{2014}' agents/inventree.md` -> Expected: `0` (exit 1)
Run: `grep -c 'homelab_inventree_' agents/inventree.md` -> Expected: `>= 4`
Run: `grep -n 'mode: primary' agents/inventree.md` -> Expected: 1 hit in frontmatter

- [ ] **Step 4: Commit**

```bash
git add agents/inventree.md
git commit -m "feat(agents): add inventree opencode agent (port of Claude Code subagent)"
```

---

### Task 2: Deny `homelab*` tools in the six existing agents

**Files:**
- Modify: `agents/planner.md`, `agents/orchestrator.md`, `agents/writer.md`, `agents/executor.md`, `agents/reviewer.md`, `agents/oracle.md`

**Interfaces:**
- Consumes: nothing from Task 1 (independent edit, same repo).
- Produces: every non-inventree agent session has zero `homelab*` tool schemas.

- [ ] **Step 1: Add the deny line** to the `tools:` block of each of the six files. If a file has no `tools:` block, add one under `model:`. The line (identical in all six):

```yaml
tools:
  "homelab*": false
```

(When a `tools:` block already exists, append only the `"homelab*": false` line to it. `permission:` needs no matching entry: MCP tool gating goes through the `tools:` map.)

- [ ] **Step 2: Verify**

Run: `grep -l '"homelab\*": false' agents/*.md | wc -l` -> Expected: `6` (all except `inventree.md`, which must keep only `"homelab_plane*": false`)

- [ ] **Step 3: Commit**

```bash
git add agents/planner.md agents/orchestrator.md agents/writer.md agents/executor.md agents/reviewer.md agents/oracle.md
git commit -m "refactor(agents): keep homelab MCP schemas out of non-inventree agents"
```

---

### Task 3: Machine-local activation (MCP config + sync)

**Files:**
- Modify (machine-local, NOT committed): `~/.config/opencode/opencode.json`
- Copy: `agents/*.md` -> `~/.config/opencode/agents/`

**Interfaces:**
- Consumes: agent files from Tasks 1-2.
- Produces: working `opencode` with `inventree` agent and homelab MCP.

- [ ] **Step 1: Merge the MCP block** (mirrors command/env from `~/.claude.json`, no secrets typed by hand):

```bash
python - <<'EOF'
import json, os
cc = json.load(open(os.path.expanduser("~/.claude.json")))
h = cc["mcpServers"]["homelab"]
p = os.path.expanduser("~/.config/opencode/opencode.json")
oc = json.load(open(p))
oc.setdefault("mcp", {})["homelab"] = {
    "type": "local",
    "command": [h["command"], *h["args"]],
    "environment": h.get("env", {}),
    "enabled": True,
}
json.dump(oc, open(p, "w"), indent=2)
print("merged:", list(oc["mcp"]))
EOF
```

Expected output: `merged: ['homelab']`

- [ ] **Step 2: Sync agent files**

```bash
cp agents/inventree.md agents/planner.md agents/orchestrator.md agents/writer.md agents/executor.md agents/reviewer.md agents/oracle.md ~/.config/opencode/agents/
```

- [ ] **Step 3: Restart opencode, then validate** (config loads at startup; any running opencode must be restarted first):

```bash
opencode agent list
```
Expected: parses without error, `inventree` listed as primary.

```bash
opencode debug agent inventree | grep -c homelab_inventree
```
Expected: `>= 20` (all inventree tools resolved)

```bash
opencode debug agent inventree | grep -c homelab_plane
```
Expected: `0`

```bash
opencode debug agent planner | grep -c homelab
```
Expected: `0` (same spot-check on one more agent, e.g. `executor`)

If the wildcard keys do not resolve (tools still present), fallback per spec: replace the glob line with explicit `homelab_plane_<name>: false` / `homelab_<name>: false` lines enumerating the tool names from `opencode debug agent`, and re-verify.

No commit in this task (machine-local only).

---

### Task 4: Catalog updates

**Files:**
- Modify: `agents/README.md`, `AGENTS.md`, `README.md`, `CHANGELOG.md`

**Interfaces:**
- Consumes: agent name and behaviour from Task 1.

- [ ] **Step 1: `agents/README.md`**: add roster table row (find the table listing planner/orchestrator/...):

```markdown
| `inventree` | primary | `minimax-coding-plan/MiniMax-M3` | InvenTree inventory sessions: AliExpress CSV import, parts/stock/POs, naming convention. Needs the machine-local `mcp.homelab` block. | file writes; task/webfetch; `homelab_plane*` schemas; planning and doc-domain skills |
```

Below the table (or in Maintenance notes), add the MCP requirement with placeholder values:

```markdown
The `inventree` agent requires the homelab MCP server registered machine-locally in `~/.config/opencode/opencode.json` (keys mirrored from `~/.claude.json`, never committed):

    "mcp": { "homelab": { "type": "local", "command": ["<venv-python>", "<path>\\server.py"], "environment": { "INVENTREE_BASE_URL": "...", "INVENTREE_API_KEY": "<secret>" }, "enabled": true } }

All other agents deny `homelab*` in `tools:`; add that line to any future agent too.
```

- [ ] **Step 2: `AGENTS.md`**: update the two roster mentions (grep `planner, orchestrator` to find them): the file-layout comment line for `agents/` and the "Agent definitions" section sentence, adding `inventree` to the name list with a phrase like "and `inventree` (InvenTree inventory sessions via the homelab MCP)".

- [ ] **Step 3: `README.md`**: grep for the agent roster mention (`git log` shows it was added in "docs: catalog planner/writer/oracle roster across README...") and add `inventree` to the list the same way.

- [ ] **Step 4: `CHANGELOG.md`**: add under the Unreleased/newest section, matching the file's existing entry style:

```markdown
- feat(agents): `inventree` opencode agent, port of the Claude Code subagent; homelab MCP registered machine-locally, `homelab*` denied in all other agents
```

- [ ] **Step 5: Verify + commit**

Run: `grep -rn 'inventree' README.md AGENTS.md agents/README.md CHANGELOG.md | wc -l` -> Expected: `>= 5`
Run: `grep -rcP '\x{2014}' agents/README.md AGENTS.md README.md CHANGELOG.md` -> Expected: `0` per file

```bash
git add agents/README.md AGENTS.md README.md CHANGELOG.md
git commit -m "docs: catalog inventree agent across README, AGENTS.md, agents/README, CHANGELOG"
```

---

### Task 5: Live smoke test

**Files:** none (runtime validation)

- [ ] **Step 1: Category smoke**

```bash
opencode run --agent inventree "List the part categories and stop."
```
Expected: output contains known categories (`Electronics/Passive Components/Resistors`, `Mechanical/Motors`, `Tools/Soldering & Rework`).

- [ ] **Step 2: CSV import smoke (user-assisted, optional now)**: if a recent AliExpress export CSV exists (check `~/Downloads/*.csv`), run one real import in an inventree session and confirm the final summary (parts created/stock added/supplier parts linked). If no CSV is at hand, record this step as Deferred in the final report; the first real import covers it.

- [ ] **Step 3: Report**: tasks done, commits with hashes, validation outputs, anything Deferred/Unverified.
