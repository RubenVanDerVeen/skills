# Design: Standardization review + documentation phase in plan execution

## Overview

Add two post-implementation phases to the orchestrator's plan-execution loop:

1. **Structure review** - a new `standardizer` subagent audits the executed branch against the `project-standardization` skill. Quick fixes are applied via the existing `executor` and re-checked by `reviewer` (oracle on two-strike failures, same rule as tasks).
2. **Documentation** - a new `documenter` subagent writes a persistent execution report to `docs/artifacts/reports/` and updates every catalog/doc touched by the work, then commits.

Plus: teach `project-standardization` to scaffold `docs/artifacts/reports/` alongside `specs/plans/reviews`, so the artifact convention stays consistent everywhere it is referenced.

## Background and current state

Orchestrator loop (`agents/orchestrator.md`, 6 steps): read plan and spec, maintain todos, dispatch `executor` then `reviewer` per task, escalate two-strike failures to `oracle`, keep momentum across tasks, finish with a relayed report. `edit`/`write`/`patch` are denied on the orchestrator; it dispatches and reports only.

Subagent roster today: `executor`, `reviewer`, `oracle`. The reviewer deliberately denies `project-standardization` (it reviews one task against a plan/spec, not repo-wide structure), so a dedicated structure-review agent is needed rather than overloading the reviewer.

`docs/artifacts/` currently scaffolds `{specs,plans,reviews}`. No `reports/` exists. The convention is referenced across ~8 files in `skills/rubens-project-standardization/` (artifacts.md, bootstrap.md, STANDARDS.md, three AGENTS templates, three tier references, SKILL.md body).

## Design

### Two new subagents

**`standardizer`** (mode: subagent, model: `zai-coding-plan/glm-5.2`)

Mirrors `reviewer`/`oracle` (long-horizon reasoning, cross-model against the MiniMax executor diffs). Read-only: `edit`/`write`/`patch`/`task`/`webfetch` denied; `bash` available for reading git state and running the skill's checks. Loads `project-standardization` (the one skill the reviewer denies that this agent needs). Audits the branch diff, or the whole repo when the diff is structural, against the standardization rules. Returns `PASS`, or a numbered findings list where each item names: the file/path, the rule violated, the fix, and a tag of `quick-fix` (kebab-case path, missing AGENTS section, changelog gap, missing catalog row) or `recommendation` (larger restructuring, tier graduation). Does not fix anything; returns findings to the orchestrator.

**`documenter`** (mode: subagent, model: `zai-coding-plan/glm-5.2`)

Write-capable leaf. `task`/`webfetch` denied; `bash` available (read git state, commit). `edit`/`write`/`patch` allowed to `docs/**` and root-level `*.md` (catalogs and root docs: `README.md`, `AGENTS.md`, `opencode-install.md`, `external-skills.md`, and equivalents in other repos). Loads `project-standardization` so catalog updates follow the convention. Receives the run's raw material from the orchestrator (plan + spec paths, per-task commit list, standardizer findings and what was fixed, verifier output, dispatch log), writes the execution report, updates every catalog/doc the work touched, commits as `docs:` commits, and returns the report path plus a short summary. Does not dispatch further subagents.

Write-scope rationale: the user-chosen scope is `docs/**` plus repo-root docs. Root-level `*.md` is matched with a root glob; if the matcher treats it as recursive it still only touches markdown, which is acceptable for a documentation role and still narrower than full-repo write.

### Orchestrator loop changes

Insert two phases after the current task loop (step 5, momentum) and renumber the final report:

- **New step 6, Structure review.** Dispatch `standardizer` against the branch. On findings: dispatch `executor` for the items tagged `quick-fix`, then `reviewer` to re-check the fixes. Two-strike failures on a fix escalate to `oracle`, same rule as task implementation. Items tagged `recommendation` are not auto-fixed; they roll forward into the report the documenter writes.
- **New step 7, Documentation.** Dispatch `documenter` with the run's raw material. It writes the report to `docs/artifacts/reports/`, updates every catalog/doc the work touched (README skills table, AGENTS current-skills/current-agents tables, commands sections, etc.), commits, and returns the report path plus a summary.
- **Step 8, Final report** (was step 6). Relay: branch; commits with hashes and one-line descriptions; files changed with diff stats; verifier output; skills loaded across the run; `ponytail:` deferrals; anything Unverified; the Dispatch Log now listing each task as `dispatched: executor + reviewer` or `self-implemented`, plus the standardizer and documenter dispatches; and the path to the report the documenter wrote.

