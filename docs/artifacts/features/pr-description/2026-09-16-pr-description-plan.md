# PR Description Standard Implementation Plan

> **For agentic workers:** Execute per /execute-plan conventions (orchestrator dispatches executor + reviewer per task, commits at task boundaries). Steps use checkbox (`- [ ]`) syntax for tracking. Spec: `docs/artifacts/features/pr-description/2026-09-16-pr-description-design.md`.

**Goal:** One standardized PR description format for every agent-created PR, delivered as a new `pr-description` skill plus condensed wiring in the close-out agents.

**Architecture:** The skills repo ships into every sbx via the `.opencode` bundle, and new skills surface in every agent by default (denylist-over-allowlist). So a single skill in this repo is the source of truth for all PR paths (sbx `PR_DESCRIPTION.md`, gateway `gh pr create`, interactive). The standard flow gets it ingrained via the documenter (close-out writer) and the orchestrator's documenter dispatch; all other sessions hit it by frontmatter description-match. Mirrors the `inventree-naming` precedent (skill = source of truth, agents embed a condensed copy).

**Tech Stack:** Markdown only. No build step, no runtime, no dependencies. Git hooks in `.githooks/` enforce frontmatter, em-dash, and catalog rules.

## Global Constraints

- No em-dashes (U+2014) anywhere, files or commit messages.
- `SKILL.md` frontmatter: `name` kebab-case matching the folder name; `description` starts with "Use when", describes only when to load, third person; total frontmatter under 1024 characters; no colon-then-space inside the YAML plain-scalar description.
- `SKILL.md` body starts with `## Overview`; no `## Skill` heading.
- Folder name, frontmatter `name`, and both catalog rows (`README.md` `## Skills` table, `AGENTS.md` `## Current skills` table) must match exactly and ship in the same commit.
- One logical change, one commit: `feat(skills): add pr-description standard for agent PRs`.
- Do not edit `PR_DESCRIPTION.md`-adjacent daemon behavior, workflow docs, or `hermes-console` (non-goal per spec).
- Branch: `feat/pr-description`. Git hooks must be active (`git config core.hooksPath .githooks`).
- Windows PowerShell 5.1 environment.

## File Structure

- Create: `skills/pr-description/SKILL.md` (the template and rules; the only new file)
- Modify: `README.md` (Skills table row + Layout block entry)
- Modify: `AGENTS.md` (`## Current skills` table row)
- Modify: `agents/documenter.md` (new step 3: PR description from the report; renumber steps 3-5 to 4-6)
- Modify: `agents/orchestrator.md` (step 8: one clause folding the PR-description requirement into the documenter dispatch)

No test files, no commands directory change (no slash command: PR creation is agent-internal, discovered by description-match).

---

### Task 1: Add the pr-description skill, catalog rows, and agent wiring

**Files:**
- Create: `skills/pr-description/SKILL.md`
- Modify: `README.md` (last row of `## Skills` table, around line 20; Layout block, around line 87)
- Modify: `AGENTS.md` (`## Current skills` table, row after `skill-harvest`, around line 130)
- Modify: `agents/documenter.md` (numbered steps, lines 50-55)
- Modify: `agents/orchestrator.md` (step 8, line 50)

**Interfaces:**
- Consumes: the documenter's execution report sections (Summary, Files changed, Verifier output, Documentation updates) as raw material for the PR description; the repo's Conventional Commits types.
- Produces: skill identity `pr-description` loadable by any agent; documenter step 3 behavior ("write PR description per the skill when the run needs a PR"); orchestrator step 8 dispatch clause. No code interfaces.

- [ ] **Step 1: Branch and hooks**

```powershell
git checkout -b feat/pr-description
git config core.hooksPath .githooks
```

Expected: branch created; the config command returns nothing (or prints `.githooks` if already set).

- [ ] **Step 2: Create `skills/pr-description/SKILL.md` with this exact content**

````markdown
---
name: pr-description
description: Use when creating or writing a pull request description, filling in PR_DESCRIPTION.md at repo root, running gh pr create, or reporting a PR url at task completion. Triggers on pull request, PR body, PR description, merge request, gh pr create, PR_DESCRIPTION.md.
---

## Overview

One standard description for every agent-created PR, whatever the path: the sbx direct path (uncommitted PR_DESCRIPTION.md at repo root, first line becomes the PR title), a gateway or interactive gh pr create, or any other agent PR.

## When to use

- The task prompt or contract asks for a PR_DESCRIPTION.md.
- You are about to run gh pr create or fill in a PR body.
- A task contract wants a PR url reported at completion.

