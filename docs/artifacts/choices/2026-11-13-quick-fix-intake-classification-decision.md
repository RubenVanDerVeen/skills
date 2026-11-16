# Quick-fix intake classification in the planner pipeline

- Date: 2026-11-13
- Status: active
- Source: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-report.md` (spec: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-design.md`, user-locked fork 1)

## Choice
The planner classifies every request at intake, mirrored in `/full-cycle`: a request is a quick fix only when ALL five criteria hold (one task with one obvious fix; expected diff about 1-2 files; no design alternatives worth weighing, no new interface, API, behavior surface, or schema; one runnable verification check covers it; nothing that belongs in `docs/artifacts/choices/`). Any failing criterion, or genuine doubt, means the full pipeline. The keywords `quick` and `full` override the classification either way, parsed alongside the pre-existing `no brainstorm` and `handoff` keywords, and the planner states the chosen tier in one line so the user sees which path ran. The quick path needs `subagent_depth >= 1` only; the full pipeline keeps its `>= 2` requirement (see `2026-10-21-subagent-depth-kept-decision.md`).

## Alternatives rejected
- Keyword-only trigger (`quick` without auto-classification): predictable, but keeps the spec/plan/report overkill as the default for users who do not know the keyword; the matrium `deb-glibc-baseline` run put a 28-line CI fix through 676 lines of process docs.
- Hard line- or file-count threshold: mechanical, but gameable and stale before any code exists; the qualitative criteria age better.
- Borderline defaults to the quick path: faster, but a misclassified feature would skip the lazy-dev gate, reviewer, and choices registry with no recovery but the scope-creep stop.

## Revisit when
Misclassification shows up in practice: quick-path fixes that needed a choices entry or a reviewer, or full-pipeline runs over changes that were obvious 2-line fixes. Also if the pipeline's phase set changes enough that the criteria list stops matching it.
