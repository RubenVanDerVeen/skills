# Choices Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. In this repo, /execute-plan conventions apply: executor per task, reviewer after each task, Conventional Commits per task.

**Goal:** Add a cross-feature decision registry at `docs/artifacts/choices/` so recorded choices explain why they exist, get consulted before being undone, and surface in PR descriptions.

**Architecture:** Markdown-only convention change. The source of truth is the `## Choices` section in `skills/rubens-project-standardization/references/artifacts.md`. Flow wiring: planner looks up before locking decisions, lazy-dev checks for contradictions, orchestrator feeds material to documenter, documenter writes entries plus `index.md` at close-out, pr-description gains a `## Choices` section. Spec: `docs/artifacts/features/choices-registry/2026-09-24-choices-registry-design.md`.

**Tech Stack:** Markdown files, PowerShell greps for verification, tracked git hooks (`.githooks/`), Conventional Commits.

## Global Constraints

- No em-dashes (U+2014) in any file. Verify per task with: `(Get-ChildItem <touched paths> -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` must return empty.
- Branch: `feat/choices-registry`, created first.
- Versioning: this repo's `AGENTS.md` has no `### Versioning` subsection: unversioned, no bump.
- No catalog rows needed: no new skill, no new command file. Catalog checks exist to catch new skills; none are added here.
- File pattern everywhere: `docs/artifacts/choices/YYYY-MM-DD-<slug>-decision.md`; index at `docs/artifacts/choices/index.md`.
- Do not create `docs/superpowers/` or `.planning/` (forbidden by pre-commit hook).
- Conventional Commits 1.0.0 per task; hooks active via `git config core.hooksPath .githooks` (verify once in Task 1 setup).

---

### Task 1: Convention source of truth + seed index

**Files:**
- Modify: `skills/rubens-project-standardization/references/artifacts.md` (tree at lines 30-41, "Two top-level directories" at line 28, grammar token list at line 172, redirect clause at line 187, memory clause at line 240, new `## Choices` section)
- Modify: `AGENTS.md` (`## Artifacts` section)
- Create: `docs/artifacts/choices/index.md`

**Interfaces:**
- Produces: the canonical entry template and threshold wording that Tasks 2 and 3 reference; the seeded `index.md` that the planner grep and documenter writes depend on.

- [ ] **Step 1: Setup checks**

Run: `git config core.hooksPath` → expect `.githooks`. If empty, run `git config core.hooksPath .githooks`.
Run: `git checkout -b feat/choices-registry` (skip if it already exists and is checked out).

- [ ] **Step 2: Read artifacts.md and apply the five point edits**

Read `skills/rubens-project-standardization/references/artifacts.md` first. Then:

1. Line 28 area, replace the sentence starting "Two top-level directories." with:

```markdown
Three top-level directories: `features/` (one folder per feature), `reviews/` (committed audits), `choices/` (decision records). Everything for one feature lives in one folder. Filename suffix signals type.
```

2. In the layout tree (lines 30-41), insert this block immediately before the `reviews/` entry:

```markdown
├── choices/                                  <- cross-feature decision records
│   ├── index.md                              <- one table row per decision
│   └── YYYY-MM-DD-<slug>-decision.md         <- one file per choice
```

3. In the filename grammar list (line 172), add the token `decision` in the same style as the existing tokens, e.g.:

```markdown
`decision` (choices registry entry)
```

4. In the per-framework redirect paragraph (line 187), append one clause to the existing sentence:

```markdown
; redirect every decision record to `docs/artifacts/choices/`
```

5. At the cross-session memory guidance (line 240, "capture that fact in a memory entry"), replace the memory clause so constraining decisions go to the registry instead:

```markdown
record it as a choices registry entry (see the Choices section)
```

- [ ] **Step 3: Add the `## Choices` section to artifacts.md**

Insert after the reviews section (or directly after the layout section if no reviews section exists). Outer fence uses four backticks because the template itself is fenced:

````markdown
## Choices

The choices registry (`docs/artifacts/choices/`) records why constraining decisions were made, so future work checks why something exists before removing or contradicting it.

**Threshold.** Record a choice when it constrains future work or a future agent might wrongly undo it: dependency and plugin picks, architecture forks, standards picks, explicit X-over-Y calls. Routine implementation trivia stays in the spec or report.

**Files.** One file per decision: `YYYY-MM-DD-<slug>-decision.md`. `index.md` holds one table row per decision (Date | Decision | Status | File). Template:

````markdown
# <Slug title>

- Date: YYYY-MM-DD
- Status: active
- Source: <path to plan, report, or PR>

## Choice
<One sentence: what was chosen.>

## Alternatives rejected
<What was not chosen and why not. One line per alternative.>

## Revisit when
<The condition that would invalidate this choice.>
````

