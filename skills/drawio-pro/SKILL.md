---
name: drawio-pro
description: Use when generating, editing, or exporting draw.io diagrams (`.drawio`) - block diagrams, flowcharts, architecture diagrams, ER/sequence/class diagrams, network diagrams, mockups. Captures the user's personal diagram style: pastel grouped containers for block diagrams, standard BPMN-style shapes for flowcharts, orthogonal routing, light-grey legend boxes. Overrides the generic `drawio` skill - when both are available, prefer this one.
---

# drawio-pro skill

## Overview

Generate `.drawio` files in the user's standardized visual style. Three diagram families are explicitly supported, **each with its own look: do not blend them**:

- **Block / system diagrams** (pastel) - color-coded grouped containers, white component blocks inside, full-width bus rails, dashed power-distribution edges, legend bottom-left, title block bottom-right. Matches `electrical/diagrams/remote-controller.drawio`.
- **Flowcharts** (monochrome) - terminator ellipses for start/stop, plain rectangles for actions, rhombi for decisions, parallelograms for I/O, "Ja" / "Nee" labels on decision branches. Matches `Schoolwork/P2_Embedded2A/Uitwerkingen/Opdracht{2,3}/flowchart_opdr*.drawio`.
- **UML / software diagrams** (monochrome) - use-case, component, deployment, class, sequence. Built-in UML shapes (`umlActor`, use-case ellipses, component boxes, boundary rectangles), white fills, black strokes, dashed dependency arrows. Matches `Aardbei-Plukkers/software/diagrams/*.drawio`. See the "UML / software diagrams" section.

When this skill loads, **prefer the templates and palettes below over hand-rolling colors, edge styles, or shape choices**. Only fall back to free-form drawio when the user explicitly asks for a non-standard look.

The fallback / generic drawio skill (the public one shipped with most agent harnesses) has CLI lookup, post-processing, and export instructions. The **process** parts (locating the CLI, running export, opening the result) are still valid. This skill **adds** the user's visual style on top of that process.

## Before you save: mandatory self-check

After writing the `.drawio` file and **before** reporting it done, run these checks on the file. They catch the failures that recur most often:

1. **Em-dash scan.** Grep the saved file for the em-dash (U+2014) in every form: the literal character, plus the entities `&#8212;`, `&#x2014;`, and `&mdash;`. Models habitually slip one into the page title (the `Foo [U+2014] Bar` shape); all of these render the forbidden glyph. Replace every hit with a spaced hyphen ` - ` or a colon. Do not skip this even if you "know" you didn't add one.
2. **Edge endpoints resolve.** Every `source=`/`target=` on an edge names a real cell `id`. No dangling references.
3. **`parent="1"`** on every vertex and edge (except cells nested in a group, whose parent is the group id).
4. **Nested cell coordinates are RELATIVE to the parent group's coordinate system.** A child component with `parent="gPowerIn"` and `mxGeometry x="20" y="30"` renders 20 pixels right and 30 pixels down from the group's top-left corner - NOT 20/30 from the page origin. Writing absolute page coordinates on a nested cell puts the component way outside its group. **Quick mental check before saving:** for any cell with `parent="g..."` (i.e., parent is a group id, not `1`), its geometry `x` and `y` should be **smaller** than the parent group's `width` and `height`.
5. **Non-aligned block-diagram data edges carry `edgeStyle=orthogonalEdgeStyle`** (no accidental diagonals).
6. **Right family, right palette:** block = pastel; flowchart and UML = monochrome. No pastel on a UML or flowchart diagram.
7. **XML attribute well-formedness in `value="..."`.** Every `<` and `>` inside a `value="..."` attribute must be `&lt;` / `&gt;`. Inline HTML like `<b>`, `<br>`, `<i>`, `<font>` is the rendered form - in the XML it has to be `&lt;b&gt;`, `&lt;br&gt;`, `&lt;i&gt;`, `&lt;font&gt;`. drawio parses the entities and renders bold/break/italic, so the visible output is identical. **Skipping the escape silently drops every cell starting at the first unescaped `<`**, with no error. Working PowerShell check (this is the only pattern that distinguishes inside-the-value from outside-the-value, because entity-escaped `&lt;` does NOT contain a literal `<` character):

