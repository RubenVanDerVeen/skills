# Cheatsheet: math, citations, misc

## Inline math `$...$`

```markdown
Einstein wrote $E = mc^2$ in 1905.
```

Pandoc-style guards - inline math only renders when all hold:

- Opening `$` is not followed by a space; closing `$` is not preceded by one (`$ x^2 $` stays literal).
- Content is single-line (no newline between the dollars).
- An unescaped `$` inside aborts; escape literal dollars as `\$`.
- Pure amounts stay literal: `$100$`, `$100$ and $200$` are currency text, never math.
- A digit right after the closing `$` blocks rendering (`$x^2$5` stays literal), so money prose like `5$ and 6$` is safe.
- KaTeX is the renderer; any KaTeX-supported LaTeX works.

## Block math `$$`

`$$` on their own lines, LaTeX between:

````markdown
$$
\int_0^1 x^2 \, dx = \frac{1}{3}
$$
````

## Citations

Three kinds only - the grammar is fixed on both console sides, do not invent variants:

```markdown
As shown in [web:arxiv-2401.12345] and [local:dossier-2026-06] ...
```

| Kind | Points at |
|---|---|
| `[local:id]` | Research corpus artifact |
| `[session:id]` | Console chat session |
| `[web:id]` | Web source |

Renders as a clickable source chip; stays literal inside code spans and fences. Used mainly in research dossiers; regular notes use wikilinks instead.

## What is plain markdown

Everything else is GitHub-flavored Markdown: headings, lists, tables, task
lists, blockquotes, fenced code blocks, links `[label](url)`. Extensions
never fire inside code spans or fences, so all syntax above documents
literally inside backticks.

## HTML

Raw HTML is stripped by the sanitizer. If markup shows up wrong in the
viewer, it is usually raw HTML; rewrite it in markdown.

## PDF export parity

| Construct | Viewer | PDF export |
|---|---|---|
| Images + `{N%}` widths | yes | yes |
| Columns fence | yes | yes |
| KaTeX math | yes | yes |
| `plot` fence | interactive chart | static SVG (subset of expressions) |
| `mermaid` fence | SVG diagram | source box, "not rendered in PDF" |
| File embeds (xlsx/pdf) | chip / inline viewer | none |

If a note must read well as PDF, prefer tables and `plot` fences over
mermaid diagrams and file embeds.
