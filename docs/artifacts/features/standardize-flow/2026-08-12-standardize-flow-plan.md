# `/standardize` explore-patch-verify flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (or the project's `/execute-plan` convention) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a three-subagent explore-patch-verify flow to the restructure path of `/standardize`, and gate every bootstrap step's close on a literal-grep verification predicate authored into `references/bootstrap.md`.

**Architecture:** Single source of truth: `references/bootstrap.md` gains a `Verification:` sub-bullet under each numbered step (the grep-gate). `/standardize` auto-detects fresh vs restructure via `Test-Path AGENTS.md`. Fresh runs the unchanged linear flow. Restructure dispatches `explore` (read-only audit, emits gap report) → `executor` (closes gaps) → `reviewer` (re-greps each closed predicate with fresh context). A new `references/restructure-flow.md` holds the dispatch protocol so the fresh path never loads it.

**Tech Stack:** Markdown only. No build, no runtime. Predicates are Windows PowerShell (`Select-String`, `Test-Path`, `Get-ChildItem`) with a documented POSIX translation note for cross-platform.

**Spec:** `docs/artifacts/features/standardize-flow/2026-08-12-standardize-flow-design.md`

## Global Constraints

- **No em-dashes** (U+2014) anywhere in authored content. Use commas, colons, periods, parentheses, or hyphens. Repo rule, verified by `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty.
- **Frontmatter rules:** `name` kebab-case matching folder; `description` starts with "Use when...", describes triggers only, under 1024 chars total. No change to the `project-standardization` skill's existing frontmatter (its triggers are unchanged).
- **Token budget:** the fresh-bootstrap path must not load `restructure-flow.md`. Keep `bootstrap.md` lean (it currently ships at 34 lines; the verification sub-bullets will grow it, but it loads on every bootstrap so stay terse).
- **No new top-level catalog rows** in `README.md` or `AGENTS.md` current-skills table. This is an enhancement to an existing skill, not a new skill.
- **Conventional Commits 1.0.0** per task. Scope: `standardization`. Types: `feat` for the new flow + reference, `docs` for the bootstrap.md predicate authoring if it lands alone (but it ships with the flow, so `feat`).
- **In-flight `AGENTS.md` modification on `main`:** there is an uncommitted Artifacts-section addition to the repo's own `AGENTS.md` on `main` (pre-existing, unrelated to this plan). The orchestrator must commit it separately as `docs(agents): ...` OR leave it staged/untouched before the first task commit. It must NOT be swept into any task commit. Verify with `git diff --name-only HEAD` before each task commit that `AGENTS.md` is not in the staged set.

---

### Task 1: Add grep-gate verification predicates + branch note to `bootstrap.md`

This is the foundational change. Both the fresh path (inline) and the restructure verify phase read these predicates. Without this task, tasks 2 and 3 have nothing to dispatch against.

**Files:**
- Modify: `skills/rubens-project-standardization/references/bootstrap.md`

**Interfaces:**
- Consumes: nothing (this is the source).
- Produces: a `Verification:` sub-bullet under each of the 12 numbered steps, expressed as runnable PowerShell; an explicit branch note at the top of the file. Downstream tasks (2, 3) and the eventual restructure flow both depend on this format.

**Predicates to author (one per step, exact text):**

| Step | `Verification:` sub-bullet text |
|------|---------------------------------|
| 1. Triage | `Verification: reasoning step, no grep predicate. The tier choice is recorded in the AGENTS.md overview line.` |
| 2. Read tier reference | `Verification: agent-internal, no project footprint. Not audited by the restructure flow.` |
| 3. Apply standards | `Verification: decision step. The application is verified via step 9 (every adopted standard has a non-empty yes/no cell in STANDARDS.md).` |
| 4. AGENTS.md + CLAUDE.md shim | `` Verification: `Test-Path AGENTS.md` AND `Test-Path CLAUDE.md` both return True, AND `Select-String -Pattern '@AGENTS\.md' CLAUDE.md` returns at least one hit. `` |
| 5. `.agents/` | `Verification: for small tier, skip. For medium/large, `Test-Path .agents` returns True AND `Get-ChildItem .agents -Filter *.md` returns at least one file.` |
| 6. `docs/artifacts/` | `` Verification: `Get-ChildItem -Path docs/artifacts -Directory` returns `features` and `reviews`. Legacy siblings (`specs`, `plans`, `multi-plans`) are a flag to the user, not a fail; their resolution is `/standardize-migrate`. `` |
| 7. Memory | `` Verification: `Test-Path MEMORY.md` (or the tool-specific memory path) returns True AND the file is non-empty. `` |
| 8. CHANGELOG.md | `` Verification: `Test-Path CHANGELOG.md` returns True AND `Select-String -Pattern 'Keep a Changelog' CHANGELOG.md` returns at least one hit. `` |
| 8.1 Versioning | `` Verification: `Select-String -Pattern 'SemVer 2\.0\.0' AGENTS.md, CHANGELOG.md, STANDARDS.md` returns at least one hit in EACH file. Skip entirely for sub-projects versioned through a parent. `` |
| 9. STANDARDS.md | `` Verification: `Test-Path STANDARDS.md` returns True AND every standards row has a non-empty yes/no cell (no `?` or blank cells). `` |
| 10. commit-msg hook | `` Verification: `Test-Path .githooks/commit-msg` returns True AND `git config core.hooksPath` returns `.githooks`. `` |
| 11. graphify | `Verification: conditional. IFF `Test-Path graphify-out/graph.json` OR `command -v graphify` succeeds: AGENTS.md contains a Knowledge graph section AND `.gitignore` contains `graphify-out/`. Otherwise skip.` |
| 12. Token budget | `Verification: soft. Run the tool's context indicator (opencode: `/context`), report the token count, confirm under the tier budget from SKILL.md.` |