```powershell
# Any line matching `value="..."` containing a literal `<` means a cell uses unescaped HTML.
# Should return zero hits if every value uses &lt;...&gt; entities.
Select-String -Path <file> -Pattern 'value="[^"]*<'
```

## When to use

- User says: "draw a block diagram", "maak een blokschema", "flowchart", "stroomdiagram", "architecture diagram", "ER diagram", "sequence diagram", "class diagram", "wireframe", "mockup".
- User mentions: `draw.io`, `drawio`, `.drawio`.
- User asks to edit an existing `.drawio` file.
- User exports diagrams to PNG / SVG / PDF.

**Do NOT use for:** Mermaid (use raw markdown), PlantUML, ASCII art, Graphviz `dot` files. Those are separate formats with their own toolchains.

## File scaffold

Every `.drawio` file starts with this exact wrapper. The `host="65bd71144e"` value matches the user's drawio desktop install - keep it identical so files diff cleanly when round-tripped.

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
- Every `mxCell` has a unique `id`. Mix of named (`esp32`) and numeric (`23`) is fine - use named IDs for components you'll reference in edges, numeric for plain edges.
- All coordinates and sizes snap to the **10-pixel grid** (`gridSize="10"`).
- **Never** include XML comments inside `<mxGraphModel>` - drawio strips them silently and they can corrupt round-trip diffs.
- Multi-line labels: use `&#xa;` inside `value="..."`. Rich formatting: HTML inline (`<br>`, `<font>`, `<span style="...">`).
- **Inline HTML inside `value="..."` attributes must be entity-escaped.** Write `<b>` as `&lt;b&gt;`, `<br>` as `&lt;br&gt;`, `<font ...>` as `&lt;font ...&gt;`. drawio parses the entities and renders the same. An unescaped `<b>` inside `value="..."` is not valid XML - drawio silently drops the cell and every cell that follows. This is the single most common reason a freshly-written title block or rich-label cell vanishes on first export.
- Edges always carry `<mxGeometry relative="1" as="geometry"/>` as a child element (not self-closing).
- **No em-dashes (U+2014) anywhere in any label** (titles, title block, node text, edge labels) for any diagram family. This includes the entity-encoded forms `&#8212;`, `&#x2014;`, and `&mdash;`, which render as the same forbidden glyph. Use a spaced hyphen ` - ` or a colon `:` instead. This is the user's house style and applies even when no AGENTS.md is loaded in the working directory.

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

- `rounded=0` - sharp corners (containers, NOT components).
- `verticalAlign=top` - title sits in the header band.
- `fontStyle=1` - bold title (`fontStyle=2` italic for sub-labels).
- `fontSize=12` - container titles. Components default 12, sub-labels 10.
- Title text uppercase. `&amp;` for `&` literal.

### Color palette

| Domain / role | fillColor | strokeColor | Typical use |
|---|---|---|---|
| Power input / charge | `#fff2cc` | `#d6b656` | USB-C, charge IC, AC mains |
| Battery / safe | `#d5e8d4` | `#82b366` | Cell + BMS, "OK" path |
| MCU / radio / telemetry | `#e1d5e7` | `#9673a6` | MCU + radio + battery monitor (always use this row when a Battery group is also present; the two never share a color) |
| Regulation / display / cool | `#dae8fc` | `#6c8ebf` | Buck-boost, LCD, output |
| Safety / fault / rail / high-power | `#f8cecc` | `#b85450` | E-stop, alarm, power rail block, motor / high-current domain |
| HMI / I/O / warm | `#ffe6cc` | `#d79b00` | Buttons, joysticks, sensors |
| Legend / annotation | `#f5f5f5` | `#666666` | Legend box, footnote box |

Pick by **semantic role**, not aesthetics. The same color must mean the same thing across the diagram. Red (`#f8cecc`) carries a "danger / high energy" reading: use it for the safety/e-stop path **or** for a high-power motor / high-voltage domain (never both meanings in one diagram), and spell out which in the legend. The bus rail (see below) is conventionally red regardless of safety meaning - always add a legend line clarifying what the red rail represents in your specific diagram.

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

