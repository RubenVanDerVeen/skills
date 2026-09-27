# Release Description Standard Implementation Plan

> **For agentic workers:** Execute via the `/execute-plan` conventions: orchestrator dispatches one `executor` + `reviewer` pair per task, `lazy-dev` gate has already passed, documenter closes out. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `release-description` skill (one body template, three copy sites: `chore(release)` commit body, `git tag -a` annotation, GitHub/GitLab Release notes) and wire it into `versioning.md`, `agents/documenter.md`, and `agents/orchestrator.md`.

**Architecture:** Mirrors the `pr-description` precedent: skill file is the single source of truth, the documenter emits the body at close-out from the execution report. Lean skill: one `SKILL.md`, no `references/`, no command. Catalogs and CHANGELOG ship in the same commit as the skill.

**Tech Stack:** Markdown only. Git hooks (`.githooks/`) verify. `opencode agent list` verifies agent files parse.

**Spec:** `docs/artifacts/features/release-description/2026-09-27-release-description-design.md`

## Global Constraints

- Branch: `feat/release-description` off `main` (Conventional Branch 1.1.0). Create before Task 1.
- No em-dashes (U+2014) in any file touched. Hyphens only.
- **Single commit boundary:** Tasks 1 and 2 make edits but DO NOT commit. Task 3 commits everything as one commit, message verbatim: `feat(skills): add release-description standard for releases, tags, and changelog headings`. The pre-commit hook rejects a new skill missing from catalogs, so the single commit must include the catalog rows (it does, by design).
- Versioning: repo `AGENTS.md` declares no `### Versioning` subsection: **unversioned, no bump**. Documenter notes "unversioned/no bump" in one report line at close-out.
- Tasks 1-2 produce no commit, so the orchestrator's commit-hash-centric review does not apply to them: Tasks 1-2 are reviewed from the working-tree diff (`git diff -- <the task's Files>`). The commit-integrity check runs once, on Task 3's single commit (Task 3 Step 7 verifies the seven-file shape).
- Skill body under 400 words; frontmatter total under 1024 characters; `description` starts with `Use when...`; `name` kebab-case matching folder name.
- Template block inside `SKILL.md` uses a 4-space indented block (matches the `pr-description` sibling skill, lines 20-33, and avoids heading-scanner ambiguity in the pre-commit hook). The design doc sketches it fenced; indentation is the deliberate deviation, reason: sibling consistency + hook safety.
- Requires `git config core.hooksPath .githooks` active in the clone (verify once in Task 3 before committing).
- No new command file, no `references/` folder, no backfill of past releases (spec non-goals).

---

### Task 1: Create `skills/release-description/SKILL.md`

**Files:**
- Create: `skills/release-description/SKILL.md`

**Depends:** none

**Interfaces:**
- Consumes: nothing.
- Produces: `skills/release-description/SKILL.md`, the file the pre-commit catalog hook checks for and that Tasks 2 and 3 reference by skill name `release-description`.

- [ ] **Step 1: Write the file**

Create `skills/release-description/SKILL.md` with exactly this content:

```
---
name: release-description
description: Use when writing the body of a `chore(release): vX.Y.Z` commit, annotating a git tag with `git tag -a`, or filling in a GitHub or GitLab Release description (`gh release create --notes-file`, the platform Release UI). Triggers on release notes, release description, tag annotation, changelog release, cut a release, ship vX.Y.Z.
---

## Overview

One body shape, three copy sites: the `chore(release): vX.Y.Z` commit body, the tag annotation, and the GitHub or GitLab Release description. Same text everywhere, character-for-character; two sources drift.

## When to use

- Writing the body of a `chore(release): vX.Y.Z` commit.
- Running `git tag -a vX.Y.Z -m "<message>"`.
- Publishing a Release page (`gh release create --notes-file`, `glab`, or the UI).

## Template

