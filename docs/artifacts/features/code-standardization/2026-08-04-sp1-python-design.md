# SP-1 Python Design

## Status

Sub-project of the code-standardization multi-plan. Depends on foundation (F) complete. Consumes the frozen 8-section template in `2026-08-04-foundation-design.md` § "Frozen per-language template".

## Goal

Write `skills/code-standardization/references/python.md` instantiating the frozen template for Python.

## Language-specific picks (filled into the template)

- **Toolchain (§1):** Ruff as the single formatter + linter + import sorter (replaces Black + flake8 + isort + pydocstyle + pyupgrade). Config in `pyproject.toml [tool.ruff]`; pin via `requirements-dev.txt` or lockfile. Check command `ruff format --check . && ruff check .`. Hook: pre-commit framework or the repo's `.githooks/`.
- **Naming (§2):** files `snake_case.py`; functions/variables `snake_case`; classes `PascalCase`; constants `UPPER_SNAKE`; test files `test_*.py`; private with leading underscore.
- **Module/file org (§3):** `src/` layout for installable packages, flat for scripts; one primary class or cohesive function group per module; import order stdlib → third-party → local (Ruff `I`); file-length ceiling ~400 lines, complexity via Ruff `C901` ~10.
- **Architecture (§4):** `import-linter` for layers and no-cycles; layers typically `api/presentation → service → domain → infra`; domain imports nothing above it.
- **Documentation (§5):** Google-style docstrings on public functions/classes/modules; type hints required on public API.
- **Testing (§6):** pytest; `test_*.py` co-located in `tests/` mirroring source; arrange-act-assert; parametrize over edge cases.
- **Error handling (§7):** exceptions for exceptional flow; never bare `except:`; log or raise, not both silently.
- **Comments (§8):** explain why; `ponytail:` markers for deliberate shortcuts; `TODO(ruben): ...` format.

Each section ends with the one-line "what the standardizer checks" note.

## Out of scope

Any file other than `references/python.md`. No edits to SKILL.md (the dispatch-table link is already a forward link from F1). No other language.
