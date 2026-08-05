# `docs/artifacts/`: per-feature layout

The `docs/artifacts/` directory holds **process meta-documents**: the design specs, implementation plans, multi-plan outlines and manifests, reviews, and execution reports that describe *how* the project is built: not the project's own deliverables.

Distinct from:

- `docs/source/`: editable source documents that become deliverables (PvE, design proposal, etc.).
- `docs/deliverables/`: generated exports of those sources.
- `docs/components/`: per-component user docs and test docs.
- `docs/research/`: IEEE-format research papers about the project's subject matter.

`docs/artifacts/` is about the **development process itself**.

## When to create `docs/artifacts/`

`docs/artifacts/` is **process metadata**, not project metadata. Specs, plans, and reviews are tied to features, not to team size or file count: a one-author utility can brainstorm a non-trivial change just as easily as a multi-team sprint produces one. The tier governs when the directory *appears*, not whether artefacts are allowed.

| Tier | When |
|------|------|
| small | Create the first time a spec, plan, or review is being written. Until then: skip. |
| medium | Create when the first brainstorming session or repo review happens. |
| large | Create at bootstrap: sprints inevitably produce reviews. |

`docs/artifacts/reviews/` and the first feature folder under `docs/artifacts/features/` appear the moment something is being written. Pre-creating both empty is decorative.

## Layout

Two top-level directories. Everything for one feature lives in one folder. Filename suffix signals type.

```
docs/artifacts/
├── reviews/
│   └── YYYY-MM-DD-<topic>-review.md          ← flat, chronological review log
└── features/
    └── <feature>/
        ├── YYYY-MM-DD-<topic>-design.md      ← spec
        ├── YYYY-MM-DD-<topic>-plan.md        ← plan
        ├── YYYY-MM-DD-<topic>-outline.md     ← multi-plan outline (optional)
        ├── YYYY-MM-DD-<topic>-manifest.md    ← multi-plan manifest (optional)
        └── YYYY-MM-DD-<topic>-report.md      ← execution report (after a plan ships)
```

A single feature folder usually holds the spec, the plan, and (after execution) the report. Multi-plan topics keep every related spec, plan, outline, and manifest inside one `features/<feature>/` folder; see § Multi-plan topic layout below.

## Features: `docs/artifacts/features/<feature>/`

A **feature** is one piece of work: a brainstormed change, a planned refactor, a shipped migration. Every artefact for that work lives under a single folder named after it. The folder is flat: there is no inner substructure for spec vs plan vs report because the filename suffix already disambiguates.

### Spec: `<feature>/<YYYY-MM-DD>-<topic>-design.md`

A **spec** documents the design decisions for a feature. Captures scope, architecture, tradeoffs, pre/post-deploy checklists. Written by the user (or by the agent via `brainstorming`) before implementation begins.

Filename: `YYYY-MM-DD-<kebab-topic>-design.md`. Date = the day brainstorming happened. Topic = the feature being designed.

Examples:

```
docs/artifacts/features/nextcloud-nas-integration/2026-04-17-nextcloud-nas-integration-design.md
docs/artifacts/features/auth-oauth-migration/2026-05-02-auth-oauth-migration-design.md
docs/artifacts/features/strawberry-detection-pipeline/2026-05-08-strawberry-detection-pipeline-design.md
```

### Spec rules

- Specs are **append-only context**. Don't delete after the feature ships: they document intent for future readers.
- If the design changes mid-implementation, **update the existing spec in place** + add a `## Amendments` section at the top with the date and reason. Do not create a second spec for the same topic.
- Specs are **not auto-loaded** into `AGENTS.md`. The agent reads them on demand when asked about historical design choices.
- Specs are committed alongside the code they describe: same commit when practical.

### Plan: `<feature>/<YYYY-MM-DD>-<topic>-plan.md`

A **plan** is a step-by-step implementation plan with review checkpoints. Written by the user (or by the agent via `writing-plans`) after the spec is approved, before code is written.

