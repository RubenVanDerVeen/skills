# Superpowers Fork Implementation Plan

> **For agentic workers:** Execute via `/execute-plan` conventions (`commands/execute-plan.md`): orchestrator dispatches executor + reviewer per task; parallel waves only where `**Files:**` are disjoint. **Tasks 1-5 are sequential** (all modify `README.md` and `AGENTS.md` catalog tables). **Task 7 must run last** (machine config; nothing may resolve a missing skill mid-run). Do not merge or push; leave the branch for user review.

**Goal:** Vendor the 5 superpowers process skills into this repo (tailored to repo conventions), update all live references, and remove the superpowers plugin from opencode.

**Architecture:** Pure markdown migration. Each vendored skill is copied from `~/.config/opencode/node_modules/superpowers/skills/<name>/`, rewritten to repo body rules (native artifact paths, batched questions, `## Overview`, no em-dashes), and ships with its catalog rows in the same commit (pre-commit hook enforces this). Live references drop the `superpowers:` namespace. Machine config (plugin removal, npm uninstall, skill sync) happens only after all repo work is committed.

**Tech Stack:** Markdown, git hooks (`.githooks/`), npm, PowerShell 5.1.

**Spec:** `docs/artifacts/features/superpowers-fork/2026-09-24-superpowers-fork-design.md`

**Versioning:** No `### Versioning` subsection in this repo's AGENTS.md. Unversioned, no bump.

## Global Constraints

- Skill names stay exactly: `brainstorming`, `writing-plans`, `using-git-worktrees`, `systematic-debugging`, `writing-skills`. Folder name = frontmatter `name`.
- Every vendored `SKILL.md` carries this credit line near the top of the body: `Adapted from obra/superpowers (MIT).`
- Frontmatter: `description` starts with "Use when...", under 1024 chars total, no em-dashes (U+2014) anywhere.
- Body starts with `## Overview`. No top-level `## Skill` heading.
- Catalog rows for a new skill land in the same commit as the skill (hook rejects otherwise).
- Commit messages: Conventional Commits, `feat(skills):` for vendored skills, `docs(skills):` for reference updates, `docs:` for the report.
- Never touch `docs/artifacts/**` history; never edit deny lists in `agents/*.md`.
- Source of all vendored content: `C:\Users\ruben\.config\opencode\node_modules\superpowers\skills\<name>\SKILL.md` (plus subdirs). It exists until Task 7; copy before then.
- Branch: `feat/superpowers-fork` off current HEAD.

---

### Task 1: Branch + vendor brainstorming

**Files:**
- Create: `skills/brainstorming/SKILL.md`
- Modify: `README.md` (Skills table), `AGENTS.md` (Current skills table)

**Interfaces:**
- Produces: local skill `brainstorming` with native spec path `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md`; Tasks 2, 6 reference it by bare name.

- [ ] **Step 1: Create branch**

Run: `git checkout -b feat/superpowers-fork`
Expected: `Switched to a new branch 'feat/superpowers-fork'`

- [ ] **Step 2: Copy source, drop dead weight**

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.config\opencode\node_modules\superpowers\skills\brainstorming" "skills\brainstorming"
Remove-Item -Recurse "skills\brainstorming\scripts"
Remove-Item "skills\brainstorming\visual-companion.md", "skills\brainstorming\spec-document-reviewer-prompt.md"
```

Expected: only `skills/brainstorming/SKILL.md` remains.

- [ ] **Step 3: Rewrite SKILL.md per spec**

Write frontmatter exactly:

```markdown
---
name: brainstorming
description: Use when doing any creative work before implementation - creating features, building components, adding functionality, or modifying behavior. Explores intent, requirements, and design before any code is written.
---
```

Body edits (keep the source's substance, apply these changes):
1. Start body with `## Overview` + the credit line `Adapted from obra/superpowers (MIT).`
2. Spec output path is native: `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md`. Delete the `docs/superpowers/specs/` default and the "user preferences override" clause (no longer an override, it is the rule). Keep the commit-the-spec step.
3. Replace "only one question per message" with: batch all clarifying questions into one message, multiple-choice sets preferred; proceed on defaults if the user defers.
4. Keep: HARD GATE (no implementation before design approval), explore context first, 2-3 approaches with a recommendation, terminal state = invoke `writing-plans`.
5. Delete: the entire Visual Companion section, the `elements-of-style` reference, the dot flowchart (checklist carries the flow).
6. Em-dash sweep: replace every U+2014 with a colon, comma, or hyphen.

