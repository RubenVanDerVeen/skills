# Registry location

- Date: 2026-09-24
- Status: active
- Source: docs/artifacts/features/choices-registry/2026-09-24-choices-registry-report.md

## Choice
The choices registry lives at `docs/artifacts/choices/` as a third top-level subdirectory alongside `features/` and `reviews/`, not under `features/` and not as a per-feature sibling.

## Alternatives rejected
- Under `features/` (per-feature folders): decisions span multiple features; per-feature would scatter the cross-feature lookup.
- A new top-level `decisions/` directory at repo root: all process meta-docs already live under `docs/artifacts/`; a third home breaks the layout rule.
- In-chat or memory-only: durability is the whole point.

## Revisit when
A future flow needs scoped (per-feature) choices that should not be cross-visible, OR the `docs/artifacts/` layout itself is restructured.
