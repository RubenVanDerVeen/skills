# C / C++

Per-language guide. Fills the frozen 8-section template from `2026-08-04-foundation-design.md`. Covers both C and C++, with the embedded angle included. Sister files: `references/tooling.md`, `references/architecture.md`.

Where C and C++ diverge (header guards, error style, naming conventions, doc comment conventions), the divergence is flagged inline within the relevant section, not as a new section.

## Toolchain

The C/C++ toolchain has two primary tools plus an optional static analyser. **clang-format** owns formatting, **clang-tidy** owns linting, and for C++ **cppcheck** is the optional second-pass static analyser. There is no single dominant import sorter; include order is a code-style discipline, enforced by clang-format's `SortIncludes` plus `IncludeBlocks: Regroup`.

### Pin and configure

Pin clang-format and clang-tidy via the LLVM release the project uses (the `clang-format --version` output names the LLVM release). Format config lives in `.clang-format` at the repo root; lint config in `.clang-tidy`. Both files are copy-pasteable.

```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
TabWidth: 4
UseTab: Never
ColumnLimit: 100
BreakBeforeBraces: Attach
AllowShortFunctionsOnASingleLine: Empty
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
PointerAlignment: Right
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^"(llvm|llvm-c|clang|clang-c)/'
    Priority: 4
  - Regex: '^<[^>]+>'
    Priority: 3
  - Regex: '^"[^/]+\.h(pp)?"'
    Priority: 2
  - Regex: '^"'
    Priority: 1
SortIncludes: true
```

```yaml
# .clang-tidy
Checks: '-*,bugprone-*,cert-*,clang-analyzer-*,concurrency-*,cppcoreguidelines-*,misc-*,modernize-*,performance-*,portability-*,readability-*'
WarningsAsErrors: '*'
HeaderFilterRegex: '.*'
```

For embedded C/C++ projects that cannot afford a clang-tidy pass on every commit, **cppcheck** is the lighter static-analysis fallback:

```
cppcheck --enable=warning,style,performance,portability --inline-suppr --quiet src/
```

### Check command

CI and the code-standardizer agent run the same checks:

```
clang-format --dry-run --Werror $(git ls-files '*.c' '*.cpp' '*.h' '*.hpp')
clang-tidy --quiet -p build/compile_commands.json $(git ls-files '*.cpp' '*.hpp')
```

