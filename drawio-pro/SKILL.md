---
name: drawio-pro
description: Use when generating, editing, or exporting draw.io diagrams (`.drawio`) — block diagrams, flowcharts, architecture diagrams, ER/sequence/class diagrams, network diagrams, mockups. Captures the user's personal diagram style: pastel grouped containers for block diagrams, standard BPMN-style shapes for flowcharts, orthogonal routing, light-grey legend boxes. Overrides the generic `drawio` skill — when both are available, prefer this one.
---

# drawio-pro skill

## Overview

Generate `.drawio` files in the user's standardized visual style. Two diagram families are explicitly supported:

- **Block / system diagrams** — color-coded grouped containers, white component blocks inside, full-width bus rails, dashed power-distribution edges, legend bottom-right. Matches `electrical/block-diagrams/remote-controller.drawio`.
- **Flowcharts** — terminator ellipses for start/stop, plain rectangles for actions, rhombi for decisions, parallelograms for I/O, "Ja" / "Nee" labels on decision branches. Matches `Schoolwork/P2_Embedded2A/Uitwerkingen/Opdracht{2,3}/flowchart_opdr*.drawio`.

When this skill loads, **prefer the templates and palettes below over hand-rolling colors, edge styles, or shape choices**. Only fall back to free-form drawio when the user explicitly asks for a non-standard look.

The fallback / generic drawio skill (the public one shipped with most agent harnesses) has CLI lookup, post-processing, and export instructions. The **process** parts (locating the CLI, running export, opening the result) are still valid. This skill **adds** the user's visual style on top of that process.

## When to use

- User says: "draw a block diagram", "maak een blokschema", "flowchart", "stroomdiagram", "architecture diagram", "ER diagram", "sequence diagram", "class diagram", "wireframe", "mockup".
- User mentions: `draw.io`, `drawio`, `.drawio`.
- User asks to edit an existing `.drawio` file.
- User exports diagrams to PNG / SVG / PDF.

**Do NOT use for:** Mermaid (use raw markdown), PlantUML, ASCII art, Graphviz `dot` files. Those are separate formats with their own toolchains.

## File scaffold

Every `.drawio` file starts with this exact wrapper. The `host="65bd71144e"` value matches the user's drawio desktop install — keep it identical so files diff cleanly when round-tripped.

```xml
<mxfile host="65bd71144e">
    <diagram id="<short-id>" name="<short-name>">
        <mxGraphModel dx="1422" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="1000" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <!-- diagram cells with parent="1" -->
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

**Page sizing conventions:**

| Diagram type | `pageWidth` × `pageHeight` | Orientation |
|---|---|---|
| Block / system diagram (wide) | 1400 × 1000 | landscape |
| Flowchart (single column) | 700 × 1100 | portrait |
| Flowchart (parallel functions side-by-side) | 850 × 1300 or wider | portrait |

**Universal hard rules:**

- All vertex / edge `mxCell`s have `parent="1"`.
- Every `mxCell` has a unique `id`. Mix of named (`esp32`) and numeric (`23`) is fine — use named IDs for components you'll reference in edges, numeric for plain edges.
- All coordinates and sizes snap to the **10-pixel grid** (`gridSize="10"`).
- **Never** include XML comments inside `<mxGraphModel>` — drawio strips them silently and they can corrupt round-trip diffs.
- Multi-line labels: use `&#xa;` inside `value="..."`. Rich formatting: HTML inline (`<br>`, `<font>`, `<span style="...">`).
- Edges always carry `<mxGeometry relative="1" as="geometry"/>` as a child element (not self-closing).

## Block-diagram style

### Group containers

Group related components in labeled, color-coded rectangles. The container holds the title; components live inside with their own white-fill rounded rectangles.

```xml
<mxCell id="grpPwrIn" value="POWER INPUT &amp; CHARGE"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;verticalAlign=top;fontStyle=1;fontSize=12"
        parent="1" vertex="1">
    <mxGeometry x="40" y="60" width="300" height="200" as="geometry"/>
</mxCell>
```

Key style flags:

- `rounded=0` — sharp corners (containers, NOT components).
- `verticalAlign=top` — title sits in the header band.
- `fontStyle=1` — bold title (`fontStyle=2` italic for sub-labels).
- `fontSize=12` — container titles. Components default 12, sub-labels 10.
- Title text uppercase. `&amp;` for `&` literal.

### Color palette

