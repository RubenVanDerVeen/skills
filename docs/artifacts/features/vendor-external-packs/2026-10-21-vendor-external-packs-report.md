# Vendor External Packs Execution Report

Date: 2026-10-21
Plan: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-plan.md`
Spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`
Branch: `feat/vendor-external-packs` (base `main`)

## Summary

Branch `feat/vendor-external-packs` vendored the four external packs that steer agent behavior into this repo: `using-superpowers` and `verification-before-completion` (superpowers leftovers), `caveman` (skill plus six `/caveman-*` commands plus a minimal own plugin), `stop-slop` (skill plus three `references/` files), and `ponytail` (core philosophy skill only). The external installs were retired: superpowers plugin registration and npm cache, the caveman npx pack, the stop-slop symlink, the ponytail clone. Machine-side opencode config was consolidated into one file, `~/.config/opencode/opencode.jsonc`. Mid-run, the caveman plugin had to be rewritten onto the opencode v2 plugin API (follow-up task 6b) because the plan's v1 hook contract never loaded on opencode 2.0.32. Aggregate diff: 27 files, +1963 / -79 lines. The repo is unversioned (no `### Versioning` in AGENTS.md): no bump, no release, no PR.

## Branch and commits

14 execution commits before close-out (1 bootstrap + 6 plan tasks + 1 follow-up task + 4 quick-fix pass + 2 review-nit cleanup), plus this documenter pass (execution report, 20 choices records, catalog and doc sweep).

| Hash | Task | Subject | Stats |
|---|---|---|---|
| `cb6ff80` | bootstrap | docs(artifacts): add vendor-external-packs spec and plan | 2 files, +886 |
| `6d3efc0` | 1 | feat(skills): vendor using-superpowers and verification-before-completion from obra/superpowers | 5 files, +186/-1 |
| `07ff7e7` | 2 | feat(skills): vendor caveman skill and command pack | 10 files, +84/-1 |
| `648c294` | 3 | feat(skills): vendor stop-slop prose-control skill | 7 files, +391/-1 |
| `fb76c06` | 4 | feat(skills): vendor ponytail core philosophy skill, repoint lazy-dev lens | 4 files, +116/-1 |
| `553b486` | 5 | feat(plugin): add minimal caveman mode plugin and skillctl plugins sync | 4 files, +111/-1 |
| `12553c2` | 6 | docs(skills): consolidate opencode config to one file, retire external pack installs | 1 file, +52/-32 |
| `668e852` | 6b (follow-up) | fix(plugin): port caveman mode plugin to the opencode v2 plugin API | 6 files, +95/-60 |
| `e92fc0d` | quick-fix | fix(plugin): make the caveman smoke test hermetic | 1 file, +18/-4 |
| `e6b18cf` | quick-fix | fix(skillctl): drop the redundant plugins dir pre-create in sync | 1 file, +1/-2 |
| `434907d` | quick-fix | ci(githooks): syntax-check staged JavaScript in the pre-commit hook | 2 files, +33/-5 |
| `dc51b8e` | quick-fix | docs(skills): align catalogs, changelog and install docs with the vendored packs | 7 files, +54/-41 |
| `f683291` | nit cleanup | fix(githooks): give the staged JavaScript check unique temp names | 1 file, +12/-6 |
| `83014c8` | nit cleanup | docs(skills): clean up review nits in the workflow and catalogs | 3 files, +3/-3 |
| (this pass) | close-out | documenter: execution report, 20 choices records, catalog and doc sweep | see Documentation updates |

The plan's seven tasks map: cb6ff80 bootstrap, `6d3efc0` Task 1, `07ff7e7` Task 2, `648c294` Task 3, `fb76c06` Task 4, `553b486` Task 5, `12553c2` Task 6, Task 7 verification-only (no commit). Task 6b and the two review passes are additions beyond the plan; see Deviations.

## Files changed

Aggregate `git diff --stat main..HEAD`: 27 files, +1963 / -79. Grouped by task:

