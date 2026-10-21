# subagent_depth kept despite legacy WARN

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

`subagent_depth: 3` stays in the consolidated `~/.config/opencode/opencode.jsonc` (both top-level and under `experimental`), accepting opencode v2's "unsupported legacy setting" normalization WARN on every start.

## Why

- The plan specified the value; single-pass `/full-cycle` depends on nested dispatch (planner dispatches orchestrator, which dispatches executor/reviewer), which needs `subagent_depth >= 2`.
- A WARN in the log is cheaper than breaking the dispatch chain on an assumption that v2 ignores the setting.

## Alternatives rejected

- Drop the key: contradicts the plan and risks the nested-dispatch depth the flow depends on.
- Hunt for a v2-native equivalent mid-run: scope creep; the WARN is cosmetic until verified otherwise.

## Revisit when

opencode v2 documents the native nested-dispatch setting (or confirms the depth limit is gone); then remove the legacy key and the WARN with it.
