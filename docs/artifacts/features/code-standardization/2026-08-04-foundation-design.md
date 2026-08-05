# code-standardization Foundation Design

## Status

Approved 2026-08-04. Foundation sub-project of the code-standardization multi-plan (see `docs/artifacts/features/code-standardization/2026-08-04-code-standardization-outline.md`).

## Problem

The `standardizer` agent and `project-standardization` skill cover repo/docs/process structure only (kebab-case paths, AGENTS.md sections, `docs/artifacts/` layout, changelog, catalog rows, Conventional Commits, ISO dates). They say nothing about **code**: no file naming inside source trees, no formatting/linting infrastructure, no module organization, no architecture boundaries, no per-language style. The standardizer cannot audit code structure because no skill defines what to audit against.

## Solution (foundation scope)

Create the `code-standardization` skill skeleton plus the cross-language references and the agent/command/catalog wiring. The foundation **does not** write any per-language guide; it freezes the template the five language sub-plans consume.

### Skill identity

- Folder: `skills/code-standardization/`
- Frontmatter `name`: `code-standardization`
- Frontmatter `description` (triggering only, "Use when...", <1024 chars):

> Use when standardizing or auditing the *structure of source code* itself (not the repo layout): setting up a formatter/linter/hooks for a project, defining per-language naming and module-organization rules, enforcing architecture/dependency boundaries, or reviewing a branch for code-structure violations. Triggers: "standardize the code", "code conventions", "set up ruff/eslint/gofmt", "lint config", "architecture rules", "dependency boundaries", "code style for X". Covers Python, TypeScript/JavaScript, C/C++, Go, Rust. Flat (non-tiered) standard. Pairs with the `standardizer` agent for post-plan code audits.

### `SKILL.md` body structure

Target <120 lines, <2k tokens. Sections:

1. **Overview**: code structure standard. Flat (one standard, all project sizes). Scope: the code itself, not the repo layout (which is `project-standardization`). Multi-language: Python, TS/JS, C/C++, Go, Rust.
2. **The 4 agent checks**: presence (formatter/linter/hooks configured?), documentation (conventions written down agent-visible?), consistency (new code matches neighbors?), boundaries (architecture rules respected if a spec exists?). The agent does not re-lint; it checks the tools exist, conventions are documented, new code is consistent, and boundaries hold.
3. **The per-language guides**: dispatch table (one row per language → `references/<lang>.md`).
4. **Cross-language references**: links to `references/tooling.md` and `references/architecture.md`.
5. **How the standardizer uses this skill**: load alongside `project-standardization`, run a merged audit pass, return PASS or numbered findings (same quick-fix / recommendation tags).
6. **Commands**: `/standardize-code` table row + sync pattern.
7. **Anti-patterns**: don't restate what the pinned tool enforces line-by-line; don't re-lint in the agent (run the tool, report); don't invent conventions not in the per-language guide.

### `references/tooling.md` (cross-language)

The standardization-infra layer, language-agnostic. Covers:

- **The three-piece kit every language has**: a formatter (opinionated, non-negotiable), a linter (configurable rule set), an import sorter (often folded into the formatter/linter).
- **Config discovery table**: where each language's config lives (`pyproject.toml [tool.ruff]`, `.eslintrc.*` / `eslint.config.js`, `.golangci.yml`, `rustfmt.toml` / `clippy` via `[lints]` in `Cargo.toml`, `.clang-format` + `.clang-tidy`).
- **Hook wiring patterns**: pre-commit framework (Python-native, multi-language), husky + lint-staged (JS), native git hooks for Go/Rust, the project-local `.githooks/` pattern already used in this repo for `commit-msg`.
- **The "pin it" rule**: formatter and linter versions are pinned (lockfile or config), so CI and locals agree.
- **The "don't re-implement the tool in the agent" rule**: the standardizer runs the tool if installed (`command -v <tool> && <tool> --check`); if absent it emits a quick-fix finding, never a re-implementation.

### `references/architecture.md` (cross-language)

The boundary layer, language-agnostic. Covers:

- **Layering**: the canonical dependency direction (e.g. api/presentation → service/domain → data/infra; never reverse). Domain knows nothing about infra.
- **No circular dependencies**: enforced by an arch tool per language (see each `<lang>.md`).
- **Feature/module isolation**: features don't reach into each other's internals; public interface only.
- **Boundary spec**: where the project writes its boundaries down. A short `.agents/architecture.md` or a section in AGENTS.md naming the layers and the allowed direction. The standardizer checks *presence* of this spec for medium+ codebases and checks *adherence* via the arch tool.
- **What the agent checks vs. what the tool checks**: the tool detects cycles and forbidden imports mechanically; the agent checks the boundary spec exists, is current, and that new code's imports respect the declared layers.

