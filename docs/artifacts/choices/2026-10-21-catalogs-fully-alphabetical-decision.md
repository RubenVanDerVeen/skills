# Catalog tables fully alphabetical

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

Both skill catalog tables (`README.md` `## Skills`, `AGENTS.md` `## Current skills`) were sorted alphabetically across ALL rows (24 each) during the structure-review pass, not only the rows this branch added.

## Why

- The tables had accumulated out-of-order rows from earlier additions; half-sorted tables invite further disorder and churn diffs on every future insert.
- Alphabetical is the rule both catalogs already declare ("one row per skill, alphabetical"); the sort makes the declared rule true.

## Alternatives rejected

- Sort only the new rows: leaves the declared convention violated for pre-existing rows.

## Revisit when

Never, conventionally; the row order is now maintained by the rule, and the pre-commit catalog check (C6) guards membership.
