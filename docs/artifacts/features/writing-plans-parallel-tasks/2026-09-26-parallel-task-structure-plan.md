# Plan: Parallel-ready task structure in writing-plans

Spec: `docs/artifacts/features/writing-plans-parallel-tasks/2026-09-26-parallel-task-structure-design.md`

Versioning: AGENTS.md declares no `### Versioning` canonical source; repo docs are unversioned, no bump.

Branch: `feat/writing-plans-parallel-tasks` off `main`.

## Task 1: Add Depends slot and parallel-readiness rules to writing-plans skill

**Files:**
- Modify: `skills/writing-plans/SKILL.md`

**Depends:** none

**Interfaces:**
- Consumes: nothing (self-contained doc edit).
- Produces: a Task Structure template carrying a required `**Depends:**` line after `**Files:**`, plus parallel-readiness rules matching `agents/planner.md:47`, `agents/orchestrator.md:47`, and `commands/execute-plan.md:19` semantics.

**Context:** The downstream pipeline keys on plan metadata the skill never writes. Read the three consumer files before editing so wording matches:
- `agents/planner.md` line 47 (Depends-after-Files, default none, disjoint Files for none-tasks, serial-chain rule)
- `agents/orchestrator.md` line 47 (waves from Depends + Files, files-win guard, serial fallback when lines absent)
- `commands/execute-plan.md` line 19 (ready = all Depends reviewer-passed, concurrent dispatch, serial fallback)

**Steps:**

1. Edit `skills/writing-plans/SKILL.md`:
   - In the `## Task Structure` template block, insert directly after the `**Files:**` list and before `**Interfaces:**`:
     ````markdown
     **Depends:** none  (or: Task 2, Task 4)
     ````
     rendered as a template line showing both accepted forms, e.g. `**Depends:** none` with a comment that tasks listed here must be complete first.
   - Add a compact `## Parallel Readiness` section after `## Task Structure` (before `## No Placeholders`) with the contract:
     - Default `**Depends:** none`; list tasks only when the Interfaces `Consumes:` block cites an earlier task's output.
     - All `Depends: none` tasks must have mutually disjoint `**Files:**` sets; overlap → merge the tasks or add a dependency edge.
     - Domain forces a serial chain → maximize independent branches around it.
     - Missing `Depends:` lines forfeit parallelism: the executor runs the whole plan serially, one task at a time.
   - Add one Self-Review checklist item: every task carries a `**Depends:**` line, and every `none`-dependency task's `**Files:**` set is disjoint from the other `none` tasks.
   - Style: no em-dashes, keep additions tight (target +120 words or less), do not touch frontmatter, do not touch other sections.
2. Verify:
   - `grep -n "Depends" skills/writing-plans/SKILL.md` shows the template slot, rules section, and checklist item.
   - Em-dash scan over the file returns nothing: `grep -n $'\u2014' skills/writing-plans/SKILL.md`
   - `wc -w skills/writing-plans/SKILL.md` grew by roughly 100-140 words, nothing else moved.
3. Commit on `feat/writing-plans-parallel-tasks`: `feat(skills): require parallel-ready task structure in writing-plans`
4. Reviewer gate: re-derive the Depends rules from the edited skill alone; confirm they match the planner/orchestrator/execute-plan semantics quoted above (Depends after Files, default none, disjoint-Files rule, serial fallback). Report any drift.

## Self-Review

- Single task, no hidden dependencies; spec path referenced.
- Exact file path, exact insertion points, consumer files named for wording alignment.
- Verification commands concrete and runnable.
- Catalog rows and frontmatter explicitly out of scope, so no catalog sync needed for this commit.
