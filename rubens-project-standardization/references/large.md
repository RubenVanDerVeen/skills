# Large project pattern

Team projects with sprints, formal deliverables, multi-discipline content. The canonical example is `Schoolprojects/Aardbei-Plukkers` — an NHL Stenden IDP team project with mechanical / electrical / software disciplines, sprints, a research-paper-backed standards stack, and a graded portfolio.

The goal is **a layered context: slim auto-load, rich on-demand `claude/`, committed design history in `docs/artifacts/`, and a configuration-managed `docs/` tree for sources, deliverables, components, and project-management artefacts.**

## Directory layout

```
project-root/
├── README.md                          ← user-facing, English, references standards stack
├── CLAUDE.md                          ← slim Claude entry point — auto-loaded
├── CHANGELOG.md                       ← Keep a Changelog, grouped by sprint
├── .gitignore
│
├── claude/                            ← Claude context (sub-files)
│   ├── todolist.md                    ← pending tasks (on-demand)
│   ├── censoring.md                   ← public/private sanitization (auto-load if relevant)
│   ├── <domain>.md                    ← per major area (auto-load if used every session)
│   └── <domain>/                      ← sub-dir when domain has 3+ sub-topics
│       ├── <sub>.md
│       └── <sub>.md
│
├── <discipline-1>/                    ← e.g. mechanical/  — owned by one discipline
│   ├── <subsystem>/
│   └── ...
├── <discipline-2>/                    ← e.g. electrical/
├── <discipline-3>/                    ← e.g. software/
├── tests/                             ← cross-discipline tests (ISO 29119-3)
│
├── docs/
│   ├── source/                        ← editable source documents (ISO 15289)
│   │   ├── typst/                     ← Typst sources for PvE, design proposal, research
│   │   └── word/                      ← Word docs when Typst is impractical
│   ├── deliverables/                  ← per-sprint exports (PDF / DOCX) — generated artefacts only
│   │   └── sprint<N>-<topic>/
│   ├── research/                      ← IEEE-format research articles
│   ├── components/                    ← per-component documentation
│   │   └── <component>/
│   │       ├── manuals/               ← user manuals (ISO 26514)
│   │       ├── test/                  ← test plans + reports (ISO 29119-3)
│   │       └── diagrams/              ← component diagrams
│   ├── project-management/            ← SCRUM artefacts (ISO 26515)
│   │   ├── daily-standups/            ← YYYY-MM-DD-standup.md
│   │   ├── retrospectives/
│   │   └── notes/                     ← meeting minutes
│   └── artifacts/                     ← process meta: specs, plans, reviews
│       ├── specs/
│       ├── plans/
│       └── reviews/
│
└── reference/                         ← provided, read-only material (never modify)
    ├── <category>/
    └── ...
```

The discipline directories at the top (`mechanical/`, `electrical/`, `software/`) reflect ownership boundaries. For non-school large projects, replace them with whatever the actual top-level partitioning is (`backend/`, `frontend/`, `infra/`, `mobile/`, etc.) — the principle is one top-level dir per major ownership boundary.

## `CLAUDE.md` content

Slim entry point. Target ~200 lines, ~3k tokens. Must contain:

1. **Overview** — what the project is, the team composition, the client/customer if relevant.
2. **Key facts** — milestone dates, hard constraints (regulatory, physical, deadline), client contact.
3. **Discipline boundaries** — which top-level dir is owned by whom.
4. **Standards stack reference** — one line: "follows `docs/research/<paper>.pdf`; see also `references/standards-stack.md` in the skill". Do not inline the standards table in `CLAUDE.md`; that lives in `README.md` and the research paper.
5. **Git & workflow rules** — Conventional Commits, Keep a Changelog, branch model.
6. **`@imports`** — only what is needed every session (usually: censoring, services if relevant, MCP if used).
7. **On-demand table** — every other `claude/` file.

The skeleton mirrors the medium tier; differences are:

- The reference table is bigger (often a milestone table + a discipline table + a service/component table).
- `@imports` are fewer because the standards live in `README.md` and the research paper, not duplicated into `CLAUDE.md`.
- The on-demand table is longer.

## `docs/` substructure — rationale per directory

| Directory | Purpose | Standard backing |
|-----------|---------|------------------|
| `docs/source/` | Editable source documents. Typst preferred; Word only where Typst is impractical (Bedrijfskunde, TOP templates from school). | ISO 15289 — lifecycle information items |
| `docs/deliverables/` | Generated PDF / DOCX exports per sprint. Never holds source — only exports. One sub-dir per sprint: `sprint<N>-<topic>/`. | ISO 15289 — per-sprint baselines |
| `docs/research/` | IEEE-format research articles. One PDF per research topic. | IEEE article format |
| `docs/components/<component>/` | Per-component documentation: manuals, test docs, diagrams. | ISO 26514 (manuals), ISO 29119-3 (test docs) |
| `docs/project-management/` | SCRUM artefacts: standups, retros, meeting minutes. ISO 8601 prefix on filenames. | ISO 26515 — agile docs process |
| `docs/artifacts/` | Process meta: brainstorming specs, implementation plans, repo / sprint / process reviews. | Project workflow (see `references/artifacts.md`) |
| `reference/` | Provided, read-only material from the client / school. Never modified. One top-level slot, not under `docs/`. | ISO 10007 — single authoritative location |

