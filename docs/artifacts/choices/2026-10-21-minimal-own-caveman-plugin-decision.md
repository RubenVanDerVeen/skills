# Minimal own caveman plugin

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The caveman per-turn injection is a minimal own plugin (`plugins/caveman/index.js`, 73 lines, node stdlib only, no dependencies) instead of keeping the 1090-line upstream JS plugin.

## Why

- Only one upstream behavior is needed: read the mode state file and inject the matching rules line each turn.
- Upstream also does command parsing, ownership manifests, and session-detection heuristics, all unused here.
- The repo is markdown-first with a minimal tooling-exception list; 73 dependency-free lines fit it.

## Alternatives rejected

- Keep the upstream plugin: 1090 lines of unused machinery, cavecrew coupling, and v1-only API.
- No plugin at all: the base rules block in global AGENTS.md is static; `/caveman off` and per-level reinforcement need per-turn injection.

## Revisit when

opencode gains native mode/state support, or a level needs per-message logic beyond injecting a static line.
