# Standardizer Split Implementation Plan

> **For agentic workers:** This plan is executed by the `orchestrator` agent per the `/execute-plan` conventions: branch first, one `executor` + `reviewer` pair per task, per-task Conventional Commits, `oracle` consult on two-strike failures, structure review and documentation phase at the end. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the `standardizer` agent into `doc-standardizer` (repo/docs conventions) and `code-standardizer` (code structure), run sequentially in all plan flows.

**Architecture:** `git mv` the existing agent file and trim it to the repo/docs half; add a new agent file carrying the code half with the same frontmatter scaffold. Update every live reference (flow files, skills, catalogs, workflow docs, diagrams) so no standalone `standardizer` mention survives. No code, no tooling; markdown and drawio XML only.

**Tech Stack:** Markdown, opencode agent frontmatter (YAML), drawio XML, git, ripgrep, PowerShell 5.1.

**Spec:** `docs/artifacts/features/standardizer-split/2026-08-29-standardizer-split-design.md`

## Global Constraints

- Names are exactly `doc-standardizer` and `code-standardizer` (lowercase, hyphenated) everywhere.
- No em-dashes (U+2014) in any edited or created file.
- Conventional Commits 1.0.0; the commit-msg hook is active (`git config core.hooksPath .githooks` if not).
- Never edit `docs/artifacts/**` (immutable history) or existing `CHANGELOG.md` entries.
- Agent frontmatter rules (from `agents/README.md`): keep both `tools:` and the matching `permission:` denies; inside a patterned permission object the broad rule (`"*"`) comes FIRST, narrow entries LAST; every agent denies `homelab*`.
- The two new agents deny each other's skill: `doc-standardizer` denies `code-standardization`, `code-standardizer` denies `project-standardization` (the skill's frontmatter `name`, not the folder name).
- Branch: `feat/standardizer-split` off `main`.
- Read every file before editing it. Line numbers below are anchors from recon on 2026-08-29; trust the file, not the line number.

---

### Task 1: Branch, split the agent files, update rosters and changelog

**Files:**
- Rename: `agents/standardizer.md` -> `agents/doc-standardizer.md` (use `git mv`)
- Create: `agents/code-standardizer.md`
- Modify: `agents/README.md` (roster table row at ~L16, prose at ~L19)
- Modify: `AGENTS.md` (agent-definitions paragraph at ~L101)
- Modify: `CHANGELOG.md` (new entry only)

**Interfaces:**
- Produces: agent ids `doc-standardizer` and `code-standardizer` that Task 2 names in dispatch flows and Tasks 3-5 reference in prose.

- [ ] **Step 1: Commit the spec and plan, then branch**

```powershell
git status   ;# confirm clean or stash unrelated work
git checkout -b feat/standardizer-split
git add docs/artifacts/features/standardizer-split/
git commit -m "docs: add standardizer-split spec and plan"
```

- [ ] **Step 2: Rename the agent file with history**

```powershell
git mv agents/standardizer.md agents/doc-standardizer.md
```

- [ ] **Step 3: Trim doc-standardizer.md to the repo/docs half**

Three edits to `agents/doc-standardizer.md`:

a) Replace the frontmatter `description` value with (drops the "Also loads code-standardization..." sentence, keeps the versioning clause):

```
Reviews the executed branch (or whole repo when the diff is structural) against the project-standardization skill: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows, Conventional Commit hygiene, version-source sync and SemVer 2.0.0 policy presence (shipped-software projects). Dispatch after a plan's task loop completes, before documentation. Returns PASS or numbered findings tagged quick-fix or recommendation. Read-only; does not edit or dispatch.
```

b) In the `permission.skill` deny list, add one line after `"synctool-sync": deny`:

```
    "code-standardization": deny
```

c) In the body: change the opening `You are the standardizer:` to `You are the doc-standardizer:`, keep paragraphs 1-3 (the project-standardization audit and the versioning policy paragraph) unchanged, and delete the entire paragraph starting `Then load \`code-standardization\`; for each language in the diff run the four checks...`. Everything from that `Then load` up to (but not including) the final `Return short actionable findings` paragraph goes.

- [ ] **Step 4: Create agents/code-standardizer.md**

Full file content:

```markdown
---
description: Reviews the executed branch diff (or a whole repo when the diff is structural) against the code-standardization skill: formatter/linter config presence, per-language naming and module-organization rules, architecture boundary adherence. Dispatch after a plan's task loop completes, after the doc-standardizer pass. Returns PASS or numbered findings tagged quick-fix or recommendation. Read-only; does not edit or dispatch.
mode: subagent
color: info
model: zai-coding-plan/glm-5.3
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
    "project-standardization": deny
---

You are the code-standardizer: you audit the executed branch diff (or the whole repo when the diff is structural) against the `code-standardization` skill. You are read-only plus bash for git state and the skill's checks; you do not edit, write, or dispatch.

Load `code-standardization`. Determine the languages present in the branch diff (`git diff <base>..HEAD --name-only`). For each language, run the four checks (presence, documentation, consistency, boundaries) using `references/<lang>.md`. Run the pinned formatter/linter in check mode if installed (`command -v <tool>`), otherwise emit a quick-fix finding naming the tool and the config file to add. Never re-lint source code in your own body.

Return short actionable findings, not a redesign. Format: PASS, or a numbered list where each item names the file/path, the rule violated, the specific fix, and a tag:
- `quick-fix`: a mechanical correction (add a config file, rename an identifier to the naming rule, wire a missing check). The orchestrator dispatches an executor for these.
- `recommendation`: a larger change (introduce an architecture boundary, restructure modules) that is not auto-fixed and rolls forward into the execution report.

Do not re-implement. Do not fix anything yourself. Do not audit repo conventions (AGENTS.md sections, changelog, catalog rows, paths); the doc-standardizer covers those.
```

- [ ] **Step 5: Update the agents/README.md roster**

Replace the single `standardizer` row with two rows (keep table column order: Agent | Mode | Model | Role | Denied):

```markdown
| `doc-standardizer` | subagent | `zai-coding-plan/glm-5.3` | Repo/docs standardization audit after a plan's task loop: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows, commit hygiene, versioning sync. Loads `project-standardization`. Returns findings tagged quick-fix or recommendation. Read-only. | edit/write/patch/task/webfetch tools; planning and review-workflow skills; `code-standardization` |
| `code-standardizer` | subagent | `zai-coding-plan/glm-5.3` | Code-structure audit after the doc-standardizer pass: formatter/linter config presence, per-language naming and module organization, architecture boundaries. Loads `code-standardization`. Returns findings tagged quick-fix or recommendation. Read-only. | edit/write/patch/task/webfetch tools; planning and review-workflow skills; `project-standardization` |
```

In the prose paragraph below the table (~L19), change `post-implementation structure review to \`standardizer\`` to `post-implementation structure review to \`doc-standardizer\` then \`code-standardizer\``.

- [ ] **Step 6: Update the AGENTS.md agent roster paragraph**

In the `### Agent definitions` section (~L101): in the agent name list, replace `standardizer` with `doc-standardizer`, `code-standardizer`; change `post-implementation structure review goes to \`standardizer\`` to `goes to \`doc-standardizer\` then \`code-standardizer\``.

- [ ] **Step 7: Add the CHANGELOG entry**

Read `CHANGELOG.md`, follow its current top-section convention (Keep a Changelog; likely an `## [Unreleased]` or dated section). Add under an appropriate `### Changed` (or the file's equivalent):

```markdown
- Split the `standardizer` agent into `doc-standardizer` (repo/docs conventions, loads `project-standardization`) and `code-standardizer` (code structure, loads `code-standardization`); plan flows now run both audits sequentially with one combined quick-fix executor pass.
```

- [ ] **Step 8: Validate the agent files parse and resolve**

```powershell
Copy-Item agents\doc-standardizer.md, agents\code-standardizer.md "$env:USERPROFILE\.config\opencode\agents\"
if (Test-Path "$env:USERPROFILE\.config\opencode\agents\standardizer.md") { Remove-Item "$env:USERPROFILE\.config\opencode\agents\standardizer.md" }
opencode agent list
opencode debug agent doc-standardizer
opencode debug agent code-standardizer
git log --follow --oneline agents/doc-standardizer.md
```

Expected: `agent list` shows both new names and no `standardizer`; both `debug agent` calls resolve (mode subagent, model pin, skill denies); `--follow` shows commits predating the rename.

- [ ] **Step 9: Commit**

```powershell
git add agents/ AGENTS.md CHANGELOG.md
git commit -m "feat(agents): split standardizer into doc-standardizer and code-standardizer"
```

---

### Task 2: Wire the sequential dispatch into the plan flows

**Files:**
- Modify: `agents/orchestrator.md` (task allowlist ~L21, steps 6/8/9 at ~L47-50)
- Modify: `commands/execute-plan.md` (steps 4/5/7 at ~L22-25)
- Modify: `commands/full-cycle.md` (step 4 at ~L15)
- Modify: `agents/documenter.md` (~L47 and ~L50)

**Interfaces:**
- Consumes: agent ids from Task 1.
- Produces: the sequential chain doc-standardizer -> code-standardizer -> one executor quick-fix pass -> one reviewer recheck, named identically in both flow definitions.

- [ ] **Step 1: Update agents/orchestrator.md**

a) In the `permission.task` allowlist, replace the `"standardizer": allow` entry with two entries (keep the existing broad-rule-first ordering of the block):

