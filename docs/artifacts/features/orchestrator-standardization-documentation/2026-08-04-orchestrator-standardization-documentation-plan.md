# Orchestrator Standardization + Documentation Phase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two post-implementation phases (structure review, documentation) to the orchestrator's plan-execution loop via two new subagents (`standardizer`, `documenter`), and teach `project-standardization` to scaffold `docs/artifacts/features/` alongside specs/plans/reviews (paths migrated to per-feature layout on 2026-08-05; current artifact set is `docs/artifacts/{features,reviews}/`).

**Architecture:** Two new read/write-scoped subagents extend the existing executor/reviewer/oracle roster. The orchestrator dispatches them in two new loop phases after the task loop. The `reports/` artifact joins the standardization convention via a find-and-extend across the ~8 files that reference `{specs,plans,reviews}`.

**Tech Stack:** opencode agent definitions (YAML frontmatter + body), Markdown. No runtime, no build step.

**Spec:** `docs/artifacts/features/orchestrator-standardization-documentation/2026-08-04-orchestrator-standardization-documentation-design.md`

## Global Constraints

- No em-dashes (U+2014). Use commas, colons, periods, parentheses, or hyphens. Verify changed files with `Select-String -Pattern ([char]0x2014)` returning empty.
- Conventional Commits 1.0.0 for every commit (`feat(agents):`, `feat(commands):`, `docs(skills):`, etc.). The plan-execution carve-out sanctions per-task commits; do not pause to ask.
- Agent frontmatter rules: `description` (not `name`) for agents; `mode`; `color` (hex `#rrggbb` or theme token); `model`; `tools` (deprecated but kept) + matching `permission`. Broad deny rule FIRST, narrow allows LAST inside a patterned permission object (last-match-wins).
- opencode loads agent config once at startup, so the new workflow is live only after the new files are synced to `~/.config/opencode/agents/` and opencode is restarted. This plan executes under the current workflow; verification is manual.
- Every new agent/skill must appear in every catalog that lists agents/skills (agents/README.md `## The set`, AGENTS.md agent-list prose). A roster entry missing from one catalog is a process failure.

---

### Task 1: Create the `standardizer` subagent

**Files:**
- Create: `agents/standardizer.md`

**Interfaces:**
- Produces: a read-only subagent the orchestrator dispatches in the new structure-review phase (Task 3). Returns PASS or a numbered findings list tagged `quick-fix` / `recommendation`.

- [ ] **Step 1: Create `agents/standardizer.md` with this exact content**

```markdown
---
description: Reviews the executed branch (or whole repo when the diff is structural) against the project-standardization skill: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows, Conventional Commit hygiene. Dispatch after a plan's task loop completes, before documentation. Returns PASS or numbered findings tagged quick-fix or recommendation. Read-only; does not edit or dispatch.
mode: subagent
color: info
model: zai-coding-plan/glm-5.2
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
    "stop-slop": deny
    "synctool-sync": deny
---

You are the standardizer: you audit the executed branch (or the whole repo when the diff is structural) against the `project-standardization` skill. You are read-only plus bash for git state and the skill's checks; you do not edit, write, or dispatch.

Load `project-standardization`. Audit the branch diff (`git diff <base>..HEAD`) for standardization violations: non-kebab-case paths, missing or malformed AGENTS.md sections, `docs/artifacts/` layout drift, missing changelog entries, missing catalog rows (README skills table, AGENTS.md current-skills/current-agents tables, agents/README.md roster) for new skills or agents, Conventional Commit hygiene on the branch's commits, ISO 8601 dates. Extend to the whole repo when a structural change (new top-level directory, tier graduation) warrants it.

Return short actionable findings, not a redesign. Format: PASS, or a numbered list where each item names the file/path, the rule violated, the specific fix, and a tag:
- `quick-fix`: a mechanical correction (rename a path, add a table row, add a changelog line, fix a heading). The orchestrator dispatches an executor for these.
- `recommendation`: a larger change (tier graduation, directory restructure) that is not auto-fixed and rolls forward into the execution report.

Do not re-implement. Do not fix anything yourself. Do not speculate about future needs outside the standardization rules.
```

- [ ] **Step 2: Verify no em-dashes and frontmatter parses**