Power / data rails run as a single horizontal rectangle that **spans the consumer groups** (not necessarily the whole page - put it just above the row it serves, leave the supply group above free of the rail). They are **vertices** (not edges) so they can carry a label and be a connection target. Conventional color is red (`#f8cecc` / `#b85450`) regardless of whether the rail is safety-critical; add a legend line so the rail's role reads unambiguously.

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
| Pure horizontal / vertical hop (anchors share an x or y) | `edgeStyle=none;` |
| Anything else (down-and-across, diagonal would result) | `edgeStyle=orthogonalEdgeStyle;` (see MANDATORY rule below) |

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

### Separate power from data (anti-spaghetti rule)

The single biggest readability failure in block diagrams is power and data arrows piling onto the same edge of a block. Keep them on different sides:

- **Power drops (dashed, from the rail above)** enter each consumer through its **top** (`entryX=0.5;entryY=0`). Run them as straight vertical orthogonal lines, one short drop per consumer. Never route one dashed line diagonally across two groups to reach a far block; give that block its own vertical drop from the nearest point on the rail.
- **Data buses (solid, labeled)** connect the MCU to its peripherals. For sensor data (sensors→MCU), the arrow points **into** the MCU; for actuator signals (MCU→display, MCU→radio, MCU→driver), the arrow points **into** the peripheral. The arrow direction follows the actual data flow, not a default "MCU as origin". Either direction is fine as long as the arrows on a single diagram are consistent: if your SPI bus points MCU→LoRa, it must not point LoRa→MCU on a sibling edge. Enter peripherals through a **side** (`entryX=0;entryY=0.5` or `entryX=1;entryY=0.5`), never the top. This guarantees data and power never share an edge and stay visually distinct.
- Give every parallel bus its **own** `entryY` offset (e.g. `0.35`, `0.5`, `0.65`) so two buses into the same neighbourhood don't overlap into one thick line.

### Orthogonal routing is the block-diagram default (MANDATORY)

An edge with `exitX/entryX` anchors but **no** `edgeStyle` draws a single **diagonal** line straight between the two anchor points. Diagonal lines across a block diagram look like a wiring mistake and cross everything in their path. So:

> Every inter-block edge in a block diagram that is **not** a pure horizontal or pure vertical shot **MUST** carry `edgeStyle=orthogonalEdgeStyle`. No exceptions for "short" diagonals.

A pure horizontal hop (same `y`, e.g. component to its right neighbour) or pure vertical drop (same `x`, e.g. rail to consumer below) can stay `edgeStyle=none`. Everything else (MCU down-and-across to a peripheral, sensor on the right back to a central MCU, a bus to a block one row down) is orthogonal. Combine with the `entryY` offsets above so the right-angle stubs don't overlap. Add `<Array as="points">` waypoints only when the auto-orthogonal route still clips a block.

### MCU placement

Put the MCU at **one end** of the consumer row (or in its own row under the rail). All data buses then fan out in one direction - simplest to keep orthogonal. A central MCU with peripherals on both sides forces every data bus to cross the vertical power drops, and turns to spaghetti almost every time even with orthogonal routing. Don't do it.

**If the MCU group also contains a peripheral (LoRa radio, modem, etc.):** put that peripheral on the side of the MCU **away from** the rest of the diagram (i.e. on the outside of the row), not between the MCU and the external peripherals. Otherwise every data edge from external sensors to the MCU has to detour around the in-group peripheral, and labels collide with its box. Two equally good options:

- **MCU closest to the data sources**, peripheral on the outside (MCU right end of left group, radio left end of left group, sensors group on the right). Short, clean data edges from sensors to MCU.
- **Split the peripheral into its own group** (e.g. dedicated `RADIO` group with its own pastel container). Cleanest when the peripheral is a significant component with its own data edges in and out.

A peripheral that takes power but no data (passive sensor: anemometer, rain gauge, tipping bucket) gets only the dashed drop. Note this in the legend so the missing data edge reads as intentional. A passive RF output (antenna) takes neither power nor data - no edge to it.

### Legend box

Bottom-left of the page (the bottom-right corner is reserved for the title block - see next section), light grey, left-aligned text:

```xml
<mxCell id="legend"
        value="Legend:&#xa;- solid arrow = signal / power flow&#xa;- dashed arrow = 3.3 V supply distribution&#xa;- red = safety (e-stop) / battery monitor&#xa;&#xa;Reference designators are placeholders. To be assigned in schematic."
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;align=left;verticalAlign=top"
        parent="1" vertex="1">
    <mxGeometry x="40" y="830" width="320" height="100" as="geometry"/>
</mxCell>
```

