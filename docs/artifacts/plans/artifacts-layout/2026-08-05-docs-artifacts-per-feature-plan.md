# docs/artifacts per-feature layout migration plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. The orchestrator dispatches one `executor` per task and a `reviewer` after each; escalates two-strike failures to `oracle`.

**Goal:** Reorganize `docs/artifacts/` from a type-bucket split (`specs/`, `plans/`, `multi-plans/`, `reports/`) to a per-feature split (`features/<feature>/...`). `reviews/` stays flat at the top level. Preserve filenames exactly. Update every reference after the move.

**Architecture:** Two top-level dirs only: `docs/artifacts/reviews/` (flat, sequential log) and `docs/artifacts/features/` (per-feature container, flat contents inside). Filename suffix (`-design`, `-plan`, `-outline`, `-manifest`, `-report`) signals artifact type inside a feature folder. Mechanical migration: `git mv` files, then sed-equivalent edits to references. Two commits: one for the move, one for the reference updates, then a verification task.

**Tech Stack:** `git mv`, `git rm`, PowerShell `Get-ChildItem` + `Select-String` for reference sweeps, Markdown edits. No new tools.

**Spec:** `docs/artifacts/specs/artifacts-layout/2026-08-05-docs-artifacts-per-feature-design.md`

## Global Constraints

- No em-dashes (U+2014) anywhere. Verify after each task: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty for edited files.
- Conventional Commits 1.0.0. Per-task commits are sanctioned by the plan-execution carve-out; do not pause to ask.
- Use `git mv`, never `mv` + `git add`. History must show renames, not delete+add.
- Filenames preserved exactly. No rename, no suffix swap.
- CHANGELOG.md historical entries and references inside `docs/artifacts/reviews/*.md` stay as-is (immutable history).
- Today is 2026-08-05 for any dated artifact paths.
- The spec itself and this plan migrate during the move. They were written under the old convention one last time.

## File Structure

Layout after migration:

```
docs/artifacts/
├── reviews/                                  (flat, unchanged)
│   └── 2026-07-{03,07,12}-harvest.md
└── features/<feature>/
    ├── <YYYY-MM-DD>-<slug>-design.md         (spec)
    ├── <YYYY-MM-DD>-<slug>-plan.md           (plan)
    ├── <YYYY-MM-DD>-<topic>-outline.md       (multi-plan outline)
    ├── <YYYY-MM-DD>-<topic>-manifest.md      (multi-plan manifest)
    └── <YYYY-MM-DD>-<slug>-report.md         (execution report)
```

Features in scope (10 total): `agent-roster`, `commitlint`, `code-standardization`, `inventree-datasheet-autopilot`, `multi-plan-orchestration`, `opencode-inventree-agent`, `orchestrator-standardization-documentation`, `single-pass-full-cycle`, `skill-harvest`, `standardization-commit-hook`.

