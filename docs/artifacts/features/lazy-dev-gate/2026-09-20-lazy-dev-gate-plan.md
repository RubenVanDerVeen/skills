# lazy-dev gate Implementation Plan

> **For agentic workers:** Execute via the `orchestrator` subagent following `/execute-plan` conventions (`commands/execute-plan.md`): branch first, per-task Conventional Commits, `executor` per task, `reviewer` per task, `oracle` on two-strike failures, structure review (`doc-standardizer`, then `code-standardizer`), then `documenter`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Insert a `lazy-dev` lean-plan review gate between the planner writing a plan and dispatching the orchestrator.

**Architecture:** New read-only subagent `agents/lazy-dev.md` (clone of `reviewer.md`'s shape, ponytail ladder as the review lens, PASS-or-findings contract). Planner gains step 5 dispatching it in a loop capped at 2 rounds; `commands/full-cycle.md` mirrors the step; catalogs updated in the same commit as the new agent.

**Tech Stack:** Markdown only. opencode agent frontmatter. No runtime code.

**Spec:** `docs/artifacts/features/lazy-dev-gate/2026-09-20-lazy-dev-gate-design.md`

**Versioning:** Repo AGENTS.md declares no `### Versioning` subsection: unversioned, no bump.

## Global Constraints

- No em-dashes (U+2014) in any markdown file. Verify per touched file: `Select-String -Pattern ([char]0x2014)` returns empty.
- Agent frontmatter mirrors: keep both `tools:` denies and matching `permission:` denies; `"*": allow` skill rule FIRST, narrow denies after; `"homelab*": false` in `tools:`.
- Agents are opencode-only: never copy to `~/.claude/`.
- Conventional Commits 1.0.0; catalog updates ship in the same commit as the change they catalog.
- Do not reformat or rewrite surrounding content in edited files; surgical edits only.
- Work on branch `feat/lazy-dev-gate`.

---

### Task 1: New lazy-dev agent plus catalogs

**Files:**
- Create: `agents/lazy-dev.md`
- Modify: `agents/README.md` (roster table `## The set`, dispatch-convention paragraph, model-routing paragraph)
- Modify: `AGENTS.md` (Agent definitions paragraph, custom-agents name list)
- Modify: `CHANGELOG.md` (Added entry under `[Unreleased]`; read the file first and follow its Keep a Changelog format)

**Interfaces:**
- Consumes: nothing.
- Produces: an opencode subagent named `lazy-dev` (dispatched by name), and catalog rows other tasks and future readers rely on.

- [ ] **Step 1: Create `agents/lazy-dev.md` with this exact content**

````markdown
---
description: Lean-plan gate. Reviews a written implementation plan for over-engineering before execution. Read-only plus bash; cannot edit files or dispatch subagents. Returns PASS or numbered findings with specific fixes. Dispatched by the planner after writing the spec and plan; the planner loops findings back until PASS, capped at 2 rounds.
mode: subagent
color: info
model: zai-coding-plan/glm-5.3
variant: high
tools:
  write: false
  edit: false
  patch: false
  task: false
  webfetch: false
  "homelab*": false
permission:
  edit: deny
  write: deny
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
    "using-git-worktrees": deny
    "requesting-code-review": deny
    "receiving-code-review": deny
    "test-driven-development": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
    "code-standardization": deny
    "stop-slop": deny
    "synctool-sync": deny
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
---

You are lazy-dev: the lean-plan gate. You review a written implementation plan for over-engineering before anything gets built. Read-only plus bash for quick repo checks; you do not edit, write, or dispatch.

Lens: ponytail. Interrogate every task with the ladder, in order:
1. Does this task need to exist at all? Speculative need = recommend deletion, say so in one line.
2. Does the plan prescribe a custom solution where the standard library, a native platform feature, or an already-installed dependency covers it?
3. Does a task build flexibility, abstraction, or configuration nothing asked for?
4. Would the fewest-tasks, shortest-diff version of this plan be materially worse? If not, collapse the tasks.
5. Is verification proportional? One runnable check per non-trivial task; no per-function suites, no frameworks unless asked.

Two passes:
1. Context: read the spec and plan end to end. The spec defines what was asked; anything in the plan the spec does not require is a finding candidate.
2. Verdict per task. Use bash only when a claim needs checking (a dependency already present in the manifest, a stdlib equivalent). Do not redesign plans that are already minimal; give them a fast PASS.

Return PASS, or a numbered list. Each finding: the plan reference (task number or heading), the problem in one line, and the specific fix ("Delete task 3; <X> already covers it"). If a finding's root cause is in the spec, prefix it with "spec:" and state what to change there. Never rewrite the plan yourself.
````

- [ ] **Step 2: Add the roster row in `agents/README.md`**

In the `## The set` table, add a row directly under the `reviewer` row, matching column structure (Agent | Mode | Model | Role | Denied):

```markdown
| `lazy-dev` | subagent | `zai-coding-plan/glm-5.3` | Lean-plan gate: reviews the written plan for over-engineering before orchestrator dispatch; PASS or findings, planner loops to a 2-round cap. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |
```

- [ ] **Step 3: Extend the dispatch-convention paragraph in `agents/README.md`**

At the end of the paragraph that describes dispatch-by-name (the one mentioning `executor`, `reviewer`, `oracle`), append this sentence:

```markdown
The `planner` gates every plan through `lazy-dev` (lean-plan review, PASS or findings, 2-round cap) before any orchestration starts.
```

- [ ] **Step 4: Add `lazy-dev` to the model-routing paragraph in `agents/README.md`**

In the model-routing paragraph, extend the `high` effort agent list from:

```markdown
(planner, reviewer, oracle, doc-standardizer, code-standardizer, documenter, explore)
```

to:

```markdown
(planner, reviewer, lazy-dev, oracle, doc-standardizer, code-standardizer, documenter, explore)
```

If the actual wording differs slightly, match the existing list style; the requirement is that `lazy-dev` appears in the `high` effort list.

- [ ] **Step 5: Add `lazy-dev` to the agent name list in `AGENTS.md`**

In the `### Agent definitions` paragraph, replace:

```markdown
Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `oracle`, `doc-standardizer`, `code-standardizer`, `documenter`, `explore`)
```

with:

```markdown
Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `lazy-dev` (lean-plan gate), `oracle`, `doc-standardizer`, `code-standardizer`, `documenter`, `explore`)
```

- [ ] **Step 6: Add the CHANGELOG entry**

Under `[Unreleased]` > `### Added` in `CHANGELOG.md` (create the subsection if missing, following the file's existing format), add:

```markdown
- lazy-dev subagent: lean-plan gate reviewing plans for over-engineering before orchestrator dispatch
```

- [ ] **Step 7: Verify Task 1**

Run from repo root:

```powershell
Select-String -Path "agents\lazy-dev.md","agents\README.md","AGENTS.md","CHANGELOG.md" -Pattern ([char]0x2014)
```

Expected: no output. Then confirm `agents/lazy-dev.md` starts with `---`, has `mode: subagent`, `color: info`, `"homelab*": false`, and `"*": allow` as the first `skill:` rule.

- [ ] **Step 8: Commit**

```powershell
git add agents/lazy-dev.md agents/README.md AGENTS.md CHANGELOG.md
git commit -m "feat(agents): add lazy-dev lean-plan gate subagent"
```

---

### Task 2: Wire the gate into the planner

**Files:**
- Modify: `agents/planner.md` (frontmatter `description`, pipeline step list)

**Interfaces:**
- Consumes: the `lazy-dev` subagent from Task 1.
- Produces: planner pipeline step 5 (lean-plan gate); steps renumbered so dispatch is 6 and handoff is 7. Task 3 mirrors this numbering.

- [ ] **Step 1: Update the frontmatter `description`**

In `agents/planner.md`, replace:

```markdown
Designs specs and implementation plans, then dispatches the orchestrator to execute the plan in the same run. Brainstorms intent (skip with `no brainstorm`), writes the spec, writes the plan, dispatches the orchestrator subagent, relays its report.
```

with:

```markdown
Designs specs and implementation plans, then dispatches the orchestrator to execute the plan in the same run. Brainstorms intent (skip with `no brainstorm`), writes the spec, writes the plan, dispatches the orchestrator subagent, relays its report. Gates every plan through the lazy-dev subagent (lean-plan review, loop to PASS capped at 2 rounds) before dispatching.
```

- [ ] **Step 2: Update step 1 keyword sentence**

Replace:

```markdown
1. Parse the prompt for keywords: `no brainstorm` skips step 2; `handoff` switches the end of the pipeline to the manual handoff in step 6.
```

with:

```markdown
1. Parse the prompt for keywords: `no brainstorm` skips step 2; `handoff` switches the end of the pipeline to the manual handoff in step 7.
```

- [ ] **Step 3: Insert the new gate step and renumber**

After the paragraph for step 4 (Plan), insert this new step:

```markdown
5. Lean-plan gate: dispatch the lazy-dev subagent with the spec and plan paths. On findings, fold the corrections into the plan (edit the spec too when a finding is prefixed "spec:") and re-dispatch. PASS is required before dispatching the orchestrator; cap the loop at 2 review rounds, and on a cap without PASS attach the remaining findings to the orchestrator dispatch as constraints. If the lazy-dev agent is unavailable, dispatch the general subagent instructed to review the plan with the ponytail skill and return PASS or findings in the same format.
```

Then renumber the two existing steps that follow: `5.` (Dispatch) becomes `6.`, `6.` (Handoff) becomes `7.`.

- [ ] **Step 4: Update the dispatch fallback reference**

In the Dispatch step (now step 6), replace:

```markdown
if no subagent dispatch is possible, fall back to step 6
```

with:

```markdown
if no subagent dispatch is possible, fall back to step 7
```

- [ ] **Step 5: Verify Task 2**

```powershell
Select-String -Path "agents\planner.md" -Pattern ([char]0x2014)
```

Expected: no output. Then confirm the pipeline reads steps 1-7 in order, exactly one step starts with `5. Lean-plan gate:`, step 1 references `step 7`, and the fallback in step 6 references `step 7`.

- [ ] **Step 6: Commit**

```powershell
git add agents/planner.md
git commit -m "feat(planner): gate plan dispatch through lazy-dev review"
```

---

### Task 3: Mirror the gate in full-cycle and the flow diagram

**Files:**
- Modify: `commands/full-cycle.md` (step list)
- Modify: `docs/workflows/plan-flow.drawio` (one gate box)

**Interfaces:**
- Consumes: the gate semantics defined in Task 2 (2-round cap, findings attached on cap).
- Produces: the mirrored step in `/full-cycle`, and the updated flow diagram.

- [ ] **Step 1: Insert the gate step in `commands/full-cycle.md`**

Read the file first. Between the step for Plan (currently step 3) and the step for Execute (currently step 4), insert:

```markdown
4. Lean-plan gate: dispatch the `lazy-dev` subagent with the spec and plan paths; fold findings into the plan and re-dispatch until PASS (max 2 rounds), attaching leftovers to the execute dispatch as constraints.
```

Renumber all steps after the insertion point so numbering stays sequential.

- [ ] **Step 2: Add the gate box in `docs/workflows/plan-flow.drawio`**

Read the XML first. Add one box between the node representing the written plan and the node representing the orchestrator dispatch, with a directed edge from plan to gate and from gate to dispatch. Label:

```
lazy-dev: lean-plan gate (PASS or findings, max 2 rounds)
```

Reuse the exact `mxCell` `style` attribute of the neighboring step boxes (copy from an existing step node) so the diagram stays visually consistent. Keep geometry plausible: place the gate box between the two existing nodes, nudging the dispatch node right if boxes would overlap.

- [ ] **Step 3: Verify Task 3**

```powershell
Select-String -Path "commands\full-cycle.md" -Pattern ([char]0x2014); Select-String -Path "commands\full-cycle.md" -Pattern "lazy-dev"
```

First command expected: no output. Second: at least one match (the new step). Then confirm `docs/workflows/plan-flow.drawio` is still well-formed XML:

```powershell
[xml](Get-Content -Raw "docs\workflows\plan-flow.drawio") | Out-Null; "XML OK"
```

Expected: `XML OK`.

- [ ] **Step 4: Commit**

```powershell
git add commands/full-cycle.md docs/workflows/plan-flow.drawio
git commit -m "feat(pipeline): mirror lazy-dev gate in full-cycle and plan-flow"
```

---

### Task 4: Whole-feature verification

**Files:**
- None modified (read-only verification). Only commit if a fix was required.

**Interfaces:**
- Consumes: Tasks 1-3 outputs.
- Produces: verification evidence for the report.

- [ ] **Step 1: Parse check**

Run: `opencode agent list`
Expected: exits clean. Then, if `lazy-dev` resolves: `opencode debug agent lazy-dev` (expect model `zai-coding-plan/glm-5.3`, variant `high`, edit/write/task/webfetch denied). If `lazy-dev` is absent because the repo copy is not synced to `~/.config/opencode/agents/`, note that in the report and fall back to Step 2-style manual frontmatter checks; do not copy files outside the repo.

- [ ] **Step 2: Cross-file consistency grep**

```powershell
Select-String -Path "agents\planner.md","commands\full-cycle.md" -Pattern "Lean-plan gate"; Select-String -Path "agents\README.md" -Pattern "lazy-dev"; Select-String -Path "AGENTS.md" -Pattern "lazy-dev"
```

Expected: gate step present in both pipeline files; `lazy-dev` present in roster, dispatch paragraph, model-routing list, and `AGENTS.md` name list.

- [ ] **Step 3: Repo-wide em-dash sweep on touched types**

```powershell
(Get-ChildItem -Recurse -Include *.md,*.drawio | Select-String -Pattern ([char]0x2014))
```

Expected: no output.

- [ ] **Step 4: Fix and commit only if a check failed**

If anything failed: fix it, re-run the failed check, and commit as `fix(agents): <what was wrong>`. If all checks passed: no commit.

---

## Execution notes for the orchestrator

- Branch first: `feat/lazy-dev-gate` from `main`.
- One `executor` per task, `reviewer` after each; the reviewer should check surgical-edit discipline (no reformatting of untouched lines) plus the Global Constraints.
- Report should list commits, verification outputs (agent list result, XML OK, em-dash sweep empty), and any deviations.