- Bootstrap (`cb6ff80`): design spec (+134), plan (+752).
- Task 1 superpowers leftovers (`6d3efc0`): `skills/using-superpowers/SKILL.md` (+59), `skills/verification-before-completion/SKILL.md` (+122); catalog rows in `README.md`, `AGENTS.md`; `external-skills.md` superpowers status.
- Task 2 caveman pack (`07ff7e7`): `skills/caveman/SKILL.md` (+45), six `commands/caveman*.md` (+34 total); catalog rows; `external-skills.md` caveman status.
- Task 3 stop-slop (`648c294`): `skills/stop-slop/SKILL.md` (+65), `references/phrases.md` (+128), `references/structures.md` (+134), `references/examples.md` (+59); catalog rows; machine symlink swap (outside repo).
- Task 4 ponytail (`fb76c06`): `skills/ponytail/SKILL.md` (+110); catalog rows; `external-skills.md` ponytail entry.
- Task 5 plugin + sync (`553b486`): `plugins/caveman/plugin.js` (later renamed `index.js`), `plugins/caveman/test.mjs`, `bin/skillctl` (+5, plugins mirror loop), `AGENTS.md` stack + layout tree.
- Task 6 config consolidation (`12553c2`): `opencode-install.md` rewritten (+52/-32); machine state (outside repo): single `opencode.jsonc`, old config, clone, caches, cavecrew removed.
- Task 6b v2 port (`668e852`): `plugins/caveman/index.js` (rewritten, 73 lines final), `plugins/caveman/test.mjs`, `skills/caveman/SKILL.md`, `AGENTS.md`, `external-skills.md`, `opencode-install.md`.
- Quick-fix pass (`e92fc0d`, `e6b18cf`, `434907d`, `dc51b8e`) and nit cleanup (`f683291`, `83014c8`): hermetic smoke test, simplified skillctl loop, pre-commit `node --check` stanza, then the doc alignment batch (`CHANGELOG.md` +8, `STANDARDS.md`, `docs/workflows/workflow.md`, `README.md`, `AGENTS.md`, `external-skills.md`, `opencode-install.md`) and two small polish commits.

## Deviations from the plan

1. **Follow-up task 6b (`668e852`), beyond the plan's 7 tasks.** The plan specced the caveman plugin against the opencode v1 API. On the installed opencode v2.0.32 it never loaded: the config `plugin` array rejects FILE paths (`configured plugin path must be a directory`), v2 requires a default export of `{id, setup}`, and the v1 hook `experimental.chat.system.transform` does not exist in v2. An oracle consult recommended the `aisdk.hook("language")` AI SDK wrapper, but the executor empirically disproved it (zero firings) and found the real v2 API (`ctx.session.hook("context", event => event.system.push({type:"text", text}))`, documented at https://opencode.ai/v2/docs/build/plugins). The rewrite was verified: the mode line was observed in the outgoing model request's system instructions, and an ultra-vs-off behaviour probe showed terse vs normal replies.
2. **Plugin file renamed `plugins/caveman/plugin.js` to `plugins/caveman/index.js`.** opencode v2 resolves a plugin DIRECTORY through `server.*` or `index.*`; a directory with neither is skipped silently. The frozen design spec still names `plugin.js`; the spec was not edited, the rename is recorded here and in the choices record.
3. **Plugin registration moved from the config array to auto-discovery.** The consolidated config's `plugin` array holds only `opencode-see-image@1.4.0`; the caveman plugin is auto-discovered from `~/.config/opencode/plugins/caveman/index.js` with no config entry (a config entry would double-load it).
4. **The graphify plugin registration was dropped, not migrated.** The upstream `graphify.js` is v1-shaped and opencode v2 refuses it (`Plugin must export a default definition with an id and an effect or setup function`); it never loaded, not even under the old `~/.opencode/opencode.json` registration, so nothing regressed. The graphify skill and CLI are untouched and `/graphify` stays available through the skill.
5. **Extra doc edits inside Task 6** (the stop-slop npx step retired, the frontmatter/Overview/When-to-use wording split, the `## Verify` ponytail claim, the graphify copy instruction removed) were authorized by the orchestrator: the plan's Step 4 list did not name them, but the change made them false.
6. **Machine state left in place on purpose**: `~/.opencode/package.json` and `~/.opencode/node_modules/` (the plan defers their removal), and therefore `~/.opencode/plugins/graphify.js`, which still logs a load-failure WARN on every opencode start. `subagent_depth` also stays in the consolidated config as the plan specified, even though opencode v2 logs an "unsupported legacy setting" normalization WARN for it.
7. **`.claude/settings.local.json`** (untracked, machine-local, predates the run) was never staged or touched.

