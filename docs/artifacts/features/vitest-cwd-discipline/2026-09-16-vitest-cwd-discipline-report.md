# Execution report: vitest-cwd-discipline

- **Date:** 2026-09-16
- **Branch:** `docs/vitest-cwd-discipline` (base: `main`)
- **Plan:** `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-plan.md`
- **Spec:** `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-design.md`
- **Summary:** Three commits. Spec + plan landed, then the cwd rule, package-manifest guard, and targeted-first test scope were encoded into `agents/executor.md`, `agents/reviewer.md`, and `commands/execute-plan.md` (bodies only, frontmatter untouched), a CHANGELOG entry was added after a doc-standardizer quick-fix, and the three files were synced machine-locally with hash verification. Markdown-only change; no code, no new skills, commands, or agents.

## Commits

| Hash | Type | Message | Description |
|---|---|---|---|
| `51afeca` | docs | `docs: add plan and spec for vitest-cwd-discipline` | Bootstrap commit: approved design and implementation plan. |
| `c903ffe` | docs | `docs(skills): enforce test cwd and targeted scope in plan-run instructions` | Task 1: the three instruction-file edits (exact spec wording). |
| `cb76fbf` | docs | `docs(changelog): note test cwd and targeted scope in plan-run instructions` | doc-standardizer quick-fix: CHANGELOG entry for `c903ffe`. |

## Files changed

Diff: `git diff main...docs/vitest-cwd-discipline` (6 files, +250 / -2).

| Path | +/− | Why |
|---|---|---|
| `agents/executor.md` | +1/−1 | Verify bullet (line 35) extended: test commands and cwd copied from the project's AGENTS.md, never run a runner from a directory lacking its package manifest, targeted scope not full suite. |
| `agents/reviewer.md` | +2/−0 | Test-runs paragraph inserted after the two passes (line 43 area): command/cwd/scope from the project's AGENTS.md, documented fast-path, targeted-first, full suite only when coverage unclear or pre-merge. |
| `commands/execute-plan.md` | +1/−1 | Folded verify bullet (line 16) extended with the same cwd/manifest/targeted-scope rule; reaches every implementer dispatch. |
| `CHANGELOG.md` | +1/−0 | Keep a Changelog entry for the instruction change. |
| `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-design.md` | +94/−0 | Spec (new). |
| `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-plan.md` | +151/−0 | Plan (new). |

## Validation output

- **Em-dash scan** (`Select-String -Pattern ([char]0x2014)`) over `agents/executor.md`, `agents/reviewer.md`, `commands/execute-plan.md`, `CHANGELOG.md`: empty, no U+2014 found.
- **Frontmatter byte-identity:** `git diff main...docs/vitest-cwd-discipline` shows no frontmatter changes to either agent file; the hunks start at line 35 (`executor.md`) and line 43 (`reviewer.md`), both after the closing `---`. Bodies only, as the spec requires.
- **opencode parse:** `opencode agent list` (Task 2) listed both `executor` and `reviewer` subagents; `opencode debug agent executor` and `opencode debug agent reviewer` both resolved as JSON without errors.
- **Sync hashes (Task 3, after Task 2 PASS):**

```
OK  agents/executor.md        SHA256 E7FF2AAEC563DA3D00E5DD6468E4055F7A888B68031031421DAB30EF57FEC894
OK  agents/reviewer.md        SHA256 47F18C0660C679BEDDC20EB143799A0BAE4C498E41A85C7BE54C27717AC42E4D
OK  commands/execute-plan.md  SHA256 2A8BEC8ABC7839DFEE0C2A996D3750C67DB6754202A6A351447E4D4916A8B607
```

Three OK, zero mismatches. Sync targets: `~/.config/opencode/agents/` and `~/.config/opencode/command/` (no commit; outside the repo).

## Standardization review

### doc-standardizer

One quick-fix: missing CHANGELOG entry for the instruction change. Fixed in commit `cb76fbf`; reviewer re-checked the fix and PASSed. No findings remain.

### code-standardizer

PASS. Markdown-only change; no code structure to flag.

## Restart caveat

**Activation requires an opencode restart.** Agents and commands load once at opencode startup; the synced files are read at that point. Already-running sessions (including the one that executed this plan) keep the old agent bodies until restarted. The files on disk are correct (hashes above); only the running processes lag.

## Unverified items

- **Behavioral effect, unobservable in advance:** this repo has no test suite, so the rule's effect is only observable in the next hermes-console plan run. Observable to watch: reviewer/executor logs should show `cd frontend` test invocations and targeted scope (e.g. `--changed main` fast-path), and no bare-root `npx vitest run`. If plan runs still misfire from the root after this fix, the spec's documented escalation path is a technical guard (stub root `package.json` or vitest `exclude`).

## Skills loaded

None. Markdown-only change executed under `/execute-plan` conventions; no skill matched the edit work.

## `ponytail:` deferrals

None in this change. The spec itself records one deliberate deferral (not a `ponytail:` comment): technical guards rejected as YAGNI, behavioral fix first.

## Catalog updates

None needed. No new skill, command, or agent; the three edited files are existing entries whose frontmatter was preserved, so README, AGENTS.md, `opencode-install.md`, and `external-skills.md` tables are unchanged.

## Dispatch Log

| Phase | Agent | Result |
|---|---|---|
| Bootstrap | orchestrator (self) | Branch `docs/vitest-cwd-discipline` created; spec + plan committed (`51afeca`). |
| Task 1: three text edits + commit | executor | Commit `c903ffe`. |
| Task 2: spec-compliance review + opencode parse | reviewer | PASS. |
| Task 3: sync + hash verify (no commit) | orchestrator (self, trivial-bash fallback per plan) | Three hash OK lines, no mismatches. |
| Closing structure review | doc-standardizer | 1 quick-fix (CHANGELOG entry). |
| Quick-fix commit | executor | Commit `cb76fbf`. |
| Re-check | reviewer | PASS. |
| Closing code review | code-standardizer | PASS (markdown-only). |
| Report | documenter | This file. |
