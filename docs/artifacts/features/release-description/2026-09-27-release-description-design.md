---
title: Release description standard for agent-created releases
date: 2026-09-27
type: design
status: approved (decisions taken in-session)
tags: [releases, versioning, changelog, skills, agent-pipeline]
related: [pr-description, project-standardization/versioning, version-bump-on-ship]
---

# Release description standard for agent-created releases

Date: 2026-09-27
Status: approved design (decisions taken in-session)

## Problem

The agent pipeline (planner, orchestrator, documenter) ships features and fixes via plan branches and PRs. For versioned projects, `agents/documenter.md` step 6 ("Ship bump") already finalizes a `chore(release): vX.Y.Z` commit at close-out and `references/versioning.md` step 5 references `git tag -a vX.Y.Z -m "..."`. Neither surface has a defined body shape: the commit subject is constrained but the body is freeform, and the tag annotation message is literally a `"..."` placeholder. Result: every release-cut currently invents its own format, the `git log` archaeology of release commits is hit-or-miss, and the GitHub or GitLab Release page (when one is published) carries whatever the user typed that day.

Three surfaces are in scope. They are written at different moments and read by different audiences, so they are not interchangeable, but they are all "the description of a release" and currently have no shared rule:

1. **The body of the `chore(release): vX.Y.Z` commit** (always, when the project is versioned).
2. **The git tag annotation message** (`git tag -a vX.Y.Z -m "<message>"`) (when the project's CI triggers release builds from tags, per `versioning.md` step 5).
3. **The GitHub or GitLab Release description** (when the release is published via `gh release create`, the platform UI, or any equivalent).

The user requirement, decided in this session: one shared template, three copy sites. The body shape is user-facing (audience: users and downstream maintainers, not this repo's agents). Internal jargon and commit hashes stay out of the body; the diff and the commit log are one click away on the release page.

## Non-goals

- No daemon (`hermes-console`) changes. The standard flow inside a run is planner, then orchestrator, then documenter for close-out; the documenter is already the writer of the `chore(release)` commit and the natural place to emit the tag annotation and Release description when called for.
- No new agent definitions. The `documenter` agent already has the close-out scope. The `orchestrator` already dispatches the documenter at step 8.
- No new slash command. Release description is an agent-internal task at close-out; description-match against the new skill is the discovery path. Commands are escape hatches, not defaults (see `AGENTS.md` "When to add a command").
- No platform-specific codepath. The template is platform-agnostic; the documenter picks the platform's release command (`gh release create`, `glab release create`, or no-op when the project only annotates the tag) at run time.
- No backfill of past releases. The repo's `CHANGELOG.md` already carries every shipped change in Keep a Changelog 1.1.0 format; past releases are not retro-tagged or re-described.

## Approaches considered

1. **One skill as source of truth, template derived from execution report (chosen).** Mirrors the `pr-description` precedent (2026-09-16): `skills/pr-description/SKILL.md` is the source of truth, the documenter writes `PR_DESCRIPTION.md` from the execution report. Same shape, same audience logic. The documenter writes the release-description body from the same execution report it already reads for the PR description; the bodies share sections (`Problem`, `Verification`, `Docs`) with wording tuned for the audience. One source, one template, no duplication.

2. **Bake the template into `agents/documenter.md`.** Rejected: copies drift across documenter edits, the template would be specific to one agent, and it pulls all of `versioning.md`'s policy into the agent body that already references it by pointer.

3. **Three separate templates (commit body, tag annotation, Release page).** Rejected: the user explicitly chose one template with three copy sites. Three templates also opens a drift vector between the git tag annotation and the GitHub Release description, which is the exact "two sources of truth" failure mode the `pr-description` skill was designed to prevent.

## The template

The skill defines one body shape. The `chore(release): vX.Y.Z` subject stays unchanged (it is already enforced by the `commit-msg` hook and the documenter's close-out step). The body fills in five sections, in this order:

```
## Summary
One paragraph in plain language. What is in this release and why a user cares.
Mention the version, the cadence ("weekly", "monthly", "ad-hoc") when it
is stable, and the audience ("library users", "CLI users", "desktop app
users") when known. Two to four sentences. No commit hashes.

## Highlights
Three to five bullets, user-visible changes only. Pull from the [Unreleased]
Added and Changed sections of CHANGELOG.md and rephrase for users
("Added dark mode", not "feat(ui): add dark mode toggle"). Each bullet
starts with a verb in past tense. Internal-only refactors and chores
belong in "Internal" below, not here.

## Breaking changes
One bullet per BREAKING CHANGE footer in the commit range since the last
tag, in the order:
  - **<one-line name>** - <what changed>. Migration: <link or one-line>.
Write "None" when the range has no BREAKING CHANGE footer. This section
must never be dropped, even when empty: empty is information.

## Internal
Refactors, chore commits, dependency bumps, test changes that shipped in
this release but are not user-visible. Write "None" when none. Skip the
section entirely only for trivial patch releases where the user signal is
zero.

## Full changelog
Link to the diff range or to the CHANGELOG section:
- For GitHub: `[vX.Y.Z...vX.Y+1.Z](https://github.com/<owner>/<repo>/compare/vX.Y.Z...vX.Y+1.Z)`
- For GitLab: the equivalent `<from>...<to>` compare URL.
- For tag-only projects: a relative link to the CHANGELOG heading
  `## [X.Y.Z] - YYYY-MM-DD` in the same repo.
Pick the form that matches the project's hosting. The link is the only
place commit hashes appear in the body.
```

### Rules

- Every section present. Write `None` when a section has no content. Never drop a section, including `Breaking changes` (empty is information).
- Derive the body from the execution report and `[Unreleased]` entries, never invent.
- Audience is users and downstream maintainers. No internal jargon. No commit hashes in the body (the diff link is one click).
- One template, three copy sites:
  - Commit body (after the `chore(release): vX.Y.Z` subject).
  - Tag annotation message (`git tag -a vX.Y.Z -m "<body>"`).
  - GitHub or GitLab Release description (`gh release create <tag> --title "vX.Y.Z" --notes-file <body>`).
  All three are the same text, character-for-character. No platform-specific rewording. This is the one source of truth rule; two sources of truth drift.
- Skip the Release description copy step when the project does not publish one. The commit body and tag annotation are always written.
- The `[Unreleased]` heading rename to `## [X.Y.Z] - YYYY-MM-DD` is unchanged from `references/versioning.md` step 3. The Release description references the new heading, not the old `[Unreleased]`.
- No em-dashes (U+2014) in any field. Same rule as every file in this repo.

## Skill scope and folder layout

New skill `skills/release-description/`, modeled on `skills/pr-description/`. Lean: one `SKILL.md`, no `references/` folder, no command file.

```
skills/release-description/
└── SKILL.md
```

### Frontmatter

```
name: release-description
description: Use when writing the body of a `chore(release): vX.Y.Z` commit, annotating a git tag with `git tag -a`, or filling in a GitHub or GitLab Release description (`gh release create --notes-file`, the platform Release UI). Triggers on release notes, release description, tag annotation, changelog release, cut a release, ship vX.Y.Z.
```

Description length target: under 500 characters. Frontmatter total under 1024 characters (the agents.md limit per `AGENTS.md` "SKILL.md frontmatter rules").

### Body shape

```
## Overview
## When to use
## Template
## Rules
## Audience and tone
## Related
```

`## Overview`: one paragraph explaining the three surfaces and the one-source-of-truth rule.
`## When to use`: three bullets, one per surface (commit body, tag annotation, Release description).
`## Template`: the five-section body from above.
`## Rules`: the rules block from above, in order.
`## Audience and tone`: short paragraph reinforcing user-facing language, no commit hashes in the body, internal-only changes go in `## Internal` not `## Highlights`.
`## Related`: pointers to `skills/pr-description/` (sibling), `skills/rubens-project-standardization/references/versioning.md` (the policy that triggers the close-out step), `docs/artifacts/features/version-bump-on-ship/2026-09-19-version-bump-on-ship-design.md` (the ship-bump default that makes this skill fire on every versioned ship).

Token budget target: lean, under 400 words in the body. The template block is the heaviest piece and stays copy-pastable.

## Changes

1. **New `skills/release-description/SKILL.md`.** Frontmatter per above. Body per above. Lean: one template, no references folder, no command.
2. **`skills/rubens-project-standardization/references/versioning.md` step 5:** replace the placeholder `git tag -a vX.Y.Z -m "..."` with `git tag -a vX.Y.Z -m "$(cat <body-file>)"` plus a pointer to the `release-description` skill. The policy pointer at the top of `versioning.md` gains one line: "Tag annotation and Release description bodies: see the `release-description` skill."
3. **`agents/documenter.md` step 6 (Ship bump):** after the `chore(release): vX.Y.Z` commit step, add a numbered step 6.1 that writes the release-description body to a scratch file at `<repo-root>/.release-notes.md`, then:
   - Passes the file as `--notes-file` to the release-publish command if the project publishes a Release page (`gh release create <tag> --title "vX.Y.Z" --notes-file .release-notes.md` or platform equivalent). Detection: presence of `gh release` or `glab release` references in the project's CI or a declared "publishes releases" flag in `AGENTS.md -> Versioning`.
   - Passes the file content as the tag annotation message when annotating the tag (`git tag -a vX.Y.Z -m "$(cat .release-notes.md)"`). Tagging only happens when the user invokes the deliberate release-cut, not at the default ship bump.
   - Removes the scratch file at end of step (or leaves it gitignored at `.release-notes.md` if the project already ships a similar scratch convention).
   This step is skipped when the project is unversioned (`AGENTS.md -> Versioning` absent) or when the ship bump determined "no bump" (docs-only ship per `versioning.md` ship-bump trigger rule).
4. **`agents/orchestrator.md` step 8 (Documentation dispatch):** one clause in the documenter dispatch instructions: when the task includes a release, write the release-description body per the `release-description` skill. No other agent definitions change.
5. **Catalogs, same commit:** row in `README.md` `## Skills` table (alphabetical, between `pr-description` and `rubens-project-standardization`), one line in the `## Layout` block under `skills/release-description/SKILL.md`, row in `AGENTS.md` `## Current skills` table (alphabetical, between `pr-description` and `rubens-project-standardization`).
6. **`CHANGELOG.md` `[Unreleased] / Added`:** one bullet describing the new skill and the spec path, matching the `pr-description` precedent on line 35.

Single logical change, single commit: `feat(skills): add release-description standard for releases, tags, and changelog headings`.

## Verification

- Pre-commit hooks pass once committed: frontmatter validity (kebab-case `name` matching folder, "Use when..." description, size limit, headings), em-dash scan over all markdown, new-skill-present-in-both-catalogs check, forbidden-paths scan. Requires `git config core.hooksPath .githooks` active in the clone.
- `opencode agent list` parses after the agent edits (per `agents/README.md` maintenance note).
- Manual check: README table row, AGENTS table row, and `skills/release-description/` folder name all agree.
- Consistency read: the documenter step and `references/versioning.md` step 5 use the same wording for the tag-annotation command and the same pointer to the `release-description` skill.
- Acceptance: an agent told to "cut a release" (any path) produces the commit subject `chore(release): vX.Y.Z`, a body with all five sections (no section dropped, `None` written where empty), and the tag annotation message identical to the commit body, character-for-character. The `[Unreleased]` heading is renamed to `## [X.Y.Z] - YYYY-MM-DD` per the existing `versioning.md` step 3.

## Out of scope

- Multi-line commit subjects, emoji subjects, or other release-commit subject variants. The subject stays `chore(release): vX.Y.Z`, no exception. The body carries the variation.
- Templating the Highlights bullets per language or framework. The Highlights section is rephrased manually from the `[Unreleased]` entries; templating it would freeze the wording.
- Auto-generating the Release description from the commit log. The body is derived from the execution report and the CHANGELOG, not from `git log`. The audience is users, not maintainers.
- Migration guide generation. When a release contains breaking changes, the body points at a migration guide or a one-line migration note; the guide itself is a separate deliverable, out of scope here.
- A slash command. Release description is an internal close-out step; description-match is the discovery path.
