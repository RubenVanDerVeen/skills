# Go

Per-language guide. Fills the frozen 8-section template from `2026-08-04-foundation-design.md`. Sister files: `references/tooling.md`, `references/architecture.md`.

Go is opinionated: `gofmt` and `go vet` ship with the toolchain, the compiler enforces no-cycles and the `internal/` visibility boundary, and `goimports` is the canonical import sorter. This guide is correspondingly lighter than the Python guide. Where Go decides for us, the guide says so in one line and links the rule; where there is a real choice (the `golangci-lint` rule set, hook wiring, layout), the guide prescribes.

## Toolchain

Three pieces, all bundled or one-binary:

- **`gofmt`** for formatting. Zero config. Non-negotiable.
- **`goimports`** for import sorting and formatting. Wraps `gofmt`; sorts into three groups (stdlib, third-party, local). Replaces `gofmt` in the local check.
- **`golangci-lint`** for lint. Aggregates `govet`, `staticcheck`, `revive`, `errcheck`, `gosec`, `gocritic`, and others into one config and one exit code.

The compiler catches a class of bugs no linter needs to (unused imports/variables, unreachable code, shadowed variables via `govet` `shadow`, missing error checks via `errcheck`). The agent does not run those by hand; they ride along with `golangci-lint` or `go vet`.

### Pin and configure

Pin the Go toolchain in `go.mod`. The `go` directive sets the minimum compiler version; the `toolchain` directive (Go 1.21+) pins the exact compiler used to build. Pin `golangci-lint` via a `tool` directive (Go 1.24+) or pin the version in CI and document it in `AGENTS.md`. Config in `.golangci.yml` at the repo root:

```yaml
# .golangci.yml
run:
  timeout: 5m
  tests: true

linters:
  disable-all: true
  enable:
    - errcheck     # unchecked errors
    - govet        # shadow, printf, unreachable
    - staticcheck  # 150+ bug and style checks
    - revive       # golint successor, naming + style
    - ineffassign  # unused assignments
    - unused       # unused identifiers (replaces deadcode)
    - gosec        # security
    - gocritic     # opinionated extras
    - misspell     # typos in comments and strings

linters-settings:
  govet:
    enable:
      - shadow
  revive:
    rules:
      - name: exported
      - name: var-naming
      - name: package-comments

issues:
  exclude-rules:
    - path: _test\.go
      linters: [errcheck, gosec]
```

Rule families enabled, not line-by-line rule ids. The standardizer checks the family list, not the rule ids inside each family.

### Check command

The exact command CI and the standardizer agent run:

```
goimports -l . && golangci-lint run
```

`goimports -l` lists files that need reformatting (exit zero means clean); `golangci-lint run` aggregates every enabled linter. `gofmt -l .` is acceptable as a fallback when `goimports` is not installed; `goimports` is preferred because it also sorts imports.

### Hook wiring

Wire into one of the patterns in `references/tooling.md`. Go's default is native git hooks; `golangci-lint` and `goimports` ship as single binaries with no framework dependency:

```sh
# .githooks/pre-commit
#!/usr/bin/env sh
set -e
goimports -l . | tee /dev/stderr | grep -q . && exit 1
golangci-lint run
```

Polyglot repos in this monorepo already use the project-local `.githooks/` pattern; add the stanza above and document `git config core.hooksPath .githooks` in `opencode-install.md` or `AGENTS.md`.

### What `golangci-lint` does not enforce

The standardizer, not `golangci-lint`, owns the items below; if the project skips these, no lint run will catch it:

- **Cyclomatic complexity**: `gocritic` has a `rangeValCopy` and `hugeParam` family but no general complexity knob. Projects that need a number add `cyclop` (separate binary) and a `MAX_COMPLEXITY` constant in the config; otherwise complexity is a code-review judgement.
- **Doc comment presence**: `revive`'s `exported` rule nudges but does not fail when a doc comment is missing. Whether a public function has one is a documentation-policy check (see Documentation below), not a lint finding.
- **Architecture boundaries inside a module**: `golangci-lint` with `depguard` can ban imports of specific packages, but the canonical Go boundary tool is the language itself: `internal/` cannot be imported from outside the parent module (the compiler refuses it). See Architecture.

Standardizer check: `goimports -l .` exits zero and `golangci-lint run` exits zero; `.golangci.yml` present with `run.timeout` and at least the `errcheck`, `govet`, `staticcheck`, `revive` linters enabled; `go.mod` declares both a `go` and a `toolchain` directive.

