# Design: `/standardize` explore-patch-verify flow + grep-gated bootstrap

- **Date:** 2026-08-12
- **Topic:** `standardize-flow`
- **Scope:** the `project-standardization` skill, its `references/bootstrap.md`, and the `/standardize` command.
- **Status:** design, awaiting user review.

## Overview

Restructure the `/standardize` command so that running it against an existing project (a restructure) goes through a three-subagent explore-patch-verify flow instead of a single linear agent. Add a literal-grep verification gate to every step of `references/bootstrap.md` so that step-close is defined by a runnable command, not by memory. Fresh bootstraps stay on the existing single-agent linear path; the multi-agent flow only triggers when existing scaffolding is detected.

## Problem

The 2026-08-12 bootstrap of `klad` missed three things the standard requires: the SemVer 2.0.0 reference in the `CHANGELOG.md` header, the SemVer row in the `STANDARDS.md` stack table, and the on-disk migration of legacy artifact buckets to `docs/artifacts/features/`. The skip report (`docs/artifacts/reviews/2026-08-12-bootstrap-semver-skip-report.md`) names the root cause as **discipline failure, not tooling failure**: the agent substituted session-cached reads for at-step verification, and wrote positive confirmations without a positive check.

A second, structural cause sits under the discipline one: the bootstrap has no machine-checkable definition of done per step. "Verify X is present" is prose, so the verifying agent has nothing concrete to run, which makes the memory shortcut cheap to take.

## Goals

1. A restructure run cannot close a bootstrap step without a runnable check that proves it. The check is a literal `Select-String` / `Test-Path` / `Get-ChildItem` command whose output is captured in the run report.
2. The verifying agent has a fresh context, so it cannot lean on a read the patching agent did earlier in the session.
3. Fresh bootstraps (no prior state) keep the cheap linear path. They pay no extra dispatch cost.
4. Single source of truth: the same per-step verification predicates are read by both the fresh path and the restructure verify phase.
5. Future additions to the standard (a new "where this must appear" requirement) only need to be added in one place (`bootstrap.md`) to be enforced on both paths.

## Non-goals

- Filesystem migration of legacy artifact buckets (`docs/artifacts/{specs,plans,multi-plans}` and the like). That stays in `/standardize-migrate`. The restructure flow flags the mismatch and stops; it does not move files inline.
- Changing the tier taxonomy, the standards stack, or the AGENTS.md templates' content.
- Adding a restructure flag to the command. Branching is auto-detected.
- Any change to `/standardize-migrate` or `/standardize-code`.

## Design

### Branch detection in `/standardize`

Triage (existing bootstrap step 1) already reasons about project state. It now also emits a branch decision:

- **Fresh:** no `AGENTS.md` at repo root (or an `AGENTS.md` that is clearly not agent-context). Run the existing linear 12-step flow, single agent.
- **Restructure:** an existing `AGENTS.md` is detected. Branch into the explore-patch-verify flow (below).

Detection predicate: `Test-Path AGENTS.md`. If true, restructure; if false, fresh. The tier choice (small/medium/large) is orthogonal and still made on both paths.

### The grep-gate (single source of truth)

Each numbered step in `references/bootstrap.md` gains a `Verification:` sub-bullet naming the literal command(s) that close the step. The fresh path runs them inline as it walks the steps; the restructure verify phase re-runs them with a fresh context. Example, for the step that failed in klad:

> **8.1** ... **Verification:** closes IFF `Select-String -Pattern 'SemVer 2.0.0' AGENTS.md, CHANGELOG.md, STANDARDS.md` returns at least one hit in each file.

Predicates are expressed as Windows PowerShell (`Select-String`, `Test-Path`, `Get-ChildItem`) because that is the active shell. Where a step is a reasoning step with no project-file footprint (tier choice, "read the tier reference", "apply standards decision"), the predicate is explicitly marked `reasoning step, no grep predicate` so the gap report can still account for the step rather than silently skipping it.

### The restructure flow: explore, patch, verify

Three subagent dispatches, run as the `orchestrator` agent per the `/execute-plan` convention.

**Explore** (dispatch to `explore` subagent, read-only):
- Input: `references/bootstrap.md` (with its new verification predicates) and the project path.
- Action: run every step's verification predicate against the project. Produce a gap report: per step, `pass` / `fail` / `reasoning step, skipped`, plus the literal command output for each fail.
- Output: the gap report as structured markdown. No edits to the project.
- The report specifically catches *additions to the standard since the project was last bootstrapped* (the klad SemVer case): anything the current `bootstrap.md` requires that the project does not yet satisfy.

**Patch** (dispatch to `executor` subagent):
- Input: the gap report.
- Action: apply the scaffold/edits needed to close each `fail`. Follow the restructure rules already in `bootstrap.md`'s closing paragraph: upgrade stale sections against the current template; flag filesystem mismatches to the user; do **not** move files inline. Apply `ponytail` per `/execute-plan` conventions (shortest diff, no speculative abstraction).
- Output: the list of files edited, with a one-line note per gap closed.
- Commit policy: per `/execute-plan`, the carve-out sanctions per-task commits. One commit per cohesive gap cluster is fine (e.g. all SemVer-touching edits in one `docs(standards): wire SemVer into changelog/standards/agents` commit).