## Standardization review

Both standardizers ran concurrently after the task loop.

**doc-standardizer findings (all branch-caused, all fixed in `dc51b8e` and `83014c8`):**

- `CHANGELOG.md` had no entry for the vendoring: Added/Changed entries added.
- README install quick-start did not name the sync command: now `bin/skillctl sync --agent opencode`.
- `docs/workflows/workflow.md` ponytail + caveman entries and the config path corrected.
- `external-skills.md` Sources-table caveman row and ponytail entry corrected.
- README external-skills bullets trimmed to the genuinely external packs.
- `STANDARDS.md` tooling exception + layout tree updated for the plugin.
- `AGENTS.md` command tree + slash-command examples list updated with the six caveman commands.
- `AGENTS.md` "four kinds of content" / "two exceptions" wording fixed (plugins are the fourth kind; the stack has two tooling exceptions).
- `opencode-install.md` graphify leftover wording corrected.
- Both catalog tables sorted alphabetically (24 rows each), not just the new rows.
- `AGENTS.md` Verify-section claim corrected; `external-skills.md` see-image step reference corrected; `opencode-install.md` `.gitattributes` claim corrected; `opencode-install.md` Verify agent list completed with `lazy-dev` and `explore`.

**code-standardizer findings (all fixed in `e92fc0d`, `e6b18cf`, `434907d`, `f683291`):**

- Smoke test made hermetic: temp HOME via `process.env.HOME`, the real `~/.config/opencode/.caveman-mode` is never touched.
- `.githooks/pre-commit` gained a `node --check` stanza for staged JavaScript that skips gracefully when node is absent (unique temp names after `f683291`).
- `bin/skillctl` dropped the redundant `mkdir -p "$oc/plugins"` and the trailing-slash trim in the plugins loop.
- Explicitly rejected as over-engineering: ESLint / Prettier / a `package.json` / `node_modules` for 149 dependency-free lines.

**What remains:** the punch-list items below (pre-existing rot, not branch-caused); of those, this close-out fixed three and left one plus the diagram redraw. No branch-caused finding remains open.

## Documentation updates

Branch-side (task commits): catalog rows shipped same-commit with every new skill (README `## Skills`, AGENTS.md `## Current skills`, both now 24 rows alphabetical); `external-skills.md` gained Status lines for the four forked packs; `opencode-install.md` rewritten around the single-config layout and the sync-based installs; `CHANGELOG.md` gained the Added/Changed entries; `STANDARDS.md` and `docs/workflows/workflow.md` aligned.

Close-out (this documenter pass):

