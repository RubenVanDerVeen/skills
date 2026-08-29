# Architecture (cross-language)

The boundary layer. Pairs with `references/tooling.md` (standardization-infra layer) and each `references/<lang>.md` (per-language detail). The code-standardizer agent uses this reference to decide whether boundaries are declared, documented, and held.

## Canonical layering and dependency direction

One canonical direction across every language. Variants exist per language (see each `<lang>.md`), but the rule of thumb is identical:

```
api / presentation  ->  service / domain  ->  data / infra
```

Dependencies flow downward only. Reverse imports are a quick-fix finding.

| Layer | Owns | May import from |
|-------|------|-----------------|
| api / presentation | HTTP handlers, CLI, UI, RPC entry points | service / domain |
| service / domain | Business rules, use cases, pure logic, ports (interfaces the domain needs from the outside world) | itself and shared kernel; must not import from api / presentation or data / infra |
| data / infra | Adapters: databases, files, network, third-party SDKs | service / domain port interfaces (only to implement them); must not import from api / presentation |

The binding rule: the domain layer knows nothing about infra. Anything the domain needs from the outside world is a port (interface) declared in the domain layer; the implementation lives in data / infra and depends inward on the port to satisfy it. api / presentation may pull from both higher layers (it sees service / domain) and is itself the top of the stack. This is dependency inversion applied at the package level, uniformly across languages.

## No circular dependencies

A cycle between two modules collapses them into one module. The arch tool per language detects cycles mechanically. The code-standardizer never has to infer a cycle from naming.

| Language | Arch tool (named) | What it enforces |
|----------|-------------------|------------------|
| Python | `import-linter` | Forbidden-import contracts (layer rules) plus cycle detection across user-defined `contracts` in `.importlinter` |
| TypeScript / JavaScript | `dependency-cruiser` | Forbidden-import rules plus cycle detection in `.dependency-cruiser.{cjs,mjs,json}` |
| C / C++ | include-guard discipline plus `include-what-you-use` (IWYU) for structural enforcement | Each header included once, in include-guarded form; IWYU flags headers that leak private types and unused includes |
| Go | layering linters (`golangci-lint` with `depguard` for forbidden imports and `gomodguard` for module-allowlist rules) plus the compiler-enforced package cycles through the built-in cycle check and `internal/` boundary enforcement | Linters ban forbidden imports; the compiler refuses cycles inside a module and refuses cross-`internal/` access from sibling packages |
| Rust | clippy's `mod_module_files` and module rules plus compiler-enforced cycles through `mod` boundaries and visibility / workspace lints | clippy flags awkward module file layout; the compiler enforces module tree, `pub(crate)` / `pub(super)` visibility, and crate (`lib` / `bin` / workspace-member) boundaries |

Each per-language guide carries the exact config snippet and the check command. The table above is the contract: the foundation specifies the tool, the language sub-plan specifies the config.

## Feature / module isolation

A feature is a vertical slice that crosses layers (api + service + data) for one capability. Features must not reach into each other's internals.

- Public interface only: `import` the feature's public entry point, not its helpers, not its adapters. If a helper must be shared, it moves to a shared module, not the caller's import.
- One-feature-per-concern: two features that largely duplicate each other are one feature with optional behavior, not two features copying each other.
- Cross-feature calls go through the public interface of the called feature, never through a sibling's data layer directly.

The code-standardizer checks this by sampling imports in new code: does this file import the public module of another feature, or does it reach inside? Reaching inside is a quick-fix finding with the suggested fix ("import from `<feature>.public_api`").

## Boundary spec: location and content

Every medium-or-larger project declares its layers in one short, agent-visible document. The location is fixed so the agent always knows where to look:

- Primary: `.agents/architecture.md` at the repo root (one file, one purpose).
- Fallback: a section in `AGENTS.md` named `## Architecture` if `.agents/` does not exist.
- Out of scope: `README.md` (human-facing, not a canonical agent context under the agents.md convention) and per-language `references/<lang>.md` (those document the standard, not the project's choices).

The boundary spec contains exactly four items, in this order, in plain prose plus a small diagram:

1. **The layers this project uses**, named. Example: `api`, `service`, `data`. Drop a layer the project does not use; do not invent one.
2. **The allowed dependency direction**, expressed as "layer X may import from layer Y; layer Y must not import from X". One sentence per layer.
3. **The features / modules**, listed as a bullet list of vertical slices that own their files across layers. New features get a new entry.
4. **Any project-specific exceptions** to the canonical direction, with the reason. Exceptions are allowed; they are documented here, not in code comments.

## What the tool checks versus what the agent checks

Split of responsibility. Tools do mechanical work; agents do judgement work. Each side owns its lane.

| What the arch tool checks | What the code-standardizer agent checks |
|--------------------------|------------------------------------|
| Every direction-changing import is forbidden and reported with file + line. | The boundary spec exists at `.agents/architecture.md` (or `AGENTS.md` `## Architecture` section) and is current. |
| Every cycle in the import graph is reported. | New files added since the last audit respect the declared layers (sample three files per changed directory; spot the bad import). |
| Layer labels in the tool config match the labels in the boundary spec. | The names of layers in the boundary spec match the names in the tool config; a stale label is a finding. |
| Forbidden cross-feature internals are reported by name. | Each feature ships a public-interface module (e.g. `<feature>.public_api`, `index` exporting the surface) and other features import only from it. |
| Tool exit code is non-zero on any violation. | The tool is installed (`command -v <tool>`) and pinned; absent tool is a quick-fix finding naming the tool and config file. |

Run order on every audit: the agent checks the boundary spec is present and current, runs the arch tool in check mode, then samples new files for imports that respect the declared layers. The tool is the source of truth for cycles and forbidden imports; the agent is the source of truth for "is the spec still true".

## Per-language guides

- Python: `references/python.md`
- TypeScript / JavaScript: `references/typescript-javascript.md`
- C / C++: `references/c-cpp.md`
- Go: `references/go.md`
- Rust: `references/rust.md`
