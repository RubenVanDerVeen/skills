# Quick-fix fast path in the planner pipeline

Date: 2026-11-13
Status: approved (user picked all three design forks)
Supersedes: none

## Problem

The planner pipeline is monolithic: every request, regardless of size, gets brainstorm, design doc, plan, lazy-dev gate, orchestrator, documenter report, and shipper. Evidence from matrium's latest run (`deb-glibc-baseline`, 2026-11-13): a one-line CI fix (`runs-on: ubuntu-latest` to `ubuntu-22.04`, 28 changed lines in one YAML file) produced 676 lines of process docs (139 design + 300 plan + 237 report), 6 commits, and 4 plan tasks of which 3 were pure bookkeeping. Ratio ~24:1 docs-to-code.

Root cause: neither `agents/planner.md` nor `commands/full-cycle.md` has an intake gate that decides "this change needs no artifacts". The only size-relief valves (brainstorm skip, lazy-dev task collapsing, orchestrator one-line self-implement) all operate after the spec/plan/report machinery is already committed to.

## Decision (user-locked)

Three forks, all resolved to the recommended option:

1. **Classification**: auto-classification by the planner at intake, plus keyword override (`quick` forces the fast path, `full` forces the pipeline). Borderline cases default to the full pipeline.
2. **Artifacts**: none. Git log + changelog entry + patch version bump (when the target project declares a version source) are the record. No spec, plan, or report files.
3. **Review and shipping**: one executor implements, verifies, and commits. No reviewer dispatch by default. Scope creep triggers a stop-and-report; the planner converts to the full pipeline. Shipper runs after the relay, same tail as the full pipeline.

## Quick-path classification criteria

The planner classifies at intake (step 1 of its pipeline). The quick path applies only when ALL hold:

- Single task: no meaningful decomposition, one obvious fix.
- Small surface: expected diff is about 1-2 files, no new module or file expected.
- No design work: one obvious approach, no alternatives worth weighing, no new interface, API, behavior surface, or schema change.
- Cheap verification: one runnable check (existing test, lint, or build command) covers it.
- No decision weight: nothing that belongs in `docs/artifacts/choices/`.

Any criterion failing, or genuine doubt, means the full pipeline. Safe default is full.

Keywords (parsed alongside `no brainstorm` and `handoff`):
- `quick` (also matches "quick fix", "small fix" phrasing): force the quick path.
- `full`: force the full pipeline.

## Quick-path steps

1. **Classify** (intake, with keyword override). State the tier in one line in the reply ("Quick path: single executor, no spec/plan artifacts") so the user sees which path ran.
2. **Recon if needed**: one `explore` dispatch when the target file or fix site is unknown; skip when the request already names it.
3. **Dispatch one executor** with an inline task brief (no plan file). The brief names: branch name (`fix/<scope>` or `chore/<scope>` per Conventional Branch), the target file(s) and the fix, the one verification command (copied from the target project's AGENTS.md), and the bookkeeping rules below.
4. **Executor rules for a quick-fix brief**:
   - Create the branch, implement, verify, commit once with Conventional Commits (`fix(scope): ...` typically).
   - Changelog: if the target project has a `CHANGELOG.md` with an `[Unreleased]` section, add the entry line in the same commit.
   - Version: if the target project's AGENTS.md declares a version source, apply the patch bump in the same run (there is no documenter to do it later).
   - **Scope-creep stop**: if the real fix exceeds the brief (more files than named, new logic branches, new interface, second task emerging), stop before committing the expanded scope and report back what was found. The planner then converts the run to the full pipeline (spec, plan, orchestrator). This is the single escape hatch.
5. **Relay**: planner relays the executor's report (files, diff summary, verification, commit hash).
6. **Ship**: dispatch the shipper after the relay, same as the full pipeline tail (push, PR, merge question, tag/release on a merged answer). Skip when the branch carries nothing shippable.

Explicitly skipped on the quick path: spec file, plan file, lazy-dev gate (nothing to gate), orchestrator, per-task reviewer, structure review (doc/code standardizers), documenter report. Choices registry is never written on the quick path; a fix that deserves a decision record is by definition not a quick fix (consistent with the `2026-09-24-documenter-single-writer-decision`, the documenter stays the only choices writer).

## Changes

| File | Change |
|---|---|
| `agents/planner.md` | Frontmatter description gains the quick-path clause. Step 1 becomes intake classification (criteria + `quick`/`full` keywords). New quick-path step between steps 1 and 2: criteria, executor dispatch shape, scope-creep conversion, relay, shipper tail. |
| `commands/full-cycle.md` | Mirror: `quick`/`full` keywords listed; quick-path branch added to the steps; description updated. |
| `agents/executor.md` | Frontmatter description mentions quick-fix dispatch (no plan file). Body gains a short quick-fix paragraph: inline brief, branch, single commit, changelog/version rules, scope-creep stop. |
| `agents/README.md` | Planner and executor roster rows updated to mention the quick-fix fast path. |
| `README.md` | Agents paragraph gains a short clause (planner quick-fix fast path). |
| `AGENTS.md` | Same clause in the Agent definitions paragraph. |

No other agents change: orchestrator, lazy-dev, documenter, reviewer, standardizers, and shipper only run on the full path (or, for the shipper, identically on both). `/execute-plan` is untouched: the existence of a plan file implies the full path.

## Alternatives considered

- **Keyword-only trigger**: predictable but keeps the overkill as default; rejected.
- **Hard line/file threshold**: mechanical but gameable and stale before any code exists; rejected.
- **Mini note file per quick fix**: keeps a paper trail but re-adds one doc per 2-line fix; rejected.
- **Report-only tail (full-lite)**: retains the disproportionate ceremony the matrium run exposed; rejected.
- **Always one reviewer pass on quick fixes**: safer, but re-adds the dispatch the path exists to remove; the scope-creep stop plus the shipper's PR review cover it; rejected.
- **Planner self-implements quick fixes**: fastest, but the planner's edit permissions are docs/** only and it blurs role boundaries; rejected.

## Verification

- `bin/skillctl check` passes (no new skill, no frontmatter rule violations).
- Frontmatter of both edited agent files stays well-formed (paired `---` fences, description present). `opencode agent list` cannot verify this: it reads synced config dirs, not the repo source.
- `bin/skillctl sync --check` reports the agent files as STALE/MISSING for the global config dir (expected until the user syncs; the report lists `bin/skillctl sync` as the next step).
- Manual read-through: every quick-path mention is consistent across the six files (same criteria, same keywords, same scope-creep rule).

## Out of scope

- No changes to target projects (matrium et al.); they inherit the behavior via the synced planner/executor.
- No new agent, no new command, no new skill.
- No line-count thresholds or enforcement tooling.
