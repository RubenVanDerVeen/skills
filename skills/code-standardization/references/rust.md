# Rust

Per-language guide. Fills the frozen 8-section template from `2026-08-04-foundation-design.md`. Sister files: `references/tooling.md`, `references/architecture.md`.

## Toolchain

Two bundled tools cover the three-piece kit: **`rustfmt`** for formatting and **`clippy`** for lint. Both ship with `rustup`; there is no separate install step. Import sorting is folded into `rustfmt`. Add **`cargo-deny`** for license and advisory gates, separately installed (`cargo install cargo-deny --locked`).

### Pin and configure

Pin the toolchain version in `rust-toolchain.toml` so CI and locals agree. Format config lives in `rustfmt.toml` at the repo root; lint config lives in `[lints]` in `Cargo.toml` (or `[workspace.lints]` for multi-crate workspaces). The blocks below are copy-pasteable.

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.81.0"
components = ["rustfmt", "clippy"]
profile = "minimal"
```

```toml
# rustfmt.toml
edition = "2021"
max_width = 100
tab_spaces = 4
newline_style = "Unix"
use_small_heuristics = "default"
imports_granularity = "Crate"
reorder_imports = true
```

```toml
# Cargo.toml (workspace root or single crate)
[workspace]
members = ["crates/*"]

[workspace.lints.rust]
unsafe_code = "forbid"
unused_must_use = "warn"

[workspace.lints.clippy]
# Lint families enabled; the code-standardizer checks the family list, not the rule ids.
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }
# Selected pedantic groups we do enforce
module_name_repetitions = "warn"
must_use_candidate = "warn"
missing_errors_doc = "warn"
missing_panics_doc = "warn"

# Allow these pedantic lints; tune per project.
allow = [
    "missing_docs_in_private_items",
    "module_name_repetitions",
]
```

In a single-crate repo, replace `[workspace.lints.*]` with `[lints.*]` in that crate's `Cargo.toml`. Project policy lives in `[workspace.lints]`, not per-crate; per-crate additions override, they do not shadow.

### Check command

The exact command CI and the code-standardizer agent run, from the workspace root:

```
cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings
```

`cargo fmt --check` covers formatting; `cargo clippy -- -D warnings` promotes every warning to a deny and fails the build. `--all-targets` covers binaries, libraries, examples, and tests; `--all-features` exercises feature-gated code. One command, two exit codes, no separate sorter step.

For license and advisory gates, add:

```
cargo deny check
```

`cargo-deny` reads `deny.toml` at the repo root and flags banned licenses, duplicate crates, unmaintained advisories, and yanked versions. Pin the `cargo-deny` version next to the toolchain pin in CI.

### Hook wiring

Wire the check command into one of the patterns in `references/tooling.md`. For Rust-only repos the native git hook is the default:

```sh
# .git/hooks/pre-commit (or project-local .githooks/pre-commit)
#!/usr/bin/env sh
set -e
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
```

Make the file executable (`chmod +x`). Polyglot repos in this monorepo use the project-local `.githooks/` pattern already wired for `commit-msg`; add a `pre-commit` stanza that runs the two `cargo` lines. The `pre-commit` framework is acceptable too; the config is longer but the result is the same.

### What rustfmt and clippy do not enforce

`rustfmt` and `clippy` cover formatting, style, common bugs, modernization, and a wide rule set. The code-standardizer, not the linter, owns the items below; if the project skips these, neither tool will catch it:

- **Cyclomatic complexity**: clippy has `cognitive_complexity` (warn-by-default via `clippy::pedantic`); projects that want a hard ceiling configure `#[cognitive_complexity = "N"]` per function or accept the warning. There is no project-wide knob; the code-standardizer samples instead.
- **Doc-test coverage of all examples**: clippy enforces `missing_docs_in_private_items` and `missing_errors_doc` (when enabled), but does not require every public function to carry a runnable example. Whether the example exists is a documentation-policy check, not a lint finding.
- **Architecture boundaries**: clippy cannot express layer rules or no-cycle contracts beyond visibility. Use `cargo-deny` plus workspace crates for hard boundaries (see Architecture below).
- **Dependency-policy enforcement**: `cargo-deny` covers license and advisory; semantic-version policy (e.g. forbid `^0.x` for production crates) is a separate `cargo-deny` configuration block.

