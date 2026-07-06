---
name: altium-pro
description: Use when working in Altium Designer - PCB layout, schematic capture, rooms, queries, design rules, polygon pours, output jobs, or when hitting an Altium quirk/error/unexpected behavior. Captures the user's personal Altium troubleshooting notes, proven flows, and query snippets so they are not re-derived each time. Detailed human-readable log lives in references/troubleshooting.md.
---

# altium-pro skill

## Overview

Personal knowledge base for Altium Designer. Two jobs:

1. **Proven flows** - step-by-step recipes the user has confirmed work (rooms, queries, rule scoping, etc.).
2. **Troubleshooting log** - issues hit + their fix, so the same wall is not hit twice.

The full human-readable record is **references/troubleshooting.md**. This SKILL.md is the index: scan it, then open the reference for detail. When the user describes a new issue or a new flow, **append it to references/troubleshooting.md** (see "Adding an entry" below).

Hotkeys live separately in **references/hotkeys.md** - add keyboard shortcuts there, not in the troubleshooting log.

## When to use

- User mentions: Altium, Altium Designer, PCB, schematic, room, query, design rule, polygon pour, gerber, output job, BOM (from Altium), footprint, `.PcbDoc`, `.SchDoc`, `.PrjPcb`.
- User hits an Altium error, quirk, or "why does Altium do X" question.
- User wants to document a flow or issue they just solved ("remember this Altium flow", "document this").

**Do NOT use for:** KiCad, Eagle, generic EDA theory unrelated to Altium's tooling.

## Index of documented flows & issues

| Topic | Type | Where |
|---|---|---|
| Rooms - confine + move all components together | Flow | references/troubleshooting.md → "Rooms" |
| Rooms disappear on Update PCB / Import Changes | Issue | references/troubleshooting.md → "Rooms disappear" |
| PGND vs GND split on switching converters | Design note | references/troubleshooting.md → "PGND vs GND split" |
| Polygon pours - place, net, edit, settings | Flow | references/troubleshooting.md → "Polygon pours" |
| Find Similar Objects - bulk-select + bulk-edit | Flow | references/troubleshooting.md → "Find Similar Objects" |
| Pour won't flood over same-net trace/pad | Issue | references/troubleshooting.md → "Pour won't flood over" |
| Polygon pours -- shelve and restore (hide fills) | Flow | references/troubleshooting.md → "Polygon pours -- shelve and restore" |
| Resize / redefine the board shape | Flow | references/troubleshooting.md → "Resize / redefine the board shape" |
| Laser-cut solder paste stencil - Gerber X2 layer selection | Flow | references/troubleshooting.md → "Laser-cut solder paste stencil" |
| Pick and Place (PnP) output - Tronstol E1 | Flow | references/troubleshooting.md → "Pick and Place (PnP) output" |
| Polygon pour that fits an irregular board outline (Tools > Convert flow) | Flow | references/troubleshooting.md → "Polygon pour that fits an irregular board outline" |

> Keep this table in sync with references/troubleshooting.md. One row per documented flow/issue.

## Quick reference - query snippets

| Goal | Query |
|---|---|
| Room owns everything physically inside it | `WithinRoom('<RoomName>')` |
| Scope by a component class (stable across moves) | `InComponentClass('<ClassName>')` |
| Single component by designator | `Name = 'U1'` |
| Combine | `InComponentClass('BMS') Or (Name = 'U1')` |

`WithinRoom` is **positional** - re-evaluates on where parts currently sit. For a membership that survives moves, scope to a **component class** instead.

## Rooms - confine all components and move them together

Confirmed flow:

1. `Design > Rooms > Place Rectangular Room` - drop the room on the board.
2. Double-click the room → **Edit Room Definition**.
3. **Where The Object Matches** → set dropdown to **Custom Query** → enter `WithinRoom('<RoomName>')` (e.g. `WithinRoom('BMS')`).
4. Tick **Components Locked** (and optionally **Room Locked**) so the grouped parts move as a unit and resist accidental drag.
5. Bottom-left layer dropdown → target layer (e.g. `Top Layer`); keep the constraint dropdown on **Keep Objects Inside**.
6. **Test Queries** → confirm the expected component count matches before OK.

Default empty query is `False` → matches nothing → room moves alone. That is the usual "my room is empty / components don't follow" cause.

## Adding an entry

When a new flow or fix is confirmed:

1. Open **references/troubleshooting.md**.
2. Add a `## <Topic>` section using the template at the top of that file (Symptom → Cause → Fix → Notes, or Flow → Steps).
3. Add one row to the **Index** table above.
4. Only document what was **confirmed working** - not guesses. Mark anything unverified explicitly as `UNVERIFIED`.
