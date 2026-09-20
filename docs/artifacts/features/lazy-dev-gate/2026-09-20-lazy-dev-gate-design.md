# lazy-dev gate: lean-plan review in the planner flow

- **Date:** 2026-09-20
- **Status:** approved (user sign-off on approaches + design)
- **Scope:** `agents/`, `commands/full-cycle.md`, repo catalogs. No runtime code.

## Problem

The planner writes a spec and plan, then dispatches the orchestrator. Nothing independently checks the plan for over-engineering before execution. Ponytail principles (YAGNI, stdlib first, fewest tasks, shortest diff) are applied downstream by executor/reviewer, but by then a bloated plan has already been priced into tasks, commits, and reviews. The user wants an explicit gate: a new read-only subagent `lazy-dev`, focused on the ponytail skill, that reviews the plan and returns corrections to the planner.

## Goals

- New subagent `agents/lazy-dev.md`: reviews the written plan for over-engineering, returns PASS or numbered findings with specific fixes.
- Planner gains a gate step between "plan written" and "orchestrator dispatched": loop findings into the plan until PASS, capped at 2 review rounds.
- Always-on: every spec+plan run passes through the gate. No new keyword.
- Lean: no re-review loop invention, no spec rewrites unless a finding invalidates the spec, no new sync steps (existing `agents/` sync convention covers the new file).

## Non-goals (YAGNI)

- Reviewing implementation code (reviewer already covers ponytail violations per task).
- A skip keyword (`no lazy-review`): trivial plans get a fast PASS instead; no keyword surface to maintain.
- Loading supporting skills beyond ponytail (`code-standardization`, `writing-plans`, `ponytail-review` etc.): the gate reviews a *plan*, not code or plan formatting. The ponytail ladder, embedded in the agent body, is the whole lens. The ponytail plugin already auto-activates `ponytail` at level `full` every session, so availability is not a concern.
- Changes to `orchestrator.md` or `commands/execute-plan.md`: the gate is planner-flow only; leftover findings reach the orchestrator via the planner's dispatch prompt.

## Approaches considered

| Approach | Verdict |
|---|---|
| **A. New `agents/lazy-dev.md` read-only subagent, planner gate step** | Chosen. Independent eyes, clear contract, fits the existing agent roster pattern (clone of `reviewer.md` shape). |
| B. Reuse `reviewer` with a "review the plan" prompt | Rejected: reviewer's contract is per-task diff review after implementation; muddling plan review into it weakens both roles. |
| C. Planner self-review with ponytail | Rejected: the writer grades its own homework; no independence, which is the point of a gate. |

## Design

### 1. New agent: `agents/lazy-dev.md`

Structural clone of `agents/reviewer.md`: `mode: subagent`, GLM 5.3 with `variant: high`, read-only (edit/write/patch/task/webfetch denied, bash allowed for quick repo checks), `homelab*` denied in `tools:`, `"*": allow` + denylist `permission.skill:` pattern so the ponytail suite surfaces and planning-workflow skills do not.

Exact file content:

```markdown
---
description: Lean-plan gate. Reviews a written implementation plan for over-engineering before execution. Read-only plus bash; cannot edit files or dispatch subagents. Returns PASS or numbered findings with specific fixes. Dispatched by the planner after writing the spec and plan; the planner loops findings back until PASS, capped at 2 rounds.
mode: subagent
color: info
model: zai-coding-plan/glm-5.3
variant: high
tools:
  write: false
  edit: false
  patch: false
  task: false
  webfetch: false
  "homelab*": false
permission:
  edit: deny
  write: deny
  patch: deny
  task: deny
  webfetch: deny
  skill:
    "*": allow
    "brainstorming": deny
    "writing-plans": deny
    "executing-plans": deny
    "subagent-driven-development": deny
    "dispatching-parallel-agents": deny
    "multi-plan-orchestration": deny
    "finishing-a-development-branch": deny
    "using-git-worktrees": deny
    "requesting-code-review": deny
    "receiving-code-review": deny
    "test-driven-development": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
    "code-standardization": deny
    "stop-slop": deny
    "synctool-sync": deny
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
---

You are lazy-dev: the lean-plan gate. You review a written implementation plan for over-engineering before anything gets built. Read-only plus bash for quick repo checks; you do not edit, write, or dispatch.

Lens: ponytail. Interrogate every task with the ladder, in order:
1. Does this task need to exist at all? Speculative need = recommend deletion, say so in one line.
2. Does the plan prescribe a custom solution where the standard library, a native platform feature, or an already-installed dependency covers it?
3. Does a task build flexibility, abstraction, or configuration nothing asked for?
4. Would the fewest-tasks, shortest-diff version of this plan be materially worse? If not, collapse the tasks.
5. Is verification proportional? One runnable check per non-trivial task; no per-function suites, no frameworks unless asked.

Two passes:
1. Context: read the spec and plan end to end. The spec defines what was asked; anything in the plan the spec does not require is a finding candidate.
2. Verdict per task. Use bash only when a claim needs checking (a dependency already present in the manifest, a stdlib equivalent). Do not redesign plans that are already minimal; give them a fast PASS.

Return PASS, or a numbered list. Each finding: the plan reference (task number or heading), the problem in one line, and the specific fix ("Delete task 3; <X> already covers it"). If a finding's root cause is in the spec, prefix it with "spec:" and state what to change there. Never rewrite the plan yourself.
```

