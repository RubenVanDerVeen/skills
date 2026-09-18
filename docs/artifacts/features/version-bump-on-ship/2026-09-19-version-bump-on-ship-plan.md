# Version bump on ship: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When a plan branch ships feat/fix commits and the project declares a version source, the documenter bumps the version at close-out (ship-bump default); the planner states the applicability in every plan; the policy source of truth reflects this.

**Architecture:** Amend the existing SemVer trigger rule in `project-standardization`'s `references/versioning.md` (policy first), then wire the two agent definitions (documenter implements, planner declares applicability), then sync catalogs. No new skill, no orchestrator change (its user-invoked release-cut stays as-is).

**Tech Stack:** Markdown only. No build step. Verification is PowerShell `Select-String`/`git grep` plus tracked pre-commit hooks.

**Spec:** `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-design.md`

## Global Constraints

- No em-dashes (U+2014) in any file, ever. Verify each edited file with `Select-String -Pattern ([char]0x2014)`; expected: empty.
- Conventional Commits 1.0.0 subjects; `commit-msg` hook enforces. Activate hooks first (Task 0).
- This repo is unversioned: no `chore(release)` commit, no tag, no version source in this repo. Only the root `CHANGELOG.md` gets an entry.
- Do not touch `agents/orchestrator.md`, `agents/executor.md`, `agents/reviewer.md`, `commands/*.md`, or `skills/**/SKILL.md`. The spec scopes them out.
- Permission rule order in agent frontmatter: broad `"*": deny` FIRST, narrow allows LAST (last-match-wins; see `agents/README.md` maintenance notes).
- Canonical wording (reuse verbatim across tasks): the close-out bump is the **ship bump**; the deliberate act is the **release cut** (user-invoked, adds tag + confirmation).

---

### Task 0: Branch bootstrap and hooks

**Files:**
- Create: none (branch only)
- Commit: `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-design.md`, `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-plan.md`

**Interfaces:**
- Consumes: spec + plan already written by the planner on `main` (untracked).
- Produces: branch `feat/version-bump-on-ship` cut from `main` at `bd100f5` or later, with spec + plan committed.

- [ ] **Step 1: Verify hooks are active**

Run: `git config core.hooksPath`
Expected: `.githooks`. If empty, run `git config core.hooksPath .githooks`.

- [ ] **Step 2: Create the branch from main**

```bash
git checkout main
git pull --ff-only origin main
git checkout -b feat/version-bump-on-ship
```

- [ ] **Step 3: Commit spec and plan**

```bash
git add docs/artifacts/features/version-bump-on-ship/
git commit -m "docs: add spec and plan for version-bump-on-ship"
```

Expected: commit succeeds; `commit-msg` hook accepts the subject.

---

### Task 1: Amend the versioning policy (source of truth)

**Files:**
- Modify: `skills/rubens-project-standardization/references/versioning.md:33-40` (Trigger rule section)
- Modify: `skills/rubens-project-standardization/templates/AGENTS-small.md:66`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-medium.md:37`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-large.md:66`

**Interfaces:**
- Consumes: existing decision table (`versioning.md` lines 22-31), unchanged.
- Produces: the canonical trigger wording that Tasks 2 and 3 reference (ship bump = close-out default; release cut = user-invoked, adds confirmation + tag).

- [ ] **Step 1: Replace the Trigger rule section**

In `references/versioning.md`, replace lines 33-40 (from `## Trigger rule` through `There is no automatic continuous bumping. Cutting a version is an act, not a side-effect.`) with:

```markdown
## Trigger rule

Three touchpoints, by design.

- **During plan execution**: every feature or fix task appends the user-visible change to the `[Unreleased]` section of `CHANGELOG.md` in Keep a Changelog format. This is the only thing plan execution touches in CHANGELOG.
- **Ship bump (plan close-out, default)**: when a shipped branch contains bump-worthy commits per the decision rule (any `feat`, `fix:`, `perf:`, or breaking signal since the last version) and the project declares a canonical version source, the documenter bumps the version at close-out: edit the canonical source, edit every sync target, rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add the link ref, all in a single `chore(release): vX.Y.Z` commit. Docs-only ships leave `[Unreleased]` open and commit nothing. Projects without a declared version source skip the bump; the execution report says so in one line.
- **Release-cut** (deliberate, user-invoked): unchanged. Use it when the user explicitly asks to cut a release, wants a different version than the classification produces, or needs the `vX.Y.Z` tag for CI. The orchestrator classifies commits, recommends the next version, and on confirmation dispatches an executor that (a) edits the canonical source, (b) edits every sync target, (c) renames `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, (d) adds the link ref line at the bottom, (e) commits, (f) optionally tags `vX.Y.Z` when the project's CI triggers release builds from tags.

