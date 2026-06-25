# `docs/artifacts/`: specs, plans, reviews

The `docs/artifacts/` directory holds **process meta-documents**: the design specs, implementation plans, and reviews that describe *how* the project is built: not the project's own deliverables.

Distinct from:

- `docs/source/`: editable source documents that become deliverables (PvE, design proposal, etc.).
- `docs/deliverables/`: generated exports of those sources.
- `docs/components/`: per-component user docs and test docs.
- `docs/research/`: IEEE-format research papers about the project's subject matter.

`docs/artifacts/` is about the **development process itself**.

## When to create `docs/artifacts/`

| Tier | When |
|------|------|
| small | Skip until a real spec, plan, or review materialises. |
| medium | Create when the first brainstorming session or repo review happens. |
| large | Create at bootstrap: sprints inevitably produce reviews. |

Empty `specs/ plans/ reviews/` subdirectories are fine once at least one of them is populated. Three empty subdirectories on a fresh project are decorative.

## Layout

```
docs/artifacts/
├── specs/
│   └── YYYY-MM-DD-<topic>-design.md
├── plans/
│   └── YYYY-MM-DD-<topic>-plan.md
└── reviews/
    ├── YYYY-MM-DD-<topic>-review.md        ← single-file reviews
    └── <topic>-review-<N>/                  ← multi-file reviews
        ├── <topic>-audit-data.md
        └── <topic>-review.md
```

## Specs: `docs/artifacts/specs/`

A **spec** documents the design decisions for a feature or change. Captures scope, architecture, tradeoffs, pre/post-deploy checklists. Written by the user (or by the agent via `brainstorming`) before implementation begins.

Filename: `YYYY-MM-DD-<kebab-topic>-design.md`. Date = the day brainstorming happened. Topic = the feature being designed.

Examples:

```
docs/artifacts/specs/2026-04-17-nextcloud-nas-integration-design.md
docs/artifacts/specs/2026-05-02-auth-oauth-migration-design.md
docs/artifacts/specs/2026-05-08-strawberry-detection-pipeline-design.md
```

### Spec rules

- Specs are **append-only context**. Don't delete after the feature ships: they document intent for future readers.
- If the design changes mid-implementation, **update the existing spec in place** + add a `## Amendments` section at the top with the date and reason. Do not create a second spec for the same topic.
- Specs are **not auto-loaded** into `AGENTS.md`. The agent reads them on demand when asked about historical design choices.
- Specs are committed alongside the code they describe: same commit when practical.

## Plans: `docs/artifacts/plans/`

A **plan** is a step-by-step implementation plan with review checkpoints. Written by the user (or by the agent via `writing-plans`) after the spec is approved, before code is written.

Filename: `YYYY-MM-DD-<kebab-topic>-plan.md`. Date = the day the plan was written. Topic should match the corresponding spec.

```
docs/artifacts/plans/2026-04-17-nextcloud-nas-integration-plan.md
docs/artifacts/plans/2026-05-02-auth-oauth-migration-plan.md
```

### Plan rules

- Each plan references its spec by file path.
- Plans are consumed during execution (`executing-plans` or `subagent-driven-development`). Once executed, the plan stays as historical record.
- Like specs: not auto-loaded, committed with the code, never deleted post-implementation.

## Reviews: `docs/artifacts/reviews/`

A **review** is any committed audit of the project itself: repo structure audits, sprint planning reviews, standards compliance audits, code reviews that warrant persistence beyond a PR comment.

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
| `<artefact-type>` | `design`, `plan`, `review`, `audit` |

Examples:

```
✅ 2026-04-17-nextcloud-nas-integration-design.md
✅ 2026-05-09-repo-structure-audit.md
✅ 2026-05-11-standards-compliance-audit.md
❌ 17-04-2026-NextcloudNasIntegration_Design.md
❌ design-nextcloud-nas-integration-2026-04-17.md   (date must be first)
❌ NextcloudNAS_design.md                            (no date, no kebab-case)
```

## Workflow

1. **Brainstorm** (`brainstorming` skill) → outputs a spec in `docs/artifacts/specs/`.
2. User reviews spec, approves.
3. **Write plan** (`writing-plans` skill) → outputs a plan in `docs/artifacts/plans/` referencing the spec.
4. User reviews plan, approves.
5. **Execute** (`executing-plans` or `subagent-driven-development` skill) → consumes plan.
6. **Review** post-implementation if the change warrants it → adds a review to `docs/artifacts/reviews/`.

Each step's artefact is committed before the next step starts.

## Interaction with `AGENTS.md`

- `docs/artifacts/` files are **not** auto-imported into `AGENTS.md`. They are project history, not session context.
- Reference them on demand: "What was the original design for X?" → the agent greps `docs/artifacts/specs/` for the matching topic and reads that file.
- If a critical decision in a spec needs to be remembered cross-session (e.g. "we explicitly chose A over B because of constraint C"), capture that fact in a memory entry (`project_<topic>.md` at the active tool's memory location; see `references/memory.md`) **as well as** keeping the full spec in `docs/artifacts/specs/`.

## Anti-patterns

- Putting reviews in `.agents/reviews/`. Reviews are committed project history: `docs/artifacts/reviews/`. `.agents/` is for context files, not artefacts.
- Multiple specs for the same topic. Update the existing spec with an amendments section.
- Specs without dates. Date is mandatory: historical context depends on knowing when the decision was made.
- Specs without a topic slug. `2026-04-17-design.md` is ambiguous; `2026-04-17-nextcloud-nas-integration-design.md` is greppable.
- Empty `specs/ plans/ reviews/` for an entire project. Delete the empty ones, or be honest: the structure is decorative.
