# Choices registry: decision records in docs/artifacts/choices/

- Date: 2026-09-24
- Status: approved (user confirmed via brainstorm Q&A)
- Feature: choices-registry

## Overview

Agents executing plans make choices: which plugin to add, which approach to take, which standard to follow. Today those choices live scattered across specs, task reports, and commit messages. When someone later wants to remove or change one of these things, there is no reliable place to look up why it exists.

This design adds a choices registry: one decision record per qualifying choice, under `docs/artifacts/choices/`, written by the documenter at close-out, consulted by the planner before locking new decisions, and surfaced in PR descriptions through a new `## Choices` section.

## Goals

1. Durable, findable record of why a choice was made, including rejected alternatives.
2. A lookup step so agents check prior choices before undoing or contradicting them.
3. Standardized in the flow (planner, lazy-dev, orchestrator, documenter) and in PR messages.

## Non-goals

- A standalone skill file. The convention lives in `references/artifacts.md` plus agent wiring. A third home for the same rules is the two-homes anti-pattern this repo already forbids. The user's future custom flow can cite the convention directly.
- Recording every approach considered. Only constraining choices get entries; spec-local detail stays in the spec.
- Tooling, hooks, or validation for the registry. `.githooks/pre-commit` needs no changes (verified: it validates em-dashes, frontmatter, catalog rows, forbidden dirs only).

## Decisions (locked with user)

1. **Threshold:** reversible/constraining choices only. Things a future agent might wrongly undo or that constrain future work: dependency and plugin picks, architecture forks, standards picks, explicit X-over-Y calls. Routine trivia stays in the spec/report.
2. **Layout:** one file per decision plus an index (`docs/artifacts/choices/YYYY-MM-DD-<slug>-decision.md` and `docs/artifacts/choices/index.md`). Lookup greps the directory full-text, so correctness never depends on the index staying fresh; the index is the human-scannable view, maintained by the documenter in the same write pass. (Kept despite a gate finding, because the user explicitly chose it.)
3. **Enforcement:** at planner level. The planner greps the registry before locking spec decisions. lazy-dev gets a lightweight contradiction check. The user's future custom skill set will absorb the same step into its own flow description.
4. **Writer:** documenter is the single registry writer, at close-out, from run material. No new writers.

## Design

### Registry layout

- `docs/artifacts/choices/YYYY-MM-DD-<slug>-decision.md`: one file per decision.
- `docs/artifacts/choices/index.md`: one table row per decision (Date | Decision | Status | File). Seeded at implementation. The decision file is the source of truth; the index is a scannable view the documenter updates in the same write pass.
- `decision` becomes a new token in the artifacts filename grammar in `references/artifacts.md`.

### Entry template

```markdown
# <Slug title>

- Date: YYYY-MM-DD
- Status: active            <!-- or: superseded by YYYY-MM-DD-<slug>-decision.md -->
- Source: <path to plan, report, or PR that produced the choice>

## Choice
<One sentence: what was chosen.>

## Alternatives rejected
<What was not chosen and why not. One line per alternative.>

## Revisit when
<The condition that would invalidate this choice.>
```

Superseding never deletes: the old entry's status line flips to `superseded by <file>`, and the new entry cites it.

### Flow integration

| Agent/file | Change |
|---|---|
| `agents/planner.md` | New step before locking the spec: grep `docs/artifacts/choices/` (all files, full text) for the task's topics and likely dependency/plugin names, read hits, carry constraints into the spec, note contradictions as supersessions. |
| `agents/lazy-dev.md` | One check bullet: a plan that contradicts an active registry entry fails review unless the plan explicitly supersedes it. |
| `agents/orchestrator.md` | Step 8 dispatch payload gains: approaches considered and rejected (from the spec), defaults taken, choices superseded. |
| `agents/documenter.md` | New step after the report: write one decision file per qualifying choice using the template, add an index row, include the files in the PR description. Skip silently when nothing qualifies. Frontmatter description updated to mention the registry. |
| `commands/execute-plan.md` | Setup line "pick the obvious choice, note it" gains its destination: the task report, which feeds the documenter. |
| `commands/full-cycle.md` | Step 5 documentation deliverable list gains `choices entries` (the wiring itself lives in the planner and documenter agent definitions; no separate description). |

### PR integration

`skills/pr-description/SKILL.md` gains a `## Choices` section between `## Verification` and `## Docs`: lists new/updated decision files with a one-line why each, and mentions the registry path. Existing rule holds: every section present, write `None` when empty.

### Convention home (source of truth)

`skills/rubens-project-standardization/references/artifacts.md`:

- Layout tree: add `choices/` alongside `reviews/` (cross-feature scope, like reviews).
- Filename grammar: add the `decision` token.
- New `## Choices` section: threshold rule, template, index, supersede flow, documenter-writes rule, planner-looks-up rule.
- Per-framework redirect clause: redirect decisions to `docs/artifacts/choices/`.
- Cross-session memory overlap: the existing line-240 guidance (copy critical A-over-B decisions into a memory entry) gets repointed to the registry for constraining decisions; memory stays for non-constraining session context.

`AGENTS.md` `## Artifacts` section: add the `choices/` folder and `-decision.md` suffix to the tree and prose.

## Error handling

- Missing or empty registry: treated as "no recorded choices", not a failure. The directory is seeded with `index.md` at implementation so this is rare.
- Nothing qualifies in a run: documenter writes nothing and the PR section says `None`.
- Contradiction found at planner time: planner records the supersession intent in the spec; documenter flips the old entry's status line at close-out.

## Verification

1. All listed files contain their edits; `grep` for `choices` hits each intended file.
2. No em-dashes in any touched file (repo rule, hook-enforced).
3. Convention self-consistency: artifacts.md tree, grammar token, section, redirect, and memory clause all mention the registry.
4. `docs/artifacts/choices/index.md` exists with a header row.
5. Hook pass: pre-commit rejects nothing on the final diff.
