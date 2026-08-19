# InvenTree Naming Skill Implementation Plan

> **For agentic workers:** Execute via /execute-plan conventions: branch first, one executor per task, reviewer after each task, per-task Conventional Commits, oracle on two-strike failures, final report. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the Homelab InvenTree naming convention doc as the `inventree-naming` skill in this repo, catalogued and committed.

**Architecture:** Two new files under `skills/inventree-naming/` (lean SKILL.md body + full per-category detail in `references/formats.md`), ported verbatim from the Homelab projectdock doc with an em-dash scrub. Catalog rows and CHANGELOG land in the same feat commit. No agent files touched.

**Tech Stack:** Markdown only. No build step, no runtime.

**Spec:** `docs/artifacts/features/inventree-naming-skill/2026-08-19-inventree-naming-skill-design.md`

## Global Constraints

- Repo: `C:\Users\ruben\Projects\Tools\skills`, branch `main` at start. Work on `feat/inventree-naming-skill`; do NOT merge or push (user merges).
- No em-dashes (U+2014) in any file this plan creates or modifies. × (U+00D7), ⌀ (U+2300), en-dashes (U+2013) in numeric ranges are allowed and ported verbatim.
- `SKILL.md` frontmatter: `name` kebab-case matching the folder name; `description` starts with "Use when...", trigger-focused; total frontmatter under 1024 chars.
- Body starts with `## Overview` (never `## Skill`); lean body, detail lives in `references/`.
- Conventional Commits 1.0.0; the commit-msg hook (`.githooks/commit-msg`) is active in this clone.
- Port fidelity: content is ported from the source doc, not rewritten. Only transforms: em-dash scrub, plus fixing the one broken code fence noted in Task 1.

---

### Task 1: Create `skills/inventree-naming/` (SKILL.md + references/formats.md)