code-standardizer check: `cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings` exits zero; `rust-toolchain.toml` exists with a pinned `channel`; `Cargo.toml` has `[workspace.lints]` (multi-crate) or `[lints]` (single-crate) with `clippy` rules selected; `rustfmt.toml` exists at the repo root.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Files (modules) | `snake_case.rs` or `mod.rs` for module dirs | `user_service.rs`, `user_service/mod.rs` |
| Test files | in-file `#[cfg(test)] mod tests` or `tests/*.rs` integration | `src/user_service.rs` (inline `mod tests`), `tests/test_user_service.rs` |
| Crate / workspace names | `kebab-case` (Cargo rewrites to `snake_case` in `use`) | `my-cool-crate` -> `use my_cool_crate::...` |
| Functions / variables / methods | `snake_case` | `fn fetch_user(user_id: u64)` |
| Types / traits / enum variants | `PascalCase` | `struct UserService`, `trait Repository`, `AuthError::Token` |
| Module-level constants | `UPPER_SNAKE` | `const MAX_RETRIES: u32 = 3;` |
| Statics | `UPPER_SNAKE` | `static CACHE: Lazy<...> = ...;` |
| Type parameters | `PascalCase`, short, single letter when obvious | `T`, `E`, `Item` |
| Lifetimes | short lowercase, usually `'a`, `'b` | `&'a str` |
| Private symbols | no prefix (unlike Python), use `pub(crate)` to narrow scope | `fn internal_helper()` |
| Boolean predicates | `is_`, `has_`, `can_` prefix | `fn is_active(&self) -> bool` |
| Conversions | `as_` (cheap ref), `to_` (expensive owned), `into_` (consuming) | `fn as_str(&self) -> &str`, `fn into_owned(self) -> String` |

Avoid single-letter names outside generic parameters and tight closures. Avoid `l`, `O`, `I` as identifiers; they read as digits in some fonts.

code-standardizer check: `grep -rEn "^pub (fn|struct|enum|trait) [a-z_]+\b" --include="*.rs" .` returns empty; `grep -rEn "^fn [A-Z][a-zA-Z0-9_]+\b" --include="*.rs" .` returns empty for non-test files; crate name in `Cargo.toml` matches a kebab-case folder name.

## Module / file organization

### Layout

- **Library crate**: `src/lib.rs` exposes the public surface via `pub use` re-exports. Module files sit next to `lib.rs` (`src/user_service.rs`) or in a directory with a `mod.rs` (`src/user_service/mod.rs`) for sub-modules.
- **Binary crate**: `src/main.rs` is the thin entry point. Logic lives in `src/lib.rs` or a workspace library crate; the binary pulls from it.
- **Workspace**: `Cargo.toml` at the root declares `members = ["crates/*"]` (or an explicit list). Each member has its own `Cargo.toml`, `src/`, and tests.
- **Integration tests**: top-level `tests/*.rs`. Each file is its own crate, sees only the public `lib.rs` surface.
- **Examples**: `examples/*.rs`. Public-API usage demos double as smoke tests (`cargo test --examples`).
- **Benchmarks**: `benches/*.rs`. Nightly-only `#[bench]` or the stable `criterion` crate.

### One module, one responsibility

One module owns one cohesive unit. `user_service.rs` exports `UserService`, `fetch_user`, `save_user`; it does not export `UserService`, `Invoice`, `parse_csv`. Splitting forces a module directory with sub-files.

### Import order

Three blocks, separated by blank lines, enforced by `rustfmt` with `imports_granularity = "Crate"` and `reorder_imports = true`:

1. `extern crate` and `std` (`std::fs`, `std::path::Path`).
2. External crates (`serde::Deserialize`, `tokio::spawn`).
3. Crate-internal (`crate::config::Settings`, `super::helpers`, `self::sub_module`).

`use` statements group within a block; multiple items per `use` when the path prefix matches (`use std::{fs, path::Path};`). No glob imports (`use x::*;`) outside test modules and preludes; `pub use` re-exports are fine.

### File-length and complexity ceilings

- **File length**: ~400 lines is the ceiling for non-generated source. Above that, the module has more than one responsibility and should be split into a directory with sub-modules.
- **Cyclomatic complexity**: no project-wide clippy knob. Sample high-complexity functions manually or enable `clippy::cognitive_complexity` and accept the warnings. Functions over the threshold are a quick-fix finding naming the function and the path.
- **Function length**: target under ~80 lines; clippy's `too_many_arguments` and `too_many_lines` cover the extremes.

code-standardizer check: `rustfmt` `imports_granularity = "Crate"` is set; `wc -l` per `src/**/*.rs` file under 400 (one exception per repo for legitimate generated code); `cargo clippy --all-targets --all-features -- -D warnings` reports zero findings on import and module rules.

## Architecture

`rustc` enforces module boundaries and visibility mechanically; clippy flags awkward module layout. For hard boundaries across a workspace, declare a workspace and split features into separate crates. The pattern matches the canonical direction from `references/architecture.md`:

```
api (binary / presentation)  ->  service / domain  ->  data / infra
```

Domain imports nothing above it. Infrastructure depends inward on domain port traits only.

### Module visibility is the boundary tool

Rust has four effective visibility levels:

| Visibility | Meaning |
|-----------|---------|
| (none) | private to the defining module |
| `pub(crate)` | visible anywhere in the same crate |
| `pub(super)` | visible to the parent module |
| `pub` | visible to anyone who depends on the crate |

Reach for `pub(crate)` first when a helper crosses module boundaries inside the crate; reach for `pub` only on the documented public surface. Clippy's `redundant_pub_crate` and `module_name_repetitions` lints flag over-exposed helpers.

### Clippy module rules

Enable the module-organization family under `[workspace.lints.clippy]`:

```toml
mod_module_files = "warn"
self_named_module_files = "warn"
```

`mod_module_files` warns when a `mod foo;` declaration has no matching `foo.rs` or `foo/mod.rs`. The compiler refuses a cycle inside the module tree by construction; there is no separate cycle tool to wire.

### Workspace crates for hard boundaries

When a feature must not reach into another's internals, give it its own crate in the workspace:

```
crates/
  api/        # binary or lib; depends on service
  service/    # lib; depends on domain
  domain/     # lib; pure logic, depends on nothing project-local
  data/       # lib; depends on domain ports, implements them
```

`cargo` enforces the dependency direction at the package graph level: `data` cannot import from `service` unless `service` is added to `data`'s `[dependencies]`, and that decision is visible in `Cargo.toml`. For multi-package scaffolding, **`cargo-workspaces`** is the standard CLI extension (`cargo workspaces init`, `cargo workspaces rename`). Pin it as a dev tool next to `cargo-deny`.

### Boundary spec

For medium-or-larger Rust projects, declare the actual layer names and feature list in `.agents/architecture.md` (or the `## Architecture` section of `AGENTS.md`). The boundary spec is the source of truth for "what is the layer called here"; the workspace member list and `[workspace.lints]` enforce the direction.

code-standardizer check: `[workspace]` exists for multi-crate repos; `cargo clippy --all-targets -- -D warnings` reports zero `mod_module_files` findings; `.agents/architecture.md` or `AGENTS.md` `## Architecture` section exists for medium+ projects; no crate under `crates/` declares a reverse-direction dependency in its `[dependencies]` table.

## Documentation

**rustdoc** with `///` for items and `//!` for modules. Document every public item: `pub fn`, `pub struct`, `pub enum`, `pub trait`, `pub type`, `pub const`, `pub static`, plus every `pub` field and every variant on a `pub enum`. `pub(crate)` items do not need rustdoc; private items do not need rustdoc.

Shape:

```rust
/// Load a user by id.
///
/// # Arguments
///
/// `user_id` is the primary key.
///
/// # Returns
///
/// The matching [`User`], or `None` if no row matches.
///
/// # Errors
///
/// Returns [`AuthError::InvalidToken`] when the caller's session is invalid.
///
/// # Examples
///
/// ```
/// use mycrate::user_service::fetch_user;
///
/// let user = fetch_user(1)?;
/// assert_eq!(user.name, "alice");
/// # Ok::<(), mycrate::AuthError>(())
/// ```
pub fn fetch_user(user_id: u64) -> Result<Option<User>, AuthError> {
    // ...
}
```

Examples in `///` blocks are **doc tests**: `cargo test` runs them as part of the test suite. Use doc tests for every non-trivial public function; they double as living examples and as executable assertions of the public surface. Cover the success path and at least one error path per fallible function. The `# Errors` section is mandatory for any `-> Result<_, _>` signature when `missing_errors_doc` is enabled.

Private doc-comments are allowed but optional. When present, keep them to one line describing intent; save the long form for public surfaces.

code-standardizer check: `grep -rEn "^pub (fn|struct|enum|trait|fn|const|static)" --include="*.rs" -A 5 .` finds a `///` doc-comment above each public item; `cargo test --doc` exits zero; `missing_errors_doc` is enabled in `[workspace.lints.clippy]`; `missing_docs_in_private_items` is `allow` unless the project opts in.

## Testing

**`cargo test`** runs the whole suite: unit tests, integration tests, doc tests, and examples. There is no separate test runner; the framework is bundled.