- `docs/artifacts/choices/`: 20 new decision records plus `index.md` rows (see Choices).
- `docs/workflows/workflow.md`: agent count corrected to twelve and `explore` + `lazy-dev` added to the roster table (source: `agents/README.md`); section 2 process-skill list corrected to the seven actually vendored skills; uninstalled `find-skills` bullet removed; graphify bullet no longer claims the dead nudge-hook plugin; `/execute-plan` row no longer names the unvendored `subagent-driven-development` skill; snapshot date bumped to 2026-10-21.
- `agents/README.md`: homelab MCP registration path corrected from `opencode.json` to the live `opencode.jsonc`.
- `README.md`: intro now names the fourth content kind (plugins); layout block gained `plugins/`, `academic-check.md`, and the six `caveman*.md` command lines (branch-caused gap: the branch added six commands but only updated AGENTS.md's tree).
- `AGENTS.md`: layout tree gained the missing `academic-check.md` line (pre-existing omission).
- `STANDARDS.md`: stale "step 10" reference corrected to step 9 (the hooks step; flagged as a follow-up by the 2026-09-24 superpowers-fork report).
- `CHANGELOG.md`: added entries for the pre-commit `node --check` stanza, the dropped graphify plugin registration, and this close-out.

## Verifier output

Task 7 battery, final state (re-run by the documenter at close-out where cheap; marked re-run):

```
bin/skillctl check                          -> checks: 0 fail, 3 warn (re-run, reproduces)
                                               (the 3 warns are pre-existing C7: commands/full-cycle.md,
                                                commands/goal.md, commands/iterate-skill.md)
bin/skillctl sync --check --agent opencode  -> sync: 0 missing, 0 stale, 144 extra (dry run) (re-run, reproduces)
                                               (the 144 EXTRA are 6 externally installed skills
                                                x 24 loop iterations: graphify, vercel-composition-patterns,
                                                vercel-react-best-practices, vercel-react-native-skills,
                                                vercel-react-view-transitions, web-design-guidelines)
node plugins/caveman/test.mjs               -> absent: PASS / ultra: PASS / off: PASS / garbage: PASS (re-run, reproduces)
opencode plugin list                        -> caveman  local  /home/ruben/.config/opencode/plugins/caveman/index.js
                                                opencode-see-image  1.4.0  opencode-see-image@1.4.0
                                                -  local  /home/ruben/.opencode/plugins/graphify.js   (load failed, residual)
opencode log                                -> msg="loading plugin" id=/home/ruben/.config/opencode/plugins/caveman
                                                entrypoint=file:///home/ruben/.config/opencode/plugins/caveman/index.js
                                                0 caveman-attributed load failures after the fix
cat ~/.config/opencode/opencode.jsonc       -> plugin array: ["opencode-see-image@1.4.0"] only
test ! -e ~/.opencode/opencode.json         -> old config gone
test ! -e /home/ruben/tools/ponytail        -> clone gone
ls ~/.cache/opencode/npm/ | grep superpowers -> no match (superpowers npm cache removed)
ls ~/.config/opencode/skills/               -> own set incl. caveman, stop-slop, ponytail, using-superpowers,
                                                verification-before-completion; no cavecrew; no superpowers-pack skills
ls ~/.config/opencode/command/ | grep caveman | wc -l  -> 6
grep -rn "cavecrew" ~/.config/opencode/     -> no hits
diff -r plugins/caveman ~/.config/opencode/plugins/caveman -> identical
```

## Skills loaded

- `using-superpowers` (vendored in this branch, Task 1): skill-invocation discipline shaped the per-task dispatch.
- `verification-before-completion` (vendored in this branch, Task 1): evidence-before-assertions drove the verifier battery and the "report what was actually run" discipline.
- `ponytail` (vendored in this branch, Task 4): the YAGNI standard kept the plugin at 73 dependency-free lines and blocked ESLint/Prettier.
- `writing-plans` and `brainstorming`: the plan's shape (task per commit, explicit paths, verification commands) came from them.
- `systematic-debugging`: hypothesis-first used for the plugin-load defect (registration form vs export shape vs hook existence were three separate hypotheses, each falsified by evidence).
- `subagent-driven-development` / `execute-plan`: the executor-per-task, reviewer-per-task loop.
- `code-standardization` and `project-standardization`: the structure-review pass.

## ponytail: deferrals

- Removal of `~/.opencode/package.json`, `~/.opencode/node_modules/`, and `~/.opencode/plugins/graphify.js` is deferred by the plan; the residual load-failure WARN on every start is accepted until that follow-up (choices record 13).
- `subagent_depth` stays in the consolidated config (with its "unsupported legacy setting" WARN) rather than being redesigned mid-run (choices record 14).
- No upstream-sync tooling for the vendored packs: copies are frozen-and-owned by decision; upstream updates are drift risk, not value.
- Nothing was flagged as over-engineering by the executors; the lazy lens ran the other way (ESLint/Prettier/package.json explicitly rejected for 149 dependency-free lines).

## Unverified items

- **Fresh-session checklist** (cannot be exercised from inside a running session; the user must restart opencode and confirm):
  1. Skill list shows `caveman`, `stop-slop`, `ponytail`, `using-superpowers`, `verification-before-completion`; no superpowers-pack skills (test-driven-development, executing-plans etc. gone).
  2. `/caveman ultra` then a reply: terse; `/caveman off`: normal prose.
  3. Attach an image: `see_image` still works (see-image registration survived).
  4. `/graphify` still available. Nuance: the graphify PLUGIN was dropped (it cannot load on opencode v2); `/graphify` remains available through the graphify skill and CLI, which are untouched. The plan's checklist wording "plugin migrated" is superseded by the drop decision (choices record 12).
- The background opencode server that hosted the run still holds the pre-consolidation plugin set; a restart is required for the new config to apply.
- Windows / Git Bash behaviour of `bin/skillctl` was not re-tested in this run (the sync code path is unchanged apart from the plugins loop; last verified 2026-10-20 per `opencode-install.md`).

## Known follow-ups (pre-existing rot, outside this branch's scope)

Fixed in this close-out pass (cheap and clearly correct):

- `docs/workflows/workflow.md` agent count "Ten" vs 12 actual: corrected to twelve, roster table completed with `explore` and `lazy-dev`.
- `docs/workflows/workflow.md` section 2 listing six unvendored superpowers siblings as loading "from the repo's own skills/ directory": corrected to the seven vendored skills.
- `docs/workflows/workflow.md` naming `find-skills` (not installed): bullet removed.
- `agents/README.md` MCP registration pointing at `~/.config/opencode/opencode.json` (live file is `.jsonc`): corrected.

Left open (listed for a future pass, not fixed here):

- `docs/workflows/stack.drawio` (rev E) still shows ten agents, a "ponytail (plugin)" chip, a "find-skills" chip, unvendored process-skill names (`executing-plans`, `requesting-code-review`, `receiving-code-review`, `subagent-driven-development`, `dispatching-parallel-agents`), and the retired `~/.opencode/opencode.json` config path. Needs a redraw (rev F), not a text edit.
- `commands/execute-plan.md` still instructs loading the `subagent-driven-development` skill, which is one of the 8 unvendored superpowers siblings and no longer installed; the command works because the repo's own orchestrator flow supersedes it, but the reference is stale (commands/ was outside this dispatch's write scope).
- `CHANGELOG.md` line 29 says "opencode-install.md step 10": historical record of the original hook entry, intentionally untouched.

