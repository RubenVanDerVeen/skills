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
