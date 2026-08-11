# Versioning standard for `project-standardization`

**Status:** design
**Date:** 2026-08-11
**Author:** planner session, brainstormed with user
**Skill touched:** `skills/rubens-project-standardization/` (existing) + `agents/standardizer.md` + `agents/orchestrator.md`

## Problem

`project-standardization` covers Conventional Commits 1.0.0 and Keep a Changelog 1.1.0 as part of its floor, but it has no policy for **when** to bump a version, **which** semver flavour applies, or how to keep version strings in sync across multiple source files. Drift is already visible in the user's projects:

- `klad` (Tauri app) jumped `0.1.0 → 0.3.0`. The 0.2.0 string was bumped in source files but never released, never changelogged. The 0.3.0 CHANGELOG entry explicitly notes "Supersedes the untagged 0.2.0 version-string bump."
- `synctool` (Tauri app) skipped `0.4.0`. The 0.5.0 CHANGELOG entry notes "v0.4 work, never released as installer."
- Both apps maintain the version in three files (`src-tauri/tauri.conf.json`, `src-tauri/Cargo.toml`, `package.json`) with no documented canonical source or sync procedure.
- Neither project's CHANGELOG references SemVer 2.0.0; `STANDARDS.md` does not list it in the stack.

The result: agents working in these projects have no basis for deciding whether a change is patch, minor, or major. They either skip the bump (the default, causing drift) or guess.

## Goals

1. **One documented semver policy** that applies to every shipped-software project the skill bootstraps.
2. **A bump-type decision rule** an agent can apply from Conventional Commit history alone (no tooling required).
3. **A declared canonical version source + sync-target list** so multi-file projects (Tauri, monorepos) bump in lockstep.
4. **A release-cut recipe** that ties commits → CHANGELOG heading → version sources → optional tag.
5. **Standardizer audit coverage** so drift gets caught at review time.
6. **SemVer 2.0.0 mentioned alongside Keep a Changelog and Conventional Commits** in CHANGELOG, STANDARDS, and the standards-stack reference: the three conventions form a coherent floor.

## Non-goals (YAGNI)

- No bump scripts. Manual multi-file edit at release-cut. A per-project script can be added later if volume grows.
- No release-automation tooling (`release-please`, `semantic-release`, `git-cliff`). The decision table is tool-agnostic and the orchestrator applies it inline. Projects that later adopt a tool can slot it in without redefining the policy.
- No fixing existing CHANGELOG heading drift in klad/synctool. The standard writes the policy; existing projects migrate separately if and when the user asks.
- No new slash command. `/standardize` already bootstraps; versioning lands as an AGENTS.md subsection, not a separate command.
- No new skill. This is an extension to the existing `project-standardization` skill.

## Locked decisions (from brainstorming)

1. **Scope**: extend `project-standardization`; not a new skill, not Tauri-only.
2. **Policy**: SemVer 2.0.0 strict. During 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only. ≥1.0 follows standard semver (major = break, minor = feature, patch = fix).
3. **Trigger**: plan execution appends to `[Unreleased]` in CHANGELOG as features land; cutting a version heading + bumping source files + optional tag is a deliberate, user-invoked act. No continuous bumps.
4. **Sync mechanism**: AGENTS.md declares one canonical version source plus a list of sync targets; at release-cut, the executor edits all declared sources in one commit. No mandatory script.

## Design

### A. New reference: `references/versioning.md`

Location: `skills/rubens-project-standardization/references/versioning.md`.

The actual standard. Sections:

1. **Policy: SemVer 2.0.0.** Link to <https://semver.org/spec/v2.0.0.html>. Explicit bump table:

   | Change | Bump in 0.x | Bump in ≥1.0 |
   |---|---|---|
   | Breaking change (any kind) | `0.X+1.0` | `X+1.0.0` |
   | New feature, backwards-compatible | `0.X+1.0` | `0.Y+1.0` |
   | Bug fix, backwards-compatible | `0.X.Y+1` | `0.X.Y+1` |
   | Docs / chore / refactor (no behaviour) | no bump | no bump |

   Note that in 0.x the minor segment acts as the breaking-change slot; the patch segment is for fixes only. Rationale: matches semver.org's strict reading and the cargo ecosystem's behaviour; matches what the user's Tauri apps have been doing in practice.

