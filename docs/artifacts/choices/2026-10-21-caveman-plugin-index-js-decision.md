# Caveman plugin file: index.js

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The plugin entry file is `plugins/caveman/index.js`, renamed from the spec's `plugins/caveman/plugin.js` during implementation.

## Why

- opencode v2 resolves a plugin DIRECTORY through a `server.*` or `index.*` entry file; a directory with neither is skipped silently.
- `index.js` is the documented default; no config or convention needed beyond the file name.

## Alternatives rejected

- Keep `plugin.js` per the frozen spec: the plugin directory is skipped silently on v2; the feature would not load.
- `server.js`: equally valid per v2, but `index.js` is the conventional default and matches the docs.

## Revisit when

opencode changes directory resolution (then rename and update `bin/skillctl`'s plugins loop assumptions, which copy folders wholesale and are name-agnostic).
