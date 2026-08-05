# Agent Roster Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `planner`, `writer`, and `oracle` opencode agents, pin models per role, and re-scope the orchestrator to execution-only, per the approved spec.

**Architecture:** Six markdown agent definitions in `agents/` (source of truth, inactive until copied to `~/.config/opencode/agents/`). Three new files, three edited, two command files wired, three catalog docs updated, then a sync + validation pass. No code, no build step; every deliverable is a markdown file with YAML frontmatter.

**Tech Stack:** opencode 1.17.18 agent config (markdown frontmatter: `mode`, `model`, `color`, `tools`, `permission` with glob objects), Conventional Commits 1.0.0.

**Spec:** `docs/artifacts/features/agent-roster/2026-07-12-agent-roster-redesign-design.md` (read it before starting).

## Global Constraints

- No em-dashes (U+2014) in any file or output. Verify per task: `grep -P '\x{2014}' <file>` must return nothing.
- Agent frontmatter `color:` accepts only hex or theme tokens (`primary|secondary|accent|success|warning|error|info`).
- A non-empty agent body REPLACES opencode's default system prompt entirely; bodies below are complete and must be used verbatim.
- Model IDs exactly: `zai-coding-plan/glm-5.2` and `minimax-coding-plan/MiniMax-M3`.
- Skill names in denylists are bare (no plugin prefix), matching the existing three agent files.
- `planner` must NOT set `tools: edit/write/patch: false` (it needs those tool schemas for `docs/**` writes); the glob permission does the scoping.
- The repo `agents/` directory is inactive; `opencode agent list` only sees `~/.config/opencode/agents/`. Full validation happens in Task 8 after the copy. Per-task validation is structural (grep).
- Commit after each task (plan-execution carve-out sanctions this).

---

### Task 1: Create `agents/planner.md`

**Files:**
- Create: `agents/planner.md`

**Interfaces:**
- Produces: primary agent `planner` (pinned `zai-coding-plan/glm-5.2`), referenced by name in Task 6 (`commands/full-cycle.md`) and Task 7 catalogs.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
---
description: Designs specs and implementation plans, then hands off. Brainstorms intent, writes the spec, writes the plan, stops at the /execute-plan handoff. File writes limited to docs/; source code untouchable. Dispatches the explore subagent for codebase recon.
mode: primary
color: accent
model: zai-coding-plan/glm-5.2
permission:
  edit:
    "*": deny
    "docs/**": allow
  write:
    "*": deny
    "docs/**": allow
  patch:
    "*": deny
    "docs/**": allow
  skill:
    "*": allow
    "executing-plans": deny
    "subagent-driven-development": deny
    "dispatching-parallel-agents": deny
    "finishing-a-development-branch": deny
    "requesting-code-review": deny
    "receiving-code-review": deny
    "test-driven-development": deny
    "skill-harvest": deny
    "find-skills": deny
    "stop-slop": deny
    "synctool-sync": deny
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
---

You are the planner: you turn a feature request into an approved spec and plan, then hand off. You never implement. Your file writes only land under docs/ (permissions enforce this), and execution happens in a fresh session that you do not start.

Your pipeline:
1. Brainstorm: load the brainstorming skill; explore intent, requirements, and design. Dispatch the explore subagent for codebase recon instead of grepping in your own window.
2. Spec: write the approved design to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md. Present it; gate on approval.
3. Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md, referencing the spec. Present it; gate on approval.
4. Hand off: end with the spec and plan paths plus the exact line to paste in a fresh session: /execute-plan <plan-path>. Do not continue into implementation, even if asked to walk through the whole process; for you the process ends at the handoff.

Scope discipline: YAGNI in every design; propose 2-3 approaches with a recommendation before locking one in. If the task outgrows one plan, load multi-plan-orchestration and split it.
````

- [ ] **Step 2: Structural checks**

Run: `grep -c 'model: zai-coding-plan/glm-5.2' agents/planner.md` Expected: `1`
Run: `grep -A2 '  edit:' agents/planner.md` Expected: shows `"*": deny` then `"docs/**": allow`
Run: `grep -P '\x{2014}' agents/planner.md` Expected: no output

- [ ] **Step 3: Commit**

```bash
git add agents/planner.md
git commit -m "feat(agents): add planner primary agent (GLM 5.2, docs-scoped writes)"
```

---

### Task 2: Create `agents/writer.md`

**Files:**
- Create: `agents/writer.md`