**Branch note to add at the top of `bootstrap.md`** (after the title, before step 1):

```markdown
## Branch: fresh vs restructure

This checklist runs on two paths, decided by triage in step 1:

- **Fresh bootstrap** (`Test-Path AGENTS.md` returns False): walk the 12 steps linearly in a single agent. Run each step's `Verification:` predicate inline before moving on.
- **Restructure** (`Test-Path AGENTS.md` returns True): dispatch the three-subagent explore-patch-verify flow in `references/restructure-flow.md`. The explore and verify phases run these same predicates; the verify phase re-runs them with a fresh context.

When adding a requirement to any step below, add or update its `Verification:` predicate in the same edit. A step without a runnable predicate is a step the restructure flow cannot confirm.
```

- [ ] **Step 1: Read the current `bootstrap.md` in full**

Run: `read skills/rubens-project-standardization/references/bootstrap.md`
Expected: 34 lines, 12 numbered steps, closing `### Git section` + restructure paragraph.

- [ ] **Step 2: Insert the branch note after the title**

Insert the `## Branch: fresh vs restructure` block (text above) immediately after the `# Bootstrap checklist` title line and its existing intro paragraph, before `1. **Triage**`.

- [ ] **Step 3: Append a `Verification:` sub-bullet to each of the 12 numbered steps**

Use the exact text from the table above. For step 8.1, the sub-bullet is indented under step 8's sub-bullets (it is already a sub-step `8.1.`). For step 10, indent under the existing `10.` sub-items. For step 11, indent under the existing `11.` sub-items.

- [ ] **Step 4: Run the structural self-check**

Run: `rg --count '^\d+\.' skills/rubens-project-standardization/references/bootstrap.md` (count numbered top-level steps; expect 12).
Run: `rg --count 'Verification:' skills/rubens-project-standardization/references/bootstrap.md` (expect at least 12, since step 8.1 also has one and the branch note mentions the word).
Expected: 12 numbered steps, >= 12 `Verification:` lines.

- [ ] **Step 5: Em-dash scan**

Run: `(Get-ChildItem -Recurse -Include *.md -Path skills/rubens-project-standardization | Select-String -Pattern ([char]0x2014))`
Expected: empty output.

