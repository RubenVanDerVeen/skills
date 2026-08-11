# Versioning standard implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a SemVer 2.0.0 versioning policy to the `project-standardization` skill, with bump-trigger rule, multi-source sync convention, release-cut recipe, standardizer audit checks, orchestrator release-cut step, and SemVer mentions in CHANGELOG/STANDARDS templates.

**Architecture:** Pure docs change. One new reference file (`references/versioning.md`) is the source of truth. Nine existing files in `skills/rubens-project-standardization/` and `agents/` get small surgical edits that point at it. No code, no scripts, no new skill, no new command.

**Tech Stack:** Markdown only.

**Spec:** `docs/artifacts/features/versioning-standard/2026-08-11-versioning-standard-design.md`. Every task implicitly references the spec's components A-H.

## Global constraints

- **No em-dashes (U+2014)** in any file this plan touches. Verify with `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty for the touched paths. Note: pre-existing repo files may have em-dashes elsewhere; only the lines touched by this plan must be clean.
- **No new skill, no new command.** Therefore no `README.md`, no repo-root `AGENTS.md`, no `opencode-install.md` catalog row changes. The internal References table of `skills/rubens-project-standardization/SKILL.md` does get a new row (component B).
- **Cross-references use the exact path** `references/versioning.md` (not "the versioning reference" or "versioning.md"). When the reference is reached via the skill, the path is `references/versioning.md` inside `skills/rubens-project-standardization/`.
- **CHANGELOG heading format** is Keep a Changelog canonical: `## [X.Y.Z] - YYYY-MM-DD` (square brackets, space-dash-space, ISO date). Not `vX.Y.Z`, not `0.X.Y: date`.
- **Conventional Commits 1.0.0** for every commit subject. The commit-msg hook is active in this repo.
- **Token budget**: the small AGENTS template's commented-out Versioning block adds zero tokens when inactive (it is inside an HTML comment). Uncommented at bootstrap only if the project ships versions.
- **TDD does not apply** to markdown. Each task's verification is: read the edited file back, grep for the structural marker, run the em-dash check.

## File structure

| File | Action | Spec component |
|---|---|---|
| `skills/rubens-project-standardization/references/versioning.md` | NEW | A |
| `skills/rubens-project-standardization/SKILL.md` | modify | B |
| `skills/rubens-project-standardization/templates/AGENTS-small.md` | modify | C |
| `skills/rubens-project-standardization/templates/AGENTS-medium.md` | modify | C |
| `skills/rubens-project-standardization/templates/AGENTS-large.md` | modify | C |
| `skills/rubens-project-standardization/templates/CHANGELOG.md` | modify | D |
| `skills/rubens-project-standardization/templates/STANDARDS.md` | modify | E |
| `skills/rubens-project-standardization/references/bootstrap.md` | modify | F |
| `agents/standardizer.md` | modify | G |
| `agents/orchestrator.md` | modify | H |

**Task ordering rationale**: Task 1 writes the foundation reference. Tasks 2-5 edit files that point at it. Each task is a coherent unit that gets its own reviewer gate and its own commit. The standardizer agent (dispatched by the orchestrator after the task loop) catches any cross-task inconsistency.

---

## Task 1: Write `references/versioning.md` (foundation)

**Files:**
- Create: `skills/rubens-project-standardization/references/versioning.md`

**Interfaces:**
- Produces: the file that components B, C, F, G, H all reference. Later tasks cite it as `references/versioning.md`.

**Content**: the spec's component A is the full source. The executor writes the file with these sections in this order, in their own words but covering exactly what the spec lists:

1. Header + purpose: SemVer 2.0.0 policy for shipped-software projects. Link to <https://semver.org/spec/v2.0.0.html>. Note that this reference is part of the `project-standardization` skill and applies to projects that ship versioned releases (Tauri apps, CLIs, libraries, installers); skip for sub-projects versioned through a parent.
2. **Policy: SemVer 2.0.0**: the bump table from spec A.1 (4 rows: breaking / feature / fix / no-bump; columns for 0.x and ≥1.0). Brief rationale paragraph.
3. **Bump-type decision rule**: the Conventional Commit → bump table from spec A.2.
4. **Trigger rule**: the two-phase description from spec A.3 (plan execution updates `[Unreleased]`; release-cut is deliberate).
5. **Source-of-truth declaration**: the AGENTS.md `### Versioning` subsection shape from spec A.4, plus the canonical-source selection guidance for Tauri 2 / Cargo workspace / Node / Python / Go.
6. **Release-cut recipe**: the 5-step procedure from spec A.5, scoped to semver projects (sprint-based and CD projects skip this).
7. **The 3 standardizer checks**: from spec A.6 (sync / alignment / presence), each described in 1-2 sentences.
8. **Anti-patterns**: the 6 bullets from spec A.6 anti-patterns.