Filename: `YYYY-MM-DD-<kebab-topic>-plan.md`. Date = the day the plan was written. Topic should match the corresponding spec.

```
docs/artifacts/features/nextcloud-nas-integration/2026-04-17-nextcloud-nas-integration-plan.md
docs/artifacts/features/auth-oauth-migration/2026-05-02-auth-oauth-migration-plan.md
```

### Plan rules

- Each plan references its spec by file path (both live inside the same feature folder).
- Plans are consumed during execution (`executing-plans` or `subagent-driven-development`). Once executed, the plan stays as historical record.
- Like specs: not auto-loaded, committed with the code, never deleted post-implementation.

### Report: `<feature>/<YYYY-MM-DD>-<topic>-report.md`

An execution report closes out a completed plan: what the plan set out, what shipped, the standardization review, the documentation updates, verifier output, and the dispatch log. Written by the documenter subagent at the end of `/execute-plan` and `/full-cycle` runs.

Filename: `YYYY-MM-DD-<kebab-topic>-report.md`. Date matches the plan's date; topic matches the plan's topic.

```
docs/artifacts/features/nextcloud-nas-integration/2026-04-17-nextcloud-nas-integration-report.md
```

Reports are written by the documenter from the run's git state and the orchestrator's dispatch log; they are not authored by hand during normal development.

- An execution report belongs in the same `features/<feature>/` folder as the plan it closes out, with matching date and slug.
- Do not hand-write a report for work that has no plan. Reports document executed plans, not ad-hoc changes.

## Multi-plan topic layout

When a single topic produces multiple specs and plans (via `multi-plan-orchestration` or any other split flow), every related artefact still lives in one `features/<topic>/` folder. The folder is the unit of decomposition: foundation plus sub-projects all inside it, flat.

```
docs/artifacts/features/
└── learning-site-physics/                                    ← one feature, one folder
    ├── 2026-06-28-learning-site-physics-outline.md           ← orchestration outline
    ├── 2026-06-28-learning-site-physics-manifest.md          ← dispatch manifest
    ├── 2026-06-28-foundation-design.md                       ← foundation spec
    ├── 2026-06-28-foundation-plan.md                         ← foundation plan
    ├── 2026-06-28-sp-1-vectors-module-design.md              ← sub-project spec
    ├── 2026-06-28-sp-1-vectors-module-plan.md                ← sub-project plan
    ├── 2026-06-28-sp-2-calculators-module-design.md          ← sub-project spec
    └── 2026-06-28-sp-2-calculators-module-plan.md            ← sub-project plan
```

### Rules

- The folder name is a kebab-case slug, no date prefix. It groups all specs, plans, and orchestration artefacts for that topic.
- Files inside keep the standard `YYYY-MM-DD-<kebab-topic>-<type>.md` grammar.
- Two orchestration artefacts live alongside the specs and plans inside the same folder: `<topic>-outline.md` (the decomposition outline, approved before specs are written) and `<topic>-manifest.md` (the dispatch manifest, produced after all plans exist).
- When the `brainstorming` and `writing-plans` skills are delegated to per sub-project, pass the feature-scoped path explicitly. Both skills accept user-preferred locations as an override.
- Migrating existing flat artefacts: if a feature already has multiple flat specs/plans that should be grouped, move them into `features/<feature>/` in one commit. For an existing multi-plan topic split across `specs/<topic>/`, `plans/<topic>/`, and `multi-plans/<topic>/`, `git mv` all of those files into one `features/<topic>/` folder in a separate commit. No content changes.

## Reviews: `docs/artifacts/reviews/`

A **review** is any committed audit of the project itself: repo structure audits, sprint planning reviews, standards compliance audits, code reviews that warrant persistence beyond a PR comment. Reviews stay flat at the top level: they form a chronological log, not a per-topic collection.

### Two layout patterns

**Single-file reviews**: most common. Date-prefixed flat file:

```
docs/artifacts/reviews/2026-05-08-top-review.md
docs/artifacts/reviews/2026-05-09-repo-structure-audit.md
docs/artifacts/reviews/2026-05-11-standards-compliance-audit.md
```

**Multi-file reviews**: when a review includes raw data, multiple supporting documents, or per-sprint comparisons. Use a subdirectory:

```
docs/artifacts/reviews/plane-review-1/
├── plane-audit-data.md
└── plane-sprint-planning-review.md

docs/artifacts/reviews/plane-review-2/
├── plane-audit-data.md
└── plane-sprint-planning-review.md
```

Subdirectory names omit the date: instead use `-<N>` suffixes for iterations of the same review type. The review files inside can still have ISO 8601 prefixes if individually dated.

### Review rules

- Reviews are **committed**, not stored in chat history or memory.
- Repo-structure audits, standards-compliance audits, and project-structure reviews go here, **not** under `.agents/`.
- Reviews are not auto-loaded; read on demand when revisiting findings or comparing to a later audit.
- When a review supersedes an earlier one (e.g. `2026-05-09-repo-structure-audit.md` followed by `2026-05-11-standards-compliance-audit.md`), do not delete the older review: both stay so the audit trail is preserved.

## Filename grammar

```
YYYY-MM-DD-<kebab-topic>-<artefact-type>.md
```

| Token | Rules |
|-------|-------|
| `YYYY-MM-DD` | ISO 8601 date: the day the artefact was written, not the day the feature was deployed |
| `<kebab-topic>` | Short kebab-case slug matching the feature, e.g. `nextcloud-nas-integration`, `auth-oauth-migration`, `repo-structure` |
| `<artefact-type>` | `design` (spec), `plan`, `outline`, `manifest`, `report`, `review`, `audit` |

Examples:

```
✅ docs/artifacts/features/nextcloud-nas-integration/2026-04-17-nextcloud-nas-integration-design.md
✅ docs/artifacts/reviews/2026-05-09-repo-structure-audit.md
✅ docs/artifacts/reviews/2026-05-11-standards-compliance-audit.md
❌ 17-04-2026-NextcloudNasIntegration_Design.md
❌ design-nextcloud-nas-integration-2026-04-17.md   (date must be first)
❌ NextcloudNAS_design.md                            (no date, no kebab-case)
```

## Per-framework redirect

Several planning frameworks ship their own default artifact paths. None of those paths are authoritative for projects following this convention. **Redirect every spec, plan, outline, manifest, and report to `docs/artifacts/features/<feature>/`**; redirect every review to `docs/artifacts/reviews/`. Origin framework does not matter.

### Default vs canonical

| Framework skill | Default path | Canonical path |
|---|---|---|
| superpowers `brainstorming` | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | `docs/artifacts/features/<feature>/YYYY-MM-DD-<topic>-design.md` |
| superpowers `writing-plans` | `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` | `docs/artifacts/features/<feature>/YYYY-MM-DD-<topic>-plan.md` |
| GSD `.planning/` family | `.planning/specs/`, `.planning/plans/` | `docs/artifacts/features/<feature>/` (specs + plans) |
| Any other framework | framework-native default | `docs/artifacts/features/<feature>/` for specs/plans/reports, `docs/artifacts/reviews/` for reviews |

### Override pattern

Each skill accepts a target path as a user preference. **State the canonical path before the skill writes the file**, or move the artifact straight after. Two working shapes:

- **Pre-write override**: when delegating to `superpowers:brainstorming` or `superpowers:writing-plans`, name the canonical path in the delegation prompt. Both skill bodies explicitly support this: each ends its default-path line with *"User preferences for spec/plan location override this default"*. The agent that delegates is expected to honour that.
- **Post-write redirect**: if the skill already wrote to its default path before the override was honoured, `git mv` the file into `docs/artifacts/` in the same commit. Never leave both versions. Two homes rot fast, and you will forget which one is current.

