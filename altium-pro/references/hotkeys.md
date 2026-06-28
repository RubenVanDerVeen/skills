# Altium Designer - Hotkeys

Personal list of confirmed-useful Altium shortcuts. Add to it as you learn them.
Only list keys you've actually used or confirmed against official docs.

Sources: official Altium docs - [PCB editor shortcuts](https://www.altium.com/documentation/altium-designer/shortcut-keys/pcb-editors),
[Schematic editor shortcuts](https://www.altium.com/documentation/altium-designer/shortcut-keys/schematic-editors).

## How to add

One row per shortcut. Group under the right `##` editor heading (PCB / Schematic / Global).
Note if it opens a menu vs fires an action directly. `+`/`-`/`*` = numeric keypad keys.

## Global / both editors

| Key | Action | Notes |
|---|---|---|
| `Spacebar` | Rotate object 90° CCW (during placement/move) | `Shift+Spacebar` = clockwise. |
| `G` | Cycle snap grid | `Shift+G` = cycle backward. |
| `Alt` (while moving) | Constrain move to horizontal/vertical | Start the move first, then hold Alt. |
| `Ctrl+arrow` | Nudge selection by one grid step | Add `Shift` for 10× grid step. |
| `Ctrl+A` | Select all | |
| `X` / `Y` | Mirror object along X / Y axis (during placement) | |

## PCB editor

### View

| Key | Action | Notes |
|---|---|---|
| `1` | Board Planning mode | |
| `2` | 2D Layout mode | |
| `3` | 3D Layout mode | |
| `Ctrl+Alt+2` / `Ctrl+Alt+3` | Switch 2D / 3D keeping view position | |
| `Ctrl+F` | Flip board (view from the back) | Like turning the board over in your hand. |
| `Ctrl+PgDn` | Fit / display all design objects | |
| `L` | View Configuration (layers & colors) | Where connection-line color/visibility lives. |

### Layers

| Key | Action | Notes |
|---|---|---|
| `+` / `-` | Next / previous enabled layer | Numeric keypad. |
| `*` | Next signal layer | `Shift+*` = previous signal layer. |

### Routing & connections

| Key | Action | Notes |
|---|---|---|
| `Ctrl+W` | Start interactive routing | |
| `N` | Show/Hide Connections menu | `Show Connections` → `All` reveals all ratsnest lines. Fix for "can't see unrouted connection lines". |
| `*` (while routing) | Drop via + switch to next signal layer | Numeric keypad. |
| `2` (while routing) | Add via without changing layer | |
| `Shift+W` | Pick track width from favorites | |
| `Shift+V` | Pick via size from favorites | |
| `Ctrl+H` | Select whole connected net (same copper) | |
| `Ctrl+Click` on net | Highlight entire routed net | |

### Edit / inspect

| Key | Action | Notes |
|---|---|---|
| `Ctrl+M` | Measure distance between two points | |
| `Ctrl+B` | Select objects within board boundary | |
| `Shift+C` | Clear current filter / mask | Un-dims the board after Find Similar Objects or a PCB-panel filter. |

## Schematic editor

| Key | Action | Notes |
|---|---|---|
| `P`, `W` | Place wire | Press P then W. |
| `Spacebar` (placing wire) | Toggle wire start/end mode | |
| `Ctrl+Spacebar` (dragging) | Rotate 90° CCW while dragging | |

> Re-entrant editing: you can press a shortcut (e.g. `Spacebar` to rotate) mid-placement
> without quitting the current command.