## Dispatch Log

- Task 1 (vendor superpowers leftovers): dispatched: executor + reviewer. Amended once for plan fidelity (the executor had appended one unspecced word to a vendored table row), then re-reviewed and passed.
- Task 2 (vendor caveman skill + commands): dispatched: executor + reviewer.
- Task 3 (vendor stop-slop, swap the live symlink): dispatched: executor + reviewer.
- Task 4 (vendor ponytail core skill, repoint lazy-dev): dispatched: executor + reviewer.
- Task 5 (minimal caveman plugin + skillctl plugins sync): dispatched: executor + reviewer.
- Task 6 (config consolidation, external teardown, install doc): dispatched: executor + reviewer.
- Task 6b (follow-up: port the plugin to the opencode v2 plugin API): dispatched: executor + reviewer. Added after an oracle consult, because the plan's plugin contract could not be met on opencode v2.0.32.
- Task 7 (final verification battery): dispatched: executor (verification only, no commit).
- Structure review: dispatched doc-standardizer + code-standardizer (concurrent).
- Quick-fix pass: dispatched executor (four commits) + reviewer.
- Review-nit cleanup: dispatched executor (two commits).
- Close-out: documenter (this dispatch).
- Zero tasks were self-implemented.

## Choices

Candidate ledger: all 20 candidates from the run material were recorded; none disqualified. Spec "Prior decisions consulted" confirmed no existing record covers vendoring; nothing was superseded (the 2026-09-29 stdctl record's "vendor stdctl only if it grows beyond one bash file" line is untouched by this run).

| # | Decision | Record |
|---|---|---|
| 1 | Vendor all four packs (superpowers remainder, caveman, stop-slop, ponytail) | 2026-10-21-vendor-all-four-packs-decision.md |
| 2 | Approach A: freeze-and-own per pack; Approach B (unified rewrite/merge) rejected | 2026-10-21-freeze-and-own-per-pack-decision.md |
| 3 | Port a minimal own caveman plugin (73 lines) instead of keeping the 1090-line upstream plugin | 2026-10-21-minimal-own-caveman-plugin-decision.md |
| 4 | Superpowers scope limited to `using-superpowers` + `verification-before-completion` (7 of 15 vendored) | 2026-10-21-superpowers-two-leftovers-scope-decision.md |
| 5 | Consolidate into one config `~/.config/opencode/opencode.jsonc`; drop broken cavecrew references | 2026-10-21-single-opencode-config-decision.md |
| 6 | Cavecrew dropped entirely; roles covered by own explore/executor/reviewer agents | 2026-10-21-cavecrew-dropped-decision.md |
| 7 | graphify, opencode-see-image, vercel-labs/agent-skills, markitdown, open-code-review stay external | 2026-10-21-external-packs-stay-external-decision.md |
| 8 | State-file contract `~/.config/opencode/.caveman-mode` (`off\|lite\|full\|ultra\|wenyan-*`); absent = base rules; unknown = treated as absent | 2026-10-21-caveman-state-file-contract-decision.md |
| 9 | Plugin hook: ported to v2 `ctx.session.hook("context", ...)` after the v1 hook proved absent and the oracle's `aisdk.hook("language")` was disproven | 2026-10-21-caveman-plugin-v2-context-hook-decision.md |
| 10 | Plugin discovery via directory auto-discovery, no config entry (avoids double load) | 2026-10-21-caveman-plugin-auto-discovery-decision.md |
| 11 | Plugin file renamed `plugin.js` to `index.js` (v2 resolves directories via `server.*` or `index.*`) | 2026-10-21-caveman-plugin-index-js-decision.md |
| 12 | graphify plugin registration dropped, not migrated (v1-shaped, never loaded); skill and CLI stay | 2026-10-21-graphify-plugin-dropped-decision.md |
| 13 | Legacy `~/.opencode/` root left untouched; its graphify.js still WARNs on start; removal is a follow-up | 2026-10-21-legacy-opencode-root-deferred-decision.md |
| 14 | `subagent_depth` kept in the consolidated config despite the v2 legacy-setting WARN | 2026-10-21-subagent-depth-kept-decision.md |
| 15 | Smoke test made hermetic via `process.env.HOME` temp dir, not a production override | 2026-10-21-hermetic-caveman-smoke-test-decision.md |
| 16 | Pre-commit `node --check` stanza for staged JS instead of ESLint/Prettier | 2026-10-21-node-check-over-eslint-decision.md |
| 17 | skillctl plugins loop simplified to `mirror plugins "$g" "$oc/plugins"`, matching the skills loop | 2026-10-21-skillctl-plugins-loop-shape-decision.md |
| 18 | Both catalog tables sorted alphabetically entirely, not only new rows | 2026-10-21-catalogs-fully-alphabetical-decision.md |
| 19 | Follow-up task 6b added beyond the plan's seven tasks (plugin contract unmeetable as written) | 2026-10-21-followup-task-v2-port-decision.md |
| 20 | Frozen spec still names `plugin.js`; deviation recorded in report + choices, spec not edited | 2026-10-21-frozen-spec-not-amended-decision.md |

## Spec/plan not modified

The design spec and plan are untouched since bootstrap commit `cb6ff80`. Deviations from them are recorded above and in the choices records, not by editing the approved documents. This report plus the 20 choices records are the only new artifacts in `docs/artifacts/` for this feature.