Five sections, in order. Write to `.release-notes.md` at the repo root, copy verbatim to each surface.

    ## Summary
    One paragraph, plain language. What is in this release and why a user
    cares. Mention the version and cadence ("weekly", "monthly") when
    stable, the audience when known. Two to four sentences. No commit
    hashes.

    ## Highlights
    Three to five bullets, user-visible changes only. Pull from the
    [Unreleased] Added and Changed sections of CHANGELOG.md and rephrase
    for users ("Added dark mode", not "feat(ui): add dark mode toggle").
    Past-tense verbs. Internal-only work goes in Internal, not here.

    ## Breaking changes
    One bullet per BREAKING CHANGE footer since the last tag:
      - **<one-line name>** - <what changed>. Migration: <link or one-line>.
    Write "None" when there are none; empty is information.

    ## Internal
    Refactors, chores, dependency bumps, test changes that are not
    user-visible. Write "None" when none. Skip only for trivial patch
    releases with zero user signal.

    ## Full changelog
    Link to the diff range or the CHANGELOG section:
    - GitHub: [vX.Y.Z...vX.Y+1.Z](https://github.com/<owner>/<repo>/compare/vX.Y.Z...vX.Y+1.Z)
    - GitLab: the equivalent compare URL.
    - Tag-only: a relative link to the ## [X.Y.Z] - YYYY-MM-DD heading.
    Commit hashes appear only here.

## Rules

- Every section present; write `None` when empty. Never drop one, including Breaking changes.
- Derive from the execution report and `[Unreleased]` entries; never invent.
- Three copy sites, same text character-for-character; no platform-specific rewording.
- Skip the Release page copy when the project publishes none; commit body and tag annotation are always written.
- The `[Unreleased]` rename to `## [X.Y.Z] - YYYY-MM-DD` stays per `references/versioning.md` step 3.
- No em-dashes.

## Audience and tone

Users and downstream maintainers. Plain language, no internal jargon, no commit hashes (the Full changelog link is one click away). Internal-only changes go in `## Internal`, not `## Highlights`.

## Related

- `skills/pr-description/`: sibling skill, same shape for PR bodies.
- `skills/rubens-project-standardization/references/versioning.md`: release-cut recipe and ship-bump policy.
- `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-design.md`: the ship-bump default behind every versioned ship.
```

- [ ] **Step 2: Verify frontmatter rules**

Run: `awk '/^---$/{c++;next} c==1' skills/release-description/SKILL.md | wc -c`
Expected: under 1024 (actual is ~350).

Run: `head -3 skills/release-description/SKILL.md | grep -c '^description: Use when'`
Expected: `1`.

- [ ] **Step 3: Verify body budget and em-dash rule**

Run: `awk '/^---$/{c++;next} c>=2' skills/release-description/SKILL.md | wc -w`
Expected: under 400 (trimmed draft measures ~390). A count of 400 or more means the file drifted from this plan's verbatim block: re-copy it, do not improvise a trim.

Run: `grep -rPn '\x{2014}' skills/release-description/ || echo CLEAN`
Expected: `CLEAN`.

- [ ] **Step 4: Do not commit**

Leave changes uncommitted. Task 3 makes the single commit.

---

### Task 2: Wire the skill into versioning.md, documenter.md, orchestrator.md

**Files:**
- Modify: `skills/rubens-project-standardization/references/versioning.md` (line 7 policy pointer, line 71 step 5)
- Modify: `agents/documenter.md` (insert step 6.1 between lines 68 and 69)
- Modify: `agents/orchestrator.md` (line 52, step 8)

**Depends:** none

**Interfaces:**
- Consumes: the skill name `release-description` (textual reference only; no file output from Task 1 is read).
- Produces: pipeline wiring later tasks and the documenter rely on: `versioning.md` step 5 names the body file `.release-notes.md`; `documenter.md` step 6.1 defines the scratch-file flow with the exact command `git tag -a vX.Y.Z -m "$(cat .release-notes.md)"`; `orchestrator.md` step 8 tells the documenter to apply the skill on release tasks.

- [ ] **Step 1: versioning.md step 5, replace the tag placeholder**

In `skills/rubens-project-standardization/references/versioning.md`, replace line 71:

```markdown
5. **Tag** (optional): `git tag -a vX.Y.Z -m "..."`. Only when the project's CI triggers release builds from tags (Tauri release workflow: yes; library without a release pipeline: no).
```

with:

```markdown
5. **Tag** (optional): `git tag -a vX.Y.Z -m "$(cat .release-notes.md)"`, using the release-description body written per the `release-description` skill. Only when the project's CI triggers release builds from tags (Tauri release workflow: yes; library without a release pipeline: no).
```

- [ ] **Step 2: versioning.md policy pointer, add one line**

After line 7 (the paragraph ending `see `SKILL.md`.`), add the pointer as its own paragraph with a blank line before and after (the file's existing blank line 8 stays, add one blank after the new line so the next heading keeps its separator):

```markdown
Tag annotation and Release description bodies: see the `release-description` skill.
```

- [ ] **Step 3: documenter.md, insert step 6.1**

In `agents/documenter.md`, between step 6 (line 68, ends `tagging is the user-invoked release cut.`) and step 7 (line 69, `Commit the report and catalog updates...`), insert:

```markdown
6.1. **Release description body** (skipped when the project is unversioned or step 6 concluded "no bump"). Before making the `chore(release): vX.Y.Z` commit named in step 6, write the release-description body per the `release-description` skill to `<repo-root>/.release-notes.md`: five sections (Summary, Highlights, Breaking changes, Internal, Full changelog), `None` where a section is empty, derived from the execution report and the CHANGELOG's renamed `## [X.Y.Z] - YYYY-MM-DD` section. Then use the same text, character-for-character, in every surface the release touches: the commit body (`git commit -m "chore(release): vX.Y.Z" -m "$(cat .release-notes.md)"`), the tag annotation when the user-invoked release cut tags (`git tag -a vX.Y.Z -m "$(cat .release-notes.md)"`), and the Release page when the project publishes one (`gh release create <tag> --title "vX.Y.Z" --notes-file .release-notes.md`, or the `glab`/UI equivalent; detect via `gh release`/`glab release` references in the project's CI or a publishes-releases flag in `AGENTS.md -> Versioning`). Delete the scratch file at the end of the step, or leave it gitignored when the project already ships that convention.
```

Note: the ordering inside 6.1 ("Before making the commit named in step 6") resolves the design's placement of 6.1 after step 6 while keeping the commit body populated. No change to the write-scope paragraph (line 72): `.release-notes.md` is root-level `*.md`, already in scope.

- [ ] **Step 4: orchestrator.md step 8, add the dispatch clause**

In `agents/orchestrator.md` line 52, replace the fragment:

```markdown
plus the PR-description requirement when the task needs a PR).
```

with:

```markdown
plus the PR-description requirement when the task needs a PR, plus the release-description requirement when the task includes a release: the documenter writes the body per the `release-description` skill).
```

- [ ] **Step 5: Verify agents parse**

Run: `opencode agent list`
Expected: lists agents without errors (`documenter`, `orchestrator` present).

- [ ] **Step 6: Verify wiring consistency**

Run: `grep -n 'release-description' agents/documenter.md agents/orchestrator.md skills/rubens-project-standardization/references/versioning.md`
Expected: at least one hit in each of the three files.

Run: `grep -Fc 'git tag -a vX.Y.Z -m "$(cat .release-notes.md)"' agents/documenter.md skills/rubens-project-standardization/references/versioning.md`
Expected: `1` in each file (identical wording, the consistency read the spec requires).

Run: `grep -rPn '\x{2014}' agents/documenter.md agents/orchestrator.md skills/rubens-project-standardization/references/versioning.md || echo CLEAN`
Expected: `CLEAN`.

- [ ] **Step 7: Do not commit**

Leave changes uncommitted. Task 3 makes the single commit.

---

### Task 3: Catalogs, CHANGELOG, single commit

**Files:**
- Modify: `README.md` (Skills table ~line 22, Layout block ~lines 93-94)
- Modify: `AGENTS.md` (Current skills table ~line 145)
- Modify: `CHANGELOG.md` (`[Unreleased] / Added`, after line 43)
- Commit: all files from Tasks 1-3

**Depends:** Task 1, Task 2

**Interfaces:**
- Consumes: `skills/release-description/SKILL.md` from Task 1 (the catalog hook checks it exists and is listed); the edited files from Task 2 (ship in the same commit; consistency wording already verified there).
- Produces: the single commit `feat(skills): add release-description standard for releases, tags, and changelog headings` containing all seven changed files.

- [ ] **Step 1: README.md Skills table row**

Insert a new row directly after the `pr-description` row (line 22) and before the `rubens-project-standardization` row (line 23):

```markdown
| [`release-description`](./skills/release-description/SKILL.md) | Standardized body for release descriptions: the `chore(release): vX.Y.Z` commit body, the `git tag -a` annotation, and GitHub or GitLab Release notes. One template, three copy sites: Summary, Highlights, Breaking changes, Internal, Full changelog. |
```

- [ ] **Step 2: README.md Layout block**

Line 93 currently ends the skills tree with `    └── pr-description/SKILL.md`. Change it to `├──` and append the new skill as the last entry:

```text
    ├── pr-description/SKILL.md
    └── release-description/SKILL.md
