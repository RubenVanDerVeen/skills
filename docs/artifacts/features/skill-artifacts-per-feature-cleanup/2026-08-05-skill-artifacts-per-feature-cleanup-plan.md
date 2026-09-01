# Plan: finish per-feature artifacts migration in project-standardization skill

**Date:** 2026-08-05
**Spec:** none (mechanical doc cleanup; this plan is self-contained and the user approved it directly on 2026-08-05).
**Goal:** Remove the 6 remaining stale references to the old type-bucket artifacts layout (`docs/artifacts/{specs,plans,reviews,reports}/` and the `specs/`, `plans/`, `reviews/` subdir tree) from the `project-standardization` skill. The canonical doc (`references/artifacts.md`) and all three `AGENTS-*.md` templates were already migrated to the per-feature layout on 2026-08-05; these 6 spots were missed.

The per-feature layout (source of truth: `skills/rubens-project-standardization/references/artifacts.md`):
```
docs/artifacts/
├── reviews/                        ← flat chronological log
└── features/<feature>/             ← one folder per feature, flat contents
    ├── YYYY-MM-DD-<topic>-design.md
    ├── YYYY-MM-DD-<topic>-plan.md
    ├── YYYY-MM-DD-<topic>-outline.md   (multi-plan)
    ├── YYYY-MM-DD-<topic>-manifest.md  (multi-plan)
    └── YYYY-MM-DD-<topic>-report.md
```

All edits are in `skills/rubens-project-standardization/`. No code changes. No new files.

## Task 1: apply the 6 doc edits

Branch: `docs/skill-artifacts-cleanup` cut from latest default branch.

Make exactly these 6 edits. Each `oldString` is unique within its file.

### Edit 1.1: `SKILL.md` core rule (line 41)

File: `skills/rubens-project-standardization/SKILL.md`

Replace:
```
- **Specs and plans live in the repo**: `docs/artifacts/{specs,plans,reviews,reports}/` committed alongside the code. **Override clause**: this wins over any per-framework default (superpowers, GSD, `.planning/`). See `references/artifacts.md` § Per-framework redirect for the redirect mechanics; redirect before files land elsewhere.
```
with:
```
- **Specs and plans live in the repo**: `docs/artifacts/features/<feature>/` (specs, plans, manifests, reports) plus `docs/artifacts/reviews/` (flat log), committed alongside the code. **Override clause**: this wins over any per-framework default (superpowers, GSD, `.planning/`). See `references/artifacts.md` § Per-framework redirect for the redirect mechanics; redirect before files land elsewhere.
```

### Edit 1.2: `references/bootstrap.md` step 6 (line 10)

This is the most consequential: the bootstrap checklist currently tells the agent to scaffold four subdirs that must not exist.

File: `skills/rubens-project-standardization/references/bootstrap.md`

Replace:
```
6. **Scaffold `docs/artifacts/`** (small when design history exists; medium when design history exists; large always): create `specs/`, `plans/`, `reviews/`, `reports/` per `references/artifacts.md`. At small and medium tiers, only create it the moment the first artefact is being written; never pre-create empty.
```
with:
```
6. **Scaffold `docs/artifacts/`** (small when design history exists; medium when design history exists; large always): create `features/` and `reviews/` per `references/artifacts.md` (per-feature layout: one folder per feature under `features/<feature>/`, flat review log under `reviews/`). At small and medium tiers, only create it the moment the first artefact is being written; never pre-create empty.
```

### Edit 1.3: `references/small.md` intro brace set (line 7)

File: `skills/rubens-project-standardization/references/small.md`

