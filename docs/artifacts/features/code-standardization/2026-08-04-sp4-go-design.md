# SP-4 Go Design

## Status

Sub-project of the code-standardization multi-plan. Depends on F complete. Consumes the frozen 8-section template.

## Goal

Write `skills/code-standardization/references/go.md`. Go opinionates most of this itself; the guide is correspondingly shorter on prescription and clearer on defaults.

## Language-specific picks

- **Toolchain (§1):** `gofmt`/`goimports` (format, bundled, non-negotiable) + `golangci-lint` (lint, aggregates `govet`, `staticcheck`, `revive`, etc.). Config `.golangci.yml`; pin the Go toolchain via `go.mod`'s `toolchain` directive. Check `gofmt -l . && golangci-lint run`. Hook: native git hook or pre-commit framework.
- **Naming (§2):** files `lowercase.go`, no underscores in package names; exported identifiers `PascalCase`, unexported `camelCase`; acronyms capitalized (`URL`, `ID`); test files `*_test.go`.
- **Module/file org (§3):** package-per-directory; one package per directory; import grouping (stdlib → third-party → local) via goimports; no file-length rule from the tool, keep files focused.
- **Architecture (§4):** layering via package boundaries (`cmd/ → internal/ → pkg/`); `internal/` enforces non-importability outside the module (the language-level boundary tool); no circular imports (the compiler enforces).
- **Documentation (§5):** godoc comments on every exported identifier, starting with the identifier name; package doc in `doc.go` or the first file.
- **Testing (§6):** `go test` (bundled); `*_test.go` co-located; table-driven tests idiomatic; `t.Run` for subtests.
- **Error handling (§7):** explicit error returns, always check `err`; wrap with `%w`; `errors.Is`/`errors.As`; no panic for expected failures.
- **Comments (§8):** explain why; `ponytail:` markers; `TODO(ruben): ...`.

Each section ends with the one-line "what the standardizer checks" note. Lean prescription where Go decides for us.

## Out of scope

Any other file. No SKILL.md edit.