**Verify** (dispatch to `reviewer` subagent, read-only):
- Input: the gap report (the `fail` list) and the project path.
- Action: re-run every predicate that was `fail` in explore. Confirm each flipped to `pass`. Fresh context: the reviewer must not trust the patch agent's claims, only the literal command output it runs itself.
- Output: per-predicate `closed` / `still-fail`, with the literal command output.
- Failure loop: any `still-fail` goes back to `executor` for that gap. Two-strike failure on the same gap escalates to `oracle` per `/execute-plan`.

### Filesystem-move half stays out

Legacy artifact buckets flagged by explore (e.g. `docs/artifacts/specs/`, `plans/`, `multi-plans/` coexisting with the canonical `features/` layout) are reported as `flag, not fail`. The verify phase confirms they were *flagged to the user*, not that they were moved. Moving them is `/standardize-migrate`.

### Files touched by this design

| File | Change |
|------|--------|
| `skills/rubens-project-standardization/references/bootstrap.md` | Add `Verification:` sub-bullet (literal grep) under each numbered step. Make the fresh/restructure branch explicit at the top of the file. |
| `skills/rubens-project-standardization/references/restructure-flow.md` | NEW. The 3-subagent dispatch protocol (explore/patch/verify, inputs/outputs, failure loop, oracle escalation). Separate file so the fresh path never loads it; fresh-bootstrap token budget unchanged. |
| `commands/standardize.md` | Update body: triage detects branch; fresh runs linear per `bootstrap.md`; restructure runs `references/restructure-flow.md`. Stays short, does not reimplement the skill. |
| `skills/rubens-project-standardization/SKILL.md` | Add `restructure-flow.md` row to the References table. |
| `README.md`, top-level `AGENTS.md` current-skills table | No change. Enhancement to an existing skill, not a new skill. |

## Verification predicates (draft, per bootstrap step)

These are authored in the implementation. The exact commands land in `bootstrap.md`. Drafts here so the design is reviewable.

| Step | Predicate (closes IFF) |
|------|------------------------|
| 1. Triage | reasoning step, no grep predicate. Tier choice recorded in AGENTS.md overview. |
| 2. Read tier reference | agent-internal, no project footprint. Not audited. |
| 3. Apply standards | decision step. Application is verified via step 9 (STANDARDS.md rows). |
| 4. AGENTS.md + CLAUDE.md shim | `Test-Path AGENTS.md` AND `Test-Path CLAUDE.md` AND `Select-String -Pattern '@AGENTS.md' CLAUDE.md` returns >= 1. |
| 5. `.agents/` (medium+large) | tier small: skip. medium+: `Test-Path .agents` AND `Get-ChildItem .agents/*.md` returns >= 1. |
| 6. `docs/artifacts/` | `Get-ChildItem -Directory docs/artifacts` returns `features` and `reviews`. Legacy siblings (`specs`, `plans`, `multi-plans`) = flag, not fail. |
| 7. Memory | `Test-Path MEMORY.md` (or tool-specific path) AND file is non-empty. |
| 8. CHANGELOG.md | `Test-Path CHANGELOG.md` AND `Select-String -Pattern 'Keep a Changelog' CHANGELOG.md` >= 1. |
| 8.1 Versioning (ships versions) | `Select-String -Pattern 'SemVer 2.0.0' AGENTS.md, CHANGELOG.md, STANDARDS.md` >= 1 in each. |
| 9. STANDARDS.md | `Test-Path STANDARDS.md` AND every standards row has a non-empty yes/no cell (no `?` or blank). |
| 10. commit-msg hook | `Test-Path .githooks/commit-msg` AND `git config core.hooksPath` returns `.githooks`. |
| 11. graphify | conditional. IFF `Test-Path graphify-out/graph.json` OR `command -v graphify` succeeds: AGENTS.md contains a Knowledge graph section AND `.gitignore` contains `graphify-out/`. |
| 12. Token budget | soft. Agent runs `/context` (opencode) or equivalent, reports token count, confirms under tier budget. |

## Risks

- **Predicate rot.** When a standard evolves, the predicate in `bootstrap.md` must evolve with it. Mitigation: the rule "add the predicate in the same edit as the standard" gets added to the skill's contributor notes (the `## Adding or modifying a standard` section, new). Single file, single edit.
- **Reasoning steps are ungreppable.** Triage and apply-standards are judgment, not file state. The flow marks them explicitly so they appear in the gap report as accounted-for rather than silently dropped. They cannot fail verification.
- **Over-delegation on a doc task.** Three dispatches per restructure is the floor for the fresh-context guarantee. Going below it (one agent) reintroduces the memory shortcut. Going above it (per-step) is the rejected Approach A.
- **Cross-platform predicates.** Predicates are written for Windows PowerShell (active shell). If the flow is later run on POSIX, the `explore` agent translates `Select-String` to `grep` and `Test-Path` to `test -f`. The intent is identical; the literal command is the shell's equivalent. Note this in `restructure-flow.md`.

## Validation

The klad repo (`C:\Users\ruben\Projects\Tools\klad`) is the first end-to-end exercise of the flow, folded into the implementation plan as its final task. The run must produce an honest 12-step gap report (per-step pass/fail/flag with literal command output), close every real fail through the patch and verify phases, flag (not move) the legacy artifact buckets, and commit the pending SemVer fix set the skip report describes as "fixed in commit not yet made". Predicate defects discovered against the real project are fixed on the feature branch in the same run. The gap report and closure evidence land in the skills repo's execution report; klad gets its commits but no new report file.

## Open questions

None. Branch logic and verify agent confirmed with the user on 2026-08-12; klad validation task added at the user's direction before dispatch.
