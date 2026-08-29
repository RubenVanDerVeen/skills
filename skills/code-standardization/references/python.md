# Python

Per-language guide. Fills the frozen 8-section template from `2026-08-04-foundation-design.md`. Sister files: `references/tooling.md`, `references/architecture.md`.

## Toolchain

One tool owns all three concerns: **Ruff** as formatter, linter, and import sorter. Ruff replaces Black, flake8, isort, pydocstyle, and pyupgrade. The three-piece kit collapses to one binary and one config file.

### Pin and configure

Pin Ruff in the project's lockfile (`uv.lock`, `poetry.lock`, or `requirements-dev.txt`). Configuration lives in `pyproject.toml` under `[tool.ruff]`. The block below is copy-pasteable; rule selections follow the project's enabled rule families, not line-by-line copies of Ruff's defaults.

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src", "tests"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint]
# Rule families enabled; the code-standardizer checks the family list, not the rule ids.
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort (import sort)
    "B",   # flake8-bugbear
    "UP",  # pyupgrade (modern syntax)
    "SIM", # flake8-simplify
    "RUF", # Ruff-specific
]
ignore = [
    "E501",  # line length handled by formatter
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # asserts are expected in tests
```

### Check command

The exact command CI and the code-standardizer agent run:

```
ruff format --check . && ruff check .
```

`ruff format` covers formatting; `ruff check` covers lint and import sort (the `I` family). One command, two exit codes, no separate isort or pyupgrade step.

### Hook wiring

Wire Ruff into one of the patterns in `references/tooling.md`. For Python-only repos the pre-commit framework is the default:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9  # pin to match the lockfile
    hooks:
      - id: ruff-format
      - id: ruff-check
        args: [--fix]
```

Polyglot repos in this monorepo use the project-local `.githooks/` pattern; add a `pre-commit` shell stanza that runs `ruff format --check . && ruff check .`.

### What Ruff does not enforce

Ruff covers formatting, style, import order, common bugs, and modernization. The code-standardizer, not Ruff, owns the items below; if the project skips these, Ruff will not catch it:

- **Cyclomatic complexity**: enable Ruff `C901` with a threshold (~10); projects that need finer control add `xenon` or `mccabe` as a secondary check.
- **Docstring presence and content**: Ruff `D` (pydocstyle) checks style only. Whether a public function has a docstring at all is a documentation-policy check, not a lint finding.
- **Type-hint coverage**: Ruff does not flag untyped public APIs. `mypy --strict` or `pyright` is a separate invocation; the agent reports its presence, not its output.
- **Architecture boundaries**: Ruff cannot express layer rules or no-cycle contracts. Use `import-linter` (see Architecture below).

code-standardizer check: `ruff format --check . && ruff check .` exits zero; `pyproject.toml` has `[tool.ruff]` with `select` covering `E`, `F`, `I`, `UP`; Ruff version in lockfile matches the `rev:` in `.pre-commit-config.yaml`.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Files | `snake_case.py` | `user_service.py` |
| Test files | `test_*.py` co-located or in `tests/` | `test_user_service.py` |
| Packages | `snake_case`, no hyphens | `user_service/` |
| Functions / variables | `snake_case` | `def fetch_user(user_id: int)` |
| Classes / exceptions | `PascalCase` | `class UserService`, `class AuthError(Exception)` |
| Module-level constants | `UPPER_SNAKE` | `MAX_RETRIES = 3` |
| Type aliases | `PascalCase` | `UserId = int` |
| Private symbols | leading underscore | `_cache`, `_internal_helper()` |
| Boolean predicates | `is_`, `has_`, `can_` prefix | `is_active`, `has_permission` |

Do not use single-letter names outside tight comprehensions or throwaway loop variables. Avoid `I`, `l`, `O` as identifiers; they read as digits in some fonts.

code-standardizer check: `grep -rEn "class [a-z_]+\(|def [A-Z][a-zA-Z]+\(" --include="*.py" .` returns empty for new files; private API count in `__all__` matches the public surface.

## Module / file organization

### Layout

- **Installable package**: `src/<package_name>/` layout. Tests in `tests/` at the repo root. Avoids the `src/` vs flat ambiguity for tools that look one level deep.
- **Scripts and small tools**: flat layout at the repo root or under a `scripts/` directory; no `src/` wrapper when there is no package to install.

### One module, one responsibility

One primary class or one cohesive function group per module. A module named `user.py` may export `User`, `fetch_user`, and `save_user`; it may not export `User`, `Invoice`, and `parse_csv`. Splitting forces a directory.

### Import order

Three blocks, separated by blank lines, enforced by Ruff `I`:

1. Standard library (`os`, `pathlib`, `typing`).
2. Third-party (`httpx`, `pydantic`, `sqlalchemy`).
3. Local (`from myproject.user import User`).

`from __future__ import annotations` sits above block 1. No wildcard imports (`from x import *`) outside `__init__.py` re-exports.

### File-length and complexity ceilings

- **File length**: ~400 lines is the ceiling. Above that, the module has more than one responsibility and should be split.
- **Cyclomatic complexity**: enabled via Ruff `C901` with `max-complexity = 10`. Functions above the threshold are a quick-fix finding naming the function and the path.

code-standardizer check: Ruff `I` passes; file length `awk 'END{print NR}' <file>` or `wc -l` per file; Ruff `C901` reports zero findings on `ruff check .`.

## Architecture

Ruff cannot express layer rules. Use **import-linter** to enforce the canonical dependency direction and detect cycles. Layers typically follow the canonical split from `references/architecture.md`:

```
api / presentation  ->  service / domain  ->  data / infra
```

Domain imports nothing above it. Infrastructure depends inward on domain port interfaces only.

### `import-linter` configuration

Pin in the dev lockfile (`import-linter` is a separate package). Config in `.importlinter` (INI) or `pyproject.toml` `[tool.importlinter]`:

```ini
[importlinter:contract:layers]
type = layers
layers =
    myproject.api
    myproject.service
    myproject.data

[importlinter:contract:forbidden-dependencies]
type = forbidden_imports
forbidden_imports =
    forbidden =
        myproject.data
    allow_indirect_imports = True
```

Run the contract check before every commit:

```
lint-imports
```

`lint-imports` exits non-zero on a forbidden import or a cycle. The code-standardizer runs it after Ruff; both must be clean for the audit to pass.

### Boundary spec

For medium-or-larger Python projects, declare the actual layer names and feature list in `.agents/architecture.md` (or the `## Architecture` section of `AGENTS.md`). The boundary spec is the source of truth for "what is the layer called here"; `import-linter` enforces the direction.

code-standardizer check: `command -v lint-imports && lint-imports` exits zero; `.importlinter` or `[tool.importlinter]` block present; `.agents/architecture.md` or `AGENTS.md` `## Architecture` section exists for medium+ projects.

## Documentation

**Google-style docstrings** on every public function, class, and module. Public means exported in `__all__`, or, where `__all__` is absent, every non-underscore-prefixed name at module scope.

Shape:

```python
def fetch_user(user_id: int, *, include_deleted: bool = False) -> User:
    """Load a user by id.

    Args:
        user_id: Primary key of the user to load.
        include_deleted: When True, include soft-deleted rows in the result.

    Returns:
        The matching User, or None if no row matches.

    Raises:
        AuthError: If the caller's session token is invalid.
    """
```

**Type hints required on every public function and method signature**. Internal helpers may omit hints when the types are obvious from context. Ruff does not flag missing type hints; that is a documentation-policy check, enforced by the code-standardizer via `mypy` or `pyright` presence, not by lint output.

Private docstrings are allowed but optional. When present, keep them to one line describing intent; save the long form for public surfaces.

code-standardizer check: `grep -rEn "^def [a-z]" --include="*.py" -A 1 . | grep -E '""".*"""'` finds one-line docstring above each public def; `mypy --strict` or `pyright` is configured (presence check, not output).

## Testing

**pytest** is the framework. `unittest` is allowed only inside legacy code; new tests are pytest.

- **Location**: `tests/` at the repo root, mirroring the source tree (`tests/test_user_service.py` for `src/myproject/user_service.py`).
- **File naming**: `test_*.py`. Class names `Test*`; function names `test_*`.
- **Structure**: arrange-act-assert, one behavior per test. Parametrize over edge cases instead of copy-pasting test bodies.
- **Fixtures**: shared fixtures in `conftest.py`. Avoid global mutable state; pytest fixtures reset per-test by default.
- **Coverage**: behavior-level (public API) and error-path coverage are mandatory. Internal helpers are tested through the public API when they have no independent surface.

```python
import pytest
from myproject.user_service import fetch_user

@pytest.mark.parametrize("user_id,expected", [(1, "alice"), (2, "bob")])
def test_fetch_user_returns_expected_name(user_id, expected):
    result = fetch_user(user_id)
    assert result.name == expected
```

code-standardizer check: `pytest` is in dev deps; `tests/test_*.py` files mirror `src/myproject/*.py` paths; `ruff check tests/` passes; `pytest --collect-only` resolves every collected test.

## Error handling

Python uses **exceptions** for exceptional flow. The rules below are what Ruff does not enforce on its own.

- **Never bare `except:`**. Catch the narrowest class that covers the failure mode; bare `except:` swallows `KeyboardInterrupt` and `SystemExit`.
- **Never silent swallow**. A bare `except SomeError: pass` is a quick-fix finding. Either log the exception with `logger.exception(...)` or re-raise (possibly wrapped: `raise AuthError(...) from err`).
- **Log or raise, not both silently**. If you log, log with context (the operation, the relevant identifiers, the traceback via `exc_info=True` or `logger.exception`); if you raise, do not also log a redundant line the handler will emit again.
- **Custom exceptions inherit from a project root** (`class AuthError(MyProjectError)`), not directly from `Exception`, so callers can catch project-wide failures as one family.
- **Logging** uses the stdlib `logging` module, configured once at the application entry point. Library code obtains a module logger with `logger = logging.getLogger(__name__)`. No `print()` for diagnostics in production code; `print()` is fine in scripts and notebooks.

```python
import logging

logger = logging.getLogger(__name__)

def load_config(path: str) -> Config:
    try:
        return Config.from_file(path)
    except FileNotFoundError as err:
        logger.exception("config file missing", extra={"path": path})
        raise ConfigError(f"no config at {path}") from err
```

code-standardizer check: `grep -rEn "except:\s*$" --include="*.py" .` returns empty; `grep -rEn "except [A-Za-z]+:\s*pass$" --include="*.py" .` returns empty; `print(` is absent from `src/**` outside scripts; `logger = logging.getLogger(__name__)` appears in non-trivial modules.

## Comments

- **Explain why, not what**. Code says what; comments say why. A comment that restates the next line is dead prose.
- **`ponytail:` markers for deliberate shortcuts**. When the implementation takes a known-shorter path with a documented ceiling (global lock, O(n^2) scan, naive heuristic), add a one-line comment naming the shortcut and the upgrade path: `# ponytail: global lock, per-account locks when throughput matters`.
- **TODO format**: `TODO(ruben): ...` (owner in parentheses, colon, brief description). TODOs without an owner are anonymous debt; the code-standardizer flags them. Reference an issue or plan id when one exists: `TODO(ruben): retire shim, see docs/artifacts/plans/...`.
- **What does not need a comment**: obvious type hints (no `# user_id: int` next to `user_id: int`); docstrings already cover the function (no `# fetch the user` above the docstring); standard-library calls (no `# open the file` above `open(path)`).
- **Commented-out code is forbidden**. Delete it; git remembers.

code-standardizer check: `grep -rEn "^\s*#" --include="*.py" . | grep -vE "ponytail:|TODO\([a-zA-Z0-9_-]+\):"` returns zero findings on new files; `grep -rEn "TODO[^(]" --include="*.py" .` (anonymous TODOs without an owner) returns empty.