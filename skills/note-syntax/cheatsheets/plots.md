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

## 3D lines

The same fence also draws 3D parametric curves and point polylines: add `"type": "line"`.

````markdown
```plot
{
  "type": "line",
  "curves": [
    {"fn": ["cos(t)", "sin(t)", "t/4"], "t": [0, 6.283], "samples": 200, "color": "#d62728", "label": "helix"}
  ]
}
```
````

`curves` is a non-empty array; every entry is **either**:

| Form | Shape |
|---|---|
| `fn` (parametric) | Three expression strings `[fx, fy, fz]` over parameter `t`, with optional `t: [t0, t1]` (default `[0, 2pi]`) and optional `samples` (default 200, clamped **16..500** on both sides). |
| `points` (polyline) | Array of `[x, y, z]` triples; each entry is exactly 3 finite numbers. No sampling. |

Both forms accept an optional per-curve `color` (default cycles the same 10-color palette as 2D) and `label` (default = the three `fn` strings joined with `", "`, or `"points"` for a polyline).

### Line expressions

Same safe subset as 3D surfaces: operators `+ - * / ^ %` (`^` = power), implicit multiplication (`2t`, `t(t+1)`, `2 sin(t)`), constants `pi`, `tau`, `e`, and these whitelisted functions only:

    sin  cos  tan  asin  acos  atan  atan2
    sinh cosh tanh
    sqrt cbrt
    log  log2  log10
    exp
    abs  floor  ceil  round  min  max  sign

The only variable is `t`; `x` / `y` / `z` are rejected. A non-finite sample or `|value| > 1e6` closes the pen inside one curve, so the next valid sample starts a fresh segment (pen-up gaps, same rule as the 2D path).

### Line interaction, rendering, limits

- Viewer: one plotly `scatter3d` (`mode: "lines"`) trace per curve, with the curve's color; legend chips follow the 2D dot+label convention. Drag rotates, wheel zooms, Reset view restores the default camera.
- PDF export: static isometric polylines sharing the surface projection (one `<path>` per curve, dot+label legend); pen-up gaps kept.
- Bad payloads (unknown `type`, malformed top level, all curves invalid) fall back to literal source, like bad JSON in 2D. Invalid curves inside a valid top level are skipped individually, not the whole fence.
- Fixed limits: one trace type per fence (don't mix surface + line or line + vector), no camera presets, no axis chrome.

### Line examples

Helix (parametric, `t` in `[0, 4π]`):

````markdown
```plot
{
  "type": "line",
  "curves": [
    {"fn": ["cos(t)", "sin(t)", "t/4"], "t": [0, 12.566]}
  ]
}
```
````

Polyline read straight from collected points:

````markdown
```plot
{
  "type": "line",
  "curves": [
    {"points": [[0, 0, 0], [1, 1, 0], [2, 0, 1], [1, -1, 1]], "label": "poly"}
  ]
}
```
````

## 3D vectors

The same fence also draws 3D arrow fields: add `"type": "vector"`.

````markdown
```plot
{
  "type": "vector",
  "vectors": [[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0]],
  "color": "#1f77b4"
}
```
````

| Field | Required | Meaning |
|---|---|---|
| `vectors` | yes | Non-empty array of `[x, y, z, dx, dy, dz]` entries (tail position + direction, each exactly 6 finite numbers). |
| `color` | no | Single stroke color for every arrow. Default `#1f77b4`. |

### Vector interaction, rendering, limits

- Viewer: one plotly `cone` trace (`anchor: "tail"`, absolute sizing) per fence; no legend chips. Drag rotates, wheel zooms, Reset view restores the default camera.
- PDF export: static isometric shaft + arrowhead per arrow (one `<line>` shaft + two short `<line>` strokes at the projected tip), sharing the surface projection.
- Bad payloads (unknown `type`, malformed top level, no valid entries) fall back to literal source, like bad JSON in 2D. Invalid entries inside a valid top level are skipped individually, not the whole fence.
- Fixed limits: one trace type per fence, single shared color (no per-vector colors, no vector labels or legend).

### Vector example

Coordinate basis at the origin:

````markdown
```plot
{
  "type": "vector",
  "vectors": [[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]
}
```
````

## Plot, 3D, or mermaid?

- Function charts, data series, math curves: `plot` (no `type`).
- 3D landscape of `f(x, y)`: `plot` with `"type": "surface"`.
- 3D parametric curves or point polylines: `plot` with `"type": "line"`.
- 3D arrows (single or small field): `plot` with `"type": "vector"`.
- Diagrams, flow, structure: `mermaid`.
