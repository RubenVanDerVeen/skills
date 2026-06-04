# Library-internal idioms, common mistakes, troubleshooting, syntax reference

## Library-internal idioms (learned during the migration)

These patterns came up while authoring `typst-tools`. Apply them when writing new template / element / component code in the lib (or in user code that needs the same tricks).

### Reading counters in show rules requires `context`

`counter(heading).get()` directly inside a `show heading: it => {...}` rule does **not** read the live counter (modern Typst returns introspection-empty values). Wrap in `context`:

```typst
show heading: it => {
  if it.level == 1 and it.numbering != none {
    context {
      let chapter-num = counter(heading).at(it.location()).first()
      if chapter-num >= 2 { pagebreak(weak: true) }
      // ... emit heading ...
    }
  }
}
```

This is how `setup-headings()` triggers the pagebreak before chapter ≥ 2.

### Default-arg dicts containing `[#paramname]` capture lazily

A default like:

```typst
#let f(title: [...], footer-config: (short-title: [#title], ...)) = ...
```

renders the literal text `"title"` at footer time because `[#title]` captures a content closure; by the time the footer renders, `title` is no longer in scope. **Workaround**: use a sentinel and synthesize the dict inside the function body:

```typst
#let f(title: [...], footer-config: auto) = {
  let resolved = if footer-config == auto {
    (short-title: title, ...)
  } else {
    footer-config
  }
  ...
}
```

`IEEE-academic-journal` and `IEEE-academic-test-report` both use this pattern.

### `set page(columns: 2)` inside `if` scopes to the if-block

```typst
if two-column { set page(columns: 2) }   // applies to the rest of the if-block only
body                                     // ← back to single column!
```

Use an inline conditional value instead:

```typst
set page(columns: if two-column { 2 } else { 1 })
body
```

### Column gutter

`set columns(gutter: <length>)` applies to both `columns(N, body)` blocks and pages with `set page(columns: N)`. Bump to `24pt` (or higher) for IEEE-style readability — `12pt` is too tight.

### Hyphenation in display-size titles

Add `hyphenate: false` on the title text element to prevent ugly `Pick-` / `ing` line breaks:

```typst
#text(size: 22pt, weight: "bold", hyphenate: false)[#title]
```

The lib's IEEE cover pages already do this.

### Path resolution

- **`image()` inside library code resolves relative to the library file, not the caller's file.** Templates accept image *content* via `image("path")` at the call site — never raw path strings. Example: `logo: image("/assets/logo/nhl-logo.jpg")` not `logo: "/assets/logo/nhl-logo.jpg"`.
- `image("/assets/x.jpg")` — absolute paths starting with `/` resolve from the **project root**. Preferred convention.
- Library internal `#import` paths use absolute `/src/...` form for clarity.
- `yaml("/assets/langs.yaml")` — lib assets at the package root use absolute paths. Works for both `@local` package imports and direct source-tree usage.
- **Library assets vs user project assets**: the lib ships `assets/logos/nhl_logo.jpg` (lib-internal). User projects place their own logo at `assets/logo/nhl-logo.jpg` (kebab/English convention). Legacy projects may still use `Assets/Logo/NHL_logo.jpg` (PascalCase). These are separate files — user documents reference their own project logo, not the lib's.

### Wrapping things in `figure(kind: table)`

Anything wrapped this way appears in the **List of Tables** outline. Don't wrap acronym indexes, decoration tables, or layout helpers in `figure(... kind: table)` unless you actually want them outlined. The lib's `make-acronyms` no longer wraps the index for this reason.

### Mid-document `set page(...)`

Triggering `set page(...)` mid-document forces a new page with the new settings. Used in `IEEE-academic-journal` to switch from full-width front-matter to two-column body. Combine with `place(scope: "parent", float: true, ...)` to keep titles spanning full width even after the column rule activates. (The `fullwidth` helper wraps exactly this — see `ieee-journals.md`.)

### Auto-deriving table column counts

`#table(columns: ..., ..cells)` with `columns: auto` collapses to a single column. To match an N-cell header, pass an array of width N:

```typst
let resolved-columns = if columns == none {
  range(data.first().len()).map(_ => auto)
} else {
  columns
}
```

`measurement-table` uses this to auto-derive column count from the first row.

## Common mistakes to avoid

