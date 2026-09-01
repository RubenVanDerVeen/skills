# Project standards

Human-readable summary of the standards this repository follows. Aimed at contributors who do not use an AI coding agent or the `project-standardization` skill.

For the agent-facing operating notes (when to load which reference, bootstrap checklist, etc.), see the skill itself. **This file is the human contract; the skill is the agent contract.**

---

## Stack

Two layers: formal ISO/IEC/IEEE norms and industry conventions.

| Standard / convention   | Applied here? | Used for |
|-------------------------|---------------|----------|
| ISO/IEC/IEEE 26515:2018 | no            | Agile documentation process (no sprints in this repo) |
| ISO/IEC/IEEE 26514:2022 | no            | User-documentation structure (no user manuals) |
| ISO/IEC/IEEE 29119-3:2021 | no          | Test plan / spec / report templates (no formal tests) |
| ISO/IEC/IEEE 15289:2019 | no            | Lifecycle information items (no deliverables) |
| ISO 10007:2017          | no            | Configuration management (single-source repo, not formally adopted) |
| ISO 8601                | **yes**       | `YYYY-MM-DD` filename prefix for time-based records (none used currently) |
| IEEE article format     | no            | Research articles (none produced) |
| Kebab-case ASCII paths  | **yes**       | All directory and filenames |
| English structural paths | **yes**     | Dir names in English; content may be Dutch where applicable |
| Conventional Commits 1.0.0 | **yes**    | Commit messages |
| Keep a Changelog 1.1.0  | **yes**       | `CHANGELOG.md` format |

This is a content-only agent environment repo (skills, slash commands, agent definitions). Most formal norms are not adopted; the conventions layer is the floor.

---

## Naming rules: the floor

These apply to every file and directory.

### Kebab-case ASCII

Lowercase letters, digits, and hyphens only. No spaces, no underscores, no PascalCase, no non-ASCII characters.

```
✅ drawio-pro/
✅ typst-pro/templates/ieee-journal.typ
✅ remote-controller/SKILL.md
❌ Drawio Pro/
❌ typst_pro/
❌ RemoteController/
```

Exceptions for conventional uppercase filenames: `README.md`, `AGENTS.md`, `CLAUDE.md` (one-line shim that `@import`s `AGENTS.md` for Claude Code, which does not read `AGENTS.md` natively), `CHANGELOG.md`, `STANDARDS.md`, `LICENSE`. Everything else is kebab-case.

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
✅ feat(typst-pro): add IEEE journal template
✅ fix(drawio-pro): correct pastel palette hex
✅ docs(readme): translate to English
❌ Update stuff
❌ wip
```

Scope is the **skill folder or repo area** the change touches (`typst-pro`, `drawio-pro`, `readme`, `agents`).

Enforcement: tracked git hooks in `.githooks/` (commit-msg for Conventional Commits; pre-commit for markdown and skill-structure rules). Activate once per clone: `git config core.hooksPath .githooks` (see `opencode-install.md` step 10).

---

## Changelog: Keep a Changelog 1.1.0

`CHANGELOG.md` at repo root. Grouped by content milestone for this continuous-delivery catalog. Sections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

See `CHANGELOG.md` for the current state.

---

## Repository layout

```
skills/
├── README.md                              <- user-facing
├── AGENTS.md                              <- skill catalog spec, auto-loaded by agents
├── CLAUDE.md                              <- one-line shim that @imports AGENTS.md
├── CHANGELOG.md                           <- this file's sibling
├── STANDARDS.md                           <- this file
├── opencode-install.md                    <- discoverable install doc (also a skill)
├── external-skills.md                     <- discoverable external catalog (also a skill)
├── docs/                                  <- workflow notes and artifacts
├── .gitattributes                         <- forces LF on .githooks/* (shebang safety)
├── .gitignore
├── .githooks/
│   ├── pre-commit                         <- doc-standards enforcement hook
│   └── commit-msg                         <- Conventional Commits enforcement hook
├── .claude/                               <- Claude Code tool settings (project)
├── commands/                              <- all slash commands live here
│   ├── goal.md
│   ├── execute-plan.md
│   ├── iterate-skill.md
│   ├── harvest.md
│   ├── multi-plan.md
│   ├── standardize.md
│   └── standardize-migrate.md
│
├── agents/                                <- opencode agent definitions
│   ├── README.md
│   ├── orchestrator.md
│   ├── executor.md
│   └── reviewer.md
│
└── skills/                                <- one skill per folder
    ├── drawio-pro/
    │   ├── SKILL.md
    │   └── references/
    ├── typst-pro/
    │   ├── SKILL.md
    │   └── references/
    ├── altium-pro/
    │   ├── SKILL.md
    │   └── references/
    ├── synctool-sync/
    │   └── SKILL.md
    ├── deep-research/
    │   ├── SKILL.md
    │   ├── references/
    │   └── templates/
    ├── rubens-project-standardization/
    │   ├── SKILL.md
    │   ├── references/
    │   └── templates/
    ├── multi-plan-orchestration/
    │   └── SKILL.md
    └── skill-harvest/
        ├── SKILL.md
        └── references/
```

A skill lives in a folder under `skills/`. A folder without `SKILL.md` is not a skill. Top-level `.md` files are repo docs, not skills, with two exceptions (`opencode-install.md` and `external-skills.md` double as discoverable skills).

---

## Source vs deliverable

Not applicable in the strict sense: this catalog has no per-sprint exports or generated artefacts. The closest analogue is "skill source vs agent context": `AGENTS.md` and `STANDARDS.md` are the source, individual `SKILL.md` files in each folder are the deliverables that agents consume.

---

## Specs, plans, reviews

`docs/artifacts/{features,reviews}/` holds the design history for non-trivial skills (e.g. `multi-plan-orchestration`, `skill-harvest`), per the `project-standardization` skill.

---

## Forbidden patterns

- No `temp/`, no `old/`, no `archive/` directories. Git history is the archive.
- No secrets in tracked files. Tokens, passwords, `.env` stay out of git.
- No PascalCase or spaces in any filename. Rename on import.
- No source + generated artefact in the same directory.
- No Diátaxis-style `docs/{tutorials,how-to,reference,explanation}/` as the primary structure. Evaluated and rejected.
- No top-level `.md` files other than the documented set (`README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `STANDARDS.md`, `opencode-install.md`, `external-skills.md`).

---

## References

- Full standards-stack rationale: research paper <https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project> (local copy at `docs/research/<paper>.pdf` when present).
- Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>
- Keep a Changelog 1.1.0: <https://keepachangelog.com/en/1.1.0/>
- ISO 8601 date format: <https://www.iso.org/iso-8601-date-and-time-format.html>
- `AGENTS.md` convention: <https://agents.md>
- `project-standardization` skill: full operating notes (triage, bootstrap checklist, references, anti-patterns).