- [ ] **Step 6: Read-back review**

Read the modified `bootstrap.md` end to end. Confirm every numbered step has a `Verification:` sub-bullet, the predicates are runnable PowerShell, and the branch note is present and accurate.

- [ ] **Step 7: Commit**

```bash
git add skills/rubens-project-standardization/references/bootstrap.md
git commit -m "feat(standardization): gate each bootstrap step on a literal-grep verification predicate"
```

Before committing, verify `git diff --cached --name-only` returns ONLY `skills/rubens-project-standardization/references/bootstrap.md` (the in-flight `AGENTS.md` change must not be swept in).

---

### Task 2: Create `references/restructure-flow.md` and wire it into `SKILL.md`

The dispatch protocol for the restructure path. Separate file so the fresh path never loads it (token budget).

**Files:**
- Create: `skills/rubens-project-standardization/references/restructure-flow.md`
- Modify: `skills/rubens-project-standardization/SKILL.md` (References table only)

**Interfaces:**
- Consumes: `references/bootstrap.md` verification predicates (from task 1).
- Produces: `references/restructure-flow.md`, referenced by `commands/standardize.md` (task 3) and listed in `SKILL.md` References table.

**Content of `references/restructure-flow.md`** (author this file with the sections below; expand each into proper prose, no em-dashes):

```markdown
# Restructure flow: explore, patch, verify

When `/standardize` detects an existing `AGENTS.md` (restructure, not fresh bootstrap), the run branches into a three-subagent flow. Run this flow as the `orchestrator` agent. Each phase is a separate subagent dispatch with a fresh context.

## Why three agents

The klad bootstrap skip report (2026-08-12) showed the failure mode: a single agent substitutes a session-cached read for an at-step verification, then writes "already present" without a grep. Splitting patch from verify means the verifying agent has no memory of what the patching agent did; it must re-run the literal predicate. The verify agent's positive check is the whole point.

## Explore (dispatch to `explore`, read-only)

Input: `references/bootstrap.md` and the project path.
Action: run every step's `Verification:` predicate against the project. Mark each step `pass`, `fail`, or `reasoning step, skipped` (for steps 1, 2, 3 which have no grep predicate).
Output: a gap report as structured markdown. One row per step: `step | status | predicate output`. For every `fail`, paste the literal command and its output. No edits to the project.

The explore phase specifically catches additions to the standard since the project was last bootstrapped: anything the current `bootstrap.md` requires that the project does not yet satisfy.

## Patch (dispatch to `executor`)

Input: the gap report.
Action: apply the scaffold or edits needed to close each `fail`. Follow the restructure rules in `bootstrap.md`'s closing paragraph: upgrade stale sections against the current template, flag filesystem mismatches to the user, do NOT move files inline (filesystem migration is `/standardize-migrate`). Apply `ponytail`: shortest working diff, no speculative abstraction, mark shortcuts with `ponytail:` comments where relevant.
Output: the list of files edited, with a one-line note per gap closed.
Commit policy: the plan-execution carve-in sanctions per-cluster commits. One commit per cohesive gap group (for example, all SemVer-touching edits in one `docs(standards): wire SemVer into changelog/standards/agents` commit).

## Verify (dispatch to `reviewer`, read-only)

Input: the gap report (the `fail` list) and the project path.
Action: re-run every predicate that was `fail` in explore. Confirm each flipped to `pass`. Fresh context: do not trust the patch agent's claims, only the literal command output you run yourself.
Output: per-predicate `closed` or `still-fail`, with the literal command output.
Failure loop: any `still-fail` goes back to `executor` for that gap. Two-strike failure on the same gap escalates to `oracle` (read-only consult) per the `/execute-plan` convention; fold the oracle's recommendation into the next executor dispatch.

## Filesystem-move half is out of scope

Legacy artifact buckets flagged by explore (for example `docs/artifacts/specs/`, `plans/`, `multi-plans/` coexisting with the canonical `features/` layout) are `flag, not fail`. The verify phase confirms they were flagged to the user, not that they were moved. Moving them is `/standardize-migrate`.

## Cross-platform predicates

Predicates in `bootstrap.md` are written for Windows PowerShell (the active shell): `Select-String`, `Test-Path`, `Get-ChildItem`. On POSIX, the explore and verify agents translate: `Select-String` becomes `grep`, `Test-Path` becomes `test -f` / `test -d`, `Get-ChildItem` becomes `ls` / `find`. The intent is identical; the literal command is the shell's equivalent. When in doubt, paste the actual command you ran into the gap report.
```