- [ ] **Step 1: Write the file**

Write `skills/rubens-project-standardization/references/versioning.md` with the 8 sections above. Use markdown tables for the two bump tables. No em-dashes. Cross-link to `SKILL.md` for the bootstrap checklist.

- [ ] **Step 2: Verify structure**

Run: `Get-Content skills/rubens-project-standardization/references/versioning.md | Select-String -Pattern '^## '`
Expected: 8 top-level section headings corresponding to the 8 sections above.

- [ ] **Step 3: Verify both bump tables render**

Run: `Get-Content skills/rubens-project-standardization/references/versioning.md | Select-String -Pattern '^\| Bump|^\| Breaking|^\| New feature|^\| Bug fix|^\| Docs'`
Expected: at least 6 matching lines (the table rows from both tables combined).

- [ ] **Step 4: Verify no em-dashes**

Run: `Select-String -Path skills/rubens-project-standardization/references/versioning.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 5: Verify the SemVer link is present**

Run: `Select-String -Path skills/rubens-project-standardization/references/versioning.md -Pattern 'semver.org/spec/v2.0.0'`
Expected: at least one match.

- [ ] **Step 6: Commit**

```bash
git add skills/rubens-project-standardization/references/versioning.md
git commit -m "feat(skills): add versioning reference to project-standardization"
```

---

## Task 2: Update `SKILL.md` and `bootstrap.md`

**Files:**
- Modify: `skills/rubens-project-standardization/SKILL.md`
- Modify: `skills/rubens-project-standardization/references/bootstrap.md`

**Interfaces:**
- Consumes: Task 1's `references/versioning.md`.
- Produces: SKILL.md's References table now lists the new reference; bootstrap.md has a sub-step pointing at the Versioning subsection.

- [ ] **Step 1: SKILL.md floor bullet**

In `skills/rubens-project-standardization/SKILL.md`, find the line that currently reads:

```
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0**: `<type>(<scope>): <description>`; `CHANGELOG.md` grouped by version or sprint. Commits are enforced by the `commit-msg` hook installed in bootstrap step 10.
```

Replace with:

```
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0 + SemVer 2.0.0** (shipped-software projects): commits, changelog, and version numbers form one coherent floor. `<type>(<scope>): <description>`; `CHANGELOG.md` grouped by version or sprint; versions follow SemVer 2.0.0 strict (during 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only). Commits are enforced by the `commit-msg` hook installed in bootstrap step 10. Version policy, bump triggers, and multi-source sync: `references/versioning.md`.
```

- [ ] **Step 2: SKILL.md References table row**

Find the References table (lines ~56-67). Add this row immediately after the `references/artifacts.md` row:

```
| `references/versioning.md` | When the project ships versions (Tauri apps, CLIs, libraries, installers): SemVer 2.0.0 policy, bump triggers, multi-source sync, release-cut recipe |
```

- [ ] **Step 3: SKILL.md anti-pattern**

Find the Anti-patterns section at the bottom. Add these two bullets (placed before the "Older `rubens-project-standardization` / `project-standardization.md` projects" closing line):

```
- Do not bump a version source without also bumping every declared sync target in the same commit, and do not bump at all without a corresponding CHANGELOG entry.
- Do not adopt a release-automation tool that redefines the SemVer policy. The policy lives in `references/versioning.md`; the tool only applies it.
```

- [ ] **Step 4: bootstrap.md sub-step**

In `skills/rubens-project-standardization/references/bootstrap.md`, find step 8 (the "Add `CHANGELOG.md`" step). After the existing step 8 text and before step 9, insert:

```
    8.1. **If the project ships versions** (Tauri apps, CLIs, libraries, installers): fill in the `### Versioning` subsection of `AGENTS.md`. Declare the canonical source, the sync targets, and the policy pointer. Verify the CHANGELOG header line names SemVer 2.0.0 alongside Keep a Changelog and Conventional Commits. Verify `STANDARDS.md` has the SemVer row in its stack table. Skip 8.1 entirely for sub-projects versioned through a parent.
