# External packs stay external

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

graphify, opencode-see-image, vercel-labs/agent-skills, markitdown, and open-code-review stay external: cataloged in `external-skills.md`, not vendored into this repo.

## Why

- graphify is useless without its CLI binary; the skill is a thin skin over the tool.
- opencode-see-image is npm plugin code, not prose; pinning `@1.4.0` in the config is the right integration point.
- vercel-labs/agent-skills moves fast and encodes Vercel-stack opinions; a frozen copy would rot in months.
- markitdown and open-code-review are CLIs, not skills; out of scope by kind.

## Alternatives rejected

- Vendor them too: would pull code and binaries into a markdown-first repo and break the stack rule; the vercel pack drifts too fast to freeze.

## Revisit when

An external source stabilizes AND becomes opinion-shaped (prose, process) rather than tooling; then it joins the vendoring pattern.
