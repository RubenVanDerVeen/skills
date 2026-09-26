# Remove Cross-Session Memory Bootstrap: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the orphaned cross-session memory mechanism (MEMORY.md seeding, format spec, tier guidance) from the project-standardization skill and every outer mention, leaving `.agents/` and AGENTS.md as the only context mechanisms.

**Architecture:** Pure deletion across markdown files in `skills/rubens-project-standardization/` plus two outer files (`commands/standardize.md`, `skills/skill-harvest/SKILL.md`). Removing bootstrap step 7 requires renumbering steps 8-12 to 7-11 and updating every step-number cross-reference. No new content is added anywhere.

**Tech Stack:** Markdown only. No build, no runtime.

**Spec:** `docs/artifacts/features/memory-bootstrap-removal/2026-09-26-kill-memory-bootstrap-design.md`

## Global Constraints

- No em-dashes (U+2014) in any markdown file, including chat-free file edits. Use commas, colons, periods, parentheses, hyphens.
- `SKILL.md` frontmatter stays valid after edits: `description` starts with "Use when", under 1024 characters total frontmatter, `name` kebab-case.
- Single commit for the whole change (repo rule: one logical change = one commit). Tasks 1 and 2 edit only; Task 3 commits.
- Branch: `feat/remove-memory-bootstrap`, created before any edit.
- Versioning: repo has no `### Versioning` section in AGENTS.md. Unversioned, no bump.
- Do NOT touch: `docs/artifacts/**` (history stays as written), `/home/ruben/projects/Tools/klad/**` (different repo, explicitly out of scope).
- Do NOT touch installed copies under `~/.config/opencode/`. Repo is source of truth; user re-syncs manually.

---

### Task 1: Remove the memory mechanism from skills/rubens-project-standardization

**Files:**
- Delete: `skills/rubens-project-standardization/references/memory.md`
- Modify: `skills/rubens-project-standardization/references/bootstrap.md`
- Modify: `skills/rubens-project-standardization/SKILL.md`
- Modify: `skills/rubens-project-standardization/references/small.md`
- Modify: `skills/rubens-project-standardization/references/medium.md`
- Modify: `skills/rubens-project-standardization/references/large.md`
- Modify: `skills/rubens-project-standardization/references/todolist.md`
- Modify: `skills/rubens-project-standardization/references/artifacts.md`
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md`

**Interfaces:**
- Consumes: none.
- Produces: none (markdown-only deletion; no later task depends on Task 1 output).

- [ ] **Step 1: Create the feature branch**

Run: `git checkout -b feat/remove-memory-bootstrap`
Expected: branch created, clean working tree (`git status` shows no staged changes).

- [ ] **Step 2: Delete the memory format spec**

Run: `git rm skills/rubens-project-standardization/references/memory.md`
Expected: file deleted from disk and staged.

- [ ] **Step 3: Remove bootstrap step 7 and renumber**

In `references/bootstrap.md`:

Delete the entire step 7 block (heading line 26 plus its body and verification sub-bullet, lines ~26-27):

```markdown
7. **Seed cross-session memory** (always): every major agent has a memory mechanism; consult the tool's docs for the path. At minimum, create a `MEMORY.md` index and a `user.md` if not present. See `references/memory.md`. Substitute the tool's path.
    - Verification: `Test-Path MEMORY.md` (or the tool-specific memory path) returns True AND the file is non-empty.
