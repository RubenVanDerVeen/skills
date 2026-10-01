# skillctl: repo maintenance CLI (sync + check)

Date: 2026-09-29
Status: approved (brainstorm answers: scope = sync + check; location = in-repo `bin/`; language = bash + coreutils)

## Problem

Two chores dominate agent work in this repo:

1. **Agent-dir sync drift.** Skills, commands, and agents activate only after a two-step manual copy (`AGENTS.md` "Slash commands" section, `agents/README.md`, `opencode-install.md` step 8). Three feature reports document verification blocked by unsynced files: `lazy-dev-gate` (lazy-dev agent never registered), `explore-recon-delegation` (explore dispatches resolved to the built-in), `superpowers-fork` (manual `Copy-Item` x4 with hand verification). Known traps: opencode uses singular `command/`, Claude Code uses plural `commands/`; `agents/*.md` must never go to Claude; opencode needs a restart after agent changes.
2. **Manual verification scans.** `.githooks/pre-commit` only checks staged files at commit time. Agents re-run lint checks by hand mid-edit, and the documented incantations are PowerShell (`Select-String`), which does not run on this linux environment. Catalog consistency is only checked for brand-new skills (hook rule P6), not modified or renamed ones.

## Goals

- One command that syncs repo content to agent directories, correct mappings encoded once.
- One command that lints the whole worktree on demand, superset of the pre-commit rules, platform-stable (bash).
- Reuse the check logic patterns already present in `.githooks/pre-commit` (port, do not refactor the hooks).

## Non-goals

- `new`, `harvest`, `release` subcommands (deferred; YAGNI).
- Choices-registry lookup tooling (decision 2026-09-24: registry stays markdown by design).
- Release-automation tooling (explicit non-goal in versioning-standard design).
- Commit message enforcement (`.githooks/commit-msg` owns it, unchanged).
- Per-project sync targets (`.opencode/command/`, `.claude/commands/` inside other repos). Global destinations only, matching the documented defaults.
- Syncing top-level doc-skills (`opencode-install.md`, `external-skills.md`). Unclear mechanics, not a documented pain.
- Word-count budget enforcement in `check` (classification is manual, rule would be fuzzy).
- Refactoring `.githooks/*` to call skillctl. Hooks read staged content via `git show :$f`; skillctl reads the worktree. Deliberate separation.

## Design

Single executable bash script `bin/skillctl`, subcommand dispatch via `case`. Bash + coreutils only (grep, sed, awk, find, cp, rm, mkdir, diff). Resolve repo root from script location (`$(cd "$(dirname "$0")/.." && pwd)`), so it works from any cwd.

### `skillctl check`

Lints the whole worktree. Rules (ported from `.githooks/pre-commit` where they exist):

| # | Rule | Source |
|---|---|---|
| C1 | No U+2014 em-dash in any tracked `*.md` | hook P1 |
| C2 | Every `skills/*/SKILL.md`: frontmatter present, `name` kebab-case, `name` == folder (exception: `rubens-project-standardization` folder keeps old name) | hook P2 |
| C3 | `description` starts with `Use when` | hook P3 |
| C4 | Frontmatter <= 1024 bytes | hook P4 |
| C5 | Body contains `## Overview`, no `## Skill` heading | hook P5 |
| C6 | Every skill folder appears in `README.md` `## Skills` table AND `AGENTS.md` `## Current skills` table (all skills, not just new) | extends hook P6 |
| C7 | Every `commands/*.md` file is referenced by name in at least one `SKILL.md` (warn-level) | AGENTS.md red flag |
| C8 | No forbidden paths: `temp/`, `old/`, `archive/`, `docs/superpowers/`, `.planning/` | hook P7 |

Output: one `PASS`/`FAIL`/`WARN` line per rule plus a summary. Exit 0 when no FAIL, 1 otherwise (WARN does not fail). Agents use it as the standard verification step in plans and reviews.

### `skillctl sync`

Copies repo content to global agent directories. Repo is the single source of truth: mirror semantics (destination copy removed, then re-copied) so deletions propagate.

| Source | Destination | Notes |
|---|---|---|
| `skills/*/` | `~/.config/opencode/skills/` and `~/.claude/skills/` | all skill folders |
| `commands/*.md` | `~/.config/opencode/command/` (singular) and `~/.claude/commands/` (plural) | do not normalise the dir names |
| `agents/*.md` | `~/.config/opencode/agents/` | opencode ONLY, never Claude Code. Exclude `agents/README.md` (roster doc, not an agent definition) |

Flags:

- `--agent opencode|claude` (default: both)
- `--check` (dry-run): report MISSING / STALE / EXTRA per destination via `diff -rq`, change nothing. Exit contract matches `check`: MISSING or STALE count as FAIL (exit 1); EXTRA is informational WARN (destinations also hold foreign skills from other sources, e.g. externally installed ones).

Behaviour: `mkdir -p` destinations, mirror each unit, print what changed, and after touching `~/.config/opencode/agents/` print the reminder "restart opencode to reload agents" (config loads once at startup, per `agents/README.md`).

### Docs changes (same change-set)

- `AGENTS.md`:
  - Stack section: amend "No build step, no tooling, no runtime" with the single exception: maintenance CLI `bin/skillctl` (bash + coreutils, no dependencies). No other tooling allowed.
  - "Slash commands" sync subsection: replace the manual two-step instructions with `bin/skillctl sync` (keep the mapping table for reference; keep the "dead weight until synced" warning).
  - Body rules section: replace the PowerShell em-dash verification incantation with `bin/skillctl check`.
- `opencode-install.md`: step 8 (command/agent sync) points at `bin/skillctl sync` run from the clone.

## Error handling

- Unknown subcommand or flag: usage message, exit 2.
- Missing destination dir: created (`mkdir -p`) in real runs only, never in `--check` mode.
- `--check` never mutates anything.

## Testing / verification

- `bin/skillctl check` on the repo after implementation: exit 0 (repo is currently clean per the hooks).
- Deliberate dirty fixture in `/tmp/opencode` (em-dash file, bad frontmatter) run against a copied tree or via targeted flags if trivially supported: exit 1. Keep this manual smoke, no fixture framework.
- `bin/skillctl sync --check`: runs, reports per-destination status, exits 0, changes nothing.
- Real `bin/skillctl sync`: run once, then `diff -rq` spot-check one destination folder.
- Ponytail self-check: a non-trivial branch script ships with one runnable check; `skillctl check` on the repo itself is that check.

## Prior decisions carried

- Choices registry stays markdown, no tooling-backed lookup (2026-09-24, active).
- Choices location, documenter single-writer, PR Choices section: unaffected.
- No release-automation tooling (versioning-standard design): no release subcommand.
