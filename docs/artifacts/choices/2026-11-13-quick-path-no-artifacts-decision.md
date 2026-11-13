# Quick path writes no spec, plan, or report artifacts

- Date: 2026-11-13
- Status: active
- Source: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-report.md` (spec: `docs/artifacts/features/quick-fix-path/2026-11-13-quick-fix-path-design.md`, user-locked fork 2)

## Choice
The quick path produces no process artifacts: no spec, no plan, no execution report, no structure review, no choices entry. The record is git log (exactly one Conventional Commit), a `CHANGELOG.md` `[Unreleased]` entry when the target project keeps one, and the patch version bump when its `AGENTS.md` declares a canonical version source. The executor produces all of it in the same run, because no documenter follows on the quick path.

## Alternatives rejected
- Mini note file per quick fix: keeps a paper trail, but re-adds one doc per 2-line fix, the exact ceremony the path exists to remove.
- Report-only tail (full-lite): retains the disproportionate docs-to-code ratio the matrium `deb-glibc-baseline` run exposed (about 24:1).
- Choices entry per quick fix: the classification criteria already exclude anything with decision weight; a fix that deserves a decision record was never a quick fix.

## Revisit when
Quick-path fixes need after-the-fact auditing often enough that git log plus changelog stops being an adequate record, OR the single-commit rule starts hiding context the team actually misses.
