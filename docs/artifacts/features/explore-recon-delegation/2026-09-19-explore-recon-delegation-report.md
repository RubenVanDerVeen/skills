# Explore recon delegation: execution report

Date: 2026-09-19
Branch: `plan-explore-recon` (base `main`)
Plan: `docs/artifacts/features/explore-recon-delegation/2026-09-19-explore-recon-delegation-plan.md`
Spec: `docs/artifacts/features/explore-recon-delegation/2026-09-19-explore-recon-delegation-design.md`

## Summary

The planner's exploration is now hard-delegated to a custom `explore` subagent. A new `agents/explore.md` shadows the opencode built-in of the same name: mode `subagent`, model `zai-coding-plan/glm-5.3-flash`, variant `high`, read-only for the repo (edit/write/patch/task denied) with webfetch allowed, plus a 15-skill denylist covering planning and review-workflow skills. Because it shadows the built-in name, every existing dispatch site (planner, orchestrator, writer, full-cycle, restructure-flow) routes to it with zero call-site edits, and machines without the synced file fall back to the built-in. The planner is now forced, not just asked, to delegate: its frontmatter carries `webfetch: false` in `tools:` and `webfetch: deny` in `permission:` so direct fetching is impossible, and a standing "Exploration discipline" body rule covers the whole run instead of only step 2. `commands/full-cycle.md` step 1 was extended for consistency ("for codebase recon and web lookups"). All catalogs (agents/README.md roster, shadow paragraph, routing list; root README.md; root AGENTS.md) shipped in Task 1's commit per the same-commit rule, and CHANGELOG.md carries one Added and one Changed entry. Both tasks completed and verified; both reviewer passes returned PASS with no findings; doc-standardizer returned 11/11 PASS with one quick-fix (untracked spec/plan files), resolved by this docs commit.

## Branch and commits

| Hash | Subject |
|---|---|
| `952af7f` | `feat(agents): add explore subagent pinned to glm-5.3-flash high` |
| `f703f7f` | `feat(agents): force planner recon through explore subagent` |
| (this commit) | `docs(artifacts): add explore-recon-delegation report and ship spec/plan` |

Base: `main`. Branch is local-only; not pushed, no PR.

## Files changed (diff stats)

```
 AGENTS.md              |  2 +-
 CHANGELOG.md           |  2 ++
 README.md              |  2 +-
 agents/README.md       |  5 +++--
 agents/explore.md      | 48 ++++++++++++++++++++++++++++++++++++++++++++++++
 agents/planner.md      |  6 +++++-
 commands/full-cycle.md |  2 +-
 7 files changed, 61 insertions(+), 6 deletions(-)
```

This commit adds the three artifact files (design, plan, this report) under `docs/artifacts/features/explore-recon-delegation/`.

## Task breakdown

### Task 1: Create `agents/explore.md` and update all catalogs (commit `952af7f`)

- Created `agents/explore.md` exactly per plan step 2: frontmatter with `mode: subagent`, `color: info`, `model: zai-coding-plan/glm-5.3-flash`, `variant: high`, `tools:` denying write/edit/patch/task and `homelab*`, `permission:` denying edit/write/patch/task, and a skill block with broad `"*": allow` first and 15 narrow denies last (brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, multi-plan-orchestration, finishing-a-development-branch, using-git-worktrees, requesting-code-review, receiving-code-review, test-driven-development, skill-harvest, find-skills, deep-research, project-standardization, synctool-sync). Non-empty body carries the recon protocol (scope, search-before-read, verbatim quoting, web lookup with cited URLs, structured findings).
- `agents/README.md`: roster row inserted after the `planner` row; built-in-explore paragraph rewritten to describe the shadowing custom agent; `explore` appended to the `high`-effort GLM routing list.
- Root `README.md` and root `AGENTS.md`: `explore` inserted into the agent lists (after `documenter`).
- `CHANGELOG.md`: Added entry under `[Unreleased]`.
- Verifier output: `opencode agent list` exit 0 with `explore` listed; `opencode debug agent explore` resolved model `zai-coding-plan/glm-5.3-flash`, variant `high`, mode `subagent`, webfetch not denied, edit/write/patch/task denied; em-dash sweep empty; `explore` present in all three catalogs.
- Reviewer: PASS, no findings.

### Task 2: Hard-require planner delegation to explore (commit `f703f7f`)

