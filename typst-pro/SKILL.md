---
name: typst-pro
description: Use when working with Typst files (*.typ) or when the user mentions Typst markup, document creation, or formatting. Covers the personal `@local/typst-tools` library (academic frontpage, IEEE journal, IEEE test report, meetrapport, testplan), typed MoSCoW + BOM + section-DB + figure helpers, chapter-style TOC, color/theme tokens, Dutch academic project layout, acronym/version handling, and idiomatic Typst syntax.
---

# typst-pro skill

Generate, edit, and reason about Typst documents, with a strong bias toward the user's standardized workflow built on the local **`@local/typst-tools`** package.

This `SKILL.md` holds the always-needed rules (when to use, punctuation, version pinning, template selection, layout summary, workflows). Detailed material lives in `references/`, **load the relevant file on demand**:

| Load `references/...` | When you need |
|---|---|
| `library-api.md` | umbrella exports, granular imports, repo layout, theme/colors/TOC, preview-package list |
| `templates.md` | minimal `.with(...)` examples for all 5 templates |
| `ieee-journals.md` | **how to write a proper IEEE journal** (emphasis, units, full-width floats, colbreak, footer, captions) |
| `data-driven.md` | acronyms, version history, MoSCoW, BOM, section-DB, image-grid, eur |
| `project-layout.md` | full project tree, config/type construction, legacy Dutch layout + rename cheat-sheet |
| `migration.md` | `academic-tools:0.1.29` → `typst-tools` migration steps |
| `idioms-troubleshooting.md` | library-internal idioms, common mistakes, troubleshooting, quick syntax reference |

**Runnable examples:** the library ships full, compilable demo documents at `C:\Users\ruben\Projects\Tools\TypstTools\examples\` (academic, IEEE journal/test-report, meetrapport, testplan, moscow, version-history, database, toc). They are version-matched to the lib, read those for an end-to-end, known-good reference. The skill keeps trimmed snippets in `references/`; it does **not** maintain its own `examples/` (that would duplicate and drift from the lib's).

## Overview

- All non-trivial documents extend a template from `@local/typst-tools` (academic, IEEE journal, IEEE test report, meetrapport, testplan). ISO/IEC/IEEE 29119-3 was removed; use the `testplan` template + `academic-test-plan-config` preset instead.
- Project files follow a fixed flat **kebab-case English** layout (`config/`, `subdocs/`, `research/`, `bom/`, `test-plans/`, `refs/`, `assets/`). Legacy projects may still use the Dutch layout (`Config/`, `Subdocumenten/`, `Onderzoeken/`, `Referenties/`, `Assets/`); keep that convention in existing projects. Details in `project-layout.md`.
- Dutch remains the default **body language** (`#set text(lang: "nl")`) for Dutch projects. The kebab/English rule applies to paths and filenames, **not** to prose, headings, or captions.
- Acronyms use `@preview/acrostiche` via an `acronyms_db` dict; version history uses `version-entry` + `version-history`; MoSCoW uses typed `moscow-item` / `moscow-category` fed into `moscow-renderer`; section content (PvE, contract, BOM) uses `slice-db` / `section-render` / `bom-*`. See `data-driven.md`.
- Section-DB rows use **lowercase `id:`** (matches `moscow-category.id`). Old uppercase `ID:` dict rows are unsupported.

When this skill loads, **prefer the templates and helpers over hand-rolled cover pages, TOCs, headings, footers, MoSCoW tables, BOM tables, or section renderers.** Only fall back to raw Typst when the user explicitly asks for a one-off document or `typst-tools` is unavailable.

### Hard rules (apply every time)

These are the most common mistakes an agent makes when authoring Typst here. Violating any of them produces a broken or off-style document.

