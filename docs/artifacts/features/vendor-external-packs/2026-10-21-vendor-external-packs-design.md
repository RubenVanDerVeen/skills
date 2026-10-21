# Design: Vendor external skill packs into own repo

- **Date:** 2026-10-21
- **Status:** approved (design approved in session; cavecrew explicitly confirmed dropped by user)
- **Feature folder:** `docs/artifacts/features/vendor-external-packs/`
- **Branch:** `feat/vendor-external-packs`

## Motivation

Four external packs currently shape this user's agent behavior: superpowers (obra, MIT), caveman (JuliusBrussee), stop-slop (hardikpandya), ponytail (DietrichGebert). These encode opinion (prose style, process discipline, YAGNI philosophy) rather than tooling. Depending on upstream means another person's decisions steer the agent. Precedent exists: 2026-09-24 five superpowers process skills were forked into this repo (commit `9b0d4c4`). This feature finishes that pivot and extends it to the other three packs.

Known rot from the status quo, to be eliminated:

- Duplicate superpowers copies (vendored + upstream plugin) both loadable; name-collision risk.
- cavecrew commands/agents from the caveman pack reference agents that do not exist on this machine.
- ponytail plugin registered but apparently not loading on Linux; fragile manual clone.
- Plugin registrations split across two global configs (`~/.config/opencode/opencode.jsonc` and `~/.opencode/opencode.json`).

## Goals

1. Own copies of the four packs live in this repo, synced by `skillctl sync`, attribution preserved.
2. Upstream dependencies removed: superpowers plugin registration, caveman npx install, stop-slop symlink, ponytail clone + registration.
3. Minimal own caveman plugin replaces the 1090-line upstream JS plugin.
4. One consolidated opencode config file.
5. Catalogs (`README.md`, `AGENTS.md`), `external-skills.md`, and `opencode-install.md` reflect the new state.

## Non-goals (stay external, unchanged)

- `graphify`: skill is useless without its CLI binary; keep external.
- `opencode-see-image`: npm plugin, code not prose; keep external.
- `vercel-labs/agent-skills`: fast-moving upstream, Vercel-stack opinions; keep external.
- `markitdown`, `open-code-review`: CLIs, not skills; out of scope.
- No unified rewrite/merge of packs (Approach B rejected in session): trigger continuity preserved.
- Cavecrew: dropped entirely. User confirms non-use. Its investigator/builder/reviewer roles are covered by this repo's `explore`, `executor`, `reviewer` agents.

## Prior decisions consulted

`docs/artifacts/choices/` (7 records + index) contains no decision about external skills or vendoring. Only adjacent note: `2026-09-29-stdctl-decision.md` line 30 (vendor stdctl only if it grows beyond one bash file). No contradictions; a new choices record for this vendoring lands at close-out via the documenter.

## Decisions (user-confirmed in session)

| Question | Decision |
|---|---|
| Vendor targets | All four: superpowers remainder, caveman, stop-slop, ponytail |
| Caveman JS plugin | Port minimal own plugin (~100-200 lines, mode state + per-turn injection) |
| Superpowers scope | Only actively used leftovers: `using-superpowers`, `verification-before-completion` |
| Config hygiene | Consolidate into one config; drop broken cavecrew refs |
| Approach | A: freeze-and-own per pack (adapted copies, not rewrite) |

## Component specs

### 1. superpowers leftovers

- New `skills/using-superpowers/SKILL.md` and `skills/verification-before-completion/SKILL.md`.
- Source: the cached upstream copies currently live in `~/.cache/opencode/npm/git-superpowers-0958a5557860/.../node_modules/superpowers` (executor copies from there; upstream GitHub fallback if cache is gone).
- Adaptation rules (match the existing five vendored skills):
  - Line 8 style attribution: `Adapted from obra/superpowers (MIT).`
  - Keep opencode tool mapping; drop other-harness reference files not applicable to opencode.
  - Frontmatter per house rules: `name` kebab-case, `description` starts with "Use when...".
- Own process skill set after this: 5 existing + 2 new = 7.
- Upstream plugin registration removed (component 6). Cache directory itself is disposable; removal optional, not a task goal.

### 2. caveman skill + commands

- New `skills/caveman/SKILL.md`:
  - Levels: `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`, plus `off`.
  - Core rules as currently embedded in `~/.config/opencode/AGENTS.md` (`<!-- caveman-begin -->` block): drop articles/filler/pleasantries/hedging, fragments OK, technical terms exact, code/commits/PRs written normal.
  - Auto-clarity carve-outs: security warnings, irreversible actions, confused user; resume after.
  - `## Commands` section listing own command files.
  - Attribution line: `Adapted from JuliusBrussee/caveman.`
- Six command files in top-level `commands/`: `caveman.md` (switch level), `caveman-commit.md`, `caveman-compress.md`, `caveman-review.md`, `caveman-stats.md`, `caveman-help.md`. Behavior ported from upstream commands, wording own.
- `/caveman` switching mechanism: the command instructs the agent to write the mode string to the state file (see component 4) via shell; no JS command parsing.

