# docs/artifacts per-feature layout

## Goal

Reorganize `docs/artifacts/` so every artifact for one piece of work lives under a single feature folder. Two top-level dirs: `reviews/` (flat log) and `features/` (per-feature container). The existing 4-way split (`specs/`, `plans/`, `multi-plans/`, `reports/`) goes away.

## Current state

```
docs/artifacts/
├── specs/<feature>/<YYYY-MM-DD>-<slug>-design.md
├── plans/<feature>/<YYYY-MM-DD>-<slug>-plan.md
├── multi-plans/<feature>/<YYYY-MM-DD>-<topic>-{outline,manifest}.md
├── reports/<feature>/<YYYY-MM-DD>-<slug>-report.md
└── reviews/<YYYY-MM-DD>-harvest.md (flat, sequential log)
```

To assemble feature X's full artifact set you visit four sibling folders.

## Target state

```
docs/artifacts/
├── reviews/<YYYY-MM-DD>-harvest.md         (flat, unchanged)
└── features/<feature>/
    ├── <YYYY-MM-DD>-<slug>-design.md      (spec)
    ├── <YYYY-MM-DD>-<slug>-plan.md        (plan)
    ├── <YYYY-MM-DD>-<topic>-outline.md    (multi-plan outline)
    ├── <YYYY-MM-DD>-<topic>-manifest.md   (multi-plan manifest)
    └── <YYYY-MM-DD>-<slug>-report.md      (execution report)
```

One folder per feature. Flat contents inside. Filename suffix signals type.

## Why this shape

- "Show me everything for X" becomes one folder to open. Today it is four.
- Sharing or archiving a feature is one folder to zip.
- The two-dir structure (reviews + features) reads in one glance. Reviews stays flat because it is a sequential log, not a per-topic collection.
- Filename suffix already exists (`-design`, `-plan`, `-outline`, `-manifest`, `-report`); no rename churn.

## Internal layout of a feature folder

Flat. No subfolders. Listing alphabetically sorts chronologically; the suffix tells you the type. The alternative (subfolders per artifact type) costs the nesting `features/<feature>/plans/` and adds zero information because the suffix already disambiguates.

## Path mapping (the only renames)

| Old | New |
|-----|-----|
| `docs/artifacts/specs/<feature>/<file>` | `docs/artifacts/features/<feature>/<file>` |
| `docs/artifacts/plans/<feature>/<file>` | `docs/artifacts/features/<feature>/<file>` |
| `docs/artifacts/multi-plans/<feature>/<file>` | `docs/artifacts/features/<feature>/<file>` |
| `docs/artifacts/reports/<feature>/<file>` | `docs/artifacts/features/<feature>/<file>` |
| `docs/artifacts/reviews/<file>` | `docs/artifacts/reviews/<file>` (no change) |

`docs/artifacts/plans/<feature>/` already lives at the target path; only the top-level `plans/` dir is renamed to `features/`. Filenames preserved exactly. No content rewrites beyond reference updates.

## Reviews/

Stays flat at the top level. Harvest reviews are a chronological log (`2026-07-03-harvest.md`, `2026-07-07-harvest.md`, `2026-07-12-harvest.md`), not grouped by topic. Promoting them into a `harvest/` feature folder would be churn for no benefit.

## What needs updating after the move

Every reference to the old paths becomes stale. Update in four batches:

1. **Active generators** (paths where new artifacts are written):
   - `agents/planner.md` (spec, plan)
   - `agents/documenter.md` (report)
   - `agents/orchestrator.md` (dispatches documenter)
   - `commands/full-cycle.md` (spec, plan, handoff line)
   - `commands/execute-plan.md` (spec, report)
   - `commands/harvest.md` (reviews - path unchanged)
   - `commands/multi-plan.md` (outline)
   - `skills/multi-plan-orchestration/SKILL.md` (outline, manifest)

2. **Layout documentation**:
   - `STANDARDS.md` (line 168)
   - `AGENTS.md` (line 181)
   - `agents/README.md` (roster rows)
   - `agents/standardizer.md` (audit brief)
   - `skills/code-standardization/SKILL.md` (mentions)
   - `commands/standardize.md` (scaffolds docs/artifacts/)
   - `docs/workflows/workflow.md` (multiple refs)
   - `docs/workflows/plan-flow.drawio` (path text in labels)
   - `docs/workflows/multi-plan-flow.drawio` (path text in labels)
   - `docs/workflows/stack.drawio` (if mentions docs/artifacts)

3. **Cross-references inside moved artifacts**: every `docs/artifacts/specs/X` / `docs/artifacts/multi-plans/X` / `docs/artifacts/reports/X` reference inside the moved files. Use grep to enumerate, fix mechanically. The `plans/` references inside moved files are already correct (plans -> features is just a top-level rename of the parent).

4. **Left as-is (historical)**:
   - `CHANGELOG.md` entries reference paths at the time they were written. History stays immutable.
   - References inside `docs/artifacts/reviews/*.md` (those reviews are themselves historical artifacts).

## Out of scope

- Renaming file suffixes (`-design` -> `-spec`, etc.). Filenames preserved.
- Redirect shims for old paths. None.
- Restructuring `docs/artifacts/reviews/`. Stays flat.
- Touching drawio visual layout. Only the embedded path text in labels.
- Adding new skills/agents/catalogs.

## Verification

After migration:

1. `git status` shows four old top-level dirs deleted (`specs/`, `plans/`, `multi-plans/`, `reports/`) and one new top-level dir created (`features/`). All artifact files moved via `git mv`.
2. `git grep -n 'docs/artifacts/specs/'` returns nothing.
3. `git grep -n 'docs/artifacts/multi-plans/'` returns nothing.
4. `git grep -n 'docs/artifacts/reports/'` returns nothing (except inside `docs/artifacts/reviews/` and `CHANGELOG.md`, which are historical and stay).
5. `git grep -n 'docs/artifacts/plans/'` returns nothing in active contexts (only historical entries in CHANGELOG/reviews if any).
6. `git grep -n 'docs/artifacts/reviews/'` returns existing references unchanged.
7. `git grep -n 'docs/artifacts/features/'` returns all the new references.
8. All previously-existing artifact files now live under `docs/artifacts/features/<feature>/`.
9. `docs/artifacts/` tree: only `reviews/` and `features/` at the top.
10. Skills, commands, agents, and workflow docs that referenced old paths now reference the new layout.

## Risks

- Cross-references in moved files are easy to miss. Mitigation: grep before commit.
- Drawio files embed path text in XML; edits must preserve XML well-formedness.
- Some references use brace-glob patterns like `docs/artifacts/{specs,plans,reviews}/` that need rephrasing, not mechanical replacement.
