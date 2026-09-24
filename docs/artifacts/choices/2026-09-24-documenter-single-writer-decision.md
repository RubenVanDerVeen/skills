# Documenter single writer

- Date: 2026-09-24
- Status: active
- Source: docs/artifacts/features/choices-registry/2026-09-24-choices-registry-report.md

## Choice
The documenter subagent is the only writer of the choices registry; it writes entries at plan close-out from run material, and skips silently when nothing qualifies.

## Alternatives rejected
- Multi-writer (each agent writes its own entries): scattered writers drift the threshold rule and the template; one writer keeps the convention enforced.
- Planner writes entries: the planner has no run-material (no per-task defaults, no executor notes) and would write stale entries.
- A separate registry-writer agent: adding an agent for a doc-only task is over-engineering; the documenter already runs at the same close-out point.

## Revisit when
A future flow runs without a documenter step, OR the documenter's write scope changes materially.
