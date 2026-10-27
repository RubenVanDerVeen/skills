# Choices index

One row per recorded decision. Files: `YYYY-MM-DD-<slug>-decision.md`. Convention: `skills/rubens-project-standardization/references/artifacts.md`.

| Date | Decision | Status | File |
|------|----------|--------|------|
| 2026-09-24 | Choices registry lives at `docs/artifacts/choices/`, third top-level subdirectory alongside `features/` and `reviews/` | active | 2026-09-24-registry-location-decision.md |
| 2026-09-24 | Documenter subagent is the only writer of the choices registry; writes at close-out from run material | active | 2026-09-24-documenter-single-writer-decision.md |
| 2026-09-24 | Planner greps `docs/artifacts/choices/` full-text across all files; correctness does not depend on `index.md` staying fresh | active | 2026-09-24-planner-full-text-lookup-decision.md |
| 2026-09-24 | PR descriptions gain a `## Choices` section between `## Verification` and `## Docs`; `None` when nothing qualifies | active | 2026-09-24-pr-choices-section-decision.md |
| 2026-09-27 | Release bodies use one template, three copy sites (`chore(release)` commit body, tag annotation, Release notes); `release-description` skill is the source of truth | active | 2026-09-27-release-description-template-decision.md |
| 2026-09-29 | General standards check CLI lives out-of-tree as `Tools/stdctl` with PATH-symlink distribution; skills repo markdown-only rule preserved, `skillctl` untouched | active | 2026-09-29-stdctl-decision.md |
| 2026-10-13 | academic-writing-pro vocab suppression is line-granular (accept suppresses, reject escalates per line); flat `vocab/*.txt` data files partially supersede v1 non-goal 3 (no config file) | active | 2026-10-13-academic-writing-pro-vocab-line-granularity-decision.md |
| 2026-10-21 | All four external behavior packs (superpowers remainder, caveman, stop-slop, ponytail) are vendored into this repo via `skillctl sync`; external installs retired | active | 2026-10-21-vendor-all-four-packs-decision.md |
| 2026-10-21 | Vendoring uses Approach A: freeze-and-own adapted copies per pack with attribution; unified rewrite/merge (Approach B) rejected to preserve trigger continuity | active | 2026-10-21-freeze-and-own-per-pack-decision.md |
| 2026-10-21 | Caveman per-turn injection is a minimal own plugin (73 lines, node stdlib), not the 1090-line upstream plugin | active | 2026-10-21-minimal-own-caveman-plugin-decision.md |
| 2026-10-21 | Superpowers scope: only `using-superpowers` + `verification-before-completion` vendored (7 of 15 upstream skills); other 8 stay unvendored | active | 2026-10-21-superpowers-two-leftovers-scope-decision.md |
| 2026-10-21 | One opencode config (`~/.config/opencode/opencode.jsonc`); plugin array holds only see-image; caveman auto-discovered; legacy config deleted; cavecrew refs dropped | active | 2026-10-21-single-opencode-config-decision.md |
| 2026-10-21 | Cavecrew dropped entirely; investigator/builder/reviewer roles covered by own explore/executor/reviewer agents | active | 2026-10-21-cavecrew-dropped-decision.md |
| 2026-10-21 | graphify, opencode-see-image, vercel-labs/agent-skills, markitdown, open-code-review stay external (tooling or fast-moving, not opinion prose) | active | 2026-10-21-external-packs-stay-external-decision.md |
| 2026-10-21 | Caveman state contract: `~/.config/opencode/.caveman-mode` with `off\|lite\|full\|ultra\|wenyan-*`; absent file = base rules; unknown value treated as absent | active | 2026-10-21-caveman-state-file-contract-decision.md |
| 2026-10-21 | Caveman plugin uses the opencode v2 `ctx.session.hook("context")` API; v1 hook absent on 2.0.32, oracle's `aisdk.hook("language")` empirically disproven | active | 2026-10-21-caveman-plugin-v2-context-hook-decision.md |
| 2026-10-21 | Caveman plugin registered via directory auto-discovery (no config entry) to avoid a double load | active | 2026-10-21-caveman-plugin-auto-discovery-decision.md |
| 2026-10-21 | Plugin file is `index.js` (renamed from spec's `plugin.js`): opencode v2 resolves plugin directories via `server.*` or `index.*` only | active | 2026-10-21-caveman-plugin-index-js-decision.md |
| 2026-10-21 | graphify plugin registration dropped, not migrated (v1-shaped, never loaded on v2); `/graphify` stays available through the skill and CLI | active | 2026-10-21-graphify-plugin-dropped-decision.md |
| 2026-10-21 | Legacy `~/.opencode/` root (package.json, node_modules, plugins/graphify.js) left in place; its start WARN accepted; removal deferred | active | 2026-10-21-legacy-opencode-root-deferred-decision.md |
| 2026-10-21 | `subagent_depth` kept in the consolidated config despite v2's unsupported-legacy-setting WARN (nested dispatch depends on it) | active | 2026-10-21-subagent-depth-kept-decision.md |
| 2026-10-21 | Caveman smoke test is hermetic via `process.env.HOME` temp dir; no production override added | active | 2026-10-21-hermetic-caveman-smoke-test-decision.md |
| 2026-10-21 | Pre-commit `node --check` stanza for staged JS instead of ESLint/Prettier/package.json (149 dependency-free lines) | active | 2026-10-21-node-check-over-eslint-decision.md |
| 2026-10-21 | skillctl plugins loop mirrors the skills loop shape (`mirror plugins "$g" "$oc/plugins"`); redundant pre-create and slash-trim dropped | active | 2026-10-21-skillctl-plugins-loop-shape-decision.md |
| 2026-10-21 | Both catalog tables sorted alphabetically across all rows (24 each), not only branch-added rows | active | 2026-10-21-catalogs-fully-alphabetical-decision.md |
| 2026-10-21 | Follow-up task 6b added beyond the plan's seven tasks: the plugin contract was unmeetable on opencode v2.0.32 as written | active | 2026-10-21-followup-task-v2-port-decision.md |
| 2026-10-21 | Frozen spec keeps naming `plugin.js`; deviations recorded in report + choices, spec not edited | active | 2026-10-21-frozen-spec-not-amended-decision.md |
| 2026-10-27 | Agent-written PR and release description bodies use one source line per paragraph and bullet (the renderer wraps); PR bodies link commits as markdown links, never bare or backticked shas | active | 2026-10-27-pr-body-no-hard-wrap-decision.md |
