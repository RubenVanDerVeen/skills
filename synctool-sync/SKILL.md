---
name: synctool-sync
description: Use when the user asks to sync, push, pull, or back up a directory to/from their NAS, or to run a SyncTool job. Drives the `synctool` CLI on the user's Windows/Linux dev machine. Triggers include "sync X to NAS", "push/pull this job", "run a sync", "back up to NAS", "synctool".
---

# synctool-sync skill

## Overview

Drive the `synctool` CLI to run the user's saved NAS sync jobs on their behalf. Syncs are single-direction (push = local->remote, pull = remote->local) in one of three modes: `copy`, `update`, `mirror`. **Mirror is destructive** (deletes dest files missing from source). This skill runs copy/update for the user but never executes a destructive mirror.

## Prerequisite

`synctool` must be on PATH. Check with `synctool --help`. If it is missing, tell the user to install it once (do NOT attempt the build yourself unless asked — the dev machine uses MinGW and needs MSYS2 on PATH):

```
# from the SyncTool repo, with MSYS2 on PATH (Windows):
cargo install --path crates/synctool-cli
```

## Hard rails — never violate

- **Always pass `--push` or `--pull`.** A bare `run`/`dry-run` opens an interactive direction prompt that hangs a non-interactive agent. If the user did not state a direction, ask.
- **Always `dry-run` before any live `run`.** Show the deltas and get the user's explicit approval first.
- **Never run a `mirror` job.** Mirror deletes files and requires a typed job-id stdin confirm. Dry-run only, then hand the exact command back to the user. Mirror jobs are tagged `[DESTRUCTIVE]` in `list`.

## Workflow

1. `synctool list` — enumerate jobs. Columns: `ID  MODE  NAME`; `[DESTRUCTIVE]` marks mirror jobs.
2. Pick the target job + direction. If unstated, ask which side wins (push = local->remote, pull = remote->local).
3. `synctool dry-run <id> --push|--pull` — read-only preview. Report the trailing `Summary: N add, N update, N delete` and any `SELECTION DRIFT` line.
4. **copy/update only:** after the user explicitly approves the dry-run, run `synctool run <id> --push|--pull`.

### Scoping to a subpath (copy/update jobs)

To sync only part of a job, pass `--subdir <REL>` (repeatable; a dir or file relpath under the job source) and/or `--exclude <REL>` (repeatable carve-out) on both `dry-run` and `run`. Use this when the user wants one folder of a broad job, e.g. just `Tools/skills` of a whole-`Projects` job:

```
synctool dry-run projects-to-nas --push --subdir Tools/skills
synctool run     projects-to-nas --push --subdir Tools/skills
```

`--exclude` without `--subdir` means "whole side minus these". Paths are validated against the source; a missing relpath errors out. **`--subdir`/`--exclude` are rejected on mirror jobs** — mirror runs whole-job only, so scoping is a copy/update feature.
5. **mirror:** stop. Show the dry-run deltas (especially deletions), then give the user the command to run themselves and tell them they must type the job id at the confirm prompt.
6. Report the final `Done: N add, N update, N delete`. Logs land in `<log_dir>/<id>-<ISO-ts>.log`.

### Drift gate

If the dry-run printed `SELECTION DRIFT`, the live `run` will prompt `[y/N]` on stdin and hang you. Call the drift out to the user; only after they approve, pipe the confirm so the run does not block:

- PowerShell: `"y" | synctool run <id> --push`
- bash: `echo y | synctool run <id> --push`

## Delete counts are mode-dependent

A `dry-run` of a **copy** or **update** job can show `- ` lines and a non-zero delete count. Those are extra files already in the destination — copy/update **keep** them; they are **not** deleted. Only **mirror** actually deletes. Never tell the user a copy/update sync will delete files.

## Scope

The CLI runs **saved jobs only**, but `--subdir` can scope a run to a subpath *within* a job's source (see Scoping above). There is still no ad-hoc / Quick Sync from the CLI (GUI-only): to sync a path not covered by any job's source tree, tell the user to use the SyncTool app or create a job first.

## Quick reference

| Goal | Command |
|---|---|
| List jobs | `synctool list` |
| Preview a push | `synctool dry-run <id> --push` |
| Preview a pull | `synctool dry-run <id> --pull` |
| Run copy/update (push) | `synctool run <id> --push` |
| Scope to a subpath | `synctool run <id> --push --subdir <REL>` (repeatable; `--exclude <REL>` to carve out) |
| Run when drift was approved | `"y" \| synctool run <id> --push` |
| Mirror job | dry-run only -> hand command back to user (no `--subdir`/`--exclude`) |

## Common mistakes

- Running bare `run <id>` / `dry-run <id>` -> hangs on the direction prompt. Always pass `--push`/`--pull`.
- Skipping the dry-run -> the user cannot see the impact before files move.
- Reporting a copy/update "delete" count as real deletions -> they are kept extras.
- Auto-confirming a mirror, or piping the job id to its confirm prompt -> forbidden; a destructive mirror is the user's call.
- Building or installing `synctool` unprompted on the MinGW machine.

## Red flags — STOP

- About to run a `[DESTRUCTIVE]` / mirror job
- About to run without `--push` or `--pull`
- About to run without a dry-run first
- The user has not explicitly approved this live run

All of these mean: stop and hand control back to the user.