For C-only projects, drop the `.cpp`/`.hpp` globs from the clang-tidy line. clang-tidy reads `compile_commands.json`; generate it once per build (`cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` for CMake, or invoke the project's build system with the equivalent flag). Without `compile_commands.json` clang-tidy reports false positives, so presence of the file is itself a code-standardizer check.

### Hook wiring

Wire into one of the patterns in `references/tooling.md`. C/C++ projects in this monorepo use the project-local `.githooks/` pattern:

```sh
# .githooks/pre-commit
#!/usr/bin/env bash
set -e
clang-format --dry-run --Werror $(git ls-files '*.c' '*.cpp' '*.h' '*.hpp')
clang-tidy --quiet -p build/compile_commands.json $(git ls-files '*.cpp' '*.hpp')
```

Activate with `git config core.hooksPath .githooks`. For polyglot repos the pre-commit framework is the alternative, with `clang-format` invoked via the `pre-commit-hooks` mirror.

### C vs C++ note

clang-format handles both languages from one config. clang-tidy applies cleanly to C++ and to modern C (C99+); for older C (C89/90) some checks (modernize-*, cppcoreguidelines-*) emit false positives and should be disabled in `.clang-tidy` with `Checks: '-*,<family>-*'` overrides.

code-standardizer check: `command -v clang-format && clang-format --dry-run --Werror <files>` exits zero; `.clang-format` and `.clang-tidy` exist at repo root; `compile_commands.json` present when CMake is the build system; `clang-format --version` and `clang-tidy --version` match the pinned LLVM release.

## Naming

C and C++ diverge here: C has no classes and no implicit privacy, while C++ projects often mix free functions, classes, namespaces, and templates. The table below covers both with side-by-side conventions.

| Element | C convention | C++ convention | Example (C) | Example (C++) |
|---------|--------------|----------------|-------------|---------------|
| Files | `snake_case.c`, `snake_case.h` | `snake_case.cpp`, `snake_case.hpp` | `user_service.c` | `user_service.cpp` |
| Test files | `test_*.c` | `*_test.cpp` | `test_user_service.c` | `user_service_test.cpp` |
| Functions / methods | `snake_case` | `snake_case` (C-style code) or `camelCase` (OOP code); pick one per codebase | `fetch_user()` | `fetchUser()` |
| Classes / structs | n/a | `PascalCase` | n/a | `class UserService` |
| Structs (POD in C) | `snake_case_t` (suffixed `_t`) | `PascalCase` (no `_t` suffix; reserved by POSIX) | `user_record_t` | `struct UserRecord` |
| Constants (`#define`) | `UPPER_SNAKE` | `UPPER_SNAKE` | `#define MAX_RETRIES 3` | `#define MAX_RETRIES 3` |
| Constants (`const` / `constexpr`) | `UPPER_SNAKE` | `kCamelCase` (Google style) or `UPPER_SNAKE` | `static const int MAX_RETRIES = 3` | `static constexpr int kMaxRetries = 3` |
| Enums | tag `snake_case_t`, values `UPPER_SNAKE` | type `PascalCase`, values `kCamelCase` or `UPPER_SNAKE` | `enum status_t { STATUS_OK }` | `enum class Status { kOk }` |
| Namespaces | n/a | `snake_case` | n/a | `namespace user_service` |
| Macros | `UPPER_SNAKE` | `UPPER_SNAKE` | `#define MAX_RETRIES 3` | `#define MAX_RETRIES 3` |
| Private members | leading underscore on `static` only | trailing underscore `_` | `static int _cache` | `int cache_;` |
| Boolean predicates | `is_`, `has_`, `can_` prefix | `Is`, `Has`, `Can` (Google) or `is_`, `has_` (LLVM) | `is_active` | `IsActive()` |

**Pick a methods-naming convention once and document it in the codebase's `AGENTS.md`** (or a `## Conventions` block). The mixed style (`snake_case` for free functions, `camelCase` for class methods) is the most common modern C++ choice; the unified style (`snake_case` for both) is the safer pick for C-with-classes code. Either is fine; flipping later is the costly option.

In C, avoid leading-underscore identifiers in the global namespace: the C standard reserves identifiers starting with `_` followed by an uppercase letter or another underscore for the implementation, and POSIX reserves many more. Use trailing underscores on `static` module-private variables, not leading underscores.

Avoid `l`, `I`, `O` as identifiers; they read as digits in some fonts.

code-standardizer check: `grep -rEn "^(class|struct) [a-z_]+[ {]" --include="*.cpp" --include="*.hpp" .` returns empty (classes and structs are PascalCase); `grep -rEn "^(static )?[a-zA-Z_]+ [A-Z][A-Z_]+\(" --include="*.c" --include="*.cpp" .` returns empty (functions are snake_case or camelCase, not UPPER_SNAKE); the chosen methods convention is documented in `AGENTS.md`.

## Module / file organization

### Header / source pairs

Every public symbol declared in a header (`*.h` for C, `*.hpp` for C++) has its definition in a matching source file. Headers are the contract; sources are the implementation. Inline functions stay in the header.

### One primary type per header

Each header exposes one primary type or one cohesive group of free functions. A `user_service.h` declaring `UserService`, `fetch_user`, and `save_user` is one cohesive unit. A `user_service.h` declaring `UserService`, `Invoice`, and `parse_csv` is three units; split it.

### Include guards: C vs C++

- **C**: use traditional include guards (`#ifndef USER_SERVICE_H` / `#define USER_SERVICE_H` / `#endif`). `#pragma once` is widely supported but not in the C standard; some embedded toolchains reject it. Stick to include guards in C for portability.
- **C++**: use `#pragma once`. The C++ standard does not formally include it either, but every compiler in active use supports it (GCC, Clang, MSVC, ICC), and the brevity wins. If the project must support a niche compiler, fall back to include guards.

### Include order

Five blocks, separated by blank lines, enforced by clang-format's `IncludeBlocks: Regroup` plus the `IncludeCategories` table:

1. The matching header for this source file (`#include "user_service.h"`).
2. Same module headers (sibling headers in the same folder).
3. Other project headers (`#include "hal/gpio.h"`).
4. Third-party library headers (`#include <spdlog/spdlog.h>`).
5. Standard library / system headers (`#include <vector>`).

clang-format sorts each block alphabetically and inserts blank lines between blocks. Forward-declare in headers wherever possible, include in sources.

### File-length and complexity ceilings

- **File length**: ~400 lines is the ceiling. Above that, the unit has more than one responsibility and should be split.
- **Cyclomatic complexity**: clang-tidy `readability-function-cognitive-complexity` and `bugprone-branch-clone` flag overly complex functions. A cognitive-complexity threshold above 30 is the cutoff; projects with stricter taste lower it to 20.

code-standardizer check: `wc -l <file>` stays at or under 400 lines per file on new files; clang-format exits zero on `--dry-run --Werror`; `find . -name '*.h' -o -name '*.hpp' | wc -l` paired with a count of source files shows a header-to-source ratio close to 1; clang-tidy `readability-function-cognitive-complexity` reports zero findings on new files.

## Architecture

There is no single dominant arch tool for C/C++. Boundary enforcement is structural: directory layout, include discipline, forward declarations, and `include-what-you-use` (IWYU). The agent reviews; the structure prevents.

### Layering for embedded and application code

For embedded projects, the canonical layering is:

```
drivers/  ->  hal/  ->  app/  ->  lib/
```

Drivers know hardware. HAL wraps drivers behind a portable interface. App code uses HAL. `lib/` holds reusable, hardware-independent components (data structures, parsers, math helpers) and is the only layer every other layer may import from. The rule mirrors `references/architecture.md` adapted to embedded: domain (`lib/`) imports nothing from above it; infrastructure (`drivers/`, `hal/`) depends inward on domain ports.

For application (non-embedded) C++, the canonical layering from `references/architecture.md` applies:

```
api / presentation  ->  service / domain  ->  data / infra
```

### No circular header dependencies

Forward-declare in headers, include in sources. A header that includes another header to use a pointer or reference to its type is creating a coupling that does not need to exist. The structural rule:

- If header A needs only a pointer or reference to type T declared in header B, A forward-declares `struct T` (or `class T`) and does not include B.
- If header A needs the full definition of T (member access, `sizeof`, value parameter), A includes B.
- A header cycle (A includes B includes A) is a cycle; break it with forward declarations.

`include-what-you-use` (IWYU) enforces include discipline mechanically: it flags headers that leak private types and includes that pull in more than the source file actually uses. The agent audits IWYU output; IWYU does the mechanical work.

### Boundary spec

For medium-or-larger C/C++ projects, declare the actual layer names and the IWYU mapping in `.agents/architecture.md` (or a `## Architecture` section in `AGENTS.md`). The boundary spec names the layers, the allowed dependency direction, and which folder maps to which layer. IWYU's mapping file flags violations mechanically; the agent audits that the spec is current and that new files respect it.

code-standardizer check: `.agents/architecture.md` or `AGENTS.md` `## Architecture` section exists for medium+ projects; `command -v include-what-you-use && iwyu_tool -p build/compile_commands.json` exits zero; no upward includes in new files (`grep -rEn '#include "' --include='*.h' --include='*.hpp' new_files/` shows only forward-friendly includes).

## Documentation

**Doxygen comments** (`/** ... */`) on every public function, class, struct, enum, and macro. Document parameters, return values, preconditions, postconditions, invariants, and ownership semantics (who allocates, who frees, who locks).

Shape (C):

```c
/**
 * Fetch a user record by id.
 *
 * @param user_id     Primary key of the user to load.
 * @param out_user    Output buffer; must be non-null, caller-owned.
 * @return 0 on success, -EINVAL if user_id is out of range, -ENOENT if no row matches.
 *
 * @pre    out_user != NULL
 * @post   On success, *out_user holds the loaded record.
 */
int fetch_user(int user_id, struct user_record_t *out_user);
```

Shape (C++):

```cpp
/**
 * Load a user by id.
 *
 * @param user_id          Primary key of the user to load.
 * @param include_deleted  When true, include soft-deleted rows.
 * @return The matching User, or std::nullopt if no row matches.
 *
 * @throws AuthError      If the caller's session token is invalid.
 */
std::optional<User> fetchUser(int user_id, bool include_deleted = false);
```

For C++ projects with richer APIs, Javadoc-style tags (`@param`, `@return`, `@throws`, `@pre`, `@post`) are the most common convention; Qt-style (`\\a`, `\\b`) and `@brief` are also valid. Pick one per project and use it consistently.

Private functions may omit Doxygen blocks; when present, keep them to one line describing intent. Macros (`#define MAX_RETRIES 3`) get a one-line comment above the definition naming the contract.

code-standardizer check: `command -v doxygen && doxygen Doxyfile` runs with `WARNINGS = NO`; `grep -rEn "^(int|void|static [a-z]+|[A-Z][a-zA-Z]+) [a-z_]+\(" --include="*.h" --include="*.hpp" -A 1 .` shows a `/**` block above each public function declaration in new headers.

## Testing

**CTest** is the runner for both C and C++. CMake's built-in test driver, hooked to `add_test()` from `CTestTestfile.cmake`, gives CI a single `ctest` invocation that finds and runs every registered test.

- **C**: **Unity** (ThrowTheSwitch) for the harness, with **CMock** for mocking when needed. Unity is the de facto standard for embedded C testing because it runs on-host without an OS.
- **C++**: **GoogleTest** or **Catch2**. GoogleTest is the more common pick for application C++; Catch2 reads better for BDD-style tests.

### Layout

- Tests under `tests/` mirroring the source tree. `tests/test_user_service.c` for `src/user_service.c`; `tests/user_service_test.cpp` for `src/user_service.cpp`.
- One test file per source unit. Multiple `TEST(...)` / `TEST_F(...)` blocks per file are fine.
- Embedded hardware tests live under `tests/hardware/` and are excluded from the on-host CTest run via a CMake label (`add_test(NAME ... LABELS "hardware")`); CI runs them on the target, not on the build host.

### Structure

Arrange-act-assert (or given-when-then for BDD). One behavior per test. Parametrize over edge cases:

```cpp
#include <gtest/gtest.h>
#include "user_service.h"

TEST(UserServiceTest, FetchUserReturnsExpectedName) {
    // arrange
    auto service = UserService::forTesting();
    // act
    auto user = service.fetchUser(42);
    // assert
    ASSERT_TRUE(user.has_value());
    EXPECT_EQ(user->name(), "alice");
}
```

Coverage targets: every public function has at least one happy-path test and one error-path test. Internal helpers are tested through the public API unless they are independently exposed (HAL primitives, math helpers, parsers).

code-standardizer check: `command -v ctest && ctest --output-on-failure` exits zero; `tests/test_*.c` and `tests/*_test.cpp` mirror `src/*.c` / `src/*.cpp` paths; CMakeLists.txt registers every test via `add_test()`; `ctest -N` lists tests matching the count of public functions in `src/`.

## Error handling

C and C++ diverge sharply here. The rule of thumb: **never ignore a return value that carries an error**.

### C: return codes and `errno`

C has no exceptions. Errors propagate as return values, with `errno` carrying the detail.

- **Return type**: `int` (zero on success, negative errno on failure) or a project-specific `enum result_t`. `void` is allowed only when the function truly cannot fail.
- **`errno`**: set on failure only; never set on success. Standard library functions set `errno`; project functions may set `errno` for cross-translation-unit consistency, but the primary signal is the return code.
- **Never ignore a return value**. A bare `some_call();` where `some_call()` returns `int` is a clang-tidy `bugprone-unused-return-value` finding. Either check the return, or assign to `[[maybe_unused]] int rc = ...` with an explanatory comment.

```c
int rc = fetch_user(42, &out_user);
if (rc != 0) {
    fprintf(stderr, "fetch_user failed: %s\n", strerror(-rc));
    return rc;
}
```

### C++: exceptions, `std::expected`, or return codes

Three options, in order of preference for modern C++:

1. **Exceptions** for truly exceptional paths (network down during startup, corrupt configuration file). Reserve them for situations where the caller has no reasonable local recovery.
2. **`std::expected<T, E>`** (C++23) for expected failure modes (parse error, lookup miss). Caller inspects the error before continuing; no exception cost on the hot path.
3. **Return codes** for embedded projects that disable exceptions (`-fno-exceptions`) or where the binary size of exceptions is unacceptable.

Embedded C++ often runs with `-fno-exceptions -fno-rtti`. In that mode, `std::expected` is unavailable (C++23 is rare on embedded toolchains); use return codes plus a project-specific error type.

### `assert` for invariants

Use `assert` (from `<cassert>` / `<assert.h>`) for invariants that must hold in correct code: preconditions, postconditions, loop invariants. `assert` is compiled out under `-DNDEBUG`; do not put side effects inside it.

### Logging

Application C/C++ uses `fprintf(stderr, ...)` or a third-party logger (spdlog, Quill). Embedded targets use the project-specific logger or write to a UART ring buffer via the HAL. Production code never calls `printf` for diagnostics on embedded targets (buffer overruns, blocking I/O).

code-standardizer check: `grep -rEn "^\s*[a-z_][a-z_0-9]*\([^)]*\)\s*;" --include="*.c" --include="*.cpp" .` returns empty for functions with non-void return types (catches discarded return values); C++ builds with `-Werror -Wall -Wextra`; no `catch (...) { }` blocks (silent swallow); `assert` appears in non-trivial functions for documented invariants.

## Comments

- **Explain why, not what**. Code says what; comments say why. A comment that restates the next line is dead prose.
- **`ponytail:` markers for deliberate shortcuts**. When the implementation takes a known-shorter path with a documented ceiling, add a one-line comment naming the shortcut and the upgrade path. Embedded targets get specific ceilings:
  - `// ponytail: polling loop, switch to DMA when throughput matters`
  - `// ponytail: linear scan, hash lookup when item count > 100`
  - `// ponytail: ISR disables interrupts globally, switch to nested-critical-section when latency budget tightens`
  - `// ponytail: fixed-size ring buffer, bump to dynamic when payload size grows`
- **TODO format**: `TODO(ruben): ...` (owner in parentheses, colon, brief description). TODOs without an owner are anonymous debt; the code-standardizer flags them. Reference an issue or plan id when one exists: `TODO(ruben): retire shim, see docs/artifacts/plans/...`.
- **What does not need a comment**: obvious function names (`// fetch the user` above `fetch_user`); standard-library calls (`// open the file` above `fopen(path, "r")`); type aliases (`// user_id_t is the user id` above `typedef int user_id_t`).
- **Commented-out code is forbidden**. Delete it; git remembers.

code-standardizer check: `grep -rEn "^\s*(//|/\*)" --include="*.c" --include="*.cpp" --include="*.h" --include="*.hpp" . | grep -vE "ponytail:|TODO\([a-zA-Z0-9_-]+\):"` returns zero findings on new files; `grep -rEn "TODO[^(]" --include="*.c" --include="*.cpp" .` (anonymous TODOs without an owner) returns empty.