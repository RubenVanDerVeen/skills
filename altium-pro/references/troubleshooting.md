# Altium Designer — Troubleshooting & Flows

Personal log of Altium issues hit and flows that work. Human-readable. Add to it whenever
you solve something or work out a reliable flow.

## How to add an entry

Copy one of the templates below into a new `##` section. Keep the most-used stuff near the top.
Only write down what you **confirmed works**. Tag anything you're unsure about as `UNVERIFIED`.

**Issue template**

```
## <Short title>

- **Symptom:** what you saw / the error text
- **Cause:** why it happens
- **Fix:** the steps that resolved it
- **Notes:** gotchas, related settings, version if relevant
```

**Flow template**

```
## <Short title>

Goal: <what this achieves>

1. step
2. step
3. step

Notes: <gotchas>
```

---

## Rooms — confine all components and move them together

Goal: a room that owns every component placed inside it, so they all move with the room and
stay confined to it.

1. `Design > Rooms > Place Rectangular Room` — draw the room on the board.
2. Double-click the room to open **Edit Room Definition**.
3. **Where The Object Matches** → switch the dropdown to **Custom Query**.
4. Enter the query: `WithinRoom('<RoomName>')` — e.g. `WithinRoom('BMS')`.
5. Tick **Components Locked** (optionally **Room Locked** too) so the group moves as one and
   doesn't get dragged apart by accident.
6. Bottom-left: pick the layer (e.g. `Top Layer`) and keep the constraint dropdown on
   **Keep Objects Inside**.
7. Click **Test Queries** to confirm the right number of components match, then OK.

Notes:

- The default query is `False`, which matches **nothing** — that's why a fresh room looks empty
  and components don't follow it. Always replace `False`.
- `WithinRoom(...)` is **positional**: it matches whatever currently sits inside the room
  outline. Move a part out and it's no longer a member.
- For membership that survives moves (parts grouped logically, not by position), scope the room
  to a **component class** instead: create a class in the PCB panel, add the parts, then use
  `InComponentClass('<ClassName>')` as the query.

### Query cheatsheet

| Goal | Query |
|---|---|
| Everything physically inside the room | `WithinRoom('<RoomName>')` |
| A logical group (survives moves) | `InComponentClass('<ClassName>')` |
| One part by designator | `Name = 'U1'` |
| Combine several | `InComponentClass('BMS') Or (Name = 'U1') Or (Name = 'C2')` |

---

## Rooms disappear on Update PCB / Import Changes

- **Symptom:** Rooms vanish every time you update the PCB from schematic or import changes
  into the layout. You re-place them, they get wiped again on the next sync.
- **Cause:** The ECO (Engineering Change Order) generation defaults to issuing "Change Rooms"
  and "Remove Rooms" change orders, so each sync removes/overwrites manually-placed rooms.
- **Fix:** `Project > Project Options > ECO Generation`. Find **Change Rooms** and
  **Remove Rooms** in the list, set both to **Ignore Differences**, OK.
- **Notes:** This makes rooms purely a layout concern that the schematic sync leaves alone —
  exactly what you want for manually defined rooms. Leave the other room-related ECO rows
  (e.g. Add Rooms) as-is unless you hit a related problem.

## PGND vs GND split (switching converters, e.g. TPS63020)

> Design knowledge, not an Altium-tool quirk — general rule of thumb for split-ground
> switchers. Always confirm pin assignment against the part datasheet.

Goal: decide which nets go to **PGND** (power ground) vs **GND** (signal/analog ground) on a
switching converter that exposes both.

- **PGND** = high-current switching return. Carries inductor ripple. Noisy.
- **GND** = quiet analog reference for feedback + control.

Assignment:

| Net / component | Ground | Why |
|---|---|---|
| Device PGND pin | PGND | power return |
| Bulk output caps (VOUT) | PGND | carry switching ripple |
| Bulk input caps (VIN) | PGND | carry input switching ripple |
| Device GND pin | GND | analog reference |
| FB divider bottom resistor | **GND** | divider noise → output error; most critical |
| Analog-supply decoupling (e.g. VINA 100nF) | GND | quiet reference |
| EN / control pin returns | GND | quiet reference |

Rules:

1. FB divider bottom leg always on **GND**, never PGND.
2. VIN + VOUT bulk caps on **PGND** (their ripple return path).
3. Tie GND ↔ PGND at **one star point** under the IC thermal pad. Don't merge them as a
   blind plane fill.

Worked example (TPS63020 buck/boost): C8–C11 (VOUT) → PGND; C6,C7 (VIN) → PGND; R16 (FB
bottom) → GND; C12 (VINA 100nF) → GND; pin 2 → GND, pin 15 → PGND.

## Polygon pours — place, net, edit, and settings

Goal: place a copper polygon pour, tie it to a net, and get clean repour behavior.

Place + assign:

1. Top toolbar component/place selector → **Polygon Pour**. Draw a rough outline to size it.
2. After sizing, open **Properties** → set **Net** to the net it should connect to (e.g. GND).
3. To add vertices to an existing polygon, hold **CTRL** and drag one of its edges — this
   inserts a new point you can reshape.