## Naming

Go's rules are stronger than Python's; the compiler and `go vet` enforce several of them.

| Element | Convention | Example |
|---------|-----------|---------|
| Files | `lowercase.go`, underscores allowed for `_test.go` and grouped files (`url_parser.go`) | `user_service.go`, `user_service_test.go` |
| Test files | `*_test.go` co-located with the package | `user_service_test.go` |
| Test data / fixtures | `testdata/` directory, not committed-as-source files | `internal/parser/testdata/fixture.json` |
| Packages | `lowercase`, no underscores, no mixed case, singular noun | `package user`, `package httputil` |
| Exported identifiers | `PascalCase` | `FetchUser`, `UserService`, `MaxRetries` |
| Unexported identifiers | `camelCase` | `fetchUser`, `userCache` |
| Acronyms | capitalized uniformly (`URL`, `ID`, `HTTP`, `API`) | `ServeHTTP`, `UserID`, `parseURL` |
| Interfaces | noun or `-er` suffix describing behavior | `Reader`, `UserStore`, `TokenSigner` |
| Constants | `PascalCase` for exported, `camelCase` for unexported (not `SCREAMING_SNAKE`) | `const DefaultTimeout = 30 * time.Second` |
| Errors (sentinel) | `Err` prefix | `var ErrNotFound = errors.New("not found")` |
| Custom error types | `Error` suffix | `type AuthError struct { ... }` |
| Constructors | `New` prefix | `func NewUserService(...) *UserService` |
| Getters | field name without `Get` prefix | `func (u *User) Name() string` |

`golint` and `revive` flag underscores in package names, mixed-case package names, and inconsistent acronym capitalization. The standardizer runs them; manual override is rare.

Standardizer check: `grep -rEn "^func [a-z][a-zA-Z0-9]*\(" --include="*.go" . | grep -v "_test.go"` returns no exported-looking function names with a lowercase first letter; package names match the directory name exactly (single import block per dir, all `package <dir>` agree); `revive` `var-naming` and `exported` rules pass.

## Module / file organization

### Layout

The Go standard layout, applied verbatim:

```
cmd/<binary>/main.go      <- entry points; thin, delegate to internal/
internal/                  <- module-private code; not importable outside the module
  <feature>/...            <- one directory per feature or component
pkg/                       <- public API intended for external consumers (optional)
go.mod                     <- module path, Go version, toolchain pin
go.sum                     <- dependency hashes
```

`cmd/` contains only `main` packages that wire dependencies and start the server. Business logic lives in `internal/<feature>/`. `pkg/` is reserved for code meant to be imported by other modules; omit it when there is no external consumer.

### One package, one concern

One package per directory, named after the directory. Files inside the package group related types and functions; the package boundary is the unit of reuse. A `user` package may spread across `user.go`, `user_service.go`, `user_repository.go`; it must not export an `Invoice` or a `CSVParser`. Splitting forces a new package, which forces a new directory.

### Import order

Three groups, separated by blank lines, enforced by `goimports`:

1. Standard library (`fmt`, `os`, `net/http`).
2. Third-party (`github.com/...`, `golang.org/x/...`).
3. Local module (`github.com/<owner>/<repo>/internal/...`).

`goimports` rewrites the groups and runs `gofmt` over the file in one pass. Dot imports (`import . "fmt"`) are forbidden outside generated code; underscore imports (`import _ "embed"`) only for side-effect packages.

### File-length and complexity ceilings

Go ships no file-length or complexity rule. The community conventions:

- **File length**: ~400 lines is the ceiling. Above that, the file has more than one type with non-trivial methods and should be split. The standardizer samples new files and flags files over the ceiling; the agent does not enforce mechanically.
- **Cyclomatic complexity**: no first-party tool ships a default. `cyclop` is the usual add-on; the ceiling is the same ~10 as Python.

Standardizer check: `goimports -l .` exits zero; no `_test.go` file in production directories; `cmd/` contains only `main` packages; package directory names match the `package` declaration in every file inside.

## Architecture

Go ships two architectural primitives no other language in this guide has: the `internal/` directory and the compiler-enforced package cycle check. Both belong to the language; the standardizer reports them, not a third-party tool.

### Layering via package boundaries

The canonical Go layering maps onto the cross-language pattern:

