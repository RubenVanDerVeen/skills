# stdctl execution report

- Date: 2026-09-29
- Branch: `feat/stdctl-docs` (skills repo), `main` (stdctl repo)
- Plan: `docs/artifacts/features/stdctl/2026-09-29-stdctl-plan.md`
- Spec: `docs/artifacts/features/stdctl/2026-09-29-stdctl-design.md`
- Versioning: both repos unversioned, no bump.

## TL;DR

stdctl shipped: single-file bash CLI (`bin/stdctl check`) linting any standardized repo against floor G1-G7, structure/tier S1-S5, skills-collection K1-K2. Lives in new sibling repo `~/projects/Tools/stdctl` (small tier, 6 commits), symlinked at `~/.local/bin/stdctl`. Skills repo convention docs fixed on `feat/stdctl-docs` (3 commits): kebab exceptions, tier line, line-budget fix, versioning table fix, stdctl wiring. Final matrix: stdctl repo exit 0, skills repo exit 0, non-git exit 2, unstandardized exit 1.

## Outcome

| Task | What | Result |
|---|---|---|
| 1 | Bootstrap stdctl repo (small tier) | done, `daaabac` |
| 2 | `bin/stdctl` skeleton + gate + floor G1-G7 | done, `28414d0` + fix `23ba60e` (1 fix round) |
| 3 | Structure S1-S5 + skills-collection K1-K2 | done, `68402c9` + seed `a9905e0` (1 fix round) |
| 4 | Symlink install + cross-repo smoke | clean, no commit needed (skills repo FAILs deferred to Task 5 per plan) |
| 5 | Standard docs fixes + stdctl wiring (skills repo) | done, `3c3801b` |
| 6 | Final matrix + structure review + close-out | matrix green; quick-fix bundle `726fb8e` + `929f6a4`; this report |
| Phase 2 | Doc/code standardizer quick-fixes | all 7 findings addressed, both repos clean |

## Branch and commits

stdctl repo (`main`, 6 commits):

| Hash | Subject |
|---|---|
| `daaabac` | chore: bootstrap stdctl repo (small tier) |
| `28414d0` | feat: add check with floor rules G1-G7 |
| `23ba60e` | fix: read current branch via git branch --show-current |
| `68402c9` | feat: add structure, tier, and skills-collection checks |
| `a9905e0` | chore: seed docs/artifacts/ subdirs for self-lint |
| `726fb8e` | chore: ship docs/artifacts/features/.gitkeep, .editorconfig, .shellcheckrc, shellcheck gate |

skills repo (`feat/stdctl-docs` vs `main`, 3 commits):

| Hash | Subject |
|---|---|
| `63faef7` | docs: add stdctl design and plan |
| `3c3801b` | docs(standardization): kebab exceptions, tier line, line-budget fix, stdctl wiring |
| `929f6a4` | chore(standardization): add .editorconfig |

Close-out commit (this report + choices entry): `docs: add stdctl execution report`.

## Files changed

stdctl repo, full history: 13 files, 419 insertions.

| File | Change |
|---|---|
| `AGENTS.md` | +17 (small tier, Git section) |
| `CLAUDE.md` | +2 (shim) |
| `README.md` | +7 |
| `bin/stdctl` | +286 (whole CLI) |
| `.githooks/pre-commit` | +57 (P1 + P7 + P8 shellcheck gate) |
| `.githooks/commit-msg` | +36 |
| `.gitattributes` | +2 |
| `.gitignore` | +1 |
| `.editorconfig` | +10 |
| `.shellcheckrc` | +1 |
| `docs/artifacts/{features,reviews,choices}/.gitkeep` | 3 empty markers |

skills repo, `main..feat/stdctl-docs`: 11 files, +721 -5.

| File | Change |
|---|---|
| `AGENTS.md` | +2 -2 (frontmatter name rule "must start with a letter or number", `Tier: small` line) |
| `.editorconfig` | +6 (base block, markdown-only repo so no `[*.sh]`) |
| `docs/artifacts/features/stdctl/2026-09-29-stdctl-design.md` | +91 (spec) |
| `docs/artifacts/features/stdctl/2026-09-29-stdctl-plan.md` | +612 (plan) |
| `skills/rubens-project-standardization/references/bootstrap.md` | +2 -2 (line budget `<80` to tier table values, stdctl wiring line) |
| `skills/rubens-project-standardization/references/standards-stack.md` | +1 -1 (kebab exception list) |
| `skills/rubens-project-standardization/references/versioning.md` | +1 -1 (bump-table malformed cells fixed) |
| `skills/rubens-project-standardization/templates/AGENTS-{small,medium,large}.md` | +1 each (stdctl verification wiring) |
| `skills/rubens-project-standardization/templates/STANDARDS.md` | +1 -1 (kebab exception list) |

Close-out adds: this report, `docs/artifacts/choices/2026-09-29-stdctl-decision.md`, one index row.

## Standardization review

Doc-standardizer: 4 findings, all fixed in Phase 2.

- `docs/artifacts/features/.gitkeep` missing in stdctl repo (S5 fresh-clone FAIL). Fixed in `726fb8e`.
- `.shellcheckrc` + `.editorconfig` missing in stdctl repo. Fixed in `726fb8e`.
- `.editorconfig` missing in skills repo. Fixed in `929f6a4`.
- Untracked per-task reports (`task-{1..5}-report.md`) in both repos: removed; canonical report is this file.

Code-standardizer: 2 findings fixed (same shellcheck + editorconfig items, shared with doc pass). 2 findings remain as recommendations, recorded as ponytail deferrals below (GNU-isms: `$'\u2014'`, `\<` word boundary).

