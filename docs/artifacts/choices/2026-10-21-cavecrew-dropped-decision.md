# Cavecrew dropped entirely

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The caveman pack's cavecrew companion (investigator/builder/reviewer agents and commands) was dropped entirely, not vendored and not kept installed.

## Why

- User confirmed non-use in the design session.
- Its roles are already covered by this repo's own agents: `explore` (investigator/recon), `executor` (builder), `reviewer` (reviewer).
- The installed copy referenced agents that do not exist on this machine (broken refs were part of the rot list).

## Alternatives rejected

- Vendor cavecrew: dead weight duplicating the own agent roster.
- Leave it installed: broken references in `~/.config/opencode/`.

## Revisit when

A workflow genuinely needs a dedicated investigator/builder/reviewer trio distinct from the own agents (unlikely; the own roster is pinned per role already).
