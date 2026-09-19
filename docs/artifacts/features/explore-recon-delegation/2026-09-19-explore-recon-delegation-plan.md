# Explore Recon Delegation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a custom `agents/explore.md` subagent (shadows the opencode built-in) pinned to `zai-coding-plan/glm-5.3-flash` variant `high`, with read-only repo access plus webfetch, and hard-require the planner to delegate ALL exploration (file reading for recon, online lookup) to it.

**Architecture:** Naming the custom agent `explore` overrides opencode's built-in of the same name, so all existing dispatch sites (planner, orchestrator, writer, full-cycle command, restructure-flow) route to it with zero call-site edits and fall back to the built-in when the file is not synced. Enforcement on the planner is two-layered: a body rule (whole run, not just step 2) plus a `webfetch` deny in its frontmatter so direct fetching is impossible.

**Tech Stack:** Markdown only. opencode agent frontmatter (`mode`, `model`, `variant`, `tools`, `permission`). Validation via `opencode agent list` / `opencode debug agent` when the CLI is on PATH.

**Spec:** `docs/artifacts/features/explore-recon-delegation/2026-09-19-explore-recon-delegation-design.md`

**Versioning:** This repo's AGENTS.md declares no `### Versioning` subsection: unversioned, no bump. CHANGELOG.md still gets entries (repo keeps one).

## Global Constraints

- No em-dashes (U+2014) in any touched file. Verify with: `Get-ChildItem -Recurse -Include *.md -Path agents,commands | Select-String -Pattern ([char]0x2014)` plus the same for `README.md`, `AGENTS.md`, `CHANGELOG.md`. Must return empty.
- Every pinned agent also pins its variant explicitly (agents/README.md rule; dispatched subagents otherwise run the `default` variant).
- Keep BOTH `tools:` entries and matching `permission:` entries (`tools:` is deprecated but still strips tool schemas from context).
- `permission:` patterned objects are last-match-wins: broad `"*"` rule FIRST, narrow rules LAST. Never end a patterned block with `"*": deny`.
- `homelab*: false` in `tools:` is mandatory on every agent.
- Catalogs ship in the same commit as the agent they document: `agents/README.md` roster + routing paragraph, root `README.md`, root `AGENTS.md`.
- Branch: `plan-explore-recon`, created before Task 1.
- If `opencode` is not on PATH in the executing shell, substitute a careful line-by-line frontmatter review and note the substitution in the task report.

---

### Task 1: Create `agents/explore.md` and update all catalogs

**Files:**
- Create: `agents/explore.md`
- Modify: `agents/README.md` (roster table, built-in-explore paragraph, model-routing paragraph)
- Modify: `README.md` (root, agents paragraph)
- Modify: `AGENTS.md` (root, Agent definitions paragraph)
- Modify: `CHANGELOG.md` (Added entry)

**Interfaces:**
- Produces: agent named `explore` (mode `subagent`, model `zai-coding-plan/glm-5.3-flash`, variant `high`, webfetch allowed, edit/write/patch/task denied). Task 2 and all existing dispatch sites reference it by the name `explore`.

- [ ] **Step 1: Create the branch**

```powershell
git checkout -b plan-explore-recon
```

- [ ] **Step 2: Create `agents/explore.md` with exactly this content**