### 3. Minimal caveman plugin

- New file `plugins/caveman/plugin.js` in this repo. Dependency-free Node JS, target under ~200 lines.
- Behavior contract:
  - State file: `~/.config/opencode/.caveman-mode`, content one of the level strings. Default when absent: `full`.
  - On each assistant turn (opencode plugin API; executor verifies exact hook against the `opencode` skill/plugin docs), read state file and inject the matching terse-rules block into the prompt context (equivalent of today's `caveman-begin` block).
  - No command parsing, no ownership manifests, no session detection heuristics beyond mode read.
  - Fails silent: unreadable/missing state never breaks a session.
- `bin/skillctl sync` extended to copy `plugins/caveman/plugin.js` to `~/.config/opencode/plugins/caveman/plugin.js`; `sync --check` reports drift for it.
- `AGENTS.md` stack section gains one line acknowledging the plugin exception (repo stays markdown-first; exceptions: `bin/skillctl`, `plugins/caveman/plugin.js`).

### 4. stop-slop

- New `skills/stop-slop/SKILL.md` with heavy reference material split into `references/` (upstream is 496 lines across 7 files; house token budgets demand body under ~500 words for frequently-loaded skills).
- Rule wording aligned with house style where it overlaps (no-em-dash rule already exists as rule C1).
- Attribution: `Adapted from hardikpandya/stop-slop.`
- External symlink `~/.config/opencode/skills/stop-slop` removed so `skillctl sync` owns the location.

### 5. ponytail

- Executor inspects clone at `/home/ruben/tools/ponytail` (4.7 MB, 6 skills + `ponytail.mjs`).
- Vendor only the core YAGNI/lazy-philosophy skill (max 2 skills if genuinely separable and valuable). Delegation mechanics skipped: own agents (`lazy-dev`, `explore`, `executor`, `reviewer`) cover them.
- Folder `skills/ponytail/`, attribution `Adapted from DietrichGebert/ponytail.`
- `agents/lazy-dev.md` repointed from external clone to own skill.
- Clone directory `/home/ruben/tools/ponytail` deleted (user-confirmed in session: ponytail was chosen for vendoring; deletion is part of dropping the dependency).

### 6. Config consolidation

- Single config file: `~/.config/opencode/opencode.jsonc`.
- Plugin registrations after migration: `opencode-see-image` (npm, unchanged), graphify plugin (path re-registered from `~/.opencode/opencode.json`), own `plugins/caveman/plugin.js` path.
- Superpowers and ponytail registrations dropped with the old file.
- `~/.opencode/opencode.json` deleted after migration; verify graphify still loads.
- Any cavecrew/caveman-pack leftovers in `~/.config/opencode/commands/` and skills dir removed (own synced versions replace them).
- Stale upstream caveman state artifacts removed: `~/.config/opencode/.caveman-active`, `~/.config/opencode/.caveman-opencode-ownership.json`, `~/.config/opencode/plugins/caveman/` (upstream JS). Own plugin uses a fresh state file name (`.caveman-mode`).

### 7. Docs and catalogs

- Per-task (pre-commit hook requires same-commit catalog rows): each new skill ships with its row in `README.md` `## Skills` and `AGENTS.md` `## Current skills`.
- `external-skills.md`: superpowers, caveman, stop-slop, ponytail entries get `Status: forked into this repo 2026-10-21 ...` lines (pattern already used by superpowers entry); sources stay for attribution.
- `opencode-install.md`: external install steps for the four packs replaced by `bin/skillctl sync`; plugin registration instructions updated to the single-config layout.
- Choices record written at close-out by the documenter.

## Error handling

- Plugin: any state-file read/parse failure degrades to `full` mode or silence; never throws into a session.
- Migration: config consolidation only after new plugin path verified loadable; old config deleted last.
- Skill sync: `skillctl sync --check` must be clean before task completion; symlink collisions resolved by explicit removal first.

## Verification

1. `bin/skillctl check` passes (frontmatter, no em-dash, budgets, headings).
2. `bin/skillctl sync --check` reports no drift after sync.
3. Fresh opencode session: own skills listed (including `caveman`, `stop-slop`, `ponytail`, `using-superpowers`, `verification-before-completion`); no superpowers-cache skills; no cavecrew.
4. `/caveman ultra` flow: state file changes, next turn reflects ultra rules (manual or observed session check).
5. `see_image` tool still present (see-image registration survived consolidation).
6. `grep -r caveman\|superpowers\|ponytail\|cavecrew` over `~/.config/opencode/` and `~/.opencode/` shows no stale upstream registrations or broken refs.
7. Repo catalogs list every new skill; pre-commit hook passes on each task commit.

## Versioning

Repo AGENTS.md has no `### Versioning` subsection: unversioned, no bump.