- [ ] **Step 4: Verify em-dash free**

Run: `Get-ChildItem -Recurse -Include *.md skills\brainstorming | Select-String -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 5: Add catalog rows (same commit)**

`README.md` Skills table and `AGENTS.md` Current skills table, alphabetical position, adapting to each table's column order:
- folder `skills/brainstorming/`, name `brainstorming`, what it does: `Design-first gate for creative work. Batched questions, 2-3 approaches, spec at docs/artifacts/features/.`

- [ ] **Step 6: Commit**

```bash
git add skills/brainstorming README.md AGENTS.md
git commit -m "feat(skills): vendor brainstorming from superpowers, tailored to repo conventions"
```

Expected: pre-commit hook passes.

---

### Task 2: Vendor writing-plans

**Files:**
- Create: `skills/writing-plans/SKILL.md`
- Modify: `README.md`, `AGENTS.md`

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: local skill `writing-plans`; native plan path used by Task 6 wording updates.

- [ ] **Step 1: Copy source**

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.config\opencode\node_modules\superpowers\skills\writing-plans" "skills\writing-plans"
Remove-Item "skills\writing-plans\plan-document-reviewer-prompt.md"
```

Expected: only `skills/writing-plans/SKILL.md` remains.

- [ ] **Step 2: Rewrite SKILL.md per spec**

Frontmatter exactly:

```markdown
---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code.
---
```

Body edits:
1. `## Overview` start + credit line `Adapted from obra/superpowers (MIT).`
2. Plan path native: `docs/artifacts/features/<feature>/YYYY-MM-DD-<slug>-plan.md`; delete the `docs/superpowers/plans/` default and the override clause.
3. Delete the REQUIRED SUB-SKILL plan-header boilerplate and the subagent-driven-development / executing-plans handoff section. Replace with one line: `Execution: run /execute-plan (commands/execute-plan.md); the orchestrator agent dispatches executor + reviewer per task, parallel waves where **Files:** are disjoint.`
4. Keep: bite-sized task granularity, exact file paths, complete code in steps, no-placeholders list, per-task verification commands, self-review checklist.
5. Keep the `using-git-worktrees` reference (bare name).
6. Em-dash sweep.

- [ ] **Step 3: Verify em-dash free** (same command pattern, `skills\writing-plans`). Expected: no output.

- [ ] **Step 4: Catalog rows**: folder `skills/writing-plans/`, name `writing-plans`, what it does: `Turns an approved spec into bite-sized tasks with exact paths, steps, and verification commands.`

- [ ] **Step 5: Commit**

```bash
git add skills/writing-plans README.md AGENTS.md
git commit -m "feat(skills): vendor writing-plans from superpowers, native artifact paths"
```

---

### Task 3: Vendor using-git-worktrees

**Files:**
- Create: `skills/using-git-worktrees/SKILL.md`
- Modify: `README.md`, `AGENTS.md`

- [ ] **Step 1: Copy source**

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.config\opencode\node_modules\superpowers\skills\using-git-worktrees" "skills\using-git-worktrees"
```

- [ ] **Step 2: Rewrite SKILL.md per spec**

Frontmatter exactly:

```markdown
---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from the current workspace, or before executing implementation plans.
---
```

Body edits: `## Overview` start + credit line; keep the worktree mechanics and fallback logic as-is; trim repeated rationale paragraphs (one rationale, then mechanics); em-dash sweep. No path or flow changes.

- [ ] **Step 3: Verify em-dash free** (`skills\using-git-worktrees`). Expected: no output.