### Standardizer agent edit (`agents/standardizer.md`)

Widen the `description` and the body so the agent loads **both** `project-standardization` and `code-standardization`, and runs a **merged audit pass**. Specifically:

- Description: append "Also loads `code-standardization` and audits code structure in the same pass: formatter/linter config presence, per-language naming and module-organization rules, architecture boundary adherence."
- Body: after the repo-structure audit paragraph, add a code-structure audit paragraph: "Then load `code-standardization`. For each language present in the diff, run the 4 agent checks (presence, documentation, consistency, boundaries) using the matching `references/<lang>.md`. Run the pinned formatter/linter in check mode if installed (`command -v`); if absent, emit a quick-fix finding naming the tool and the config file to add. Return findings in the same PASS / numbered-list format with quick-fix / recommendation tags."
- Keep the agent read-only; it reports, the orchestrator dispatches executors for fixes.

### Command file (`commands/standardize-code.md`)

Frontmatter `description` only (no `name` field; filename is the command name). Body: load `code-standardization`; run the 4 agent checks against the current branch or whole repo; report PASS or numbered findings. `$ARGUMENTS` optional for scoping (path or language).

### Catalog updates (same commit as the skill)

Per repo `AGENTS.md` rules, a new skill must land in every catalog in the same commit:

- `README.md` `## Skills` table: add `code-standardization` row (alphabetical).
- `AGENTS.md` `## Current skills` table: add `code-standardization` row (alphabetical).
- `skills/code-standardization/SKILL.md` gets a `## Commands` section pointing to `commands/standardize-code.md` with the sync pattern (mirrors `project-standardization`).

## Frozen per-language template (the contract sub-plans consume)

Every `references/<lang>.md` produced by SP-1..SP-5 MUST have exactly these 8 sections, in this order, with this content shape. Sub-plans instantiate; they do not add, remove, or reorder sections. Language-specific deviation goes *inside* a section, not as a new section.

| # | Section | Content the sub-plan fills in |
|---|---------|-------------------------------|
| 1 | **Toolchain** | Pinned formatter + linter + import sorter; a copy-pasteable config snippet; the check command (`<tool> --check`); hook wiring line. |
| 2 | **Naming** | File names; identifiers (functions, classes/structs, constants, types/interfaces, modules/packages, enums); test file naming. |
| 3 | **Module / file organization** | Source layout convention (e.g. `src/`, flat, package-per-feature); one-X-per-file rule; import ordering rules; file-length ceiling (e.g. ≤400 lines) and complexity ceiling (e.g. cyclomatic ≤10) where a tool enforces it. |
| 4 | **Architecture** | Layering and dependency-direction rules for that language's idioms; the arch tool that enforces no-circular-deps and forbidden imports (e.g. `import-linter`, `dependency-cruiser`, `go vet`/layering linters, clippy rules); feature-isolation rule. |
| 5 | **Documentation** | Doc format (Google-style / TSDoc / rustdoc / Doxygen / godoc); what must be documented (public API minimum); where private docs go. |
| 6 | **Testing** | Framework; test file naming and location; structure (arrange-act-assert or equivalent); what must be tested (public behavior, error paths). |
| 7 | **Error handling** | Language pattern (exceptions / Result / error values / errno); what must not be swallowed; logging convention. |
| 8 | **Comments** | When to comment (why, not what); `ponytail:` marker convention; TODO format (`TODO(name): ...` or language equivalent); what does not need a comment. |

Each section ends with a one-line "what the standardizer checks" note naming the grep/tool the agent runs.

## Verification (foundation)

- `opencode agent list` parses after the standardizer edit; `opencode debug agent standardizer` shows the widened description.
- Frontmatter passes repo rules: `name` kebab-case matching folder, `description` starts with "Use when...", <1024 chars.
- No em-dashes anywhere: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty for the new files.
- `README.md` and `AGENTS.md` both have the new row; names match the folder exactly.
- `SKILL.md` has a `## Commands` section pointing at `commands/standardize-code.md`.
- Token budget: `SKILL.md` <2k tokens.

## Out of scope

- The five `references/<lang>.md` files (SP-1..SP-5).
- Any change to `project-standardization` (it stays focused on repo/docs/process structure; `code-standardization` is its code-focused sibling).
- Per-project code-conventions bootstrap in AGENTS.md (the skill defines the standard; whether a project injects it into its own AGENTS.md is a future, per-project decision).
