# Single consolidated opencode config

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

All opencode configuration lives in one file, `~/.config/opencode/opencode.jsonc`. Its `plugin` array holds only `opencode-see-image@1.4.0`; the caveman plugin is auto-discovered from `~/.config/opencode/plugins/caveman/index.js` with no config entry. The legacy `~/.opencode/opencode.json` is deleted. Broken cavecrew references are dropped.

## Why

- Split registrations across `~/.config/opencode/opencode.jsonc` and `~/.opencode/opencode.json` were the status-quo rot: stale superpowers and ponytail entries, old graphify registration, double-maintenance.
- opencode v2 rejects FILE paths in the config `plugin` array (`configured plugin path must be a directory`), so path-based registration of the own plugin was never an option on v2.

## Alternatives rejected

- Keep both config files: split-brain, the exact rot the feature removed.
- Register the caveman plugin in the config array: rejected by v2 (file path) and would double-load it (directory entry plus auto-discovery).

## Revisit when

opencode changes its plugin discovery semantics, or a plugin needs an explicit version pin that auto-discovery cannot express.