The ship bump finalizes the version; it never tags. Cutting a tag is an act, not a side-effect.
```

- [ ] **Step 2: Update the Trigger field in all three AGENTS templates**

In each of `templates/AGENTS-small.md` (line 66, inside the HTML comment), `templates/AGENTS-medium.md` (line 37), `templates/AGENTS-large.md` (line 66), replace:

```markdown
- **Trigger:** plan execution appends to `[Unreleased]` in `CHANGELOG.md`. Cutting a version is deliberate, user-invoked.
```

with:

```markdown
- **Trigger:** plan execution appends to `[Unreleased]` in `CHANGELOG.md`. At plan close-out the documenter ship-bumps the version when the branch carries feat/fix commits and this section declares a canonical source. Tagging a release stays deliberate, user-invoked.
```

- [ ] **Step 3: Verify**

Run: `git grep -n "no automatic continuous bumping" -- skills/rubens-project-standardization`
Expected: empty (old stance gone).

Run: `git grep -c "Ship bump" -- skills/rubens-project-standardization/references/versioning.md skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md`
Expected: 4 files, at least 1 hit each.

Run: `Select-String -Path skills/rubens-project-standardization/references/versioning.md,skills/rubens-project-standardization/templates/AGENTS-small.md,skills/rubens-project-standardization/templates/AGENTS-medium.md,skills/rubens-project-standardization/templates/AGENTS-large.md -Pattern ([char]0x2014)`
Expected: empty.

- [ ] **Step 4: Commit**

```bash
git add skills/rubens-project-standardization/references/versioning.md skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md
git commit -m "docs(skills): make ship-time version bump the close-out default"
```

---

### Task 2: Documenter implements the ship bump

**Files:**
- Modify: `agents/documenter.md:2` (description), `:11-23` (permission blocks), `:50-56` (Do, in order), `:58` (write scope)

**Interfaces:**
- Consumes: the ship-bump wording and decision rule from Task 1 (`references/versioning.md`).
- Produces: documenter steps renumbered so the orchestrator's existing "documentation via documenter" dispatch needs no change. Step 5 = ship bump, step 6 = docs commits, step 7 = return.

- [ ] **Step 1: Extend the frontmatter description (line 2)**

Append to the description, before the final sentence about write scope:

```text
Ship-bumps the project version at close-out when the branch carries feat/fix and AGENTS.md declares a canonical source; tagging stays user-invoked.
```

- [ ] **Step 2: Add version-source write permissions**

In each of the three permission blocks (`edit:`, `write:`, `patch:`), after the `"*.md": allow` line, add:

```yaml
    "**/package.json": allow
    "**/Cargo.toml": allow
    "**/pyproject.toml": allow
    "**/tauri.conf.json": allow