1. **Never fabricate template parameters.** Each template's signature is exact; unused kwargs are silently accepted (Typst 0.x behaviour). Always read the signature in `references/templates.md` or the lib source at `C:\Users\ruben\Projects\Tools\TypstTools\src\templates/<name>.typ` before calling `.with(...)`. `academic-frontpage` does **not** take `use-toc`, `use-front-cover`, `extend-abstract`, `footer-config`, `subject`, or `version`. Those are `IEEE-academic-journal` keys. `meetrapport` does not take `authors: students` (it wants `(name,) | string`); `testplan` does not take `supervisor` (it wants `instructor` only on `meetrapport` and `tutor`/`reviewers` on `testplan`).
2. **Use typed constructors in `config-general.typ`, not flat variables.** Build `project = metadata(...)` and `students = (author(...), author(...))`, never hand-rolled `#let title = ...` / `#let authors = "..."`. The lib reads `project.institution`, `project.degree`, `project.program`, `project.year`, `students.map(s => s.name)`; inventing flat names like `project.university` or `s.name` will compile but render the wrong values. Field map in `references/project-layout.md`.
3. **Don't repeat setup rules the template already applies.** The academic-style templates (`academic-frontpage`, `IEEE-academic-journal`, `IEEE-academic-test-report`, `meetrapport`, `testplan`) call `setup-headings()`, `setup-figures()`, `setup-paragraphs()`, `setup-outline()` themselves (or, in the IEEE case, inline `set par(justify: true)` and `set text(... costs: (hyphenation: 500%))` directly). Repeating `#set par(justify: true)`, `#set text(costs: (hyphenation: 500%))`, `#show link: underline`, or `#set math.equation(numbering: "(1)")` in an entrypoint that uses one of those templates is redundant. **This rule applies to every entrypoint that uses one of those templates**, including `research/*.typ` (IEEE-academic-journal) and `test-plans/*.typ` (testplan). The exception is **standalone subdocs that use no template** (`subdocs/*.typ`, `bom/*.typ`, `research/*.typ` that drop straight into content). Those DO need a small block of setup rules (see "Standalone subdoc boilerplate" below). Note: the IEEE-journal research example in `references/ieee-journals.md` previously showed those redundant rules; treat the SKILL rule, not the reference example, as authoritative.
4. **Use backticks for inline raw, not `#raw[...]`.** Both compile; backticks are shorter and are the modern Typst idiom. Reserve `#raw[...]` for code-block contexts where you explicitly need a raw block element.
5. **No `#show:` rule inside `config/`.** Each document declares its own template. Putting `#show: academic-frontpage.with(...)` in `config-general.typ` double-applies the front cover / TOC / acronyms.
6. **Don't assume `typst-tools` exports project-specific helpers** like `letop`, `checkpoint`, `docent`, or `screenshot`. If a project needs them, define them in `config/helpers.typ` (project-local). The lib exports generic callout-like elements only via the theme tokens in `library-api.md`; there's no `letop` builtin.
7. **Don't put a `#show:` rule in `config/imports.typ`** either, even when adding `setup-ieee-headings()`; the template is responsible for that call.
8. **Handle the `#include` heading-level collision.** A subdoc is standalone-compilable, so it starts with `= Title`. When main.typ `#include`s it, the chapter numbering gets confused if main also adds its own `= Inleiding` or `== Bijlage X` heading around the include. The rule in one line: **main.typ must have no `=` heading between `#make-version-history` (or any other front-matter terminator) and the first `#include`.** Each subdoc's own `=` is the level-1 chapter. If you want a "Bijlage A" label, compose it into the subdoc's first heading (`= Bijlage A: Programma van Eisen`) or restructure the subdoc so its main heading sits at the desired level. Same rule applies to `#include` inside a research paper between sections: do not add a `=` heading in main that wraps the include.
9. **`academic-frontpage` has no version-history parameter; use `make-version-history`.** The lib exports `make-version-history(...)` from the umbrella; call it manually right after the `#show: academic-frontpage.with(...)` rule. It renders a heading + table and `pagebreak()`s at the end, so placement matters: putting it after TOC/acronyms is correct (it lands between the front matter and the body). `IEEE-academic-test-report` and `testplan` accept `version-history` directly; don't use the manual call there.
10. **Import lib helpers only in the file that uses them.** `config/config-general.typ` should only import the constructors that are re-exported to other files (`metadata`, `author`, `version-entry`, `person`, `moscow-category`, `moscow-item`, ...). Specific renderers (`moscow-legend`, `moscow-range`, `bom-render`, `bom-range`, `make-priority-cells`, ...) belong in the subdoc that calls them. Do **not** import a helper in `config-general.typ` and then re-export via the umbrella `*`; the subdoc that needs it should import the lib directly. This keeps config lean and avoids surprises when the lib ships a new helper.
11. **`academic-frontpage`'s `keywords:` is consumed only when `abstract:` is not `none`.** If you pass `abstract: none` (or omit abstract), the `keywords:` kwarg is dead. Pass `keywords` only when you also pass an `abstract`, otherwise drop both. `keywords` is a **content block** (`keywords: [BLDC, balancer, IEC 60034-14]`), not an array.
12. **Preview packages need their own version pin.** Typst looks up `@preview/<name>:<X.Y.Z>` in `%LOCALAPPDATA%\typst\packages\preview\<name>\` (or `~/.local/share/typst/packages/preview/<name>/` on Linux). To find the installed version: `Get-ChildItem "$env:LOCALAPPDATA%\typst\packages\preview\<name>" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name`. If the directory does not exist, the package will fail at compile time; either run `typst install` or copy the package manually. Common pinned versions verified on this machine: `unify:0.7.1`, `transl:0.1.1`, `acrostiche:0.7.0`. Always verify by listing the local dir before pinning.
13. **Every entrypoint declares `#set text(lang: "nl")` itself.** None of the academic-style templates (including `testplan`, `IEEE-academic-journal`, `IEEE-academic-test-report`, `meetrapport`, `academic-frontpage`) calls `set text(lang: ...)` for the body. The lang yaml is loaded by `transl` for label translation, but the document language (which controls hyphenation, date formatting, and `transl` lookups) is set by the entrypoint. Without this line, the body defaults to English even if every keyword is Dutch. Place it BEFORE the `#show:` rule.

