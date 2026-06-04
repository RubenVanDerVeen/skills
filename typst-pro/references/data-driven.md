# Data-driven content (acronyms, version history, MoSCoW, BOM, section-DB, figures)

## Acronyms (`acrostiche`)

Define the database once in `config/config-general.typ` (legacy: `Config/GeneralConfig.typ`):

```typst
#let acronyms_db = (
  "PvE":   ("Pakket van Eisen"),
  "MoSCoW":("Must have, Should have, Could have, Won't have"),
  "PCB":   ("Printed Circuit Board"),
)
```

Pass it to the template (`acronyms: (acronyms_db)`) — the template calls `init-acronyms(...)` and renders the index. In the body, use `#acr("PvE")` for the first/expanded form and `#acrpl("PvE")` for plural variants. **Do not** call `init-acronyms` manually; the template owns it.

The acronyms list is **no longer** wrapped in a `figure(kind: table)` — it does not pollute the List of Tables anymore. Pass `caption: [...]` if you want a centred italic caption beneath the index; default is `none`.

## Version history

The `version-entry` type replaces the old `version` constructor. Field names are all lowercase:

- `contributors` (was `committee` — renamed)
- `department`
- `description`
- `date` (ISO-8601 string)
- `level` (1 = major, 2 = minor, 3 = patch)

```typst
version-history: (
  version-entry(
    contributors: "R. van der Veen",
    department: "ELT",
    description: [Initiële commit],
    date: "2026-04-26",
    level: 1,    // first level-1 entry → 1.0.0 (baseline is 0.0.0)
  ),
  version-entry(
    contributors: "T. Boschma",
    department: "ICT",
    description: [Vision benchmark suite toegevoegd],
    date: "2026-04-29",
    level: 2,    // → 1.1.0
  ),
)
```

The version baseline is `(0, 0, 0)`. So the first level-1 entry produces `1.0.0`, the first level-2 entry on its own produces `0.1.2`, the first level-3 entry on its own produces `0.0.1`. The version table is rendered automatically by `academic-frontpage`, `testplan`, and `IEEE-academic-test-report`. For other templates, render manually with `version-history(title: ..., level: ..., ..entries)`.

## Section-driven content (PvE, MoSCoW, BOM, contract)

Database files in `config/` should hold **data only**. The slicing, rendering, MoSCoW, and BOM helpers all live in the lib.

### MoSCoW data shape

Always use the typed `moscow-category` + `moscow-item` from `src/types/`:

```typst
#let pve = (
  moscow-category(
    id: "mandatory",                       // lowercase id, used for slicing
    label: <verplichte-eisen>,             // optional Typst label
    title: [Verplichte eisen],
    items: (
      moscow-item(
        id: "PVE-001",
        title: "Rijpe aardbeien herkennen en plukken",
        priority: "must",                  // "must" | "should" | "could" | "wont"
        description: [De robot zal autonoom rijpe aardbeien plukken.],
        owner: "Vision team",
        status: "accepted",
        rationale: [],   source: "",       // optional fields
      ),
    ),
  ),
)
```

### MoSCoW: simple two-column table (PvE-style)

Best fit for "Programma van Eisen" documents — one row per requirement, two columns (`Eis / Beschrijving`, `Prioriteit`):

```typst
#let pc = make-priority-cells()              // theme-driven defaults
#moscow-legend(cells: pc, show-indicator: true)

// Whole DB
#moscow-simple-table(pve, cells: pc)

// Sliced range (inclusive on both ends)
#moscow-range(pve, "mandatory", "wishes", cells: pc)

// Tweak via simple config
#moscow-simple-table(
  pve,
  cells: pc,
  config: moscow-simple-config(
    header: ([*Eis / Beschrijving*], [*Prioriteit*]),
    columns: (1fr, 22mm),
    justify-cells: false,
    hyphenate-cells: true,
    lang: "nl",
  ),
)
```

### MoSCoW: configurable multi-column tables

Pick columns by name. Built-in presets:

| Preset | Columns |
|---|---|
| `"overview"` | id, title, description, priority, status |
| `"owner"` (default) | id, title, description, priority, owner, status |
| `"detailed"` | id, title, priority, description, rationale, status |
| `"full"` | id, title, priority, description, rationale, source, owner, status |

```typst
// Preset
#moscow-overview(pve, cells: pc)             // overview preset
#moscow-detail-table(pve, cells: pc)         // detailed preset

// Custom column list
#moscow-table(
  pve,
  title: [MoSCoW Overview],
  cells: pc,
  config: moscow-config(
    columns: ("title", "description", "priority", "owner", "status"),
    widths:  (title: 42mm, description: 1fr, priority: 20mm, status: 24mm),
    justify-cells: false,
    hyphenate-cells: true,
    lang: "nl",
  ),
)

// Grouped by priority (Must → Should → Could → Won't, each its own subtable)
#moscow-grouped(pve, cells: pc)
```

`moscow-table` always operates on a flat item list; pass categories and they get auto-flattened via `flatten-moscow-items`.

### Generic section-render (PvE, samenwerkingscontract, anything keyed on `id`)

```typst
// Typed moscow-item data requires render-item: pve-item
// (pve-item reads .description instead of .text)
#section-range-render(
  pve, "mandatory", "functional",
  header-level: 3,
  render-item: pve-item,                    // REQUIRED for typed data
)

// Raw dict data with .text field — no render-item needed
#section-render(samenwerkingscontract_db, header-level: 2)

// Custom item rendering (overrides style:):
#section-range-render(
  db, "a", "b",
  header-level: 3,
  render-item: (it, sec) => block(spacing: 0.8em)[*#it.label*: #it.text],
)
```

### BOM

```typst
// Single combined table with subtotals + grand total.
#bom-range(
  bom, "remote.power", "arm.servos",
  colors: bom-colors,                        // see palette pattern below
  thousand: ".",                             // NL grouping → "€ 1.234,50"
)

// One table per section with a heading per section.
#bom-render(bom, header-level: 3, colors: bom-colors)
```

### Palette override pattern (IDP idiom)

The lib helpers no longer pull project palettes implicitly — each project binds its own dict and passes it in. Two recurring patterns:

```typst
// MoSCoW: bind once in db-*.typ or imports.typ, expose pc + p1..p4 aliases.
#let pc = make-priority-cells(
  must:   rgb(150, 255, 150),
  should: rgb(255, 255, 180),
  could:  rgb(255, 210, 150),
  wont:   rgb(255, 150, 150),
)
#let p1 = pc.p1
#let p2 = pc.p2
#let p3 = pc.p3
#let p4 = pc.p4

// BOM: bind once, pass as `colors:` to bom-range / bom-render.
#let bom-colors = (
  header:      COL.primary,
  section:     COL.light,
  total:       COL.primary,
  header-text: white,
)
```

### pve-item

Render callback for `section-render` / `section-range-render` when items are typed `moscow-item` values. Reads `.description` instead of the default `.text`:

```typst
pve-item = (it, sec) => enum.item(it.description)
```

Pass as `render-item: pve-item`. Required when rendering `moscow-category` data through the section-DB pipeline — without it, items render blank because `moscow-item` has no `.text` field.

### image-grid

Side-by-side images in a grid figure. Images are content — pass `image("path")` not raw strings:

```typst
// Two images side by side
#image-grid((image("../assets/<doc>/patent1.png"), image("../assets/<doc>/patent2.png")),
  caption: [Figuur uit patent US12269158B2.])

// Three images, two per row, narrower
#image-grid((image("a.png"), image("b.png"), image("c.png")),
  columns: 2, gutter: 0.5em, width: 80%)
```

Parameters: `images` (array of content), `caption` (none), `width` (100%), `gutter` (1em), `columns` (auto from `images.len()`).

### Format helper

```typst
#eur(12.5)                              → "€ 12,50"
#eur(none)                              → "-"
#eur(1234.5, thousand: ".")             → "€ 1.234,50"
#eur(12.5, decimal: ".")                → "€ 12.50"
#eur(none, none-text: "n.v.t.")         → "n.v.t."
```
