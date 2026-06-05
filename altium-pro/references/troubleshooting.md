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

<!-- Add new sections below this line -->