```markdown
---
description: Fast read-only codebase recon and online lookup subagent. Finds files, maps where changes land, answers architecture questions, verifies syntax and behavior against online docs via webfetch. Dispatch for any multi-file reading or web research instead of reading files in your own window. Returns structured findings with verbatim quotes.
mode: subagent
color: info
model: zai-coding-plan/glm-5.3-flash
variant: high
tools:
  write: false
  edit: false
  patch: false
  task: false
  "homelab*": false
permission:
  edit: deny
  write: deny
  patch: deny
  task: deny
  skill:
    "*": allow
    "brainstorming": deny
    "writing-plans": deny
    "executing-plans": deny
    "subagent-driven-development": deny
    "dispatching-parallel-agents": deny
    "multi-plan-orchestration": deny
    "finishing-a-development-branch": deny
    "using-git-worktrees": deny
    "requesting-code-review": deny
    "receiving-code-review": deny
    "test-driven-development": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
    "synctool-sync": deny
---

You are the read-only recon subagent. Other agents dispatch you so they never read files or fetch web pages themselves: codebase exploration (find files, map where changes land, answer how-does-X-work) and online lookup (docs, schemas, syntax verification). You never edit files and never dispatch subagents.

Method:

1. Scope first: restate the question and pick the depth. quick = one fact. medium = focused map of one area. very thorough = multi-round search across naming conventions and references.
2. Search before reading: glob/grep to narrow, then read only the files that answer the question. Batch independent tool calls in one round.
3. Read with intent: quote verbatim what matters (frontmatter blocks, key lines with file:line); summarize the rest. Never dump whole files unless asked.
4. Web lookup: when asked to verify something online, fetch the official docs or schema, quote the exact syntax or wording, and cite the URL.
5. Return structured findings: direct answers first, then evidence, then an explicit "not found" for anything the search did not surface. Flag contradictions between files.

You change nothing: no edits, no writes, no commits, no dispatches.
```

- [ ] **Step 3: `agents/README.md`, insert roster row**

Insert this row on the line immediately AFTER the table row that starts with `| \`planner\` |`:

```markdown
| `explore` | subagent | `zai-coding-plan/glm-5.3-flash` (`high` variant) | Read-only recon: codebase exploration (find files, map landing zones, explain code) plus online lookup via webfetch. Shadows the opencode built-in of the same name; existing dispatch sites route to it once synced, built-in remains the fallback. | edit/write/patch/task tools; planning and review-workflow skills |
```

- [ ] **Step 4: `agents/README.md`, rewrite the built-in paragraph**

Find (exact):

```markdown
The built-in `explore` subagent handles codebase recon for planner and orchestrator; no custom file needed.
```

Replace with:

```markdown
The custom `explore` subagent handles codebase recon and web lookup for planner and orchestrator. It shadows the opencode built-in of the same name: every existing dispatch site routes to the custom definition once synced, and falls back to the built-in on machines without the file.
```

- [ ] **Step 5: `agents/README.md`, routing paragraph**

Find (exact):

```markdown
`high` effort on the GLM agents (planner, reviewer, oracle, doc-standardizer, code-standardizer, documenter).
```

Replace with:

```markdown
`high` effort on the GLM agents (planner, reviewer, oracle, doc-standardizer, code-standardizer, documenter, explore).
```

- [ ] **Step 6: Root `README.md`, agent list**

Find (exact): `` `documenter`, `oracle` `` and replace with: `` `documenter`, `explore`, `oracle` ``. If the string matches more than once, expand surrounding context to the unique occurrence inside the "Custom opencode agents (" paragraph.

- [ ] **Step 7: Root `AGENTS.md`, agent list**

In the "### Agent definitions" section (or "## Agent definitions" heading variant), find (exact): `` `documenter`, `oracle` `` and replace with: `` `documenter`, `explore`, `oracle` ``. Same uniqueness rule as Step 6.

- [ ] **Step 8: `CHANGELOG.md`, Added entry**

Read `CHANGELOG.md` first, then add one entry in the repo's existing style, at the top of the most recent unreleased/Added section (create the section matching the file's Keep a Changelog conventions if absent):

```markdown
- Custom `explore` subagent pinned to `zai-coding-plan/glm-5.3-flash` (`high` variant): read-only codebase recon plus web lookup; shadows the opencode built-in of the same name.
```

- [ ] **Step 9: Verify**

Run (expect exit 0 and `explore` listed):

```powershell
opencode agent list
```

Run (expect model `zai-coding-plan/glm-5.3-flash`, variant `high`, mode `subagent`):

```powershell
opencode debug agent explore
```

Run (expect empty):

```powershell
Get-ChildItem -Recurse -Include *.md -Path agents,commands | Select-String -Pattern ([char]0x2014); Select-String -Path README.md,AGENTS.md,CHANGELOG.md -Pattern ([char]0x2014)
```

Run (expect `explore` present in all three catalogs):