| Domain / role | fillColor | strokeColor | Typical use |
|---|---|---|---|
| Power input / charge | `#fff2cc` | `#d6b656` | USB-C, charge IC, AC mains |
| Battery / MCU / safe | `#d5e8d4` | `#82b366` | Cell + BMS, MCU + radio, "OK" path |
| Regulation / display / cool | `#dae8fc` | `#6c8ebf` | Buck-boost, LCD, output |
| Monitor / aux | `#e1d5e7` | `#9673a6` | Battery monitor, telemetry |
| Safety / fault / rail | `#f8cecc` | `#b85450` | E-stop, alarm, 3.3 V/5 V rail block |
| HMI / I/O / warm | `#ffe6cc` | `#d79b00` | Buttons, joysticks, sensors |
| Legend / annotation | `#f5f5f5` | `#666666` | Legend box, footnote box |

Pick by **semantic role**, not aesthetics. The same color must mean the same thing across the diagram.

### Component blocks

Inside containers, components are **rounded** rectangles with white fill + black border:

```xml
<mxCell id="ip2312" value="IP2312&#xa;1S Li-ion charger&#xa;USB-C, ~2A, power-path"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000"
        parent="1" vertex="1">
    <mxGeometry x="200" y="100" width="120" height="80" as="geometry"/>
</mxCell>
```

Standard component sizes: `120×60` (single line), `120×80` (3 lines), `160×100` (joystick / multi-line). Match heights within a row so the bottom edges align.

### Bus rails

Power / data rails span multiple groups as a single full-width rectangle, with a domain color (red for safety-critical 3.3 V supply, etc.). They are **vertices** (not edges) so they can carry a label and be a connection target.

```xml
<mxCell id="rail33" value="3.3 V rail"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12"
        parent="1" vertex="1">
    <mxGeometry x="250" y="320" width="790" height="30" as="geometry"/>
</mxCell>
```

### Edge conventions

| Meaning | Style fragment |
|---|---|
| Solid signal / power flow | `endArrow=classic;html=1;` |
| Dashed power-supply distribution (rail → consumer) | `endArrow=classic;html=1;dashed=1;` |
| Safety / fault path | add `strokeColor=#b85450;strokeWidth=2;` |
| Direct line | `edgeStyle=none;` (default) |
| Routed around obstacles | `edgeStyle=orthogonalEdgeStyle;` |

Always anchor with explicit attach points so the line stays glued when you reflow:

```xml
<mxCell id="eUsbToIp"
        style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=11"
        parent="1" source="usbc" target="ip2312" edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

`exitX/exitY/entryX/entryY` are normalized 0–1: `0` = top/left, `0.5` = center, `1` = bottom/right. Center sides (`0.5/0` top, `1/0.5` right, `0.5/1` bottom, `0/0.5` left) are the readable defaults.

For routes that bend around blocks, list waypoints:

```xml
<mxGeometry relative="1" as="geometry">
    <Array as="points">
        <mxPoint x="670" y="230"/>
        <mxPoint x="670" y="140"/>
    </Array>
</mxGeometry>
```

Edges can label themselves: add `value="3.3 V"` (and `fontStyle=1` for emphasis). Labels on bus drops and signal labels (e.g. `SPI + BL`, `ADC (Vbat)`) are common and helpful.

### Legend box

Bottom-left of the page (the bottom-right corner is reserved for the title block — see next section), light grey, left-aligned text:

```xml
<mxCell id="legend"
        value="Legend:&#xa;— solid arrow = signal / power flow&#xa;— dashed arrow = 3.3 V supply distribution&#xa;— red = safety (e-stop) / battery monitor&#xa;&#xa;Reference designators are placeholders. To be assigned in schematic."
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;align=left;verticalAlign=top"
        parent="1" vertex="1">
    <mxGeometry x="40" y="830" width="320" height="100" as="geometry"/>
</mxCell>
```

Keep it small (~240–320 × 100). Always include it on a non-trivial block diagram.

### Page title (top header)

A full-width plain text cell at the top, bold 18pt, centered:

```xml
<mxCell id="title" value="Handheld Remote Controller — Block Diagram (rev A)"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1"
        parent="1" vertex="1">
    <mxGeometry x="40" y="10" width="1320" height="30" as="geometry"/>
