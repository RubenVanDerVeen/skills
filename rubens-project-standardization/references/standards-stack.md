# Standards stack

The user's projects follow an explicit two-layer standards stack: formal ISO/IEC/IEEE norms plus four industry conventions. The full justification: with citations and design-decision history: lives in the research paper `Project standaarden pakket voor het IDP-project` (v1.0, Ruben van der Veen, 2026-05-11). This document is the operational summary for AI coding agents.

**Scope reminder:** the conventions layer (kebab-case, English paths, ISO 8601 prefix, Conventional Commits, Keep a Changelog) applies to **most** projects regardless of size. The ISO/IEC/IEEE norms are opt-in per project. A simple tool typically adopts only naming + commits + changelog; a homelab adopts naming + commits + changelog + maybe ISO 10007 config thinking; a school engineering project adopts the full stack.

## Layer 1: Formal ISO/IEC/IEEE norms

### ISO/IEC/IEEE 26515:2018: Agile documentation process

Defines how to integrate user documentation into agile sprints: docs as backlog items, doc reviews integrated with sprint reviews, per-sprint doc baselines.

**Apply when:** project runs sprints with formal deliverables. School projects always; team tool projects often; solo tools no.

**How:** treat doc work as backlog items with their own Definition of Done. Each feature ships with corresponding doc updates in `docs/source/`. Per-sprint exports go to `docs/deliverables/sprint<N>-<topic>/`. Retrospectives go to `docs/project-management/retrospectives/`.

### ISO/IEC/IEEE 26514:2022: User documentation structure & quality

Defines the structure of user-facing information: information architecture, topic types, navigation, consistency. Each user-doc topic has purpose, usage context, tasks, reference info, error handling where relevant.

**Apply when:** the project ships a user-facing artefact (manual, runbook, component documentation). School + tool projects yes; pure libraries with docstrings no.

**How:** `docs/source/` and `docs/components/<component>/manuals/` use standard sections (installation, operation, maintenance, troubleshooting). Terminology is consistent across all docs.

### ISO/IEC/IEEE 29119-3:2021: Test documentation

Defines templates for the four test-doc artefact types: Test Plan, Test Design Specification, Test Case Specification, Test Report. Successor to the older IEEE 829.

**Apply when:** the project has formal testing (unit, integration, system, acceptance) that needs to be defensible to a third party: assessors, auditors, customers. School projects yes. Internal tools usually no; the test code itself is the documentation.

**How:** for each test level, maintain artefacts matching the four 29119-3 templates. Component-level tests go under `docs/components/<component>/test/`. System-level tests go under `tests/` or `docs/source/tests/`. Filenames reflect the artefact type: `remote-controller-test-design-spec.md`, `remote-controller-test-report-sprint-3.md`.

### ISO/IEC/IEEE 15289:2019: Lifecycle information items

Defines the purpose and content of lifecycle information items (plans, design descriptions, reports). Describes how items can be combined, split, or held in repositories.

**Apply when:** projects with formal deliverable types that must be linked to lifecycle phases. Always at large tier; sometimes at medium.

**How:** each main document in `docs/source/` is treated as a lifecycle information item with a clear purpose and bounded scope. Per-sprint baselines live in `docs/deliverables/sprint<N>-<topic>/`; editable sources stay in `docs/source/`. `docs/research/` and `docs/project-management/` group items by purpose.

### ISO 10007:2017: Configuration management

Defines configuration management: identifying configuration items, controlling changes, status accounting, audits.

**Apply when:** any project where multiple artefacts must stay consistent and where confusion about "which is the source" causes real problems. Large always; medium usually; small only when shipping versioned releases.

**How:**
- The repository **is** the configuration management system. Top-level dirs (`mechanical/`, `electrical/`, `software/`, `docs/`, `reference/`) are configuration items or groupings.
- Each CAD model, schematic, PCB layout, firmware module, or key document has **exactly one** authoritative source location.
- No `temp/`, no `old/`, no `archive/`. Git history is the version history.
- Source vs generated rules are explicit (e.g. Typst source in `docs/source/typst/`, generated PDF in `docs/deliverables/`).

### ISO 8601: Date format

Defines `YYYY-MM-DD` as the unambiguous international date format.

**Apply when:** always. Universal.

**How:** all time-based document filenames use the ISO 8601 prefix:

```
✅ 2026-05-09-standup.md
✅ 2026-05-06-sprint-retrospective.md
❌ Standup_2026-05-09.md
❌ 09-05-2026-standup.md
❌ 9may2026.md
```

The prefix must be first so sort-by-filename produces chronological order: that's the entire reason for the rule.

### IEEE article format

IEEE's formal guidelines for scientific articles and conference papers: two-column 10pt Times New Roman, 24pt centred title, structured abstract + index terms, Roman-numeral section headings (I, II, III, …), numbered references in IEEE citation style.

**Apply when:** the project produces research output that should be directly reusable in actual IEEE venues. School engineering projects yes (training the team in real paper formatting); tool projects usually no.