### 2. Planner wiring: `agents/planner.md`

Insert a new step 5 between current step 4 (plan) and current step 5 (dispatch); renumber 5 to 6 and 6 to 7:

> 5. Lean-plan gate: dispatch the lazy-dev subagent with the spec and plan paths. On findings, fold the corrections into the plan (edit the spec too when a finding is prefixed "spec:") and re-dispatch. PASS is required before dispatching the orchestrator; cap the loop at 2 review rounds, and on a cap without PASS attach the remaining findings to the orchestrator dispatch as constraints. If the lazy-dev agent is unavailable, dispatch the general subagent instructed to review the plan with the ponytail skill and return PASS or findings in the same format.

Consistency edits inside existing steps:
- Step 1: "the manual handoff in step 6" becomes "the manual handoff in step 7".
- Current step 5 (dispatch), fallback clause: "fall back to step 6" becomes "fall back to step 7".
- Current step 6 (handoff) renumbered to 7, text otherwise unchanged.

Frontmatter description: append the clause "Gates every plan through the lazy-dev subagent (lean-plan review, loop to PASS capped at 2 rounds) before dispatching." placed after the sentence describing spec and plan writing.

### 3. Mirror: `commands/full-cycle.md`

Insert one step between current step 3 (Plan) and current step 4 (Execute); renumber subsequent steps:

> 4. Lean-plan gate: dispatch the `lazy-dev` subagent with the spec and plan paths; fold findings into the plan and re-dispatch until PASS (max 2 rounds), attaching leftovers to the execute dispatch as constraints.

### 4. Catalogs (same commit as the new agent, repo convention)

- `agents/README.md`:
  - Roster row (`## The set`): `lazy-dev` | subagent | `zai-coding-plan/glm-5.3` | "Lean-plan gate: reviews the written plan for over-engineering before orchestrator dispatch; PASS or findings, planner loops to a 2-round cap." | "edit/write/patch/task/webfetch tools; planning and review-workflow skills".
  - Dispatch-convention paragraph: mention that the `planner` dispatches plan reviews to `lazy-dev` before any orchestration.
  - Model-routing paragraph: add `lazy-dev` to the list of GLM agents running `high` effort.
- `AGENTS.md` (Agent definitions paragraph): add `lazy-dev` to the custom-agents name list, right after `reviewer`, with the parenthetical "(lean-plan gate)".
- `CHANGELOG.md`: `Added` entry: "lazy-dev subagent: lean-plan gate reviewing plans for over-engineering before orchestrator dispatch".
- `docs/workflows/plan-flow.drawio`: one gate box for lazy-dev between the plan step and the orchestrator dispatch, mirroring existing box style and ponytail labeling.

## Loop semantics

1. Round 1: planner writes plan, dispatches lazy-dev with spec+plan paths.
2. PASS: proceed to orchestrator immediately.
3. Findings: planner folds corrections into the plan (and spec for "spec:" findings), re-dispatches. Round 2.
4. Round 2 PASS: proceed. Round 2 findings: attach them to the orchestrator dispatch as constraints and proceed. No round 3.
5. lazy-dev unavailable: general subagent with the same review instructions. No subagent dispatch possible at all: skip the gate and note it in the orchestrator dispatch prompt.

## Verification

- `opencode agent list` exits clean (frontmatter parses).
- `opencode debug agent lazy-dev` resolves the agent with expected model, variant, and denies.
- Em-dash check passes: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty.
- Grep confirms the gate step exists in both `agents/planner.md` and `commands/full-cycle.md`, and the roster row exists in `agents/README.md`.

## Risks / edge cases

- **Gate adds latency to every run.** Accepted by user (always-on). A minimal plan costs one fast PASS.
- **lazy-dev over-reaches into redesign.** Output contract forbids rewriting; findings must name a specific fix, planner owns the edit.
- **Ponytail suite absent on a machine.** The agent body embeds the ladder itself, so the gate degrades gracefully; denylist entries for absent skills are inert.

## Files changed

| File | Change |
|---|---|
| `agents/lazy-dev.md` | New (content above) |
| `agents/planner.md` | New step 5, renumber, description clause |
| `commands/full-cycle.md` | New gate step, renumber |
| `agents/README.md` | Roster row, dispatch paragraph, model routing |
| `AGENTS.md` | Agent name list |
| `CHANGELOG.md` | Added entry |
| `docs/workflows/plan-flow.drawio` | Gate box |
