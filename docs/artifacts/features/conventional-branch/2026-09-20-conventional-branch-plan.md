# Conventional Branch Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt Conventional Branch 1.1.0 (<https://conventionalbranch.org/>) as a named standard: documented in both STANDARDS.md copies, applied by default by the branch-creating agent, legacy `plan-<name>` removed.

**Architecture:** Markdown-only, edit-in-place across 9 living docs (no new files). Spec types (`feature|feat`, `bugfix|fix`, `hotfix`, `release`, `chore`) are the standard; the repo's extra branch types (`docs/`, `refactor/`, `test/`, `ci/`) and the `feat/<slug>-spN-<name>` multi-plan suffix are documented as the spec-sanctioned custom extensions. No git hooks.

**Tech Stack:** Markdown only. Verification is grep/Select-String (no test runner in this content repo).

**Spec:** `docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-design.md`

## Global Constraints

- Every branch created for this plan: `docs/conventional-branch` (Conventional Branch compliant: `docs/` is a documented project extension type).
- No em-dashes (U+2014) in any file. Check with `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty.
- Commits: Conventional Commits 1.0.0, per-task. The plan-execution carve-out in `AGENTS.md` sanctions committing without asking.
- Historical files under `docs/artifacts/` (other features) are append-only history: never edit them.
- No new files anywhere. All changes are edits to existing markdown.
- The pre-commit hook (if activated via `core.hooksPath`) enforces em-dash and frontmatter rules; do not use `--no-verify`.

---

### Task 1: Root STANDARDS.md branch section

**Files:**
- Modify: `STANDARDS.md` (3 edits: Stack table row, new section, References link)

**Interfaces:**
- Produces: the canonical branch-naming section other tasks point to ("see `STANDARDS.md`").

- [ ] **Step 1: Add Stack table row**

In `STANDARDS.md`, after the line:

```
| Conventional Commits 1.0.0 | **yes**    | Commit messages |
```

insert:

```
| Conventional Branch 1.1.0 | **yes**    | Git branch names |
```

- [ ] **Step 2: Add branch section**

In `STANDARDS.md`, between the end of the "Commit messages: Conventional Commits 1.0.0" section (after the line `Enforcement: tracked git hooks in ...` paragraph and its trailing `---`) and the `## Changelog: Keep a Changelog 1.1.0` heading, insert:

````markdown
## Branches: Conventional Branch 1.1.0

Format: `<type>/<description>`. Specification: <https://conventionalbranch.org/>.

- Lowercase letters, digits, hyphens. Dots only for release versions (`release/v1.2.0`). No underscores, no spaces, no consecutive, leading, or trailing separators.
- Trunk branches (`main`) carry no prefix.
- Prefixes `docs/`, `refactor/`, `test/`, `ci/` are a project extension mirroring the matching Conventional Commit type (the spec allows custom types when documented). Multi-plan runs append a sub-plan segment instead of nesting: `feat/<slug>-spN-<name>` (git cannot hold `feat/<slug>` and `feat/<slug>/sp-1` at once: ref file/dir conflict).

| Prefix | Use |
|--------|-----|
| `feature/` or `feat/`  | New features |
| `bugfix/` or `fix/`    | Bug fixes |
| `hotfix/`              | Urgent fixes |
| `release/`             | Release preparation |
| `chore/`               | Non-code tasks (deps, tooling) |
| `docs/`, `refactor/`, `test/`, `ci/` | Project extension: mirrors the Conventional Commit type |
| `ai/`, `claude/`, `codex/`, `copilot/`, `cursor/` | AI agent source prefixes (spec v1.1.0; allowed, not required here) |

```
✅ feat/conventional-branch
✅ fix/header-bug
✅ feat/skills-md-sp2-catalogs
❌ Feature/Add-Login    (uppercase)
❌ plan-my-plan         (no type prefix)
❌ fix/header_bug       (underscore)
```

Agents apply this by default: the orchestrator branches as `<type>/<plan-slug>` when executing a plan (see `agents/orchestrator.md` and `commands/execute-plan.md`).

---

````

