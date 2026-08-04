# code-standardization Decomposition Outline

## Goal

A new `code-standardization` skill that defines a full, flat (non-tiered) code-structure standard across five languages (Python, TypeScript/JavaScript, C/C++, Go, Rust), plus a widened `standardizer` agent that audits code structure in a merged pass alongside repo structure, plus a `/standardize-code` command.

## Foundation (shared, runs first)

- **What it is:** the skill skeleton, the two cross-language references, the standardizer agent wiring, the command file, and the catalog rows. Critically, the foundation **freezes the per-language guide template** (8 sections) that every language sub-plan consumes.
- **Scope boundaries:**
  - IN: `skills/code-standardization/SKILL.md`, `references/tooling.md`, `references/architecture.md`, edit to `agents/standardizer.md`, `commands/standardize-code.md`, catalog updates (`README.md` skills table, `AGENTS.md` current-skills table), the frozen 8-section template definition.
  - NOT IN: any `references/<lang>.md` (those are the sub-plans).
- **Depended on by:** SP-1 Python, SP-2 TS/JS, SP-3 C/C++, SP-4 Go, SP-5 Rust. All five consume the frozen template.
- **Frozen interface:** the 8-section per-language guide structure defined in `2026-08-04-foundation-design.md` § "Frozen per-language template". Sub-plans instantiate it; they never redefine the section set.

## Sub-projects (run in parallel after foundation)

### SP-1: Python
- **Goal:** `references/python.md` instantiating the frozen template.
- **Why independent:** distinct language, distinct toolchain (ruff), distinct file.
- **Depends on:** F complete (template + skill dir exist).
- **Touches:** `skills/code-standardization/references/python.md` (new file only).
- **Toolchain picks:** Ruff (format + lint + isort-equivalent), `import-linter` for architecture, Google-style docstrings, pytest.

### SP-2: TypeScript/JavaScript
- **Goal:** `references/typescript-javascript.md`.
- **Why independent:** distinct toolchain (Prettier + ESLint/oxlint).
- **Depends on:** F complete.
- **Touches:** `skills/code-standardization/references/typescript-javascript.md` (new file only).
- **Toolchain picks:** Prettier (format), ESLint or oxlint (lint), `dependency-cruiser` for architecture, TSDoc/JSDoc, Vitest/Jest.

### SP-3: C/C++
- **Goal:** `references/c-cpp.md`.
- **Why independent:** distinct toolchain (clang-format + clang-tidy), embedded angle.
- **Depends on:** F complete.
- **Touches:** `skills/code-standardization/references/c-cpp.md` (new file only).
- **Toolchain picks:** clang-format (format), clang-tidy (lint), include-guard discipline, Doxygen comments, Unity/CMock or CTest.

### SP-4: Go
- **Goal:** `references/go.md`.
- **Why independent:** Go opinionates most of this itself.
- **Depends on:** F complete.
- **Touches:** `skills/code-standardization/references/go.md` (new file only).
- **Toolchain picks:** `gofmt`/`goimports` (format, bundled), `golangci-lint` (lint), `go test` (bundled), godoc comments.

### SP-5: Rust
- **Goal:** `references/rust.md`.
- **Why independent:** distinct toolchain (rustfmt + clippy), Result-based error model.
- **Depends on:** F complete.
- **Touches:** `skills/code-standardization/references/rust.md` (new file only).
- **Toolchain picks:** `rustfmt` (format, bundled), `clippy` (lint, bundled), `cargo-deny`/`cargo-workspaces`, rustdoc, `cargo test`.

## Execution order

1. **F** (foundation) on `feat/code-std`.
2. **SP-1 .. SP-5** after F is complete and verified. Independent additive files; no merge conflicts possible. See manifest for the lean branch model.

## Deviation note (lean branch model)

Pure multi-plan-orchestration prescribes per-SP branches + worktrees + an integration merge pass. The five SP outputs are independent *additive* markdown files (one new file each, no shared file touched). Integration risk is zero. This run lands all SPs directly on `feat/code-std` after the foundation, preserving per-SP plans and per-SP Conventional Commits but skipping worktree/integration-merge ceremony. Recorded here so the simplification is explicit, not silent.
