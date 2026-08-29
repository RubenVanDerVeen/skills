# Design: split `standardizer` into `doc-standardizer` + `code-standardizer`

Date: 2026-08-29
Status: approved (naming and dispatch flow confirmed by user)

## Overview

The single `standardizer` agent runs a merged audit: repo/docs conventions via `project-standardization` (paragraphs 1-3 of its body) plus code structure via `code-standardization` (paragraph 4). Split it into two read-only subagents:

- `doc-standardizer`: repo/docs conventions audit (kebab-case paths, AGENTS.md sections, `docs/artifacts/` layout, changelog, catalog rows, Conventional Commit hygiene, versioning sync).
- `code-standardizer`: code-structure audit (the 4 checks per language: presence, documentation, consistency, boundaries; pinned formatter/linter in check mode).

## Motivation

- Each dispatch loads one heavy skill instead of two, roughly halving per-audit context.
- Findings arrive separated by domain; the execution report can attribute quick-fixes cleanly.
- Mirrors the existing command pair: `/standardize` (project bootstrap) and `/standardize-code` (code checks).

## Decisions (user-confirmed)

1. Naming: rename the existing agent to `doc-standardizer` (full rename, no `standardizer` name survives) and add `code-standardizer`.
2. Dispatch flow: sequential chain. `doc-standardizer` first, then `code-standardizer`, then ONE executor pass over all combined `quick-fix` findings, then ONE reviewer recheck.

## Agent definitions

### `agents/doc-standardizer.md` (rename of `agents/standardizer.md`)

- `git mv agents/standardizer.md agents/doc-standardizer.md` (preserves history).
- Frontmatter `description`: keep the current first half (repo conventions audit, PASS or numbered findings, read-only, dispatch timing) and drop the sentence "Also loads `code-standardization` and audits code structure in the same pass...".
- Body: keep paragraphs 1-3 (project-standardization audit + versioning policy). Delete paragraph 4 (the code-standardization pass).
- Skill denylist: add `"code-standardization": deny`. All other frontmatter (mode `subagent`, color, model pin, tool/permission denies, `homelab*` deny) unchanged.

### `agents/code-standardizer.md` (new file)

- Same frontmatter scaffold as doc-standardizer: mode `subagent`, color `info`, model `zai-coding-plan/glm-5.3`, identical read-only tool and permission denies, `homelab*` deny, same planning/review skill denylist.
- `description`: audits the executed branch diff against the `code-standardization` skill: formatter/linter config presence, per-language naming and module-organization rules, architecture boundary adherence. Returns PASS or numbered findings tagged quick-fix or recommendation. Read-only.
- Body: the current paragraph 4, promoted to a standalone mandate: load `code-standardization`; for each language in the diff run the four checks (presence, documentation, consistency, boundaries) using `references/<lang>.md`; run the pinned formatter/linter in check mode if installed (`command -v`), otherwise emit a quick-fix finding naming tool and config; never re-lint in the agent body; same PASS / numbered findings format with `quick-fix` / `recommendation` tags.
- Skill denylist: add `"project-standardization": deny`.

## Dispatch flow changes

Sequential chain replaces the single merged dispatch:

1. `doc-standardizer` audits the branch diff (repo conventions + versioning).
2. `code-standardizer` audits the same diff (code structure).
3. One `executor` pass fixes all combined `quick-fix` findings from both.
4. One `reviewer` pass re-checks the fixes.
5. `documenter` receives both audits' findings (fixed vs remaining recommendations).

## Reference sweep (per-file mapping)

No blind sed: each mention maps to its successor by meaning.