```

Then renumber the remaining steps: 8 → 7 (including sub-step 8.1 → 7.1), 9 → 8 (sub-step 9.1 → 8.1), 10 → 9, 11 → 10, 12 → 11. Update the file's own step-count phrase at line ~9 ("walk the 12 steps linearly") to "walk the 11 steps linearly". Also fix line ~19: "verified via step 9 (every adopted standard has a non-empty yes/no cell in STANDARDS.md)" → `step 8` (the STANDARDS step's new number).

- [ ] **Step 4: Update SKILL.md**

In `skills/rubens-project-standardization/SKILL.md`, five edits:

1. Line 3, frontmatter description: delete the phrase `seeding cross-session memory, ` so the clause reads `...specs/plans/reviews/reports from any framework, or applying the ISO/IEC/IEEE + industry standards stack...`. Description must still start with "Use when".
2. Line 40: `**No secrets in any tracked file**: `.env`, tokens, passwords out of git. Memory included.` → delete the trailing sentence ` Memory included.` so the line ends at `out of git.`
3. Line 42: delete the whole bullet `- **Memory ≠ plans ≠ tasks**: memory = cross-session facts; plans = committed artefacts; tasks = per-session in-tool items.`
4. Line 58: `| `references/bootstrap.md` | The 12-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS + README AI section → commit hook → graphify → verify) |` → `| `references/bootstrap.md` | The 11-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → CHANGELOG → STANDARDS + README AI section → commit hook → graphify → verify) |`
5. Line 65: delete the whole table row `| `references/memory.md` | Cross-session memory, `MEMORY.md` index, tool paths |`

Then grep the file for `step 10` (lines ~31 and ~84-85 reference "bootstrap step 10" for the git hooks). Since step 10 became step 9, change those to `bootstrap step 9`.

- [ ] **Step 5: Remove the three tier Memory sections**

- `references/small.md`: delete lines 89-96, the whole `## Memory` section (heading through the `feedback_*.md` bullet).
- `references/medium.md`: delete lines 144-153, the whole `## Memory` section.
- `references/large.md`: delete lines 135-144, the whole `## Memory` section.

Line numbers are pre-edit anchors; match on the `## Memory` heading and delete through the last line before the next `##` heading.

- [ ] **Step 6: Clean todolist.md disambiguation**

In `references/todolist.md` (~98-105):

- Heading `## When to use `todolist.md` vs in-tool task list vs memory` → `## When to use `todolist.md` vs in-tool task list`
- Delete the table row `| Memory (`project_*.md`) | Cross-session facts, decisions, deadlines. NOT tasks. |`

- [ ] **Step 7: Clean artifacts.md disambiguation**

In `references/artifacts.md`:

- Line 160: `- Reviews are **committed**, not stored in chat history or memory.` → `- Reviews are **committed**, not stored in chat history.`
- Line 243: delete the final sentence ` Memory entries remain the right home for non-constraining session context.` (the bullet then ends after the parenthetical about the Choices section).

- [ ] **Step 8: Fix the step reference in templates/STANDARDS.md**

In `templates/STANDARDS.md` line ~87: "(installed by the `project-standardization` bootstrap, step 10)" → `step 9`. (`templates/commit-msg` and `templates/pre-commit` contain no step references; nothing to edit there.)

- [ ] **Step 9: Verify Task 1**

Run: `grep -rin "memory" skills/rubens-project-standardization/`
Expected: exactly one hit, `references/restructure-flow.md:7` ("the verifying agent has no memory of what the patching agent did"), which is English prose, not the mechanism. Zero other hits.

Run: `grep -rn "12-step\|12 steps\|step 10\|step 12" skills/rubens-project-standardization/`
Expected: zero hits.

Run: `grep -rn "step 9" skills/rubens-project-standardization/`
Expected: every hit refers to the git-hooks step (SKILL.md lines ~31 and ~84-85, `templates/STANDARDS.md` line ~87). No hit refers to STANDARDS/README steps (those are now 8).