```
cmd/<binary>/     ->  internal/<feature>/     ->  internal/<infra>/
(top entry)           (service / domain)          (data / infra adapters)
```

`internal/` is a Go visibility boundary: any package under `<module>/internal/` can be imported only by packages inside `<module>/`. The compiler refuses cross-module imports of `internal/` packages. This is the language-level boundary tool; no linter is required.

Domain packages depend inward only. Adapters depend on domain interfaces to satisfy them. `cmd/` wires concrete adapters into domain interfaces and starts the binary.

### No circular imports

The Go compiler refuses cyclic imports between packages. A cycle in two packages `a` and `b` is a build error:

```
package a imports b
package b imports a
./b.go:5:8: cycle not allowed
```

The standardizer does not run a separate cycle tool; the compiler enforces it on every build. The agent checks that the build passes (`go build ./...`), which transitively enforces the no-cycle rule.

### Feature isolation

A feature is a package subtree under `internal/<feature>/`. Other features import only its exported surface; helpers stay lowercase. `internal/user` may export `Service`, `Repository`, `User`; `internal/billing` calls them through `Service`, never through a private helper. The Go visibility rules (lowercase = unexported, package-private) make the public surface mechanically visible.

For explicit forbidden imports beyond `internal/`, add `depguard` to `.golangci.yml`:

```yaml
linters:
  enable:
    - depguard

linters-settings:
  depguard:
    rules:
      main:
        files:
          - $all
          - "!**/internal/**"
        allow:
          - $gostd
          - github.com/owner/repo
```

This bans any import of a non-allowlisted module from files outside `internal/`.

### Boundary spec

For medium-or-larger Go projects, declare the actual layer names and feature list in `.agents/architecture.md` (or the `## Architecture` section of `AGENTS.md`). The boundary spec is the source of truth for "what is the layer called here"; the `internal/` tree is the source of truth for "what is private to this module".

Standardizer check: `go build ./...` exits zero (cycle-free); `internal/` exists at the module root and contains the bulk of the package code; `.agents/architecture.md` or `AGENTS.md` `## Architecture` section exists for medium+ projects and lists the feature packages.

## Documentation

**godoc** comments on every exported identifier. The comment must start with the identifier name and be a complete sentence:

```go
// FetchUser loads a user by id. It returns ErrNotFound when no row matches.
func FetchUser(ctx context.Context, id int64) (*User, error) { ... }
```

The first word must be the identifier name (`FetchUser`, not `This function`). `revive`'s `exported` rule and `golint`'s successor both flag the broken form.

### Package documentation

Every package has a doc comment, conventionally in a `doc.go` file containing only the package declaration and the comment:

```go
// Package user implements the user domain: identity, lookup, and persistence.
package user
```

Alternatively, the package comment lives on the `package` line of the first file the compiler reads. `revive`'s `package-comments` rule enforces that every package has one.

### What must be documented

- Every exported function, method, type, constant, and variable.
- Every exported struct field whose meaning is not obvious from the name.
- Package-level doc on every package.

### What does not need a doc

- Unexported (lowercase) identifiers; allowed but optional, keep them to one line when present.
- Test files; the test name describes the behavior.
- Generated files; the generator owns the docs.

Standardizer check: `golangci-lint run` with `revive` enabled passes (the `exported` and `package-comments` rules catch missing or malformed godoc); `go doc ./...` exits zero and produces non-empty output for every package.

## Testing

**`go test`** is the framework. Bundled with the toolchain, no install step. `testing` plus standard library; community adds `testify` for assertions and `gomock` or `mockery` for mocks, both optional.

### Location and naming

- **Location**: `*_test.go` co-located with the package under test. White-box tests live next to the code; black-box tests live in a separate `<pkg>_test` package declared as `package <name>_test` in the test file (enables testing only the public API).
- **File naming**: `*_test.go`. The test file mirrors the source file it covers (`user.go` -> `user_test.go`).
- **Test data**: `testdata/` directory inside the package, ignored by `go test`.

### Structure

Arrange-act-assert. Table-driven tests are idiomatic; one `[]struct{ name string; ... }` slice, one loop, one `t.Run` per row:

```go
func TestFetchUser(t *testing.T) {
    tests := []struct {
        name    string
        userID  int64
        want    *User
        wantErr error
    }{
        {"existing user", 1, &User{ID: 1, Name: "alice"}, nil},
        {"missing user", 99, nil, ErrNotFound},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FetchUser(context.Background(), tt.userID)
            if !errors.Is(err, tt.wantErr) {
                t.Fatalf("err = %v, want %v", err, tt.wantErr)
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got %+v, want %+v", got, tt.want)
            }
        })
    }
}
```

`t.Run` names every subtest for readable `go test -v` output and selective `-run` flags. Subtests can share setup via `t.Run` sub-benchmarks or a `setup` helper called per row.

### What must be tested

- Public behavior of every exported function or method.
- Error paths (`errors.Is` against the sentinel error returned).
- Edge cases at boundary values (zero, max, negative for numeric inputs; empty slice, nil map for collections).

Coverage tooling: `go test -cover ./...` reports per-package coverage. Coverage of public behavior is the target; internal helpers are tested through the public API when they have no independent surface.

Standardizer check: `go test ./...` exits zero; `*_test.go` files co-located with their package; `go test -cover ./...` reports non-zero coverage for every non-trivial package.

## Error handling

Go uses **explicit error returns**. The rules below are what `errcheck` does not enforce on its own.

- **Always check `err`**. `errcheck` (enabled in `.golangci.yml`) flags `_, _ = foo()` and unchecked return values; the standardizer reports findings. An unchecked error is a quick-fix finding.
- **Wrap with `%w`, not `%v` or `+`**. `%w` preserves the original error for `errors.Is`/`errors.As` unwrapping:

```go
if err != nil {
    return fmt.Errorf("fetch user %d: %w", id, err)
}
```

`fmt.Errorf("...: %v", err)` formats but discards the chain; callers cannot match the sentinel. `err.Error()` plus a string concat (`err := "fetch user: " + err.Error()`) is worse: same loss, plus string allocation.

- **Use `errors.Is` and `errors.As` for matching**. `err == ErrNotFound` does not unwrap; `errors.Is(err, ErrNotFound)` does. Match sentinel errors with `errors.Is`; match error types with `errors.As`.
- **No panic for expected failures**. `panic` is reserved for programmer errors (impossible states, violated invariants the program cannot recover from). HTTP handlers, database calls, file I/O: return an error, never panic.
- **No silent swallow**. `if err != nil { /* nothing */ }` is a quick-fix finding. Either log with context (`slog.Error("...", "err", err, "user_id", id)`) or return the error wrapped.
- **Logging**: `log/slog` (Go 1.21+) for structured logging. Configure once at the application entry point; library code obtains no logger and returns errors instead.

```go
func loadConfig(path string) (*Config, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("open config %q: %w", path, err)
    }
    defer f.Close()
    // ...
}
```

Standardizer check: `golangci-lint run` with `errcheck` enabled passes; `grep -rEn "panic\(" --include="*.go" . | grep -v "_test.go"` returns only entries that are documented invariants; `grep -rEn "_ *= [a-z][a-zA-Z]+\(" --include="*.go" .` returns no discarded errors in non-test files.

## Comments

- **Explain why, not what**. Code says what; comments say why. A comment that restates the next line is dead prose.
- **`ponytail:` markers for deliberate shortcuts**. When the implementation takes a known-shorter path with a documented ceiling (global mutex, O(n^2) scan, naive heuristic), add a one-line comment naming the shortcut and the upgrade path: `// ponytail: global mutex, per-account locks when throughput matters`.
- **TODO format**: `TODO(ruben): ...` (owner in parentheses, colon, brief description). TODOs without an owner are anonymous debt; the standardizer flags them. Reference an issue or plan id when one exists: `TODO(ruben): retire shim, see docs/artifacts/plans/...`.
- **What does not need a comment**: obvious type signatures (no `// id is the user id` next to `id int64`); godoc already covers the function (no `// fetch the user` above the doc comment); standard-library calls (no `// open the file` above `os.Open(path)`).
- **Commented-out code is forbidden**. Delete it; git remembers. `gofmt` will not reformat it, but reviewers will.

Standardizer check: `grep -rEn "^\s*//" --include="*.go" . | grep -vE "ponytail:|TODO\([a-zA-Z0-9_-]+\):|^//.*\.$|^// Package"` (the loose pattern matches non-template comments; tighten per project) returns zero findings on new files beyond the expected godoc and `ponytail:` lines; `grep -rEn "TODO[^(]" --include="*.go" .` (anonymous TODOs without an owner) returns empty.