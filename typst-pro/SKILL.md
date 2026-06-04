---
name: typst-pro
description: Use when working with Typst files (*.typ) or when the user mentions Typst markup, document creation, or formatting. Covers the personal `@local/typst-tools` library (academic frontpage, IEEE journal, IEEE test report, meetrapport, testplan), typed MoSCoW + BOM + section-DB + figure helpers, chapter-style TOC, color/theme tokens, Dutch academic project layout, acronym/version handling, and idiomatic Typst syntax.
---

# typst-pro skill

Generate, edit, and reason about Typst documents — with a strong bias toward the user's standardized workflow built on the local **`@local/typst-tools`** package.

This `SKILL.md` holds the always-needed rules (when to use, punctuation, version pinning, template selection, layout summary, workflows). Detailed material lives in `references/` — **load the relevant file on demand**:

| Load `references/...` | When you need |
|---|---|
| `library-api.md` | umbrella exports, granular imports, repo layout, theme/colors/TOC, preview-package list |
| `templates.md` | minimal `.with(...)` examples for all 5 templates |
| `ieee-journals.md` | **how to write a proper IEEE journal** (emphasis, units, full-width floats, colbreak, footer, captions) |
| `data-driven.md` | acronyms, version history, MoSCoW, BOM, section-DB, image-grid, eur |
| `project-layout.md` | full project tree, config/type construction, legacy Dutch layout + rename cheat-sheet |
| `migration.md` | `academic-tools:0.1.29` → `typst-tools` migration steps |
| `idioms-troubleshooting.md` | library-internal idioms, common mistakes, troubleshooting, quick syntax reference |

**Runnable examples:** the library ships full, compilable demo documents at `C:\Users\ruben\Projects\Tools\TypstTools\examples\` (academic, IEEE journal/test-report, meetrapport, testplan, moscow, version-history, database, toc). They are version-matched to the lib — read those for an end-to-end, known-good reference. The skill keeps trimmed snippets in `references/`; it does **not** maintain its own `examples/` (that would duplicate and drift from the lib's).

## Overview

- All non-trivial documents extend a template from `@local/typst-tools` (academic, IEEE journal, IEEE test report, meetrapport, testplan). ISO/IEC/IEEE 29119-3 was removed; use the `testplan` template + `academic-test-plan-config` preset instead.
- Project files follow a fixed flat **kebab-case English** layout (`config/`, `subdocs/`, `research/`, `bom/`, `test-plans/`, `refs/`, `assets/`). Legacy projects may still use the Dutch layout (`Config/`, `Subdocumenten/`, `Onderzoeken/`, `Referenties/`, `Assets/`); keep that convention in existing projects. Details in `project-layout.md`.
- Dutch remains the default **body language** (`#set text(lang: "Nl")`) for Dutch projects — the kebab/English rule applies to paths and filenames, **not** to prose, headings, or captions.
- Acronyms use `@preview/acrostiche` via an `acronyms_db` dict; version history uses `version-entry` + `version-history`; MoSCoW uses typed `moscow-item` / `moscow-category` fed into `moscow-renderer`; section content (PvE, contract, BOM) uses `slice-db` / `section-render` / `bom-*`. See `data-driven.md`.
- Section-DB rows use **lowercase `id:`** (matches `moscow-category.id`). Old uppercase `ID:` dict rows are unsupported.

When this skill loads, **prefer the templates and helpers over hand-rolled cover pages, TOCs, headings, footers, MoSCoW tables, BOM tables, or section renderers.** Only fall back to raw Typst when the user explicitly asks for a one-off document or `typst-tools` is unavailable.

## When to use

- Any `.typ` file in any of the user's project directories (school, hobby, embedded).
- User says: "schrijf een meetrapport / testplan / onderzoek / hoofddocument", "maak een Typst-document", "typst-tools" / "academic-tools", "IEEE journal", "NHL Stenden rapport", "PvE / PvA / MoSCoW", "BOM tabel".
- Editing an existing document that already imports `@local/typst-tools` or any of `academic-frontpage` / `IEEE-academic-journal` / `IEEE-academic-test-report` / `meetrapport` / `testplan`.