Run:
```powershell
$f = 'agents\standardizer.md'; (Get-Content $f -Raw | Select-String -Pattern ([char]0x2014)).Matches.Count
```
Expected: `0`.
If `opencode` is on PATH: `opencode agent list` and confirm `standardizer` appears without a parse error. If not on PATH, note as Unverified.

- [ ] **Step 3: Commit**

```bash
git add agents/standardizer.md
git commit -m "feat(agents): add standardizer subagent for post-implementation structure review"
```

---

### Task 2: Create the `documenter` subagent

**Files:**
- Create: `agents/documenter.md`

**Interfaces:**
- Produces: a write-scoped leaf subagent the orchestrator dispatches in the new documentation phase (Task 3). Writes `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-report.md`, updates catalogs, commits as docs.

- [ ] **Step 1: Create `agents/documenter.md` with this exact content**

```markdown
---
description: Closes out a completed plan by writing its execution report and updating every catalog/doc the work touched. Write-capable leaf scoped to docs/** and root-level markdown. Dispatch after the structure-review phase. Produces docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-report.md, updates README/AGENTS/commands catalogs, commits as docs, returns the report path.
mode: subagent
color: "#3B82F6"
model: zai-coding-plan/glm-5.2
tools:
  task: false
  webfetch: false
  "homelab*": false
permission:
  edit:
    "*": deny
    "docs/**": allow
    "*.md": allow
  write:
    "*": deny
    "docs/**": allow
    "*.md": allow
  patch:
    "*": deny
    "docs/**": allow
    "*.md": allow
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
    "stop-slop": deny
    "synctool-sync": deny
---

You are the documenter: you close out a completed plan by writing its execution report and updating every catalog/doc the work touched. You write; you do not dispatch (task is denied) and you do not implement feature code.

Inputs you receive from the orchestrator: the plan path and any spec it references; the per-task commit list (hashes + one-liners); the standardizer's findings and which were fixed vs which remain as recommendations; verifier output; the dispatch log.

Do, in order:
1. Read the plan, the spec, the branch's commits (`git log <base>..HEAD --oneline`), and the diff stat. Read the standardizer's findings.
2. Write the execution report to `docs/artifacts/features/` following the layout the repo already uses for its specs and plans (flat or topic-subfoldered). Filename grammar: `YYYY-MM-DD-<slug>-report.md`. Sections: Summary; Branch and commits; Files changed (diff stats); Standardization review (findings, what was fixed, what remains); Documentation updates (catalogs/docs changed and why); Verifier output; Skills loaded; `ponytail:` deferrals; Unverified items; Dispatch Log.
3. Update every catalog/doc the work touched: README skills table, AGENTS.md current-skills/current-agents tables, commands `## Commands` sections, `opencode-install.md` name references, `external-skills.md` rows. Follow the repo's own catalog rules verbatim (the AGENTS.md "Adding or modifying a skill" section, the agents/README.md roster rules). A skill or agent that exists but is missing from one of its catalogs is a process failure: fix it before committing.
4. Commit the report and catalog updates as Conventional Commits 1.0.0 docs commits (e.g. `docs(reports): add execution report for <slug>` and `docs: update catalogs for <change>`). The plan-execution carve-out sanctions these commits; do not pause to ask.
5. Return the report path and a one-paragraph summary of what shipped.