- Hand-rolling a cover page when one of the templates would do — **always check first**.
- Hand-rolling `slice_db`, `pve_render`, `moscow_range`, `bom_render` when the lib provides them.
- Re-importing preview packages on a per-file basis when granular `src/...` imports avoid the duplication.
- Using `arr[0]` for array access (use `arr.at(0)`).
- Using `[]` for arrays or `()` for content (mix-up).
- Forgetting `#` in markup/content blocks (e.g., `text[numbering(...)]` should be `text[#numbering(...)]`).
- Using `#` inside argument lists (`figure(#image(...))`).
- Calling things "tuples" — Typst only has arrays.
- Calling `init-acronyms(...)` manually — the template handles it.
- Forgetting `#set text(lang: "Nl")` on Dutch documents (affects hyphenation, dates, and `transl` lookups).
- Using LaTeX syntax (`\begin{...}`, `\section`, `tabular`) — these don't exist in Typst.
- Hardcoding paths for `assets/logo/nhl-logo.jpg` instead of project-root absolute (`/assets/logo/...`). Legacy projects: `/Assets/Logo/NHL_logo.jpg` — match the casing the project already uses; do **not** rename casing as a side effect of an unrelated edit.
- Renaming Dutch folder/file names → kebab/English in a legacy project without being asked. New projects use kebab/English; old projects keep their existing names until the user explicitly requests a migration. Partial renames break compilation because paths are referenced from many files (subdocs, research papers, bib references, image calls).
- Bumping `@local/typst-tools` version inconsistently across files in the same project — keep them in sync.
- **Rewriting an existing `@local/typst-tools:<X.Y.Z>` import back to `0.1.2` because that's the version shown in this skill's examples.** `0.1.2` is a baseline, not a mandate. Preserve whatever version the project already pins. Only fall back to `0.1.2` for brand-new files with no sibling reference. See **Version pinning** in `SKILL.md`.
- Using em-dash (`—`) or sentence-level hyphen (`-`) in body prose. Use `.`, `;`, or `,` instead. Hyphens in compound words and identifiers are fine.
- Over-bolding keyword emphasis in IEEE papers — use italic for mid-sentence terms, bold only for headings and colon-terminated run-in labels (see `ieee-journals.md`).
- Using the old `version(committee: ...)` constructor — that's `version-entry(contributors: ...)` now.
- Spelling `IEEE-academic-test-repport` (the old typo) — it's `IEEE-academic-test-report` now.
- Using uppercase `ID:` for section-DB rows — the lib now keys off lowercase `id:` (matches `moscow-category.id`).
- Importing `src/components/moscow.typ` — that file is gone; use `src/renderers/moscow-renderer.typ` (or just the umbrella `lib.typ`).
- Importing `src/elements/...` or `src/styling/...` — those folders are renamed to `src/components/` and `src/styles/` respectively.
- Hand-rolling a "Prioritisering / Uitleg / Indicatie" legend — use `moscow-legend(cells: pc, show-indicator: true)` instead.
- Calling `make-priority-cells()` and assuming it pulls a project palette — it doesn't. Pass per-priority RGB overrides explicitly when the project palette differs from `default-theme`.
- Forgetting to pass `cells: pc` to `moscow-table` / `moscow-range` / `moscow-grouped` / `moscow-legend` when you've bound a custom palette — the renderer falls back to the theme palette otherwise.
- Forgetting to pass `colors:` to `bom-range` / `bom-render` — defaults are decent but won't match a project's primary/light tokens.
- Passing raw string paths to `image-grid` — it accepts content. Wrap with `image("path")`.
- Forgetting `render-item: pve-item` on `section-range-render` with typed `moscow-item` data — items have `.description` not `.text`.
- Using `project.university` after migrating to `metadata()` type — it's `project.institution` now.
- Using `project.startdate` / `project.enddate` — these are now `project.start-date` / `project.end-date` on `metadata`.
- Using `project.lokaal` — renamed to `project.room`.
- Accessing `s.opleiding` on student entries — `author` type uses `s.affiliation` instead.
- Putting a `#show:` rule inside `config/config-general.typ` (legacy: `GeneralConfig.typ`) — each document declares its own template.
- Forgetting to wire new exports into `lib.typ` after adding a util/helper to `src/`.

## Troubleshooting

### `package not found: @local/typst-tools`

Pkg isn't installed in the local data dir. Source lives at `C:\Users\ruben\Projects\Tools\TypstTools\`. Copy or symlink to the Typst local packages directory. On Windows: `%APPDATA%\typst\packages\local\typst-tools\0.1.2\`.

### `package not found: @local/academic-tools`

Project still imports the old name. Update imports to `@local/typst-tools:0.1.2` and apply the migration steps (see `migration.md`). Or, as a temporary measure, install the old `academic-tools` v0.1.29 alongside.

### `unknown variable: acr` / acronyms not expanding

`acrostiche` wasn't initialized. Make sure the template was given `acronyms: (acronyms_db)` — that's what triggers `init-acronyms`. The `#acr(...)` call must come **after** the show-set rule that runs the template.

### `unknown font family`