`artifacts-layout` (this spec/plan's own feature) is created during the move.

---

### Preflight: branch + commit the spec and plan

Follow `/execute-plan` conventions. Before Task 1:

- [ ] **Step 0a: Branch.** Run `git rev-parse --abbrev-ref HEAD`. If it returns `main`/`master`, create and switch to `feat/docs-artifacts-per-feature`. Re-run `git branch --show-current`; do not proceed until off the default branch.
- [ ] **Step 0b: First commit (artifacts).** `git add docs/artifacts/specs/artifacts-layout docs/artifacts/plans/artifacts-layout`, then `git commit -m "docs: add plan and spec for docs/artifacts per-feature layout"`.

---

### Task 1: Move all artifact files into `features/<feature>/`

**Files:**
- Move: every file under `docs/artifacts/specs/`, `docs/artifacts/multi-plans/`, `docs/artifacts/reports/` -> `docs/artifacts/features/<feature>/`
- Rename: top-level `docs/artifacts/plans/` -> `docs/artifacts/features/` (the existing per-feature subdirs stay, the parent dir is renamed)
- Delete: now-empty `docs/artifacts/specs/`, `docs/artifacts/multi-plans/`, `docs/artifacts/reports/` (and the now-merged old `docs/artifacts/plans/`)

**Depends on:** Preflight. **Affects:** every later task (all references update against this new layout).

- [ ] **Step 1: Rename `plans/` to `features/`.** The per-feature subdirs under `plans/` already match the target layout; only the parent dir needs renaming. `git mv docs/artifacts/plans docs/artifacts/features`.
- [ ] **Step 2: Move specs into features.** For each feature with a `docs/artifacts/specs/<feature>/` directory, `git mv docs/artifacts/specs/<feature>/* docs/artifacts/features/<feature>/`. Then `git rm -r docs/artifacts/specs/<feature>`.
- [ ] **Step 3: Move multi-plans into features.** For each feature with a `docs/artifacts/multi-plans/<feature>/` directory, `git mv docs/artifacts/multi-plans/<feature>/* docs/artifacts/features/<feature>/`. Then `git rm -r docs/artifacts/multi-plans/<feature>`.
- [ ] **Step 4: Move reports into features.** For each feature with a `docs/artifacts/reports/<feature>/` directory, `git mv docs/artifacts/reports/<feature>/* docs/artifacts/features/<feature>/`. Then `git rm -r docs/artifacts/reports/<feature>`.
- [ ] **Step 5: Remove the now-empty old top-level dirs.** `git rm -r docs/artifacts/specs docs/artifacts/multi-plans docs/artifacts/reports`.
- [ ] **Step 6: Verify directory structure.** `Get-ChildItem -Recurse docs/artifacts | Select-String -Pattern '\.md$'` (or equivalent listing) must show only `reviews/*.md` files at the top level (under `reviews/`) and feature-named subdirs of `features/`. No stray `specs/`, `multi-plans/`, `reports/`, or `plans/` dirs anywhere.
- [ ] **Step 7: Commit.** `git add -A` then `git commit -m "docs(artifacts): reorganize docs/artifacts into per-feature layout"`.

**Known feature-to-source mapping (use this to avoid per-feature guessing):**

| Feature | specs source | multi-plans source | reports source |
|---|---|---|---|
| `agent-roster` | `docs/artifacts/specs/agent-roster/` | (none) | (none) |
| `commitlint` | `docs/artifacts/specs/commitlint/` | (none) | (none) |
| `code-standardization` | `docs/artifacts/specs/code-standardization/` | `docs/artifacts/multi-plans/code-standardization/` | `docs/artifacts/reports/code-standardization/` |
| `inventree-datasheet-autopilot` | `docs/artifacts/specs/inventree-datasheet-autopilot/` | (none) | (none) |
| `multi-plan-orchestration` | `docs/artifacts/specs/multi-plan-orchestration/` | (none) | (none) |
| `opencode-inventree-agent` | `docs/artifacts/specs/opencode-inventree-agent/` | (none) | (none) |
| `orchestrator-standardization-documentation` | `docs/artifacts/specs/orchestrator-standardization-documentation/` | (none) | (none) |
| `single-pass-full-cycle` | `docs/artifacts/specs/single-pass-full-cycle/` | (none) | (none) |
| `skill-harvest` | `docs/artifacts/specs/skill-harvest/` | (none) | (none) |
| `standardization-commit-hook` | `docs/artifacts/specs/standardization-commit-hook/` | (none) | (none) |
| `artifacts-layout` | (none, already in specs/) | (none) | (none) |

---

### Task 2: Update active generators (skills, commands, agents)

**Files:**
- Edit: `agents/planner.md`
- Edit: `agents/documenter.md`
- Edit: `agents/orchestrator.md`
- Edit: `commands/full-cycle.md`
- Edit: `commands/execute-plan.md`
- Edit: `commands/multi-plan.md`
- Edit: `commands/harvest.md`
- Edit: `skills/multi-plan-orchestration/SKILL.md`

**Depends on:** Task 1. **Affects:** every future artifact written by these generators.

- [ ] **Step 1: Rewrite path instructions in each generator.** For each file in the list above, find every reference to `docs/artifacts/specs/`, `docs/artifacts/multi-plans/`, `docs/artifacts/reports/`, `docs/artifacts/plans/` (when used as a parent dir, not as a feature subdir), and rewrite to `docs/artifacts/features/`. Keep `docs/artifacts/reviews/` unchanged.
- [ ] **Step 2: Rephrase brace-glob patterns.** Some references use patterns like `docs/artifacts/{specs,plans,reviews}/` or `docs/artifacts/{specs,plans,reviews,reports}/`. Rewrite to `docs/artifacts/{features,reviews}/`.
- [ ] **Step 3: Verify no stale paths.** Run `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/'` against `agents/`, `commands/`, `skills/multi-plan-orchestration/SKILL.md`. Expect zero hits.
- [ ] **Step 4: Commit.** `git add -A` then `git commit -m "docs(skills): point generators at docs/artifacts/features/ layout"`.

**Per-file edit map (use as the authoritative list; anything missed fails verification):**

| File | Current | Replace with |
|---|---|---|
| `agents/planner.md` | `docs/artifacts/specs/<topic>/YYYY-MM-DD-<slug>-design.md` | `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md` |
| `agents/planner.md` | `docs/artifacts/plans/<topic>/YYYY-MM-DD-<slug>-plan.md` | `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md` |
| `agents/documenter.md` | `docs/artifacts/reports/<topic>/YYYY-MM-DD-<slug>-report.md` (twice) | `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-report.md` |
| `agents/documenter.md` | `docs/artifacts/reports/` (bare) | `docs/artifacts/features/` |
| `agents/orchestrator.md` | `docs/artifacts/reports/` (bare) | `docs/artifacts/features/` |
| `commands/full-cycle.md` | `docs/artifacts/specs/<topic>/...design.md` | `docs/artifacts/features/<topic>/...design.md` |
| `commands/full-cycle.md` | `docs/artifacts/plans/<topic>/...plan.md` | `docs/artifacts/features/<topic>/...plan.md` |
| `commands/full-cycle.md` | `docs/artifacts/reports/` (bare) | `docs/artifacts/features/` |
| `commands/full-cycle.md` | `docs/artifacts/plans/<topic>/<file>.md` (handoff line) | `docs/artifacts/features/<topic>/<file>.md` |
| `commands/execute-plan.md` | `docs/artifacts/specs/` | `docs/artifacts/features/` |
| `commands/execute-plan.md` | `docs/artifacts/reports/<topic>/YYYY-MM-DD-<slug>-report.md` | `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-report.md` |
| `commands/multi-plan.md` | `docs/artifacts/multi-plans/<topic>/...` | `docs/artifacts/features/<topic>/...` |
| `commands/harvest.md` | `docs/artifacts/reviews/YYYY-MM-DD-harvest.md` | (no change) |
| `skills/multi-plan-orchestration/SKILL.md` | all `docs/artifacts/{multi-plans,specs,plans}/` patterns | `docs/artifacts/features/` |

---

### Task 3: Update layout documentation (top-level docs + workflows)

**Files:**
- Edit: `STANDARDS.md`
- Edit: `AGENTS.md`
- Edit: `agents/README.md`
- Edit: `agents/standardizer.md`
- Edit: `skills/code-standardization/SKILL.md`
- Edit: `commands/standardize.md`
- Edit: `docs/workflows/workflow.md`
- Edit: `docs/workflows/plan-flow.drawio`
- Edit: `docs/workflows/multi-plan-flow.drawio`
- Edit: `docs/workflows/stack.drawio` (only if it mentions `docs/artifacts/`)

**Depends on:** Task 1. **Affects:** discoverability and standardization audits.

- [ ] **Step 1: Rewrite path references in each doc.** Same rewrite rules as Task 2: `docs/artifacts/specs/`, `docs/artifacts/multi-plans/`, `docs/artifacts/reports/` -> `docs/artifacts/features/`. Top-level `docs/artifacts/plans/` -> `docs/artifacts/features/`. Brace-globs: `docs/artifacts/{specs,plans,reviews}/` -> `docs/artifacts/{features,reviews}/`; `docs/artifacts/{specs,plans,reviews,reports}/` -> `docs/artifacts/{features,reviews}/`. `docs/artifacts/reviews/` unchanged.
- [ ] **Step 2: Update drawio path labels.** Edit the XML in `plan-flow.drawio` and `multi-plan-flow.drawio` so the path strings inside `<mxCell value="...">` match the new layout. Preserve all other XML attributes byte-for-byte.
- [ ] **Step 3: Verify no stale paths.** `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/'` against all non-`docs/artifacts/` non-`CHANGELOG.md` non-`reviews/` paths. Expect zero hits.
- [ ] **Step 4: Commit.** `git add -A` then `git commit -m "docs: update layout documentation for docs/artifacts/features/"`.

---

### Task 4: Update cross-references inside moved artifacts

**Files:** every `.md` under `docs/artifacts/features/` (cross-references between sibling artifacts in the same folder or other features).

**Depends on:** Task 1. **Affects:** navigation between artifacts.

- [ ] **Step 1: Enumerate stale cross-references.** `git grep -n 'docs/artifacts/specs/' docs/artifacts/features/` returns the lines that still reference the old spec path. Same for `docs/artifacts/multi-plans/` and `docs/artifacts/reports/`. Note: `docs/artifacts/plans/` references inside `features/` are already correct (the rename was just the top-level dir).
- [ ] **Step 2: Rewrite each hit.** `docs/artifacts/specs/<feature>/<file>` -> `docs/artifacts/features/<feature>/<file>`. Same for `multi-plans/` and `reports/`. Edit the actual file content, not just the path in the comment.
- [ ] **Step 3: Re-grep to confirm.** `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/' docs/artifacts/features/` returns zero hits.
- [ ] **Step 4: Commit.** `git add -A` then `git commit -m "docs(artifacts): update cross-references for per-feature layout"`.

---

### Task 5: Repo-wide verification

**Depends on:** Tasks 1-4.

- [ ] **Step 1: Grep audit (active code).** `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/' -- ':!CHANGELOG.md' ':!docs/artifacts/reviews/*'` returns zero hits. If anything hits, fix and amend or add a follow-up commit.
- [ ] **Step 2: Grep audit (historical, accepted).** `git grep -n 'docs/artifacts/\(specs\|multi-plans\|reports\)/' -- CHANGELOG.md docs/artifacts/reviews/` returns the historical references that stay. Confirm those are the only stale references remaining.
- [ ] **Step 3: Directory tree sanity.** `Get-ChildItem docs/artifacts -Directory` returns exactly `reviews` and `features`. No `specs`, `plans`, `multi-plans`, or `reports` at the top level.
- [ ] **Step 4: New path is reachable.** `git grep -n 'docs/artifacts/features/' -- ':!docs/artifacts/features/*'` returns the new reference sites (skills, commands, agents, top-level docs). Confirm the count looks right.
- [ ] **Step 5: Reviews unchanged.** `git diff main -- docs/artifacts/reviews/` returns empty.
- [ ] **Step 6: Filename preservation.** `git diff main --name-only --diff-filter=R | ForEach-Object { ... }` (or equivalent) confirms every rename is purely a directory move, not a content rename. Spot-check a few: filenames should be identical to their pre-migration names.
- [ ] **Step 7: No em-dashes introduced.** `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty.
- [ ] **Step 8: Conventional Commits on the branch.** `git log main..HEAD --oneline` shows three `docs:` or `docs(...):` commits matching Task 1/2/3/4 messages.

---

### Done

Hand off to the standardizer for the structure-review phase, then the documenter for the execution report. Report back to the planner with the branch name, commit list, and verification output.