```

- [ ] **Step 3: AGENTS.md Current skills table row**

Insert a new row directly after the `pr-description` row (line 145) and before the `rubens-project-standardization` row (line 146):

```markdown
| `skills/release-description/` | `release-description` | Standardized body for release descriptions: the `chore(release): vX.Y.Z` commit body, the `git tag -a` annotation, and GitHub or GitLab Release notes. One template, three copy sites: Summary, Highlights, Breaking changes, Internal, Full changelog. |
```

- [ ] **Step 4: CHANGELOG.md bullet**

At the end of the `[Unreleased]` `### Added` list (after line 43, before the blank line preceding `### Changed`), append:

```markdown
- `skills/release-description/`: one template, three copy sites (`chore(release)` commit body, `git tag -a` annotation, GitHub or GitLab Release notes). Wired into `agents/documenter.md` step 6.1, `agents/orchestrator.md` step 8, and `references/versioning.md` step 5. Spec: `docs/artifacts/features/release-description/2026-09-27-release-description-design.md`.
```

- [ ] **Step 5: Verify catalog agreement before committing**

Run: `grep -c 'release-description' README.md AGENTS.md CHANGELOG.md`
Expected: at least `1` per file.

Run: `ls skills/release-description/SKILL.md`
Expected: the file lists.

