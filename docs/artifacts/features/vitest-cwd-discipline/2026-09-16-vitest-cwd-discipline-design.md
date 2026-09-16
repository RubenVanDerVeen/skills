# Design: test cwd and scope discipline for plan-run agents

Date: 2026-09-16
Status: approved (user decision recorded below)
Target repo: `C:\Users\ruben\Projects\Tools\skills` (the agent/command definitions), machine-local sync for activation.

## Problem

Plan-run executors and reviewers run `npx vitest run` from the hermes-console repo root. The root has no `package.json`, so vitest resolves anyway and its discovery starts at cwd, crawling the live worktrees (`worktrees/feat-loading-followups`, `worktrees/feat-note-properties-and-path-chip`). Observed: 256 files / 1700 tests, 141 false-failing suites, exit 1, minutes wasted per run, and agents "fixing" phantom breaks. The correct run from `frontend/` is 89 files / 1053 tests, green, about 60 s.

Recon finding (2026-09-16): hermes-console's own `AGENTS.md` Commands section already documents the correct invocations and even a reviewer fast-path:

```
cd frontend && npm run build && npx vitest run    # frontend tests, run ONLY from frontend/, never repo root
cd frontend && npx vitest run --changed main      # reviewers: fast re-check of touched tests; full suite before merge
```

Agents still ran vitest from the root. The instructions those agents actually follow are the generic ones in this repo: `agents/executor.md` ("run lint, typecheck, tests"), the `agents/reviewer.md` body (runs tests, no cwd or scope guidance), and `commands/execute-plan.md` line 16 ("run the project's lint / typecheck / unit tests"), which is folded into every implementer dispatch. None names a working directory, none forbids the bare-root invocation, none constrains scope. So agents guess cwd and default to the full suite.

## User decision (2026-09-16)

Test-run policy: **Targeted-first**.

- Executors: run only tests covering the files they changed (seconds), from the correct directory. Never wait on a full suite.
- Reviewers: default to diff-scoped re-checks (the project's documented fast-path where present, e.g. `npx vitest run --changed main`). Full suite only when targeted coverage is unclear or the branch/phase is about to merge.
- Everyone: test commands, cwd, and scope come from the project's `AGENTS.md`; never invoke a test runner from a directory that lacks its package manifest (`package.json`, `pyproject.toml`, ...), because discovery crawls siblings and worktrees and false-fails.

Rejected scope alternatives: reviewer-owns-full-suite-per-task (60 s per task is still wasted when a 5 s targeted run covers the diff); never-run-full-suite (drops the pre-merge safety net).

## Goals

1. The generic plan-execution instructions carry the cwd rule, the manifest guard, and the targeted-first scope.
2. The change activates on this machine (sync to `~/.config/opencode/`).
3. Minimal diff: three small text edits plus a local sync. No new files.

## Non-goals

- No hermes-console changes. Its AGENTS.md already warns correctly; the repo sits on an in-flight feature branch (`fix/daemon-activity-heartbeat`), so a cross-repo docs commit there is friction for zero new information.
- No technical guards (root stub `package.json`, vitest `exclude` config). Behavioral layer first; add a guard only if agents still misfire after this fix.
- No CI changes, no frontmatter/description changes (descriptions are the agents' public interface; bodies only).

## Approaches considered

**A. Skills-repo text fix (recommended, chosen).** Extend the verify bullet in `agents/executor.md`, add a test-runs rule to `agents/reviewer.md`, extend the folded verify bullet in `commands/execute-plan.md`, then sync the three files to `~/.config/opencode/`. Fixes the behavior where it originates (the instructions every plan run uses), works for every project repo, not just hermes-console.

**B. A plus a why-clause in hermes-console/AGENTS.md** ("no package.json at root; vitest crawls worktrees/ and false-fails"). Rejected: the warning and the policy already exist there; an extra clause does not address why agents ignored it (they follow the generic text). Cross-repo commit on an in-flight branch for marginal gain.

**C. A plus a technical guard** (stub root `package.json` or vitest exclude). Rejected as YAGNI: try the behavioral fix first; the guard is the escalation if plan runs still misfire. Noted as the documented upgrade path.

## Changes (exact new wording)

### 1. `agents/executor.md`, bullet at line 35

Replace with:

```markdown
- Verify beyond unit tests: run lint, typecheck, tests, then exercise the real behavior path if the task has one. Copy test commands and their working directory from the project's AGENTS.md; never run a test runner from a directory that lacks its package manifest (package.json, pyproject.toml): a bare-root run crawls sibling packages and worktrees and reports false failures. Scope: targeted tests covering the files you changed, not the full suite; broader scope is the reviewer's call. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

### 2. `agents/reviewer.md`, insert after the "Two passes" list (before the Return-format paragraph)

```markdown
Test runs: take the command, working directory, and scope from the project's AGENTS.md (where a reviewer fast-path is documented, e.g. `npx vitest run --changed main` from `frontend/`, use it). Targeted-first: re-check tests covering the diff; run the full suite only when targeted coverage is unclear or the branch is about to merge. Never run a test runner from a directory that lacks its package manifest.
```

### 3. `commands/execute-plan.md`, bullet at line 16

Replace with:

```markdown
- Verify beyond unit tests: run the project's lint / typecheck / unit tests (commands, working directory, and scope per the project's AGENTS.md; targeted tests covering the changed files, never a runner invoked from a directory that lacks its package manifest), then, if the task has a user-facing or integration behavior, exercise the actual path (start the dev server, hit the endpoint, open the route); passing unit tests are necessary, not sufficient. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

### 4. Machine-local sync (activation, no commit)

Per `agents/README.md` line 3 and the AGENTS.md sync table:

- `agents/executor.md`, `agents/reviewer.md` to `~/.config/opencode/agents/`
- `commands/execute-plan.md` to `~/.config/opencode/command/` (singular, opencode)

Verify with hash comparison per file pair. Activation requires an opencode restart (config loads once at startup); the report must state this.

## Verification

1. Repo hooks enforce em-dash and frontmatter rules at commit; additionally run the explicit em-dash scan over the three edited files.
2. `opencode agent list` parses and `opencode debug agent executor` / `opencode debug agent reviewer` resolve (agents/README.md maintenance note).
3. Synced copies hash-identical to repo sources.
4. No test suite exists in this repo; the behavioral effect (next hermes-console plan run uses `frontend/` cwd and targeted scope) is observable only in future runs. The execution report lists this as Unverified-in-advance with the observable to watch: reviewer/executor logs should show `cd frontend` invocations and no bare-root `npx vitest run`.

## Risks

- Wording drift between the three copies of the rule: accepted; each audience needs its own phrasing. Keep each addition under ~80 words.
- Token growth in agent bodies: negligible (about 60 words each); agent files have no hard size limit (agents/README.md measures startup context, not per-file caps).
- Sync is machine-local and silent: if skipped, the fix stays inactive. The plan makes it a separate task with hash verification, after review passes, so a rejected wording never gets synced.
