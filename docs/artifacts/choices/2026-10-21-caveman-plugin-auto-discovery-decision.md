# Caveman plugin: directory auto-discovery

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The caveman plugin has NO entry in the config `plugin` array. opencode auto-discovers it from `~/.config/opencode/plugins/caveman/index.js` (the `skillctl sync` plugins loop drops it there).

## Why

- A config entry for an auto-discovered directory would load the plugin twice.
- A config entry with a file path is rejected by opencode v2 outright (`configured plugin path must be a directory`).
- Verified: `opencode plugin list` shows caveman loaded from the auto-discovered path with zero load failures.

## Alternatives rejected

- Register in the config array: double load, plus the v2 file-path rejection.

## Revisit when

opencode removes directory auto-discovery or adds double-load dedup; then an explicit config entry becomes the safe form.
