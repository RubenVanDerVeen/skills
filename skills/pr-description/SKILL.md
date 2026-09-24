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

    ## Choices
    New or updated `docs/artifacts/choices/` decision files, one line each on why. None if the run made or changed no constraining choices.

    ## Docs
    Catalogs and docs updated alongside (README or AGENTS tables, CHANGELOG, command sections). Write None when nothing changed.

## Rules

- Every section present; write None when a section has no content. Never drop a section.
- Derive the description from the execution report when one exists; it already carries the same information.
- On the sbx path, keep PR_DESCRIPTION.md uncommitted at repo root (the daemon amends committed copies out of the push).
- No em-dashes.