- [ ] **Step 4: Catalog rows**: folder `skills/using-git-worktrees/`, name `using-git-worktrees`, what it does: `Isolated worktree or plain branch before executing implementation plans.`

- [ ] **Step 5: Commit**

```bash
git add skills/using-git-worktrees README.md AGENTS.md
git commit -m "feat(skills): vendor using-git-worktrees from superpowers"
```

---

### Task 4: Vendor systematic-debugging

**Files:**
- Create: `skills/systematic-debugging/SKILL.md`, `skills/systematic-debugging/references/` (only if needed)
- Modify: `README.md`, `AGENTS.md`

- [ ] **Step 1: Copy source + disposition of side files**

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.config\opencode\node_modules\superpowers\skills\systematic-debugging" "skills\systematic-debugging"
New-Item -ItemType Directory "skills\systematic-debugging\references" | Out-Null
Move-Item "skills\systematic-debugging\root-cause-tracing.md","skills\systematic-debugging\defense-in-depth.md","skills\systematic-debugging\condition-based-waiting.md" "skills\systematic-debugging\references"
Remove-Item "skills\systematic-debugging\test-*.md","skills\systematic-debugging\CREATION-LOG.md","skills\systematic-debugging\*.ts","skills\systematic-debugging\*.sh" -ErrorAction SilentlyContinue
```

Expected: `SKILL.md` at the folder root; `references/` holding exactly `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`.

- [ ] **Step 2: Rewrite SKILL.md per spec**

Frontmatter exactly:

```markdown
---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---
```

Body edits: `## Overview` start + credit line; keep the core loop (read the error, form hypotheses, test the cheapest first, follow evidence not plausibility, root cause before fix); merge duplicated guidance; link the three `references/` files from the body where relevant; drop references to other superpowers skills by namespace (bare names or delete); em-dash sweep over `SKILL.md` **and every kept `references/` file**.

- [ ] **Step 3: Verify em-dash free** (`skills\systematic-debugging`). Expected: no output.

- [ ] **Step 4: Catalog rows**: folder `skills/systematic-debugging/`, name `systematic-debugging`, what it does: `Hypothesis-first debugging: cheapest test first, follow evidence, fix the root cause.`

- [ ] **Step 5: Commit**

```bash
git add skills/systematic-debugging README.md AGENTS.md
git commit -m "feat(skills): vendor systematic-debugging from superpowers"
```

---

### Task 5: Vendor writing-skills

**Files:**
- Create: `skills/writing-skills/SKILL.md`, `skills/writing-skills/references/anthropic-best-practices.md`, `skills/writing-skills/references/persuasion-principles.md`, `skills/writing-skills/references/testing-skills-with-subagents.md`
- Modify: `README.md`, `AGENTS.md`

**Interfaces:**
- Produces: local `writing-skills`; Task 6 updates the AGENTS.md pointer to reference it as local.

- [ ] **Step 1: Copy source + disposition of side files**

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.config\opencode\node_modules\superpowers\skills\writing-skills" "skills\writing-skills"
New-Item -ItemType Directory "skills\writing-skills\references" | Out-Null
Move-Item "skills\writing-skills\anthropic-best-practices.md","skills\writing-skills\persuasion-principles.md","skills\writing-skills\testing-skills-with-subagents.md" "skills\writing-skills\references"
Remove-Item -Recurse "skills\writing-skills\examples"
Remove-Item "skills\writing-skills\graphviz-conventions.dot","skills\writing-skills\render-graphs.js" -ErrorAction SilentlyContinue
```

Expected: `SKILL.md` at the folder root; `references/` holding exactly the three moved `.md` files.

- [ ] **Step 2: Rewrite SKILL.md per spec**

Frontmatter exactly:

```markdown
---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment.
---
```

Body edits:
1. `## Overview` start + credit line.
2. Keep the authoring method: frontmatter rules, description-as-trigger guidance, one-excellent-example, testing a skill before deployment.
3. The three kept reference files (`anthropic-best-practices.md`, `persuasion-principles.md`, `testing-skills-with-subagents.md`) stay under `references/`; the body links to them instead of inlining long material.
4. Where its frontmatter guidance conflicts with this repo's AGENTS.md (e.g. description format), note "in this repo, AGENTS.md rules win" once.
5. Trim ceremony; target body under ~2000 words; em-dash sweep over `SKILL.md` and the three `references/` files.