```yaml
    "doc-standardizer": allow
    "code-standardizer": allow
```

b) Step 6 (structure review) becomes:

```markdown
Structure review (after the task loop is complete): dispatch the `doc-standardizer` subagent against the branch diff, then the `code-standardizer` subagent against the same diff. On findings from either: dispatch `executor` once for all items tagged `quick-fix` (kebab-case paths, missing AGENTS sections, changelog gaps, catalog rows, formatter/linter config gaps), then `reviewer` to re-check each fix.
```

c) Step 8: change `standardizer findings and what was fixed` to `doc-standardizer and code-standardizer findings and what was fixed`.

d) Step 9: change `plus the standardizer and documenter dispatches` to `plus the doc-standardizer, code-standardizer, and documenter dispatches`.

- [ ] **Step 2: Update commands/execute-plan.md**

a) Step 4 (structure review) becomes:

```markdown
Structure review: dispatch the `doc-standardizer` subagent against the branch diff, then `code-standardizer` against the same diff. On findings from either, dispatch `executor` once for all `quick-fix` items, then `reviewer` to re-check each.
```

b) Step 5: change `standardizer findings` to `doc-standardizer and code-standardizer findings`.

c) Step 7: change `plus the standardizer and documenter dispatches` to `plus the doc-standardizer, code-standardizer, and documenter dispatches`.

- [ ] **Step 3: Update commands/full-cycle.md**

Step 4: change ``(`standardizer` plus quick-fix `executor` passes)`` to ``(`doc-standardizer` then `code-standardizer`, plus quick-fix `executor` passes)``.

- [ ] **Step 4: Update agents/documenter.md**

a) In the inputs list: change `the standardizer's findings and which were fixed vs which remain as recommendations` to `the doc-standardizer's and code-standardizer's findings and which were fixed vs which remain as recommendations`.

b) In step 1: change `Read the standardizer's findings.` to `Read the findings from both audits.` (avoid the bare word `standardizers`; the final orphan scan in Task 6 flags any unprefixed form).

- [ ] **Step 5: Verify no orphaned mentions in the flow files**

```powershell
rg -i -n "standardizer" agents\orchestrator.md agents\documenter.md commands\execute-plan.md commands\full-cycle.md
```

Expected: every hit contains `doc-standardizer` or `code-standardizer`.

- [ ] **Step 6: Commit**

```powershell
git add agents\orchestrator.md agents\documenter.md commands\execute-plan.md commands\full-cycle.md
git commit -m "docs: dispatch doc-standardizer then code-standardizer in plan flows"
```

---

### Task 3: Point the code-standardization skill at code-standardizer

**Files:**
- Modify: `skills/code-standardization/SKILL.md` (description tail ~L3, body ~L10, heading ~L40, body ~L42)
- Modify: `skills/code-standardization/references/python.md`, `go.md`, `rust.md`, `typescript-javascript.md`, `c-cpp.md`, `architecture.md`, `tooling.md` (~74 mentions total)

**Interfaces:**
- Consumes: agent id `code-standardizer` from Task 1.
- Produces: the skill and all its references reference only `code-standardizer`.

- [ ] **Step 1: Update SKILL.md**

a) Description tail: `Pairs with the \`standardizer\` agent for post-plan code audits.` -> `Pairs with the \`code-standardizer\` agent for post-plan code audits.`

b) In the overview (~L10), replace the sentence naming the `standardizer` agent and its merged pass with: `The \`code-standardizer\` agent runs the code-structure audit; the \`doc-standardizer\` agent covers repo conventions.`

c) Heading ~L40: `## How the standardizer uses this skill` -> `## How the code-standardizer uses this skill`.