Write scope is `docs/**` and root-level `*.md`. Do not edit skill bodies under `skills/**/SKILL.md` or source code: that is executor work. You update indexes and catalogs only.
```

- [ ] **Step 2: Verify no em-dashes**

Run:
```powershell
(Get-Content 'agents\documenter.md' -Raw | Select-String -Pattern ([char]0x2014)).Matches.Count
```
Expected: `0`.

- [ ] **Step 3: Commit**

```bash
git add agents/documenter.md
git commit -m "feat(agents): add documenter subagent for execution reports and catalog updates"
```

---

### Task 3: Wire the new phases into the orchestrator

**Files:**
- Modify: `agents/orchestrator.md` (body loop + `task:` permission block)

**Interfaces:**
- Consumes: `standardizer` (Task 1) and `documenter` (Task 2).
- Produces: the orchestrator loop now has 8 steps (two new phases + renumbered report).

- [ ] **Step 1: Add the two new steps and renumber the report**

Read `agents/orchestrator.md`. Replace the current step 5 and step 6 (the `5. Momentum...` and `6. Finish with a report...` lines) with this block, keeping steps 1-4 unchanged:

```markdown
5. Momentum: dispatch the next task in the same turn a subagent returns. End the turn only when the plan is done, a verifier failure needs a user decision, or a blocker question cannot be defaulted.
6. Structure review (after the task loop is complete): dispatch the `standardizer` subagent against the branch diff. On findings: dispatch `executor` for the items tagged `quick-fix` (kebab-case paths, missing AGENTS sections, changelog gaps, catalog rows), then `reviewer` to re-check each fix. Two-strike failures on a fix escalate to `oracle`, same rule as task implementation. Items tagged `recommendation` are not auto-fixed; carry them forward to step 7.
7. Documentation: dispatch the `documenter` subagent with the run's raw material (plan and spec paths, per-task commit list, standardizer findings and what was fixed, verifier output, dispatch log). It writes the execution report to `docs/artifacts/features/`, updates every catalog/doc the work touched, commits as docs commits, and returns the report path. You do not write the report yourself: the documenter does (you cannot; edit/write/patch are denied).
8. Finish with a report: branch; commits with hashes and one-line descriptions; files changed with diff stats; verifier output; skills loaded across the run; any `ponytail:` deferrals; anything Unverified; a Dispatch Log listing each task as "dispatched: executor + reviewer" or "self-implemented: <reason>", plus the standardizer and documenter dispatches; and the path to the report the documenter wrote. A plan completed with zero executor dispatches is a process failure - if that happened, say so explicitly at the top of the report and explain why dispatch was impossible for every task.
```

- [ ] **Step 2: Add `standardizer` and `documenter` to the `task:` permission block**

In the same file, replace:
```yaml
  task:
    "*": deny
    "executor": allow
    "reviewer": allow
    "oracle": allow
    "explore": allow
```
with:
```yaml
  task:
    "*": deny
    "executor": allow
    "reviewer": allow
    "oracle": allow
    "standardizer": allow
    "documenter": allow
    "explore": allow