Keep it small (~240–320 × 100). Always include it on a non-trivial block diagram.

### Page title (top header)

A full-width plain text cell at the top, bold 18pt, centered:

```xml
<mxCell id="title" value="Handheld Remote Controller - Block Diagram (rev A)"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1"
        parent="1" vertex="1">
    <mxGeometry x="40" y="10" width="1320" height="30" as="geometry"/>
</mxCell>
```

Use a spaced hyphen ` - ` (never an em-dash, U+2014) to separate scope and revision marker. The user's no-em-dash rule applies to generated diagram text as well as prose, so a hyphen or colon is the house style everywhere. Keep titles in English even when labels are Dutch: keeps the diagram skim-friendly across disciplines.

### Title block (engineering metadata, bottom-right)

ASME-style title block in the bottom-right corner. **Always include** on every formal block diagram - it identifies project, owner, revision, sheet number for printed/exported drawings.

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

Cell style - same on every cell:

```text
rounded=0;whiteSpace=wrap;html=1;
fillColor=#ffffff;strokeColor=#000000;
align=left;verticalAlign=top;
fontSize=9;spacingLeft=4;spacingTop=2
```

Exception - `tbTitle` (drawing-title row) uses `align=left;verticalAlign=middle;fontSize=10` so the longer drawing title sits centered vertically in its 30 px row.

Exception - `tbOrg` (school/company cell) uses `align=center;verticalAlign=middle` for a centered logo-style organization name.

Cell value HTML pattern: bold field label on first line via `<b>...</b>`, value on the next line via `<br>`. **In the actual XML these angle brackets are entity-escaped** (`&lt;b&gt;`, `&lt;br&gt;`) - see "Universal hard rules" above. The rendered form below is what the user sees; the literal XML in `value="..."` looks like the right column:

| Rendered (what the user sees) | Literal XML (what you write) |
|---|---|
| `<b>Drawn by</b><br>R. van der Veen` | `&lt;b&gt;Drawn by&lt;/b&gt;&lt;br&gt;R. van der Veen` |
| `<b>Date</b><br>2026-04-26` | `&lt;b&gt;Date&lt;/b&gt;&lt;br&gt;2026-04-26` |
| `<b>Rev</b><br>A` | `&lt;b&gt;Rev&lt;/b&gt;&lt;br&gt;A` |

For the drawing-title cell, label and value go on the same line (the row is shorter):

```xml
value="&lt;b&gt;Drawing&lt;/b&gt;&nbsp;&nbsp;Handheld Remote Controller - Block Diagram"
```

Optional: an outer 1.5 px border `mxCell id="tbBox"` around the whole 400×150 footprint as a single rectangle behind the cells, for a slightly thicker outer frame:

```xml
<mxCell id="tbBox" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1.5"
        parent="1" vertex="1">
    <mxGeometry x="980" y="830" width="400" height="150" as="geometry"/>
</mxCell>
```

When the page is **smaller** than 1400 × 1000, scale the title block proportionally - keep it at the bottom-right with a 20 px margin, but you can shrink to 320 × 120 on a 1000-wide page. **Don't** make it wider than 30 % of the page width.

When the page is **portrait** (flowcharts), the title block goes at the bottom-right too, but the drawing-title row may need to wrap to two lines - use `verticalAlign=top` and bump the row to 40 px.

### Layout discipline

1. **Top row**: input → primary processing → output, left to right.
2. **Bus rail**: horizontal across the diagram, between the top row and the consumers.
3. **Consumer row**: HMI / sensors / display below the bus rail.
4. **MCU position**: at one end of the consumer row or in its own row under the rail, so data buses fan out one direction (see "MCU placement drives bus cleanliness"). Not in the middle with peripherals on both sides.
5. **Aux blocks** (battery monitor, programming header): in margins, with their own pastel container.
6. **Legend**: bottom-left.
7. **Title block**: bottom-right (engineering metadata - always present).
8. **Spacing**: minimum 20 px between containers; align top edges within a row.

When 4–5 groups don't fit horizontally, drop the consumer row to the second tier and let the bus rail span the page width.

## Flowchart style

### Page setup