- **Unit tests**: in-file `#[cfg(test)] mod tests { ... }` at the bottom of the source file. Sees private items. One module per file is the convention; one behavior per test.
- **Integration tests**: top-level `tests/*.rs`. Each file is its own crate, sees only the public `lib.rs` surface; this is the test that catches accidental over-exposure of internals.
- **Doc tests**: `///` examples inside `cargo test --doc`. Coverage of the public surface comes essentially for free if every public function has an example.
- **Assertions**: `assert!`, `assert_eq!`, `assert_ne!`. For readable diffs on struct equality, add `pretty_assertions` as a dev dependency and call `use pretty_assertions::assert_eq;` inside each test module; the macro shadows the std one.
- **Structure**: arrange-act-assert, one behavior per test. Parametrize over edge cases with `rstest` or hand-rolled table-driven tests instead of copy-pasting test bodies.
- **Coverage**: behavior-level (public API) and error-path coverage are mandatory. Internal helpers are tested through the public API when they have no independent surface; coverage tooling is `cargo-llvm-cov` or `grcov`.

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn fetch_user_returns_expected_name() {
        let user = fetch_user(1).unwrap();
        assert_eq!(user.name, "alice");
    }

    #[test]
    fn fetch_user_errors_on_invalid_token() {
        let err = fetch_user(1).unwrap_err();
        assert!(matches!(err, AuthError::InvalidToken));
    }
}
```

code-standardizer check: `cargo test --all-features` exits zero; `tests/*.rs` integration files exist for multi-module crates; `#[cfg(test)] mod tests` is present in non-trivial source files; `pretty_assertions` is in `[dev-dependencies]` when struct comparison is asserted.

## Error handling

Rust uses **`Result<T, E>`** for fallible operations and `panic!` for unrecoverable states. The rules below are what `clippy` does not enforce on its own.

- **Never `unwrap` or `expect` in production paths**. `unwrap` and `expect` are fine in tests, in `const` evaluators, and in single-shot startup where a failure means "kill the process". Anywhere else, propagate with `?` or handle the error explicitly.
- **Library code defines a typed error enum**. Use **`thiserror`** to derive `std::error::Error`, `Display`, and `From` conversions for the enum's variants. The public error type is part of the public API.
- **Application code uses `anyhow`**. Binaries and glue code use `anyhow::Result<T>` for ergonomic `?` propagation across heterogeneous crates; libraries do not depend on `anyhow`.
- **Never silently swallow**. A bare `let _ = fallible();` or `if let Err(_) = ...` is a quick-fix finding. Either log with context (`tracing::error!`) or re-raise. Use `tracing` (or `log` + `env_logger`) for diagnostics, configured once at the application entry point.
- **Conversion boundaries**: implement `From` for cross-domain errors so `?` works without an explicit `.map_err(...)` at every callsite. The conversion is a single point of policy; do not duplicate it inline.
- **Panics**: reserve for programmer error (index out of bounds, violated invariant). Document with `# Panics` in the rustdoc when a function can panic; enable `clippy::missing_panics_doc`.

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AuthError {
    #[error("invalid token")]
    InvalidToken,
    #[error("user {0} not found")]
    UserNotFound(u64),
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}

pub fn fetch_user(user_id: u64) -> Result<User, AuthError> {
    let row = sqlx::query!("SELECT * FROM users WHERE id = ?", user_id)
        .fetch_one(&pool)
        .map_err(AuthError::from)?;
    Ok(User::from_row(row)?)
}
```

code-standardizer check: `grep -rEn "\.unwrap\(\)|\.expect\(" --include="*.rs" . | grep -vE "/tests/|mod tests|examples/"` returns empty for production paths; `[dependencies]` includes `thiserror` for library crates and `anyhow` for binaries; `cargo clippy --all-targets -- -D warnings` reports zero `unwrap_used` or `expect_used` findings when the corresponding `restriction` lints are enabled.

## Comments

- **Explain why, not what**. Code says what; comments say why. A comment that restates the next line is dead prose.
- **`ponytail:` markers for deliberate shortcuts**. When the implementation takes a known-shorter path with a documented ceiling (global lock, O(n^2) scan, naive heuristic), add a one-line comment naming the shortcut and the upgrade path: `// ponytail: global lock, per-account locks when throughput matters`.
- **TODO format**: `TODO(ruben): retire shim, see docs/artifacts/plans/...`. Owner in parentheses, colon, brief description. TODOs without an owner are anonymous debt; the code-standardizer flags them. Reference an issue or plan id when one exists.
- **What does not need a comment**: obvious type signatures (no `// user_id: u64` next to `user_id: u64`); rustdoc already covers the function (no `// fetch the user` above the doc-comment); standard-library calls (no `// open the file` above `File::open(path)`).
- **Commented-out code is forbidden**. Delete it; git remembers. `#[allow(dead_code)]` on commented-out logic is debt; remove the code, remove the allow.
- **Doc-comments vs. line comments**: `///` and `//!` are rustdoc, rendered to HTML and tested as doc tests. `//` is a plain comment. Use `///` for public API, `//!` at the top of modules to describe the module, plain `//` for inline reasoning.

code-standardizer check: `grep -rEn "^\s*//" --include="*.rs" . | grep -vE "ponytail:|TODO\([a-zA-Z0-9_-]+\):"` returns zero findings on new files (plain comments other than `ponytail:` and `TODO(owner):` need justification); `grep -rEn "TODO[^(]" --include="*.rs" .` (anonymous TODOs without an owner) returns empty; no `// xxx` commented-out code blocks larger than one line remain in source.