(Insert the section, then the existing `## Changelog: Keep a Changelog 1.1.0` heading follows it.)

- [ ] **Step 3: Add References link**

In the `## References` section, after the Conventional Commits line:

```
- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
```

insert:

```
- Conventional Branch 1.1.0: <https://conventionalbranch.org/>
```

- [ ] **Step 4: Verify**

Run: `Select-String -Path STANDARDS.md -Pattern "Conventional Branch"`
Expected: 3 hits (Stack row, section heading, References link). Run the em-dash check from Global Constraints scoped to this file: `(Select-String -Path STANDARDS.md -Pattern ([char]0x2014))` returns empty.

- [ ] **Step 5: Commit**

```bash
git add STANDARDS.md
git commit -m "docs(standards): adopt conventional branch 1.1.0"
```

---

### Task 2: Template STANDARDS.md branch section

**Files:**
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md` (3 edits, generic version: no repo-specific `-spN-` rule)

**Interfaces:**
- Consumes: nothing from Task 1 (same doc shape, stamped into bootstrapped projects).

- [ ] **Step 1: Add Stack table row**

After the line:

```
| Conventional Commits 1.0.0 | **yes**    | Commit messages |
```

insert:

```
| Conventional Branch 1.1.0 | **yes**    | Git branch names |
```

- [ ] **Step 2: Add generic branch section**

Between the end of "Commit messages: Conventional Commits 1.0.0" (after its `---`) and `## Changelog: Keep a Changelog 1.1.0`, insert:

````markdown
## Branches: Conventional Branch 1.1.0

Format: `<type>/<description>`. Specification: <https://conventionalbranch.org/>.

- Lowercase letters, digits, hyphens. Dots only for release versions (`release/v1.2.0`). No underscores, no spaces, no consecutive, leading, or trailing separators.
- Trunk branches (`main`, `master`, `develop`) carry no prefix.
- Spec prefixes: `feature/` (`feat/`), `bugfix/` (`fix/`), `hotfix/`, `release/`, `chore/`. Extra types mirroring Conventional Commits (`docs/`, `refactor/`, `test/`, `ci/`) are a sanctioned team extension: document any custom type here so tooling and teammates know it.

```
✅ feat/add-login-page
✅ fix/header-bug
❌ Feature/Add-Login    (uppercase)
❌ my-branch            (no type prefix)
```

---

````

- [ ] **Step 3: Add References link**

After the line:

```
- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
```

insert:

```
- Conventional Branch 1.1.0: <https://conventionalbranch.org/>
```

- [ ] **Step 4: Verify**

Run: `Select-String -Path "skills\rubens-project-standardization\templates\STANDARDS.md" -Pattern "Conventional Branch"`
Expected: 3 hits. Em-dash check on the file returns empty.

- [ ] **Step 5: Commit**

```bash
git add skills/rubens-project-standardization/templates/STANDARDS.md
git commit -m "docs(standardization): add conventional branch to STANDARDS template"
```

---

### Task 3: Agent defaults (AGENTS.md, orchestrator, execute-plan)

**Files:**
- Modify: `AGENTS.md:194` (branch bullet)
- Modify: `agents/orchestrator.md` (step 1 of the loop, one sentence)
- Modify: `commands/execute-plan.md` (step 2 of Setup, one clause)

**Interfaces:**
- Consumes: the STANDARDS.md branch section from Task 1 (referenced by name only).

- [ ] **Step 1: Replace the AGENTS.md branch bullet**

Replace (exact current text):

```
- **Default to a feature branch for non-trivial work.** Use `feat/<scope>` (or a per-plan `plan-<name>`) for features, new skills, and multi-step changes. Typos, single-line tweaks, and catalog-row syncs can land directly on `main`.
```

with:

```
- **Default to a feature branch for non-trivial work.** Branch names follow Conventional Branch 1.1.0 (see `STANDARDS.md`): `<type>/<scope>` such as `feat/<scope>`, `fix/<scope>`, `docs/<scope>`, `chore/<scope>`. Multi-plan runs use `feat/<slug>-spN-<name>`, never nested slashes. Typos, single-line tweaks, and catalog-row syncs can land directly on `main`.
```

