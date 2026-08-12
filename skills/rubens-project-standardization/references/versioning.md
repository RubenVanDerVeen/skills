# Versioning

## Overview

This reference defines the SemVer 2.0.0 policy for projects that ship versioned releases. It is part of the `project-standardization` skill. Applies when the project ships versioned releases (Tauri apps, CLIs, libraries, installers); skip for sub-projects versioned through a parent.

Policy: [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html). Bump triggers, multi-source sync convention, and the release-cut recipe live here. For the bootstrap checklist that wires this policy into a new project, see `SKILL.md`.

## Policy: SemVer 2.0.0

Versions follow [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html) strict. During `0.x` development, the minor segment acts as the breaking-change slot; the patch segment is for fixes only. Once the project reaches `1.0.0`, standard semver applies: major = breaking change, minor = new feature, patch = bug fix.

| Change | Bump in 0.x | Bump in ≥1.0 |
|---|---|---|
| Breaking change (any kind) | `0.X+1.0` | `X+1.0.0` |
| New feature, backwards-compatible | `0.X+1.0` | `0.Y+1.0` |
| Bug fix, backwards-compatible | `0.X.Y+1` | `0.X.Y+1` |
| Docs / chore / refactor (no behaviour) | no bump | no bump |

Rationale: matches the strict reading of semver.org and the cargo ecosystem's behaviour, and matches what shipped Tauri apps have been doing in practice.

## Bump-type decision rule

Read commits since the last tag (or, with no tags, since the canonical source's previous version string). Classify each commit by its Conventional Commit type. Pick the highest bump that applies. Ties break upward. If only no-bump commits accumulated since the last release, no release is cut.

| Conventional Commit signal | Bump |
|---|---|
| `BREAKING CHANGE:` footer, or `<type>!:` | major-equivalent (per the 0.x or ≥1.0 row above) |
| `feat:` | minor-equivalent |
| `fix:`, `perf:` | patch |
| `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `ci:`, `build:` | no bump |

## Trigger rule

Two phases, by design.

- **During plan execution**: every feature or fix task appends the user-visible change to the `[Unreleased]` section of `CHANGELOG.md` in Keep a Changelog format. This is the only thing plan execution touches in CHANGELOG.
- **Release-cut** (deliberate, user-invoked): the orchestrator classifies commits per the decision rule, recommends the next version to the user, and on confirmation dispatches an executor that (a) edits the canonical source, (b) edits every sync target, (c) renames `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, (d) adds the link ref line at the bottom, (e) commits, (f) optionally tags `vX.Y.Z` when the project's CI triggers release builds from tags.

There is no automatic continuous bumping. Cutting a version is an act, not a side-effect.

## Source-of-truth declaration

The project's `AGENTS.md` carries a `### Versioning` subsection that declares four fields:

- **Canonical source**: one file + field that holds the version string.
- **Sync targets**: zero or more other files that must mirror the canonical source at every release.
- **Policy pointer**: the SemVer 2.0.0 reference and the path to this file.
- **Last release**: tag + date, for quick orientation.

### Canonical-source selection

Pick the single file a release tool would touch first. Common choices:

- **Tauri 2 app** (default): canonical = `src-tauri/tauri.conf.json` -> `version`. Sync targets = `src-tauri/Cargo.toml` (and any workspace `Cargo.toml` that uses `version.workspace = true`), `package.json`.
- **Cargo workspace**: canonical = root `Cargo.toml` -> `[workspace.package].version`. Members inherit via `version.workspace = true`.
- **Node-only**: canonical = `package.json` -> `version`.
- **Python**: canonical = `pyproject.toml` -> `[project].version`, or `__init__.py`'s `__version__` if the project prefers.
- **Go**: canonical = the git tag. Embed at build time via `-ldflags "-X main.version=<tag>"`. No source file holds a literal version.
- **Other / uncertain**: pick the file a release tool would touch first.

## Release-cut recipe

Scoped to semver projects. Sprint-based and continuous-delivery projects cut headings on their own cadence without bumping a version source, and skip this recipe.

1. **Recommend**: read `git log <last-tag>..HEAD --oneline` (or, with no tags, the commit range since the canonical version source last changed). Classify per the bump-type decision rule. Recommend a bump with one line of reasoning.
2. **Confirm**: the user approves, or picks a different bump.
3. **Apply**: edit the canonical source and every sync target. Rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`, move its entries under the new heading, add the link ref line at the bottom.
4. **Commit**: single commit, Conventional Commits subject `chore(release): vX.Y.Z` (or `release(<scope>): ...` when a scope is meaningful). Bundle the version-source edits and the CHANGELOG edit; never split them across commits.
5. **Tag** (optional): `git tag -a vX.Y.Z -m "..."`. Only when the project's CI triggers release builds from tags (Tauri release workflow: yes; library without a release pipeline: no).

## The 3 standardizer checks

For shipped-software projects, the standardizer audits three things.

- **Version sources in sync**: every sync target matches the canonical source. Drift on any one is a `quick-fix` finding naming both files.
- **CHANGELOG alignment**: every `## [X.Y.Z]` heading in `CHANGELOG.md` corresponds to a version string that appeared in the canonical source's history, and the latest heading matches the canonical source's current value. The `[Unreleased]` section may exist between releases. Out-of-order or missing headings = `quick-fix`.
- **Policy presence**: SemVer 2.0.0 is referenced in (a) the `AGENTS.md` `### Versioning` subsection, (b) the `CHANGELOG.md` header line, (c) the `STANDARDS.md` stack table. Missing any one = `quick-fix`.

## Anti-patterns

- Bumping one source without bumping every declared sync target in the same commit.
- Skipping a version in `CHANGELOG.md` that exists in the source files (the "ghost release": version-string bump that never shipped).
- Cutting a version with no `[Unreleased]` entries; nothing to release.
- Mixing heading formats in one `CHANGELOG.md` (Keep a Changelog semver headings `## [X.Y.Z] - YYYY-MM-DD` alongside sprint headings `## [Sprint N]: ...`). Pick one mode at bootstrap.
- Using a patch bump in 0.x for a feature; `0.X.Y+1` is backwards-compatible fixes only.
- Treating a `0.x` bump as a major bump. There is no major bump before `1.0.0`; `0` to `1.0.0` is the major.
