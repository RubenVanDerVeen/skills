# Design: vendor the superpowers process skills, drop the plugin

Date: 2026-09-24
Status: approved (approach A selected by user)
Source analysis: explore recon 2026-09-24 (ses_f2af76465ffe1XGYUieIHKlJ6n)

## Context

superpowers 6.1.1 (npm, `github:obra/superpowers`, MIT, Jesse Vincent) is installed as an opencode plugin at `~/.config/opencode/node_modules/superpowers`. The plugin does two things: registers its `skills/` dir at runtime, and prepends the `using-superpowers` bootstrap block to the first user message of every session.

This repo already overrides most of it at the prompt layer:

- Output paths redirected to `docs/artifacts/features/<topic>/` (both skills honor the override clause).
- `agents/orchestrator.md` wave dispatch supersedes `subagent-driven-development`.
- 6 of 14 skills denied by name across 12 agent files (`test-driven-development`, `dispatching-parallel-agents`, both review skills, `finishing-a-development-branch`); `verification-before-completion` has zero references.

Friction: overrides must outvote upstream text every session, upstream updates are drift risk, every generated plan carries the REQUIRED SUB-SKILL boilerplate, and brainstorming's one-question-at-a-time rule conflicts with the user's recorded preference for batched questions (harvest 2026-07-03).

## Goal

Own the process-skill layer as first-class files in this repo. Conventions live in skill bodies, not in prompt clauses layered over upstream.

## Decision record

- "Finetuned" means fork + tailor markdown. No model finetuning: skills-as-markdown is versioned, deterministic, and cheap to iterate.
- Vendor exactly 5 skills: `brainstorming`, `writing-plans`, `using-git-worktrees`, `systematic-debugging`, `writing-skills`.
- Drop the other 9, including `using-superpowers`. The session bootstrap injection disappears with the plugin; accepted. Upgrade path if generic sessions get sloppy: a ~20-line local plugin injecting an own bootstrap.
- Skill names stay identical: deny lists and bare-name invocations in `commands/`, `agents/` keep resolving.
- Descriptions minimally adjusted to the repo frontmatter standard ("Use when..." form), trigger keywords preserved.
- Deny lists in `agents/*.md` stay as-is: denying nonexistent skills is harmless and defensive against reinstall.
- Each vendored `SKILL.md` carries a credit line: "Adapted from obra/superpowers (MIT)."
- No `### Versioning` subsection in this repo's AGENTS.md: unversioned, no bump.

## Per-skill edit specs

Source for all: `~/.config/opencode/node_modules/superpowers/skills/<name>/SKILL.md`.

### brainstorming (159 lines / 1553 words)
- Spec path becomes native: `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md`.
- Questions batched in one message, multiple-choice sets preferred (recorded user preference).
- Keep: HARD GATE (design approval before any implementation), checklist flow, 2-3 approaches rule, terminal state = writing-plans.
- Drop: visual companion (all of `scripts/`, the offer flow), `elements-of-style` reference.
- Restructure to repo body rules: `## Overview` first, no em-dashes, compliant frontmatter.

### writing-plans (174 / 1068)
- Plan path becomes native: `docs/artifacts/features/<feature>/YYYY-MM-DD-<slug>-plan.md`.
- Drop: the REQUIRED SUB-SKILL header boilerplate; the subagent-driven-development / executing-plans handoff section.
- Replace with: execution goes through `/execute-plan` (`commands/execute-plan.md`) and `agents/orchestrator.md` wave dispatch.
- Keep: task format (explicit steps, per-task verification, disjoint `**Files:**` lists the orchestrator depends on).

### using-git-worktrees (202 / 1154)
- Near as-is. Heading restructure, em-dash sweep, light trim of repeated rationale.

### systematic-debugging (296 / 1504)
- Keep the core method (hypotheses first, test cheapest first, follow evidence). Trim repetition; long reference material moves to `references/`.

### writing-skills (689 / 3807)
- Heaviest. Keep the authoring method and checklist; move examples to `references/`; trim ceremony. Target under ~2000 words in the body.