</mxCell>
```

Use `—` (em-dash) to separate scope and revision marker. Keep titles in English even when labels are Dutch — keeps the diagram skim-friendly across disciplines.

### Title block (engineering metadata, bottom-right)

ASME-style title block in the bottom-right corner. **Always include** on every formal block diagram — it identifies project, owner, revision, sheet number for printed/exported drawings.

Outer footprint: **400 × 150** in the bottom-right corner, with a 20 px margin to the page edges. For a 1400 × 1000 page, place at `x=980 y=830`.

Cell layout (all cells `parent="1"`, `vertex="1"`, IDs prefixed `tb*`):

| Row | Cell | x | y | w | h | Field |
|---|---|---|---|---|---|---|
| 1 | `tbProj` | 980 | 830 | 300 | 40 | **Project** + project subtitle |
| 1 | `tbOrg` | 1280 | 830 | 100 | 40 | School / company name |
| 2 | `tbTitle` | 980 | 870 | 400 | 30 | **Drawing** + drawing title |
| 3 | `tbDrawn` | 980 | 900 | 140 | 40 | **Drawn by** + name |
| 3 | `tbDate` | 1120 | 900 | 130 | 40 | **Date** + ISO date |
| 3 | `tbRev` | 1250 | 900 | 130 | 40 | **Rev** + letter (A, B, ...) |
| 4 | `tbTutor` | 980 | 940 | 140 | 40 | **Tutor** / **Checked by** + name |
| 4 | `tbScale` | 1120 | 940 | 130 | 40 | **Scale** (NTS for block diagrams) |
| 4 | `tbSheet` | 1250 | 940 | 130 | 40 | **Sheet** + `1 / 1` etc. |

Cell style — same on every cell:

```text
rounded=0;whiteSpace=wrap;html=1;
fillColor=#ffffff;strokeColor=#000000;
align=left;verticalAlign=top;
fontSize=9;spacingLeft=4;spacingTop=2
```

Exception — `tbTitle` (drawing-title row) uses `align=left;verticalAlign=middle;fontSize=10` so the longer drawing title sits centered vertically in its 30 px row.

Exception — `tbOrg` (school/company cell) uses `align=center;verticalAlign=middle` for a centered logo-style organization name.

Cell value HTML pattern: bold field label on first line via `<b>...</b>`, value on the next line via `<br>`:

```text
<b>Drawn by</b><br>R. van der Veen
<b>Date</b><br>2026-04-26
<b>Rev</b><br>A
```

For the drawing-title cell, label and value go on the same line (the row is shorter):

```text
<b>Drawing</b>&nbsp;&nbsp;Handheld Remote Controller — Block Diagram
```

Optional: an outer 1.5 px border `mxCell id="tbBox"` around the whole 400×150 footprint as a single rectangle behind the cells, for a slightly thicker outer frame:

```xml
<mxCell id="tbBox" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1.5"
        parent="1" vertex="1">
    <mxGeometry x="980" y="830" width="400" height="150" as="geometry"/>
</mxCell>
```

When the page is **smaller** than 1400 × 1000, scale the title block proportionally — keep it at the bottom-right with a 20 px margin, but you can shrink to 320 × 120 on a 1000-wide page. **Don't** make it wider than 30 % of the page width.

When the page is **portrait** (flowcharts), the title block goes at the bottom-right too, but the drawing-title row may need to wrap to two lines — use `verticalAlign=top` and bump the row to 40 px.

### Layout discipline

1. **Top row**: input → primary processing → output, left to right.
2. **Bus rail**: horizontal across the diagram, between the top row and the consumers.
3. **Consumer row**: HMI / sensors / display below the bus rail.
4. **Aux blocks** (battery monitor, programming header): in margins, with their own pastel container.
5. **Legend**: bottom-left.
6. **Title block**: bottom-right (engineering metadata — always present).
7. **Spacing**: minimum 20 px between containers; align top edges within a row.

When 4–5 groups don't fit horizontally, drop the consumer row to the second tier and let the bus rail span the page width.

## Flowchart style

### Page setup

Portrait. Single column at one fixed x (e.g. `x=120` or `x=240`). Multiple independent functions go side-by-side at distinct columns (e.g. `x=120`, `x=500`, `x=1000`) — same flowchart file, different start/stop ellipses per function.

### Shape catalog

| Role | Shape | Style fragment | Default size |
|---|---|---|---|
| Start / Stop terminator | Ellipse | `ellipse;whiteSpace=wrap;html=1;` | 120×60 |
| Process / Action | Plain rectangle | `rounded=0;whiteSpace=wrap;html=1;` | 120×50 |
| Decision | Rhombus | `rhombus;whiteSpace=wrap;html=1;` | 91.75×90 (or 123.5×120 for long predicates) |
| Input / Output | Parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=10` | 147.5×40 |