```

Resulting order per block: `"*": deny`, `"docs/**": allow`, `"*.md": allow`, the four new allows. (Broad first, narrow last.)

- [ ] **Step 3: Insert the ship-bump step and renumber**

In the `Do, in order` list, insert a new step 5 after the catalog step and renumber the old steps 5-6 to 6-7. Steps 5-7 become:

```markdown
5. **Ship bump (default when the project is versioned).** Read the project's `AGENTS.md`. If it declares a `### Versioning` canonical source, classify the branch's commits per the bump-type decision rule in project-standardization's `references/versioning.md`. Any `feat` (minor-equivalent), `fix:`/`perf:` (patch), or breaking signal (major-equivalent per 0.x/1.0+ row) means: edit the canonical source and every declared sync target, rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` in the project's `CHANGELOG.md`, add the link ref at the bottom, all in a single `chore(release): vX.Y.Z` commit. Only docs/chore/test commits, or no declared version source: skip the bump and note "unversioned/no bump" in one report line. Never tag in this step; tagging is the user-invoked release cut.
6. Commit the report and catalog updates as Conventional Commits 1.0.0 docs commits (e.g. `docs(reports): add execution report for <slug>` and `docs: update catalogs for <change>`). The plan-execution carve-out sanctions these commits; do not pause to ask.
7. Return the report path and a one-paragraph summary of what shipped.
```

- [ ] **Step 4: Update the write-scope paragraph (line 58)**

Replace:

```markdown
Write scope is `docs/**` and root-level `*.md`. Do not edit skill bodies under `skills/**/SKILL.md` or source code: that is executor work. You update indexes and catalogs only.
```

with:

```markdown
Write scope is `docs/**`, root-level `*.md`, and the version sources the project's `AGENTS.md` declares (canonical source + sync targets, e.g. `package.json`, `Cargo.toml`, `pyproject.toml`, `tauri.conf.json`) for the close-out ship bump only. Do not edit skill bodies under `skills/**/SKILL.md` or feature source code: that is executor work. You update indexes, catalogs, and versions only.
```

- [ ] **Step 5: Verify**

Run: `Select-String -Path agents/documenter.md -Pattern ([char]0x2014)`
Expected: empty.

Run: `Select-String -Path agents/documenter.md -Pattern "^\d\. "`
Expected: 7 numbered steps in order, step 5 starts `**Ship bump`.

Run: `git diff --stat -- agents/documenter.md`
Expected: only `agents/documenter.md` changed in this task.

- [ ] **Step 6: Commit**

```bash
git add agents/documenter.md
git commit -m "feat(agents): documenter applies the ship bump at close-out"
```

---

### Task 3: Planner declares version applicability

**Files:**
- Modify: `agents/planner.md:45` (step 4), `:46` (step 5 dispatch list)

**Interfaces:**
- Consumes: the ship-bump policy from Task 1.
- Produces: every plan states the expected bump (or "unversioned, no bump"); the orchestrator dispatch instruction names the documenter's ship bump so the close-out phase applies it.

- [ ] **Step 1: Extend step 4 (line 45)**

Replace:

```markdown
4. Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md, referencing the spec.
```

with:

```markdown
4. Plan: load the writing-plans skill; write the plan to docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md, referencing the spec. Check the project's AGENTS.md for a `### Versioning` subsection: if it declares a canonical version source, the plan states the expected bump type for the shipped work; if not, the plan records "unversioned, no bump".
```

- [ ] **Step 2: Extend the step 5 dispatch list (line 46)**

In the parenthetical convention list, insert `documenter ship-bumps the version when the project is versioned` between `oracle on two-strike failures` and `final report`.

- [ ] **Step 3: Verify**

Run: `Select-String -Path agents/planner.md -Pattern ([char]0x2014)`
Expected: empty.

Run: `git grep -n "unversioned, no bump" -- agents/planner.md`
Expected: 1 hit (step 4).

- [ ] **Step 4: Commit**

```bash
git add agents/planner.md
git commit -m "feat(agents): planner states version-bump applicability in plans"
```

---

### Task 4: Catalog and changelog sync

**Files:**
- Modify: `agents/README.md:9` (planner Role cell), `:18` (documenter Role cell)
- Modify: `CHANGELOG.md` (under `## [Unreleased]` -> `### Changed`)

**Interfaces:**
- Consumes: finished Tasks 1-3.
- Produces: catalogs consistent with the changed agent behavior; repo changelog entry. Repo policy check: this repo is unversioned, so no `chore(release)` commit here.

- [ ] **Step 1: Update the planner Role cell (line 9)**

Append to the Role cell: `States the expected version bump (or unversioned skip) in every plan.`

- [ ] **Step 2: Update the documenter Role cell (line 18)**

Append to the Role cell: `Ship-bumps the project version at close-out when the branch carries feat/fix and AGENTS.md declares a version source (tagging stays user-invoked).`

- [ ] **Step 3: Add the changelog entry**

In root `CHANGELOG.md`, append to `### Changed` (last item in that section, after the vitest-cwd entry):

```markdown
- Versioning policy: plan close-out now ship-bumps the project version by default. When a plan branch ships feat or fix commits and the project's `AGENTS.md` declares a canonical version source, the documenter bumps canonical source + sync targets, finalizes the `[Unreleased]` heading, and commits `chore(release): vX.Y.Z`. Docs-only ships and unversioned projects skip; tagging remains a deliberate, user-invoked release cut. Spec: `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-design.md`.
```

- [ ] **Step 4: Verify**

Run: `Select-String -Path agents/README.md,CHANGELOG.md -Pattern ([char]0x2014)`
Expected: empty.

Run: `git grep -n "Ship-bumps\|version bump" -- agents/README.md CHANGELOG.md`
Expected: hits in both files.

- [ ] **Step 5: Commit**

```bash
git add agents/README.md CHANGELOG.md
git commit -m "docs: sync agent catalog and changelog for ship-bump policy"
```
