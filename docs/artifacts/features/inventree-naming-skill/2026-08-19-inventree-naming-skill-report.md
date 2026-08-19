# InvenTree naming skill: execution report

Date: 2026-08-19

## Summary

Shipped the `inventree-naming` skill on branch `feat/inventree-naming-skill`, feat commit `3247d4d`. Five files changed, +402 lines: `skills/inventree-naming/SKILL.md` (77 lines, lean body), `skills/inventree-naming/references/formats.md` (319 lines, per-category detail), plus catalog rows in `README.md`, `AGENTS.md`, and a `CHANGELOG.md` entry, all in the same feat commit per repo rules. This commit adds the spec, plan, and this report.

## What was ported

- Source (read-only): Homelab `projectdock/inventree-naming-convention.md` (406 lines), the primary variant per the spec's source hierarchy.
- `SKILL.md` is the new lean body: overview, when-to-use triggers, name rules, description rules, the 16-row quick reference table, two worked examples (screw; switch with feature flags), pointer to `references/formats.md`.
- `references/formats.md` is a verbatim port of source lines 68-383: Fasteners, Bearings, Connectors, Switches, Dev Boards, Power Modules, Motors, Displays (incl. optional resolution), Tools (incl. tools-category mapping), with all field tables and name/description example pairs.
- Intentionally not re-ported: the source's intro/General Rules (covered by SKILL.md's Name rules and Description rules) and the final Quick Reference table (already in SKILL.md).

## Transforms applied

- Em-dash scrub: every U+2014 replaced with a comma, colon, parenthesis, or hyphen. × (U+00D7), ⌀ (U+2300), and en-dashes (U+2013) in numeric ranges kept verbatim.
- One formatting fix: the Displays "(with touch)" example (source lines ~349-355) had a stray unclosed code fence and a duplicated description block; rendered as one proper example with the `Resistive touchscreen.` feature flag.
- Nothing else. No rewording, no reordering, no new categories.

## Verification

Actual outputs, run from repo root on `feat/inventree-naming-skill` after `3247d4d`:

Em-dash scan (both new files):

```powershell
Get-ChildItem -Recurse skills\inventree-naming -Filter *.md | Select-String -Pattern ([char]0x2014)
# (no output: zero hits)
```

Frontmatter size (first 5 lines, the frontmatter block):

```powershell
(Get-Content skills\inventree-naming\SKILL.md -TotalCount 5 | Measure-Object -Character).Characters
474
```

Well under the 1024-char frontmatter cap. (`-TotalCount 5`, not `-Raw`: PS 5.1 cannot combine the two flags.)

First body heading:

```powershell
Select-String -Path skills\inventree-naming\SKILL.md -Pattern '^## Overview'
skills\inventree-naming\SKILL.md:6:## Overview
```

`references/formats.md` section headings (all 9 expected, in source order):

```text
Fasteners, Bearings, Connectors, Switches, Dev Boards, Power Modules, Motors, Displays, Tools
```

Catalog hits:

```powershell
Select-String -Path README.md,AGENTS.md -Pattern 'inventree-naming'
README.md:16   Skills table row
README.md:80   Layout block entry (skills/inventree-naming/)
AGENTS.md:139  Current skills row
```

Folder name, frontmatter `name`, and both table entries all read `inventree-naming`. `opencode-install.md` unchanged (its Verify section does not name skills).

## Commits

| Hash | Subject |
|---|---|
| `3247d4d` | `feat(skills): add inventree-naming skill (InvenTree part naming conventions)` |
| (this commit) | `docs(features): inventree-naming-skill spec, plan, and execution report` |

## Follow-ups

- `agents/inventree.md` and `~/.claude/agents/inventree.md` still embed a condensed copy of the convention; consolidating them onto the skill is optional future work.
- The Homelab `projectdock/inventree-naming-convention.md` is now superseded by this skill as source of truth; reducing it to a pointer is optional future work in the Homelab repo.

## Sync to activate

Machine-local (Windows PowerShell), then restart the agent session:

```powershell
Copy-Item -Recurse skills\inventree-naming $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse skills\inventree-naming $env:USERPROFILE\.config\opencode\skills\
```
