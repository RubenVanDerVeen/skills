# Writing proper IEEE journals

`IEEE-academic-journal` gives you the scaffold (cover, full-width front-matter, two-column body, footer, bib). Writing a paper that actually *reads* like a real IEEE journal is mostly about typographic discipline in the body. Match the conventions of published IEEE papers, summarized below.

## Document skeleton (order matters)

```typst
#import "@local/typst-tools:0.1.8": *
#import "@preview/unify:0.7.1": num, qty, numrange, qtyrange

#set text(lang: "nl", costs: (hyphenation: 500%))   // or "en"
#set par(justify: true)
#show link: underline
#set math.equation(numbering: "(1)")

#show: IEEE-academic-journal.with(
  title: [...], authors: "...", department: [...], university: [...],
  supervisor: [...], date: datetime.today(), location: [...],
  use-front-cover: true, use-toc: false,
  logo: image("../assets/logo/nhl-logo.jpg", width: 140pt),
  abstract: [One dense paragraph. State problem, approach, result.],
  two-column: true,
  footer-config: auto,                 // or a full dict (see below)
  references: bibliography("../refs/<topic>-research.bib"),
  reference-style: "ieee",
)

= Introductie
= Methode
= Resultaten
= Discussie
= Conclusie
```

The cover, abstract, and TOC render **full-width**; the two-column rule activates on the first body page. Don't fight it.

## Page size

`paper-size: "a4"` is the default. Pass `paper-size: "us-letter"` for US Letter (margins are derived as % of the Letter trim). Body font is fixed at `10pt STIX Two Text`; don't override per-document.

## Emphasis: italic for keywords, bold only for labels

Published IEEE papers **almost never bold mid-sentence**. They use:

- **Headings** → bold (template-generated, numbered `I`, `II`, …).
- ***Italic*** for first-use terms / emphasis mid-sentence: `_grid-forming_`, `_buck-boost_`, `_1S Li-ion_`, `_RISC-V_`.
- **Bold run-in labels** that start a paragraph or list item and name it, then a colon: `*Catalog.*`, `*Planner.*`, `*Keuze: IP2312*`, `*Protected cell*: …`.

| Case | Markup |
|---|---|
| Decision verdict line (`Keuze: …`) | `*Keuze: ESP32-S3*` (bold) |
| Option list where every bullet names an item | `*Protected cell*:` … `*Discrete BMS*:` (bold) |
| Mid-sentence keyword / feature lead-in | `_BLE 5.0_`, `_native USB-OTG_` (italic) |
| Component part numbers in prose | `_DW01A_`, `_FS8205A_` (italic) |

**Anti-pattern:** bolding every keyword (`*BLE 5.0*`, `*1S Li-ion*`, `*DW01A*` scattered through sentences). That's the #1 tell of a non-IEEE-looking paper. Sweep `*...*` → `_..._` for anything that isn't a heading, a `Keuze:`-style verdict, or a colon-terminated run-in label.

## Numbers and units → `unify`

Use `qty` / `qtyrange` for every physical quantity so spacing and unit typesetting are consistent. **Pass numbers as strings** to preserve exact formatting (trailing zeros, decimals):

```typst
#qty("200", "mA")            // 200 mA  (thin space)
#qty("3.3", "V")             // 3.3 V   (string keeps the .3)
#qty("2.4", "GHz")
#qtyrange("80", "130", "mA") // 80–130 mA (en-dash range)
#qtyrange("3.0", "4.2", "V") // 3.0–4.2 V (passing 3.0 as float would print "3")
```

Apply to mA, A, V, Hz/MHz/GHz, ms/s, m, nF, etc. Units whose `unify` spelling is uncertain (`%`, `″`, `kΩ`/`kohm`) are safer left as literal text until verified in the Web UI — a bad unit name is a hard compile error and there is no local compiler.

## Full-width figures and tables across both columns

A wide diagram or comparison table should span **both columns** while the running text flows around it — the standard IEEE "Fig. 1 at top of page" look. Use the lib's `fullwidth` helper (exported from `ieee-journal.typ`), which floats the content with `place(scope: "parent", float: true)`:

```typst
#fullwidth(
  figure(image("../assets/<doc>/network.png"), caption: [System overview.]),
)

// Bottom of the page instead of the top:
#fullwidth(placement: bottom)[
  #figure(table(..), caption: [Big comparison.])
]
```

- Signature: `fullwidth(body, placement: top)` — `placement` is `top` (default), `bottom`, or `auto`.
- Wrap a `figure(...)` as the body so the document's `Fig.`/`TABLE` numbering and caption rules apply.
- **Do NOT** use the old pagebreak-into-single-column trick for this — that wastes a page. `fullwidth` keeps the two-column flow intact.
- **Caveat:** a float that is taller than the page region won't place. For a near-full-page artifact (e.g. a 60-line repo tree or a huge table), don't float it — give it its own single-column page instead (`set page(columns: 1)` block, or a dedicated page), because a too-tall float gets pushed to the end or dropped.

## Column break (not page break)

To push the rest of the text to the next column (right column, or first column of the next page) **without** a page break, use the built-in `#colbreak()`. Handy to balance the final two columns before the references or a summary table. `#colbreak(weak: true)` collapses if already at a column top. Don't reach for `#pagebreak()` to nudge column flow — it leaves half-empty pages.

## Footer

`footer-config: auto` derives the footer from `title` + a `v1` default. For a custom footer pass a full dict (synthesized inside the fn body, so it's safe from the lazy-capture bug):

```typst
footer-config: (
  short-title: [Onderzoek Remote Controller],
  version: "1.0",
  confidentiality: [Internal Use Only],
  author: [],
  affiliation: [NHL Stenden],
  font-size: 8.5pt,
),
```

## Index Terms / keywords

Real IEEE papers print an *Index Terms* block (italic) right after the abstract. The current `IEEE-academic-journal` template has **no `keywords` / `index-terms` parameter** — if the user wants one, either add it manually at the top of the body (italic line under the abstract) or extend the template in the lib. Note this gap rather than silently omitting it when a user asks for a "proper" IEEE paper.

## Captions and tables

- **Every table and image goes in a `figure(...)` with a `caption`, no exceptions.** This is the IEEE default: a bare `#table(...)` or `#image(...)` gets no `TABLE N` / `Fig. N` number, no caption styling, and can't be cross-referenced. Wrap it, give it a label (`<tbl-...>` / `<fig-...>`), and reference it from the prose (`@tbl-...`). For wide ones, nest the `figure` inside `fullwidth` (see §"Full-width figures and tables"). The only things left bare are template arguments like the cover `logo:` image — those aren't body content.
- Table captions sit **on top** (`TABLE N`, smallcaps), figure captions **below** (`Fig. N`) — the template's `show figure` rules handle this automatically. Just provide `caption: [...]`.
- A plain `#table(columns: auto, ..)` collapses to one column. Give an explicit column array matching the header cell count.
- Don't manually `\`-break text inside table cells to control wrapping — it splits words oddly. Use `#text(hyphenate: false)[...]` on the cell if you want word-boundary wrapping only.

## Punctuation

Body prose follows the **Body text punctuation** rule in `SKILL.md`: no em-dash / sentence-level hyphen. Note that published IEEE papers *do* use en-dash in compounds (`MMC–WTG`, `speed–fidelity`) and numeric ranges — those are fine; only clause-separator dashes are banned in the user's house style.