- [ ] **Step 3: Verify em-dash free** (`skills\writing-skills`). Expected: no output.

- [ ] **Step 4: Catalog rows**: folder `skills/writing-skills/`, name `writing-skills`, what it does: `Meta-skill for authoring and editing skills: frontmatter, body structure, verify before deployment.`

- [ ] **Step 5: Commit**

```bash
git add skills/writing-skills README.md AGENTS.md
git commit -m "feat(skills): vendor writing-skills from superpowers, examples moved to references"
```

---

### Task 6: Update live references

**Files:**
- Modify: `skills/multi-plan-orchestration/SKILL.md` (lines ~71, ~145, ~153, ~200-201)
- Modify: `skills/rubens-project-standardization/references/artifacts.md` (lines ~196-205)
- Modify: `AGENTS.md` (delegation-path rule ~line 188; writing-skills pointer ~line 205)
- Modify: `opencode-install.md` (step 1 install section; verify section ~line 143)
- Modify: `external-skills.md` (superpowers entry ~lines 20-36)
- Modify: `README.md` (external-skills bullet ~line 32; quick-install URL ~lines 46-47)
- Modify: `docs/workflows/workflow.md` (lines ~56-58, ~110)
- Modify: `docs/workflows/stack.drawio` (layer-2 label ~line 56)

**Interfaces:**
- Consumes: all 5 vendored skills from Tasks 1-5.

- [ ] **Step 1: multi-plan-orchestration edits**

1. `superpowers:brainstorming` to `brainstorming` (all occurrences).
2. `superpowers:using-git-worktrees` to `using-git-worktrees`.
3. The dispatch line `execute with superpowers:subagent-driven-development or executing-plans` becomes: `execute via /execute-plan (commands/execute-plan.md) with the orchestrator agent`.

- [ ] **Step 2: artifacts.md edit**

Update the "Pre-write override" wording: delegation now names local skills (`brainstorming`, `writing-plans`); the redirect table stays as documentation of framework defaults. Add one line: `Since 2026-09-24 the process skills are vendored in this repo and the paths above are native.`

- [ ] **Step 3: AGENTS.md edits**

1. Line ~188 delegation rule: reword from override framing to "the vendored `brainstorming` and `writing-plans` skills write to the canonical paths natively; if any framework default ever reappears, redirect to `docs/artifacts/features/`". Keep the forbidden-paths rule itself unchanged.
2. Line ~205: `The writing-skills skill (from superpowers)` becomes `The writing-skills skill (vendored in this repo)`.

- [ ] **Step 4: opencode-install.md edits**

1. Remove the "1. Superpowers" install step (fetch-from-raw.githubusercontent instruction); renumber following steps.
2. Verify section: replace `A superpowers skill (e.g. test-driven-development)` with `A vendored process skill (e.g. brainstorming)`.

- [ ] **Step 5: external-skills.md edit**

Superpowers entry gains: `Status: process skills forked into this repo 2026-09-24 (brainstorming, writing-plans, using-git-worktrees, systematic-debugging, writing-skills), MIT.`

- [ ] **Step 6: workflow.md edit**

Replace the using-superpowers session-start description (lines ~56-58, ~110) with: skill discipline is enforced by this repo's commands and agents; process skills load from the repo's own `skills/` directory.

- [ ] **Step 7: README.md edits**

Drop the External skills bullet that points at installing superpowers (~line 32) and the superpowers quick-install URL (~lines 46-47); renumber any list they belonged to. Catalog rows added in Tasks 1-5 stay.

- [ ] **Step 8: stack.drawio edit**