**Do NOT use for:** plain Markdown, LaTeX, or non-Typst formats.

## Body text punctuation (always applies)

The user does **not** use the em-dash (`—`) or the hyphen (`-`) as a sentence-level separator in prose. Replace them with `.`, `;`, or `,`:

| Relation | Use |
|---|---|
| Two independent clauses | `.` (new sentence) or `;` |
| Tight aside or parenthetical | `,` on both sides, or `(...)` |
| List separator inside a sentence | `,` |

The hyphen `-` is **only** allowed in:

- Compound words and adjectives (`buck-boost`, `power-path`, `4-laags`, `e-stop`, `5V-rail`).
- Identifiers, file paths, package names, command flags, part numbers.
- Numeric ranges where a typographic en-dash would be visually wrong.

Apply to all body prose (abstracts, introductions, section text, captions). Code comments, headings, and identifiers are exempt.

```typst
// BAD — em-dash separator
De robot zal autonoom plukken — niet knippen — en in een tray plaatsen.
// GOOD
De robot zal autonoom plukken, niet knippen, en in een tray plaatsen.

// BAD — hyphen as clause separator
ESP32 stuurt aan via BLE - dit voorkomt extra bekabeling.
// GOOD
ESP32 stuurt aan via BLE. Dit voorkomt extra bekabeling.   // or `;`

// FINE — hyphen in compound word
De buck-boost converter levert 3.3V aan de ESP32.
```

