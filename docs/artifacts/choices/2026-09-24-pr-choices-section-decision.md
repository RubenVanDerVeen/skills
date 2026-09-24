# PR Choices section

- Date: 2026-09-24
- Status: active
- Source: docs/artifacts/features/choices-registry/2026-09-24-choices-registry-report.md

## Choice
PR descriptions gain a `## Choices` section between `## Verification` and `## Docs`, listing new or updated `docs/artifacts/choices/` decision files with a one-line why each; the section says `None` when nothing qualifies (matches the pr-description skill's "Every section present; write None" rule).

## Alternatives rejected
- Inline in `## What changed and why`: choices are metadata about the run, not the diff; mixing them with the diff summary hides them.
- In the commit body: commit bodies do not reach PR reviewers consistently and are not standardized.
- In a separate `DECISIONS.md` at repo root: it would be a third home for the same content.

## Revisit when
PR tooling changes (e.g. the pr-description skill is replaced), OR the registry moves to a different surface.