- [ ] **Step 2: Add the default-application sentence to agents/orchestrator.md**

In `agents/orchestrator.md`, step 1 of "Your loop", after the sentence ending `The plan is the spec; do not write a new one.` insert:

```
Branch first: if on the default branch, create and switch to `<type>/<plan-slug>` per Conventional Branch 1.1.0 (`STANDARDS.md`), `<type>` matching the plan's dominant Conventional Commit type, and commit the plan and spec as the first `docs:` commit.
```

- [ ] **Step 3: Point commands/execute-plan.md at the standard**

In `commands/execute-plan.md` Setup step 2, replace:

```
(match the dominant Conventional Commit type the plan will produce)
```

with:

```
(match the dominant Conventional Commit type the plan will produce, per Conventional Branch 1.1.0, see `STANDARDS.md`)
```

- [ ] **Step 4: Verify**

Run: `Select-String -Path AGENTS.md,agents\orchestrator.md,commands\execute-plan.md -Pattern "Conventional Branch"`
Expected: 3 files, at least 3 hits total. Run: `Select-String -Path AGENTS.md -Pattern "plan-<name>"` returns nothing.

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md agents/orchestrator.md commands/execute-plan.md
git commit -m "docs(agents): apply conventional branch naming by default"
```

---

### Task 4: project-standardization coherence (standards-stack + AGENTS templates)

**Files:**
- Modify: `skills/rubens-project-standardization/references/standards-stack.md` (3 edits)
- Modify: `skills/rubens-project-standardization/templates/AGENTS-small.md:50`, `AGENTS-medium.md:20`, `AGENTS-large.md:48` (identical bullet replacement)

**Interfaces:**
- Consumes: nothing. Keeps the skill that owns the STANDARDS.md template consistent with Tasks 1-2.

- [ ] **Step 1: Add Conventional Branch to the floor list**

In `standards-stack.md`, replace (line 5, exact):

```
**Scope reminder:** the conventions layer (kebab-case, English paths, ISO 8601 prefix, Conventional Commits, Keep a Changelog) applies to **most** projects regardless of size.
```

with:

```
**Scope reminder:** the conventions layer (kebab-case, English paths, ISO 8601 prefix, Conventional Commits, Conventional Branch, Keep a Changelog) applies to **most** projects regardless of size.
```

- [ ] **Step 2: Add the Conventional Branch subsection**

After the Conventional Commits subsection (after the line `**Why:** machine-parseable history, automation-friendly (release notes, version bumps), traceable changes per configuration item (ties into ISO 10007).`) and before `### Keep a Changelog 1.1.0`, insert:

````markdown
### Conventional Branch 1.1.0

Branch names: `<type>/<description>`. Spec prefixes: `feature/` (`feat/`), `bugfix/` (`fix/`), `hotfix/`, `release/`, `chore/`. Extra types mirroring Conventional Commits (`docs/`, `refactor/`, `test/`, `ci/`) are a sanctioned team extension: document them in the project's `STANDARDS.md`. Lowercase, digits, hyphens; no underscores, spaces, or consecutive/leading/trailing separators. Trunk branches (`main`, `master`, `develop`) carry no prefix. Specification: <https://conventionalbranch.org/>.

```
✅ feat/add-login-page
✅ fix/header-bug
❌ Feature/Add-Login
❌ my-branch
```

**Why:** the branch name alone states purpose and type, CI can route on branch type, and it pairs with Conventional Commits the same way that spec pairs with Keep a Changelog.

````

- [ ] **Step 3: Add Conventional Branch to the "How to apply" floor**

Replace (exact):

```
1. **Always apply:** kebab-case ASCII paths, English structural paths, ISO 8601 date prefix, Conventional Commits, Keep a Changelog. These are the floor: small to large, every project.
```

with:

```
1. **Always apply:** kebab-case ASCII paths, English structural paths, ISO 8601 date prefix, Conventional Commits, Conventional Branch, Keep a Changelog. These are the floor: small to large, every project.
```

- [ ] **Step 4: Replace the branch bullet in all three AGENTS templates**

