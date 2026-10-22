# Follow-up task 6b beyond the plan

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

A follow-up task (6b, commit `668e852`) was added beyond the plan's seven tasks to port the caveman plugin to the opencode v2 plugin API, after an oracle consult.

## Why

- The plan's plugin contract (v1 `experimental.chat.system.transform` hook, `plugin.js` file, config-array registration) could not be met as written on opencode v2.0.32: the plugin never loaded.
- The feature's stated goal is a working minimal own plugin; closing the branch with a plugin that silently never loads would fake the deliverable.
- Process precedent: two-strike failure escalates to oracle; the executor then empirically verified the oracle's own recommendation was wrong before finding the real v2 API.

## Alternatives rejected

- Ship as planned: the core deliverable would be dead code, and verification would have caught it (making this deferred failure, not avoided failure).
- Defer the port to a future plan: leaves the branch's headline feature broken and the machine half-migrated.

## Revisit when

Never, process-wise; the pattern (verify the plugin actually loads, escalate, re-verify the fix) is the reusable lesson.