```

- [ ] **Step 5: Verify both files**

Run: `Select-String -Path skills/rubens-project-standardization/SKILL.md,skills/rubens-project-standardization/references/bootstrap.md -Pattern 'versioning.md'`
Expected: at least 2 matches in SKILL.md (floor bullet + References row) and 1 in bootstrap.md.

Run: `Select-String -Path skills/rubens-project-standardization/SKILL.md -Pattern 'SemVer 2.0.0'`
Expected: at least 2 matches.

Run: `Select-String -Path skills/rubens-project-standardization/SKILL.md,skills/rubens-project-standardization/references/bootstrap.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add skills/rubens-project-standardization/SKILL.md skills/rubens-project-standardization/references/bootstrap.md
git commit -m "docs(skills): wire versioning reference into project-standardization SKILL and bootstrap"
```

---

## Task 3: Update the three AGENTS.md templates

**Files:**
- Modify: `skills/rubens-project-standardization/templates/AGENTS-small.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-medium.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-large.md`

**Interfaces:**
- Consumes: Task 1's reference.
- Produces: all three templates have a `### Versioning` subsection under `## Git & workflow`.

The Versioning block content (used in all three templates, with the comment wrapper differing per tier):

```markdown
### Versioning

<!--
For shipped-software projects (Tauri apps, CLIs, libraries, installers): uncomment the block below and fill it in. Skip for sub-projects versioned through a parent. During 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only.
-->

<!--
- **Canonical source:** <one file + field, e.g. `src-tauri/tauri.conf.json` -> `version`>
- **Sync targets** (must mirror canonical source in every release commit): <e.g. `src-tauri/Cargo.toml`, `package.json`>
- **Policy:** SemVer 2.0.0. Decision table + release-cut recipe: `references/versioning.md` in the `project-standardization` skill.
- **Trigger:** plan execution appends to `[Unreleased]` in `CHANGELOG.md`. Cutting a version is deliberate, user-invoked.
- **Last release:** <tag + date, e.g. `v0.3.0` - `2026-08-02`>
-->
```

The whole block sits inside HTML comments so the small template ships it inactive (zero tokens at load). At bootstrap, when the project ships versions, the agent uncomments just the inner list (keeping the explanatory comment).

- [ ] **Step 1: AGENTS-small.md**

In `skills/rubens-project-standardization/templates/AGENTS-small.md`, find the `## Git & workflow` section. It currently ends with a `<Any other project-specific rules: branch model, hooks, signing.>` bullet, followed by `## Artifacts`. Insert the Versioning block above between the last Git bullet and the `## Artifacts` heading.

- [ ] **Step 2: AGENTS-medium.md**

In `skills/rubens-project-standardization/templates/AGENTS-medium.md`, find the `## Git & Workflow` section. It ends with `<Any project-specific git rules.>`, followed by `## Artifacts`. Insert the same Versioning block between them.

- [ ] **Step 3: AGENTS-large.md**

Read the file first to confirm the Git section heading and what immediately follows it. Insert the same Versioning block at the equivalent position (after the last Git bullet, before the next `##` heading).

- [ ] **Step 4: Verify all three**

Run: `Select-String -Path skills/rubens-project-standardization/templates/AGENTS-small.md,skills/rubens-project-standardization/templates/AGENTS-medium.md,skills/rubens-project-standardization/templates/AGENTS-large.md -Pattern '### Versioning'`
Expected: 3 matches (one per file).

Run: `Select-String -Path skills/rubens-project-standardization/templates/AGENTS-small.md -Pattern 'Canonical source'`
Expected: 1 match (inside the comment).

Run: `Select-String -Path skills/rubens-project-standardization/templates/AGENTS-small.md,skills/rubens-project-standardization/templates/AGENTS-medium.md,skills/rubens-project-standardization/templates/AGENTS-large.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md
git commit -m "feat(skills): add Versioning subsection to project-standardization AGENTS templates"
```

---

## Task 4: Update CHANGELOG template

