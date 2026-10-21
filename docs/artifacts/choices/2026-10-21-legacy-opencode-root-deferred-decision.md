# Legacy ~/.opencode/ root removal deferred

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

`~/.opencode/package.json` and `~/.opencode/node_modules/` were left in place (the plan defers their removal), and with them `~/.opencode/plugins/graphify.js`, which opencode still probes and refuses on every start, logging a load-failure WARN.

## Why

- The plan explicitly scoped npm-artifact removal out (harmless leftovers, removal is a follow-up).
- Deleting the legacy root mid-run adds teardown risk for zero functional gain; the consolidated config already ignores it.

## Alternatives rejected

- Delete `~/.opencode/` wholesale during Task 6: outside the plan's teardown list; a machine-state chore, not a repo change.

## Revisit when

The follow-up cleanup runs: delete `~/.opencode/package.json`, `node_modules/`, and `plugins/graphify.js` to silence the start WARN; documented in `opencode-install.md` step 2.
