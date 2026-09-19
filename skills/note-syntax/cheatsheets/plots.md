# Cheatsheet: plot fence

A ` ```plot ` fence draws an interactive function chart. The fence body is
[function-plot](https://github.com/benmarren/function-plot) options as JSON.

````markdown
```plot
{
  "xAxis": {"domain": [-3, 3]},
  "yAxis": {"domain": [-2, 8]},
  "data": [
    {"fn": "x^2"},
    {"fn": "2x + 1", "color": "#d62728"}
  ]
}
```
````

## Options that matter

| Option | Meaning |
|---|---|
| `xAxis.domain`, `yAxis.domain` | `[min, max]` axis ranges. Set them explicitly; plots without ranges are hard to read. |
| `grid` | Grid lines. On by default; `"grid": false` turns them off. |
| `data[].fn` | Function of `x` drawn as a curve. |
| `data[].points` | Point series: `[[1, 2], [2, 4], ...]`. |
| `data[].color` | Per-series hex color. Omitted series get the default palette in order: blue, orange, green, red, purple, brown, pink, grey, olive, cyan. |
| `data[].graphType` | `"scatter"` for point clouds (points default to connected polylines otherwise). |

## Function expressions

In `fn`, use `x`, operators `+ - * / ^`, parentheses, and the usual functions:
`sin cos tan sqrt exp log abs`, constants `pi`, `e`. Implicit multiplication
works: `2x`, `3sin(x)`.

## Interaction and failure modes

- Drag pans, the mouse wheel zooms, and a Reset view button restores the default ranges. Viewer-only; none of this changes the note.
- Legend chips show each curve's formula (math-rendered) in its series color.
- Invalid JSON or a render failure shows the raw source in an error box inside the note; fix the JSON and it renders live in the editor.
- Width follows the container; height is fixed (about 280px).

## PDF export

Plots export as static SVG with the same palette, grid, and legend. There is
no zoom/pan in PDF, and the expression support is a safe subset (implicit
multiplication and `sqrt` included). Keep exotic expressions out of
PDF-critical notes.

## Plot or mermaid?

- Function charts, data series, math curves: `plot`.
- Diagrams, flow, structure: `mermaid`.