d) Body ~L42: replace `The \`standardizer\` agent loads **both** \`project-standardization\` and \`code-standardization\`, then runs a **merged audit pass** in the same invocation:` with `The \`code-standardizer\` agent loads \`code-standardization\` and runs the code-structure audit:`. Adjust the following lines if they continue the merged-pass wording.

- [ ] **Step 2: Sweep the references directory**

In every file under `skills/code-standardization/references/`, replace each occurrence of `Standardizer check:` with `code-standardizer check:` and every other standalone `standardizer` / `Standardizer` mention with `code-standardizer` (agent ids stay lowercase). Files and expected match counts from recon: python.md (14), go.md (17), rust.md (13), typescript-javascript.md (13), c-cpp.md (11), architecture.md (4), tooling.md (2). Then also update `commands/standardize-code.md` line ~L17: `same format as the \`standardizer\` agent` -> `same format as the \`code-standardizer\` agent`.

- [ ] **Step 3: Verify**

```powershell
rg -i -n "standardizer" skills\code-standardization commands\standardize-code.md
```

Expected: every hit contains `doc-standardizer` or `code-standardizer` (most likely zero doc- hits; a doc- mention is fine only if the sentence contrasts the two agents).

- [ ] **Step 4: Commit**

```powershell
git add skills\code-standardization commands\standardize-code.md
git commit -m "docs(skills): point code-standardization at the code-standardizer agent"
```

---

### Task 4: Repo-side reference sweep

**Files:**
- Modify: `skills/rubens-project-standardization/references/versioning.md` (~L72-74)
- Modify: `README.md` (agent list at ~L24)
- Modify: `opencode-install.md` (agent copy step ~L126, `## Verify` list ~L152)

**Interfaces:**
- Consumes: agent ids from Task 1.

- [ ] **Step 1: Update versioning.md**

Heading ~L72: `## The 3 standardizer checks` -> `## The 3 doc-standardizer checks`. Body ~L74: `the standardizer audits three things` -> `the doc-standardizer audits three things`. Grep the whole file for any other `standardizer` mention and map it to `doc-standardizer` (versioning is a repo-side concern).

- [ ] **Step 2: Update README.md**

Find the sentence at ~L24 that enumerates the agent set (currently stale: names only `orchestrator`, `executor`, `reviewer`, `inventree`). Replace the enumeration with a pointer, e.g.:

```markdown
Custom opencode agents (planner, orchestrator, writer, executor, reviewer, doc-standardizer, code-standardizer, documenter, oracle; see `agents/README.md` for the roster) live in the top-level `agents/` directory.
```

Adapt the wording to the surrounding sentence; the requirement is: no stale enumeration, `agents/README.md` named as the roster source.

- [ ] **Step 3: Update opencode-install.md**

In step 9 (copy skills/commands/agents), the agent copy sub-step (~L126) and the `## Verify` section (~L152) name only `orchestrator`, `executor`, `reviewer`. Update both to name the full current set: `planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `doc-standardizer`, `code-standardizer`, `documenter`, `oracle` (plus `inventree` if the machine uses the homelab MCP). Keep the surrounding instructions unchanged. Do not add frontmatter to this file.

- [ ] **Step 4: Verify**

```powershell
rg -i -n "standardizer" skills\rubens-project-standardization\references\versioning.md README.md opencode-install.md
```

Expected: every hit contains `doc-standardizer` or `code-standardizer`.

- [ ] **Step 5: Commit**

```powershell
git add skills\rubens-project-standardization\references\versioning.md README.md opencode-install.md
git commit -m "docs: finish repo-side reference sweep for the standardizer split"
```

---

### Task 5: Workflow doc and diagrams

**Files:**
- Modify: `docs/workflows/workflow.md` (~L11, L35, L93, L96, L116)
- Modify: `docs/workflows/plan-flow.drawio` (node ~L67, edges ~L178-190)
- Modify: `docs/workflows/stack.drawio` (node ~L103)
- Modify: `docs/workflows/multi-plan-flow.drawio` (legend ~L82)

**Interfaces:**
- Consumes: agent ids from Task 1; the sequential chain from Task 2.

- [ ] **Step 1: Update workflow.md**

a) ~L11 model table: replace `standardizer` in the long-horizon reasoning list with `doc-standardizer`, `code-standardizer`.

b) ~L35 skills table, `code-standardization` row: `Pairs with \`standardizer\` agent.` -> `Pairs with \`code-standardizer\` agent.`