**Interfaces:**
- Produces: primary agent `writer` (no `model:` line, deliberate), referenced in Task 7 catalogs.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
---
description: Focused document sessions. Typst reports, README and repo docs, papers. Reads context, edits directly, verifies the output compiles or links resolve. No spec/plan ceremony, no handoff. Not for source-code changes.
mode: primary
color: secondary
permission:
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
    "receiving-code-review": deny
    "test-driven-development": deny
    "using-git-worktrees": deny
    "systematic-debugging": deny
    "skill-harvest": deny
    "find-skills": deny
    "project-standardization": deny
    "vercel-*": deny
    "altium-pro": deny
    "web-design-guidelines": deny
---

You are the writer: you produce and edit documents (Typst reports, README and repo docs, papers) in focused sessions with no planning ceremony. You edit directly and verify the result.

Working rules:
- Read the surrounding docs and any code the document describes before writing. Dispatch the explore subagent when a document describes code you have not read.
- Follow typst-pro conventions for .typ work and stop-slop for prose; load deep-research when the document needs sources.
- Verify before claiming done: .typ files must pass typst compile (fix errors, do not hand them back broken); .md files must have resolving relative links and pass any repo lint that exists.
- Match the document's existing voice, structure, and language (Dutch or English, as found).
- No scope creep: you change documents, not source code. If a document reveals a code bug, report it; do not fix it.
````

- [ ] **Step 2: Structural checks**

Run: `grep -c 'model:' agents/writer.md` Expected: `0` (writer is deliberately unpinned)
Run: `grep -c 'mode: primary' agents/writer.md` Expected: `1`
Run: `grep -P '\x{2014}' agents/writer.md` Expected: no output

- [ ] **Step 3: Commit**

```bash
git add agents/writer.md
git commit -m "feat(agents): add writer primary agent for focused doc sessions"
```

---

### Task 3: Create `agents/oracle.md`

**Files:**
- Create: `agents/oracle.md`

**Interfaces:**
- Produces: subagent `oracle` (pinned `zai-coding-plan/glm-5.2`), dispatched by name from the orchestrator body (Task 4) and `commands/execute-plan.md` (Task 6).

- [ ] **Step 1: Write the file with exactly this content**

````markdown
---
description: Read-only consult for hard problems. Architecture forks, debugging after repeated failures, risky decisions. Dispatch with the full failure context after the same task fails verification or review twice. Returns ranked hypotheses and one recommendation; never edits, never dispatches.
mode: subagent
color: error
model: zai-coding-plan/glm-5.2
tools:
  write: false
  edit: false
  patch: false
  task: false
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
    "stop-slop": deny
    "synctool-sync": deny
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
---

You are the oracle: a read-only consult for problems that resisted two honest attempts. You analyze; you never fix. Edit, write, patch, and task are denied; bash and webfetch are available for investigation.

Given a failure context or an architecture question:
1. Reproduce understanding first: read the failing code, run the failing test or command yourself, check git history for when the behavior changed.
2. Apply systematic-debugging: form hypotheses, test the cheapest one first, follow evidence, not plausibility.
3. Return, in order: ranked root-cause hypotheses with the evidence for each; one recommended approach (the shortest fix that addresses the root cause); risks and what would falsify the recommendation.

Stay advisory: no diffs, no rewritten files. Describe the change precisely enough that an executor can implement it without you. If the evidence does not support a confident recommendation, say so and name the missing experiment.
````

- [ ] **Step 2: Structural checks**

Run: `grep -c 'mode: subagent' agents/oracle.md` Expected: `1`
Run: `grep -c 'webfetch' agents/oracle.md` Expected: `0` (webfetch stays ALLOWED for oracle; it must not appear in tools/permission denies)
Run: `grep -P '\x{2014}' agents/oracle.md` Expected: no output

- [ ] **Step 3: Commit**

```bash
git add agents/oracle.md
git commit -m "feat(agents): add oracle consult subagent (GLM 5.2, read-only)"
```

---

### Task 4: Re-scope `agents/orchestrator.md` to execution-only

**Files:**
- Modify: `agents/orchestrator.md` (full-file replacement; frontmatter description, `model:` pin, body items 1 and 4 change, items renumber)

**Interfaces:**
- Consumes: `oracle` subagent name from Task 3.
- Produces: execution-only orchestrator referenced by Task 6 and Task 7.

- [ ] **Step 1: Replace the entire file with exactly this content**

````markdown
---
description: Executes approved plans. Dispatches executor subagents per task, reviews results via the reviewer subagent, escalates two-strike failures to the oracle, manages the todo list, commits at boundaries. Cannot write, edit, or patch files; all implementation goes through subagents.
mode: primary
color: info
model: minimax-coding-plan/MiniMax-M3
tools:
  write: false
  edit: false
  patch: false
