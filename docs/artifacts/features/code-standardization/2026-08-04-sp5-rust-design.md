# SP-5 Rust Design

## Status

Sub-project of the code-standardization multi-plan. Depends on F complete. Consumes the frozen 8-section template.

## Goal

Write `skills/code-standardization/references/rust.md`.

## Language-specific picks

- **Toolchain (§1):** `rustfmt` (format, bundled) + `clippy` (lint, bundled). Config `rustfmt.toml` and `[lints]`/`[workspace.lints]` in `Cargo.toml`; pin via `rust-toolchain.toml`. Add `cargo-deny` for license/advisory gates. Check `cargo fmt --check && cargo clippy -- -D warnings`. Hook: native git hook or pre-commit framework.
- **Naming (§2):** files `snake_case.rs` (or `mod.rs` for module dirs); functions/variables/methods `snake_case`; types/traits/enum variants `PascalCase`; constants `UPPER_SNAKE`; test modules `#[cfg(test)] mod tests` in-file, or `tests/` integration tests.
- **Module/file org (§3):** module-per-file or module-in-file per Rust conventions; `src/lib.rs` + `src/main.rs`; `pub` is the boundary; import grouping (std → external → crate `crate::` → `super::/self::`); keep modules focused.
- **Architecture (§4):** module visibility (`pub`/`pub(crate)`) is the boundary tool; clippy's `mod_module_files` and module rules; no cycles (the compiler rejects); workspace crates for hard boundaries (`cargo-workspaces`).
- **Documentation (§5):** rustdoc (`///` for items, `//!` for modules); document every public item; include examples that are tested by `cargo test` (doc tests).
- **Testing (§6):** `cargo test` (bundled, runs unit + integration + doc tests); unit tests in `#[cfg(test)] mod tests`; integration tests in `tests/`; `assert!`/`assert_eq!`/`pretty_assertions` for readable diffs.
- **Error handling (§7):** `Result<T, E>` with `?` propagation; thiserror for library error enums, anyhow for application code; never `unwrap`/`expect` in production paths (tests and non-fallible inits are fine).
- **Comments (§8):** explain why; `ponytail:` markers; `TODO(ruben): ...`.

Each section ends with the one-line "what the standardizer checks" note.

## Out of scope

Any other file. No SKILL.md edit.
