# Design: custom `explore` subagent + explore-only planner recon

- Date: 2026-09-19
- Status: approved for planning
- Scope: `agents/` definitions and their catalogs. Markdown only, no code.

## Problem

Two gaps in how the planner (and by extension the roster) handles exploration:

1. **Partial delegation.** `agents/planner.md` step 2 says "Dispatch the explore subagent for codebase recon instead of grepping in your own window", but in practice the planner drifts: after the first explore dispatch it starts reading code files itself to pinpoint where changes land. The instruction covers only step 2 and only "grepping"; nothing forbids direct file reading later in the run.
2. **Unenforced and unpinned recon tooling.** Recon currently uses opencode's **built-in** `explore` subagent (`agents/README.md`: "no custom file needed"). That built-in has no model pin (inherits the caller's model), no variant pin, and **no webfetch access**, so "let explore do the online lookup" is impossible today. The planner itself has no `webfetch` deny, so it can (and does) fetch pages directly.

Requested behavior: ALL exploration by the planner, for the whole run, goes through an explore subagent. That includes (a) reading code files to pinpoint where changes land, and (b) any online lookup. Plus: our own explore definition, pinned to `zai-coding-plan/glm-5.3-flash`, variant `high`.

## Goals

- Custom `agents/explore.md` that shadows the built-in `explore`, pinned to `zai-coding-plan/glm-5.3-flash`, `variant: high`.
- Explore is read-only for the repo but can `webfetch` (online lookup is part of its job).
- Planner is hard-required to delegate: body rule covering the whole run, plus a `webfetch` deny in planner `tools:` + `permission:` so direct fetching is impossible, not just discouraged.
- All catalogs updated in the same change (agents/README.md roster + built-in sentence + routing paragraph, root README.md, root AGENTS.md).

## Non-goals

- No changes to orchestrator/writer bodies (they already dispatch `explore` by name and inherit the new definition automatically).
- No change to the planner's own model pin (`zai-coding-plan/glm-5.3` stays).
- No deep-research integration; explore stays a lean recon agent.
- No sync automation; sync stays manual per `agents/README.md`.

## Approaches considered

### A. Shadow the built-in name (recommended)

Create `agents/explore.md` named `explore`. In opencode, a custom agent with the same name as a built-in overrides it. Consequences:

- Zero call-site edits for dispatch: `planner.md`, `orchestrator.md`, `writer.md`, `commands/full-cycle.md`, and `restructure-flow.md` all already dispatch `explore` by name.
- Graceful fallback: on machines without the synced file, dispatches hit the built-in (still functional, just unpinned and web-less).
- One new file, catalog rows updated. Smallest possible diff that satisfies every requirement.

### B. Keep built-in explore, tighten planner wording only

Rejected: cannot pin model/variant (explicit requirement), and the built-in has no webfetch, so delegated online lookup would fail. Wording-only fixes are also exactly what already failed (the current step-2 sentence is being drifted away from).

### C. New differently-named agent (e.g. `recon`) + edit every dispatch site

Rejected: 5+ call-site edits for no gain, loses the built-in fallback, larger review surface.

## Detailed design

### 1. New file: `agents/explore.md`

Frontmatter follows house style (both `tools:` and matching `permission:`, broad `"*"` first / narrow last, `homelab*` denied, explicit variant pin, reviewer-style skill denylist for a read-only subagent). Non-empty body intentionally replaces the built-in's default prompt and carries the recon protocol plus web lookup.

```markdown
---
description: Fast read-only codebase recon and online lookup subagent. Finds files, maps where changes land, answers architecture questions, verifies syntax and behavior against online docs via webfetch. Dispatch for any multi-file reading or web research instead of reading files in your own window. Returns structured findings with verbatim quotes.
mode: subagent
color: info
model: zai-coding-plan/glm-5.3-flash
variant: high
tools:
  write: false
  edit: false
  patch: false
  task: false
  "homelab*": false
permission:
  edit: deny
  write: deny
  patch: deny
  task: deny
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
    "synctool-sync": deny
---

You are the read-only recon subagent. Other agents dispatch you so they never read files or fetch web pages themselves: codebase exploration (find files, map where changes land, answer how-does-X-work) and online lookup (docs, schemas, syntax verification). You never edit files and never dispatch subagents.

Method:

1. Scope first: restate the question and pick the depth. quick = one fact. medium = focused map of one area. very thorough = multi-round search across naming conventions and references.
2. Search before reading: glob/grep to narrow, then read only the files that answer the question. Batch independent tool calls in one round.
3. Read with intent: quote verbatim what matters (frontmatter blocks, key lines with file:line); summarize the rest. Never dump whole files unless asked.
4. Web lookup: when asked to verify something online, fetch the official docs or schema, quote the exact syntax or wording, and cite the URL.
5. Return structured findings: direct answers first, then evidence, then an explicit "not found" for anything the search did not surface. Flag contradictions between files.

You change nothing: no edits, no writes, no commits, no dispatches.
```