```

- [ ] **Step 3: Verify**

Run:
```powershell
(Get-Content 'agents\orchestrator.md' -Raw | Select-String -Pattern ([char]0x2014)).Matches.Count
```
Expected: `0`. Also confirm both `standardizer: allow` and `documenter: allow` are present, and that step 8 (not 6) is the final report.

- [ ] **Step 4: Commit**

```bash
git add agents/orchestrator.md
git commit -m "feat(agents): add structure-review and documentation phases to orchestrator loop"
```

---

### Task 4: Update the slash-command entry points

**Files:**
- Modify: `commands/execute-plan.md` (End section)
- Modify: `commands/full-cycle.md` (step 4 prose)

**Interfaces:**
- Produces: the command docs match the orchestrator's new 8-step loop.

- [ ] **Step 1: Add the two new phases to `commands/execute-plan.md`**

Read `commands/execute-plan.md`. The current End section has steps 4 (graphify) and 5 (report). Renumber: insert two new steps for structure review and documentation, shift graphify to step 6 and the final report to step 7. Replace the current `End:` block (from the `End:` line through the final report bullet) with:

```markdown
End:
4. Structure review: dispatch the `standardizer` subagent against the branch diff. On findings, dispatch `executor` for the `quick-fix` items, then `reviewer` to re-check each. Two-strike failures escalate to `oracle`. `recommendation` items roll forward to the report.
5. Documentation: dispatch the `documenter` subagent with the run material (plan + spec paths, per-task commits, standardizer findings, verifier output, dispatch log). It writes `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-report.md`, updates every catalog/doc touched (README, AGENTS, commands sections), commits as docs commits, returns the report path.
6. If `graphify-out/graph.json` exists in the repo, run `graphify update .` (AST-only, no LLM, ~30 s) so the knowledge graph reflects the plan's changes. Non-blocking nicety: if the command is missing or fails, note it and move on.
7. Stop. Do NOT invoke `finishing-a-development-branch` or offer merge/PR unless the user asks. Instead report: branch name; commits with hashes and one-line descriptions; files changed with diff stats; verifier output (test counts, build/typecheck result); skills loaded across the run (name + one line on how each shaped the work); any `ponytail:` deferrals; anything Unverified; the Dispatch Log (each task as "dispatched: executor + reviewer" or "self-implemented", plus the standardizer and documenter dispatches); and the path to the report the documenter wrote.
```

- [ ] **Step 2: Update step 4 prose in `commands/full-cycle.md`**

Read `commands/full-cycle.md`. Replace the current step 4 sentence:
```
4. Execute (default): dispatch the `orchestrator` subagent with the spec and plan paths; it branches, runs executor/reviewer per task, escalates two-strike failures to `oracle`, commits at boundaries, and returns a final report. Relay that report.
```
with:
```
4. Execute (default): dispatch the `orchestrator` subagent with the spec and plan paths; it branches, runs executor/reviewer per task, escalates two-strike failures to `oracle`, then runs a structure review (`standardizer` plus quick-fix `executor` passes) and a documentation phase (`documenter` writes the execution report to `docs/artifacts/features/` and updates catalogs), commits at boundaries, and returns a final report. Relay that report.
```

- [ ] **Step 3: Verify no em-dashes in both files**

Run:
```powershell
Get-ChildItem commands\execute-plan.md,commands\full-cycle.md | ForEach-Object { $_.Name + ": " + (Get-Content $_.FullName -Raw | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count }
```
Expected: both `0`.

- [ ] **Step 4: Commit**

```bash
git add commands/execute-plan.md commands/full-cycle.md
git commit -m "docs(commands): document structure-review and documentation phases in execute-plan and full-cycle"
```

---

### Task 5: Update the agent catalogs

**Files:**
- Modify: `agents/README.md` (table + prose)
- Modify: `AGENTS.md` (agent-list prose)

**Interfaces:**
- Produces: both catalogs that list agents now include `standardizer` and `documenter`.

- [ ] **Step 1: Add two rows to `agents/README.md` `## The set` table**

Read `agents/README.md`. After the `oracle` row (the last data row of the table), add:

```markdown
| `standardizer` | subagent | `zai-coding-plan/glm-5.2` | Repo-wide standardization audit after a plan's task loop: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows. Returns findings tagged quick-fix or recommendation. Read-only. | edit/write/patch/task/webfetch tools; planning and review-workflow skills |
| `documenter` | subagent | `zai-coding-plan/glm-5.2` | Closes out a completed plan: writes the execution report to `docs/artifacts/features/`, updates every catalog/doc touched (README, AGENTS, commands sections), commits as docs. Write-scoped to docs/** + root markdown. | task/webfetch tools; planning and review-workflow skills; writes outside docs/** + root markdown |
```

- [ ] **Step 2: Update the `/execute-plan` prose paragraph in `agents/README.md`**

In the same file, replace:
```
`/full-cycle` runs as `planner`. `/execute-plan` (see `commands/execute-plan.md`) dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, two-strike failures to `oracle`, the command itself runs as `orchestrator`.
```
with:
```
`/full-cycle` runs as `planner`. `/execute-plan` (see `commands/execute-plan.md`) dispatches by name: implementer tasks to `executor`, reviews to `reviewer`, two-strike failures to `oracle`, post-implementation structure review to `standardizer`, and the documentation/report phase to `documenter`; the command itself runs as `orchestrator`.
```

- [ ] **Step 3: Update the agent list in `AGENTS.md`**

Read `AGENTS.md`. In the `### Agent definitions` section, replace:
```
Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `oracle`) and `inventree` (InvenTree inventory sessions via the homelab MCP) live in the top-level `agents/` directory.
```
with:
```
Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `standardizer`, `documenter`, `oracle`) and `inventree` (InvenTree inventory sessions via the homelab MCP) live in the top-level `agents/` directory.
```

Then, in the same section, replace:
```
They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult).
```
with:
```
They pair with `/full-cycle` (runs as `planner`; single-pass dispatches the `orchestrator` to execute in the same run) and `/execute-plan` (implementer tasks go to `executor`, reviews to `reviewer`, two-strike failures to the `oracle` consult, post-implementation structure review goes to `standardizer`, and the documentation/report phase goes to `documenter`).
```

- [ ] **Step 4: Verify no em-dashes**

Run:
```powershell
Get-ChildItem 'agents\README.md','AGENTS.md' | ForEach-Object { $_.Name + ": " + (Get-Content $_.FullName -Raw | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count }
```
Expected: both `0`.

- [ ] **Step 5: Commit**

```bash
git add agents/README.md AGENTS.md
git commit -m "docs(agents): add standardizer and documenter to roster catalogs"
```

---

### Task 6: Add the Reports section to `references/artifacts.md`

**Files:**
- Modify: `skills/rubens-project-standardization/references/artifacts.md`

**Interfaces:**
- Produces: the canonical artifacts doc now defines reports under `docs/artifacts/features/`.

- [ ] **Step 1: Read the file, then make four edits**

Read `skills/rubens-project-standardization/references/artifacts.md` in full. Apply these four edits:

Edit A, the H1 title (line 1):
```
# `docs/artifacts/`: specs, plans, reviews
```
to:
```
# `docs/artifacts/`: specs, plans, reviews, reports
```

Edit B, the intro paragraph (line 3):
```
The `docs/artifacts/` directory holds **process meta-documents**: the design specs, implementation plans, and reviews that describe *how* the project is built: not the project's own deliverables.
```
to:
```
The `docs/artifacts/` directory holds **process meta-documents**: the design specs, implementation plans, reviews, and execution reports that describe *how* the project is built: not the project's own deliverables.
```

Edit C, add a new `## Reports` section. Place it immediately after the existing `## Reviews: docs/artifacts/reviews/` section (before the next `##` heading, which is the per-framework redirect section). Insert:
```markdown
## Reports: `docs/artifacts/features/`

Execution reports close out a completed plan: what the plan set out, what shipped, the standardization review, the documentation updates, verifier output, and the dispatch log. They are the persisted artefact the orchestrator's `documenter` subagent writes at the end of `/execute-plan` and `/full-cycle` runs.

```
docs/artifacts/features/code-standardization/2026-08-05-execution-report.md
```

Reports are written by the documenter from the run's git state and the orchestrator's dispatch log; they are not authored by hand during normal development. Layout follows the repo's specs/plans layout (flat by default, topic-subfoldered for multi-plan or grouped topics).

- An execution report belongs with the plan it closes out. If the plan lives under `docs/artifacts/features/<topic>/`, the report lives alongside it under `docs/artifacts/features/<topic>/` with the same date and slug.
- Do not hand-write a report for work that has no plan. Reports document executed plans, not ad-hoc changes.
```

Edit D, the per-framework redirect table and summary. Update every target-column cell and summary line that references the brace set so `{specs,plans,reviews}` becomes `{specs,plans,reviews,reports}`. In particular the `Any other framework` row target cell becomes `docs/artifacts/{specs,plans,reviews,reports}/`, and the summary line near the redirect section that says `Redirect every spec, plan, and review to docs/artifacts/{specs,plans,reviews}/` becomes `Redirect every spec, plan, review, and report to docs/artifacts/{specs,plans,reviews,reports}/`. Rows that name a single kind (a superpowers-specs row pointing only at `docs/artifacts/features/...`) stay as-is (paths migrated to per-feature layout on 2026-08-05; final form is `docs/artifacts/{features,reviews}/`).

- [ ] **Step 2: Add report production to the default-workflow list**

In the same file, the workflow list (the numbered sequence ending with the review item) gets one more item after the review item:
```
7. **Document and report** (the documenter subagent at the end of `/execute-plan` or `/full-cycle`) -> writes an execution report to `docs/artifacts/features/` and updates catalogs.
```

- [ ] **Step 3: Verify no em-dashes and the section is present**

Run:
```powershell
$f='skills\rubens-project-standardization\references\artifacts.md'; (Get-Content $f -Raw | Select-String -Pattern ([char]0x2014)).Matches.Count; (Get-Content $f -Raw | Select-String -Pattern '## Reports').Matches.Count
```
Expected: `0` then `1`.

- [ ] **Step 4: Commit**

```bash
git add skills/rubens-project-standardization/references/artifacts.md
git commit -m "docs(skills): add reports artifact to project-standardization references/artifacts.md"
```

---

### Task 7: Add reports to the scaffolded set in bootstrap and STANDARDS

**Files:**
- Modify: `skills/rubens-project-standardization/references/bootstrap.md`
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md`

**Interfaces:**
- Produces: the scaffolded set is `{features,reviews}` in both the bootstrap procedure and the STANDARDS template.

- [ ] **Step 1: Update `references/bootstrap.md` step 6**

Read `references/bootstrap.md`. In step 6 (the `Scaffold docs/artifacts/` step), replace:
```
create `specs/`, `plans/`, `reviews/` per `references/artifacts.md`
```
with:
```
create `features/`, `reviews/` per `references/artifacts.md`
```

- [ ] **Step 2: Update `templates/STANDARDS.md`**

Read `templates/STANDARDS.md`. In the `docs/artifacts/` list (around the features/reviews bullets), after the reviews bullet:
```
- `docs/artifacts/reviews/YYYY-MM-DD-<topic>-review.md`: audits and reviews.
```
add:
```
- `docs/artifacts/features/YYYY-MM-DD-<topic>-report.md`: execution reports for completed plans.
```

- [ ] **Step 3: Verify no em-dashes**

Run:
```powershell
Get-ChildItem 'skills\rubens-project-standardization\references\bootstrap.md','skills\rubens-project-standardization\templates\STANDARDS.md' | ForEach-Object { $_.Name + ": " + (Get-Content $_.FullName -Raw | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count }
```
Expected: both `0`.

- [ ] **Step 4: Commit**

```bash
git add skills/rubens-project-standardization/references/bootstrap.md skills/rubens-project-standardization/templates/STANDARDS.md
git commit -m "docs(skills): add reports to scaffolded docs/artifacts set in bootstrap and STANDARDS"
```

---

### Task 8: Add reports to the three AGENTS templates

**Files:**
- Modify: `skills/rubens-project-standardization/templates/AGENTS-small.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-medium.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-large.md`

**Interfaces:**
- Produces: all three tier templates reference `{specs,plans,reviews,reports}`.

- [ ] **Step 1: In each of the three template files, update the artifacts line**

Read each file. In each, find the line:
```
Specs, plans, and reviews live in `docs/artifacts/{specs,plans,reviews}/` (filename: `YYYY-MM-DD-<topic>-<type>.md`).
```
and replace with:
```
Specs, plans, reviews, and reports live in `docs/artifacts/{specs,plans,reviews,reports}/` (filename: `YYYY-MM-DD-<topic>-<type>.md`).
```

- [ ] **Step 2: Verify**

Run:
```powershell
Get-ChildItem 'skills\rubens-project-standardization\templates\AGENTS-*.md' | ForEach-Object { $_.Name + ": reports=" + ((Get-Content $_.FullName -Raw) -match 'reports') + " em=" + (Get-Content $_.FullName -Raw | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count }
```
Expected: each line shows `reports=True em=0`.

- [ ] **Step 3: Commit**

```bash
git add skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md
git commit -m "docs(skills): add reports to docs/artifacts set in all three AGENTS tier templates"
```

---

### Task 9: Add reports to tier references, SKILL.md body, and memory

**Files:**
- Modify: `skills/rubens-project-standardization/references/small.md`
- Modify: `skills/rubens-project-standardization/references/medium.md`
- Modify: `skills/rubens-project-standardization/references/large.md`
- Modify: `skills/rubens-project-standardization/SKILL.md`
- Modify: `skills/rubens-project-standardization/references/memory.md`

**Interfaces:**
- Produces: every `{specs,plans,reviews}` mention in the standardization skill now includes `reports`.

- [ ] **Step 1: `references/small.md`**

Read the file. Update the `{specs,plans,reviews}` brace mentions (line ~7 and the surrounding text) to include `reports`:
- `docs/artifacts/{specs,plans,reviews}/` -> `docs/artifacts/{specs,plans,reviews,reports}/`
- Where the prose says "a spec, plan, or review", extend to "a spec, plan, review, or report".
- The "Creating `docs/artifacts/{specs,plans,reviews}/` empty" anti-pattern line -> `docs/artifacts/{specs,plans,reviews,reports}/`.

- [ ] **Step 2: `references/medium.md`**

Read the file. In the "When to add `docs/artifacts/`" section (line ~134-136):
- `Create `docs/artifacts/{specs,plans,reviews}/` the first time any of these become true:` -> `Create `docs/artifacts/{specs,plans,reviews,reports}/` the first time any of these become true:`
- Any other `{specs,plans,reviews}` brace in this file -> add `reports`.

- [ ] **Step 3: `references/large.md`**

Read the file. Update:
- The `docs/artifacts/` table row (line ~89): `Process meta: brainstorming specs, implementation plans, repo / sprint / process reviews.` -> add `and execution reports.` before the period.
- Any `{specs,plans,reviews}` brace -> add `reports`.

- [ ] **Step 4: `SKILL.md` body and description**

Read `SKILL.md`. Update:
- Body reference (around line 41): `docs/artifacts/{specs,plans,reviews}/` -> `docs/artifacts/{specs,plans,reviews,reports}/`.
- Body line ~116 if it references the brace set: add `reports`.
- Frontmatter `description` (line 3): the phrase "setup `docs/artifacts/` for specs/plans/reviews from any framework" -> "setup `docs/artifacts/` for specs/plans/reviews/reports from any framework".

IMPORTANT: this frontmatter `description` change is in-scope (it names the artifact kinds the skill scaffolds). Keep the `description` starting with "Use when..." and under 1024 chars total; only the inline list of artifact kinds changes.

- [ ] **Step 5: `references/memory.md`**

Read the file. After the existing lines:
```
- **Plans**: committed implementation steps with checkpoints. Lives in `docs/artifacts/features/`.
- **Specs**: committed design rationale. Lives in `docs/artifacts/features/`.
```
add:
```
- **Reports**: committed execution history for a completed plan (what shipped, standardization review, dispatch log). Lives in `docs/artifacts/features/`. Not memory: memory is cross-session context, reports are a single plan's record.
```

- [ ] **Step 6: Verify no em-dashes across all five files**

Run:
```powershell
Get-ChildItem 'skills\rubens-project-standardization\references\small.md','skills\rubens-project-standardization\references\medium.md','skills\rubens-project-standardization\references\large.md','skills\rubens-project-standardization\SKILL.md','skills\rubens-project-standardization\references\memory.md' | ForEach-Object { $_.Name + ": em=" + (Get-Content $_.FullName -Raw | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count }
```
Expected: all `em=0`.

- [ ] **Step 7: Commit**

```bash
git add skills/rubens-project-standardization/references/small.md skills/rubens-project-standardization/references/medium.md skills/rubens-project-standardization/references/large.md skills/rubens-project-standardization/SKILL.md skills/rubens-project-standardization/references/memory.md
git commit -m "docs(skills): add reports artifact across project-standardization tier refs, SKILL.md, memory"
```

---

### Task 10: Whole-feature verification

**Files:** none modified (verification only).

- [ ] **Step 1: Agent frontmatter parses**

Run (if `opencode` is on PATH):
```bash
opencode agent list
```
Expected: `standardizer` and `documenter` appear; no parse errors for any agent. If `opencode` is not on PATH, note as Unverified and fall back to a frontmatter-delimiter check (`---` opens and closes, `description:`/`mode:`/`model:` present) on `agents\standardizer.md` and `agents\documenter.md`.

- [ ] **Step 2: No leftover unreported `{specs,plans,reviews}` braces in the standardization skill**

Run:
```powershell
Get-ChildItem 'skills\rubens-project-standardization' -Recurse -Include *.md | Select-String -Pattern '\{specs,plans,reviews\}' | Select-Object Path, LineNumber, Line
```
Expected: no matches. Every brace set should now be `{specs,plans,reviews,reports}`. If any `{specs,plans,reviews}` remains, fix it before finishing.

- [ ] **Step 3: No em-dashes in any changed file**

Run:
```powershell
git diff --name-only main..HEAD | Where-Object { $_ -match '\.md$' } | ForEach-Object { if ((Get-Content $_ -Raw -ErrorAction SilentlyContinue | Select-String -Pattern ([char]0x2014) -AllMatches).Matches.Count) { "EM: $_" } }
```
Expected: no output (no em-dashes in any changed markdown file).

- [ ] **Step 4: Both new agents are in both catalogs**

Confirm `standardizer` and `documenter` each appear in: `agents/README.md` (the table) AND `AGENTS.md` (the agent-list prose). A roster entry missing from one catalog is a process failure.

Run:
```powershell
foreach ($a in 'standardizer','documenter') { foreach ($c in 'agents\README.md','AGENTS.md') { "$a in $c : " + ((Get-Content $c -Raw) -match [regex]::Escape($a)) } }
```
Expected: all four `True`.

- [ ] **Step 5: Report the verification results**

Report which checks passed, which were Unverified (e.g. `opencode agent list` if the CLI is unavailable), and any fixes applied during verification. No commit unless a fix was applied (then commit with `fix(...)` matching the file's scope).