**`SKILL.md` References table change:**

Add one row, alphabetically placed (between `references/migration.md` and `references/small.md`):

```markdown
| `references/restructure-flow.md` | Three-subagent explore-patch-verify dispatch protocol for `/standardize` on the restructure path (existing `AGENTS.md` detected) |
```

- [ ] **Step 1: Create `references/restructure-flow.md`**

Write the file with the content above, expanded to proper prose (each `##` section as 2-4 sentences). No em-dashes. No frontmatter (reference files have none; see other `references/*.md`).

- [ ] **Step 2: Add the row to `SKILL.md` References table**

Insert the `restructure-flow.md` row in alphabetical position. Verify against the existing table ordering.

- [ ] **Step 3: Verify the file is discoverable and the path is correct**

Run: `Test-Path skills/rubens-project-standardization/references/restructure-flow.md` (expect True).
Run: `rg 'restructure-flow' skills/rubens-project-standardization/SKILL.md` (expect one hit in the References table).

- [ ] **Step 4: Em-dash scan on the new file**

Run: `(Get-ChildItem -Recurse -Include *.md -Path skills/rubens-project-standardization | Select-String -Pattern ([char]0x2014))`
Expected: empty.

- [ ] **Step 5: Read-back review**

Confirm `restructure-flow.md` names all three subagents (`explore`, `executor`, `reviewer`), documents the two-strike oracle escalation, includes the cross-platform note, and states the filesystem-move exclusion. Confirm the `SKILL.md` row matches the filename exactly.

- [ ] **Step 6: Commit**

```bash
git add skills/rubens-project-standardization/references/restructure-flow.md skills/rubens-project-standardization/SKILL.md
git commit -m "feat(standardization): add restructure-flow reference for explore-patch-verify dispatch"
```

Verify `git diff --cached --name-only` returns ONLY those two files.

---

### Task 3: Update `commands/standardize.md` to describe the branch

The user-facing entry point. Stays short; does not reimplement the skill.

**Files:**
- Modify: `commands/standardize.md`

**Interfaces:**
- Consumes: `references/bootstrap.md` (task 1) and `references/restructure-flow.md` (task 2).
- Produces: updated `/standardize` body that mentions both paths.

**Current body** (for reference, lines 5-17 of the existing file): a 7-step linear list ending with "Optional tier override: `$ARGUMENTS`".

**New body** (replace the numbered list with a branch-aware version; keep the frontmatter description, which is still accurate):

```markdown
Load the `project-standardization` skill and run the full bootstrap from `references/bootstrap.md`.

1. Triage: pick the tier (small / medium / large) from README + top-level layout, AND detect the branch. State both with reasoning; ask if unsure.
   - Fresh (`AGENTS.md` absent): walk the 12 steps in `references/bootstrap.md` linearly. Run each step's `Verification:` predicate inline before moving on.
   - Restructure (`AGENTS.md` present): dispatch the explore-patch-verify flow from `references/restructure-flow.md` (explore audits state, executor patches gaps, reviewer re-verifies with fresh context).
2. Stop and confirm before each destructive step.

Optional tier override: `$ARGUMENTS` (for example `small`, `medium`, `large`).
```

- [ ] **Step 1: Replace the body of `commands/standardize.md`**

Swap the existing 7-step linear list for the branch-aware body above. Keep the YAML frontmatter unchanged (the description is still accurate: it already says "Bootstrap or restructure a project").

