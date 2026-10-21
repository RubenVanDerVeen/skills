# Caveman plugin: opencode v2 context hook

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

The caveman plugin injects its mode line through the opencode v2 API: `ctx.session.hook("context", event => event.system.push({type:"text", text}))`, with a default export of `{id, setup}`. Documented at https://opencode.ai/v2/docs/build/plugins. Verified by observing the mode line in the outgoing model request's system instructions and an ultra-vs-off behaviour probe.

## Why

- The plan's v1 hook `experimental.chat.system.transform` does not exist on opencode v2.0.32; a plugin using it silently never loads.
- The oracle consult recommended `aisdk.hook("language")`; the executor empirically disproved it (zero firings across probes).
- The `context` session event is the documented v2 way to mutate system instructions per turn.

## Alternatives rejected

- Keep the v1 hook per plan: plugin never loads; the feature's core deliverable would be dead code.
- `aisdk.hook("language")` per the oracle: sounded right, fired never; falsified by evidence.

## Revisit when

opencode v2 changes the session context event shape or documents a purpose-built system-prompt hook; then re-verify with the same probe method (observe the outgoing request, count hook firings).
