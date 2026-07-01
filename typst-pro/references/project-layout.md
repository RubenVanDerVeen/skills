# Standard project layout

All multi-document projects follow a **flat kebab-case English** layout. The Typst project root contains the entrypoint and the convention folders directly; do **not** wrap them in a `Documenten/` subdirectory.

**Naming rule (authoritative as of 2026-05-11):**

- **Folder names**: lowercase kebab-case English (`assets/`, `bom/`, `config/`, `refs/`, `research/`, `subdocs/`, `test-plans/`).
- **File names**: lowercase kebab-case English (`main.typ`, `config-general.typ`, `db-pve-moscow.typ`, `cooperation-contract.typ`, `research-actuators.typ`, `ax12-testplan.typ`).
- **Body prose stays Dutch** (`#set text(lang: "nl")`) when the project is Dutch. The kebab/English rule applies to paths and filenames, **not** to headings or sentences inside the document.
- **`db-` prefix** marks data-only files (`db-pve-moscow.typ`, `db-bom.typ`, `db-cooperation-contract.typ`). **`config-` prefix** marks structural / metadata files (`config-general.typ`, `config-stakeholders.typ`).

**Current layout:**

```
<typst-project-root>/
├─ main.typ                              ← entrypoint, uses academic-frontpage
├─ config/
│  ├─ imports.typ                        ← shared imports for main.typ
│  ├─ config-general.typ                 ← team (author[]), project (metadata),
│  │                                       clients (person[]), colors, acronyms_db
│  ├─ config-stakeholders.typ            ← stakeholder data + project-specific render fns
│  ├─ db-pve-moscow.typ                  ← requirements DATA only (typed moscow-category[])
│  ├─ db-cooperation-contract.typ        ← contract DATA only (section-DB)
│  └─ db-bom.typ                         ← BOM DATA + project palette binding
├─ subdocs/                              ← #include-d into main.typ AND standalone-compilable
│  ├─ pve.typ                            ← Programme of Requirements (standalone or included)
│  ├─ design-proposal.typ                ← design proposal pitch
│  ├─ cooperation-contract.typ           ← collaboration contract
│  └─ stakeholder-analysis.typ           ← stakeholder analysis
├─ research/                             ← standalone IEEE-style papers
│  ├─ research-actuators.typ
│  ├─ research-remote-controller.typ
│  └─ research-<topic>.typ
├─ bom/                                  ← standalone BOM documents
│  ├─ main-bom.typ                       ← full BOM
│  └─ <subsystem>-bom.typ                ← per-subsystem BOM (e.g. controller-bom.typ)
├─ test-plans/
│  └─ <component>-testplan.typ           ← e.g. ax12-testplan.typ
├─ refs/                                 ← one .bib per topic/scope
│  ├─ <topic>-research.bib
│  └─ <doc>.bib
├─ assets/
│  ├─ logo/                              ← project + institution logos
│  │  └─ nhl-logo.jpg                    (lowercase, kebab-case)
│  └─ <doc-name>/                        ← per-document images (e.g. design-proposal/)
│     ├─ <image>.png
│     └─ patents/                        ← optional grouping subfolder
└─ README.md
```

**Conventions:**

- Entrypoint is **`main.typ`** at the project root (not `Hoofddocument.typ`).
- `config/config-general.typ` imports `@local/typst-tools:*` and defines: `students` (`author[]` with `name`, `affiliation`, `email`, `role`), `clients` (`person[]`; was `opdrachtgevers`), `project` (`metadata(...)` with `title`, `institution`, `supervisor`, `tutor`, `room`, `client`, `group`, `degree`, `program`, `city`, `country`, `year`, `start-date`, `end-date`), `acronyms_db`, optional `COL` color palette. **Do NOT put a `#show:` rule in config files**; each document declares its own template.
- `config/imports.typ` centralizes extra packages and config imports for `main.typ`. `config-general.typ` imports `@local/typst-tools` directly.
- **Subdocs are both `#include`-able and standalone-compilable**: pattern: each `subdocs/*.typ` re-imports `@local/typst-tools` + its own `config/` data so it can compile in the Web UI on its own, while `main.typ` pulls them in via `#include`.
- Asset paths: `image("/assets/logo/nhl-logo.jpg")` (project-root absolute, lowercase). For per-document images: `assets/<doc-name>/<image>.png`, referenced from the subdoc with `../assets/<doc-name>/<image>.png` or root-absolute `/assets/<doc-name>/<image>.png`.
- Bibliography paths from `subdocs/` / `research/`: `../refs/<name>.bib`. From `main.typ`: `refs/<name>.bib`.

## Type construction examples (`config/config-general.typ`)