```powershell
Select-String -Path README.md,AGENTS.md,agents/README.md -Pattern "explore"
```

- [ ] **Step 10: Commit**

```powershell
git add agents/explore.md agents/README.md README.md AGENTS.md CHANGELOG.md
git commit -m "feat(agents): add explore subagent pinned to glm-5.3-flash high"
```

### Task 2: Hard-require planner delegation to explore

**Files:**
- Modify: `agents/planner.md` (description, `tools:`, `permission:`, body)
- Modify: `commands/full-cycle.md` (step 1 wording)
- Modify: `CHANGELOG.md` (Changed entry)

**Interfaces:**
- Consumes: agent name `explore` from Task 1.
- Produces: planner frontmatter with `webfetch: false` / `webfetch: deny`; body carrying the exploration-discipline rule verbatim as given below.

- [ ] **Step 1: `agents/planner.md` description**

Find (exact):

```markdown
File writes limited to docs/; source code untouchable. Dispatches the explore subagent for codebase recon.
```

Replace with:

```markdown
File writes limited to docs/; source code untouchable. Delegates all recon (codebase reading and web lookup) to the explore subagent.
```

- [ ] **Step 2: `agents/planner.md` tools block**

Find (exact):

```yaml
tools:
  "homelab*": false
```

Replace with:

```yaml
tools:
  webfetch: false
  "homelab*": false
```

- [ ] **Step 3: `agents/planner.md` permission block**

Find (exact):

```yaml
  patch:
    "*": deny
    "docs/**": allow
  skill:
```

Replace with:

```yaml
  patch:
    "*": deny
    "docs/**": allow
  webfetch: deny
  skill:
```

- [ ] **Step 4: `agents/planner.md` body rule**

After the paragraph starting `Scope discipline: YAGNI in every design` (ends with `...load multi-plan-orchestration and split it.`), append a blank line, then this paragraph verbatim:

```markdown
Exploration discipline (whole run, not just step 2): every read of project files and every online lookup goes through the explore subagent. That includes pinpointing where code lands, reading files to size up edit targets, and web lookups for docs or syntax. The only files you read directly are ones you authored under docs/artifacts/ and repo-level context docs (AGENTS.md, README.md). webfetch is denied to you by permission; recon is a dispatch, not a fetch.
```

- [ ] **Step 5: `commands/full-cycle.md` step 1**

Read the file first. Find the step 1 line containing `Dispatch the \`explore\` subagent for codebase recon` and replace the phrase `for codebase recon` with `for codebase recon and web lookups` (keep the rest of the line intact).

- [ ] **Step 6: `CHANGELOG.md`, Changed entry**

Add one entry in the repo's existing style, at the top of the most recent unreleased/Changed section (create matching the file's conventions if absent):

```markdown
- `planner` agent delegates all exploration to the `explore` subagent: body rule covering the whole run plus `webfetch` denied in frontmatter.
```

- [ ] **Step 7: Verify**

Run (expect exit 0):

```powershell
opencode agent list
```

Run (expect `webfetch` denied / false in resolved planner config, and planner still model `zai-coding-plan/glm-5.3` variant `high`):

```powershell
opencode debug agent planner
```

Run (expect empty):

```powershell
Get-ChildItem -Recurse -Include *.md -Path agents,commands | Select-String -Pattern ([char]0x2014); Select-String -Path README.md,AGENTS.md,CHANGELOG.md -Pattern ([char]0x2014)
```

- [ ] **Step 8: Commit**

```powershell
git add agents/planner.md commands/full-cycle.md CHANGELOG.md
git commit -m "feat(agents): force planner recon through explore subagent"
```

---

## Post-task (orchestrator conventions, not executor tasks)

- doc-standardizer review after the task loop (code-standardizer skipped: diff touches no source code, markdown/config only).
- documenter close-out: execution report to `docs/artifacts/features/explore-recon-delegation/`, catalog drift check, docs commit.
- Remind the user in the final report: restart opencode to load the new agent definitions (config loads once at startup), and `agents/*.md` are inert until copied to `~/.config/opencode/agents/`.