## Source vs deliverable split

Critical at this tier — also a recurring failure mode. The rules:

- A document has exactly **one** authoritative source. Typst (`.typ`) when possible; Word (`.docx`) when the school template forces it.
- Sources live in `docs/source/<format>/<topic>/`.
- Generated artefacts (PDF, DOCX exports) live in `docs/deliverables/sprint<N>-<topic>/`.
- Never commit both the source and a sibling PDF in the same directory.
- The `.docx` of a Typst-sourced document is not a "source" — it is a deliverable. Put it in `docs/deliverables/`.

## Standards stack — what to apply at this tier

Most ISO/IEC/IEEE norms from the standards stack apply at this tier (for school projects, all of them apply because the assessment expects it). Specifically:

- **ISO 26515** — docs as agile backlog items.
- **ISO 26514** — user-doc structure for manuals.
- **ISO 29119-3** — test plan / design spec / case spec / report templates.
- **ISO 15289** — lifecycle information items (source vs deliverable).
- **ISO 10007** — config management (one authoritative source, no `temp/`, no `old/`).
- **ISO 8601** — date prefix on time-based filenames.
- **IEEE article format** — research output.
- **Conventions** — kebab-case ASCII paths, English structural paths, discipline monorepo, Conventional Commits, Keep a Changelog.

See `references/standards-stack.md` for the full explanation and rationale.

## Sprint workflow

- Each sprint closes on a milestone deadline.
- At each close, the editable sources in `docs/source/` are exported to PDF / DOCX and committed to `docs/deliverables/sprint<N>-<topic>/`.
- A retrospective note is added to `docs/project-management/retrospectives/` (ISO 8601 prefix).
- `CHANGELOG.md` is updated: a new `## [Sprint N] — YYYY-MM-DD` section captures what landed.
- Test artefacts (plans / reports) for that sprint are committed under `docs/components/<component>/test/` and / or `tests/`.

## Components

For each major physical or logical component (e.g. `main-controller`, `remote-controller`, `arm`, `vision-pipeline`), create `docs/components/<component>/` with:

- `manuals/` — user-facing documentation (ISO 26514).
- `test/` — `plans/`, `design-spec/`, `case-spec/`, `reports/`. (ISO 29119-3.)
- `diagrams/` — block diagrams, state diagrams, sequence diagrams.

Empty subdirectories are fine if a component is in early stages, but each component should have **at least** one populated subdirectory before the next sprint closes — otherwise the structure is decorative.

## Memory

Cross-session memory at `~/.claude/projects/<slug>/memory/`. Large projects typically have:

- `user.md` — user role.
- `feedback_*.md` — behavioural rules.
- `project_*.md` — decisions, constraints, deadlines.
- `reference_*.md` — external systems (Plane, Blackboard, school portals).

See `references/memory.md`.

## What "large" looks like in practice — IDP annotated

```
project-idp/
├── README.md                          ← English, full standards-stack section, full structure tree
├── CLAUDE.md                          ← team, milestones, standards-stack reference, @imports
├── CHANGELOG.md                       ← grouped by sprint
│
├── mechanical/  electrical/  software/  tests/
│
├── docs/
│   ├── source/{typst,word}/           ← editable
│   ├── deliverables/sprint0-…/        ← per-sprint exports
│   ├── research/                      ← IEEE-format papers (incl. standards research)
│   ├── components/<component>/{manuals,test,diagrams}/
│   ├── project-management/{daily-standups,retrospectives,notes}/
│   └── artifacts/{specs,plans,reviews}/
│
└── reference/                         ← school-provided material, read-only
```

The full target structure is documented inside the project's `README.md` and is mirrored in the research paper at `docs/research/research-projectstandards.pdf` §14 Listing 1.

## Restructure from medium

When a medium project graduates to large, the migration is:

1. Add `mechanical/` / `electrical/` / `software/` (or whatever the discipline split is) at top level.
2. Add `docs/source/`, `docs/deliverables/`, `docs/components/`, `docs/project-management/`, `docs/artifacts/`.
3. Move existing editable sources into `docs/source/`. Move existing exports into `docs/deliverables/`.
4. Add `CHANGELOG.md` if not present.
5. Add `reference/` for provided material.
6. Keep `claude/` — but trim items that are now redundant with the new structure. For example: a `claude/repo-structure.md` becomes redundant once `README.md` documents the structure.

## Anti-patterns for large projects

- Empty skeleton directories with no content. If `docs/components/main-controller/` exists for two sprints with nothing in it, the standards claim ("we have component documentation") is hollow.
- Sources and generated PDFs side by side. Source → `docs/source/`. PDF → `docs/deliverables/`. Always.
- Standards stack inlined into `CLAUDE.md`. It belongs in `README.md` and the research paper. `CLAUDE.md` references it.
- Diátaxis structure (`tutorials/`, `how-to/`, `reference/`, `explanation/`) at the top of `docs/`. The standards stack explicitly rejects this for deliverable-driven projects. See `references/standards-stack.md` §Diátaxis.
- Mirroring directory naming between `docs/components/<component>/` and `software/<component>/`. They serve different purposes — `software/<component>/` is the source code, `docs/components/<component>/` is the documentation. Use the same component name in both, but do not collapse them.
- Adding `claude/project-standardization.md` to the project. Use this skill; do not duplicate it locally.