**No fill colors.** Flowcharts use the drawio theme default (transparent / white), no per-domain palette. Color only when a single block needs to stand out (e.g. an error path).

### Edge conventions

| Meaning | Style |
|---|---|
| Direct vertical / horizontal hop between stacked blocks | `edgeStyle=none;` |
| Branch from a decision / orthogonal route around blocks | `edgeStyle=orthogonalEdgeStyle;` |
| Loop-back to a prior block | `edgeStyle=none;` with `<Array as="points">` waypoints |

Decision branches **must be labeled**. Convention:

- **Down** = `Ja` (yes), continue normal flow.
- **Right or Left** = `Nee` (no), exit / loop / alternate path.

```xml
<mxCell id="e7" value="Ja"
        style="edgeStyle=orthogonalEdgeStyle;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
        parent="1" source="34" target="38" edge="1">
    <mxGeometry x="-0.5" relative="1" as="geometry"/>
</mxCell>
```

Loop-back from end-of-loop body to top of decision: orthogonal route via the side, with explicit corner waypoints:

```xml
<mxGeometry relative="1" as="geometry">
    <mxPoint x="300" y="710" as="targetPoint"/>
    <Array as="points">
        <mxPoint x="40" y="1220"/>
        <mxPoint x="40" y="710"/>
    </Array>
</mxGeometry>
```

When source or target is a free point (not a vertex), use `<mxPoint .../>` with `as="sourcePoint"` / `as="targetPoint"`.

### Layout discipline

1. **Vertical pitch**: 90 px between consecutive blocks (50 px block + 40 px gap).
2. **Column alignment**: every block at the same x within a function. Decision rhombi off-center horizontally to balance their wider footprint — keep their **center** on the column.
3. **Multiple functions**: keep their start/stop pairs aligned horizontally so readers can compare entry/exit at a glance.
4. **Loop-back lanes**: route on the outside of the column (left for one decision, right for another) to avoid crossings.

### Language

Body text in **Dutch** for school flowcharts (`Start (main)`, `Roep X aan`, `Bereken Y`, `Toon Z`, `Stop (return 0)`). Predicate inside rhombus uses C-like syntax (`i &lt; 5`, `base &lt; 90000`) — escape `<` and `>` in XML.

## Workflows

### Creating a new block diagram

1. Decide page size (default 1400×1000 landscape).
2. Lay out the **groups** first, on a sheet of paper or mentally — assign each its color from the palette above.
3. Write the file: title → groups (in reading order) → components inside each group → bus rails → edges → legend.
4. Add domain-specific edges (data flow, supply distribution).
5. Sanity-check edge anchors: every edge with `source=` / `target=` should still resolve if you move the endpoints.
6. Run optional `npx @drawio/postprocess <file>` if available — it tightens edge routing.
7. Open in drawio (CLI export to PNG/PDF if requested — see generic skill for command).

### Creating a new flowchart

1. Pick portrait page (700×1100 default).
2. Sketch the function on paper, identifying terminators, processes, decisions, I/O.
3. Place the start ellipse at `(120, 40)` (or your column origin); flow downward at 90 px pitch.
4. Decisions: rhombus with `Ja` going down, `Nee` going to the side.
5. Loops: orthogonal route around the outside back to the decision.
6. Multiple functions: repeat at offset x columns (`+380`, `+760` typical).

### Editing an existing diagram

1. Read the file to identify scope and existing IDs.
2. Match the existing style — don't introduce new colors or shape conventions.
3. When adding a new component, copy an adjacent component's `style` string verbatim, then change `value` and geometry.
4. After editing, verify edges still resolve (no dangling `source=` / `target=` references).

### Export to PNG / SVG / PDF

Reuse the generic drawio skill's CLI block. Quick recap:

```bash
# Windows / WSL2
"/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -e -b 10 \
    -o diagram.drawio.png diagram.drawio
```

Flags: `-x` export, `-f` format, `-e` embed XML in output, `-b 10` 10-px border, `-o` output path. Embedded XML means PNG/SVG/PDF can be re-opened in drawio for editing — keep that flag on.

When exporting for the user's IDP project, the convention is to drop the export under `electrical/exports/` mirroring the source filename (`remote-controller.drawio` → `remote-controller.png`).

## Common mistakes to avoid

