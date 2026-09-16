# PR description standard for agent-created PRs

Date: 2026-09-16
Status: approved design (single-pass /full-cycle, decisions taken in-session)

## Problem

Agents create PRs through several paths: the sbx direct path (the inner run writes an uncommitted `PR_DESCRIPTION.md` at repo root; the daemon runs `gh pr create --title <first line> --body-file PR_DESCRIPTION.md`), gateway code runs (the session runs `gh pr create` itself and reports `PR: <url>`), and interactive sessions. Nothing defines what goes into the description. The only contracts that exist are the filename (sbx step 5), the title rule (first line becomes the PR title), and "never merge". Result: inconsistent PR bodies with no problem statement, no verification evidence, and no disclosure of which docs or catalogs were updated alongside.

The requirement: every agent-created PR carries the problem or reason for the change, technical information on what changed and why, how it was verified, and which catalogs or docs were updated.

## Key fact that shapes the solution

This skills repo ships into every sandbox via the `.opencode` bundle (NAS fetch, 15-minute cadence), so agents and skills defined here are picked up by every sbx run automatically. The standard flow inside a run is planner, orchestrator, then documenter for close-out. Per `agents/README.md`, new skills surface in every agent by default (denylist-over-allowlist), so a skill here is visible in all paths without touching the daemon in hermes-console.

## Non-goals

- No daemon (`hermes-console`) changes. The `.task-prompt.md` contract line stays as-is; the inner agents supply the structure.
- No `.github/PULL_REQUEST_TEMPLATE.md`: `gh pr create --body-file` bypasses templates, so it is dead weight for agent PRs.
- No slash command: PR creation is agent-internal; frontmatter description-match is the discovery path. Commands are escape hatches, not defaults.

## Approaches considered

1. **New skill as source of truth plus condensed pointers in the close-out agents (chosen).** Matches the repo precedent: `inventree-naming` is the source of truth and the inventree agents embed a condensed copy. The standard flow gets the template through the documenter (the close-out writer, already scoped to root `*.md` so it can write `PR_DESCRIPTION.md`); non-plan sessions (gateway coder, interactive) hit it via description-match. Single source, no duplication.
2. **Bake the full template into every agent definition.** Rejected: copies drift, every agent def pays the tokens, and the template would be triplicated across documenter, orchestrator, and executor for no gain.
3. **Docs-only template in `docs/workflows/sbx-flow.md`.** Rejected: the console and sandbox never read repo docs at run time (user confirmed).

## The template

The skill defines one description format. First line is the PR title: a Conventional Commits 1.0.0 subject, `<type>(<scope>): <description>` with the repo's types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert). Then four sections:

    ## Problem
    The problem or reason for the change. Link the issue or task source (Plane issue, GitHub issue) when one exists. One short paragraph.

    ## What changed and why
    Technical summary, grouped per change or area: what changed, and the why. Commits and diff stats when useful. No file-list dump; the diff is one click away.

    ## Verification
    How it was verified: commands run and their outcome (verifier output, tests, dry-runs). Evidence, not claims. Name what stayed unverified.

    ## Docs
    Catalogs and docs updated alongside (README or AGENTS tables, CHANGELOG, command sections). Write "None" when nothing changed.

Rules:

- Every section present; write "None" when a section has no content. Never drop a section.
- Derive the description from the execution report when one exists; it already carries the same information (Summary, Files changed, Verifier output, Documentation updates).
- On the sbx path, keep `PR_DESCRIPTION.md` uncommitted at repo root (the daemon amends committed copies out of the push).
- No em-dashes.

## Changes

1. **New `skills/pr-description/SKILL.md`.** Frontmatter `name: pr-description`, description starting "Use when..." targeting PR creation, PR body writing, `PR_DESCRIPTION.md`, `gh pr create`, and PR-url-at-completion reporting. Body: Overview, When to use, the Template (above), the Rules (above). Lean: one template, no references folder, no command.
2. **`agents/documenter.md`:** new numbered step, inserted after the report-writing step (existing steps renumber): when the run requires a PR description (the sbx `PR_DESCRIPTION.md` contract or a `gh pr create` body), write it from the execution report per the `pr-description` skill; `PR_DESCRIPTION.md` stays uncommitted at repo root.
3. **`agents/orchestrator.md`:** step 8 (Documentation dispatch) gains one clause: fold the PR-description requirement into the documenter dispatch when the task requires a PR. No other agents change: executor and gateway sessions hit the skill by description-match.
4. **Catalogs, same commit:** row in `README.md` `## Skills` table plus the Layout block entry, row in `AGENTS.md` `## Current skills` table (folder, frontmatter name, and row entries match exactly).

Single logical change, single commit: `feat(skills): add pr-description standard for agent PRs`.

## Verification

- Pre-commit hooks pass once committed: frontmatter validity (kebab-case name matching folder, "Use when..." description, size limit, headings), em-dash scan over all markdown, new-skill-present-in-both-catalogs check. Requires `git config core.hooksPath .githooks` active in the clone.
- `opencode agent list` parses after the agent edits (per `agents/README.md` maintenance note).
- Manual check: README table row, AGENTS table row, and `skills/pr-description/` folder name all agree.
- Acceptance: an agent told to open a PR (any path) produces the title line plus all four sections.
