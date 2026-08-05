---
name: code-standardization
description: Use when standardizing or auditing the *structure of source code* itself (not the repo layout): setting up a formatter/linter/hooks for a project, defining per-language naming and module-organization rules, enforcing architecture/dependency boundaries, or reviewing a branch for code-structure violations. Triggers: "standardize the code", "code conventions", "set up ruff/eslint/gofmt", "lint config", "architecture rules", "dependency boundaries", "code style for X". Covers Python, TypeScript/JavaScript, C/C++, Go, Rust. Flat (non-tiered) standard. Pairs with the `standardizer` agent for post-plan code audits.
---

## Overview

Code-structure standard for the source code itself. **Flat**: one standard, all project sizes. Multi-language: Python, TS/JS, C/C++, Go, Rust.

Sister to `project-standardization`: that skill covers repo/docs/process layout (kebab-case paths, AGENTS.md, `docs/artifacts/`, Conventional Commits, ISO dates). This skill covers what lives *inside* `src/`: file naming, module organization, formatting/linting infra, architecture boundaries, language-specific style. Load **both** for a full audit. The `standardizer` agent runs them as one merged pass.

## The 4 agent checks

For every language present in the diff, the agent runs four checks. It never re-implements the tool in its own body; it runs the tool if installed, or emits a quick-fix finding naming the tool and the config file to add.

1. **Presence**: is a formatter, a linter, and a hook wired? Config file exists (`pyproject.toml [tool.ruff]`, `eslint.config.js`, `.golangci.yml`, `[lints]` in `Cargo.toml`, `.clang-format` + `.clang-tidy`).
2. **Documentation**: are the conventions for that language written down agent-visible (this skill's per-language guide, or a project-local override)?
3. **Consistency**: does new code match neighbors? Naming, module layout, error-handling pattern, comment style. Spot-check three files per directory.
4. **Boundaries**: if the project declares architecture layers (in `.agents/architecture.md` or AGENTS.md section), do imports in new code respect the declared direction? Run the arch tool if installed.

If the tool is installed: run it (`<tool> --check` or `command -v <tool> && <tool> ...`). If absent: emit a quick-fix finding naming the tool and the config file to add. **Never re-lint in the agent body.**

## The per-language guides

Each language has a per-language reference with the same eight sections (toolchain, naming, module/file organization, architecture, documentation, testing, error handling, comments). The dispatch table below links to each.

| Language | Reference |
|----------|-----------|
| Python | `references/python.md` |
| TypeScript / JavaScript | `references/typescript-javascript.md` |
| C / C++ | `references/c-cpp.md` |
| Go | `references/go.md` |
| Rust | `references/rust.md` |

## Cross-language references

- `references/tooling.md`: the three-piece kit (formatter / linter / import sorter), config discovery per language, hook wiring patterns (pre-commit framework, husky + lint-staged, native git hooks, project-local `.githooks/`), the "pin it" rule, the "don't re-implement the tool in the agent" rule.
- `references/architecture.md`: layering and canonical dependency direction, no-circular-deps enforcement per language, feature/module isolation, the boundary spec convention (`.agents/architecture.md` or AGENTS.md section), what the agent checks vs. what the tool checks.

## How the standardizer uses this skill

The `standardizer` agent loads **both** `project-standardization` and `code-standardization`, then runs a **merged audit pass** in the same invocation:

1. Repo-structure audit (from `project-standardization`): kebab-case paths, AGENTS.md sections, `docs/artifacts/` layout, catalog rows, Conventional Commits, ISO dates.
2. Code-structure audit (from this skill): for each language in the diff, the 4 agent checks above. Run the pinned formatter/linter in check mode if installed; if absent, emit a quick-fix finding.

Output is the same format: `PASS` or a numbered findings list with `quick-fix:` and `recommendation:` tags. The agent stays read-only; the orchestrator dispatches executors for fixes.

## Commands

Slash command associated with this skill. Source file lives in the top-level `commands/` directory and is inactive until copied to the agent's commands directory.

| Command | Purpose |
|---------|---------|
| `/standardize-code` | Run the 4 agent checks against a path, language, or the current branch diff (`$ARGUMENTS` optional). Reports PASS or numbered findings. |

### Sync pattern

Two-step sync per machine, mirrors `project-standardization`:

1. Copy `skills/code-standardization/` to the agent's skills directory (e.g. `~/.claude/skills/code-standardization/`, `~/.config/opencode/skills/code-standardization/`).
2. Copy `commands/standardize-code.md` to the agent's commands directory:

| Agent | Global | Per-project |
|-------|--------|-------------|
| OpenCode | `~/.config/opencode/command/` | `.opencode/command/` |
| Claude Code | `~/.claude/commands/` | `.claude/commands/` |

The command file is dead weight inside the skills directory until step 2.

## Anti-patterns

- Do not restate what the pinned tool enforces line by line. Reference the tool's rule, link to the config.
- Do not re-lint in the agent. Run `<tool> --check` and report the result.
- Do not invent conventions not in the per-language guide. If the guide is silent, the project picks, and that override goes in `.agents/architecture.md` (or AGENTS.md section), not in the skill.
- Do not duplicate this skill into `.agents/code-standardization.md`. Reference it.
- Do not load large-project `project-standardization` guidance into a single-script repo. Same flat rule applies here: this skill is one standard for all sizes.
