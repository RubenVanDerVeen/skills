# skillctl plugins loop shape

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The `bin/skillctl sync` plugins loop is `mirror plugins "$g" "$oc/plugins"` per plugin folder, matching the neighbouring skills loop exactly. The plan's version had a redundant `mkdir -p "$oc/plugins"` and a trailing-slash trim (`"${g%/}"`); both were dropped in `e6b18cf`.

## Why

- `mirror` already creates its destination; the pre-create was dead code.
- The glob `"$REPO_ROOT"/plugins/*/` yields paths the skills loop consumes untrimmed; matching it keeps the two loops uniform.
- Plugins are opencode-only; no Claude Code branch, same as agents.

## Alternatives rejected

- Keep the plan's pre-create + trim: two lines that do nothing the mirror engine does not already do.

## Revisit when

`mirror` semantics change (dest no longer auto-created), or plugins need per-agent targeting.