- Using `rounded=1` on group containers (containers are sharp; only components are rounded).
- Mixing domain colors arbitrarily (e.g. green for both safety and battery in the same diagram).
- Forgetting `parent="1"` on a vertex / edge — it lands in the root layer and renders oddly.
- Self-closing `<mxCell ... edge="1"/>` without the geometry child — drawio renders it but won't display the arrow.
- Free-floating edges (no `source=` / `target=`) when both endpoints are vertices — anchored edges survive reflow, free edges don't.
- Using `&` literally inside `value="..."` — must be `&amp;`.
- Placing XML comments inside `<mxGraphModel>` — they break round-trips.
- Coordinates off the 10-px grid — visually fine but breaks alignment when extending the diagram later.
- Localized title text in English-Dutch mixed diagrams — keep titles in one language consistently.
- For flowcharts: coloring blocks by domain (don't — flowcharts stay monochrome).
- For block diagrams: forgetting the legend on a non-trivial diagram (always include it for diagrams with > 1 edge style).
- Forgetting the title block on a formal diagram (project / drawing / drawn-by / date / rev / sheet are required for printable / archivable engineering drawings).
- Placing the legend at the bottom-right (that's the title block's slot) — legend goes bottom-left.

## Detailed instructions (priority order)

1. **Read existing diagrams in the project before authoring** to inherit the established palette, sizes, and anchor conventions.
2. **Pick the diagram family** — block diagram vs flowchart — and apply the matching style guide. Don't blend.
3. **Lay out groups before components** for block diagrams; lay out the spine before branches for flowcharts.
4. **Generate the `.drawio` XML** following the file scaffold and style guide.
5. **Open the file in drawio** (or export) — on Windows the user's install lives at `C:\Program Files\draw.io\draw.io.exe`. From WSL use `/mnt/c/Program Files/draw.io/draw.io.exe`.
6. **For exports**, mirror the source filename and place under the project's `exports/` (or equivalent) directory.
7. **Surface any visual ambiguities** (colors, sizes, ordering) back to the user before bulk edits — don't silently restyle existing diagrams.

## Reference: cell style cheat sheet

```text
GROUP CONTAINER
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#<group-color>;strokeColor=#<group-stroke>;
  verticalAlign=top;fontStyle=1;fontSize=12

COMPONENT (inside group)
  rounded=1;whiteSpace=wrap;html=1;
  fillColor=#ffffff;strokeColor=#000000

BUS RAIL (full-width)
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12

TITLE (top of page)
  text;html=1;strokeColor=none;fillColor=none;
  align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;
  fontSize=18;fontStyle=1

LEGEND
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#f5f5f5;strokeColor=#666666;
  fontSize=10;align=left;verticalAlign=top

TITLE-BLOCK CELL (standard meta cell, 9 of these tile a 400×150 box)
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#ffffff;strokeColor=#000000;
  align=left;verticalAlign=top;
  fontSize=9;spacingLeft=4;spacingTop=2
  value: <b>Field</b><br>Value

TITLE-BLOCK DRAWING-TITLE CELL (single 400×30 row)
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#ffffff;strokeColor=#000000;
  align=left;verticalAlign=middle;
  fontSize=10;spacingLeft=4
  value: <b>Drawing</b>&nbsp;&nbsp;<title>

TITLE-BLOCK ORG CELL (centered school/company name)
  rounded=0;whiteSpace=wrap;html=1;
  fillColor=#ffffff;strokeColor=#000000;
  align=center;verticalAlign=middle;
  fontSize=9
  value: <b>NHL Stenden</b><br>Hogeschool

EDGE — solid signal / flow
  endArrow=classic;html=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  fontSize=10;

EDGE — dashed power supply
  endArrow=classic;html=1;dashed=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  fontSize=10;

EDGE — safety / e-stop
  endArrow=classic;html=1;
  strokeColor=#b85450;strokeWidth=2;
  fontSize=10;

FLOWCHART — terminator
  ellipse;whiteSpace=wrap;html=1;       (default size 120×60)

FLOWCHART — process
  rounded=0;whiteSpace=wrap;html=1;     (default size 120×50)

FLOWCHART — decision
  rhombus;whiteSpace=wrap;html=1;       (default size 91.75×90)

FLOWCHART — I/O parallelogram
  shape=parallelogram;perimeter=parallelogramPerimeter;
  whiteSpace=wrap;html=1;fixedSize=1;size=10  (default size 147.5×40)

FLOWCHART — branch edge with label
  edgeStyle=orthogonalEdgeStyle;html=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  value="Ja" or "Nee"
```