Portrait. Single column at one fixed x (e.g. `x=120` or `x=240`). Multiple independent functions go side-by-side at distinct columns (e.g. `x=120`, `x=500`, `x=1000`) - same flowchart file, different start/stop ellipses per function.

### Shape catalog

| Role | Shape | Style fragment | Default size |
|---|---|---|---|
| Start / Stop terminator | Ellipse | `ellipse;whiteSpace=wrap;html=1;` | 120×60 |
| Process / Action | Plain rectangle | `rounded=0;whiteSpace=wrap;html=1;` | 120×50 |
| Decision | Rhombus | `rhombus;whiteSpace=wrap;html=1;` | 90×90 (or 130×100 for long predicates - both snap to the 10-px grid) |
| Input / Output | Parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=10` | 150×40 |

**No fill colors.** Flowcharts use the drawio theme default (transparent / white), no per-domain palette. Color only when a single block needs to stand out (e.g. an error path).

### Edge conventions

| Meaning | Style |
|---|---|
| Direct vertical / horizontal hop between stacked blocks | `edgeStyle=none;` |
| Branch from a decision / orthogonal route around blocks | `edgeStyle=orthogonalEdgeStyle;` |
| Loop-back to a prior block | `edgeStyle=none;` with `<Array as="points">` waypoints |

Decision branches **must be labeled**. The organising principle is **the happy / normal path goes straight down the spine; the exceptional path (error, early return, loop exit) branches to the side**. Which label that puts on which arrow depends on the predicate:

- For a "keep going?" predicate (`i < 5 ?`), Ja continues the loop downward and Nee exits to the side. **Down = Ja.**
- For an error-check predicate (`meting < 0 ?`, `fout?`), the normal path is the *false* one, so **Nee goes down** the spine and **Ja branches to the side** into the error / early-return path. Do not force `Ja` downward here: that would route the error path through the main flow and read wrong.
- Always label each branch with its true `Ja` / `Nee` value for the predicate as written. Never relabel to fit the layout: rephrase the predicate instead if you want Ja to go down.

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
2. **Column alignment**: every block at the same x within a function. Decision rhombi off-center horizontally to balance their wider footprint - keep their **center** on the column.
3. **Multiple functions**: keep their start/stop pairs aligned horizontally so readers can compare entry/exit at a glance.
4. **Loop-back lanes**: route on the outside of the column (left for one decision, right for another) to avoid crossings.

### Language

Body text in **Dutch** for school flowcharts (`Start (main)`, `Roep X aan`, `Bereken Y`, `Toon Z`, `Stop (return 0)`). Predicate inside rhombus uses C-like syntax (`i &lt; 5`, `base &lt; 90000`) - escape `<` and `>` in XML.

### Page title and title block (optional for flowcharts)

A formal block-diagram-style title block is **not required** for an informal flowchart. If the flowchart is for an archivable school or engineering sheet, add the same bottom-right title block as a block diagram (Drawn by / Date / Rev / Sheet) and a centered top page title; otherwise omit both. The legend is also flowchart-typical: keep the predicate truth table and any non-obvious abbreviations near the bottom-left.

## UML / software diagrams (use-case, component, deployment, class, sequence)

These are a **third family**, distinct from block diagrams and flowcharts. The user's existing UML diagrams (`Aardbei-Plukkers/software/diagrams/`) establish the conventions. **Do NOT apply the pastel block-diagram palette here.**

**Core look: monochrome.**

- Shapes are **white or no fill** (`fillColor=#FFFFFF` or `fillColor=none`) with **black** strokes (`strokeColor=#000000`). Colour is the exception, used sparingly to group, never per-domain pastel.
- Font is **Helvetica**, larger than block diagrams: node text 12-14, use-case / actor labels ~20, page title ~24.
- The user's files wrap colours as `light-dark(#000000,#000000)` for theme-awareness; plain `#000000` / `#FFFFFF` is fine and simpler. Match the file you are editing.

**Use proper UML shape primitives** (drawio has them built in):

| Element | Style fragment |
|---|---|
| Actor | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` (label sits below) |
| Use case | `ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=3;` |
| Component / node box | `whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;` (170x80 typical), with a bold name + a small 10px description line inside |
| System / device boundary | a large rectangle, `fillColor=none;strokeColor=#000000;` (rounded for a device node, sharp for a logical boundary), label top-left, drawn **first** so it sits behind its contents |
| Class | `shape=class` or a rectangle split into name / attributes / methods compartments |

