# Freeze-and-own per pack

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

Approach A: each pack is vendored as an adapted frozen copy with attribution lines (`Adapted from <source>`), keeping its own identity and trigger surface. No unified rewrite or merge of the packs.

## Why

- Skill descriptions are a public interface: agents load by description-match, and merged/rewritten descriptions break trigger continuity.
- Per-pack copies keep provenance greppable and upstream changes diffable.

## Alternatives rejected

- Approach B, unified rewrite/merge into one "own style" skill: rejected in the brainstorm session; destroys trigger continuity and mixes four distinct concerns (output style, prose hygiene, YAGNI, process discipline).

## Revisit when

Two vendored packs grow overlapping, contradictory rules that a merge would genuinely simplify.