If you do any of the above, expect the compile to silently ignore most issues (Typst does not warn on unknown kwargs) and the final layout to be subtly wrong: wrong logo, wrong metadata field, no TOC, missing cover, double cover, etc.

## When to use

- Any `.typ` file in any of the user's project directories (school, hobby, embedded).
- User says: "schrijf een meetrapport / testplan / onderzoek / hoofddocument", "maak een Typst-document", "typst-tools" / "academic-tools", "IEEE journal", "NHL Stenden rapport", "PvE / PvA / MoSCoW", "BOM tabel".
- Editing an existing document that already imports `@local/typst-tools` or any of `academic-frontpage` / `IEEE-academic-journal` / `IEEE-academic-test-report` / `meetrapport` / `testplan`.

**Do NOT use for:** plain Markdown, LaTeX, or non-Typst formats.

## Body text punctuation (always applies)

The user does **not** use the em-dash or the hyphen as a sentence-level separator in prose. Replace them with `.`, `;`, or `,`:

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
// BAD: em-dash separator (the two em-dashes here are exactly what to avoid)
De robot zal autonoom plukken [em-dash] niet knippen [em-dash] en in een tray plaatsen.
// GOOD
De robot zal autonoom plukken, niet knippen, en in een tray plaatsen.

// BAD: hyphen as clause separator
ESP32 stuurt aan via BLE - dit voorkomt extra bekabeling.
// GOOD
ESP32 stuurt aan via BLE. Dit voorkomt extra bekabeling.   // or `;`

// FINE: hyphen in compound word
De buck-boost converter levert 3.3V aan de ESP32.
```

When editing existing prose, sweep for the em-dash character and standalone `-` between spaces and rewrite. Do not touch hyphens inside words, identifiers, or numeric ranges. (Note: published IEEE papers *do* use en-dash in compounds and ranges; that's allowed, only clause-separator dashes are banned.)

## Version pinning, DO NOT OVERWRITE EXISTING IMPORTS (always applies)

`0.1.8` is the current known-safe baseline used throughout this skill's examples, **not** "the version every project must use". The lib ships small incremental releases often, so projects may pin older (`0.1.2`, `0.1.5`) or newer (`0.1.9`, `0.2.0`, ...) versions.

1. **Never rewrite an existing `@local/typst-tools:<X.Y.Z>` import back to `0.1.8`.** If a file pins a version, keep it, that's what the user verified compiles.
2. **Only use `0.1.8` for brand-new files** with no existing pin. Prefer to grep the project for an existing import and reuse that version.
3. **Keep versions in sync within a project.** Bump all files together only when asked.
4. **Examples here are illustrative.** Every `0.1.8` is a placeholder for the project's actual pinned version.
5. **Latest-on-disk ≠ what to use.** Newest in `C:\Users\ruben\Projects\Tools\TypstTools\typst.toml` is the dev version; what is importable is whatever version is installed at `%LOCALAPPDATA%\typst\packages\local\typst-tools\<X.Y.Z>\` on Windows (or `~/.local/share/typst/packages/local/typst-tools/<X.Y.Z>/` on Linux). Don't auto-bump.
6. **If the local package is missing, the import fails at compile time.** Symlink or copy the lib to the local packages dir before authoring:

   ```powershell
   # Windows (one-time, after pulling lib changes):
   New-Item -ItemType Junction -Path "$env:LOCALAPPDATA\typst\packages\local\typst-tools\0.1.8" -Target "C:\Users\ruben\Projects\Tools\TypstTools" | Out-Null
   ```

   If that directory does not exist yet, create `local/typst-tools/` first, then junction the version subfolder. To find out which versions are actually installed:

   ```powershell
   Get-ChildItem "$env:LOCALAPPDATA\typst\packages\local\typst-tools" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
   ```

   Pin the import to one of those names. Do not pin a version that is not on disk.

Grep first if unsure:

```powershell
Select-String -Path .\**\*.typ -Pattern '@local/typst-tools:[0-9.]+' | Select-Object -First 5
```

The lib was renamed `academic-tools` to `typst-tools` (repo `EmbeddedDynamics/TypstTools`, source at `C:\Users\ruben\Projects\Tools\TypstTools\`). Projects still on `@local/academic-tools:0.1.29` need updating; see `migration.md`.

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
2. Scaffold `main.typ` with `academic-frontpage.with(...)` (see `templates.md`). Map config fields into template args, do not invent keys:

   ```typst
   #import "@local/typst-tools:<pinned>": *
   #import "config/config-general.typ": project, students, acronyms_db, COL

   #set text(lang: "nl")  // body language only, the template handles the rest

   #show: academic-frontpage.with(
     title: project.title,
     authors: students.map(s => s.name).join(", "),
     degree: project.degree,
     degree-goal: [The sentence that follows "submitted in fulfilment of..."],
     department: project.department,
     university: project.institution,
     supervisor: project.supervisor,
     tutor: project.tutor,
     program-type: project.program,
     degree-year: project.year,
     location: [#project.city, #project.country],
     logo: image("/assets/logo/nhl-logo.jpg", width: 140pt),
     date: datetime.today(),
     abstract: [Korte samenvatting van het project.],
     acronyms: (acronyms_db),
   )

   = Organisatie
   ...
   ```
3. Scaffold `config/config-general.typ` with typed `students` (`author[]`), `project` (`metadata(...)`), `clients` (`person[]`), `acronyms_db`, optional `COL`. Import `@local/typst-tools:*` directly; **no `#show:` rule here**. Use the field names the `metadata` type defines (see `references/project-layout.md`).
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

