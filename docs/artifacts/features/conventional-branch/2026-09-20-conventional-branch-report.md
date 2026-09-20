# Conventional Branch adoption: execution report

Date: 2026-09-20
Branch: `docs/conventional-branch` (base `main`)
Plan: `docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-plan.md`
Spec: `docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-design.md`

## Summary

Conventional Branch 1.1.0 is now a named standard in this repo, not just an implicit habit. Both `STANDARDS.md` copies (root and `project-standardization` template) carry a Stack row, a full branch-naming section, and a References link; the repo's extra types (`docs/`, `refactor/`, `test/`, `ci/`) and the `feat/<slug>-spN-<name>` multi-plan suffix are documented as spec-sanctioned custom extensions. The branch-creating agents now apply the convention by default: the `AGENTS.md` branch bullet, `agents/orchestrator.md`, `commands/execute-plan.md`, and all three `templates/AGENTS-*.md` point at `STANDARDS.md`, and the legacy `plan-<name>` scheme (no type prefix, invalid per spec) is gone from living docs. `references/standards-stack.md` adds Conventional Branch to the always-apply floor, and `CHANGELOG.md` records the adoption. All 5 tasks plus one verifier quick-fix landed; both standardizers passed (one quick-fix resolved); the final 4-check sweep is green.

## Branch and commits

