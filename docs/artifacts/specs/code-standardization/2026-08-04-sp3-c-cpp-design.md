# SP-3 C/C++ Design

## Status

Sub-project of the code-standardization multi-plan. Depends on F complete. Consumes the frozen 8-section template.

## Goal

Write `skills/code-standardization/references/c-cpp.md` covering both C and C++ (embedded angle included).

## Language-specific picks

- **Toolchain (§1):** clang-format (format) + clang-tidy (lint). Config `.clang-format` + `.clang-tidy`; pin via the toolchain version (LLVM release). Check `clang-format --dry-run -Werror` and `clang-tidy` via compile_commands.json. Hook: pre-commit framework or `.githooks/`. For C++ additionally consider `cppcheck` for static analysis.
- **Naming (§2):** files `snake_case.c/.cpp`/`snake_case.h/.hpp`; C functions `snake_case`; C++ classes/structs `PascalCase`; methods `camelCase` or `snake_case` per existing codebase (pick one, document); macros `UPPER_SNAKE`; test files `test_*.c` / `*_test.cpp`.
- **Module/file org (§3):** header/source pairs; one primary type or cohesive unit per header; include guards (`#pragma once` preferred for C++, include guards for C); include order (own header → same module → other project → third-party → system) enforced where a tool supports it; `include-what-you-use` discipline.
- **Architecture (§4):** layering via directory structure (`drivers/ → hal/ → app/ → lib/` for embedded); no upward includes; no circular header deps (forward-declare); include-what-you-use and manual review (no single dominant arch tool, boundary enforcement is structural).
- **Documentation (§5):** Doxygen comments (`/** ... */`); document public functions, params, returns, pre/post conditions, invariants.
- **Testing (§6):** CTest as the runner; C: Unity or CMock; C++: GoogleTest or Catch2; tests under `tests/` mirroring source structure; test harness for embedded runs on-host, hardware tests separate.
- **Error handling (§7):** C: return codes (`int`/`enum`) + `errno`, never ignore return values; C++: exceptions only for truly exceptional (embedded often disables RTTI/exceptions, use `std::expected` or return codes); assert for invariant violations.
- **Comments (§8):** explain why; `ponytail:` markers with the known ceiling (ISR timing, memory budget); `TODO(ruben): ...`.

Each section ends with the one-line "what the standardizer checks" note. Note explicitly where C and C++ diverge.

## Out of scope

Any other file. No SKILL.md edit.
