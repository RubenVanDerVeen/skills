# Execution report: skillctl

- **Date:** 2026-09-29
- **Branch:** `feat/skillctl` (base: `main` at `1ab0d46`)
- **Plan:** `docs/artifacts/features/skillctl/2026-09-29-skillctl-plan.md`
- **Spec:** `docs/artifacts/features/skillctl/2026-09-29-skillctl-design.md`
- **Versioning:** unversioned/no bump (repo `AGENTS.md` declares no `### Versioning` canonical source; plan states it)
- **PR:** none opened. The user invoked `/execute-plan`, not `finishing-a-development-branch`; no `PR_DESCRIPTION.md` written.

## Summary

Five commits. `bin/skillctl` shipped: a dependency-free bash maintenance CLI with two subcommands. `check` lints the whole worktree (rules C1-C8, superset of the `.githooks/pre-commit` rules, reading the worktree rather than the index); `sync` mirrors `skills/`, `commands/`, and `agents/` to the global agent directories with correct per-agent mappings (opencode singular `command/`, Claude Code plural `commands/`, agents to opencode only). Docs updated in the same change-set: `AGENTS.md` (Stack exception, sync-pattern rewrite, em-dash verification, skill-verification steps), `opencode-install.md` (sync step), plus layout trees in `README.md` / `AGENTS.md` / `STANDARDS.md`, the `STANDARDS.md` stack exception, and `CHANGELOG.md` entries. One plan bug found and fixed during execution (the `sync)` dispatch line dropped `"$@"`, which silently discarded `--check` and made the dry-run path perform a real sync). Structure review produced four valid findings, all quick-fixed in `41bdb74`; three findings correctly skipped with reason. Final verification: `check` exit 0, `sync --check` exit 0, no repo agents in `~/.claude/agents/`, `bash -n` clean.

## Branch and commits

| Hash | Type | Message | Description |
|---|---|---|---|
| `3d055ed` | docs | `docs(skillctl): add design and plan for skillctl maintenance CLI` | Spec (94 lines) + plan (455 lines) under `docs/artifacts/features/skillctl/`. |
| `4fe67d0` | feat | `feat(skillctl): add check subcommand for worktree-wide lint` | `bin/skillctl` skeleton, helpers (`usage`, `pass/fail/warn`, `fm_field`, `skill_check`), full `cmd_check` (C1-C8), dispatch for `check` only. Verbatim copy of plan lines 43-176. |
| `b8d5e4f` | docs | `docs(skillctl): document skillctl, add stack exception` | `AGENTS.md`: Stack exception, "Slash commands" sync rewrite, em-dash verification rewrite, skill-verification steps 4-5. `opencode-install.md`: sync step replaced with `bin/skillctl sync`. |
| `d58a20e` | feat | `feat(skillctl): add sync subcommand mirroring to agent dirs` | Adds `mirror()`, `cmd_sync()`, counters, `sync` dispatch arm. Verbatim copy of plan lines 227-332 except the dispatch-line fix (see Deviations). |
| `41bdb74` | docs | `docs(skillctl): sync layout trees, changelog, and standards stack exception` | Structure-review quick-fix: `CHANGELOG.md` `[Unreleased]` Added + Changed entries, `bin/` lines in the `README.md` / `AGENTS.md` / `STANDARDS.md` layout trees, `STANDARDS.md` Stack-section exception. |

## Files changed

Aggregate diff (`git diff main..HEAD`): 8 files, +795 / −20.

| Path | +/− | Why |
|---|---|---|
| `bin/skillctl` | +228 | New executable. `check` (C1-C8 lint) landed in `4fe67d0` (+132), `sync` (mirror + flags) in `d58a20e` (+96). |
| `AGENTS.md` | +8/−7 | Stack exception (`b8d5e4f`), sync-pattern rewrite, em-dash verification rewrite, verification steps 4-5, File-layout `bin/` line (`41bdb74`). |
| `opencode-install.md` | +6/−12 | Manual command/agent copy step replaced by `bin/skillctl sync` run from the clone (`b8d5e4f`). |
| `CHANGELOG.md` | +2 | `[Unreleased]` Added entry for `bin/skillctl`, Changed entry for the sync workflow (`41bdb74`). |
| `README.md` | +1 | Layout-tree `bin/` line (`41bdb74`). |
| `STANDARDS.md` | +2/−1 | Stack-section tooling exception + layout-tree `bin/` line (`41bdb74`). |
| `docs/artifacts/features/skillctl/2026-09-29-skillctl-design.md` | +94 | Spec. |
| `docs/artifacts/features/skillctl/2026-09-29-skillctl-plan.md` | +455 | Plan. |