In `templates/AGENTS-small.md`, `templates/AGENTS-medium.md`, and `templates/AGENTS-large.md`, replace the identical bullet (exact current text in all three):

```
- **Default to a feature branch for features.** Use `feat/<scope>` (or a per-plan `plan-<name>`) for features, modules, and non-trivial changes. Small fixes (typos, single-line tweaks, dep bumps, docs-only edits) can land directly on the default branch. Plan execution follows the same default: each plan runs in its own branch, cut from the latest default branch at plan start. The user can always say otherwise.
```

with:

```
- **Default to a feature branch for features.** Use `<type>/<scope>` per Conventional Branch 1.1.0 (`feat/<scope>`, `fix/<scope>`, `chore/<scope>`; see `STANDARDS.md`) for features, modules, and non-trivial changes. Small fixes (typos, single-line tweaks, dep bumps, docs-only edits) can land directly on the default branch. Plan execution follows the same default: each plan runs in its own branch, cut from the latest default branch at plan start. The user can always say otherwise.
```

- [ ] **Step 5: Verify**

Run: `Select-String -Path "skills\rubens-project-standardization\references\standards-stack.md","skills\rubens-project-standardization\templates\AGENTS-*.md" -Pattern "Conventional Branch"`
Expected: hits in standards-stack.md (3) plus all three AGENTS templates (1 each). Run: `Select-String -Path "skills\rubens-project-standardization\templates\AGENTS-*.md" -Pattern "plan-<name>"` returns nothing.

- [ ] **Step 6: Commit**

```bash
git add skills/rubens-project-standardization/references/standards-stack.md skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md
git commit -m "docs(standardization): add conventional branch to standards stack and templates"
```

---

### Task 5: CHANGELOG entry + final sweep

**Files:**
- Modify: `CHANGELOG.md` (one entry under `## [Unreleased]` `### Added`)

**Interfaces:**
- Consumes: all prior tasks landed.

- [ ] **Step 1: Add the changelog entry**

Under `## [Unreleased]`, `### Added`, append as the last bullet:

```
- Conventional Branch 1.1.0 adopted as the named branch-naming standard: Stack row + section in `STANDARDS.md` (root and `project-standardization` template), floor entry in `references/standards-stack.md`, branch bullet in `AGENTS.md` and the three `templates/AGENTS-*.md`, default-application line in `agents/orchestrator.md`, pointer in `commands/execute-plan.md`. Legacy `plan-<name>` branch scheme removed (no type prefix, invalid per spec). Spec: `docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-design.md`.
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): note conventional branch adoption"
```

- [ ] **Step 3: Final repo-wide verification sweep**

Run each; all must pass:

```powershell
# 1. Em-dash ban repo-wide (must return empty)
(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))

# 2. Conventional Branch named in all 7 living docs
Select-String -Path STANDARDS.md,"skills\rubens-project-standardization\templates\STANDARDS.md",AGENTS.md,"agents\orchestrator.md","commands\execute-plan.md","skills\rubens-project-standardization\references\standards-stack.md",CHANGELOG.md -Pattern "Conventional Branch"

# 3. Legacy plan-<name> only in append-only history (hits allowed under docs\artifacts\ and the CHANGELOG history note)
Select-String -Path (Get-ChildItem -Recurse -Include *.md -Exclude REPORT,test) -Pattern "plan-<name>" | Where-Object { $_.Path -notmatch "docs.artifacts|CHANGELOG" }

# 4. Branch name is spec-compliant
git branch --show-current   # expect: docs/conventional-branch
```

Expected: (1) empty, (2) hits in all 7 files, (3) empty, (4) `docs/conventional-branch`.

---

## Self-review notes

- Spec coverage: design items 1-8 map to Tasks 1-5 in order (design item 3 = Task 3, item 6+7 = Task 4, item 8 = Task 5). Success criteria covered by Task 5 Step 3.
- No placeholders: every edit shows exact old and new text.
- Consistency: all tasks reference the standard as "Conventional Branch 1.1.0"; branch examples differ only where docs differ in audience (repo-specific `-spN-` only in root STANDARDS.md and AGENTS.md, as designed).