Run: `grep -rPn '\x{2014}' README.md AGENTS.md CHANGELOG.md || echo CLEAN`
Expected: `CLEAN`.

- [ ] **Step 6: Hooks active, then the single commit**

Run: `git config core.hooksPath`
Expected: `.githooks`. If empty, run `git config core.hooksPath .githooks` first.

Run: `git add skills/release-description/SKILL.md skills/rubens-project-standardization/references/versioning.md agents/documenter.md agents/orchestrator.md README.md AGENTS.md CHANGELOG.md && git commit -m "feat(skills): add release-description standard for releases, tags, and changelog headings"`
Expected: commit succeeds; pre-commit and commit-msg hooks pass (frontmatter check, catalog-presence check, em-dash scan, Conventional Commits subject). A hook rejection is a fix-and-recommit, never a `--no-verify`.

- [ ] **Step 7: Verify the commit shape**

Run: `git show --stat HEAD`
Expected: exactly one commit touching seven files: `skills/release-description/SKILL.md`, `skills/rubens-project-standardization/references/versioning.md`, `agents/documenter.md`, `agents/orchestrator.md`, `README.md`, `AGENTS.md`, `CHANGELOG.md`.

---

## Self-review (done at plan time)

- Spec coverage: design Changes 1-6 map to Task 1 (change 1), Task 2 (changes 2-4), Task 3 (changes 5-6). Design Verification maps: hooks (Task 3 step 6), `opencode agent list` (Task 2 step 5), catalog agreement (Task 3 step 5), consistency read (Task 2 step 6), acceptance path (documenter behavior, exercised at next real release cut, out of plan scope).
- Placement note: design says step 6.1 sits "after the commit step"; 6.1's own text says "Before making the commit named in step 6", which is what makes the commit body non-empty. Documented in Task 2 step 3.
- No placeholders; every edit has verbatim before/after content.
- Parallelism: Tasks 1 and 2 have disjoint file sets, both `Depends: none`; Task 3 consumes both.