- [ ] **Step 2: Verify the command still parses and stays short**

Run: `rg -c '^- ' commands/standardize.md` (count top-level list items; expect the branch structure).
Run: `(Get-Content commands/standardize.md).Count` (expect under 25 lines total).

- [ ] **Step 3: Em-dash scan**

Run: `(Get-ChildItem -Recurse -Include *.md -Path commands | Select-String -Pattern ([char]0x2014))`
Expected: empty.

- [ ] **Step 4: Read-back review**

Confirm the body references both `references/bootstrap.md` and `references/restructure-flow.md`, names the two branch conditions (Fresh = AGENTS.md absent, Restructure = AGENTS.md present), and preserves the `$ARGUMENTS` tier override.

- [ ] **Step 5: Commit**

```bash
git add commands/standardize.md
git commit -m "feat(standardization): branch /standardize on fresh vs restructure detection"
```

Verify `git diff --cached --name-only` returns ONLY `commands/standardize.md`.

---

### Task 4: Validate the restructure flow against klad (end-to-end exercise)

The first real exercise of the predicates and the dispatch protocol. Runs after tasks 1-3 are committed. The orchestrator dispatches the three phases against `C:\Users\ruben\Projects\Tools\klad` (klad is the working directory; the flow definition is read from the skills repo). This task is what converts "predicates authored" into "predicates proven".

**Files:**
- Modify (in klad): whatever real gaps the explore phase finds. Expected candidates per the skip report: `.githooks/commit-msg` install (step 10), `.agents/` contents per tier, `MEMORY.md` (step 7). The exact set comes from explore, not from this plan.
- Modify (in skills repo, only if a predicate proves wrong): `skills/rubens-project-standardization/references/bootstrap.md`

**Interfaces:**
- Consumes: `references/bootstrap.md` predicates (task 1) and `references/restructure-flow.md` protocol (task 2), both read from the skills repo.
- Produces: a validated restructure flow; klad gap report + closure evidence folded into the execution report; optional `fix(standardization):` predicate corrections on the feature branch.

**Pre-flight (orchestrator, before any dispatch):**

- [ ] **Step 1: Record klad's git state and commit the pending SemVer fix set**

Run: `git -C C:\Users\ruben\Projects\Tools\klad status --short`
Expected (per the skip report): modified `AGENTS.md`, `CHANGELOG.md`, `STANDARDS.md` (the SemVer fixes, "fixed in commit not yet made"). If the status matches that shape, commit them in klad as ONE commit:

```bash
git -C C:\Users\ruben\Projects\Tools\klad add AGENTS.md CHANGELOG.md STANDARDS.md
git -C C:\Users\ruben\Projects\Tools\klad commit -m "docs(standards): wire SemVer 2.0.0 into changelog, standards, agents"
```

This plan sanctions that specific commit (the skip report describes it as pending). Any OTHER dirty files in klad: leave untouched, list them in the report. Record the pre-flight base commit: `git -C C:\Users\ruben\Projects\Tools\klad rev-parse HEAD`.

**Phase 1 - Explore:**

- [ ] **Step 2: Dispatch `explore` (read-only, workdir klad)**

Dispatch prompt: read `C:\Users\ruben\Projects\Tools\skills\skills\rubens-project-standardization\references\bootstrap.md` and `references/restructure-flow.md` from the skills repo, run every step's `Verification:` predicate against klad, produce the 12-step gap report (step | status | predicate output). Mark steps 1, 2, 3 as `reasoning step, skipped`. Legacy artifact buckets under `docs/artifacts/` are `flag`, not `fail`.

Success: the report accounts for all 12 steps, every non-reasoning step has literal command output pasted. If explore claims a pass without command output, the validation FAILS at this step; redispatch with the omission named.

**Phase 2 - Patch:**

- [ ] **Step 3: Dispatch `executor` (workdir klad)**

