# stdctl: general standards check CLI for all repos

Date: 2026-09-29
Status: approved (brainstorm answers: Tools/stdctl sibling project; v1 = floor + structure/tier + skills-collection + CC history at warn level; unstandardized repo = fail; single bash file + PATH symlink)

## Problem

The project-standardization convention defines a checkable floor (em-dash ban, forbidden paths, kebab-case, ISO 8601 artifact names, Conventional Commits/Branch, AGENTS.md + shim + tier + hooks), tier structure, and skills-collection rules. Enforcement today: per-repo `.githooks` templates, staged files only, at commit time, and only if `core.hooksPath` is activated per clone. No command exists that an agent can run in ANY repo to verify standards on demand. The user's goal: one `check` command usable in every repo, available to agents everywhere (including his sbx sandbox system, which pulls agents + skills).

## Decision

New sibling project `~/projects/Tools/stdctl` (small tier, bootstrapped via project-standardization templates), containing a single bash CLI `bin/stdctl` with one subcommand `check`. Installed machine-wide via symlink `~/.local/bin/stdctl -> ~/projects/Tools/stdctl/bin/stdctl`. stdctl operates on the current working repo (`git rev-parse --show-toplevel`), never on its own location, so symlinks and copies both work; sbx distribution = copying one file.

The skills repo stays markdown-only (its single `bin/skillctl` exception is unchanged). `skillctl` keeps `sync` + skills-repo-specific checks (catalogs C6/C7, folder-name match); `stdctl` does not absorb it.

## Prior decisions carried

- Skills repo stack "Markdown only" (2026-09 AGENTS.md): satisfied, stdctl lives outside it.
- Choices registry stays markdown, no tooling-backed lookup: stdctl never touches choices/.
- No release-automation tooling: no release/bump subcommand.
- Hooks remain the commit-time gate; stdctl is the on-demand superset audit. No `.githooks` template changes beyond what this spec lists.

## Design

### Invocation

```
stdctl check          # lint current repo
stdctl check --quiet  # summary + failures only
```

Repo root: `git rev-parse --show-toplevel`. Not a git repo: exit 2. No `AGENTS.md` at root: print `FAIL not standardized: no AGENTS.md (bootstrap via project-standardization, then re-run)`, exit 1. No other checks run in that case.

Output contract (same as skillctl): one `PASS`/`FAIL`/`WARN` line per rule, `checks: <n> fail, <n> warn` summary. Exit 0 = no FAIL; 1 = any FAIL or unstandardized; 2 = usage/non-git. WARN never fails.

Tier source: first `Tier: (small|medium|large)` match in AGENTS.md.

### Rules

Floor (always, once AGENTS.md exists):

| ID | Rule | Level |
|---|---|---|
| G1 | No U+2014 in tracked `*.md` (`git ls-files '*.md'` + grep -F) | FAIL |
| G2 | No forbidden dirs at any depth: `temp`, `old`, `archive`, `docs/superpowers`, `.planning` (find from repo root) | FAIL |
| G3 | Kebab-case paths: every `git ls-files` basename must be lowercase letters/digits/hyphens/dots (no uppercase, underscores, spaces) OR in the exception list | FAIL |
| G4 | Filenames under `docs/artifacts/` and `docs/project-management/` match `^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\.md$`; the basename `index.md` is exempt (registry indexes are not time-based records) | FAIL |
| G5 | Current branch matches Conventional Branch `<type>/<kebab-desc>` with types `feat fix docs style refactor perf test build ci chore revert` (multi-plan names like `feat/<slug>-spN-<name>` fit the kebab-desc pattern, no nested slash); `main`, `master`, `develop`, `trunk` exempt | FAIL |
| G6 | If `.githooks/` exists: `core.hooksPath` == `.githooks` and `.gitattributes` contains `.githooks/** text eol=lf` | WARN |
| G7 | Conventional Commits 1.0.0 subjects across `git log --format=%s`: non-matching subjects counted | WARN |

