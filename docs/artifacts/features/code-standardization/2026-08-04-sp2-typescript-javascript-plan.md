# SP-2 TypeScript/JavaScript Plan

## References

- Spec: `docs/artifacts/specs/code-standardization/2026-08-04-sp2-typescript-javascript-design.md`
- Frozen template: `2026-08-04-foundation-design.md` § "Frozen per-language template"

## Branch

Lands on `feat/code-std` after foundation. Additive file.

## Tasks

### SP2-T1: Write `references/typescript-javascript.md`

Instantiate the frozen 8-section template with the TS/JS picks. 8 sections in order; each ends with the standardizer-check note.

**Verify**: 8 sections in frozen order; check command `prettier --check . && eslint .`; arch tool `dependency-cruiser`; no em-dashes.

**Commit**: `feat(skills): add typescript-javascript code-standardization guide`

### SP2-T2: Verify

- Em-dash scan empty.
- SKILL.md dispatch link `references/typescript-javascript.md` resolves.
- Arch-tool name matches `references/architecture.md`.

**Commit**: none.
