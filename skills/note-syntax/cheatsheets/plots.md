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

## 3D surfaces

The same ` ```plot ` fence also draws a 3D surface: add `"type": "surface"`.
Without `type` (or with any other value) the fence renders as a 2D chart, so
existing 2D notes are unchanged.

````markdown
```plot
{ "type": "surface", "fn": "x^2 + y^2", "x": [-3, 3], "y": [-3, 3] }
```
````

| Field | Required | Meaning |
|---|---|---|
| `type` | no | `"surface"` switches to 3D. Any other value stays 2D. |
| `fn` | yes (3D) | Expression over `x` and `y`, see below. |
| `x`, `y` | yes (3D) | `[min, max]` domain per axis. |
| `samples` | no | Grid resolution, default 48. Viewer clamps to 16..128, PDF to 16..64 per axis. |

Extra fields are ignored.

### Surface expressions

Operators `+ - * / ^ %` (`^` = power), implicit multiplication (`2x`,
`3(x+1)`, `x y`, `2 sin(x)`), constants `pi`, `tau`, `e`, and these
whitelisted functions only:

    sin  cos  tan  asin  acos  atan  atan2
    sinh cosh tanh
    sqrt cbrt
    log  log2  log10
    exp
    abs  floor  ceil  round  min  max  sign

Anything outside the whitelist (assignment, semicolons, unknown names,
attributes) fails to compile and the fence falls back to a "could not parse"
placeholder; the note still renders. Singularities are fine: NaN cells are
gap-filled (see the sinc example below).

### Surface interaction, rendering, limits

- Viewer: interactive surface. Drag rotates the camera, wheel zooms, Reset view button restores the default camera, Viridis colormap. plotly is lazy-loaded only when a note actually contains a surface.
- PDF export: static isometric wireframe with the same Viridis colormap; no chromium in the export path.
- Bad payloads (unknown `type`, missing `fn` / `x` / `y`, unknown tokens, unparseable JSON) fall back to the literal source, exactly like bad JSON in 2D.
- Fixed limits: Viridis only (no custom colormaps, colorbars, or z-domain clamping), one surface per fence, no parametric plots or contour overlays.

### Surface examples

Saddle:

````markdown
```plot
{ "type": "surface", "fn": "x^2 - y^2", "x": [-2, 2], "y": [-2, 2] }
```
````

Sinc ring (singularity at the origin is gap-filled):

````markdown
```plot
{ "type": "surface", "fn": "sin(sqrt(x^2 + y^2)) / sqrt(x^2 + y^2)", "x": [-10, 10], "y": [-10, 10] }
```
````

Higher grid density:

````markdown
```plot
{ "type": "surface", "fn": "y * sin(x)", "x": [-3.14, 3.14], "y": [-3, 3], "samples": 64 }
```
````

## Plot, surface, or mermaid?

- Function charts, data series, math curves: `plot` (no `type`).
- 3D landscape of `f(x, y)`: `plot` with `"type": "surface"`.
- Diagrams, flow, structure: `mermaid`.
