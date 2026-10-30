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
| `data[].points` | Point series: `[[1, 2], [2, 4], ...]`. Needs `fnType` **and** `graphType`, see `## Point series`. |
| `data[].color` | Per-series hex color. Omitted series get the default palette in order: blue, orange, green, red, purple, brown, pink, grey, olive, cyan. |
| `data[].graphType` | `"polyline"` for a smooth line, `"scatter"` for point clouds, `"interval"` for the boxy default. |
| `data[].fnType` | `"points"` for a point series (with `graphType`), otherwise `"linear"`. |

## Which renderer evaluates your `fn`

The fence body is raw function-plot JSON. Only the `data[].fn` strings are
rewritten before evaluation (constants to numeric literals, implicit
multiplication to explicit `*`); every other key is passed through
untouched.

| Path | Trigger | How `fn` is evaluated |
|---|---|---|
| 2D default | no `graphType` | function-plot's `interval` sampler (interval arithmetic) - the boxy interval look |
| 2D smooth | `"graphType": "polyline"` | function-plot's `builtIn` sampler over `Math` |
| 3D viewer | `"type": "surface"`, `"line"`, `"vector"` | the shared safe-subset compiler (a JS closure) |
| PDF export | any plot fence | the same safe-subset grammar, compiled to Python |

The two 2D samplers expose **different** function sets, so the same `fn`
string can work in one and fail in the other. A function outside the path's
set fails the fence: the chart is replaced by an error box with the raw
source.

## Function expressions

In `fn`, use `x`, the operators `+ - * / ^`, parentheses, and the constants
`pi`, `tau`, `e`. The constants are substituted as numeric literals before
evaluation, so they work in every path. Implicit multiplication works:
`2x`, `3sin(x)`.

## Symbol tables

| Function | 2D default | 2D `polyline` | 3D viewer | PDF export |
|---|---|---|---|---|
| `sin cos tan asin acos atan sinh cosh tanh` | yes | yes | yes | yes |
| `sqrt exp abs log` | yes | yes | yes | yes |
| `min max` | yes | yes | yes | yes |
| `cbrt floor ceil round` | no | yes | yes | yes |
| `sign` | no | yes | yes | yes |
| `atan2 log2 log10` | no | no | no | yes |

`sign`, `cbrt`, `floor`, `ceil` and `round` need an explicit
`"graphType": "polyline"` in 2D - the default interval namespace has no
`sign` and no `cbrt`, and its `round` is not callable.

`atan2`, `log2` and `log10` end in a digit, and the viewer tokenizer splits
the digit off (`log` + `2`); they are rejected or silently mangled there.
Only the PDF export accepts them. Keep notes viewer-safe and use `log(...)`.

## Powers and the exponential

`^` is the power operator, but the 2D default path only computes **integer**
powers: `x^2` and `x^3` draw, while `2^x`, `e^x` and `x^0.5` produce an empty
interval and draw nothing at all - axes and grid only, no error box.

Use `exp(...)` for an exponential; it is safe in every path:

    exp(x)                # instead of e^x
    exp(-60*x)            # instead of e^(-60*x)
    exp(-60*(x-t))        # a logistic step, see below

A constant integer exponent (`x^2`) is fine everywhere.

## Step and piecewise signals

### Continuous branches: clamp, do not build an indicator

Where two branches meet continuously, one closed form reproduces the signal
exactly (verified max error 2.2e-16) and renders as a single continuous
stroke:

    min(max(x, 0), 2) + 0.5 * (min(max(x, 2), 4) - 4)^2 - 2

The trailing `- 2` cancels the ramp term's constant leftover for `x <= 2`.

### A genuine jump: the logistic

A jump has no closed form; approximate it with a logistic (safe in every
engine):

    1/(1+exp(-60*x))              # rising step u(x)
    1/(1+exp(60*(x-t)))           # falling step u(t-x)
    0.5*(2/(1+exp(-60*x)) - 1)    # half sign function

A ramp on `[a, b]` is `body(t)` times two window factors - the first switches
on at `a`, the second off at `b`:

    body(t) * 1/(1+exp(-60*(t-a))) * 1/(1+exp(60*(t-b)))

Know the artifacts before you trust the curve:

- At the jump the plotted value is half the exact value (the logistic passes
  through 1/2).
- The error decays exponentially: about 5e-2 at a distance of 0.05 from the
  jump, 2.7e-3 at 0.1, 7e-6 at 0.2, machine precision beyond 0.5.
- The curve keeps an exponentially small tail on the wrong side of a jump
  (~1e-6 at a distance of 0.2), so the plotted signal is never exactly zero
  off-support.
- Never test the plotted curve for an exact zero - take the support from the
  branch definition.

## Point series

A `points` series needs the full key set: `fnType: "points"` **and**
`graphType: "polyline"` (or `"scatter"`). Anything less fails the fence - the
error box replaces the chart.

````markdown
```plot
{
  "data": [
    {"fnType": "points", "graphType": "polyline", "points": [[0, 0], [1, 1], [2, 0]]},
    {"fnType": "points", "graphType": "scatter", "attr": {"r": 5, "opacity": 1}, "points": [[0, 0], [1, 1]]}
  ]
}
```
````

Use `polyline` when the shape of the signal is the point. Scatter dots are
2 px by default and effectively invisible - add `"attr": {"r": 5, "opacity": 1}`.

## Interaction and failure modes

- Drag pans, the mouse wheel zooms, and a Reset view button restores the default ranges. Viewer-only; none of this changes the note.
- Legend chips show each curve's formula (math-rendered) in its series color. The legend collapses with the chevron at its right edge - a viewer affordance, no syntax needed.
- Invalid JSON or a render failure shows the raw source in an error box inside the note; fix the JSON and it renders live in the editor.
- Width follows the container; height is fixed (about 280px).

## PDF export

Plots export as static SVG with the same palette, grid, and legend. There is
no zoom/pan in PDF. The expression support is the shared safe subset
(implicit multiplication, `sqrt`, `sign`, `min`, `max` included), plus
`atan2`, `log2` and `log10`, which the viewer paths reject. Keep exotic
expressions out of PDF-critical notes.

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
| `type` | no | Absent or null = 2D; `"surface"` = 3D. Any other value falls back to literal source. |
| `fn` | yes (3D) | Expression over `x` and `y`, see below. |
| `x`, `y` | yes (3D) | `[min, max]` domain per axis. |
| `samples` | no | Grid resolution, default 48. Viewer clamps to 16..128, PDF to 16..64 per axis. |

Extra fields are ignored.

### Surface expressions

Operators `+ - * / ^ %` (`^` = power), implicit multiplication (`2x`,
`3(x+1)`, `x y`, `2 sin(x)`), constants `pi`, `tau`, `e`, and these
whitelisted functions only:

    sin  cos  tan  asin  acos  atan
    sinh cosh tanh
    sqrt cbrt
    log
    exp
    abs  floor  ceil  round  min  max  sign

`atan2`, `log2` and `log10` are **not** in the viewer whitelist: a function
name that ends in a digit is split by the tokenizer (`atan` + `2`). The PDF
export accepts them; the 3D viewer does not.

Anything outside the whitelist (assignment, semicolons, unknown names,
attributes) fails to compile and the fence falls back to a "could not parse"
placeholder; the note still renders. Singularities are fine: NaN cells are
gap-filled (see the sinc example below).

### Surface interaction, rendering, limits

- Viewer: interactive surface. Drag rotates the camera, wheel zooms, Reset view button restores the default camera, Viridis colormap. plotly is lazy-loaded only when a note actually contains a surface.
- PDF export: static isometric wireframe with the same Viridis colormap; no chromium in the export path.
- Bad payloads (unknown `type`, missing `fn` / `x` / `y`, unknown tokens, unparseable JSON) fall back to the literal source, exactly like bad JSON in 2D.
- Fixed limits: Viridis only (no custom colormaps, colorbars, or z-domain clamping), one surface per fence, no contour overlays. Parametric curves live in `## 3D lines`.

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

    sin  cos  tan  asin  acos  atan
    sinh cosh tanh
    sqrt cbrt
    log
    exp
    abs  floor  ceil  round  min  max  sign

As with surfaces, `atan2`, `log2` and `log10` are rejected by the viewer
(tokenizer splits the trailing digit); the PDF export accepts them.

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