2. **Bump-type decision rule.** Read commits since the last tag (or since the canonical source's previous version if no tag). Classify each commit's Conventional Commit type. Pick the highest bump that applies:

   | Conventional Commit signal | Bump |
   |---|---|
   | `BREAKING CHANGE:` footer, or `<type>!:` | major-equivalent (per 0.x or ≥1.0 rule above) |
   | `feat:` | minor-equivalent |
   | `fix:`, `perf:` | patch |
   | `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `ci:`, `build:` | no bump |

   Ties break upward. If only no-bump commits accumulated since the last release, no release is cut.

3. **Trigger rule.** Two phases:
   - **During plan execution**: every feature or fix task updates CHANGELOG's `[Unreleased]` section with the user-visible change in Keep a Changelog format. This already happens informally; the skill now makes it explicit.
   - **Release-cut** (deliberate, user-invoked): the orchestrator classifies commits per the decision rule above, recommends the next version to the user, on confirmation dispatches an executor that (a) edits the canonical source, (b) edits every sync target, (c) renames `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, (d) adds the link ref line at the bottom, (e) commits, (f) optionally tags `vX.Y.Z` if the project's CI triggers on tags.

4. **Source-of-truth declaration.** The project's AGENTS.md `### Versioning` subsection declares:
   - One **canonical source** (the file + field that holds the version string).
   - Zero or more **sync targets** (other files that must mirror the canonical source).
   - The **policy pointer** (`SemVer 2.0.0` + the bump table reference).
   - The **last release** (tag + date) for quick orientation.

   Canonical-source selection guidance:
   - **Tauri 2 app** (default): canonical = `src-tauri/tauri.conf.json` → `version`. Sync targets = `src-tauri/Cargo.toml` (and any workspace `Cargo.toml` if `version.workspace = true`), `package.json`.
   - **Cargo workspace**: canonical = root `Cargo.toml` → `[workspace.package].version`. Members inherit via `version.workspace = true`.
   - **Node-only**: canonical = `package.json` → `version`.
   - **Python**: canonical = `pyproject.toml` → `[project].version` (or `__init__.py`'s `__version__` if the project prefers).
   - **Go**: canonical = the git tag. Embed at build time via `-ldflags "-X main.version=<tag>"`. No source file holds a literal version.
   - **Other / uncertain**: pick the file a release tool would touch first.

5. **Release-cut recipe** (5 steps, concrete; semver projects only: sprint-based and CD projects cut headings on their own cadence without bumping a version source):
   1. **Recommend**: orchestrator reads `git log <last-tag>..HEAD --oneline` (or, with no tags, since the version-source's previous commit), classifies per the decision rule, recommends a bump.
   2. **Confirm**: user approves (or picks a different bump).
   3. **Apply**: executor edits canonical source + every sync target + adds `## [X.Y.Z] - YYYY-MM-DD` heading to CHANGELOG + moves `[Unreleased]` items under it + adds the link ref line at the bottom.
   4. **Commit**: single commit, Conventional Commits subject `chore(release): vX.Y.Z` (or `release(<scope>): ...` if scope is meaningful). Bundle the version-source edits and the CHANGELOG edit; never split them.
   5. **Tag (optional)**: `git tag -a vX.Y.Z -m "..."`. Only when the project's CI triggers release builds from tags (Tauri release workflow: yes; library without a release pipeline: no).

6. **The 3 standardizer checks.**
   - **Version sources in sync**: every sync target matches the canonical source. If any drifts, quick-fix finding naming both files.
   - **CHANGELOG alignment**: every `## [X.Y.Z]` heading in CHANGELOG corresponds to a version string that appeared in the canonical source's history; the latest heading matches the canonical source's current value. The `[Unreleased]` section may exist between releases. Out-of-order or missing headings = quick-fix.
   - **Policy presence** (shipped-software projects only): SemVer 2.0.0 is referenced in (a) the AGENTS.md `### Versioning` subsection, (b) the CHANGELOG header line, (c) the STANDARDS.md stack table. Missing any one = quick-fix.

7. **Anti-patterns.**
   - Bumping one source without bumping every declared sync target.
   - Skipping a version in CHANGELOG that exists in the source files (the klad 0.2.0 ghost).
   - Cutting a version with no `[Unreleased]` entries (nothing to release).
   - Mixed heading formats in one CHANGELOG (mixing `## [X.Y.Z] - YYYY-MM-DD` semver headings with `## [Sprint N]: ...` sprint headings). Pick one mode at bootstrap.
   - Using patch in 0.x for a feature (`0.X.Y+1` should be backwards-compatible fixes only).
   - Major bump in 0.x (no such thing; 0 → 1.0.0 is the major).

### B. `SKILL.md` updates (`skills/rubens-project-standardization/SKILL.md`)

Three edits:

1. **Standards-stack bullet** (around line 31): change the existing "Conventional Commits 1.0.0 + Keep a Changelog 1.1.0" bullet to read:
   > **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0 + SemVer 2.0.0** (shipped-software projects): commits, changelog, and version numbers form one coherent floor. Version policy, bump triggers, and multi-source sync: `references/versioning.md`.

2. **References table**: add a row:
   > `references/versioning.md` | When the project ships versions (Tauri apps, CLIs, libraries, installers): semver policy, bump triggers, multi-source sync, release-cut recipe.

3. **Anti-patterns** list: add:
   > Do not bump a version source without also bumping every declared sync target in the same commit. Do not bump at all without a corresponding CHANGELOG entry.

### C. AGENTS.md templates (`templates/AGENTS-small.md`, `AGENTS-medium.md`, `AGENTS-large.md`)

A new `### Versioning` subsection under `## Git & workflow`. In the small template, ship it commented out (so it is invisible unless the project ships versions). In medium and large, ship it uncommented but with placeholders.

Common block:

```markdown
### Versioning (uncomment when this project ships versions: Tauri apps, CLIs, libraries, installers)

- **Canonical source:** <one file + field, e.g. `src-tauri/tauri.conf.json` -> `version`>
- **Sync targets** (must mirror canonical source in every release commit): <e.g. `src-tauri/Cargo.toml`, `package.json`>
- **Policy:** SemVer 2.0.0. During 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only. Decision table + release-cut recipe: `references/versioning.md` in the `project-standardization` skill.
- **Trigger:** plan execution appends to `[Unreleased]` in `CHANGELOG.md`. Cutting a version is deliberate, user-invoked.
- **Last release:** <tag + date, e.g. `v0.3.0` - `2026-08-02`>
```

### D. CHANGELOG template (`templates/CHANGELOG.md`)

Two edits:

1. **Header line** (currently lines 3-5). Add the SemVer reference so all three conventions are named together:

   ```markdown
   The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
   Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
   Versions follow [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
   ```

2. **Release-cut recipe comment.** Keep the existing 3-mode grouping comment (semver / sprint / continuous-delivery) unchanged; it correctly supports sprint-based school projects. Add a second comment block immediately after it, scoped to the semver case, carrying the 5-step recipe:

   ```markdown
   <!--
   How to cut a release (semver projects only):
     1. Classify commits since the last tag (or since the previous version string): BREAKING/feat/fix/etc.
     2. Pick the highest bump per the SemVer 2.0.0 + 0.x rule in references/versioning.md.
     3. Edit the canonical version source AND every sync target declared in AGENTS.md -> Versioning.
     4. Rename the [Unreleased] heading to ## [X.Y.Z] - YYYY-MM-DD and add its link ref at the bottom.
     5. Single commit `chore(release): vX.Y.Z`; tag vX.Y.Z only if CI triggers release builds from tags.
   -->
   ```

   The existing grouping comment is preserved verbatim; this plan does not regress sprint-based or continuous-delivery support. The versioning reference (component A) scopes itself to semver projects; sprint-based and CD projects do not use the canonical-source + sync-target mechanism.

### E. STANDARDS template (`templates/STANDARDS.md`)

Three edits:

1. **Stack table** (line 25, just below the Keep a Changelog row): add:
   ```
   | SemVer 2.0.0            | **yes** (when shipped) | Version numbers for releases |
   ```

2. **New section** between the existing `## Changelog: Keep a Changelog 1.1.0` section and `## Repository layout`:

   ```markdown
   ## Versioning: SemVer 2.0.0

   Applies when the project ships versioned releases (Tauri apps, CLIs, libraries, installers). Skip for sub-projects versioned through a parent.

   - **Canonical source + sync targets**: declared in `AGENTS.md` -> `### Versioning`. All sync targets are bumped in the same commit as the canonical source.
   - **Policy**: SemVer 2.0.0 strict. During 0.x, `0.X+1.0` MAY break; `0.X.Y+1` is backwards-compatible only. After 1.0, standard semver (major/minor/patch = break/feature/fix).
   - **Bump trigger**: `[Unreleased]` in `CHANGELOG.md` accumulates changes during development; cutting a version is a deliberate act (rename heading + bump sources + optional tag).

   See `CHANGELOG.md` for the release history.
   ```

3. **References list** at the bottom: add:
   ```
   - SemVer 2.0.0: https://semver.org/spec/v2.0.0.html
   ```

### F. Bootstrap checklist (`references/bootstrap.md`)

Extend step 8 ("Add CHANGELOG.md") with a sub-step:

> 8.1. **If the project ships versions** (Tauri apps, CLIs, libraries, installers): fill in the `### Versioning` subsection of `AGENTS.md`. Declare the canonical source, the sync targets, and the policy pointer. Verify the CHANGELOG header line names SemVer 2.0.0 alongside Keep a Changelog and Conventional Commits. Verify `STANDARDS.md` has the SemVer row in its stack table. Skip 8.1 entirely for sub-projects versioned through a parent.

### G. `agents/standardizer.md`

Add one sentence to the audit line (currently line 41):

> Then check versioning policy per `references/versioning.md` when the project ships versions: (a) every sync target matches the canonical source; (b) every `## [X.Y.Z]` heading in CHANGELOG corresponds to a released version string, and the latest heading matches the canonical source's current value; (c) SemVer 2.0.0 is referenced in the AGENTS.md Versioning subsection, the CHANGELOG header, and the STANDARDS.md stack table.

Update the frontmatter `description` to add "version-source sync, SemVer policy presence" to the list of things it audits.

### H. `agents/orchestrator.md`

Extend step 7 (post-task-loop, before documentation) with a release-cut branch:

> 7.1. **Release-cut (user-invoked)**: if the user asks to cut a release, or if the plan's final task is a release task, read `git log <last-tag>..HEAD --oneline` (or since the previous version string), classify each commit per the versioning reference's decision table, recommend the next version to the user with the reasoning ("3 feat commits, 1 fix → minor bump → 0.3.0 → 0.4.0"). On confirmation, dispatch an executor to apply the bump: edit canonical source + every sync target, rename `[Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` in CHANGELOG, add the link ref, single commit `chore(release): vX.Y.Z`, optionally tag. This is a normal task that goes through executor + reviewer like any other; it just happens to be triggered by a release request rather than a plan task.

## Files touched

| File | Change |
|---|---|
| `skills/rubens-project-standardization/references/versioning.md` | NEW |
| `skills/rubens-project-standardization/SKILL.md` | Floor bullet; References row; anti-pattern |
| `skills/rubens-project-standardization/templates/AGENTS-small.md` | New `### Versioning` subsection (commented out) |
| `skills/rubens-project-standardization/templates/AGENTS-medium.md` | New `### Versioning` subsection (placeholders) |
| `skills/rubens-project-standardization/templates/AGENTS-large.md` | New `### Versioning` subsection (placeholders) |
| `skills/rubens-project-standardization/templates/CHANGELOG.md` | SemVer header line; release-cut recipe comment; lock heading format |
| `skills/rubens-project-standardization/templates/STANDARDS.md` | SemVer stack row; new Versioning section; References link |
| `skills/rubens-project-standardization/references/bootstrap.md` | Sub-step 8.1 for versioning setup |
| `agents/standardizer.md` | Audit sentence + frontmatter description |
| `agents/orchestrator.md` | Release-cut branch (step 7.1) |

**No new skill, no new command** → no `README.md`, no `AGENTS.md` (this repo's), no `opencode-install.md` catalog row changes needed. The internal References table of the `project-standardization` SKILL.md does get a new row.

## Verification

- All new and edited files use no em-dash (U+2014). Verify with `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returning empty for the touched files. Note: this repo's existing files have em-dashes in places; this verification scopes to files this plan touches.
- The CHANGELOG template's heading format matches Keep a Changelog canonical exactly: `## [X.Y.Z] - YYYY-MM-DD` with the link ref line at the bottom.
- The versioning reference's bump table is internally consistent (the 0.x column matches the ≥1.0 column when scaled).
- The standardizer's three versioning checks map 1:1 to the policy sections in the reference.
- The orchestrator's release-cut step references the same decision table; no second source of truth.
- Templates stay under their tier's token budget. The small AGENTS template's commented-out versioning block adds zero tokens when inactive.

## Out-of-scope follow-ups (not in this plan)

- Migrating `klad` and `synctool` CHANGELOGs to the canonical heading format (current em-dash and `vX.Y.Z` formats predate this standard).
- Adding a per-project bump script if release-cut frequency grows.
- Wiring `git-cliff` or `release-please` for projects that want automated changelog generation.
- Extending the same policy to library sub-projects versioned through a parent (currently explicitly out of scope).
