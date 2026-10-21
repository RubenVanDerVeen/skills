# Vendor all four external packs

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

Own copies of all four external behavior packs live in this repo and arrive via `bin/skillctl sync`: the superpowers remainder (`using-superpowers`, `verification-before-completion`), caveman (skill + six commands), stop-slop (skill + references), ponytail (core skill). All external installs of the four are retired.

## Why

- The packs encode opinion (prose style, process discipline, YAGNI philosophy), not tooling; depending on upstream means another person's decisions steer the agent.
- Precedent: 2026-09-24 five superpowers process skills were forked in (commit `9b0d4c4`); this finishes that pivot.
- Status quo rot: duplicate superpowers copies both loadable, broken cavecrew refs, fragile ponytail clone, configs split across two files.

## Alternatives rejected

- Keep external installs: the rot list above, plus silent upstream drift.
- Vendor only one or two packs: each of the four is load-bearing for this user's daily flow.

## Revisit when

Upstream ships a change the user genuinely wants (then cherry-pick it into the vendored copy with the adaptation rules), or owning the copies costs more than the drift risk (then reconsider sourcing).