| File | Change |
|---|---|
| `agents/orchestrator.md` | Task allowlist: replace `"standardizer": allow` with `"code-standardizer": allow` and `"doc-standardizer": allow` (keep broad-rule-first ordering). Step 6: dispatch doc-standardizer then code-standardizer, then one executor pass for combined quick-fixes, then reviewer recheck. Steps 8-9: "standardizer findings" becomes the doc/code-standardizer findings; report lists both dispatches. |
| `commands/execute-plan.md` | Step 4 mirrors the new sequential chain. Steps 5 and 7: findings and dispatch lists name both agents. |
| `commands/full-cycle.md` | Step 4: "structure review (`doc-standardizer` then `code-standardizer` plus quick-fix `executor` passes)". |
| `agents/documenter.md` | Inputs: the doc-standardizer's and code-standardizer's findings, which were fixed vs remaining. Step 1: read both audits' findings. |
| `commands/standardize-code.md` | Line 17: "same format as the `code-standardizer` agent". |
| `skills/code-standardization/SKILL.md` | Description tail: "Pairs with the `code-standardizer` agent for post-plan code audits." Body L10, heading L40, L42: the agent is `code-standardizer`, single audit pass over code structure only. |
| `skills/code-standardization/references/*.md` (python, go, rust, typescript-javascript, c-cpp, architecture, tooling) | All ~74 mentions, including every "Standardizer check:" line, become "code-standardizer check:" / `code-standardizer`. |
| `skills/rubens-project-standardization/references/versioning.md` | L72-74 "The 3 standardizer checks" becomes "The 3 doc-standardizer checks". |
| `agents/README.md` | Roster: split the `standardizer` row into `doc-standardizer` (repo conventions, loads project-standardization) and `code-standardizer` (code structure, loads code-standardization). L19 prose: post-implementation review dispatches both. |
| `AGENTS.md` | Agent-definitions paragraph (L101): roster list gains `doc-standardizer`, `code-standardizer` in place of `standardizer`; "post-implementation structure review goes to `doc-standardizer` and `code-standardizer`". |
| `README.md` | L24 agent list is stale (names only 3 agents). Replace it with a pointer to `agents/README.md` as the roster (avoids future staleness). |
| `opencode-install.md` | Step 9.3 and `## Verify`: name the full current agent file set including both new agents. |
| `docs/workflows/workflow.md` | 5 spots: model table (both agents listed), skills table pairings, agent roster table (two rows), execute-plan description, 8-step loop description (two sequential audits). |
| `docs/workflows/plan-flow.drawio` | Split node `nStandardizer` (merged-audit label) into `nDocStandardizer` then `nCodeStandardizer`, sequential edges into `nDocumenter`; keep existing node style. Legend (L190 region): doc-standardizer loads project-standardization, code-standardizer loads code-standardization, two sequential audit passes cover repo + code. |
| `docs/workflows/stack.drawio` | Relabel `aStandardizer` to `doc-standardizer` and add a sibling `code-standardizer` node in the same style. |
| `docs/workflows/multi-plan-flow.drawio` | Legend line: name both standardizers in the post-loop review. |
| `CHANGELOG.md` | Append a new entry describing the split, following the file's existing top-section convention (Keep a Changelog). Never edit history. |

## Out of scope (do not touch)

- `docs/artifacts/**` (~120 mentions: immutable execution history).
- `CHANGELOG.md` existing entries.
- The `standardize` / `standardize-code` command bodies beyond the mapping above (no behavior change to the commands themselves).
- Any parallel-dispatch or conditional-dispatch logic.

## Verification

1. Copy `agents/doc-standardizer.md` and `agents/code-standardizer.md` to `~/.config/opencode/agents/`; remove a stale `~/.config/opencode/agents/standardizer.md` if present (Test-Path guard).
2. `opencode agent list` parses; `opencode debug agent doc-standardizer` and `opencode debug agent code-standardizer` resolve.
3. `git log --follow agents/doc-standardizer.md` shows pre-rename history.
4. Grep: no standalone `standardizer` remains in live files: `rg -P "(?<!doc-)(?<!code-)[sS]tandardizer" -g '!docs/artifacts/**' -g '!CHANGELOG.md'` returns empty (CHANGELOG history and artifacts excluded).
5. Em-dash check on all edited files returns empty.
6. Each task's verifier confirms the per-file mapping table above.

## Alternatives considered

- Keep `standardizer` as the docs half, add only `code-standardizer`: less churn, but asymmetric and ambiguous. Rejected by user decision.
- Parallel dispatch of both audits: saves wall-clock, complicates the orchestrator loop and failure handling. Rejected for sequential simplicity.
- Conditional code audit (only when diff touches source files): saves a dispatch on docs-only branches, adds a gating rule. Rejected (YAGNI).
