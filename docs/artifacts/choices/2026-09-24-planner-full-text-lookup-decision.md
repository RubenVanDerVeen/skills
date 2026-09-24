# Planner full-text lookup

- Date: 2026-09-24
- Status: active
- Source: docs/artifacts/features/choices-registry/2026-09-24-choices-registry-report.md

## Choice
The planner greps `docs/artifacts/choices/` full-text across all files when checking for prior decisions; correctness does not depend on `index.md` staying fresh. The index is a human-scannable view maintained by the documenter in the same write pass.

## Alternatives rejected
- Index-only grep (parse the table rows): the index can be stale, wrong, or missing; correctness would silently fail.
- Database or tooling-backed lookup: the registry is markdown by design (durable, greppable, git-diffable); tooling is over-engineering for the use case.
- No lookup step (rely on the planner to remember): sessions do not carry forward.

## Revisit when
The registry grows past a few hundred entries and full-text grep becomes the slow step, OR the convention migrates off plain markdown.