**Edge conventions for UML:**

- **Association** (actor to use case, plain relationship): solid line, **no** arrowhead (`endArrow=none;`).
- **Dependency / data flow / `<<include>>` / `<<extend>>`**: **dashed** line with an open or classic arrow (`dashed=1;endArrow=classic;` or `endArrow=open;`). The user's component diagrams use dashed classic-arrow connectors for flow between components.
- **Generalization / inheritance**: solid line, hollow triangle (`endArrow=block;endFill=0;`).
- Route with `edgeStyle=orthogonalEdgeStyle` when endpoints are not aligned (same MANDATORY rule as block diagrams).
- Stereotype / relationship labels go in the edge `value` (`<<include>>`, `Start AI`, multiplicities like `1..*`).

**Layout:** actors on the outside (left/right margins), use cases inside the system boundary. For component / deployment diagrams, group sub-components inside their device's boundary rectangle. Keep nodes on the 10-px grid like everything else. No legend or title block required for informal UML (a large plain-text page title is enough), but add them if the user wants a formal/archivable sheet.

Page title uses a **spaced hyphen**, never an em-dash: `value="Parking Garage System - Use-Case Diagram"` (fontSize ~20-24, `fontStyle=1`, `fontFamily=Helvetica`).

## Workflows

### Creating a new block diagram

1. Decide page size (default 1400×1000 landscape).
2. Lay out the **groups** first, on a sheet of paper or mentally - assign each its color from the palette above.
3. Write the file: title → groups (in reading order) → components inside each group → bus rails → edges → legend.
4. **Components inside groups use coordinates RELATIVE to the group's top-left corner** (e.g. an `USB-C` chip in a group at page `(120, 180)` of size `240×180` lives at group-relative `(20, 30)`, NOT absolute `(140, 210)`). Components nested in a group have `parent="g<group-id>"`. Components NOT in any group, plus edges and bus rails, have `parent="1"` and absolute coords. Forgetting this puts every nested component far outside its group on render. See hard rule #4.
5. Add domain-specific edges (data flow, supply distribution).
6. Sanity-check edge anchors: every edge with `source=` / `target=` should still resolve if you move the endpoints.
7. Run optional `npx @drawio/postprocess <file>` if available - it tightens edge routing.
8. Open in drawio (CLI export to PNG/PDF if requested - see generic skill for command).

### Creating a new flowchart

1. Pick portrait page (700×1100 default).
2. Sketch the function on paper, identifying terminators, processes, decisions, I/O.
3. Place the start ellipse at `(120, 40)` (or your column origin); flow downward at 90 px pitch.
4. Decisions: rhombus with `Ja` going down, `Nee` going to the side.
5. Loops: orthogonal route around the outside back to the decision.
6. Multiple functions: repeat at offset x columns (`+380`, `+760` typical).

### Editing an existing diagram

1. Read the file to identify scope and existing IDs.
2. Match the existing style - don't introduce new colors or shape conventions.
3. When adding a new component, copy an adjacent component's `style` string verbatim, then change `value` and geometry.
4. After editing, verify edges still resolve (no dangling `source=` / `target=` references).

### Export to PNG / SVG / PDF

Reuse the generic drawio skill's CLI block. Quick recap:

```bash
# Windows / WSL2
"/mnt/c/Program Files/draw.io/draw.io.exe" -x -f png -e -b 10 \
    -o diagram.drawio.png diagram.drawio
```

Flags: `-x` export, `-f` format, `-e` embed XML in output, `-b 10` 10-px border, `-o` output path. Embedded XML means PNG/SVG/PDF can be re-opened in drawio for editing - keep that flag on.

When exporting for the user's IDP project, the convention is to drop the export under `electrical/exports/` mirroring the source filename (`remote-controller.drawio` → `remote-controller.png`).

## Common mistakes to avoid