| Hash | Subject |
|---|---|
| `2029b79` | `docs: add plan and spec for conventional-branch` (bootstrap, per orchestrator's branch-first rule) |
| `99a6a05` | `docs(standards): adopt conventional branch 1.1.0` (Task 1) |
| `63201ea` | `docs(standardization): add conventional branch to STANDARDS template` (Task 2) |
| `767bed1` | `docs(agents): apply conventional branch naming by default` (Task 3) |
| `d63a451` | `docs(standardization): add conventional branch to standards stack and templates` (Task 4) |
| `745f116` | `docs(changelog): note conventional branch adoption` (Task 5, steps 1-2) |
| `a9f0fbb` | `docs(plan): align verifier #3 with changelog history-note carve-out` (code-standardizer quick-fix) |
| (this commit) | `docs(artifacts): add conventional-branch execution report` |

Base: `main`. Branch is local-only; not pushed, no PR. All commits passed the tracked pre-commit hooks without `--no-verify` (`core.hooksPath` resolves to `.githooks`).

## Files changed (diff stats)

Lifetime of the branch vs `main` (12 files, 523 insertions, 7 deletions):

```
 AGENTS.md                                                                             | 2 +-
 CHANGELOG.md                                                                          | 1 +
 STANDARDS.md                                                                          | 33 +++
 agents/orchestrator.md                                                                | 2 +
 commands/execute-plan.md                                                              | 2 +-
 docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-design.md  | 66 +++
 docs/artifacts/features/conventional-branch/2026-09-20-conventional-branch-plan.md    | 382 +++
 skills/rubens-project-standardization/references/standards-stack.md                   | 17 +-
 skills/rubens-project-standardization/templates/AGENTS-large.md                       | 2 +-
 skills/rubens-project-standardization/templates/AGENTS-medium.md                      | 2 +-
 skills/rubens-project-standardization/templates/AGENTS-small.md                       | 2 +-
 skills/rubens-project-standardization/templates/STANDARDS.md                          | 19 +
```

Grouped by commit:

- `2029b79` (bootstrap): adds the spec and plan under `docs/artifacts/features/conventional-branch/` (new directory, 2 new files). The plan file's 382-line insert count includes the later `a9f0fbb` in-branch edit (2 lines), collapsed by diffing against the merge base.
- `99a6a05` (Task 1): `STANDARDS.md` (Stack row, branch section, References link).
- `63201ea` (Task 2): `skills/rubens-project-standardization/templates/STANDARDS.md` (generic Stack row, section, References link).
- `767bed1` (Task 3): `AGENTS.md` branch bullet, `agents/orchestrator.md` branch-first sentence, `commands/execute-plan.md` parenthetical.
- `d63a451` (Task 4): `references/standards-stack.md` (floor list, subsection, how-to-apply floor) plus the identical branch-bullet replacement in `templates/AGENTS-small.md`, `AGENTS-medium.md`, `AGENTS-large.md`.
- `745f116` (Task 5): `CHANGELOG.md` Added entry.
- `a9f0fbb` (quick-fix): plan file only, Task 5 Step 3 check #3 (2 lines: comment text and the `-notmatch` clause gained `|CHANGELOG`).

This commit adds the report you are reading alongside the plan and spec. No new files outside `docs/artifacts/`.

## Standardization review

**doc-standardizer:** PASS, no findings. Branch state matches every convention the `project-standardization` skill enforces for markdown-only repos. Nothing to fix.

**code-standardizer:** PASS overall, one `quick-fix` finding. The plan's own Task 5 Step 3 check #3 was narrower than the design's carve-out: the design allows `plan-<name>` remnants in "changelog history notes", but the verifier only excluded `docs\artifacts\`, so running it as written flagged the legitimate `CHANGELOG.md:36` entry. RESOLVED in commit `a9f0fbb`, which widened the verifier's `-notmatch` to `docs.artifacts|CHANGELOG` (executor applied it, reviewer passed it). No recommendations remain open.

## Documentation updates

None required, confirmed by inspecting the diff (`git diff --name-status main...HEAD`): 10 modified files, all existing living docs, plus 2 added artifact files (spec, plan). The change:

- Adds no skill folder or `SKILL.md`: `README.md` `## Skills` and `AGENTS.md` `## Current skills` tables are untouched and correct as-is.
- Adds no `commands/*.md`: the `commands/execute-plan.md` edit is a one-clause change to an already-cataloged command; its parent skill's `## Commands` section still lists it accurately.
- Adds no `agents/*.md`: the `agents/orchestrator.md` edit is a one-sentence change to an already-rostered agent; `agents/README.md` needs no row.
- Touches no name listed in `opencode-install.md`'s `## Verify` section, and no external skill: `external-skills.md` is unaffected.
- The edits inside `skills/rubens-project-standardization/` (references and templates) change the skill's reference content, not its identity: frontmatter `name` (`project-standardization`) and description are unchanged, so no catalog row changes.

Catalog drift check at close-out: no skill, command, or agent exists that is missing from its catalog. No drift.

## Verification

Task 5 Step 3 final sweep, run by the orchestrator after all task commits (condensed raw output):

```
=== VERIFICATION 1: em-dash ban repo-wide (must be empty) ===
(empty)
=== VERIFICATION 2: Conventional Branch in all 7 living docs ===
STANDARDS.md:25, :90, :220                                    (Stack row, section, References)
skills\...\templates\STANDARDS.md:25, :91, :208               (Stack row, section, References)
AGENTS.md:194                                                 (branch bullet)
agents\orchestrator.md:45                                     (Branch-first sentence)
commands\execute-plan.md:11                                   (Setup step 2 parenthetical)
skills\...\references\standards-stack.md:5, :138, :185        (Scope reminder, subsection, floor)
CHANGELOG.md:36                                               (Added entry)
=== VERIFICATION 3: legacy plan-<name> outside carve-outs ===
Hits only in docs/artifacts (append-only history) and CHANGELOG.md:36 (history note,
sanctioned by design + widened verifier). Verifier as amended returns empty.
=== VERIFICATION 4: branch name ===
docs/conventional-branch
```

All four checks pass: (1) empty, (2) hits in all 7 living docs, (3) empty after the sanctioned carve-outs, (4) `docs/conventional-branch` (itself Conventional Branch compliant: `docs/` is a documented project extension type). Per-task verifiers (Tasks 1-4 Step 4/5 checks) also passed at their commits, per reviewer sign-offs.

## Skills loaded

- Orchestrator: followed the executing-plans and subagent-driven-development conventions from its system prompt; no `skill` tool calls needed (each dispatch carried its own context).
- Executors, reviewers, standardizers: none loaded; worked from the plan's verbatim replacement text and their agent definitions.
- Documenter (this report): none loaded; followed the `agents/documenter.md` definition.
- Ponytail mode active at `full` intensity throughout.

## `ponytail:` deferrals

None. Every step was executed as planned; no shortcuts were taken that need a `ponytail:` comment. The plan itself was already the minimal version: markdown edits only, no hooks (hook enforcement was rejected in the design as machinery nobody asked for).

## Unverified items

None. All checks green, both standardizers closed out, no sync-dependent caveats (the touched agent/command files are source-of-truth edits; the standard sync step from `opencode-install.md` applies to them as usual, which is routine, not unverified).

## Dispatch Log

| Task / phase | Dispatched as |
|---|---|
| Bootstrap commit (branch + spec/plan) | orchestrator (setup, not implementation) |
| Task 1: root `STANDARDS.md` | executor + reviewer: PASS |
| Task 2: template `STANDARDS.md` | executor + reviewer: PASS |
| Task 3: agent defaults (`AGENTS.md`, orchestrator, execute-plan) | executor + reviewer: PASS |
| Task 4: standards-stack + AGENTS templates | executor + reviewer: PASS |
| Task 5 steps 1-2: CHANGELOG entry | executor + reviewer: PASS |
| Task 5 Step 3: final verification sweep | orchestrator |
| Structure audit (docs) | doc-standardizer: PASS, no findings |
| Structure audit (code) | code-standardizer: PASS, 1 quick-fix |
| Quick-fix: plan verifier carve-out (`a9f0fbb`) | executor + reviewer: PASS |
| Execution report + commit (this file) | documenter |

Zero oracle escalations (no task failed verification twice).
