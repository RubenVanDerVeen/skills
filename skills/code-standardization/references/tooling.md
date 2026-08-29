# Tooling (cross-language)

The standardization infrastructure layer. Pairs with `references/architecture.md` (boundary layer). Per-language details live in each `references/<lang>.md`.

## The three-piece kit

Every supported language ships with three concerns, each owned by one tool:

- **Formatter**: opinionated, non-negotiable. Config is intentionally small; debate is the enemy.
- **Linter**: configurable rule set. Project enables rules explicitly; silence means "default on" only when the tool's defaults are sane.
- **Import sorter**: often folded into the formatter or linter (Ruff `I` rules for Python, Biome for TS/JS, `goimports` for Go). When a language has no canonical sorter, the formatter normalises a single canonical order.

A project that picks none of the three is a quick-fix finding, not a discussion.

## Config discovery table

The agent reads the config file, not its memory of "what Python usually does". One row per language; the table is the source of truth for "where do I look".

| Language | Formatter config | Linter config | Import sorter |
|----------|------------------|---------------|---------------|
| Python | `pyproject.toml` `[tool.ruff.format]` | `pyproject.toml` `[tool.ruff.lint]` | Ruff `I` rules (folded into `[tool.ruff]`) |
| TypeScript / JavaScript | Prettier (`.prettierrc*`) or Biome (`biome.json`) | `eslint.config.js` (or legacy `.eslintrc.*`) | Biome or `eslint --fix` with `import/order` |
| C / C++ | `.clang-format` | `.clang-tidy` | toolchain convention: own header, then STL, then others; clang-format enforces |
| Go | `gofmt` (zero config) | `.golangci.yml` (drives `golangci-lint`) | `goimports` (folded into `.golangci.yml` via the `gofmt` or `goimports` formatter) |
| Rust | `rustfmt.toml` (or defaults) | `[lints]` in `Cargo.toml` (clippy table) | `rustfmt` (edition-based) |

Each per-language guide lists the exact fields and a copy-pasteable starter. The table above tells the agent which file to open.

## Hook wiring patterns

Four patterns cover every language; pick one per repo, not all four. The agent reports which pattern is wired and whether the wired pattern matches the languages present.

### 1. pre-commit framework (Python-native, multi-language)

- Install: `pip install pre-commit` (or `pipx`).
- Config: `.pre-commit-config.yaml` at the repo root.
- Activate: `pre-commit install`.
- Best for Python projects and polyglot repos where Python tooling is already on the box. Runs any hook as long as it has a CLI entry point.

### 2. husky + lint-staged (JavaScript)

- Install: `npm install --save-dev husky lint-staged`, then `npx husky init`.
- Config: `.husky/pre-commit` shell script plus a `lint-staged` block in `package.json`.
- Best for TS/JS projects. Runs staged files only; fast for large repos.

### 3. Native git hooks (Go, Rust)

- Install: write the hook directly under `.git/hooks/<name>` (or via a project-local pattern, see below).
- Best for single-language repos where the formatter or linter ships as one static binary (`gofmt`, `cargo fmt`). No framework needed; one shell stanza per concern.

### 4. Project-local `.githooks/` (this repo's pattern)

- Layout: `.githooks/<hook-name>` (example: `.githooks/commit-msg` in this repo); activate per clone with `git config core.hooksPath .githooks`.
- Best for monorepos and any repo that wants hooks version-controlled without symlinks or installer steps.
- Trade-off: not automatic on a fresh clone; document the `git config` line in `opencode-install.md` or `AGENTS.md` so new contributors find it.

The code-standardizer checks that one hook layer is wired and that the wired layer runs the pinned tool, not a stale path.

## The "pin it" rule

Formatter and linter versions are pinned, full stop. Pinning lives in the place the language already uses for versions:

- Python: lockfile (`uv.lock`, `poetry.lock`, or `pip-tools requirements.txt`) plus the `rev:` field on each repo in `.pre-commit-config.yaml`.
- TS/JS: `package.json` `devDependencies` with exact versions (no `^` or `~`); pin the package manager itself with the `packageManager` field.
- C/C++: toolchain manifest (Conan, vcpkg, or a CI-pinned image); compilers move, formatters move with them.
- Go: `tool` directive in `go.mod` (Go 1.24+) for tool dependencies, plus the `go` directive and optional `toolchain` directive in `go.mod` to pin the compiler; the legacy alternative is `tools.go` with a `//go:build tools` build tag and `_ "..."` blank imports.
- Rust: `rust-toolchain.toml` for the compiler; `[lints]` in `Cargo.toml` is configuration, not version, so pin the toolchain that ships clippy.

CI and locals must produce byte-identical output. Floating versions are a quick-fix finding.

## The "don't re-implement the tool in the agent" rule

The code-standardizer agent does not re-lint source code in its own body. Its job is to check the tool exists, the tool is pinned, the tool is wired to a hook, and the conventions are documented. Style enforcement is the tool's job.

### Check-mode behavior

When auditing, the agent runs the pinned tool in check mode if it is installed:

```
command -v ruff && ruff check --no-fix .
command -v eslint && eslint .
command -v gofmt && gofmt -l .
command -v cargo && cargo fmt --check
command -v clang-format && clang-format --dry-run --Werror
```

If `command -v` succeeds and the tool exits non-zero, that is a finding with the tool's own error message attached. If `command -v` fails, the agent emits a `quick-fix:` finding naming the tool and the config file to add. It never invents a regex, never rewrites a file by hand, and never "fixes" formatting in chat.

The agent's contribution is the four checks (presence, documentation, consistency, boundaries; see `SKILL.md`). The tool's contribution is enforcement. Keep the boundary.

## Per-language guides

- Python: `references/python.md`
- TypeScript / JavaScript: `references/typescript-javascript.md`
- C / C++: `references/c-cpp.md`
- Go: `references/go.md`
- Rust: `references/rust.md`