Dispatch prompt: the gap report. Close each `fail` per `references/restructure-flow.md`. Commit per cohesive gap cluster in klad, Conventional Commits 1.0.0; this plan sanctions those commits. Do NOT touch legacy artifact buckets (flag only). Do NOT touch anything outside the gap list. Apply ponytail: shortest working diff.

**Phase 3 - Verify:**

- [ ] **Step 4: Dispatch `reviewer` (read-only, workdir klad)**

Dispatch prompt: the fail list from explore. Re-run every predicate that was `fail`; confirm each flipped to `pass`, pasting literal output. Any `still-fail` returns to executor for that gap; two-strike on the same gap escalates to `oracle`.

**Predicate fix loop:**

- [ ] **Step 5: Correct any broken predicate in the skills repo**

If a predicate from task 1 proves wrong or unrunnable against a real project (bad pattern, wrong path, ambiguous wording), fix `skills/rubens-project-standardization/references/bootstrap.md` on the feature branch, commit as `fix(standardization): correct <step> verification predicate`, then re-run that predicate against klad. This loop is expected to fire at least once; finding zero predicate defects across a full real exercise would be surprising.

**Closure:**

- [ ] **Step 6: Verify the success criteria**

All must hold:
- Gap report accounts for all 12 steps with literal outputs.
- Every explore `fail` is `closed` in verify (or explicitly oracle-resolved, with the resolution recorded).
- Legacy buckets in klad (`docs/artifacts/{specs,plans,multi-plans}`): flagged, not moved.
- `git -C C:\Users\ruben\Projects\Tools\klad log --oneline <pre-flight-base>..HEAD` shows only Conventional-Commits messages from this task.
- `git -C C:\Users\ruben\Projects\Tools\klad diff --name-only <pre-flight-base>..HEAD` stays within the gap-list paths.

- [ ] **Step 7: Fold results into the execution report (no separate klad artifact)**

The gap report and closure evidence land inside the skills repo's execution report (see End below). klad gets its commits; it does not get a new report file from this task.

**Fallback:** if subagent dispatch depth is unavailable for phases 1-3, the orchestrator runs the phases sequentially itself. The grep-gate still holds (every claim pastes literal command output); the fresh-context property is the bonus that is lost, note it in the report.

---

## End: report

After task 4, the orchestrator (per `/execute-plan`):

1. Optional: dispatch `standardizer` against the branch diff for a structure check. Most of this plan is markdown, so a full standardizer pass may be skipped; if dispatched, expect only markdown-lint-style findings.
2. Dispatch `documenter` to write `docs/artifacts/features/standardize-flow/2026-08-12-standardize-flow-report.md` and confirm the spec + plan paths are referenced.
3. Report: branch name; commit hashes with one-line descriptions, separated by repo (skills repo: tasks 1-3 + any predicate fixes; klad: the sanctioned SemVer commit + gap-closure commits); files changed with diff stats; the literal em-dash scan output (empty); the structural grep outputs from each task's verification step; the klad gap report (12-row step | status table) and verify closure evidence; skills loaded across the run; any `ponytail:` deferrals; anything Unverified.

Do NOT merge or open a PR unless the user asks. Do NOT push klad. Stop at the report.

## Notes for the orchestrator

- The in-flight `AGENTS.md` modification on `main` (Artifacts + Git workflow section, pre-existing) is unrelated to this plan. Commit it separately as `docs(agents): add Artifacts and Git workflow sections to repo AGENTS.md` BEFORE the first task, or leave it unstaged. Never sweep it into a task commit.
- Tasks 1-3 touch only markdown in the skills repo. There is no build, no tests to run, no dev server. The "test cycle" per task is the structural grep + read-back review + em-dash scan.
- Task 4 is a cross-repo exercise: the skills repo holds the flow definition and the feature branch; klad (`C:\Users\ruben\Projects\Tools\klad`) is the target. klad commits are sanctioned ONLY for: the pre-flight SemVer fix commit (step 1) and gap-closure commits from the patch phase. Never push klad.
- After task 4, the predicates ARE exercised end-to-end. Any predicate defect found there must be fixed on the feature branch (step 5 of task 4), not deferred.
