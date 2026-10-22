# Caveman state-file contract

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The caveman mode contract is the file `~/.config/opencode/.caveman-mode` containing exactly one of `off`, `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`. An absent file means the base rules (full, from the caveman block in global AGENTS.md) apply; an unknown value is treated as absent. `/caveman` commands write the file; the plugin reads it each turn and never writes it.

## Why

- One flat file is the simplest persistent cross-session, cross-process channel between command (writer) and plugin (reader).
- Fail-silent on both ends: unreadable or garbage state degrades to base rules, never breaks a session.
- Fresh name, distinct from the upstream artifacts (`.caveman-active`, `.caveman-opencode-ownership.json`) that were removed.

## Alternatives rejected

- Environment variable: does not persist across sessions or processes.
- Config entry: needs an opencode restart per switch.
- Reusing upstream `.caveman-active`: couples the own plugin to upstream's ownership-manifest semantics.

## Revisit when

The level set changes, or opencode offers native per-session state the plugin can read instead.
