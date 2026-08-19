# InvenTree naming skill: port the Homelab naming convention into a repo skill

Date: 2026-08-19
Status: approved for planning (single-pass run)

## Problem

The user's InvenTree naming conventions live in a standalone doc that was hard to find:

- Primary source: `C:\Users\ruben\Projects\Hobby\Homelab\projectdock\inventree-naming-convention.md` (406 lines; full per-category field tables, examples, tools category mapping, quick reference table). A Nextcloud mirror exists at `C:\Users\ruben\Nextcloud\NAS Home\05_projects\Hobby\Homelab\projectdock\inventree-naming-convention.md` but is a dehydrated cloud placeholder (provider not running), proving the path is not reliably readable.
- Condensed copy embedded in the agents: `agents/inventree.md` (this repo) and `~/.claude/agents/inventree.md`. Both have drifted slightly from the projectdock doc (e.g. display format omits the optional resolution section).

Only the inventree agents carry the convention. Any other session that needs to name, rename, or describe InvenTree parts has no discoverable source. The user wants the conventions packaged as a skill.

## Goal

One new skill `inventree-naming` in this repo: self-contained, catalogued, and synced to agent skill dirs like every other skill. Source of truth for the convention moves to the skill.

## Source hierarchy (read-only inputs)

1. Primary: the Homelab projectdock doc (richest, newest variant).
2. Secondary: `agents/inventree.md` naming section (condensed). Where the two differ, the projectdock doc wins.

## Design

### Files

- `skills/inventree-naming/SKILL.md`
  - Frontmatter: `name: inventree-naming`, description starting with "Use when..." covering triggers: naming/renaming/describing InvenTree parts, per-category formats, validating names during inventory (AliExpress CSV) imports.
  - Body (lean, under ~500 words): `## Overview`, `## When to use`, `## Name rules` (dash-separated sections, sentence case, × U+00D7 for dimensions, ⌀ for diameter, omit non-applicable sections, one part = one variant), `## Description rules` (full-picture sentence block + blank line + feature flags, every line ends with a period, same sentence structure within a category), `## Quick reference` (the 16-row format table), one or two worked examples (screw; switch with feature flags), pointer to `references/formats.md`.
- `skills/inventree-naming/references/formats.md`
  - Full port of the projectdock doc's per-category sections: fasteners (screws/bolts, heat-set inserts), bearings, connectors (banana, XT, JST, DC barrel, pin headers), switches, dev boards, power modules (buck/boost, BMS, chargers), motors, displays (incl. optional resolution), tools (incl. tools-category mapping), with the field tables and name/description example pairs.
  - Transform rules: em-dashes (U+2014) replaced with commas, colons, parentheses, or hyphens (repo-wide ban). × (U+00D7), ⌀ (U+2300), and en-dashes in numeric ranges (e.g. 12-24V) are kept. No other content edits; this is a port, not a rewrite.

### Not included

- No slash command: the description triggers reliably on "inventree" / "naming" / "rename part"; commands are an escape hatch, not a default.
- No changes to `agents/inventree.md` or `~/.claude/agents/inventree.md`: they keep their embedded condensed copies (live, proven agents). Consolidating them onto the skill is a possible follow-up, out of scope.
- No changes to the Homelab repo (the projectdock doc stays as-is; recommending later to reduce it to a pointer is a follow-up note, not a task).

### Catalogs (same commit as the skill)

- `README.md`: row in the `## Skills` table (alphabetical), plus the `skills/` entry in the Layout block.
- `AGENTS.md`: row in `## Current skills` (alphabetical).
- `CHANGELOG.md`: Unreleased entry for the new skill.
- `opencode-install.md`: skip (its Verify section does not list skills by name).

## Alternatives considered

- **B: SKILL.md that links to the Homelab path.** Rejected: skills must be self-contained; the Nextcloud mirror is dehydrated today and the Projects clone path is machine-specific.
- **C: Also refactor the inventree agents to load the skill instead of embedding the convention.** Deferred: touches proven live agents; separate concern from publishing the skill.

## Verification

1. Frontmatter: `name` kebab-case and matches folder name; description starts with "Use when...", trigger-focused, under 1024 chars total.
2. Em-dash scan (`Select-String -Pattern ([char]0x2014)`) on both new files returns empty.
3. Body starts with `## Overview`; no `## Skill` heading; lean word count.
4. Catalog rows present in README.md and AGENTS.md, folder name / frontmatter name / table entries match exactly.
5. Content fidelity spot-check: quick reference table rows match the projectdock doc's Quick Reference; display format includes the optional resolution section (the drift point vs the agent copy).
