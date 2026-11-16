# Plan file implies full path: /execute-plan and the other agents stay untouched

- Date: 2026-11-13
- Status: superseded by 2026-11-16-single-commit-fixes-direct-to-main-decision.md
- Source: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-report.md` (spec: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-design.md`, Changes and Out-of-scope sections)

## Choice
The quick path lives in exactly three behavior files (`agents/planner.md`, `commands/full-cycle.md`, `agents/executor.md`) plus their catalog rows (`agents/README.md`, `README.md`, `AGENTS.md`). No other agent definition changed: orchestrator, lazy-dev, reviewer, documenter, standardizers run on the full path only, and the shipper runs identically on both. `/execute-plan` is deliberately untouched: the existence of a plan file implies the full pipeline, so the command needs no quick-path branch.

Superseded in part by `2026-11-16-single-commit-fixes-direct-to-main-decision.md`: the shipper no longer runs on both paths, it is the full-path tail, and a quick fix lands as one commit on the default branch with no branch and no PR.

## Alternatives rejected
- Mirror the quick-path branch into `/execute-plan`: dead logic; no plan file ever exists on the quick path.
- A dedicated quick-fix agent: one more definition to sync and catalog for a flow that is deliberately a single executor dispatch.

## Revisit when
A flow emerges that executes plan files that are quick-fix sized, OR the quick path grows logic beyond what one executor brief can carry.