## Template

First line is the PR title: a Conventional Commits 1.0.0 subject, `<type>(<scope>): <description>`, using the repo's types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert). Then:

    ## Problem
    The problem or reason for the change. Link the issue or task source (Plane issue, GitHub issue) when one exists. One short paragraph.

    ## What changed and why
    Technical summary, grouped per change or area: what changed, and the why. Commits and diff stats when useful. No file-list dump; the diff is one click away.

    ## Verification
    How it was verified: commands run and their outcome (verifier output, tests, dry-runs). Evidence, not claims. Name what stayed unverified.

    ## Docs
    Catalogs and docs updated alongside (README or AGENTS tables, CHANGELOG, command sections). Write None when nothing changed.

## Rules

- Every section present; write None when a section has no content. Never drop a section.
- Derive the description from the execution report when one exists; it already carries the same information.
- On the sbx path, keep PR_DESCRIPTION.md uncommitted at repo root (the daemon amends committed copies out of the push).
- No em-dashes.
````

- [ ] **Step 3: Add the catalog rows**

In `README.md`, append to the `## Skills` table after the `skill-harvest` row:

```markdown
| [`pr-description`](./skills/pr-description/SKILL.md) | Standardized description for agent-created PRs. Conventional Commits title line plus Problem, What changed and why, Verification, Docs sections. |
```

In `README.md`, in the Layout code block, change the last skills-tree entry from `└── skill-harvest/` to `├── skill-harvest/` and append after its `references/extraction.md` line:

```text
    └── pr-description/SKILL.md
```

In `AGENTS.md`, append to the `## Current skills` table after the `skill-harvest` row:

```markdown
| `skills/pr-description/` | `pr-description` | Standardized description for agent-created PRs. Conventional Commits title line plus Problem, What changed and why, Verification, Docs sections. |
```

- [ ] **Step 4: Wire the documenter**

In `agents/documenter.md`, insert this as step 3 (right after the report-writing step 2), and renumber the existing steps 3, 4, 5 to 4, 5, 6:

```markdown
3. If the run requires a PR description (the sbx contract's `PR_DESCRIPTION.md` at repo root, or a `gh pr create` body), write it from the report following the `pr-description` skill: first line a Conventional Commits subject (it becomes the PR title), then the Problem, What changed and why, Verification, Docs sections. Keep `PR_DESCRIPTION.md` uncommitted at repo root.
```

The renumbered old steps keep their text unchanged: catalogs (now 4), commit (now 5), return (now 6).

- [ ] **Step 5: Wire the orchestrator**

In `agents/orchestrator.md` step 8, extend the dispatch-material parenthetical. Change:

```markdown
(plan and spec paths, per-task commit list, doc-standardizer and code-standardizer findings and what was fixed, verifier output, dispatch log)
```

to:

```markdown
(plan and spec paths, per-task commit list, doc-standardizer and code-standardizer findings and what was fixed, verifier output, dispatch log, plus the PR-description requirement when the task needs a PR)
```

- [ ] **Step 6: Verify**

```powershell
(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))
```

Expected: no output (no em-dashes anywhere).

```powershell
Select-String -Path README.md, AGENTS.md -Pattern "pr-description"
```

Expected: at least one row hit in each file (README Skills table + Layout block; AGENTS Current skills table).

```powershell
opencode agent list
```

Expected: lists agents, no parse errors (validates both edited agent files).

Frontmatter self-check: `name: pr-description` matches the folder; description starts with "Use when"; no colon-then-space inside the description scalar; body starts with `## Overview`.

- [ ] **Step 7: Commit (single commit for the whole feature)**

```powershell
git add skills/pr-description/SKILL.md README.md AGENTS.md agents/documenter.md agents/orchestrator.md
git commit -m "feat(skills): add pr-description standard for agent PRs"
```

Expected: pre-commit and commit-msg hooks pass (frontmatter, em-dash, catalog presence, Conventional Commits). If a hook rejects, fix the named issue and commit again.

---

## Verification summary (for the reviewer)

- `skills/pr-description/SKILL.md` exists, frontmatter and body follow the Global Constraints, content matches the spec's template verbatim.
- Both catalogs carry a matching row; README Layout block includes the new folder.
- `agents/documenter.md` has 6 numbered steps with the new step 3 in place and no renumbering gaps.
- `agents/orchestrator.md` step 8 carries the new clause and nothing else changed.
- Em-dash scan empty; `opencode agent list` parses.
- One commit on `feat/pr-description` with the exact message above.