## Repo integration

Ships per the repo's skill rules; catalogs update in the same commit as each skill:

- `README.md` `## Skills` table + `AGENTS.md` `## Current skills` table, one row each, alphabetical.
- Frontmatter: kebab-case `name` matching folder, description starting "Use when...", under 1024 chars.
- Body: starts `## Overview`, no em-dashes (enforced by pre-commit hook).

Suggested descriptions (trigger keywords preserved from the originals):

- brainstorming: "Use when doing any creative work before implementation - creating features, building components, adding functionality, or modifying behavior. Explores intent, requirements, and design before any code is written."
- writing-plans: "Use when you have a spec or requirements for a multi-step task, before touching code."
- using-git-worktrees: "Use when starting feature work that needs isolation from the current workspace, or before executing implementation plans."
- systematic-debugging: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes."
- writing-skills: "Use when creating new skills, editing existing skills, or verifying skills work before deployment."

## Reference updates (live files only; `docs/artifacts/**` history stays untouched)

- `skills/multi-plan-orchestration/SKILL.md`: `superpowers:brainstorming` to `brainstorming`; `superpowers:using-git-worktrees` to `using-git-worktrees`; the `superpowers:subagent-driven-development or executing-plans` dispatch line points to `/execute-plan` + the orchestrator flow instead.
- `skills/rubens-project-standardization/references/artifacts.md`: update "when delegating to superpowers:..." phrasing to local skill names; the redirect table stays as documentation of framework defaults.
- `AGENTS.md`: "writing-skills skill (from superpowers)" becomes local; the delegation-path rule wording updates (paths are now native, not an override of an external framework).
- `opencode-install.md`: remove the "install superpowers" step; the vendored skills ship with the normal repo sync.
- `external-skills.md`: superpowers entry gains "process skills forked into this repo 2026-09-24, MIT".
- `docs/workflows/workflow.md`: update the using-superpowers session-start description (no longer injected).
- `docs/workflows/stack.drawio`: layer-2 label "superpowers plugin v6.1.1 (using-superpowers...)" (~line 56) becomes "vendored process skills (this repo)".
- `README.md`: drop the external-skills bullet and the quick-install URL that point at installing superpowers (~lines 32, 46-47); renumber any list they belong to.
- Historical plan files keep their old boilerplate headers: they are records, not live flows.

## Machine config (outside the repo; runs LAST)

Only after all skills and catalogs are committed:

1. Remove the superpowers entry from the `plugin` array in `~/.config/opencode/opencode.json`.
2. `npm uninstall superpowers` in `~/.config/opencode/`.
3. Sync the 5 vendored skill folders to `~/.claude/skills/` and `~/.config/opencode/skills/` per the two-step sync pattern.

Ordering matters: nothing in this or the next session may resolve a missing skill.

## Accepted losses

- No upstream superpowers updates. Acceptable: the flow has diverged; updates were drift risk, not value.
- The `using-superpowers` bootstrap injection is gone for sessions outside this repo.
- `verification-before-completion` was never referenced and is not vendored (considered, dropped).

## Verification

- Pre-commit hooks pass on every commit (frontmatter, catalogs, em-dash, forbidden paths).
- Em-dash scan over vendored files returns empty.
- No live-flow `superpowers:` namespaced references remain outside `docs/artifacts/**`.
- Catalogs list all 5 vendored skills; folder names match frontmatter names.
- `~/.config/opencode/opencode.json` parses as valid JSON after the edit; `npm ls superpowers` in `~/.config/opencode` returns empty.
- Smoke check: a skill listing resolves `brainstorming` and `writing-plans` from the local copy, not node_modules.

## Success criteria

- `/full-cycle` and `/execute-plan` run entirely on repo-owned skills and agents.
- Zero remaining prompt-layer override clauses for paths or execution flow.

## Out of scope

Model finetuning, a replacement bootstrap plugin, vendoring the 9 dropped skills, rewriting historical artifacts.
