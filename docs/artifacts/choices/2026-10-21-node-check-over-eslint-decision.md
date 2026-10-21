# node --check over ESLint

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The `.githooks/pre-commit` hook syntax-checks staged JavaScript files with `node --check` (unique temp names, skipped gracefully when node is absent). No ESLint, no Prettier, no `package.json`, no `node_modules`.

## Why

- The repo's whole JS surface is 149 dependency-free lines (plugin + smoke test); a syntax gate catches the realistic failure (broken edit ships) at zero dependency cost.
- Preserves the repo's no-tooling convention: `bin/skillctl` and the hooks are dependency-free sh/grep/node.

## Alternatives rejected

- ESLint: a dependency tree for 149 lines; overkill by the ponytail standard.
- Prettier: formatting automation for two small hand-tuned files.
- `package.json` + `node_modules` + scripts: introduces a runtime/lockfile the markdown-first repo rule exists to avoid.

## Revisit when

The JS surface grows into multiple importing modules or ships to other machines; then a real linter earns its dependency cost.