Settings to set once:

- **Connection style:** `Design > Rules > Plane > Polygon Connect Style` → set to
  **Direct Connect** for a more uniform connection across multiple pins (vs thermal relief
  spokes).
- **Auto repour:** Altium-wide `Preferences > PCB Editor > General > Polygon Rebuild` →
  enable **Repour Polygons After Modification** so the pour rebuilds/updates automatically
  after you move or edit it.

Notes:

- Direct Connect floods solid copper to pads — good for ground/power planes; trades away the
  thermal-relief soldering benefit, so weigh it for hand-soldered boards.
- Without auto-repour, edits leave the pour stale until you manually `Tools > Polygon Pours >
  Repour`.

## Find Similar Objects — bulk-select + bulk-edit (e.g. resize all vias)

Goal: select every object of one kind (all vias, all tracks on a layer, all pads of a net…)
and change a property on all of them at once.

1. Right-click any object of the target kind → **Find Similar Objects**.
2. In the dialog, set the matching field to **Same** and leave the rest **Any**. For "all
   vias": set **Object Kind = Via → Same**.
3. (Optional) tick **Select Matching** / **Open Properties** so the matches get selected and
   the panel opens. OK.
4. The **Properties / PCB Inspector** panel now edits all selected at once — change e.g. via
   **Diameter** + **Hole Size** once → applies to every selected via.
5. Clear the filter afterwards with **`Shift+C`** (or click empty space) so the board isn't
   left masked/dimmed.

Notes:

- Also reachable via the **PCB panel** (bottom-right `PCB` tab) for filter-based multi-select,
  or a query like `IsVia` in the filter bar.
- If the objects are governed by a **design rule** (e.g. `Design > Rules > Routing > Routing
  Via Style`), prefer fixing the rule — a manual resize can be overridden on the next
  interactive route/repour.

## Pour won't flood over / connect to a same-net trace or pad

- **Symptom:** A polygon pour leaves a black clearance ring (gap) around a trace/pad that's on
  the **same net**, so they don't bond. Ratsnest airwire stays unconnected.
- **Cause:** The pour's **"Pour Over..."** mode is set to *Don't Pour Over Same Net Objects*,
  so it keeps clearance even from its own net instead of flooding over and connecting.
- **Fix:**
  1. Double-click the pour → **Properties**.
  2. Set the **"Pour Over..."** dropdown to **Pour Over All Same Net Objects and Connect**
     (or *Pour Over All Same Net Objects*).
  3. Repour: `Tools > Polygon Pours > Repour Selected`. Gap closes, ratsnest clears.
- **Notes:**
  - First confirm the pour **Net** actually matches the trace (a wrong/blank net causes the
    same clearance gap for a different reason — fix net, repour).
  - Also check `Design > Rules > Plane > Polygon Connect Style` is Direct/Relief, not
    **No Connect**.
  - After changing the pour net, Altium keeps showing the **old** shape until you repour — a
    stale pour can masquerade as "not connecting".

## Polygon pours -- shelve and restore (hide fills for clarity)

Goal: temporarily hide polygon pours so they don't obscure routing, vias, and pads; restore
them when done.

Shelve (hide):

1. `Tools > Polygon Pours > Shelve N Polygon(s)` where N is the count of active pours.
2. All pours disappear -- the board shows only traces, pads, and vias.

Restore:

1. `Tools > Polygon Pours > Restore N Shelved Polygon(s)`.
2. Pours reappear; Altium does NOT automatically repour -- see note below.

Notes:

- Shelved pours are kept in memory until restored or the file is closed. They are not deleted.
- After restoring, run `Tools > Polygon Pours > Repour All` (or `Repour Modified`) if the
  board was edited while shelved -- otherwise the pour shape is stale.
- "Restore N Shelved Polygon(s)" is greyed out when no pours are shelved (N = 0), as shown
  in the menu.
- Shortcut path: the Polygon Pour submenu is also at `Right-click canvas > Polygon Pours` when
  no object is selected.

<!-- Add new sections below this line -->

## Resize / redefine the board shape

Goal: change the PCB outline. Method A is the fastest for plain rectangles, Method B is the
cleaner flow when the new shape is irregular or driven by primitives.

Method A, Redefine (rectangular, fastest):

1. `Design > Board Shape > Redefine Board Shape` -> click 4 new corners -> right-click to
   commit. Or numeric: `Design > Board Options...` -> set `Board Width` / `Board Height` and
   the origin.

Method B, Create primitives then push back (irregular edits):

1. `Design > Board Shape > Create Primitives From Board Shape` -> OK. Drops a track-based
   outline of the current board on a mech layer.
2. Edit the primitives: drag vertices/edges, add segments, or use `Place > Line` for a clean
   closed loop. A `Place > Rectangle` filled primitive also works here.
3. Select the new outline primitives.
4. `Design > Board Shape > Define Board Shape from Selected Objects` -> board shape updates.

Notes:

- Method B works because `Create Primitives` produces the right object kind (track segments
  that `Define from Selected Objects` accepts directly).