## Standardization review

### doc-standardizer

PASS after quick-fix. Findings and dispositions:

1. `CHANGELOG.md` missing `[Unreleased]` entries for the new CLI and the sync-workflow change: fixed in `41bdb74`.
2. Layout trees in `README.md`, `AGENTS.md`, `STANDARDS.md` missing the new `bin/` directory: fixed in `41bdb74`.
3. `STANDARDS.md` Stack section did not carry the tooling exception (it states "content-only repo" and would contradict `AGENTS.md`): fixed in `41bdb74`.
4. Combined with the code audit: applied as one quick-fix commit.

Skipped findings (with reason):

- Shellcheck wiring for `bin/skillctl`: would violate the plan constraint "bash + coreutils only, no new dependencies"; also out of scope for a docs audit. Not applied.
- EXTRA-scan dedup in `mirror()`: cosmetic (EXTRA lines can repeat for nested foreign content); informational WARN only, affects no exit contract. Not applied.
- Em-dash in `deep-research/scripts/verify-multi-lens.sh`: pre-existing, predates the branch, and is a shell file outside rule C1's `*.md` scope. Not applied.

### code-standardizer

PASS after quick-fix. Same four valid items (all doc-shaped: changelog, layout trees, standards stack line); no code-structure findings against `bin/skillctl` itself. Same three skips with the same reasons. The `41bdb74` quick-fix commit satisfies both audits; the feature commits are untouched.

## Documentation updates

`bin/skillctl` is a maintenance CLI, not a skill: it does not belong in the `README.md` `## Skills` table or the `AGENTS.md` `## Current skills` table, and no rows were added there. Catalog placement verified at close-out:

- `CHANGELOG.md` `[Unreleased]`: Added entry for `bin/skillctl` (with spec path) and Changed entry for the agent-dir sync workflow. In place.
- `README.md` layout tree: `bin/` line with `skillctl maintenance CLI (check, sync)` annotation. In place.
- `AGENTS.md`: Stack exception line, File-layout `bin/` line, "Slash commands" sync subsection rewritten around `bin/skillctl sync` (mapping table kept as reference), em-dash verification sentence, "Adding or modifying a skill" steps 4-5. In place.
- `STANDARDS.md`: Stack-section tooling exception + layout-tree `bin/` line. In place.
- `opencode-install.md`: sync step now `bin/skillctl sync` with `--check` note; restart note kept. In place.
- `external-skills.md`: untouched, correctly (in-repo tool, not an external skill).
- `agents/README.md` roster: untouched, correctly (no new agent).
- No `## Commands` section needed anywhere: skillctl is not a skill.

## Verifier output

Per-task verification evidence (commands run, expected vs observed):

- Task 1: `bin/skillctl check` on clean repo: all PASS, `checks: 0 fail`, exit 0. Dirty fixtures (em-dash file via `git add -N`, `skills/zz-fixture` with bad frontmatter): FAIL on C1, C2, C3, C5, C6, exit 1; cleanup run exit 0. Usage errors: `bin/skillctl bogus` and `bin/skillctl check extra` both print usage, exit 2. Matches plan expectations.
- Task 2: dry-run `sync --check` reports MISSING/STALE/EXTRA without mutating (after the dispatch fix; see Deviations for the first-probe incident). Real `sync`: SYNCED lines, `sync: <n> synced`, restart reminder, exit 0; follow-up `sync --check` clean, exit 0. Flags: `--agent claude --check` scopes to claude lines; `--agent bogus` usage, exit 2. Regression `check` exit 0. `diff -rq` spot-check of one synced folder empty; no repo agent file in `~/.claude/agents/`.
- Task 3: `bin/skillctl check` exit 0 after docs edits (no em-dash introduced); edited sections read back consistent with CLI behavior.
- Task 4 (final): all four steps PASS, exit codes match the plan. Re-confirmed by the documenter at close-out (2026-09-29): `bin/skillctl check` exit 0 (`checks: 0 fail, 3 warn`); `bin/skillctl sync --check` exit 0 (`0 missing, 0 stale, 252 extra`); `ls ~/.claude/agents/ | grep <agent names>` empty; `bash -n bin/skillctl` no syntax errors; `git log --oneline -4` shows the three plan-specified commits.

