# graphify plugin registration dropped

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The graphify plugin registration was dropped during config consolidation, not migrated. The plan had specced re-registering `./plugins/graphify.js` in the consolidated config. The graphify skill and CLI are untouched; `/graphify` stays available through the skill.

## Why

- The upstream `graphify.js` is v1-shaped: opencode v2 refuses it (`Plugin must export a default definition with an id and an effect or setup function`).
- It never loaded, not even under the old `~/.opencode/opencode.json` registration, so dropping it regresses nothing.
- Porting a third-party plugin to v2 means owning code this repo does not maintain; violates the freeze-and-own scope (graphify stays external by decision).

## Alternatives rejected

- Migrate the registration as the plan specced: a config entry that fails to load on every start.
- Port graphify.js to the v2 API: owning external tool code for zero added function (the skill covers `/graphify`).

## Revisit when

graphify ships a v2-native plugin; then register it in `~/.config/opencode/opencode.jsonc` like opencode-see-image.