- A raw `Place > Rectangle` (filled primitive) without Method B can trigger "At least 2
  connected tracks/arcs or full circle required"; the "external edges" retry prompt usually
  does nothing useful. Stick to Method A, or draw the rectangle via `Place > Line` as a
  closed 4-segment loop.
- For shrinking a rectangle by a few mm, Method A is one click. Reach for Method B when the
  new shape is not a plain rectangle, or when you want to edit the outline vertex-by-vertex.

## Laser-cut solder paste stencil - Gerber X2 layer selection

Goal: export only the paste aperture layers (plus the board outline as a frame
reference) so the laser cutter software cuts the right holes.

1. `File > Fabrication Outputs > Gerber X2 Files`.
2. In the Gerber Options dialog tick **only** these:
   - **Board Outline** (e.g. `*_Profile.gbr`) - frame reference for the cutter software.
   - **Paste Mask** parent, then the side(s) you actually need:
     - `*_Paste_Top.gbr` for a top-side stencil.
     - `*_Paste_Bot.gbr` for a bottom-side stencil.
3. Unt everything else: Silkscreen, Solder Mask, Copper Layers, Mechanical
   Layers, Other Layers, Drills, Drill drawing, Drill guide.
4. Units: millimetres. Format: RS-274X (X2 default, no change needed).
5. Click **Plot Layers**. Import `*_Paste_Top.gbr` into the cutter software
   (JCZ EZCAD, LaserGRBL, OpenStudio, ...). The filled regions in the Gerber
   are the apertures to cut.

Notes:

- Don't tick **Solder Mask** by mistake. Solder mask is the green-lacquer
  opening, not the paste aperture. Different shape and size (stencil design
  rules vs mask expansion).
- The board outline is optional but convenient: most cutter software lets
  you frame the cut path to it, so the finished stencil blank matches the
  PCB outline.
- For a frame stencil where the cutout follows the PCB profile, also
  import `*_Profile.gbr` as the cut path; the Paste Gerber supplies the
  interior apertures only.

## Pick and Place (PnP) output - Tronstol E1

Goal: export component centroid data as a CSV the Tronstol E1 can load.

1. **Not** a Gerber output. Use `File > Assembly Outputs > Pick and Place`.
2. In the Pick and Place Setup dialog:
   - Units: **Millimeters** (the E1 works in mm).
   - Format: **CSV** (the E1 firmware expects CSV, not TXT).
3. Click OK. Altium writes one file per side: `PickPlace_Top.csv` and
   `PickPlace_Bottom.csv` (filenames follow the project name).
4. Open the CSV in Excel or a text editor. The E1 typically expects only
   these columns, in this order: `Designator, X, Y, Rotation, Side`.
   Altium's raw output also includes `Footprint, Ref X, Ref Y, Pad X,
   Pad Y, Layer, Comment` - delete the extras if the E1 import is strict.
5. Copy the file to the E1 controller/PC and load via its import dialog.

Notes:

- Don't try to extract PnP from the Gerber X2 dialog. Gerber is image
  data, not component coordinates. The Pick and Place generator is a
  separate menu item under Assembly Outputs.
- Bottom-side rotation: Altium may or may not mirror the rotation per
  layer. Run a dry cycle on one component (e.g. an SOIC on the bottom)
  before the first production run to confirm orientation is correct.
- Decimal separator: Altium writes `.` (dot). If the E1 PC locale is set
  to comma-decimal, re-save the CSV with `.` as decimal, or fix the
  locale on the import PC.
- Fiducials: the E1 uses board fiducials for alignment. Make sure the
  PCB fab places them; the E1 doesn't import them as part of the
  PnP file.

## Polygon pour that fits an irregular board outline (Tools > Convert flow)

> Confirmed working by user. Used when the polygon pour's "Boundary Mode =
> Use Board Outline" option is missing from Properties in their Altium
> version.

Goal: produce a polygon pour whose outline follows an irregular PCB outline
that exists as the board shape but has no primitives on a mechanical layer
yet (or needs the outline restated from the current board shape).

1. `Design > Board Shape > Create Primitives from Board Shape`. Altium
   drops the current board outline as track-based primitives on
   Mechanical 1.
2. Select those primitives.
3. `Tools > Convert > Create Polygon from Selected Primitives`. Altium
   creates a polygon pour on the active copper layer using the primitives
   as the outline.
4. Switch only the outline back to Mechanical 1. Leave the pour itself
   on the copper layer (the polygon's copper fill stays where step 3
   put it).
5. `Tools > Polygon Pours > Repour All` (or `Repour Selected`) to fill
   the new pour.

Notes:

- The board shape itself is unchanged by this flow. Step 1 just
  materialises the existing outline as primitives so they can be
  selected and converted.
- "Outline" = the polygon's boundary geometry (on Mechanical 1);
  "pour" = the copper fill (on the copper layer). This flow keeps
  them on separate layers by design.
- If `Tools > Convert > Create Polygon from Selected Primitives` is
  missing in your Altium version, fall back to the boundary-mode option
  in the pour Properties (see "Polygon pours" entry above) or to Method B
  in "Resize / redefine the board shape".
