# SP-5 Rust Plan

## References

- Spec: `docs/artifacts/features/code-standardization/2026-08-04-sp5-rust-design.md`
- Frozen template: `2026-08-04-foundation-design.md` § "Frozen per-language template"

## Branch

Lands on `feat/code-std` after foundation. Additive file.

## Tasks

### SP5-T1: Write `references/rust.md`

Instantiate the frozen 8-section template with the Rust picks. 8 sections in order; each ends with the standardizer-check note. Emphasize the Result/error model and doc tests (Rust's differentiators).

**Verify**: 8 sections in frozen order; check command `cargo fmt --check && cargo clippy -- -D warnings`; doc-test convention present; no em-dashes.

**Commit**: `feat(skills): add rust code-standardization guide`

### SP5-T2: Verify

- Em-dash scan empty.
- SKILL.md dispatch link `references/rust.md` resolves.
- Arch note consistent with `references/architecture.md` (compiler-enforced no-cycles, visibility/workspace boundaries).

**Commit**: none.