- `agents/planner.md`: description's last sentence now reads "Delegates all recon (codebase reading and web lookup) to the explore subagent."; `tools:` gains `webfetch: false`; `permission:` gains `webfetch: deny` after the `patch:` block; "Exploration discipline" paragraph appended after the Scope-discipline paragraph, covering the whole run (pinpointing landing zones, sizing edit targets, web lookups), with the docs/artifacts and repo-context-doc exception stated.
- `commands/full-cycle.md`: step 1 phrase extended to "for codebase recon and web lookups".
- `CHANGELOG.md`: Changed entry under `[Unreleased]`.
- Verifier output: `opencode agent list` exit 0; `opencode debug agent planner` checked (see Unverified items for the synced-copy caveat; the repo file was verified by line-by-line frontmatter review: both `webfetch: false` and `webfetch: deny` present, model pin `zai-coding-plan/glm-5.3` unchanged); em-dash sweep empty.
- Reviewer: PASS, no findings.

## Standardization review

Doc-standardizer: 11/11 PASS. One quick-fix outstanding at audit time: the design and plan files under `docs/artifacts/features/explore-recon-delegation/` were untracked. RESOLVED by this docs commit, which stages the design, plan, and this report together per the AGENTS.md "Git & workflow" carve-out ("Specs, plans, reviews, and the code they describe ship together"). Task 1 and Task 2 commits were not amended.

Code-standardizer: intentionally skipped. The diff touches no source code; every changed file is Markdown (agent definitions, a command file, catalogs, changelog). The `code-standardization` audit has nothing to review.

## Documentation updates

- `agents/README.md` (agent roster catalog): new `explore` row, rewritten shadow paragraph, routing list updated. Required by the undocumented-agents-do-not-exist rule; shipped in the same commit as the agent.
- Root `README.md` and root `AGENTS.md`: `explore` added to the agent lists. Same-commit catalog rule.
- `commands/full-cycle.md`: step 1 wording aligned with the delegation rule.
- `CHANGELOG.md`: Added bullet (explore agent) and Changed bullet (planner delegation), both under `[Unreleased]`.
- Catalog drift check at close-out (this report): re-read all five files; the landed state matches every catalog promise. `explore` appears in README.md (agents paragraph), AGENTS.md (Agent definitions section), and agents/README.md (roster row, shadow paragraph, routing list); no orphaned references to the old built-in-only wording remain. No drift found.

## Verification matrix

Every requirement from the spec's Verification section:

| Requirement | Command | Result |
|---|---|---|
| Agent set parses after each frontmatter edit | `opencode agent list` | Exit 0; both `explore` and `planner` listed (after Task 1 and after Task 2) |
| `explore` resolves pinned and read-only | `opencode debug agent explore` | model `zai-coding-plan/glm-5.3-flash`, variant `high`, mode `subagent`, webfetch not denied, edit/write/patch/task denied |
| `planner` resolves with webfetch denied | `opencode debug agent planner` | CLI read the synced copy at `~/.config/opencode/agents/planner.md` (user re-sync pending); repo file (source of truth) verified by line-by-line review: `webfetch: false` and `webfetch: deny` both present, model pin unchanged |
| Em-dash scan over touched files | `git diff main..HEAD -- '*.md' \| Select-String -Pattern ([char]0x2014)` | Empty (no U+2014 in any added or changed line) |
| Catalog cross-check | `Select-String -Path README.md,AGENTS.md,agents/README.md -Pattern "explore"` | `README.md` 1 match, `AGENTS.md` 1 match, `agents/README.md` 4 matches (roster row, shadow paragraph, routing list, planner row) |

## Skills loaded

- Executor passes: followed the plan's replacement text verbatim; no skill bodies edited.
- Documenter (this report): none loaded; followed the `agents/documenter.md` definition directly.

## `ponytail:` deferrals

None. The plan was self-contained; every edit matches the plan's replacement text verbatim. No `ponytail:` comments were introduced in any file.

## Unverified items

One caveat, a sync-time issue rather than a defect: `opencode debug agent planner` resolves against the synced copy at `~/.config/opencode/agents/planner.md`, which predates this branch until the user re-syncs. The repo file (source of truth) was verified by line-by-line frontmatter review instead. The same applies to `explore`: until `agents/explore.md` is copied to `~/.config/opencode/agents/`, dispatches resolve to the opencode built-in.

## Next steps for the user

Restart opencode (agent config loads once at startup), then copy `agents/*.md` to `~/.config/opencode/agents/` to activate the new `explore` definition and the updated `planner`; until the copy lands, `explore` dispatches fall back to the built-in and the planner runs its old definition.

## Dispatch Log

| Unit | Dispatched as |
|---|---|
| Task 1: explore agent + catalogs | executor + reviewer (PASS, no findings) |
| Task 2: planner delegation enforcement | executor + reviewer (PASS, no findings) |
| Doc-standardizer audit | doc-standardizer (11/11 PASS, 1 quick-fix resolved by this commit) |
| Code-standardizer audit | skipped (markdown-only diff, no source code) |
| Execution report + spec/plan commit (this file) | documenter |

Zero oracle escalations (no task failed verification twice).