### Standalone subdoc boilerplate

Subdocs in `subdocs/`, `bom/`, and standalone `research/` pieces often render **without** a template. They drop straight into content (MoSCoW tables, BOM tables, slice-db sections, etc.). Those `*.typ` files do **not** get `setup-paragraphs`, `setup-figures`, or link styling applied automatically. Use this block at the top:

```typst
#import "@local/typst-tools:<pinned>": *
#import "config/config-general.typ": *

#set text(lang: "nl")
#set par(justify: true)
#set text(costs: (hyphenation: 500%))

= Ondertitel  // chapter heading (level 1)
```

The `setup-ieee-headings` show-rule is only useful for IEEE-journal subdocs (`research/*.typ`); see `library-api.md`.

### Recipe: version history with `academic-frontpage`

`academic-frontpage` has no `version-history` parameter, unlike `testplan` and `IEEE-academic-test-report`. Call the lib's `make-version-history` manually, after the `#show: academic-frontpage.with(...)` rule and after the body's first heading:

```typst
#import "@local/typst-tools:<pinned>": *

// ... define project, students, versions = (version-entry(...), ...)

#show: academic-frontpage.with(
  title: project.title,
  // ... rest of the cover args (NEVER pass version-history here)
)

#make-version-history(versions)  // renders, then `pagebreak()`s

= Hoofdstuk 1
...
```

For multiple revisions, build `versions` as a `(version-entry(...), version-entry(...), ...)` array (typed `version-entry` constructor). The end-of-table pagebreak lands you on the body's first heading.

### Inspecting rendered output

The `Read` tool **can** read `.pdf` files and returns rendered pages, use it to spot layout bugs (broken columns, literal-text leaks, table stacking, hyphenation, pagebreak failures) from a compiled PDF the user shares.

### Post-edit formatting checks

1. Check `typstyle` availability (`command -v typstyle`). If absent, skip.
2. After each `.typ` edit, run `typstyle --check <file>`; inspect with `--diff`; apply with `-i` only when changes are limited to your edits or a fresh file.
3. **Stop and ask** when formatting would change untouched pre-existing code.

## Detailed instructions (priority order)

1. **Trust local resources first.** The `@local/typst-tools` library and this skill take precedence over generic Typst memory.
2. **Identify document type early**, pick the template before writing cover-page code.
3. **Read existing project files** (`config/config-general.typ`, `config/imports.typ`, `config/db-*.typ`; legacy equivalents) before authoring; reuse `students`, `acronyms_db`, `COL`, palettes, data arrays. Detect convention from entrypoint name + folder casing, do not assume kebab/English on a legacy project.
4. **Reuse lib helpers for data-driven content.** Don't reimplement `slice-db`, `section-render`, `moscow-*`, `bom-*`, `eur`.
5. **Generate or modify** the `.typ` source.
6. **Run post-edit formatting checks.**
7. **Verify in the Typst WebUI** that it compiles.
8. **Read the output PDF** (if available) to verify layout.
9. **Provide the final `.typ` content** and, when useful, the rendered PDF path.