## Documentation updates

- `standards-stack.md` + `STANDARDS.md` template: G3 exception list verbatim from spec, single source.
- `bootstrap.md`: line-budget contradiction resolved (small <60, medium <120, large <200); standing verification command `stdctl check` named at end.
- `versioning.md`: bump-table row "New feature, backwards-compatible" cells corrected (`0.(X+1).0`, `X.(Y+1).0`).
- Skills repo `AGENTS.md`: name rule gains "must start with a letter or number"; `Tier: small` declared (line budgets stay guidance, noted in commit body of `3c3801b`).
- `AGENTS-{small,medium,large}.md` templates: stdctl verification wiring line.
- No catalog rows anywhere: stdctl is not a skill, has no SKILL.md, no frontmatter, no commands.

## Verifier output

Per-task verification (commands per plan steps, exit codes recorded at dispatch):

| Task | Verify | Result |
|---|---|---|
| 1 | `git status --short` + `grep -c 'Tier: small' AGENTS.md` | scaffold files only, grep = 1 |
| 2 | `bin/stdctl check` in stdctl repo | self = 0 |
| 2 | gate fixture (git repo, no AGENTS.md) | exit 1, not-standardized FAIL |
| 2 | `bin/stdctl bogus` | exit 2, usage |
| 2 | dirty fixture (em-dash md, `temp/`, non-ISO artifact) | exit 1, FAIL G1+G2+G4 |
| 3 | structure fixture, no Tier line | exit 1, 5 FAILs (S1 tier, S1 Git heading, S2, S3 no-tier, S4 no-tier) |
| 3 | structure fixture, `Tier: medium` | exit 1, S3 + S4 medium FAILs added |
| 3 | skills repo pre-Task-5 | exit 1, S1 (no tier) + S3 (no-tier branch) FAIL, recorded as expected |
| 4 | smoke: self / skills / nogit | 0 / 1 (pre-fix, deferred to Task 5) / 2 |
| 5 | `bin/skillctl check` + `stdctl check` in skills repo | skillctl = 0, stdctl = 0, diff em-dash-free |
| 6 | matrix re-run (Task 6 Step 1) | stdctl = 0 (1 warn S4, expected at small tier), skills = 0 (0 fail 0 warn), non-git = 2, unstandardized = 1 |

Phase 2 re-verify (from `/tmp/opencode/quickfix-report.md`): both `git status --porcelain` clean (skills repo: `?? .claude/` only), `stdctl check` stdctl = 0 / skills = 0, no em-dash in changed files, P8 hook gate passes with shellcheck absent (fixture commit in `/tmp/opencode/test-hook`).

## Skills loaded

- `subagent-driven-development` (orchestrator, dispatch loop).

## Ponytail deferrals

- `bin/stdctl` uses `$'\u2014'` for the em-dash probe: GNU bash-ism. Ignored: personal tool, pinned Linux + bash 5.2. Upgrade path: `$'\xe2\x80\x94'` byte literal if portability ever matters.
- `s1` Git-heading regex uses `\<Git\>` GNU word boundary. Same caveat, same ruling.
- Pre-commit hooks validate staged content only (pre-existing `ponytail:` note, ceiling unchanged by P8).

## Unverified items

- shellcheck never ran live: not installed locally. P8 gate verified only in the absent-shellcheck branch (conditional skip).
- stdctl untested on non-GNU grep/awk (BSD/macOS): out of scope, pinned platform.
- sbx distribution path (copying the single file into a sandbox) not exercised; only the `~/.local/bin` symlink tested.

## Dispatch Log

| Unit | Mode |
|---|---|
| Task 1 | dispatched: executor + reviewer |
| Task 2 | dispatched: executor + reviewer, 1 fix round |
| Task 3 | dispatched: executor + reviewer, 1 fix round |
| Task 4 | dispatched: executor + reviewer, clean |
| Task 5 | dispatched: executor + reviewer, clean |
| Phase 2 quick-fixes | dispatched: executor + reviewer, all 7 findings addressed |

Nothing self-implemented.

## Rulings I made

1. `.claude/` untracked in skills repo predates dispatch: left in place.
2. Task 2 G5 defect: plan-verbatim `git rev-parse --abbrev-ref HEAD` breaks on unborn HEAD (fresh fixtures). Real defect inherited from plan. Fixed per spec semantics with one-line `git branch --show-current` substitution, shipped as `fix:` commit `23ba60e`.
3. Task 3 S5 self-FAIL: plan oversight, Task 1 should have seeded all three `docs/artifacts/` subdirs. Fixed retroactively by seed commit `a9905e0` (+ `726fb8e` for `features/`). Spec semantics preserved.
4. Bash `$'\u2014'` portability: noted by code-standardizer, ignored (personal tool, pinned Linux/bash 5.2).
5. `s1` regex `\<Git\>` GNU word-boundary: same, ignored.

## Deviations

| Deviation | Reason |
|---|---|
| Task 2 fix round (`23ba60e`) | plan verbatim copy carried an unborn-HEAD defect; spec semantics (current branch) won over plan letter |
| Task 3 fix round (`a9905e0`) | plan-side seed oversight; S5 self-lint required the subdirs Task 1 should have created |
| Task 6 structure-review quick-fix bundle (`726fb8e` + `929f6a4`) | doc-standardizer + code-standardizer findings merged into one Phase-2 pass; shared items (shellcheck, editorconfig) fixed once per repo |

Choices superseded during execution: G5 fix approach (spec semantics over plan verbatim), S5 seed ownership (Task 3 retro-fix instead of Task 1), quick-fix bundling (Phase 2 instead of per-audit commits).