**Status values.** `active`, or `superseded by YYYY-MM-DD-<slug>-decision.md`. Superseding never deletes: flip the old entry's status line and cite it from the new one.

**Writers and readers.** The documenter writes entries at close-out from run material and skips silently when nothing qualifies. The planner greps `docs/artifacts/choices/` (all files, full text) before locking spec decisions and carries constraints (or supersessions) into the spec.

**Registry vs spec decisions.** A spec's `## Decisions` section holds run-local detail. The registry holds the durable cross-feature record with rejected alternatives and revisit conditions. When both exist, the registry entry cites the spec; the spec never duplicates registry content. Splitting one feature's artifacts across type buckets to "organize choices" remains forbidden (see anti-patterns).
````

- [ ] **Step 4: Update AGENTS.md Artifacts section**

In the `## Artifacts` section of the repo-root `AGENTS.md`:

1. Change the prose line "Process meta-documents (specs, plans, multi-plan outlines/manifests, execution reports, reviews) live in `docs/artifacts/`, not next to the code:" to:

```markdown
Process meta-documents (specs, plans, multi-plan outlines/manifests, execution reports, reviews, decision records) live in `docs/artifacts/`, not next to the code:
```

2. Add this bullet after the `docs/artifacts/reviews/` bullet:

```markdown
- `docs/artifacts/choices/`: cross-feature decision records (`YYYY-MM-DD-<slug>-decision.md`) plus `index.md`. Written by the documenter at close-out; consulted by the planner before locking decisions. Convention: `skills/rubens-project-standardization/references/artifacts.md`.
```

- [ ] **Step 5: Conditional: check the standardization SKILL.md**

Run: `Select-String -Path skills/rubens-project-standardization/SKILL.md -Pattern "reviews/|features/"`
If (and only if) SKILL.md lists the artifacts subfolders, add `choices/` to that list in the same style. If it does not list subfolders, do nothing.

- [ ] **Step 6: Seed the index**

Create `docs/artifacts/choices/index.md`:

```markdown
# Choices index

One row per recorded decision. Files: `YYYY-MM-DD-<slug>-decision.md`. Convention: `skills/rubens-project-standardization/references/artifacts.md`.

| Date | Decision | Status | File |
|------|----------|--------|------|
```

- [ ] **Step 7: Verify**

Run: `Select-String -Path skills/rubens-project-standardization/references/artifacts.md, AGENTS.md -Pattern "choices"` → expect hits in tree, grammar, redirect, Choices section, memory clause, and the Artifacts section.
Run: `(Get-ChildItem skills/rubens-project-standardization/references/artifacts.md, AGENTS.md, docs/artifacts/choices/index.md | Select-String -Pattern ([char]0x2014))` → expect empty.

- [ ] **Step 8: Commit**

```bash
git add skills/rubens-project-standardization/references/artifacts.md AGENTS.md docs/artifacts/choices/index.md
git commit -m "feat(conventions): add choices registry convention and seed index"
```

---

### Task 2: Flow wiring in agent definitions

**Files:**
- Modify: `agents/planner.md` (step 3, Spec)
- Modify: `agents/lazy-dev.md` (review checklist)
- Modify: `agents/orchestrator.md` (step 8 dispatch payload, line ~52)
- Modify: `agents/documenter.md` (frontmatter description line 2, input list line ~60, new step between report step and PR step ~64-65)

**Interfaces:**
- Consumes: the template path `skills/rubens-project-standardization/references/artifacts.md` and `docs/artifacts/choices/index.md` from Task 1.
- Produces: the behavioral contract Task 3's command files describe ("task reports feed the choices registry", "documenter writes choices entries").

- [ ] **Step 1: Read all four agent files**

Read `agents/planner.md`, `agents/lazy-dev.md`, `agents/orchestrator.md`, `agents/documenter.md` in full before editing.

- [ ] **Step 2: Planner lookup step**

In `agents/planner.md`, inside the Spec step (step 3, which writes the design to `docs/artifacts/features/...`), add this sentence before the instruction to write the spec file:

```markdown
Before locking the spec, grep `docs/artifacts/choices/` (all files, full text) for the task's topics and likely dependency or plugin names. Read every hit: carried constraints go into the spec; contradictions note the old entry as superseded (the documenter flips its status line at close-out).
```

- [ ] **Step 3: lazy-dev contradiction check**

In `agents/lazy-dev.md`, add one item to the review checklist, in the list's existing style:

```markdown
- The plan contradicts an active entry in `docs/artifacts/choices/` without explicitly superseding it.
```

- [ ] **Step 4: Orchestrator payload**

In `agents/orchestrator.md` step 8 (the Documentation dispatch to `documenter`), extend the raw-material list with one item:

```markdown
approaches considered and rejected (from the spec), defaults taken during tasks, choices superseded
```