Orchestrator `task:` permission block gains `standardizer: allow` and `documenter: allow` (after the broad `"*": deny`, narrow allows last, per the last-match-wins rule documented in `agents/README.md`).

### Report convention

- Location: `docs/artifacts/reports/`, mirroring the layout the repo already uses for its specs and plans (flat or topic-subfoldered). In this repo that is `docs/artifacts/reports/<topic>/YYYY-MM-DD-<slug>-report.md`.
- Filename grammar: `YYYY-MM-DD-<slug>-report.md`, matching the `YYYY-MM-DD-<topic>-<type>.md` rule from `references/artifacts.md`.
- Contents, synthesized by the documenter from the orchestrator's run material plus git state: Summary (what the plan set out, what shipped); Branch and commits (hashes + one-liners); Files changed (diff stats); Standardization review (findings, what was fixed, what remains as recommendations); Documentation updates (which catalogs/docs were updated and why); Verifier output; Skills loaded; `ponytail:` deferrals; Unverified items; Dispatch Log.

### project-standardization updates

Wherever the scaffolded set is written as `{specs,plans,reviews}`, add `reports` so the convention is consistent:

- `references/artifacts.md`: add a `## Reports` section defining `docs/artifacts/reports/YYYY-MM-DD-<topic>-report.md` as the execution-report artifact; add a reports row to the per-framework redirect table; add report production to the end of the workflow list (after review); add a reports path example.
- `references/bootstrap.md`: step 6 scaffolds `{specs,plans,reviews,reports}` (same create-on-first-write rule, never pre-create empty).
- `templates/STANDARDS.md`: add the `docs/artifacts/reports/YYYY-MM-DD-<topic>-report.md` line to the artifacts list.
- `templates/AGENTS-small.md`, `AGENTS-medium.md`, `AGENTS-large.md`: `{specs,plans,reviews}` becomes `{specs,plans,reviews,reports}` in both the path-description line and the spec/plan-driven carve-out.
- `references/small.md`, `medium.md`, `large.md`: update the `{specs,plans,reviews}` mentions to include `reports`.
- `SKILL.md` body: update the artifacts references (currently lines 41, 63, 116) to include `reports`. The frontmatter `description` is unchanged: reports do not change when the skill loads.
- `references/memory.md`: note reports as committed execution history distinct from memory (minor, one line).

### Catalog updates required in the same commit set (this repo)

Adding two agents requires, per `AGENTS.md` and `agents/README.md` rules:

- `agents/README.md`: two new rows in `## The set`; update the `/execute-plan` prose to name `standardizer` and `documenter`.
- `AGENTS.md`: the prose listing agents (currently "Custom opencode agents (`planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `oracle`)") gains `standardizer` and `documenter`.
- `commands/execute-plan.md`: add the two new phases to the End section (structure review, documentation, then the final report references the report path).
- `commands/full-cycle.md`: update step 4 prose so the orchestrator's described behavior includes the new phases.
- `agents/orchestrator.md`: body loop gains steps 6-8; `task:` permission block gains `standardizer` and `documenter` allows.
- `agents/planner.md`: minor accuracy update to step 5 summary so it names the new phases (low priority; the orchestrator's contract lives in its own file).

### Activation

opencode loads agent config once at startup (`agents/README.md`). The orchestrator executing this plan runs with the current definition and will not pick up the new steps mid-run. The new workflow is exercised on the first `/execute-plan` or `/full-cycle` after the new files are synced to `~/.config/opencode/agents/` (or `.opencode/agents/`) and opencode is restarted. Verification of this plan is therefore manual (parse checks, grep for consistency), not a live run of the new phases.

## Out of scope (YAGNI)

- No skip-keyword for the new phases (not requested). Can be added later if a plan type proves not to warrant them.
- No model or variant experiments. `standardizer` and `documenter` pin `zai-coding-plan/glm-5.2` to match `reviewer`/`oracle`.
- No change to `subagent_depth`. The new phases dispatch at the same depth as the task loop (orchestrator to subagent); the existing `>= 2` requirement still holds.
- No fix for this repo's specs/plans topic-subfolder layout deviating from the standardization skill's flat-by-default rule. That is a separate consistency concern.
- The documenter does not edit skill bodies under `skills/**`; that is executor work during task implementation. The documenter updates indexes and catalogs only.
