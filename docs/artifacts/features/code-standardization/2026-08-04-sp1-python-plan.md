# SP-1 Python Plan

## References

- Spec: `docs/artifacts/features/code-standardization/2026-08-04-sp1-python-design.md`
- Frozen template: `2026-08-04-foundation-design.md` § "Frozen per-language template"

## Branch

Lands on `feat/code-std` after foundation. Additive file; no SP-specific branch.

## Tasks

### SP1-T1: Write `references/python.md`

Instantiate the frozen 8-section template with the Python picks from the spec. Each of the 8 sections present, in order, no added/removed/reordered sections. Each section ends with the one-line "what the standardizer checks" note.

**Verify**: 8 sections present in the frozen order; config snippet is copy-pasteable; check command matches `ruff format --check . && ruff check .`; no em-dashes.

**Commit**: `feat(skills): add python code-standardization guide`

### SP1-T2: Verify

- Em-dash scan empty on the new file.
- Cross-check against the dispatch table in `SKILL.md`: link target `references/python.md` resolves.
- Cross-check arch-tool name (`import-linter`) matches `references/architecture.md`.

**Commit**: none (verification only).