**Files:**
- Create: `skills/inventree-naming/SKILL.md`
- Create: `skills/inventree-naming/references/formats.md`
- Read-only source: `C:\Users\ruben\Projects\Hobby\Homelab\projectdock\inventree-naming-convention.md` (406 lines)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill folder `skills/inventree-naming/` with frontmatter `name: inventree-naming` (Task 2's catalog rows must match this name and folder exactly).

The executor should load the `writing-skills` skill before writing the files.

- [ ] **Step 1: Read the source doc**

Read `C:\Users\ruben\Projects\Hobby\Homelab\projectdock\inventree-naming-convention.md` in full. It is the primary source; the condensed copy in `agents/inventree.md` is NOT the source (it has drifted, e.g. its display format omits the optional resolution section).

- [ ] **Step 2: Write `skills/inventree-naming/SKILL.md`** with exactly this content:

```markdown
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
```

- [ ] **Step 3: Write `skills/inventree-naming/references/formats.md`**

Port from the source doc, in this order, verbatim except for the transforms below:

1. `# InvenTree naming: per-category formats` as the title, followed by one line: `Name and description rules live in the [SKILL.md](../SKILL.md); this file holds the per-category detail.` (Do NOT re-port the source's intro or General Rules sections; SKILL.md covers them.)
2. The source's `## Fasteners` through `## Tools` sections (lines 68-383), including all field tables, formats, and name/description example pairs.
3. Do NOT port the source's final `## Quick Reference` table (already in SKILL.md).

Transforms while porting:
- Replace every em-dash (U+2014) with a comma, colon, parenthesis, or hyphen, whichever reads most naturally. The source uses them in headings (`General Rules - Name`) and prose ("type → key specs → dimensions", "Parts in the same category must follow the **same sentence structure** - same order..."). Prose arrows (→) are fine to keep.
- Keep × (U+00D7), ⌀ (U+2300), and en-dashes (U+2013) in ranges such as `12–24V`, `4.5–28V`, `100–450°C` exactly as written.
- Fix the one broken formatting in the source (Displays section, the "(with touch)" example around lines 349-355): it has a stray unclosed code fence and a duplicated description block. Render it as one proper example: name line, then a single fenced description block with the `Resistive touchscreen.` feature flag.
- Nothing else changes. No rewording, no reordering, no new categories.

- [ ] **Step 4: Verify the skill files**

Run (PowerShell, repo root):

```powershell
Get-ChildItem -Recurse skills\inventree-naming -Filter *.md | Select-String -Pattern ([char]0x2014)
(Get-Content -Raw skills\inventree-naming\SKILL.md -TotalCount 5 | Measure-Object -Character).Characters
Select-String -Path skills\inventree-naming\SKILL.md -Pattern '^## Overview'
```

Expected: em-dash scan returns nothing; frontmatter block well under 1024 chars; the `^## Overview` hit is the first `##` heading in the body. Also eyeball that every `##` heading in `references/formats.md` matches a source section title (Fasteners, Bearings, Connectors, Switches, Dev Boards, Power Modules, Motors, Displays, Tools).

- [ ] **Step 5: No commit yet**

The skill ships with its catalog rows in one commit (Task 2), per the repo rule "a new skill ships with its catalog rows in one commit". Leave the files staged-or-unstaged; Task 2 commits them together.

---

### Task 2: Catalog rows, CHANGELOG, single feat commit

**Files:**
- Modify: `README.md` (Skills table + Layout block)
- Modify: `AGENTS.md` (`## Current skills` table)
- Modify: `CHANGELOG.md` (Unreleased section)
- Commit: everything from Tasks 1-2

**Interfaces:**
- Consumes: skill folder `skills/inventree-naming/` and frontmatter name `inventree-naming` from Task 1.
- Produces: commit `feat(skills): add inventree-naming skill (InvenTree part naming conventions)` on branch `feat/inventree-naming-skill`.

- [ ] **Step 1: README.md Skills table row.** Insert immediately after the `deep-research` row:

```markdown
| [`inventree-naming`](./skills/inventree-naming/SKILL.md) | InvenTree part naming convention. Dash-separated names, sentence case, ×/⌀ symbols, description structure with feature flags, per-category formats (fasteners, bearings, connectors, switches, dev boards, power modules, motors, displays, tools). |
```

- [ ] **Step 2: README.md Layout block.** In the `skills/` tree of the Layout block, add `├── inventree-naming/` with nested `│   ├── SKILL.md` and `│   └── references/formats.md` lines, placed after the `deep-research/` entry, matching the block's existing ASCII-tree style.

- [ ] **Step 3: AGENTS.md Current skills row.** In the `## Current skills` table, insert immediately after the `deep-research` row:

```markdown
| `skills/inventree-naming/` | `inventree-naming` | InvenTree part naming convention: dash-separated names, description structure, per-category formats. Source of truth for the convention; the inventree agents embed a condensed copy. |
```

- [ ] **Step 4: CHANGELOG.md.** Read the file first. Under the Unreleased/top section (create `## Unreleased` only if missing), add a bullet matching the house style shown by the existing `- feat(agents): ...` lines:

```markdown
- feat(skills): `inventree-naming` skill, port of the Homelab naming convention doc; catalog rows in README.md + AGENTS.md
```

- [ ] **Step 5: Verify catalogs**

```powershell
Select-String -Path README.md,AGENTS.md -Pattern 'inventree-naming'
```

Expected: hits in README.md (table row + layout block) and AGENTS.md (table row). Confirm folder name (`skills/inventree-naming/`), frontmatter `name` (`inventree-naming`), and both table entries match exactly. `opencode-install.md` needs no change (its Verify section does not name skills).

- [ ] **Step 6: Commit**

```powershell
git checkout -b feat/inventree-naming-skill
git add skills/inventree-naming README.md AGENTS.md CHANGELOG.md
git commit -m "feat(skills): add inventree-naming skill (InvenTree part naming conventions)"
```

(If the branch already exists from an earlier attempt, reuse it.) Do NOT merge and do NOT push.

---

### Task 3: Execution report + docs commit (documenter)

**Files:**
- Create: `docs/artifacts/features/inventree-naming-skill/2026-08-19-inventree-naming-skill-report.md`
- Commit: spec + plan + report

**Interfaces:**
- Consumes: completed Tasks 1-2.
- Produces: the final report the orchestrator relays.

- [ ] **Step 1: Write the report**: short execution report (what was ported from where, transforms applied, verification results with actual command output, commit hash, and the machine-local sync commands that activate the skill: copy `skills/inventree-naming/` to `~/.claude/skills/` and `~/.config/opencode/skills/`). Include the follow-up notes: the inventree agent files still embed a condensed copy (consolidation is optional future work), and the Homelab projectdock doc is superseded by the skill as source of truth (reducing it to a pointer is optional future work in the Homelab repo).

- [ ] **Step 2: Commit docs**

```powershell
git add docs/artifacts/features/inventree-naming-skill
git commit -m "docs(features): inventree-naming-skill spec, plan, and execution report"
```

Do NOT merge, do NOT push.

---

## Self-Review

- Spec coverage: skill files (Task 1), no-command decision (Task 1 design), catalogs incl. CHANGELOG (Task 2), verification gates (Task 1 Step 4, Task 2 Step 5), report (Task 3). Alternatives B/C from the spec are non-goals, no tasks needed. Covered.
- Placeholders: every step names exact paths, exact row content, or exact transforms. No TBDs.
- Consistency: folder `inventree-naming` = frontmatter `name` = both table entries; commit messages follow `<type>(<scope>): <description>`.