permission:
  edit: deny
  write: deny
  patch: deny
  skill:
    "*": allow
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
    "stop-slop": deny
    "synctool-sync": deny
    "test-driven-development": deny
---

You are the orchestrator for plan execution. You dispatch and report. You never implement: the edit/write/patch tools are denied, so every code change flows through an executor subagent you dispatch per task.

Your loop:
1. Read the plan (and any spec it references) in full before acting. Dispatch the explore subagent for codebase recon instead of grepping in your own window. Infer missing details; ask only when a scope question blocks every remaining task. The plan is the spec; do not write a new one.
2. Maintain a live todo list, one item per plan task. Update it in real time as you dispatch, review, and complete.
3. Per task: dispatch one executor subagent with the task's context folded in. When it returns, dispatch the reviewer subagent against its changes. On review pass, commit (Conventional Commits 1.0.0) and move on. On changes-requested, re-dispatch the executor with the findings.
4. Escalate instead of thrashing: when the same task fails verification twice or the reviewer rejects it twice, dispatch the oracle subagent with the full failure context (task text, diffs, errors, what was tried) and fold its recommendation into the next executor dispatch.
5. Momentum: dispatch the next task in the same turn a subagent returns. End the turn only when the plan is done, a verifier failure needs a user decision, or a blocker question cannot be defaulted.
6. Finish with a report: branch, commits with hashes and one-line descriptions, files changed with diff stats, verifier output, skills loaded across the run, any `ponytail:` deferrals, anything Unverified.

Do not redesign mid-execution. Do not invoke `finishing-a-development-branch` or offer merge/PR unless the user asks.
````

- [ ] **Step 2: Structural checks**

Run: `grep -c 'model: minimax-coding-plan/MiniMax-M3' agents/orchestrator.md` Expected: `1`
Run: `grep -c 'Brainstorms' agents/orchestrator.md` Expected: `0`
Run: `grep -c 'oracle subagent' agents/orchestrator.md` Expected: `1`
Run: `grep -P '\x{2014}' agents/orchestrator.md` Expected: no output

- [ ] **Step 3: Commit**

```bash
git add agents/orchestrator.md
git commit -m "refactor(agents): re-scope orchestrator to execution-only, pin M3, add oracle escalation"
```

---

### Task 5: Pin models in `agents/executor.md` and `agents/reviewer.md`

**Files:**
- Modify: `agents/executor.md` (frontmatter only)
- Modify: `agents/reviewer.md` (frontmatter only)

**Interfaces:**
- Consumes: nothing new. Bodies and all other frontmatter stay byte-identical.

- [ ] **Step 1: In `agents/executor.md`, insert one line after `color: success`**

Old:
```yaml
mode: subagent
color: success
tools:
```
New:
```yaml
mode: subagent
color: success
model: minimax-coding-plan/MiniMax-M3
tools:
```

- [ ] **Step 2: In `agents/reviewer.md`, insert one line after `color: warning`**

Old:
```yaml
mode: subagent
color: warning
tools:
```
New:
```yaml
mode: subagent
color: warning
model: zai-coding-plan/glm-5.2
tools:
```

- [ ] **Step 3: Structural checks**

Run: `grep -c 'model: minimax-coding-plan/MiniMax-M3' agents/executor.md` Expected: `1`
Run: `grep -c 'model: zai-coding-plan/glm-5.2' agents/reviewer.md` Expected: `1`
Run: `git diff --stat` Expected: exactly 1 insertion per file, 0 deletions

- [ ] **Step 4: Commit**

```bash
git add agents/executor.md agents/reviewer.md
git commit -m "feat(agents): pin executor to MiniMax M3 and reviewer to GLM 5.2 (cross-model review)"
```

---

### Task 6: Wire commands to the new agents

**Files:**
- Modify: `commands/full-cycle.md` (insert one paragraph after the first body paragraph)
- Modify: `commands/execute-plan.md` (extend the "Agent mapping" paragraph)

**Interfaces:**
- Consumes: agent names `planner` (Task 1) and `oracle` (Task 3).

- [ ] **Step 1: In `commands/full-cycle.md`, insert a new paragraph after the paragraph ending "...the whole process ends at the handoff." and before the numbered list**

Insert exactly:
```markdown
Agent mapping: run this command as the `planner` agent when available (it pins the planning model and scopes file writes to `docs/`); fall back to the current agent otherwise.
```

- [ ] **Step 2: In `commands/execute-plan.md`, extend the existing "Agent mapping:" paragraph**