- [ ] **Step 5: Documenter writes the registry**

In `agents/documenter.md`:

1. Frontmatter `description`: append `, writes docs/artifacts/choices/ decision entries and index when the run made constraining choices` before the final clause about returning the report path. Keep total frontmatter under 1024 chars.
2. Input list (the dispatch payload it receives, around line 60): add `approaches rejected (spec), defaults taken (task notes)`.
3. Insert a new numbered step between the report step (step 2) and the PR-description step (step 3), renumbering later steps:

```markdown
3. **Choices registry:** for each qualifying choice in the run material (spec's rejected approaches, executor default-notes, orchestrator dispatch material), write `docs/artifacts/choices/YYYY-MM-DD-<slug>-decision.md` using the template in `skills/rubens-project-standardization/references/artifacts.md`, add one row to `docs/artifacts/choices/index.md`, flip the status line of any superseded entry, and list the files in the PR description's `## Choices` section. Write nothing when nothing qualifies.
```

- [ ] **Step 6: Verify**

Run: `Get-ChildItem agents -Filter *.md | Select-String -Pattern "choices"` → expect at least one hit in each of planner.md, lazy-dev.md, orchestrator.md, documenter.md.
Run: `(Get-ChildItem agents -Filter *.md | Select-String -Pattern ([char]0x2014))` → expect empty.

- [ ] **Step 7: Commit**

```bash
git add agents/planner.md agents/lazy-dev.md agents/orchestrator.md agents/documenter.md
git commit -m "feat(agents): wire choices registry into planner, lazy-dev, orchestrator, documenter"
```

---

### Task 3: Commands and PR template

**Files:**
- Modify: `commands/execute-plan.md` (setup step, line ~10)
- Modify: `commands/full-cycle.md` (pipeline steps, lines ~12-17)
- Modify: `skills/pr-description/SKILL.md` (template lines ~18-30)

**Interfaces:**
- Consumes: registry path and template from Task 1; documenter behavior from Task 2.
- Produces: the user-visible PR `## Choices` section.

- [ ] **Step 1: Read the three files**

Read `commands/execute-plan.md`, `commands/full-cycle.md`, `skills/pr-description/SKILL.md` in full before editing.

- [ ] **Step 2: execute-plan note destination**

In `commands/execute-plan.md`, change the setup sentence:

```markdown
A missing detail is not a blocker, pick the obvious choice, note it, proceed.
```

to:

```markdown
A missing detail is not a blocker, pick the obvious choice, note it in the task report (task reports feed the choices registry), proceed.
```

- [ ] **Step 3: full-cycle deliverable mention**

In `commands/full-cycle.md`, in the Execute step (step 5) where the documentation phase is described, extend the documenter deliverable list with `choices entries`. Make no other change to this file; the wiring itself lives in the planner and documenter agent definitions.

- [ ] **Step 4: PR description Choices section**

In `skills/pr-description/SKILL.md`, in the template (between `## Verification` and `## Docs`), insert:

```markdown
## Choices
<New or updated `docs/artifacts/choices/` decision files, one line each on why. None if the run made or changed no constraining choices.>
```

- [ ] **Step 5: Verify**

Run: `Select-String -Path commands/execute-plan.md, commands/full-cycle.md, skills/pr-description/SKILL.md -Pattern "choices"` → expect the new clause, the deliverable mention, and the Choices template section.
Run: `(Get-ChildItem commands, skills/pr-description -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` → expect empty.
Run: `Select-String -Path skills/pr-description/SKILL.md -Pattern "^## "` → confirm template section order: Problem, What changed and why, Verification, Choices, Docs.

- [ ] **Step 6: Commit**

```bash
git add commands/execute-plan.md commands/full-cycle.md skills/pr-description/SKILL.md
git commit -m "feat(commands): route choice notes to registry and add PR Choices section"
```

---

## Self-review record

- Spec coverage: convention home (Task 1), planner lookup + lazy-dev check + orchestrator payload + documenter writing (Task 2), execute-plan note destination + full-cycle deliverable mention + PR section (Task 3), index seed (Task 1 Step 6), memory repoint (Task 1 Step 2 item 5), error handling behaviors (missing registry treated as none, nothing qualifies, supersede flow). All spec sections map to tasks.
- Gate round 1 adopted: directory full-text lookup instead of index-only greps; anti-pattern bullet and PR rules bullet cut as duplicates; memory overlap reconciled; `rg` swapped for `Select-String` (repo shell convention); full-cycle reduced to a two-word deliverable mention. Index kept: user-locked decision (see spec Decisions #2).
- Placeholders: `<Slug title>`-style angle brackets are the intentional template content, not plan gaps.
- Consistency: file pattern `YYYY-MM-DD-<slug>-decision.md` and registry path identical across all tasks; section order in PR template verified by a grep step.
