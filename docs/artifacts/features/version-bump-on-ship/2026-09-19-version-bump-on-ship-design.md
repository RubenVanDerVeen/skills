# Version bump on ship: design

Date: 2026-09-19
Status: approved (single-pass full-cycle)

## Problem

The agent pipeline (planner -> orchestrator -> documenter) ships features and fixes via plan branches and PRs, but never touches the project version. The existing policy in `skills/rubens-project-standardization/references/versioning.md` makes any version change a deliberate, user-invoked release cut, so versions rot while features ship. Requirement from the user:

- Shipping a feature with a branch or PR bumps the version per Conventional Commits/SemVer (feature -> `0.x.0` pre-1.0, major bump post-1.0 as `x.0.0` only for breaking changes).
- A fix bumps `0.0.x`.
- The planner must be aware of this; the documenter must always implement it.
- Evaluate whether project-standardization also needs to cover it: yes, it owns the policy and its trigger rule currently contradicts the new default.

## Approaches considered

- **A. Amend the existing policy and wire planner + documenter (chosen).** `references/versioning.md` already has the SemVer decision table, canonical-source and sync-target rules, and the release-cut recipe. Only the trigger rule changes; two agent files gain a few lines. Smallest diff that satisfies every requirement.
- **B. Auto release-cut in the orchestrator.** Rejected: duplicates the close-out phase, and the user explicitly named the documenter as the implementer.
- **C. New standalone versioning skill.** Rejected: YAGNI. The policy already lives in project-standardization; a second copy would drift.

## Decision: ship-bump by default

Reuse the existing decision table in `references/versioning.md` verbatim. Change only the trigger rule:

1. **Applicability gate.** Bump only if the project declares a canonical version source (the `Versioning` section in `AGENTS.md`). Unversioned projects (docs/content repos like this skills repo) skip the bump; the execution report notes this in one line.
2. **Classification.** Per the existing table: `feat` -> `0.(X+1).0` pre-1.0, `(Y+1).0` post-1.0; `fix` -> `0.X.(Y+1)`; breaking change -> `+1.0.0`; only `docs`/`chore`/`test` commits -> no bump.
3. **Close-out mechanics (documenter).** When the shipped branch contains bump-worthy commits and the project is versioned: bump the canonical source plus every declared sync target, rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` and add the link reference, all in a single `chore(release): vX.Y.Z` commit. A docs-only ship leaves `[Unreleased]` open and does not commit.
4. **Release-cut stays user-invoked.** Tagging and CI-triggered release flows keep the existing deliberate recipe; ship-bump only finalizes the version, it never tags by itself.

## Changes

| File | Change |
|---|---|
| `skills/rubens-project-standardization/references/versioning.md` | Amend the two-phase trigger rule (plan execution appends `[Unreleased]`; close-out bumps when applicable; release-cut stays deliberate). Touch up anti-patterns that say bumping is never automatic. |
| `agents/planner.md` | Plan step: check `AGENTS.md -> Versioning`, state the expected bump (or "unversioned, skip") in the plan; dispatch instruction list gains the changelog/bump mention. |
| `agents/documenter.md` | New numbered ship-bump step in "Do, in order"; write scope widened to declared version sources and root `CHANGELOG.md`. |
| `templates/AGENTS-*.md` (all three tiers) | Versioning trigger field default text updated to the ship-bump default. |
| Catalog/doc sync | `agents/README.md` role blurbs if they enumerate documenter/planner duties; root `CHANGELOG.md` entry under the current milestone grouping. |

Out of scope: tagging, CI wiring, executor/reviewer/oracle definitions, the `pr-description` skill, and any version for this repo itself (it is unversioned by design).

## Verification

- No em-dashes (U+2014) in any edited file (pre-commit hook enforces repo-wide).
- Pre-commit hooks pass on every commit: frontmatter checks, catalog checks.
- Consistency read: the documenter step and the amended `versioning.md` trigger rule use the same wording for the applicability gate and the commit mechanics.
- Grep confirms `agents/planner.md` and `agents/documenter.md` now contain the ship-bump instructions and `references/versioning.md` no longer claims bumping is never automatic.
