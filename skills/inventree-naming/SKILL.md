---
name: inventree-naming
description: Use when naming, renaming, or writing descriptions for InvenTree parts: applying the dash-separated name convention (sentence case, × and ⌀), picking per-category name formats (screws, inserts, bearings, connectors, switches, dev boards, power modules, motors, displays, tools), or validating names during inventory work such as AliExpress CSV imports. Triggers: InvenTree, part name, naming convention, rename or redescribe part.
---

## Overview

The single source of truth for naming InvenTree parts. Ported from the Homelab `projectdock/inventree-naming-convention.md` doc (2026-08-19). Every part gets a dash-separated name that identifies it at a glance, and a description that gives the full picture.

## When to use

- Creating or renaming a part in InvenTree (any harness, not just the inventree agent).
- Writing or restructuring a part description.
- Naming parts during AliExpress CSV imports or bulk backfills.
- Reviewing existing part names for convention compliance.

## Name rules

All names follow `Section 1 - Section 2 - Section 3 ...`:

- Sentence case: capitalise the first word and proper nouns only.
- Use × (U+00D7) for dimensions, not x. Use ⌀ for diameter.
- Sections carry only what uniquely identifies the part at a glance; extra details (color variants, protection ratings, certifications, notes) go in the description.
- Omit sections that don't apply rather than writing N/A.
- One part = one variant. Red vs Black are separate parts.

## Description rules

Full picture in one or two flowing sentences (type → key specs → dimensions/ratings → material), then optional feature flags after a blank line. Every sentence and every feature flag ends with a period. Parts in the same category follow the same sentence structure.

```
[One or two sentences covering all specs, materials, and identifying details.]

[Feature flag 1].
[Feature flag 2].
```

Omit the feature-flag block when there is nothing extra. Typical flags: `Waterproof.`, `Latching.`, `PCB mount.`

## Quick reference

| Part type | Name format |
|---|---|
| Screw | `M[n]x[L] - [Head] screw - [Drive]` |
| Insert | `M[n] Insert - Length=[L]mm ⌀=[D]mm` |
| Bearing | `[PN] Ball Bearing ([B]×[OD]×[W]mm)` |
| Banana Jack | `Banana Jack [size] - [M/F] - [Color]` |
| XT Connector | `XT[n] Connector - [M/F]` |
| JST Connector | `JST [Series] [Pitch]mm - [nP] - [M/F]` |
| DC Barrel Jack | `DC Barrel Jack [OD]×[ID]mm - [M/F]` |
| Pin Header | `Pin Header [Pitch]mm - [nP] - [M/F]` |
| Switch | `[Type] - [Config] - [Voltage][/Amps]` |
| Dev Board | `Dev Board - [Controller Chip] - [USB]` |
| Buck/Boost | `[Chip -] [Type] - [Input] / [Rating]` |
| BMS | `[Chip -] [nS] BMS - [Current]` |
| Charger | `[Chip -] [nS] [Chem] Charger - [A] - [USB]` |
| Motor | `[Type] - [Model/Voltage] - [KV/RPM]` |
| Display | `[Type] Display - [Size] - [Bus] - [Driver] - [Resolution]` |
| Tool | `[Type] - [Brand] [Model]` |

## Worked examples

**Screw.** Name: `M4x10 - Cap head screw - Hex`. Description: `M4 cap head hex socket screw, 10mm length.`

**Switch with feature flags.** Name: `Push Button 16mm - 1NO 1NC - 12-24V`. Description:

```
Metal panel-mount push button, 16mm, 1NO 1NC contacts, rated 12–24V, black shell.

Waterproof.
Latching.
Illuminated (red LED).
```

## Per-category formats

Field-by-field tables and more name/description pairs for every category live in [`references/formats.md`](./references/formats.md). Check existing parts in the same category first and mirror their sentence structure.
