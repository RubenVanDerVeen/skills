# Design: Conventional Branch standard adoption

Date: 2026-09-20
Status: approved (single-pass)
Source spec: https://conventionalbranch.org/ (Conventional Branch 1.1.0)

## Problem

The repo already uses Conventional-Branch-shaped branch names (`feat/<scope>`, `fix/...`, `chore/...`, `<type>/<plan-slug>`, `feat/<slug>-spN-<name>`), but:

- `STANDARDS.md` (root) and `skills/rubens-project-standardization/templates/STANDARDS.md` have **zero** branch coverage: no Stack row, no section.
- The word "Conventional Branch" and a link to conventionalbranch.org appear nowhere.
- `orchestrator` is the only agent that creates branches, yet branch naming lives only in `commands/execute-plan.md`; the agent file itself never states it, so application is not "by default".
- `AGENTS.md` still offers the legacy `plan-<name>` alternative, which violates the spec grammar (no type prefix).
- Branch types used in practice (`docs/`, `refactor/`, `test/`, `ci/`) are not in the spec's type list; the spec allows custom types but requires they be documented.

## Decision (approach 1 of 3, recommended)

**Adopt Conventional Branch 1.1.0 as a named standard, document the repo's extensions as sanctioned custom types, drop the legacy `plan-<name>`, and make the branch-creating agent apply the convention by default. No git hooks.**

Rejected:

- *Strict spec types only* (`feature|feat|bugfix|fix|hotfix|release|chore`): breaks the existing execute-plan mapping where a docs-heavy plan branches as `docs/...` or `refactor/...`. Churn without benefit.
- *Hook enforcement* (branch-name check in `.githooks/`): machinery nobody asked for; docs + agent defaults cover the actual need.

## Spec-conformance notes

- Trunk: `main` (unprefixed). Valid.
- `feat/<slug>` = short alias of `feature/<slug>`. Valid per spec.
- `feat/<slug>-spN-<name>`: hyphens separate desc-segments; `spN` is a valid segment. Valid per grammar.
- `plan-<name>`: no type prefix, not a trunk name. **Invalid. Remove.**
- Custom types `docs/`, `refactor/`, `test/`, `ci/` (mirroring Conventional Commit types): spec-sanctioned team extension, must be documented. STANDARDS.md documents them.
- AI agent source prefixes (`ai/`, `claude/`, `codex/`, `copilot/`, `cursor/`): listed in the reference table as allowed, not required for this repo.

## Changes (file by file)

1. **`STANDARDS.md` (root)**
   - Stack table: add row `| Conventional Branch 1.1.0 | **yes** | Branch names |`.
   - New section after "Commit messages": `## Branches: Conventional Branch 1.1.0`. Format `<type>/<description>`, lowercase alphanumerics + hyphens (dots only in release versions), no consecutive/leading/trailing separators, trunk (`main`) unprefixed. Table of types: spec types (`feature|feat`, `bugfix|fix`, `hotfix`, `release`, `chore`) plus documented project extensions (`docs`, `refactor`, `test`, `ci`) and the multi-plan suffix rule (`feat/<slug>-spN-<name>`, dashes never nesting). Link https://conventionalbranch.org/ in References.
2. **`skills/rubens-project-standardization/templates/STANDARDS.md`**
   - Same Stack row + a condensed generic branch section (spec types + "document your custom types" note, no repo-specific `-spN-` rule).
3. **`AGENTS.md` (root)**
   - Replace the `feat/<scope> (or a per-plan plan-<name>)` bullet in "Git & workflow" with a Conventional Branch bullet: `<type>/<scope>` per STANDARDS.md, examples `feat/`, `fix/`, `docs/`, `chore/`; drop `plan-<name>`.
4. **`agents/orchestrator.md`**
   - Add one line where it branches (bootstrap step): create `<type>/<plan-slug>` per Conventional Branch 1.1.0 (STANDARDS.md), type matches the dominant commit type of the plan.
5. **`commands/execute-plan.md`**
   - Step 2 already names `<type>/<plan-slug>`; append "(Conventional Branch 1.1.0, see STANDARDS.md)".
6. **`skills/rubens-project-standardization/references/standards-stack.md`**
   - Add Conventional Branch 1.1.0 to the "always apply" floor list next to Conventional Commits, with one-line rule.
7. **`skills/rubens-project-standardization/templates/AGENTS-small.md`, `AGENTS-medium.md`, `AGENTS-large.md`**
   - Update the feature-branch bullet: `feat/<scope>` per Conventional Branch, drop `plan-<name>`.
8. **`CHANGELOG.md`**
   - Added entry: Conventional Branch 1.1.0 adopted in STANDARDS.md (root + template) and agent defaults; legacy `plan-<name>` branch scheme removed.

## Out of scope (YAGNI)

- Branch-name git hook or commit-check tooling.
- `release/` or AI-source prefix workflows (allowed, unused here).
- Renaming any existing branch or rewriting multi-plan scheme (already spec-valid).

## Success criteria

- `Select-String "Conventional Branch"` hits: root STANDARDS.md, template STANDARDS.md, AGENTS.md, agents/orchestrator.md, commands/execute-plan.md, standards-stack.md, CHANGELOG.md.
- No `plan-<name>` string remains in tracked markdown (grep `plan-<name>` returns empty outside changelog history notes).
- No em-dashes (U+2014) in any touched file (repo-wide rule; pre-commit enforces).
- Multi-plan suffix scheme documented as valid extension; existing branch examples in docs unchanged where already valid.