Remove the font specification or install the font. Compilation succeeds with a fallback; only the warning appears.

### "expected content, found ..." / "expected expression, found ..."

You're using code where markup is expected (or vice versa). Wrap with `#{ }` for code in markup, or check for a missing `#`.

### Heading "Hoofdstuk 2" sits on the same page as "Hoofdstuk 1"

`setup-headings()` from `src/styles/base.typ` only fires the pagebreak when (a) the heading is level 1, (b) `it.numbering != none`, and (c) the **live** counter (read inside `context`) is ≥ 2. If pagebreaks aren't firing, check that you didn't override `set heading(numbering: ...)` to `none` after the show-set rule, and that the heading detection is wrapped in `context`. The current lib version has the fix.

### IEEE journal footer prints literal `title` / `vversion`

This was the default-arg lazy-capture bug. Fixed in `0.1.2` by switching the default to `auto` and synthesizing inside the fn body. If the user is on an older snapshot, advise upgrading or pass an explicit `footer-config: (...)` dict.

### Two-column body extends to the cover page

`set page(columns: 2)` was probably placed before the cover / front-matter. The lib applies it **after** front-matter for this reason. When writing your own template, insert the column rule between the front-matter block and the body emission.

### Compilation fails after bumping `typst-tools`

Check the changelog / git history at `C:\Users\ruben\Projects\Tools\TypstTools\`. Breaking changes between minor versions are not unusual; pin the version per file. The migration table (see `migration.md`) covers the `academic-tools:0.1.29` → `typst-tools:0.1.2` shift. If a bump broke things, **roll back to the previously-pinned version** rather than re-pinning everything to `0.1.2` — `0.1.2` is just the baseline used in this skill's examples, not necessarily the safest version for any given project.

### Acronyms appear in the List of Tables

Old `make-acronyms` wrapped the index in `figure(kind: table)`. Fixed in `0.1.2`. If still seen, you're either on an older version or you've wrapped your own `print-index(...)` call in a figure.

## Quick syntax reference

### Critical distinctions

- **Arrays**: `(item1, item2)` (parentheses, comma-separated). Singleton: `(elem,)`.
- **Dictionaries**: `(key: value, key2: value2)` (parentheses with colons).
- **Content blocks**: `[markup content]` (square brackets).
- **Code blocks**: `{...}` — only inside expressions.
- **No tuples**: Typst only has arrays.

### Hash usage (markup vs code)

- Use `#` to start a code expression inside markup or content blocks: `#figure[...]`, `#image("file.png")`, `text(...)[#numbering(...)]`.
- Do NOT use `#` inside code contexts (argument lists, code blocks, show-rule bodies): `figure(image("file.png"))`.

```typst
// Wrong (missing # inside content block)
text(...)[(numbering(...))]
// Right
text(...)[(#numbering(...))]
```

### Set vs show vs show-set

```typst
#set heading(numbering: "I.")           // configure params for an element
#set text(font: "New Computer Modern")
#show heading: set text(navy)            // show-set: apply set rule selectively
#show heading: it => block[#emph(it.body)] // show transform: replace output
```

### Array access

- Use `arr.at(0)` — **not** `arr[0]` (square brackets are content blocks).

### Function shorthand

- `#let f(x) = body` is shorthand for `#let f = (x) => body`. Both are valid.
- Default args may reference earlier args: `#let f(a: 1, b: a + 1) = b`.

### Imports

- Package: `#import "@preview/<pkg>:<version>": <names or *>`.
- Local package: `#import "@local/typst-tools:0.1.2": *`.
- Path: `#import "config/config-general.typ": *` (legacy: `Config/GeneralConfig.typ`).
- Module alias: `#import "lib/foo.typ" as foo` → call as `foo.bar(...)`.
- File include (executes body inline): `#include "/subdocs/<name>.typ"` (legacy: `Subdocumenten/X.typ`) or `#let X = include "..."`.

### Bibliography

- `references: bibliography("refs/<name>.bib")` is passed to `IEEE-academic-journal` (from `main.typ`). From `subdocs/` or `research/`: `references: bibliography("../refs/<name>.bib")`.
- Multiple bibs: `bibliography(("refs/ai.bib", "refs/hardware.bib"))`.
- For other templates use `bibliography("refs/<name>.bib", style: "ieee")` near the end of the body.
- Legacy Dutch layout: replace `refs/` with `Referenties/` throughout.

## Reference docs (Typst language)

The full Typst reference (guides, tutorials, function index) lives under the existing `typst-author/docs/` tree in the install. Use it for language-level questions (foundations, layout, math, visualize, introspection). This skill focuses on **the user's standardized workflow**; the reference docs cover **the language itself**.