```typst
// Students, author type (document authors/contributors)
#let students = (
  author(name: "Ruben van der Veen", affiliation: "ELT",
         email: "ruben@student.nhlstenden.com", role: "Project Leider"),
  author(name: "Tim Boschma", affiliation: "ICT",
         email: "tim@student.nhlstenden.com", role: "Lead ICT"),
)

// Project metadata
#let project = metadata(
  title: "IDP Robotica 2025-2026",
  subtitle: "Autonoom aardbeien plukken met robots",
  group: "Groep 4",  client: "DigiAgro",
  institution: "NHL Stenden Hogeschool",
  department: "Elektrotechniek / HBO-ICT / Werktuigbouwkunde",
  degree: "Jaar 2",  program: "BD.ELT / BD.WTB / BD.ICT",
  supervisor: "Jelle Huitema",  tutor: "Sarah Mross",
  city: "Leeuwarden",  country: "Nederland",
  room: "F2.159",  year: "2026",
  start-date: "20-04-2026",  end-date: "18-06-2026",
)

// Clients, person type (contacts, not document authors)
// (renamed from `opdrachtgevers` under the kebab/English convention)
#let clients = (
  person(name: "Jelle Huitema", department: "E"),
  person(name: "Rieno Moedt",   department: "E"),
)
```

**BAD (legacy flat-variable style, do NOT write):**

```typst
#let title    = "IDP Robotica 2025-2026"
#let authors  = "Ruben van der Veen, Tim Boschma"
#let city     = "Leeuwarden"
#let country  = "Nederland"
#let year     = "2026"
#let university = "NHL Stenden Hogeschool"
#let department = "Elektrotechniek"
// ... etc, one #let per field
```

The flat style does not match any template signature; the cover will render with empty placeholders or fall back to the template defaults (`Bachelor of Science`, `Department Name`, etc.). It is also the legacy pattern from `Config/GeneralConfig.typ` and should not be reintroduced in new projects. **Map typed values into the template call instead** (`degree: project.degree`, `university: project.institution`, `authors: students.map(s => s.name).join(", ")`).

- `config/db-*.typ` files hold **data only** using typed constructors (`moscow-category`, `moscow-item`, `person`, `author`, `metadata`). Slice/render/table helpers come from the lib.
- Subdocuments are pulled in with `#include "/subdocs/<name>.typ"` (assigning to a `#let` lets you place them later in the document body).
- Logos and images are passed as content: `logo: image("/assets/logo/nhl-logo.jpg")`. **Never** raw path strings.
- `refs/` holds one or more `.bib` files, named per topic/scope (`<topic>-research.bib`, `<doc>.bib`). Split by topic when a single `.bib` would be unwieldy; merge into one when the project is small.
- Standalone research papers in `research/` re-import `@local/typst-tools` themselves and use `IEEE-academic-journal`; they reference assets with `../assets/...` (or root-absolute `/assets/...`) and bib files with `../refs/<name>.bib`.

## Legacy Dutch flat layout (pre-2026-05-11)

Older projects used Dutch folder/file names: `Hoofddocument.typ`, `Subdocumenten/`, `Onderzoeken/`, `Referenties/`, `Assets/Logo/NHL_logo.jpg`, `Config/_Imports.typ`, `Config/GeneralConfig.typ`, `Config/PvE_MoSCoW.typ`, `Config/BOM_DB.typ`, `Config/Samenwerkingscontract_DB.typ`, `Config/StakeholderConfig.typ`, plus optional `Leerdoelen/`, `Notities/`, `Peerreview/`, `Reflecties/`, `Archive/`. **Do not migrate an old project to the new layout mid-stream** unless the user explicitly asks: paths are referenced from many files, the Web UI project sync expects the existing names, and a partial rename will break compilation. When adding new files to an old project, follow the existing convention in that project. New projects start with the kebab/English layout above.

**Migration cheat-sheet (only when explicitly requested):**

| Old (Dutch) | New (kebab/English) |
|---|---|
| `Hoofddocument.typ` | `main.typ` |
| `Subdocumenten/` | `subdocs/` |
| `Onderzoeken/` | `research/` (files prefixed `research-`) |
| `Referenties/` | `refs/` |
| `Assets/Logo/NHL_logo.jpg` | `assets/logo/nhl-logo.jpg` |
| `Config/_Imports.typ` | `config/imports.typ` |
| `Config/GeneralConfig.typ` | `config/config-general.typ` |
| `Config/PvE_MoSCoW.typ` | `config/db-pve-moscow.typ` |
| `Config/BOM_DB.typ` | `config/db-bom.typ` |
| `Config/Samenwerkingscontract_DB.typ` | `config/db-cooperation-contract.typ` |
| `Config/StakeholderConfig.typ` | `config/config-stakeholders.typ` |
| `Samenwerkingscontract.typ` | `subdocs/cooperation-contract.typ` |
| `Stakeholder_analyse.typ` | `subdocs/stakeholder-analysis.typ` |
| `Plan_Van_Aanpak.typ` | `subdocs/design-proposal.typ` (or `subdocs/plan-of-approach.typ`) |
| `<Topic>_onderzoek.typ` | `research/research-<topic>.typ` |
| `opdrachtgevers` (variable) | `clients` |