The 3 C7 warnings are `commands/full-cycle.md`, `commands/goal.md`, `commands/iterate-skill.md`: universal commands without a parent skill, a legitimate warn-level condition per the plan ("universal commands without a parent skill may legitimately warn"). The 252 EXTRA lines are foreign, externally installed skills in the destination directories: informational WARN per the spec's exit contract.

Reviewer outcomes: Task 1 PASS, Task 2 PASS, Task 3 PASS (each committed at its plan-specified boundary after review), Task 4 PASS (report-only).

## Skills loaded

- `project-standardization` (by doc-standardizer, per its agent definition).
- `code-standardization` (by code-standardizer, per its agent definition).

## Deviations from the plan

1. **Task 2 dispatch-line fix (plan bug).** Plan line 329 read `sync) shift; cmd_sync ;;`; without `"$@"` the flags were silently dropped, so `sync --check` performed a real sync and `--agent` was ignored. Executor fixed it to `sync) shift; cmd_sync "$@"` (`bin/skillctl` line 226). Mechanical correction, not a design change; no choices entry needed.
2. **Task 2 verification sequence adapted.** The first dry-run probe ran before the dispatch fix was recognized, so it accidentally populated the destinations (a real sync under a dry-run name). The subsequent verification order was adapted to the already-synced state; final verification confirms idempotence and a clean `sync --check`.
3. **Task 3 wording.** Lead-in changed from "Two-step sync per machine:" to "Sync skills, commands, and agents in one step per machine:" because the old lead-in contradicted the new "in one command" copy. Meaning preserved, contradiction removed.

## Defaults taken

None of substance. The executor noted no judgment calls beyond the deviations above.

## Choices superseded

None. No `docs/artifacts/choices/` entry written: the one candidate (the dispatch-line fix) is a typo correction that constrains nothing. Prior decisions carried unchanged: choices registry stays markdown (2026-09-24), no release-automation tooling.

## Approaches considered and rejected (per spec)

- `new`, `harvest`, `release` subcommands: deferred, YAGNI.
- Choices-registry lookup tooling: not adopted (decision 2026-09-24, registry stays markdown by design).
- Release-automation tooling: not adopted (explicit non-goal from the versioning-standard design).
- Refactoring `.githooks/*` to call skillctl: skipped by design (hooks read staged content via `git show :$f`; skillctl reads the worktree; deliberate separation).
- Per-project sync targets and syncing top-level doc-skills: excluded (not a documented pain).
- Word-count budget enforcement in `check`: excluded (fuzzy classification).

## Re-runnable verification

```bash
bin/skillctl check; echo "exit=$?"        # expect: 0 fail, exit 0
bin/skillctl sync --check; echo "exit=$?" # expect: 0 missing, 0 stale, exit 0
```

## `ponytail:` deferrals

None. No `ponytail:` comments landed in the diff; the executor reported no deliberate shortcuts. The spec's ponytail self-check requirement is satisfied by `skillctl check` on the repo itself.

## Unverified items / outstanding follow-ups

- Cosmetic: EXTRA-scan output in `mirror()` can double-report nested foreign content; dedup is a cosmetic improvement, no exit-contract impact. Skipped by the structure review.
- Pre-existing: em-dash in `deep-research/scripts/verify-multi-lens.sh`; predates this branch and sits outside rule C1's `*.md` scope. Left for a future cleanup pass.
- Behavioral acceptance of `sync` under a fresh machine (empty destinations) is inferred from the code path and the accident in Deviation 2 (a first-run real sync did populate destinations correctly), not re-tested on a clean home directory.

## Dispatch Log

| Phase | Agent | Result |
|---|---|---|
| Task 1: `bin/skillctl` skeleton + `check` | dispatched: executor + reviewer | PASS; commit `4fe67d0`. |
| Task 2: `sync` subcommand | dispatched: executor + reviewer | PASS; dispatch-line plan bug fixed during execution; commit `d58a20e`. |
| Task 3: docs (AGENTS.md, opencode-install.md) | dispatched: executor + reviewer | PASS; commit `b8d5e4f`. |
| Task 4: final verification | orchestrator (no dispatch) | All four steps PASS, exit codes match plan; no commit (report-only). |
| Structure review | doc-standardizer + code-standardizer (concurrent) | 4 valid findings, 3 skipped with reason. |
| Quick-fix | executor (in-run) | Commit `41bdb74` (CHANGELOG, layout trees, STANDARDS stack exception). |
| Execution report + close-out | dispatched: documenter | This report; no choices entry, no PR, no version bump. |
