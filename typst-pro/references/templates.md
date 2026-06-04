# Template usage — minimal examples

All templates use the **show-set pattern** (`#show: <template>.with(...)`). For IEEE-journal-specific authoring guidance see `ieee-journals.md`.

> **Runnable demos:** full, compilable example documents ship with the library itself at `C:\Users\ruben\Projects\Tools\TypstTools\examples\` (`academic`, IEEE `journal` / `test-report`, `meetrapport`, `testplan`, `moscow`, `version-history`, `role-calculations`, `database`, `toc-adavanced`, `types`). They are version-matched to the lib — prefer reading those for a known-good, end-to-end reference over the trimmed snippets below.

## `academic-frontpage` — main project document (`main.typ`)

```typst
#import "@local/typst-tools:0.1.2": *
#import "config/imports.typ": *

#set text(lang: "Nl")
#set par(justify: true)
#set text(costs: (hyphenation: 500%))
#show link: underline
#set math.equation(numbering: "(1)")

#show: academic-frontpage.with(
  title: [Embedded Systems Project\ Robothond],
  authors: students.map(s => s.name).join(", "),
  degree: project.degree,
  degree-goal: [Het realiseren van een Robothond],
  department: project.department,
  university: project.institution,
  program-type: project.program,
  degree-year: project.year,
  location: [#project.city, #project.country],
  supervisor: project.supervisor,
  tutor: project.tutor,
  logo: image("/assets/logo/nhl-logo.jpg"),
  date: datetime.today(),
  abstract: [Korte samenvatting van het project.],
  keywords: [],
  acknowledgments: [],
  acronyms: (acronyms_db),
)

= Organisatie

== Team Structuur
...
```

## `IEEE-academic-journal` — research paper (two-column body)

```typst
#import "@local/typst-tools:0.1.2": *
#import "@preview/unify:0.7.1": num, qty, numrange, qtyrange

#set text(lang: "nl")
#set math.equation(numbering: "(1)")

#show: IEEE-academic-journal.with(
  title: [Onderzoek voor de AI gestuurde diepte herkenning],
  authors: "Ruben van der Veen",
  degree: [Bachelor of Electrical Engineering],
  degree-goal: [Een onderzoek naar spraakherkenning en omgevingsperceptie...],
  department: [Bachelors student],
  university: [NHL Stenden, Hogeschool],
  supervisor: [R. Moedt],
  date: datetime.today(),
  location: [Leeuwarden, Nederland],

  use-front-cover: true,
  use-toc: true,
  // IEEE templates expect logo as content (not path) — call `image()` here.
  logo: image("../assets/logo/nhl-logo.jpg", width: 140pt),

  extend-abstract: false,
  abstract: [Dit onderzoek...],

  // Default `true` matches IEEE convention. Set `false` for single-column.
  two-column: true,

  // Default `"a4"`. Pass `"us-letter"` for US Letter.
  paper-size: "a4",

  // Pass `auto` to derive footer from `title` + a v1 default; or pass a
  // full dict to override.
  footer-config: (
    short-title: [AI Diepte],
    version: "1.0",
    confidentiality: [Internal Use Only],
    affiliation: [NHL Stenden],
    font-size: 8.5pt,
  ),

  references: bibliography("../refs/ai.bib"),
  reference-style: "ieee",
)

= Introductie
...
```

## `IEEE-academic-test-report` — test report

```typst
#import "@local/typst-tools:0.1.2": *

#show: IEEE-academic-test-report.with(
  title: [Vision Pipeline Test Report],
  project-name: [DigiAgro IDP 2026],
  version: "1.0.0",

  authors: [R. van der Veen, T. Boschma],
  reviewers: [J. Huitema],
  approvers: [P. van Dijk],

  department: [Electrical Engineering / ICT],
  university: [NHL Stenden Hogeschool],

  date: datetime.today(),
  location: [Leeuwarden, Netherlands],

  use-front-cover: false,
  logo: image("/assets/logo/nhl-logo.jpg", width: 120pt),

  show-version-history: true,
  version-history: (
    version-entry(
      contributors: "R. van der Veen",
      department: "ELT",
      description: [Initial draft.],
      date: "2026-05-10",
      level: 1,
    ),
  ),

  abstract: [Results from the vision-pipeline benchmark.],

  // `auto` derives footer from `title` + `version`.
  footer-config: auto,
)
```

## `meetrapport` — lab measurement report

```typst
#import "@local/typst-tools:0.1.2": *

#show: meetrapport.with(
  title: [Meetrapport — Spanningsdeler],
  subtitle: [Experiment 3],
  course: [Analoge Elektronica 1],
  course-code: [AE-1],
  experiment-number: 3,
  date: datetime.today(),
  authors: ("Ruben van der Veen",),
  instructor: [Dhr. Bijlsma],
  university: [NHL Stenden],
  logo: image("/assets/logo/nhl-logo.jpg"),

  show-toc: true,
  acronyms: (
    "URM": "Uncertainty in Resistor Measurement",
  ),
  samenvatting: [Korte samenvatting van de meting.],
)

= Doel
...

= Meetopstelling
// `columns` auto-derives from header length. Pass `columns: ...` only
// when you want non-default sizing.
#measurement-table(
  (
    ([R₁ (kΩ)], [R₂ (kΩ)], [Vout (V)]),
    ([1.0], [2.2], [3.43]),
  ),
  caption: [Meetwaarden van de spanningsdeler.],
)

= Resultaten

// `result-section` emits a level-2 heading by default. Override `level:`
// when you nest it deeper.
#result-section(
  [Spanningsdeler],
  [$V_o = V_i dot R_2 / (R_1 + R_2)$],
  [$V_o = 5 dot 2.2 / 3.2 = 3.44$ V],
  [3.44],
  unit: [V],
)
```

## `testplan` — formal QA test plan

```typst
#import "@local/typst-tools:0.1.2": *

#show: testplan.with(
  title: [Testplan — Robothond Firmware],
  project-name: [Embedded Systems 2025-2026],
  version: "1.2",
  date: datetime.today(),
  authors: ("Ruben van der Veen", "Daan Smit"),
  reviewers: ("Perijn Huijser",),
  approver: "R. Moedt",
  organization: "NHL Stenden",
  logo: image("/assets/logo/nhl-logo.jpg"),

  version-history: (
    version-entry(
      contributors: "Team",
      department: "ELT",
      description: [Initieel testplan],
      date: "2026-02-01",
      level: 1,
    ),
  ),

  show-toc: true,
  show-version-history: true,
  executive-summary: [Dit testplan beschrijft...],
)

= Test Scope
#test-scope-table(
  in-scope: ("Firmware unit tests", "CAN-bus integratie"),
  out-of-scope: ("Mechanische belastingstesten",),
)

= Test Cases
#test-case-table(
  (
    (id: "TC-001", description: [Boot init], expected: [LED knippert],
     type: [Unit], priority: [High]),
  ),
)
```