- Using `rounded=1` on group containers (containers are sharp; only components are rounded).
- Mixing domain colors arbitrarily (e.g. green for both safety and battery in the same diagram).
- Writing inline HTML (`<b>`, `<br>`, `<font>`) **unescaped** in a `value="..."` attribute - the XML parser hits the first `<` and silently drops every cell from there on. Always `&lt;b&gt;`, `&lt;br&gt;`, `&lt;font ...&gt;`. See "Universal hard rules" and self-check #6.
- Forgetting `parent="1"` on a vertex / edge - it lands in the root layer and renders oddly.
- Writing **page-absolute** coordinates on a child cell with `parent="g..."` (a group). Nested cell geometry is relative to the parent group's top-left, so `x="140"` inside a group at `(120, 180)` puts the child at page-coordinate `(260, ...)` - way outside the group. See hard rule #4 and self-check #6.
- Self-closing `<mxCell ... edge="1"/>` without the geometry child - drawio renders it but won't display the arrow.
- Free-floating edges (no `source=` / `target=`) when both endpoints are vertices - anchored edges survive reflow, free edges don't.
- Using `&` literally inside `value="..."` - must be `&amp;`.
- Placing XML comments inside `<mxGraphModel>` - they break round-trips.
- Coordinates off the 10-px grid - visually fine but breaks alignment when extending the diagram later.
- Localized title text in English-Dutch mixed diagrams - keep titles in one language consistently.
- For flowcharts: coloring blocks by domain (don't - flowcharts stay monochrome).
- For block diagrams: forgetting the legend on a non-trivial diagram (always include it for diagrams with > 1 edge style).
- Forgetting the title block on a formal diagram (project / drawing / drawn-by / date / rev / sheet are required for printable / archivable engineering drawings).
- Placing the legend at the bottom-right (that's the title block's slot) - legend goes bottom-left.
- Power (dashed) and data (solid) arrows entering a block on the **same edge** - keep power on the top, data on a side, so the two never merge into one line.
- A central MCU with peripherals on both sides, forcing every data bus to cross the vertical power drops - put the MCU at one end or in its own row.
- One dashed power line routed diagonally across two groups to a far block - give the far block its own vertical drop from the nearest point on the rail.
- Em-dashes (U+2014) anywhere in diagram text (titles, title block, labels) - use a spaced hyphen ` - ` or a colon.

## Detailed instructions (priority order)

1. **Read existing diagrams in the project before authoring** to inherit the established palette, sizes, and anchor conventions.
2. **Pick the diagram family** - block diagram vs flowchart - and apply the matching style guide. Don't blend.
3. **Lay out groups before components** for block diagrams; lay out the spine before branches for flowcharts.
4. **Generate the `.drawio` XML** following the file scaffold and style guide.
5. **Open the file in drawio** (or export) - on Windows the user's install lives at `C:\Program Files\draw.io\draw.io.exe`. From WSL use `/mnt/c/Program Files/draw.io/draw.io.exe`.
6. **For exports**, mirror the source filename and place under the project's `exports/` (or equivalent) directory.
7. **Surface any visual ambiguities** (colors, sizes, ordering) back to the user before bulk edits - don't silently restyle existing diagrams.

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

EDGE - solid signal / flow (pure horizontal or vertical hop)
  endArrow=classic;html=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  fontSize=10;

EDGE - data bus, down-and-across (DEFAULT for non-aligned data edges)
  edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  fontSize=10;     value="I2C" / "SPI" / "PWM" etc.

EDGE - dashed power supply
  endArrow=classic;html=1;dashed=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  fontSize=10;

EDGE - safety / e-stop
  endArrow=classic;html=1;
  strokeColor=#b85450;strokeWidth=2;
  fontSize=10;

FLOWCHART - terminator
  ellipse;whiteSpace=wrap;html=1;       (default size 120×60)

FLOWCHART - process
  rounded=0;whiteSpace=wrap;html=1;     (default size 120×50)

FLOWCHART - decision
  rhombus;whiteSpace=wrap;html=1;       (default size 90×90, snaps to 10-px grid)

FLOWCHART - I/O parallelogram
  shape=parallelogram;perimeter=parallelogramPerimeter;
  whiteSpace=wrap;html=1;fixedSize=1;size=10  (default size 150×40, snaps to 10-px grid)

FLOWCHART - branch edge with label
  edgeStyle=orthogonalEdgeStyle;html=1;
  exitX=<n>;exitY=<n>;entryX=<n>;entryY=<n>;
  value="Ja" or "Nee"
```
