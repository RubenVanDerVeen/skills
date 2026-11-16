# Quick path: one executor, no reviewer, scope-creep stop

- Date: 2026-11-13
- Status: active
- Source: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-report.md` (spec: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-design.md`, user-locked fork 3)

## Choice
On the quick path the planner dispatches exactly one executor with an inline brief (branch name, target files, the fix, one verification command) and no reviewer. Skipped: the lazy-dev gate (nothing to gate), the orchestrator, the per-task reviewer, the structure review, and the documenter report. The single safety valve is the scope-creep stop: when the real fix exceeds the brief (more files than the brief names, new logic branches, a new interface, a second task emerging), the executor stops before committing the expanded scope and reports back, and the planner converts the run to the full pipeline with the findings as recon input. Never silently expand a quick fix. The shipper tail (PR, merge question, tag and release) runs after the relay on both paths. The choices registry is never written on the quick path; `2026-09-24-documenter-single-writer-decision.md` stands un-superseded: its revisit condition (a flow without a documenter step) is now met by the quick path, and its substance holds because no other writer exists.

## Alternatives rejected
- Always one reviewer pass on quick fixes: safer, but re-adds the dispatch the path exists to remove; the scope-creep stop plus the shipper's PR review cover the risk.
- Planner self-implements quick fixes: fastest, but the planner's edit permissions are `docs/**` only and it blurs role boundaries.
- Executor silently expands a small fix to finish the job: one tidy commit, but it carries unreviewed scope the brief never named; hence the hard stop instead.

## Revisit when
Scope creep keeps being discovered only after commit, or misclassified quick-path fixes need rework a reviewer would have caught. Also if the executor's single-commit constraint proves too tight for legitimate small fixes.