**Files:**
- Modify: `skills/rubens-project-standardization/templates/CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1's reference (path mentioned in the recipe comment).

- [ ] **Step 1: Add SemVer to header**

In `skills/rubens-project-standardization/templates/CHANGELOG.md`, find lines 3-5 which currently read:

```
All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
```

Replace the second paragraph with:

```
The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Versions follow [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
```

Leave the existing 3-mode grouping comment (`<!-- Grouping: ... -->`) verbatim. It is preserved for sprint-based and continuous-delivery projects.

- [ ] **Step 2: Add the release-cut recipe comment**

Immediately after the existing `<!-- Grouping: ... -->` comment block (which closes with `-->` on its own line) and before the `---` separator, insert:

```
<!--
How to cut a release (semver projects only):
  1. Classify commits since the last tag (or since the previous version string): BREAKING / feat / fix / docs / chore.
  2. Pick the highest bump per the SemVer 2.0.0 + 0.x rule in `references/versioning.md`.
  3. Edit the canonical version source AND every sync target declared in AGENTS.md -> Versioning.
  4. Rename the [Unreleased] heading to `## [X.Y.Z] - YYYY-MM-DD` and add its link ref at the bottom.
  5. Single commit `chore(release): vX.Y.Z`; tag `vX.Y.Z` only if CI triggers release builds from tags.
-->
```

- [ ] **Step 3: Verify**

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern 'semver.org/spec/v2.0.0'`
Expected: 1 match (the header line).

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern 'How to cut a release'`
Expected: 1 match.

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern 'Grouping:'`
Expected: 1 match (the preserved 3-mode comment).

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add skills/rubens-project-standardization/templates/CHANGELOG.md
git commit -m "feat(skills): add SemVer header and release-cut recipe to CHANGELOG template"
```

---

## Task 5: Update STANDARDS template

**Files:**
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md`

**Interfaces:**
- Consumes: Task 1's reference (referenced by name in the new section).

- [ ] **Step 1: Add stack table row**

In `skills/rubens-project-standardization/templates/STANDARDS.md`, find the stack table. After the row:

```
| Keep a Changelog 1.1.0  | **yes**       | `CHANGELOG.md` format |
```

Add immediately below it:

```
| SemVer 2.0.0            | **yes** (when shipped) | Version numbers for releases |
```

- [ ] **Step 2: Add the new Versioning section**

Find the section `## Changelog: Keep a Changelog 1.1.0` (around line 89) and its content. Immediately after its closing content (which ends with `See CHANGELOG.md for the current state.`) and before the next `---` separator + `## Repository layout` heading, insert:

```
## Versioning: SemVer 2.0.0

Applies when the project ships versioned releases (Tauri apps, CLIs, libraries, installers). Skip for sub-projects versioned through a parent.

- **Canonical source + sync targets**: declared in `AGENTS.md` -> `### Versioning`. All sync targets are bumped in the same commit as the canonical source.
- **Policy**: SemVer 2.0.0 strict. During 0.x, `0.X+1.0` MAY break; `0.X.Y+1` is backwards-compatible only. After 1.0, standard semver (major / minor / patch = break / feature / fix).
- **Bump trigger**: `[Unreleased]` in `CHANGELOG.md` accumulates changes during development; cutting a version is a deliberate act (rename heading + bump sources + optional tag).

Full bump decision table and release-cut recipe: `references/versioning.md` in the `project-standardization` skill. See `CHANGELOG.md` for the release history.
```

- [ ] **Step 3: Add to the References list**

Find the `## References` section at the bottom. After the line:

```
- Keep a Changelog 1.1.0: <https://keepachangelog.com/en/1.1.0/>
```

Add:

```
- SemVer 2.0.0: <https://semver.org/spec/v2.0.0.html>
```

- [ ] **Step 4: Verify**

Run: `Select-String -Path skills/rubens-project-standardization/templates/STANDARDS.md -Pattern 'SemVer 2.0.0'`
Expected: at least 4 matches (stack table row, new section heading + body, References list link).

Run: `Select-String -Path skills/rubens-project-standardization/templates/STANDARDS.md -Pattern '## Versioning: SemVer'`
Expected: 1 match.

Run: `Select-String -Path skills/rubens-project-standardization/templates/STANDARDS.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add skills/rubens-project-standardization/templates/STANDARDS.md
git commit -m "feat(skills): add SemVer 2.0.0 to STANDARDS template stack, section, and references"
```

---

## Task 6: Update `agents/standardizer.md`

**Files:**
- Modify: `agents/standardizer.md`

**Interfaces:**
- Consumes: Task 1's reference (the 3 checks defined there).
- Produces: the standardizer agent now audits versioning policy on shipped-software projects.

- [ ] **Step 1: Update frontmatter description**

In `agents/standardizer.md`, the YAML frontmatter `description:` field currently ends with:

```
...per-language naming and module-organization rules, architecture boundary adherence.
```

Change that tail to:

```
...per-language naming and module-organization rules, architecture boundary adherence, version-source sync and SemVer 2.0.0 policy presence (shipped-software projects).
```

- [ ] **Step 2: Add the audit sentence**

Find the paragraph that begins "Then load `code-standardization`" (line 43). Insert this new paragraph immediately before it (after the existing project-standardization audit paragraph ends with "...ISO 8601 dates."):

```
Then check versioning policy per `project-standardization`'s `references/versioning.md` when the project ships versions: (a) every sync target declared in `AGENTS.md` -> Versioning matches the canonical source; (b) every `## [X.Y.Z]` heading in CHANGELOG corresponds to a released version string, and the latest heading matches the canonical source's current value (the `[Unreleased]` section may exist between releases); (c) SemVer 2.0.0 is referenced in the AGENTS.md Versioning subsection, the CHANGELOG header, and the STANDARDS.md stack table. Report drift in any of the three as `quick-fix`. Skip entirely for sub-projects versioned through a parent or for projects that do not ship versions.
```

- [ ] **Step 3: Verify**

Run: `Select-String -Path agents/standardizer.md -Pattern 'versioning.md'`
Expected: at least 1 match (the new audit paragraph).

Run: `Select-String -Path agents/standardizer.md -Pattern 'SemVer 2.0.0'`
Expected: at least 2 matches (frontmatter description + audit paragraph).

Run: `Select-String -Path agents/standardizer.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 4: Verify the YAML frontmatter still parses**

Run: `Get-Content agents/standardizer.md | Select-Object -First 40`
Verify the frontmatter block (`---` ... `---`) is intact, the `description:` field is a single line, and no required fields were lost.

- [ ] **Step 5: Commit**

```bash
git add agents/standardizer.md
git commit -m "feat(agents): add versioning-policy audit to standardizer"
```

---

## Task 7: Update `agents/orchestrator.md`

**Files:**
- Modify: `agents/orchestrator.md`

**Interfaces:**
- Consumes: Task 1's decision table + release-cut recipe.
- Produces: the orchestrator now has a release-cut branch (step 7.1) it can fire when the user asks.

- [ ] **Step 1: Add release-cut step 7.1**

In `agents/orchestrator.md`, find step 7 (the "Documentation" paragraph that begins "Documentation: dispatch the `documenter` subagent..."). Insert this new numbered step immediately BEFORE step 7:

```
7. **Release-cut (user-invoked)**: if the user asks to cut a release, or if the plan's final task is a release task, read `git log <last-tag>..HEAD --oneline` (or, with no tags, the commit range since the canonical version source last changed), classify each commit's Conventional Commit type per the decision table in `project-standardization`'s `references/versioning.md`, and recommend the next version to the user with the reasoning in one line (e.g. "3 `feat:` + 1 `fix:` since v0.3.0 -> minor bump -> 0.4.0"). On user confirmation, dispatch an executor with the release task: edit the canonical version source AND every sync target declared in `AGENTS.md` -> Versioning, rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` in CHANGELOG, add the link ref at the bottom of CHANGELOG, single commit `chore(release): vX.Y.Z`, and tag `vX.Y.Z` only if the project's CI triggers release builds from tags. This is a normal executor task that goes through executor + reviewer like any other; it is triggered by a release request rather than a plan task. Renumber the original step 7 (Documentation) to step 8 and the original step 8 (Finish with a report) to step 9 in the same edit.
```

- [ ] **Step 2: Update the frontmatter description**

In `agents/orchestrator.md`, the YAML `description:` field mentions "escalates two-strike failures to the oracle, manages the todo list, and reports." Append before the final period:

```
..., and on user-invoked release-cut classifies commits per the SemVer 2.0.0 decision table and dispatches a release-bump executor task.
```

- [ ] **Step 3: Verify step numbering**

Run: `Get-Content agents/orchestrator.md | Select-String -Pattern '^\d+\.'`
Expected: numbered steps from 1 through 9, with the new "Release-cut" step at position 7, "Documentation" at 8, "Finish with a report" at 9. No duplicate numbers, no gaps.

Run: `Select-String -Path agents/orchestrator.md -Pattern 'versioning.md'`
Expected: at least 1 match.

Run: `Select-String -Path agents/orchestrator.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add agents/orchestrator.md
git commit -m "feat(agents): add release-cut branch to orchestrator"
```

---

## Task 8: Whole-plan verification

**Files:** none modified. Read-only sweep.

**Interfaces:** consumes all previous tasks.

- [ ] **Step 1: Em-dash check across every touched file**

Run:
```powershell
$files = @(
  "skills/rubens-project-standardization/references/versioning.md",
  "skills/rubens-project-standardization/SKILL.md",
  "skills/rubens-project-standardization/templates/AGENTS-small.md",
  "skills/rubens-project-standardization/templates/AGENTS-medium.md",
  "skills/rubens-project-standardization/templates/AGENTS-large.md",
  "skills/rubens-project-standardization/templates/CHANGELOG.md",
  "skills/rubens-project-standardization/templates/STANDARDS.md",
  "skills/rubens-project-standardization/references/bootstrap.md",
  "agents/standardizer.md",
  "agents/orchestrator.md"
)
Select-String -Path $files -Pattern ([char]0x2014)
```
Expected: no output. If any line matches, fix it inline (replace with `:`, `,`, `-`, or `;` per context).

- [ ] **Step 2: Cross-reference consistency**

Run: `Select-String -Path $files -Pattern 'versioning\.md'`
Expected: matches in SKILL.md (2), bootstrap.md (1), AGENTS-small/medium/large (1 each), CHANGELOG.md (1, inside the recipe comment), STANDARDS.md (1), standardizer.md (1), orchestrator.md (1). Versioning.md itself does not match.

- [ ] **Step 3: SemVer 2.0.0 mention sweep**

Run: `Select-String -Path $files -Pattern 'SemVer 2\.0\.0'`
Expected: matches in versioning.md (multiple), SKILL.md (≥2), CHANGELOG.md (1), STANDARDS.md (≥4), standardizer.md (≥2), orchestrator.md (1). AGENTS templates mention "SemVer 2.0.0" inside the commented block (1 each).

- [ ] **Step 4: CHANGELOG heading format check**

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern '## \[X\.Y\.Z\] - YYYY-MM-DD'`
Expected: 1 match in the recipe comment (the canonical format demonstration).

Run: `Select-String -Path skills/rubens-project-standardization/templates/CHANGELOG.md -Pattern '\[<First Version or Sprint>\]'`
Expected: 1 match (the placeholder example block is preserved).

- [ ] **Step 5: No accidental catalog edits**

Run: `git status --porcelain`
Expected: only the 10 files listed in the File structure table above show as modified/added. No changes to `README.md`, repo-root `AGENTS.md`, or `opencode-install.md`. If any of those show up, revert them; this plan does not touch catalogs.

- [ ] **Step 6: Commit nothing**

This task is verification only. No commit. Report results in the execution report.

---

## Out-of-scope (do NOT do in this plan)

- Do not migrate `klad/CHANGELOG.md` or `synctool/CHANGELOG.md` to the canonical heading format. Their existing `v0.X.Y <date>` formats predate this standard; a separate migration handles them if the user asks.
- Do not add a per-project bump script. Manual multi-file edit is the policy; a script can come later if release frequency grows.
- Do not install `release-please`, `semantic-release`, `git-cliff`, or any other automation tool.
- Do not extend the policy to library sub-projects versioned through a parent.
- Do not edit `README.md` or repo-root `AGENTS.md` "Current skills" tables: no new skill is being added.

## Self-review notes

- **Spec coverage**: every component A-H from the spec maps to exactly one task. Component A -> Task 1. Components B + F -> Task 2. Component C -> Task 3. Components D + E -> Tasks 4 + 5 (split for reviewability). Components G + H -> Tasks 6 + 7. Task 8 is the verification sweep.
- **Type consistency**: the path string `references/versioning.md` is used verbatim everywhere. The CHANGELOG heading format `## [X.Y.Z] - YYYY-MM-DD` is used identically in versioning.md, CHANGELOG template, STANDARDS template, standardizer audit, and orchestrator step.
- **No placeholders in the plan itself**: every step shows the exact text to add or the exact command to run.