When editing existing prose, sweep for `—` and standalone `-` between spaces and rewrite. Do not touch hyphens inside words, identifiers, or numeric ranges. (Note: published IEEE papers *do* use en-dash in compounds and ranges — that's allowed; only clause-separator dashes are banned.)

## Version pinning — DO NOT OVERWRITE EXISTING IMPORTS (always applies)

`0.1.2` is a known-safe baseline used throughout this skill's examples, **not** "the version every project must use". The lib ships small incremental releases often, so projects regularly pin newer versions (`0.1.5`, `0.1.8`, `0.2.0`, ...).

1. **Never rewrite an existing `@local/typst-tools:<X.Y.Z>` import back to `0.1.2`.** If a file pins a version, keep it — that's what the user verified compiles.
2. **Only use `0.1.2` for brand-new files** with no existing pin. Prefer to grep the project for an existing import and reuse that version.
3. **Keep versions in sync within a project.** Bump all files together only when asked.
4. **Examples here are illustrative.** Every `0.1.2` is a placeholder for the project's actual pinned version.
5. **Latest-on-disk ≠ what to use.** Newest in `C:\Users\ruben\Projects\Tools\TypstTools\typst.toml` is the dev version; what's installed at `%APPDATA%\typst\packages\local\typst-tools\<X.Y.Z>\` is importable. Don't auto-bump.

Grep first if unsure:

```powershell
Select-String -Path .\**\*.typ -Pattern '@local/typst-tools:[0-9.]+' | Select-Object -First 5
```

The lib was renamed `academic-tools` → `typst-tools` (repo `EmbeddedDynamics/TypstTools`, source at `C:\Users\ruben\Projects\Tools\TypstTools\`). Projects still on `@local/academic-tools:0.1.29` need updating — see `migration.md`.

## Template selection

| User intent / artifact | Template | Layout | Body language |
|---|---|---|---|
| Full Dutch project document with cover + title page + TOC + acronyms + version history | `academic-frontpage` | single column | Dutch |
| Research paper / journal-style article | `IEEE-academic-journal` | two-column body by default (toggle `two-column: false`); cover, abstract, TOC stay full-width | Dutch or English |
| Test report (formal, signed off) | `IEEE-academic-test-report` | IEEE-style, single column | Dutch or English |
| Lab measurement report ("Meetrapport") | `meetrapport` | single column, simple cover | Dutch |
| Test plan (general QA-style) | `testplan` | single column, version-history table | Dutch |

Invoke with the show-set pattern: `#show: <template>.with(...)`. Minimal examples per template are in `templates.md`; IEEE-journal authoring detail is in `ieee-journals.md`.

## Project layout (summary)

Flat kebab-case English: entrypoint `main.typ` at root; `config/` (with `config-*` metadata and `db-*` data-only files); `subdocs/` (both `#include`-able and standalone-compilable); `research/` (standalone IEEE papers); `bom/`, `test-plans/`, `refs/` (one `.bib` per topic), `assets/logo/`. Body prose stays Dutch; only paths/filenames are kebab/English. Logos and images are passed as content (`image("/assets/logo/nhl-logo.jpg")`), never raw path strings. Full tree, config construction, and the legacy Dutch layout + rename cheat-sheet are in `project-layout.md`.

## Workflows

### Creating a new project from scratch

1. Create the directory tree (kebab-case English; see `project-layout.md`).
2. Scaffold `main.typ` with `academic-frontpage.with(...)` (see `templates.md`).
3. Scaffold `config/config-general.typ` with typed `students` (`author[]`), `project` (`metadata(...)`), `clients` (`person[]`), `acronyms_db`. Import `@local/typst-tools:*` directly — **no `#show:` rule here**.
4. Scaffold `config/imports.typ` for `main.typ`'s extra packages and config files.
5. Drop `nhl-logo.jpg` into `assets/logo/` (lowercase, kebab-case).
6. Verify in Typst WebUI (compilation happens there, not locally).

### Editing an existing document

1. Identify the template (grep for `#show: academic-frontpage`, `IEEE-academic-journal`, `IEEE-academic-test-report`, `meetrapport`, `testplan`).
2. Make changes in the matching section (cover args, body, or helper config).
3. Verify in the Typst WebUI.

### Adding a research paper

1. Create `research/research-<topic>.typ` (legacy: `Onderzoeken/<Topic>_onderzoek.typ`).
2. Re-import `@local/typst-tools` directly (research papers are standalone).
3. Use `IEEE-academic-journal.with(...)`. Read `ieee-journals.md` for emphasis/units/float conventions.
4. Reference shared assets via `../assets/...` (or `/assets/...`); bib via `../refs/<name>.bib`.

### Inspecting rendered output

The `Read` tool **can** read `.pdf` files and returns rendered pages — use it to spot layout bugs (broken columns, literal-text leaks, table stacking, hyphenation, pagebreak failures) from a compiled PDF the user shares.

### Post-edit formatting checks

1. Check `typstyle` availability (`command -v typstyle`). If absent, skip.
2. After each `.typ` edit, run `typstyle --check <file>`; inspect with `--diff`; apply with `-i` only when changes are limited to your edits or a fresh file.
3. **Stop and ask** when formatting would change untouched pre-existing code.

## Detailed instructions (priority order)

1. **Trust local resources first.** The `@local/typst-tools` library and this skill take precedence over generic Typst memory.
2. **Identify document type early** — pick the template before writing cover-page code.
3. **Read existing project files** (`config/config-general.typ`, `config/imports.typ`, `config/db-*.typ`; legacy equivalents) before authoring; reuse `students`, `acronyms_db`, `COL`, palettes, data arrays. Detect convention from entrypoint name + folder casing — don't assume kebab/English on a legacy project.
4. **Reuse lib helpers for data-driven content.** Don't reimplement `slice-db`, `section-render`, `moscow-*`, `bom-*`, `eur`.
5. **Generate or modify** the `.typ` source.
6. **Run post-edit formatting checks.**
7. **Verify in the Typst WebUI** that it compiles.
8. **Read the output PDF** (if available) to verify layout.
9. **Provide the final `.typ` content** and, when useful, the rendered PDF path.