GSD and other frameworks follow the same shape: name `docs/artifacts/features/<feature>/` in the delegation prompt, or move the file once it lands. The target is `docs/artifacts/features/<feature>/` (or `docs/artifacts/reviews/` for reviews) regardless of origin.

### Concrete example (superpowers)

User: "Brainstorm the foo feature."
Agent (after loading `superpowers:brainstorming`):

> "Saving the design doc to `docs/artifacts/features/foo/2026-06-29-foo-design.md` per the project's artifact convention."

User approves and the spec lands at the canonical path. Plan writing targets `docs/artifacts/features/foo/2026-06-29-foo-plan.md`. Reviews (when warranted) target `docs/artifacts/reviews/2026-06-29-foo-review.md`.

For multi-plan topics, apply the same redirect with the per-feature layout from § Multi-plan topic layout: `docs/artifacts/features/<feature>/<date>-<sub>-design.md`, `docs/artifacts/features/<feature>/<topic>-outline.md`, etc.

### Anti-patterns

- A `docs/superpowers/` (or `.planning/`, or any framework-native) directory ever landing in the repo. If it does, it is a missed redirect. **Move, never delete**: `git mv` its contents into `docs/artifacts/features/<feature>/` (or `docs/artifacts/reviews/` for review-shaped files), then remove the emptied dir. `git rm` only files that are true duplicates of something already at the canonical path.
- Two copies of the same spec or plan in different folders. Pick the canonical home and remove the other.
- Framework-default paths appearing as the target inside this skill's body, the templates, or any project's `AGENTS.md`.

## Workflow

1. **Brainstorm** (`brainstorming` skill) → outputs a spec in `docs/artifacts/features/<feature>/`.
2. User reviews spec, approves.
3. **Write plan** (`writing-plans` skill) → outputs a plan in the same `docs/artifacts/features/<feature>/` folder, referencing the spec.
4. User reviews plan, approves.
5. **Execute** (`executing-plans` or `subagent-driven-development` skill) → consumes plan.
6. **Review** post-implementation if the change warrants it → adds a review to `docs/artifacts/reviews/`.
7. **Document and report** (the documenter subagent at the end of `/execute-plan` or `/full-cycle`) -> writes an execution report to `docs/artifacts/features/<feature>/` (alongside the plan) and updates catalogs.

Each step's artifact is committed before the next step starts. **Step 1, 3, 6 must respect § Per-framework redirect** when the underlying skill ships its own default path.

## Interaction with `AGENTS.md`

- `docs/artifacts/` files are **not** auto-imported into `AGENTS.md`. They are project history, not session context.
- Reference them on demand: "What was the original design for X?" → the agent greps `docs/artifacts/features/<feature>/` for the matching topic and reads that file.
- If a critical decision in a spec needs to be remembered cross-session (e.g. "we explicitly chose A over B because of constraint C"), capture that fact in a memory entry (`project_<topic>.md` at the active tool's memory location; see `references/memory.md`) **as well as** keeping the full spec under `docs/artifacts/features/<feature>/`.

## Anti-patterns

- Putting reviews in `.agents/reviews/`. Reviews are committed project history: `docs/artifacts/reviews/`. `.agents/` is for context files, not artefacts.
- Splitting one feature's artefacts across four type-bucket subdirs (`specs/`, `plans/`, `multi-plans/`, `reports/`) instead of one `features/<feature>/` folder. The per-feature layout exists precisely to avoid this.
- Multiple specs for the same topic. Update the existing spec with an amendments section.
- Specs without dates. Date is mandatory: historical context depends on knowing when the decision was made.
- Specs without a topic slug. `2026-04-17-design.md` is ambiguous; `2026-04-17-nextcloud-nas-integration-design.md` is greppable.
- Empty `reviews/` plus an empty `features/` for an entire project. Delete the empty ones, or be honest: the structure is decorative.