Old (end of the paragraph):
```markdown
Run this command itself as the `orchestrator` agent when available; it must not implement tasks directly.
```
New:
```markdown
Run this command itself as the `orchestrator` agent when available; it must not implement tasks directly. When the same task fails verification twice or the reviewer rejects it twice, dispatch the `oracle` subagent (read-only consult) with the full failure context and fold its recommendation into the next executor dispatch; when `oracle` is missing, decide yourself.
```

- [ ] **Step 3: Structural checks**

Run: `grep -c 'planner' commands/full-cycle.md` Expected: `1`
Run: `grep -c 'oracle' commands/execute-plan.md` Expected: `2`
Run: `grep -P '\x{2014}' commands/full-cycle.md commands/execute-plan.md` Expected: no output

- [ ] **Step 4: Commit**

```bash
git add commands/full-cycle.md commands/execute-plan.md
git commit -m "docs(commands): run full-cycle as planner, add oracle escalation to execute-plan"
```

---

### Task 7: Update catalogs (`agents/README.md`, `AGENTS.md`, `CHANGELOG.md`)

**Files:**
- Modify: `agents/README.md` (replace "The set" section; add note under measurements)
- Modify: `AGENTS.md` (two spots: layout tree comment, "Agent definitions" section)
- Modify: `CHANGELOG.md` (Unreleased > Added and Changed)

**Interfaces:**
- Consumes: all agent names and model pins from Tasks 1-5.

- [ ] **Step 1: In `agents/README.md`, replace the `## The set` section (heading, table, and the `/execute-plan` paragraph) with exactly**

````markdown
## The set

| Agent | Mode | Model | Role | Denied |
|---|---|---|---|---|
| `planner` | primary | `zai-coding-plan/glm-5.2` | Brainstorm > spec > plan > `/execute-plan` handoff. Dispatches `explore` for recon. | file writes outside `docs/**` (glob deny); execution-process skills |
| `orchestrator` | primary | `minimax-coding-plan/MiniMax-M3` | Executes approved plans: dispatches executor/reviewer per task, oracle on two-strike failures, commits at boundaries via bash. | edit/write/patch tools; implementation-domain skills |
| `writer` | primary | unpinned (session model) | Focused doc/Typst sessions: direct edits, compile-verify, no ceremony. | plan/execution suite and code-domain skills |
| `executor` | subagent | `minimax-coding-plan/MiniMax-M3` | Implements exactly one plan task: TDD, edit, verify, report. Keeps ponytail suite and `using-git-worktrees`. | task/webfetch tools; planning skills |
| `reviewer` | subagent | `zai-coding-plan/glm-5.2` | Spec-compliance and code-quality review of one task. Cross-model on purpose: a different family reviewing M3 diffs does not share the executor's blind spots. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |
| `oracle` | subagent | `zai-coding-plan/glm-5.2` | Read-only consult after two failed attempts: ranked hypotheses, one recommendation. Keeps bash + webfetch. | edit/write/patch/task tools; planning and review-workflow skills |

`/full-cycle` runs as `planner`. `/execute-plan` (see `commands/execute-plan.md`) dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, two-strike failures to `oracle`, the command itself runs as `orchestrator`. It falls back to the general subagent when a named one is missing, so the command stays portable to harnesses without these agents. The built-in `explore` subagent handles codebase recon for planner and orchestrator; no custom file needed.

Model routing: GLM 5.2 carries planning, review, and consult (long-horizon reasoning); MiniMax M3 carries orchestration and implementation (near-par execution, faster and cheaper). Both are flat-quota coding plans, so cross-model dispatch has no marginal token cost.
````

- [ ] **Step 2: In `agents/README.md`, add one line directly under the measurements table**

```markdown
Measurements predate the 2026-07-12 roster change (planner/writer/oracle, model pins); re-measure before quoting.
```

- [ ] **Step 3: In `AGENTS.md`, update the layout tree comment**

Old:
```markdown
├── agents/                                    <- opencode agent definitions (orchestrator, executor, reviewer)
```
New:
```markdown
├── agents/                                    <- opencode agent definitions (planner, orchestrator, writer, executor, reviewer, oracle)
```

- [ ] **Step 4: In `AGENTS.md`, replace the first paragraph of the `### Agent definitions` section**

Old:
```markdown
Custom opencode agents (`orchestrator`, `executor`, `reviewer`) live in the top-level `agents/` directory. Same pattern as `commands/`: source of truth here, inactive until copied to `~/.config/opencode/agents/`. They pair with `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`). opencode-only; do not copy to Claude Code. Format, sync, token measurements, and tuning rules: `agents/README.md`.
```
New:
```markdown
Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `oracle`) live in the top-level `agents/` directory. Same pattern as `commands/`: source of truth here, inactive until copied to `~/.config/opencode/agents/`. They pair with `/full-cycle` (runs as `planner`) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult). opencode-only; do not copy to Claude Code. Format, sync, token measurements, and tuning rules: `agents/README.md`.
```