Run: `grep -n "MEMORY" skills/rubens-project-standardization/SKILL.md`
Expected: zero hits, frontmatter intact (first body heading still the skill's existing top heading; `description` still starts with "Use when").

---

### Task 2: Remove outer memory mentions (commands + skill-harvest)

**Files:**
- Modify: `commands/standardize.md`
- Modify: `skills/skill-harvest/SKILL.md`

**Interfaces:**
- Consumes: none.
- Produces: none.

- [ ] **Step 1: commands/standardize.md**

Two edits:

1. Line 2 frontmatter description: `Bootstrap or restructure a project for AI coding agents: triage tier, then apply AGENTS.md, .agents/, docs/artifacts/, memory, CHANGELOG, STANDARDS` → `Bootstrap or restructure a project for AI coding agents: triage tier, then apply AGENTS.md, .agents/, docs/artifacts/, CHANGELOG, STANDARDS`
2. Line ~8: "walk the 12 steps" → "walk the 11 steps".

- [ ] **Step 2: skills/skill-harvest/SKILL.md**

Delete line 26, the whole table row:

```markdown
| memory | fact about user or project, not process | suggest memory write |
```

Do not add a replacement row. The remaining categories (fix-skill, new-skill, config) stay.

- [ ] **Step 3: Verify Task 2**

Run: `grep -rin "memory" commands/ skills/skill-harvest/`
Expected: zero hits.

Note: `README.md` and root `AGENTS.md` were checked during design: zero memory mentions in the project-standardization rows. No edit needed. If a grep disagrees, remove the memory wording from those rows and mention it in the task report.

---

### Task 3: Full sweep, single commit

**Files:**
- Modify: none (verification and commit only).

**Interfaces:**
- Consumes: completed Tasks 1 and 2 (all edits landed on `feat/remove-memory-bootstrap`).
- Produces: one commit containing every change; final report notes.

- [ ] **Step 1: Repo-wide sweep**

Run: `grep -rin "memory" skills/ commands/ agents/ README.md AGENTS.md opencode-install.md external-skills.md`
Expected: only known English-word noise, all judged mechanism-vs-noise and left alone: `skills/altium-pro/references/troubleshooting.md` (pours in memory), `skills/deep-research/SKILL.md` (profile memory), `skills/typst-pro/SKILL.md` (generic Typst memory), `skills/code-standardization/references/tooling.md` (memory of what Python usually does), plus `skills/rubens-project-standardization/references/restructure-flow.md:7` (prose). Any hit describing a MEMORY.md / cross-session memory mechanism is a failure: fix it.

Run: `grep -rn --include='*.md' $'\u2014' skills/ commands/ agents/ *.md`
Expected: zero hits (no em-dashes in markdown; matches the pre-commit hook's markdown-only scope; a pre-existing em-dash in `skills/deep-research/scripts/verify-multi-lens.sh` is out of scope).

- [ ] **Step 2: Frontmatter sanity**

Run: `head -5 skills/rubens-project-standardization/SKILL.md`
Expected: `name: project-standardization`, `description:` starts with "Use when", no memory phrase, frontmatter under 1024 chars.

- [ ] **Step 3: Stage and commit (hooks must run)**

Run: `git add -A && git commit -m "feat(standardization): remove unused cross-session memory bootstrap"`
Expected: commit succeeds; `pre-commit` hook passes (em-dash check, frontmatter check, catalog check). If the hook rejects, fix the flagged issue and commit again; do not use `--no-verify`.

- [ ] **Step 4: Confirm end state**

Run: `git show --stat HEAD`
Expected: one commit, files exactly: deleted `references/memory.md`, modified `bootstrap.md`, `SKILL.md`, `small.md`, `medium.md`, `large.md`, `todolist.md`, `artifacts.md`, `templates/STANDARDS.md`, `commands/standardize.md`, `skills/skill-harvest/SKILL.md`. Nothing under `docs/artifacts/`.

- [ ] **Step 5: Report notes for the user**

Include in the final report: (a) installed copies at `~/.config/opencode/skills/` need a manual re-copy to pick this up, (b) `klad/MEMORY.md` now links to a deleted format-reference URL and is never loaded; delete it manually whenever convenient (explicitly out of scope here).

## Self-Review

- Spec coverage: spec items 1-8a map to Tasks 1-2 (including the STANDARDS.md step renumber); spec end-state greps map to Tasks 1-3 verification steps; spec commit rule maps to Task 3. Covered.
- Placeholder scan: every edit quotes verbatim before/after text or exact line anchors. No TBDs.
- Consistency: step renumbering (12 → 11, hooks 10 → 9, STANDARDS 9 → 8) applied consistently across bootstrap.md (incl. line 19), SKILL.md, templates/STANDARDS.md, commands/standardize.md. Task boundaries have disjoint file sets. Verification greps list expected noise hits explicitly, no false failures.
