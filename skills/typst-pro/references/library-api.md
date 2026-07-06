# typst-tools library API

The lib imported as `#import "@local/typst-tools:<version>": *`. Examples use `0.1.8` as a known-safe baseline, but the lib is released frequently. Reuse the version already pinned in the project (see **Version pinning** in `SKILL.md`). The umbrella `lib.typ` re-exports everything; granular imports from `src/...` are also supported.

## Repo layout (post-restructure)

```
typst-tools/
  typst.toml                  pkg = "typst-tools" v0.1.8, entrypoint = lib.typ
  lib.typ                     umbrella re-exports
  README.md
  assets/                     langs.yaml, logos/nhl_logo.jpg
  src/
    types/                    elembic data types (mod.typ aggregates them)
    components/               cover-pages, front-matter, version-history,
                              role-calculations, bom,
                              ieee-cover-pages, ieee-footer,
                              ieee-front-matter
    renderers/                moscow-renderer (typed MoSCoW tables)
    standards/
      ieee/                   ieee.typ (heading show-rule), ieee-journal,
                              ieee-test-report
    styles/                   base, colors, theme, toc
    templates/                academic, meetrapport, testplan
    utils/                    db (slice-db, section-render,
                              section-range-render, pve-item),
                              format (eur), figure (image-grid)
  examples/                   runnable demos (academic, meetrapport,
                              testplan, IEEE journal/test-report,
                              moscow, version-history,
                              role-calculations, database, toc-adavanced,
                              types)
```

**Restructure summary** (vs. the old `academic-tools` v0.1.29 layout):

- `src/elements/` → folded into `src/components/` (`version-history.typ`, `role-calculations.typ`).
- `src/styling/` → `src/styles/`. New siblings `colors.typ`, `theme.typ`, `toc.typ`.
- IEEE files moved out of `src/components/` into `src/standards/ieee/` (`ieee.typ`, `ieee-journal.typ`, `ieee-test-report.typ`). The IEEE cover/footer/front-matter components stayed under `src/components/`.
- New `src/renderers/moscow-renderer.typ` (typed MoSCoW). The old `src/components/moscow.typ` was deleted; **all MoSCoW helpers now come from the renderer**.
- Assets moved out of `src/assets/` to top-level `assets/`. Library logo path: `src/assets/NHL_logo.jpg` → `assets/logos/nhl_logo.jpg`. `langs.yaml` is now at `assets/langs.yaml`. User projects keep their own logo in `assets/logo/`.

## Granular imports

For finer control, import a specific module directly:

```typst
#import "@local/typst-tools:0.1.8/src/standards/ieee/ieee-journal.typ": IEEE-academic-journal
#import "@local/typst-tools:0.1.8/src/standards/ieee/ieee.typ": setup-ieee-headings
#import "@local/typst-tools:0.1.8/src/components/version-history.typ": version-history
#import "@local/typst-tools:0.1.8/src/components/role-calculations.typ": (
  role-calculations, add-role, add-roles, add-assignment, add-assignments,
)
#import "@local/typst-tools:0.1.8/src/types/requirement.typ": requirement
#import "@local/typst-tools:0.1.8/src/types/moscow-item.typ": moscow-item
#import "@local/typst-tools:0.1.8/src/types/moscow-category.typ": moscow-category
#import "@local/typst-tools:0.1.8/src/renderers/moscow-renderer.typ": *
#import "@local/typst-tools:0.1.8/src/styles/toc.typ": chapter-toc-style, chapter-toc-config
#import "@local/typst-tools:0.1.8/src/styles/theme.typ": default-theme
#import "@local/typst-tools:0.1.8/src/styles/colors.typ": *
```

## What the umbrella `lib.typ` re-exports

| Group | Names |
|---|---|
| Templates | `academic-frontpage`, `meetrapport`, `testplan`, `IEEE-academic-journal`, `IEEE-academic-test-report` |
| Elembic types | every type in `src/types/mod.typ`: identity (`author`, `person`, `affiliation`, `metadata`, `document-id`); control/review (`version-entry`, `approval-entry`); requirements (`demand`, `stakeholder`, `use-case`, `requirement`, `requirement-set`, `moscow-item`, `moscow-category`, `acceptance-criterion`); verification/testing (`verification-method`, `test-plan`, `test-case`, `test-step`); risk (`risk`); academic support (`glossary-entry`, `nomenclature-entry`, `appendix-entry`, `figure-info`, `table-info`); economics (`role`, `assignment`) |
| Rendering elements | `version-history`, `role-calculations` |
| Element state helpers | `add-role`, `add-roles`, `add-assignment`, `add-assignments` |
| Base styling | `setup-document`, `setup-headings`, `setup-figures`, `setup-paragraphs`, `setup-bibliography`, `setup-outline`, `chapter-numbering` |
| IEEE styling | `setup-ieee-headings`, `ieee-heading` *(opt-in; call `setup-ieee-headings()` to activate)* |
| IEEE journal helpers | `fullwidth` *(float content across both columns; see `ieee-journals.md`)* |
| Theme + colors | `default-theme`, `color-neutral-border`, `color-neutral-fill`, `color-success-soft`, `color-warning-soft`, `color-attention-soft`, `color-danger-soft`, `color-unknown-soft` |
| Chapter-style TOC | `chapter-toc-style`, `chapter-toc-config` |
| Cover-pages helpers | `page-footer`, `date-section`, `academic-front-cover`, `academic-title-page`, `measurement-cover`, `testplan-cover` |
| Front-matter helpers | `make-abstract`, `make-acknowledgments`, `make-toc`, `make-list-of-figures`, `make-list-of-tables`, `make-acronyms`, `make-version-history`, `make-executive-summary`, `make-preface` |
| Meetrapport helpers | `measurement-table`, `result-section`, `uncertainty-analysis` |
| Testplan helpers | `testplan`, `test-case-table`, `test-scope-table`, `risk-assessment-table`, `test-schedule-table`, `test-environment`, `criteria-section` |
| Section-DB helpers | `slice-db`, `section-render`, `section-range-render`, `pve-item` *(rows keyed on lowercase `id:`; `pve-item` = render callback for typed `moscow-item` data)* |
| MoSCoW renderer | `make-priority-cells`, `normalize-priority`, `priority-cell`, `priority-label`, `priority-description`, `moscow-simple-config`, `moscow-config`, `moscow-column-labels`, `moscow-column-widths`, `moscow-column-alignments`, `moscow-simple-table`, `moscow-table`, `moscow-range`, `moscow-overview`, `moscow-detail-table`, `moscow-grouped`, `moscow-legend`, `flatten-moscow-items`, `moscow-slice-categories` |
| BOM helpers | `bom-total`, `bom-cells`, `bom-table`, `bom-range`, `bom-render`, `bom-range-render` |
| Figure helpers | `image-grid(images, caption: none, width: 100%, gutter: 1em, columns: none)`, side-by-side images in a grid. Images are content (`image("path")`), not raw paths. |
| Format utility | `eur(n, decimal: ",", thousand: "", none-text: "-")` |