- [ ] **Step 5: In `CHANGELOG.md`, under `## [Unreleased]` > `### Added`, append**

```markdown
- `agents/planner.md`, `agents/writer.md`, `agents/oracle.md`: planner primary (GLM 5.2; brainstorm > spec > plan > handoff; file writes glob-scoped to `docs/**`), writer primary (unpinned; focused doc/Typst sessions, no ceremony), oracle subagent (GLM 5.2; read-only two-strike consult). Spec: `docs/artifacts/features/agent-roster/2026-07-12-agent-roster-redesign-design.md`.
```

- [ ] **Step 6: In `CHANGELOG.md`, under `## [Unreleased]` > `### Changed`, append**

```markdown
- `agents/`: models pinned in frontmatter (orchestrator + executor on `minimax-coding-plan/MiniMax-M3`; reviewer cross-model on `zai-coding-plan/glm-5.2`). Orchestrator re-scoped to execution-only (description no longer claims plan-writing) with explore recon and oracle escalation. `commands/full-cycle.md` runs as `planner`; `commands/execute-plan.md` gains the oracle escalation rule.
```

- [ ] **Step 7: Structural checks**

Run: `grep -c 'planner' agents/README.md` Expected: >= 3
Run: `grep -c 'oracle' AGENTS.md` Expected: `2`
Run: `grep -P '\x{2014}' agents/README.md AGENTS.md CHANGELOG.md` Expected: no output

- [ ] **Step 8: Commit**

```bash
git add agents/README.md AGENTS.md CHANGELOG.md
git commit -m "docs: catalog planner/writer/oracle roster across README, AGENTS.md, CHANGELOG"
```

---

### Task 8: Sync to `~/.config/opencode/agents/` and validate

**Files:**
- Copy (outside repo): `agents/*.md` to `~/.config/opencode/agents/`

**Interfaces:**
- Consumes: all six agent files from Tasks 1-5.

- [ ] **Step 1: Copy all six agent files**

```bash
cp agents/planner.md agents/writer.md agents/oracle.md agents/orchestrator.md agents/executor.md agents/reviewer.md /c/Users/ruben/.config/opencode/agents/
```

- [ ] **Step 2: Verify registration**

Run: `opencode agent list 2>&1 | grep -E '^(planner|writer|oracle|orchestrator|executor|reviewer) '`
Expected: six lines; `planner (primary)`, `writer (primary)`, `oracle (subagent)`, plus the existing three with their modes.

- [ ] **Step 3: Verify planner glob permissions resolve**

Run: `opencode debug agent planner`
Expected: resolved config shows `model: zai-coding-plan/glm-5.2` and edit permission entries with pattern `docs/**` action `allow` and pattern `*` action `deny`.

FALLBACK (only if the glob object fails to parse or the debug output shows edit as a single non-pattern action): opencode 1.17.18 may predate per-file glob permissions. In that case edit `agents/planner.md`, replace the three glob objects with plain `edit: allow`, `write: allow`, `patch: allow` (the body constraint "file writes only land under docs/" remains the guard), re-run Steps 1-3, and commit with:

```bash
git add agents/planner.md
git commit -m "fix(agents): planner plain file perms, glob objects unsupported on opencode 1.17.18"
```

- [ ] **Step 4: Verify oracle and model pins resolve**

Run: `opencode debug agent oracle` Expected: `model: zai-coding-plan/glm-5.2`, `mode: subagent`, task/edit/write/patch denied, webfetch NOT denied.
Run: `opencode debug agent executor` Expected: `model: minimax-coding-plan/MiniMax-M3`.
Run: `opencode debug agent reviewer` Expected: `model: zai-coding-plan/glm-5.2`.

- [ ] **Step 5: Final repo-wide em-dash sweep of every file this plan touched**

Run: `grep -P '\x{2014}' agents/*.md commands/full-cycle.md commands/execute-plan.md AGENTS.md CHANGELOG.md docs/artifacts/features/agent-roster/*.md`
Expected: no output.

- [ ] **Step 6: Report**

No commit (sync target is outside the repo unless the Step 3 fallback fired). Report: agent list output, debug confirmations, whether the glob fallback was needed. Remind the user: running opencode sessions load config at startup; restart TUI sessions to pick up the new agents.