In `docs/workflows/stack.drawio`, the layer-2 label `superpowers plugin v6.1.1 (using-superpowers...)` (~line 56) becomes `vendored process skills (this repo)`.

- [ ] **Step 9: Verify no live namespaced refs**

Run: `git grep -in "superpowers:" -- ':!docs/artifacts'`
Expected: no output.

- [ ] **Step 10: Commit**

```bash
git add skills/multi-plan-orchestration/SKILL.md skills/rubens-project-standardization/references/artifacts.md AGENTS.md opencode-install.md external-skills.md README.md docs/workflows/workflow.md docs/workflows/stack.drawio
git commit -m "docs(skills): point live flows at vendored process skills, drop superpowers namespace"
```

---

### Task 7: Machine config + sync (runs LAST, no commit; outside the repo)

**Files:**
- Modify: `C:\Users\ruben\.config\opencode\opencode.json` (plugin array)
- Modify: `C:\Users\ruben\.config\opencode\package.json` (npm uninstall)
- Create: copies of the 5 skill folders in `~\.claude\skills\` and `~\.config\opencode\skills\`

- [ ] **Step 1: Remove plugin entry**

In `C:\Users\ruben\.config\opencode\opencode.json`, the plugin array currently:

```json
"plugin":  [ "~/.config/opencode/node_modules/superpowers",
             "opencode-see-image@1.3.2",
             "@ramtinj95/opencode-tokenscope" ]
```

becomes:

```json
"plugin":  [ "opencode-see-image@1.3.2",
             "@ramtinj95/opencode-tokenscope" ]
```

Line-level edit; preserve all other formatting and keys.

- [ ] **Step 2: Validate JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync(process.env.USERPROFILE + '/.config/opencode/opencode.json','utf8')); console.log('valid')"`
Expected: `valid`

- [ ] **Step 3: Uninstall package**

Run (workdir `C:\Users\ruben\.config\opencode`): `npm uninstall superpowers`
Then: `npm ls superpowers`
Expected: `empty` (or "not found"); no entry in `package.json` dependencies.

- [ ] **Step 4: Sync skills to both agent dirs**

```powershell
$skills = 'brainstorming','writing-plans','using-git-worktrees','systematic-debugging','writing-skills'
foreach ($s in $skills) {
  Copy-Item -Recurse -Force "skills\$s" "$env:USERPROFILE\.claude\skills\$s"
  Copy-Item -Recurse -Force "skills\$s" "$env:USERPROFILE\.config\opencode\skills\$s"
}
```

Expected: 5 folders present in both targets, each containing `SKILL.md`.

---

### Task 8: Final verification + report

**Files:**
- Create: `docs/artifacts/features/superpowers-fork/2026-09-24-superpowers-fork-report.md`

- [ ] **Step 1: Repo checks**

1. `git log --oneline -8`: 6 new commits on `feat/superpowers-fork` (Tasks 1-6), clean working tree.
2. Em-dash scan over the whole repo: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty.
3. Catalogs: `brainstorming`, `writing-plans`, `using-git-worktrees`, `systematic-debugging`, `writing-skills` each appear in both the `README.md` Skills table and the `AGENTS.md` Current skills table; folder names match frontmatter names.
4. No live `superpowers:` refs (Task 6 Step 9 command: `git grep -in "superpowers:" -- ':!docs/artifacts'`).

- [ ] **Step 2: Machine checks**

1. `npm ls superpowers` in `~\.config\opencode`: empty.
2. `opencode.json` valid JSON.
3. Both skill target dirs contain the 5 folders.

- [ ] **Step 3: Documenter report + commit**

Documenter writes `docs/artifacts/features/superpowers-fork/2026-09-24-superpowers-fork-report.md` (what changed, verification evidence, accepted losses from the spec: no upstream updates, no session bootstrap) and commits:

```bash
git add docs/artifacts/features/superpowers-fork
git commit -m "docs: superpowers fork execution report"
```

- [ ] **Step 4: Stop on the branch**

No merge, no push. The final report tells the user the branch is ready for review.
