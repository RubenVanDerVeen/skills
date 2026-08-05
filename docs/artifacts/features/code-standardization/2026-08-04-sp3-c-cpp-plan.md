# SP-3 C/C++ Plan

## References

- Spec: `docs/artifacts/features/code-standardization/2026-08-04-sp3-c-cpp-design.md`
- Frozen template: `2026-08-04-foundation-design.md` § "Frozen per-language template"

## Branch

Lands on `feat/code-std` after foundation. Additive file.

## Tasks

### SP3-T1: Write `references/c-cpp.md`

Instantiate the frozen 8-section template with the C/C++ picks. Cover both C and C++, flagging divergences inline (e.g. `#pragma once` C++ vs include guards C; exceptions vs return codes). 8 sections in order; each ends with the standardizer-check note.

**Verify**: 8 sections in frozen order; both `.clang-format` and `.clang-tidy` named; CTest + (Unity/GoogleTest) named; C vs C++ divergences flagged inline; no em-dashes.

**Commit**: `feat(skills): add c-cpp code-standardization guide`

### SP3-T2: Verify

- Em-dash scan empty.
- SKILL.md dispatch link `references/c-cpp.md` resolves.
- Arch-tool note consistent with `references/architecture.md` (structural enforcement, include-what-you-use).

**Commit**: none.
