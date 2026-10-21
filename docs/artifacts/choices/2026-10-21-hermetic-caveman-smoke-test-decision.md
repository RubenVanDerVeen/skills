# Hermetic caveman smoke test

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The plugin smoke test (`plugins/caveman/test.mjs`) is hermetic: it points `os.homedir()` at a temp directory by setting `process.env.HOME` before importing the plugin, so the real `~/.config/opencode/.caveman-mode` is never read or written.

## Why

- The test writes state values (ultra, off, garbage, absent) to exercise every branch; doing that against the real home dir would clobber the user's active mode.
- `process.env.HOME` redirection is node-stdlib behavior; zero production code changes needed.

## Alternatives rejected

- Add an env-var override to the plugin itself (e.g. `CAVEMAN_STATE_PATH`): production API surface existing only for tests.
- Test against the real file: mutates user state; the original version of the test did exactly this and was fixed in `e92fc0d`.

## Revisit when

The plugin grows real configuration (then prefer dependency injection over env tricks), or the test outgrows a single file.
