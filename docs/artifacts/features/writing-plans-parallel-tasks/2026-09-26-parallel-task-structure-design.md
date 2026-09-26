# Design: Parallel-ready task structure in writing-plans

Date: 2026-09-26
Status: approved (user request: "making tasks in plans able to run in parallel is not yet executed perfectly. can you make sure that writing-plans mentions this explicitly?")

## Problem

The repo's parallel execution pipeline depends on plan metadata that the plan-producing skill never writes:

- `agents/planner.md:47` mandates every task carry a `**Depends:**` line directly after its `**Files:**` block.
- `agents/orchestrator.md:47` computes parallel waves from `**Depends:**` lines + disjoint `**Files:**` sets.
- `commands/execute-plan.md:19` same; both define the fallback: **no `Depends:` lines in the plan → execute serially**.

`skills/writing-plans/SKILL.md` (879 words) contains **zero** occurrences of `Depends` and no parallel-readiness rules. Its Task Structure template (lines 46-93) has `**Files:**` and `**Interfaces:**` but no `**Depends:**` slot. Result: plans authored via the skill omit the marker, the consumer fallback fires, and parallel execution silently degrades to serial. Producer/consumer contract mismatch.

Baseline failure evidence (RED): user-observed production behavior, plans not executing in parallel; confirmed by recon that the skill template lacks the slot the whole downstream pipeline keys on.

## Constraint carry-over from docs/artifacts/choices/

Full-text lookup done 2026-09-26: no decision record touches plan task structure, `Depends`, or parallelism. No constraints carried, none superseded.

## Approaches considered

1. **Prose paragraph** ("tasks should be parallelizable"): rejected. Failure type is an omitted structural element; prose reminders near a template are the wrong form (see writing-skills "Match the Form to the Failure").
2. **Structural template slot + rules** (chosen): add the required `**Depends:**` line to the Task Structure template, a short parallel-readiness rules block, and a Self-Review checklist item. Mirrors exactly what planner/orchestrator/execute-plan already expect, so the contract aligns without touching consumers.
3. **Rewrite/restructure the skill**: rejected, scope creep. The skill is otherwise healthy.

## Chosen design

Edit `skills/writing-plans/SKILL.md` only. Three insertions:

1. **Task Structure template**: add a `**Depends:**` line between the `**Files:**` block and `**Interfaces:**` block, showing both forms (`**Depends:** none` / `**Depends:** Task 2, Task 4`).
2. **New short section "Parallel Readiness"** (or rules folded under Task Structure, whichever diffs smaller) stating the contract verbatim-compatible with the consumers:
   - Default `**Depends:** none`; list tasks only when the Interfaces `Consumes:` block cites an earlier task's output.
   - All `Depends: none` tasks must have mutually disjoint `**Files:**` sets; overlapping files → merge the tasks or add a dependency edge.
   - Serial chain forced by the domain → maximize independent branches around it.
   - Downstream (`/execute-plan`, orchestrator) dispatches ready tasks in parallel waves and runs serially if `**Depends:**` lines are absent; missing lines forfeit parallelism.
3. **Self-Review checklist**: one new item, every task carries `**Depends:**`, and every `none`-dependency task's `**Files:**` set is disjoint from the other `none` tasks.

## Non-goals

- No changes to agents/, commands/, or workflow docs; they already state the convention.
- No changes to the vendored superpowers copy (package cache; repo is source of truth).
- No catalog row changes (README/AGENTS rows still describe the skill accurately).
- No frontmatter change (description stays trigger-only).

## Constraints

- Repo rules: no em-dashes, frontmatter untouched, `## Overview` body start preserved, Conventional Commits.
- Wording must stay compatible with `agents/orchestrator.md:47` and `commands/execute-plan.md:19` semantics (Depends after Files, files-win conflict guard, serial fallback).

## Verification intent (GREEN)

Reviewer re-derives the Depends rules from the edited skill alone and confirms they match `agents/planner.md:47` / `agents/orchestrator.md:47` semantics. Mechanical checks: `grep Depends` hits in the template + rules, em-dash scan, word count delta small.
