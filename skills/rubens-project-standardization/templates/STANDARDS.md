# Project standards

Human-readable summary of the standards this repository follows. Aimed at contributors who do not use an AI coding agent or the `project-standardization` skill.

For the agent-facing operating notes (when to load which reference, bootstrap checklist, etc.), see the skill itself. **This file is the human contract; the skill is the agent contract.**

---

## Stack

Two layers: formal ISO/IEC/IEEE norms and industry conventions.

| Standard / convention   | Applied here? | Used for |
|-------------------------|---------------|----------|
| ISO/IEC/IEEE 26515:2018 | <yes / no>    | Agile documentation process |
| ISO/IEC/IEEE 26514:2022 | <yes / no>    | User-documentation structure |
| ISO/IEC/IEEE 29119-3:2021 | <yes / no>   | Test plan / spec / report templates |
| ISO/IEC/IEEE 15289:2019 | <yes / no>    | Lifecycle information items (source vs deliverable) |
| ISO 10007:2017          | <yes / no>    | Configuration management |
| ISO 8601                | **yes**       | `YYYY-MM-DD` filename prefix for time-based records |
| IEEE article format     | <yes / no>    | Research articles |
| Kebab-case ASCII paths  | **yes**       | All directory and filenames |
| English structural paths | **yes**      | Dir names in English; content may be Dutch |
| Conventional Commits 1.0.0 | **yes**    | Commit messages |
| Keep a Changelog 1.1.0  | **yes**       | `CHANGELOG.md` format |

Mark each row `yes` / `no` per what is actually in force here. Delete rows that do not apply.

---

## Naming rules: the floor

These apply to every file and directory.

### Kebab-case ASCII

Lowercase letters, digits, and hyphens only. No spaces, no underscores, no PascalCase, no non-ASCII characters.

```
✅ remote-controller/
✅ deployment-diagram.drawio
✅ esp32-c3-datasheet.pdf
❌ Remote Controller/
❌ Deployment_Diagram.drawio
❌ ESP32_C3_Datasheet.pdf
```

Exceptions for conventional uppercase filenames: `README.md`, `AGENTS.md`, `CLAUDE.md` (one-line shim that `@import`s `AGENTS.md` for Claude Code, which does not read `AGENTS.md` natively), `CHANGELOG.md`, `STANDARDS.md`, `LICENSE`, `Makefile`, `Cargo.toml`, `package.json`. Everything else is kebab-case.

### English structural paths

Directory and file **names** in English. Document **content** may be Dutch where the deliverable requires it. Dutch acronyms that are the proper name of a deliverable (`pve`, `top`) are permitted.

### ISO 8601 date prefix

Time-based records start with the date:

```
✅ 2026-05-09-standup.md
✅ 2026-05-06-sprint-retrospective.md
❌ Standup_2026-05-09.md
❌ 09-05-2026-standup.md
```

The date must come first so sort-by-filename produces chronological order.

---

## Commit messages: Conventional Commits 1.0.0

Format: `<type>(<scope>): <description>`.

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

```
✅ feat(remote-controller): add wireless pairing
✅ fix(motor): correct current calculation
✅ docs(readme): translate to English
❌ Update stuff
❌ wip
```

Scope is the **module or component**, not the discipline. `feat(remote-controller)` not `feat(electrical)`.

Enforcement: a tracked `commit-msg` hook (`.githooks/commit-msg`) rejects non-conforming subjects. Activate once per clone: `git config core.hooksPath .githooks` (installed by the `project-standardization` bootstrap, step 10).

---

## Changelog: Keep a Changelog 1.1.0

`CHANGELOG.md` at repo root. Grouped by version (semver) or milestone (sprint). Sections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

See `CHANGELOG.md` for the current state.

---

## Repository layout

<Describe the actual directory layout. For small projects, a few lines. For medium/large, the full structure tree. Example for a discipline-monorepo:>

```
project-root/
├── README.md
├── CHANGELOG.md
├── STANDARDS.md                    ← this file
├── AGENTS.md                       ← agent context file (auto-loaded)
├── mechanical/                     ← <discipline> ownership
├── electrical/                     ← <discipline> ownership
├── software/                       ← <discipline> ownership
├── .agents/                        ← on-demand agent context files
├── docs/
│   ├── source/                     ← editable source documents
│   ├── deliverables/               ← per-sprint exports
│   ├── components/                 ← per-component docs
│   ├── project-management/         ← SCRUM artefacts
│   └── artifacts/                  ← specs, plans, reviews
└── reference/                      ← provided, read-only material
```

---

## Source vs deliverable

One authoritative source per document. Generated artefacts (PDF, DOCX) live in `docs/deliverables/<sprint>/`, never alongside the source.

- Source files (Typst, Markdown) → `docs/source/<format>/<topic>/`.
- Generated exports → `docs/deliverables/sprint<N>-<topic>/`.

A `.docx` of a Typst-sourced document is **not** a source. It is a deliverable.

---

## Specs, plans, reviews

`docs/artifacts/` holds process meta-documents:

- `docs/artifacts/specs/YYYY-MM-DD-<topic>-design.md`: design specs.
- `docs/artifacts/plans/YYYY-MM-DD-<topic>-plan.md`: implementation plans.
- `docs/artifacts/reviews/YYYY-MM-DD-<topic>-review.md`: audits and reviews.
- `docs/artifacts/reports/YYYY-MM-DD-<topic>-report.md`: execution reports for completed plans.

When a single topic produces multiple specs and plans (split flow, parallel agents), group them under a `<topic>/` subfolder:

- `docs/artifacts/multi-plans/<topic>/YYYY-MM-DD-<topic>-outline.md`: decomposition outline.
- `docs/artifacts/multi-plans/<topic>/YYYY-MM-DD-<topic>-manifest.md`: dispatch manifest.
- `docs/artifacts/specs/<topic>/YYYY-MM-DD-<foundation>-design.md`: foundation spec.
- `docs/artifacts/specs/<topic>/YYYY-MM-DD-<sp-N>-<name>-design.md`: sub-project specs.
- `docs/artifacts/plans/<topic>/YYYY-MM-DD-<foundation>-plan.md`: foundation plan.
- `docs/artifacts/plans/<topic>/YYYY-MM-DD-<sp-N>-<name>-plan.md`: sub-project plans.

Single-plan topics stay flat. Multi-plan topics get a subfolder. See `references/artifacts.md`.

Each is append-only history. If a spec changes mid-implementation, edit in place + add an `## Amendments` section. Do not create a second spec for the same topic.

---

## Forbidden patterns

- No `temp/`, no `old/`, no `archive/` directories. Git history is the archive.
- No secrets in tracked files. `.env`, tokens, passwords stay out of git.
- No PascalCase or spaces in any filename. Rename on import.
- No source + generated PDF in the same directory. Source ↔ deliverables split is non-negotiable.
- No Diátaxis-style `docs/{tutorials,how-to,reference,explanation}/` as the primary structure. Evaluated and rejected.

---

## References

- Full standards-stack rationale: `docs/research/<paper>.pdf` <or omit if no paper exists>.
- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
- Keep a Changelog 1.1.0: <https://keepachangelog.com/en/1.1.0/>
- ISO 8601 date format: <https://www.iso.org/iso-8601-date-and-time-format.html>
- `AGENTS.md` convention: <https://agents.md>
