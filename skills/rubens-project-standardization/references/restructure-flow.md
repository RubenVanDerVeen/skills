# Restructure flow: explore, patch, verify

When `/standardize` detects an existing `AGENTS.md` (restructure, not fresh bootstrap), the run branches into a three-subagent flow. Run this flow as the `orchestrator` agent. Each phase is a separate subagent dispatch with a fresh context, so the verify step cannot inherit the patch step's assumptions.

## Why three agents

The klad bootstrap skip report (2026-08-12) showed the failure mode this flow exists to prevent: a single agent substitutes a session-cached read for an at-step verification, then writes "already present" without a grep. Splitting patch from verify means the verifying agent has no memory of what the patching agent did; it must re-run the literal predicate. The verify agent's positive check is the whole point, and that property only holds when the context is fresh.

## Explore (dispatch to `explore`, read-only)

Input: `references/bootstrap.md` and the project path. Action: run every step's `Verification:` predicate against the project, marking each step `pass`, `fail`, or `reasoning step, skipped` (for steps 1, 2, 3 which have no grep predicate). Output: a gap report as structured markdown, one row per step (`step | status | predicate output`), with the literal command output pasted for every `fail`. The explore agent does not edit the project.

The explore phase specifically catches additions to the standard since the project was last bootstrapped: anything the current `bootstrap.md` requires that the project does not yet satisfy. That is the klad-class failure: the standard moved forward, the project did not.

## Patch (dispatch to `executor`)

Input: the gap report. Action: apply the scaffold or edits needed to close each `fail`. Follow the restructure rules in `bootstrap.md`'s closing paragraph: upgrade stale sections against the current template, flag filesystem mismatches to the user, do NOT move files inline (filesystem migration is `/standardize-migrate`). Apply `ponytail`: shortest working diff, no speculative abstraction, mark shortcuts with `ponytail:` comments where relevant.

Output: the list of files edited, with a one-line note per gap closed. Commit policy is per-cluster under the plan-execution carve-in: one commit per cohesive gap group, for example all SemVer-touching edits ship in one `docs(standards): wire SemVer into changelog/standards/agents` commit.

## Verify (dispatch to `reviewer`, read-only)

Input: the gap report (the `fail` list) and the project path. Action: re-run every predicate that was `fail` in explore, confirming each flipped to `pass`. Fresh context: do not trust the patch agent's claims, only the literal command output you run yourself. Output: per-predicate `closed` or `still-fail`, with the literal command output.

Failure loop: any `still-fail` goes back to `executor` for that gap. Two-strike failure on the same gap escalates to `oracle` (read-only consult) per the `/execute-plan` convention; fold the oracle's recommendation into the next executor dispatch.

## Filesystem-move half is out of scope

Legacy artifact buckets flagged by explore (for example `docs/artifacts/specs/`, `plans/`, `multi-plans/` coexisting with the canonical `features/` layout) are `flag, not fail`. The verify phase confirms they were flagged to the user, not that they were moved. Moving them is `/standardize-migrate`.

## Cross-platform predicates

Predicates in `bootstrap.md` are written for Windows PowerShell (the active shell): `Select-String`, `Test-Path`, `Get-ChildItem`. On POSIX, the explore and verify agents translate: `Select-String` becomes `grep`, `Test-Path` becomes `test -f` / `test -d`, `Get-ChildItem` becomes `ls` / `find`. The intent is identical; the literal command is the shell's equivalent. When in doubt, paste the actual command you ran into the gap report.
