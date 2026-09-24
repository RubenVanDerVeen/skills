# Commit Race Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This repo's parallel-dispatch rules (agents/orchestrator.md) supersede the skill's serial-momentum red flags. This plan has a single task; execute it through executor + reviewer as usual.

**Goal:** Close the sibling-stage race between parallel executors by making every executor commit a pathspec commit, plus an orchestrator commit-integrity check as backstop.

**Architecture:** One concern, three mirror sites. The executor's Parallel safety paragraph gains pathspec-commit discipline (git's `--only` semantics: commit exactly the task's paths, leave sibling staged entries staged); the orchestrator's Per wave paragraph gains a commit-integrity check with the proven split recipe as the backstop; the `/execute-plan` command's per-task commit bullet mirrors the discipline so every implementer dispatch carries it.

**Tech Stack:** Markdown only. Verification via Select-String greps; git hooks enforce Conventional Commits and the em-dash ban.

**Spec:** `docs/artifacts/features/parallel-plan-execution/2026-09-24-commit-race-hardening-design.md`

## Global Constraints

- No em-dashes (U+2014, `-`) in any edited file. Verify per file with `Select-String -Path <file> -Pattern ([char]0x2014)`; expected: no output.
- Canonical term: `pathspec commit`. Use it wherever the discipline is named.
- One commit for the whole task (one logical change across three mirror sites). Stage explicit paths only.
- Shell is Windows PowerShell 5.1. Work on branch `feat/parallel-plan-execution` (already checked out, clean, on-topic).
- Versioning: unversioned, no bump (root AGENTS.md has no `### Versioning` subsection).

---

### Task 1: Pathspec commits plus commit-integrity backstop

**Files:**
- Modify: `agents/executor.md:37` (Parallel safety paragraph)
- Modify: `agents/orchestrator.md:47` (Per wave paragraph)
- Modify: `commands/execute-plan.md:17` (per-task commit convention bullet)

**Depends:** none

**Interfaces:**
- Consumes: none (anchors verified against current branch state).
- Produces: the `pathspec commit` discipline; the orchestrator's commit-integrity check with split recipe `git reset --soft HEAD~1` + re-stage + pathspec commit.

- [ ] **Step 1: Amend the executor's Parallel safety paragraph**

In `agents/executor.md`, replace the sentence "Exactly one commit per task." (inside the Parallel safety paragraph) with:

```markdown
Exactly one commit per task, and always a pathspec commit (`git commit <message> -- <exact files from the task's Files block>`): git then commits exactly those paths even if a sibling task's staged entries sit in the shared index, and leaves those entries staged for the sibling's own commit; a plain `git commit` takes the whole index and can bundle a sibling's in-flight staging into your commit.
```

- [ ] **Step 2: Add the orchestrator's commit-integrity check**

In `agents/orchestrator.md`, inside the "Per wave:" paragraph, insert a new sentence directly after the Pipelined review sentence (which ends "...not a range."):

```markdown
Commit integrity: before accepting a review pass, confirm `git show --name-only <hash>` touches exactly the task's `**Files:**` paths; a commit carrying sibling paths is a verification failure, and you re-dispatch that task's executor to split it (`git reset --soft HEAD~1`, re-stage its own paths, commit again with its pathspec).
```

- [ ] **Step 3: Mirror the discipline in the command**

In `commands/execute-plan.md`, append to the per-task commit bullet (the one beginning "- Commit with Conventional Commits 1.0.0 (`feat:`, `fix:`, ..."):

```markdown
Always a pathspec commit (`git commit <message> -- <exact files from the task's Files block>`): a plain `git commit` can sweep a parallel sibling's staged files into your commit.
```

- [ ] **Step 4: Verify**

```powershell
Select-String -Path agents/executor.md,agents/orchestrator.md,commands/execute-plan.md -Pattern 'pathspec'
Select-String -Path agents/orchestrator.md -Pattern 'Commit integrity'
Select-String -Path agents/executor.md,agents/orchestrator.md,commands/execute-plan.md -Pattern ([char]0x2014)
```

Expected: `pathspec` found in all three files; `Commit integrity` found in orchestrator.md; third command returns nothing.

- [ ] **Step 5: Commit**

```powershell
git add agents/executor.md agents/orchestrator.md commands/execute-plan.md
git commit -m "fix(agents): pathspec commits close the sibling-stage race in parallel waves" -- agents/executor.md agents/orchestrator.md commands/execute-plan.md
```

(The commit itself demonstrates the discipline: a pathspec commit.)
