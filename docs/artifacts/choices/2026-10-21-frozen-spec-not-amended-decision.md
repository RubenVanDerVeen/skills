# Frozen spec not amended for the plugin rename

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The approved spec still names `plugins/caveman/plugin.js`, the v1 hook, and config-array registration. It was NOT edited after approval; the deviations (index.js rename, v2 context hook, auto-discovery, graphify drop) are recorded in the execution report and the choices records instead.

## Why

- The orchestrator froze the spec and plan at dispatch ("approved, FROZEN, do not edit"); the run treats approved documents as immutable inputs.
- The report and choices registry are the designated living record for deviations; a future reader greps the feature folder and gets both the plan-era intent and the as-built truth.

## Alternatives rejected

- Amend the spec in place with an `## Amendments` section (allowed by the artifacts convention): correct in principle, but the freeze instruction for this run chose the record-elsewhere path; an amendment pass can fold this record in if the spec is ever reopened.

## Revisit when

The vendor-external-packs spec is reopened for any reason; then fold the four deviations into an `## Amendments` section citing this record.