## IEEE styling is opt-in

`setup-ieee-headings` is exported by the umbrella import, but the show-rule **only activates when you call it** (the module has no top-level side effects, so importing it never affects layout on its own). Activate inside your document body:

```typst
#import "@local/typst-tools:0.1.8": *
#setup-ieee-headings()
```

`setup-ieee-headings()` wraps `set heading(numbering: none)` + `show heading: ieee-heading`. The standalone module lives at `src/standards/ieee/ieee.typ` if you want a granular import.

## Preview packages (per-file imports)

The new lib does **not** auto-re-export preview packages. Each module imports only what it needs. In your own document, import these explicitly when you use them:

| Package | Used for |
|---|---|
| `@preview/acrostiche:0.7.0` | acronyms (`#acr("PvE")`) |
| `@preview/transl:0.1.1` | translations |
| `@preview/elembic:1.1.1` | type/element declarations (only needed if you declare your own) |
| `@preview/oxifmt:0.2.1` | string/number formatting |
| `@preview/tablex:0.0.9` | merged-cell tables |
| `@preview/tablem:0.1.2` | markdown-style tables |
| `@preview/lilaq:0.5.0` | plotting (`as lq`) |
| `@preview/sigfig:0.1.2` | sig-fig rounding |
| `@preview/zero:0.5.0` | numerical formatting (`zi`, `ztable`, `num`) |
| `@preview/circuiteria:0.2.0` | digital circuits |
| `@preview/neural-netz:0.3.0` | neural-net diagrams (`draw-network`) |
| `@preview/rivet:0.3.0` | bit-field schemas |
| `@preview/unify:0.7.1` | SI units (`qty`, `num`, `numrange`, `qtyrange`) |
| `@preview/numbly:0.1.2` | number formatting |
| `@preview/gantty:0.5.1` | gantt charts |
| `@preview/fletcher:0.5.8` | block diagrams |
| `@preview/muchpdf:0.1.2` | embed external PDFs |
| `@preview/cetz:0.4.2` + `@preview/cetz-plot:0.1.3` | charts |
| `@preview/meander:0.4.0` | reflowable layouts |

## Theme, colors, and TOC styling

The lib ships a small theme dict and a palette of neutral / status colors. Both are re-exported by the umbrella.

### Color tokens (`src/styles/colors.typ`)

```typst
color-neutral-border    // rgb(90, 90, 90)
color-neutral-fill      // rgb(245, 245, 245)
color-success-soft      // rgb(210, 245, 210), Must have
color-warning-soft      // rgb(255, 248, 205), Should have
color-attention-soft    // rgb(255, 226, 190), Could have
color-danger-soft       // rgb(255, 210, 210), Won't have
color-unknown-soft      // rgb(230, 230, 230)
```

### `default-theme` (`src/styles/theme.typ`)

```typst
default-theme = (
  table:  (stroke: 0.45pt + color-neutral-border, inset: 5pt,
           header-fill: color-neutral-fill),
  moscow: (must:    color-success-soft,
           should:  color-warning-soft,
           could:   color-attention-soft,
           wont:    color-danger-soft,
           unknown: color-unknown-soft),
)
```

The MoSCoW renderer reads `theme.moscow.*` for fills and `theme.table.*` for stroke / inset. Pass a custom theme via `theme:` to `make-priority-cells`, `moscow-simple-config`, `moscow-config`, `moscow-overview`, `moscow-detail-table`, `moscow-legend`. Or override individual fills via the explicit `must / should / could / wont` parameters of `make-priority-cells`, which is the IDP pattern.

### Chapter-style TOC (`src/styles/toc.typ`)

Replaces Typst's flat outline with a chapter-block / dotted-leader layout. Apply as a show rule:

```typst
#import "@local/typst-tools:0.1.8": chapter-toc-style, chapter-toc-config

#set heading(numbering: "1.1.1.1")

#show: chapter-toc-style.with(
  config: chapter-toc-config(
    title: [Inhoudsopgave],
    prefixes:    ("1": "Hoofdstuk", "2": "Artikel", "3": "Paragraaf", "4": ""),
    show-prefixes: ("1": true,      "2": true,      "3": true,        "4": false),
    max-styled-level: 4,
  ),
)

#outline(title: none, depth: 4)
```

`chapter-toc-config()` takes a long list of keyword args for sizes, indent, leader stroke, gutters, before/after spacing per level. See `examples/toc-adavanced.typ` for a runnable demo.