c) ~L93 agent roster table: replace the single `standardizer` row with two rows matching the agents/README.md roster (condensed to the table's existing column style).

d) ~L96: `post-implementation structure review to \`standardizer\`` -> `post-implementation structure review to \`doc-standardizer\` then \`code-standardizer\``.

e) ~L116 loop description: replace the merged-pass wording with `doc-standardizer then code-standardizer structure review (repo structure first, then code structure) with quick-fix \`executor\` passes`, keeping the sentence's surrounding structure.

- [ ] **Step 2: Update plan-flow.drawio**

a) Node `nStandardizer` (~L67, label starts `Standardizer (glm-5.3) Merged audit pass:`): rename the node id to `nDocStandardizer` and relabel it to cover only the repo half, e.g. `doc-standardizer (glm-5.3) Repo audit: - kebab-case paths - AGENTS.md sections - docs/artifacts - catalogs, changelog`. Keep the existing style/geometry.

b) Add a sibling node `nCodeStandardizer` after it (same style, position it between the doc node and the documenter node, adjusting geometry minimally so edges do not overlap), label: `code-standardizer (glm-5.3) Code audit: - formatter/linter presence - naming and module rules - architecture boundaries`.

c) Edges: retarget the loop-to-standardizer edge (~L178, `e_m7no`) to `nDocStandardizer`; change the standardizer-to-documenter edge (`e_stdDoc`) to run `nDocStandardizer` -> `nCodeStandardizer`; add one new edge `nCodeStandardizer` -> documenter node (id `e_codeDoc`, copy the edge style of `e_stdDoc`).

d) Legend (~L190): replace the standardizer legend text with `doc-standardizer loads project-standardization; code-standardizer loads code-standardization; two sequential audit passes cover repo + code`.

- [ ] **Step 3: Update stack.drawio**

Relabel node `aStandardizer` (~L103) to `doc-standardizer (subagent) glm-5.3 - repo structure review (post-loop)` and add a sibling node in the same style labeled `code-standardizer (subagent) glm-5.3 - code structure review (post-loop)`, positioned next to it.

- [ ] **Step 4: Update multi-plan-flow.drawio**

Legend ~L82: `then standardizer structure review` -> `then doc-standardizer and code-standardizer structure reviews`.

- [ ] **Step 5: Verify**

```powershell
rg -i -n "standardizer" docs\workflows
```

Expected: every hit contains `doc-standardizer` or `code-standardizer`.

- [ ] **Step 6: Commit**

```powershell
git add docs\workflows
git commit -m "docs(workflows): show both standardizers in flow diagrams"
```

---

### Task 6: Final verification (no commit unless it finds issues)

**Files:** none modified (verification only).

- [ ] **Step 1: Whole-repo orphan scan**

```powershell
rg -i -n "standardizer" -g "!docs/artifacts/**" -g "!CHANGELOG.md" | rg -i -v "(doc|code)-standardizer"
```

Expected: empty output (no standalone `standardizer` in any live file; artifacts and changelog history excluded).

- [ ] **Step 2: Em-dash check on everything this branch touched**

```powershell
git diff --name-only main..HEAD | Where-Object { $_ -match '\.(md|drawio)$' -and (Test-Path $_) } | ForEach-Object { Select-String -Path $_ -Pattern ([char]0x2014) }
```

Expected: empty.

- [ ] **Step 3: Agent registration still valid**

```powershell
opencode agent list
```

Expected: `doc-standardizer` and `code-standardizer` listed, no `standardizer`.

- [ ] **Step 4: Working tree clean**

```powershell
git status
```

Expected: nothing to commit.

Then the orchestrator proceeds to its structure review (dispatching `doc-standardizer` then `code-standardizer`, which is also this split's first live dogfood), quick-fix pass, and the `documenter` phase per the usual flow.

---

## Self-review

- Spec coverage: agent files + rosters + changelog (Task 1), dispatch flow (Task 2), code-side sweep incl. standardize-code.md (Task 3), repo-side sweep incl. README.md + opencode-install.md (Task 4), workflow doc + 3 diagrams (Task 5), spec's verification list (Task 6). Out-of-scope files untouched. Covered.
- Placeholders: every step carries exact target text or a precise mapping rule with match counts; no TBDs.
- Consistency: agent ids, deny names (`project-standardization` is the skill's frontmatter name, not the folder name `rubens-project-standardization`), and the sequential chain wording are identical across tasks.