Replace:
```
`docs/artifacts/{specs,plans,reviews,reports}/` is **allowed** at this tier. Specs, plans, reviews, and reports are tied to features, not project size: a one-author utility can absolutely brainstorm a non-trivial change, write a plan for it, ship it, and commit a report of what shipped. Add `docs/artifacts/` the first time a real spec, plan, review, or report materialises, the same rule that applies to every tier. The layout below shows it as an optional directory; treat it as part of small projects the moment it becomes useful.
```
with:
```
`docs/artifacts/` is **allowed** at this tier. Specs, plans, reviews, and reports are tied to features, not project size: a one-author utility can absolutely brainstorm a non-trivial change, write a plan for it, ship it, and commit a report of what shipped. Add `docs/artifacts/` the first time a real spec, plan, review, or report materialises, the same rule that applies to every tier. The layout below shows it as an optional directory; treat it as part of small projects the moment it becomes useful.
```

### Edit 1.4: `references/small.md` directory tree (lines 18-22)

File: `skills/rubens-project-standardization/references/small.md`

Replace:
```
├── docs/                      ← optional, only if design history exists
│   └── artifacts/             ← specs, plans, reviews, reports (see references/artifacts.md)
│       ├── specs/
│       ├── plans/
│       └── reviews/
```
with:
```
├── docs/                      ← optional, only if design history exists
│   └── artifacts/             ← per-feature layout (see references/artifacts.md)
│       ├── features/<feature>/  ← specs, plans, manifests, reports for one feature
│       └── reviews/             ← flat review log
```

### Edit 1.5: `references/small.md` anti-pattern (line 118)

File: `skills/rubens-project-standardization/references/small.md`

Replace:
```
- Creating `docs/artifacts/{specs,plans,reviews,reports}/` empty. Create it the moment a spec, plan, review, or report is being written; do not pre-create it as scaffolding.
```
with:
```
- Creating `docs/artifacts/` empty. Create it the moment a spec, plan, review, or report is being written; do not pre-create it as scaffolding.
```

### Edit 1.6: `references/medium.md` "When to add" (line 136)

File: `skills/rubens-project-standardization/references/medium.md`

Replace:
```
Create `docs/artifacts/{specs,plans,reviews,reports}/` the first time any of these become true:
```
with:
```
Create `docs/artifacts/` (per-feature layout: `features/<feature>/` + flat `reviews/`) the first time any of these become true:
```

## Verification (run after the edits, before commit)

From the repo root:

1. `git grep -n "{specs,plans,reviews,reports}" -- skills/rubens-project-standardization/` returns **nothing**.
2. `git grep -n "artifacts/{specs\|artifacts/specs/\|artifacts/plans/\|artifacts/reports/" -- skills/rubens-project-standardization/` returns **nothing** (no old type-bucket paths).
3. The four files above parse as valid markdown (no broken fences): `SKILL.md`, `references/bootstrap.md`, `references/small.md`, `references/medium.md`.
4. Confirm `references/artifacts.md` was NOT touched (it is already correct).
5. No em-dashes introduced: `(Get-ChildItem -Recurse -Include *.md skills/rubens-project-standardization/ | Select-String -Pattern ([char]0x2014))` returns empty.

## Commit

Single commit on the branch, after verification passes:

```
docs(skills): finish per-feature artifacts migration in project-standardization

The 2026-08-05 migration to docs/artifacts/features/<feature>/ updated the
canonical references/artifacts.md and all three AGENTS-*.md templates but
missed 6 spots that still named the old type-bucket layout
({specs,plans,reviews,reports}). The bootstrap checklist was actively
mis-scaffolding four subdirs that no longer exist.

Updates SKILL.md core rule, bootstrap step 6, small.md (intro + directory
tree + anti-pattern), and medium.md "When to add".

Spec: docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-skill-artifacts-per-feature-cleanup-plan.md
```

## Out of scope

- Touching `references/artifacts.md` (already correct).
- Touching the `AGENTS-*.md` templates or `STANDARDS.md` (already correct).
- Frontmatter description wording in `SKILL.md` (L3 lists artifact *types* generically; acceptable).
- Any CHANGELOG entry (the migration CHANGELOG entry already exists from 2026-08-05; this is the cleanup tail).