**How:** research documents in `docs/research/` use the IEEE template (the user's Typst library `@local/typst-tools` ships `ieee-journal.typ` for this). Standard sections (Introduction, Methods, Results, Discussion, Conclusion). IEEE reference style throughout.

## Layer 2: Industry conventions

These apply to **most** projects regardless of tier. They are the floor.

### kebab-case ASCII-only paths

Lowercase letters, digits, and hyphens. No spaces, no underscores, no PascalCase, no non-ASCII characters.

```
✅ remote-controller/
✅ deployment-diagram.drawio
✅ esp32-c3-datasheet.pdf
❌ Remote Controller/
❌ Deployment Diagram.drawio
❌ ESP32_C3_Datasheet.pdf
❌ remote_controller/
```

**Why:** cross-platform safe (Windows / macOS / Linux), URL-safe, shell-safe, sorts consistently, no case-sensitivity bugs on case-insensitive filesystems.

**Exceptions:** conventional uppercase filenames are kept: `README.md`, `AGENTS.md`, `CLAUDE.md` (legacy alias for Claude Code), `CHANGELOG.md`, `LICENSE`, `Makefile`, `Cargo.toml`, `package.json`. Anything else is kebab-case.

### English structural paths

Directory and file names in English. Dutch acronyms that are the proper name of a deliverable (`pve` = Programma van Eisen, `top` = Technisch Ontwerp Portfolio) are permitted as path segments.

```
✅ docs/research/
✅ docs/meeting-minutes/
✅ docs/source/typst/subdocuments/pve.typ
❌ docs/Onderzoek/
❌ docs/notulen/
❌ docs/PvE's/
```

**Why:** universal collaboration, tool compatibility, future-proofing. Content inside files may be Dutch where the deliverable requires it; structural paths are English so a non-Dutch reader can still navigate.

### Discipline-based monorepo (large only)

For multidisciplinary engineering projects, the top level splits by discipline (`mechanical/`, `electrical/`, `software/`) plus shared areas (`docs/`, `reference/`, `tests/`). Inspired by ROS Industrial and Open Compute Project layouts.

For non-multidisciplinary projects, replace with the relevant top-level partitioning (`backend/`, `frontend/`, `infra/`).

### Conventional Commits 1.0.0

Format: `<type>(<scope>): <description>`.

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`.

```
✅ feat(arm): add inverse-kinematics solver
✅ fix(motor): correct current calculation
✅ docs(readme): translate to English
❌ Update stuff
❌ wip
```

**Why:** machine-parseable history, automation-friendly (release notes, version bumps), traceable changes per configuration item (ties into ISO 10007).

### Keep a Changelog 1.1.0

Human-readable `CHANGELOG.md` at repo root. Grouped by version (semver) or milestone (sprint). Sections per change type: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

```markdown
# Changelog

## [Unreleased]
### Added
- _TBD_: feature X for sprint 3

## [Sprint 2]: 2026-05-13
### Added
- Test Plan for remote-controller
### Changed
- Renamed standups to ISO 8601 prefix
```

**Why:** documents what shipped, when, and at what milestone. Together with Conventional Commits, gives a complete change history.

## Diátaxis: evaluated and rejected

The Diátaxis framework (Daniele Procida) organises documentation into four quadrants: tutorials, how-to guides, reference, explanation. It is well-suited for product documentation where users come with one of four needs.

**Evaluated but not adopted as the primary organising structure** for the user's projects. Reasoning:

1. School deliverables are defined by **document type and discipline** (PvE, design proposal, patent research, manuals, test documentation), not by user-need category. Forcing a Diátaxis structure scatters related documents across four top-level dirs.
2. Project assessors and new team members navigate by component or deliverable, not by "I want a tutorial".
3. ISO 15289 (lifecycle info items) groups items by **purpose and lifecycle phase**, not by user need: which conflicts with Diátaxis as a primary structure but aligns with the document-type approach used here.

Diátaxis concepts are still used **inside individual documents** (separating conceptual background from step-by-step procedures), just not as the top-level repo layout.

## How to apply this stack to a new project

1. **Always apply:** kebab-case ASCII paths, English structural paths, ISO 8601 date prefix, Conventional Commits, Keep a Changelog. These are the floor: small to large, every project.
2. **Apply when relevant:** ISO 10007 (configuration management thinking) for any project with multiple artefact types that must stay in sync. Typically medium and large.
3. **Apply for team / formal projects:** ISO 26515 (agile docs), ISO 26514 (user docs), ISO 29119-3 (test docs), ISO 15289 (lifecycle info items). Large tier defaults; medium tier when graduating.
4. **Apply when shipping research:** IEEE article format. Usually large tier only.

State which standards are being applied in the project's `README.md` under a "Project standards stack" section. This makes the choice auditable and gives future contributors a starting point.

## Anti-patterns

- Adopting the full stack on a 200-line utility. Overhead exceeds benefit.
- Adopting only naming + commits but not source/deliverable separation on a project with both. The split is what makes the standards claim defensible.
- Naming files with timezone-suffixed dates (`2026-05-09T10:00+0200-standup.md`). Use plain `YYYY-MM-DD`: the time is in the file content if needed.
- Mixing kebab-case and snake_case in the same tree to "preserve external naming" (e.g. `esp32_c3.pdf` next to `dw01a.pdf`). Pick kebab; rename externals on import.
- Putting Conventional Commits scope as the discipline name (`feat(electrical): ...`). Scope should be the **module or component**, not the discipline (`feat(remote-controller): ...`).
- Documenting standards adoption in `AGENTS.md` instead of `README.md`. `AGENTS.md` is for agent operating notes; `README.md` is the auditable, human-facing standards declaration.