G3 exception list (single source: this spec, mirrored into the standard docs by this run): `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `STANDARDS.md`, `LICENSE`, `LICENSE.md`, `Makefile`, `Dockerfile`, `SKILL.md`, `Cargo.toml`, `Cargo.lock`, `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `pyproject.toml`, `poetry.lock`, `go.mod`, `go.sum`, `composer.json`, `tauri.conf.json`, `.release-notes.md`, `AGENTS-small.md`, `AGENTS-medium.md`, `AGENTS-large.md`, `README-ai-assistance.md` (project-standardization template names), plus any basename starting with `.` (dotfiles).

Structure (always, once AGENTS.md exists):

| ID | Rule | Level |
|---|---|---|
| S1 | AGENTS.md declares `Tier: small|medium|large` and contains a Git section (heading match `^#+ .*Git`) | FAIL |
| S2 | `CLAUDE.md` exists at root and contains `@AGENTS.md` | FAIL |
| S3 | `.agents/` exists with at least one `.md`: FAIL if missing at medium/large; WARN if present at small | FAIL/WARN |
| S4 | `CHANGELOG.md` exists and contains `Keep a Changelog`: missing = FAIL (medium/large) or WARN (small); present without marker = FAIL | FAIL/WARN |
| S5 | If `docs/artifacts/` exists: `features/` and `reviews/` subdirs must exist (FAIL); `choices/` missing = WARN; legacy siblings `specs/`, `plans/`, `multi-plans/` = WARN | FAIL/WARN |

Skills-collection (only when `skills/*/SKILL.md` files exist):

| ID | Rule | Level |
|---|---|---|
| K1 | Frontmatter: present, terminated, `name` kebab-case starting alphanumeric, `description` starts `Use when`, block <= 1024 bytes | FAIL |
| K2 | Body: contains `## Overview`, no `## Skill` heading | FAIL |

Deliberately NOT in stdctl v1: catalog consistency (skills-repo-specific, stays in skillctl), folder-name match (idem), commands-referenced check, versioning/SemVer trio, graphify wiring, STANDARDS.md blank-cell + README AI-section predicates, todolist format, AGENTS.md line budgets, secrets heuristics, source/deliverable separation, `fix`/`init` subcommands, `--json`.

### Standard docs fixes (this run, skills repo)

1. Kebab exception list (above) added to `skills/rubens-project-standardization/references/standards-stack.md` and the `STANDARDS.md` template, replacing/augmenting any partial list.
2. AGENTS.md line-budget contradiction resolved in favor of the tier table (small <60, medium <120, large <200); `references/bootstrap.md` step 4 `<80` corrected.
3. `references/versioning.md` bump-table row "New feature, backwards-compatible": both malformed cells corrected, `0.X+1.0` to `0.(X+1).0` (pre-1.0 column) and `0.Y+1.0` to `X.(Y+1).0` (>=1.0 column).
4. Frontmatter name rule in skills-repo `AGENTS.md`: "letters, numbers, hyphens only" gains "must start with a letter or number" (resolves hook/skillctl regex divergence; live `.githooks` unchanged, rule documented).
5. Discovery wiring: the project-standardization `AGENTS.md` template and `references/bootstrap.md` final step name `stdctl check` as the standard on-demand verification command for standardized repos.

## Testing / verification

- Dogfood: `stdctl check` in the stdctl repo itself: exit 0 after bootstrap (small tier: no `.agents/`, no CHANGELOG needed at start; expect possible S4 WARN, acceptable as WARN).
- Skills repo: exit 0 (its known state is clean per skillctl; branch `feat/...` passes G5; G7 may WARN on legacy subjects, acceptable).
- Unstandardized fixture in `/tmp/opencode/stdctl-fixture`: dir with git repo but no AGENTS.md: exit 1 with the not-standardized message.
- Dirty fixture in `/tmp/opencode`: AGENTS.md (Tier: medium) + em-dash md file, `My_File.MD`-style path violation, non-ISO artifact name, missing `.agents/`: expect specific FAILs, exit 1.
- Symlink install: `stdctl check` resolves repo from cwd, not symlink path.

## Non-goals

See the "Deliberately NOT" list. Also: no remote/git hosting setup for stdctl (local repo; user adds remote when wanted), no versioning for stdctl until first release (repo born unversioned), no sbx automation changes (user adds `~/.local/bin/stdctl` or the file copy to his sbx pull list himself).