Notes:

- `webfetch` is deliberately NOT denied anywhere in the frontmatter: online lookup is half the job. `websearch` is left at its default.
- `variant: high` on `glm-5.3-flash` is proven in-repo (doc-standardizer, code-standardizer use exactly this pair) and schema-valid (free-form string, `high` is a documented built-in variant name).
- The body is short on purpose: this agent is dispatched many times per run; context cost compounds.

### 2. `agents/planner.md`: explore-only recon, whole run

Three edits:

a. Description, replace last sentence: "Dispatches the explore subagent for codebase recon." becomes "Delegates all recon (codebase reading and web lookup) to the explore subagent."

b. Frontmatter, add webfetch removal so the rule is enforced, not just written (house pattern: keep both `tools:` and `permission:`):

```yaml
tools:
  webfetch: false
  "homelab*": false
```

and in `permission:`, after the `patch:` block:

```yaml
  webfetch: deny
```

c. Body, add a standing rule after the "Scope discipline" paragraph:

```markdown
Exploration discipline (whole run, not just step 2): every read of project files and every online lookup goes through the explore subagent. That includes pinpointing where code lands, reading files to size up edit targets, and web lookups for docs or syntax. The only files you read directly are ones you authored under docs/artifacts/ and repo-level context docs (AGENTS.md, README.md). webfetch is denied to you by permission; recon is a dispatch, not a fetch.
```

The existing step-2 sentence stays (it is now a special case of the standing rule).

### 3. `commands/full-cycle.md`: one-line consistency

Step 1 currently says "Dispatch the `explore` subagent for codebase recon." Extend to "...for codebase recon and web lookups." (exact wording matched at execution time).

### 4. Catalog updates (same change, house rule: undocumented agents do not exist)

- `agents/README.md` `## The set` table: insert a row directly after the `planner` row (dispatch-order grouping): `explore` | subagent | `zai-coding-plan/glm-5.3-flash` (`high` variant) | Read-only recon: codebase exploration (find files, map landing zones, explain code) plus online lookup via webfetch. Shadows the opencode built-in of the same name; existing dispatch sites route to it once synced, built-in remains the fallback. | edit/write/patch/task tools; planning and review-workflow skills
- `agents/README.md` paragraph currently reading "The built-in `explore` subagent handles codebase recon for planner and orchestrator; no custom file needed." becomes: "The custom `explore` subagent handles codebase recon and web lookup for planner and orchestrator. It shadows the opencode built-in of the same name: every existing dispatch site routes to the custom definition once synced, and falls back to the built-in on machines without the file."
- `agents/README.md` model-routing paragraph: add `explore` to the `high`-effort GLM list (planner, reviewer, oracle, doc-standardizer, code-standardizer, documenter, explore).
- Root `README.md` agents paragraph: insert `explore` into the agent list (after `documenter`).
- Root `AGENTS.md` "Agent definitions" section: insert `explore` into the agent list (after `documenter`).
- `CHANGELOG.md`: one `Added` line for the explore agent and one `Changed` line for planner delegation (match existing entry style; landed with the respective commits).

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Name shadowing surprises someone ("why is explore pinned?") | Documented explicitly in agents/README.md paragraph and roster row; fallback behavior stated |
| Planner blocked from a legitimate fetch (e.g. reading a linked doc mid-spec) | Intended behavior per request; escape hatch is dispatching explore (which has webfetch), same cost pattern as file recon |
| Non-empty body loses the built-in explore's default prompt | Intentional: body carries a full recon + web protocol; verified via `opencode debug agent explore` |
| Subagent runs `default` variant instead of `high` when dispatched | Explicit `variant: high` pin (the exact failure mode agents/README.md documents for the orchestrator, verified 2026-07-31) |

## Verification

- `opencode agent list` parses after each frontmatter edit (if the opencode CLI is on PATH in the executing shell; otherwise careful frontmatter review and note it).
- `opencode debug agent explore` resolves: model `zai-coding-plan/glm-5.3-flash`, variant `high`, mode `subagent`, webfetch not denied, edit/write/patch/task denied.
- `opencode debug agent planner` resolves: `webfetch` denied.
- Em-dash scan over touched files returns empty.
- Catalog cross-check: `explore` present in agents/README.md table, agents/README.md routing paragraph, root README.md, root AGENTS.md.
