# TypeScript / JavaScript

Per-language guide. Fills the frozen 8-section template from `2026-08-04-foundation-design.md`. Sister files: `references/tooling.md`, `references/architecture.md`. Covers TS-first projects; plain JS projects use the same file/import rules but replace TSDoc with JSDoc and TS compiler checks with `// @ts-check` plus a `jsconfig.json`.

## Toolchain

Two tools cover the three concerns: **Prettier** as the formatter (opinionated, non-negotiable) and **ESLint** as the linter (configurable rule set) that also owns import sort via `eslint-plugin-import`. The kit splits because Prettier's "no config debates" stance is worth keeping; ESLint covers the rules Prettier deliberately ignores (correctness, complexity, imports, type-aware rules via `typescript-eslint`).

### Pin and configure

Pin Prettier and ESLint exact versions in `package.json` `devDependencies` (no `^` or `~`); pin the package manager itself with the `packageManager` field. Config lives in `.prettierrc.json` plus `eslint.config.js` (flat config, ESLint 9+, the modern default). The block below is copy-pasteable; rule selections follow the families the standardizer checks, not exhaustive rule lists.

```json
// .prettierrc.json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

```js
// eslint.config.js (flat config, ESLint 9+)
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import importPlugin from "eslint-plugin-import";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    plugins: { import: importPlugin },
    rules: {
      "import/order": ["error", { "groups": ["builtin", "external", "internal", ["parent", "sibling", "index"]] }],
      "import/no-cycle": "error",
      "no-console": ["warn", { "allow": ["warn", "error"] }],
      complexity: ["error", { max: 10 }],
    },
  },
];
```

### Check command

The exact command CI and the standardizer agent run:

```
prettier --check . && eslint .
```

`prettier --check` reports files that would change; `eslint .` covers lint, import order, and complexity. One command, two exit codes, no separate import-sort step.

### Hook wiring

Wire Prettier and ESLint into one of the patterns in `references/tooling.md`. For TS/JS-only repos the default is **husky + lint-staged**:

```json
// package.json
{
  "devDependencies": {
    "husky": "9.x.x",
    "lint-staged": "15.x.x",
    "prettier": "3.x.x",
    "eslint": "9.x.x"
  },
  "lint-staged": {
    "*.{ts,tsx,js,jsx,json,md,css}": ["prettier --write", "eslint --fix"]
  },
  "scripts": {
    "check": "prettier --check . && eslint ."
  }
}
```

Activate once per clone with `npx husky init` and a `.husky/pre-commit` shell stanza that runs `npx lint-staged`.

### What ESLint does not enforce

Prettier covers formatting; ESLint covers correctness, complexity, and imports. The items below are policy, not lint:

- **TSDoc / JSDoc presence**: ESLint has `jsdoc/require-jsdoc` and `tsdoc/syntax`, but rule families vary; whether a public function has any doc comment at all is a documentation-policy check, not a lint finding.
- **Type coverage**: `strict` in `tsconfig.json` is a TS compiler check. ESLint does not run the type checker unless `@typescript-eslint/no-unsafe-*` rules are enabled with type info.
- **Architecture boundaries**: ESLint cannot express layer rules or no-cycle contracts across the project graph. Use `dependency-cruiser` (see Architecture below).

**oxlint alternative**: `oxlint` is faster and covers many ESLint rules; pick it for very large monorepos where ESLint's runtime is the bottleneck. The standardizer accepts either, pinned in `devDependencies`. Mixing ESLint and oxlint in the same repo is not allowed.

Standardizer check: `prettier --check . && eslint .` exits zero; `.prettierrc*` (or `prettier` field in `package.json`) present; `eslint.config.js` (or legacy `.eslintrc.*`) present; ESLint and Prettier versions in `package.json` `devDependencies` are exact (no `^` or `~`); `packageManager` field pinned.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Files (modules) | `kebab-case.ts` / `kebab-case.js` | `user-service.ts` |
| React component files | `PascalCase.tsx` / `PascalCase.jsx` | `UserCard.tsx` |
| Test files | `*.test.ts` / `*.spec.ts` (or `.tsx`, `.js`, `.jsx`) | `user-service.test.ts` |
| Functions / variables | `camelCase` | `fetchUser(userId)` |
| Classes / exceptions | `PascalCase` | `class UserService`, `class AuthError extends AppError` |
| Interfaces / types / enums | `PascalCase`, no `I` prefix on interfaces | `type UserId = string`, `interface FetchOptions`, `enum OrderState` |
| Module-level constants | `UPPER_SNAKE` | `MAX_RETRIES = 3` |
| React components | `PascalCase`, file matches component name | `function UserCard(props: Props)` |
| Boolean predicates | `is`, `has`, `can` prefix | `isActive`, `hasPermission`, `canDelete` |
| Private symbols (TS classes) | `private` / `protected` modifier; leading `_` for module-scope | `_cache`, `_internalHelper()` |
| Generic type parameters | Single capital, PascalCase when multi-word | `function map<T, U>(items: T[])` |
| File suffixes | `.ts` logic, `.tsx` JSX, `.d.ts` ambient | `types.ts`, `Button.tsx`, `global.d.ts` |

Avoid single-letter names outside generic parameters, tight closures, or throwaway loop counters.

Standardizer check: `grep -rEn "^(export )?(class|interface|type|enum) [a-z_]+ " --include="*.ts" --include="*.tsx" .` returns empty; `grep -rEn "interface I[A-Z]" --include="*.ts" .` returns empty (no `I` prefix on interfaces); React component files start with a capital letter (`grep -rEln "^(export )?(default )?function [a-z]" --include="*.tsx" .` returns empty).

## Module / file organization

### Layout

- **Library / app**: `src/<feature>/` for vertical slices; `src/lib/` for shared utilities; tests co-located with source (see Testing).
- **Single-package scripts**: flat at the repo root or under `src/`. No `src/` wrapper when the project has no test runner or bundler.
- **Public surface**: package boundaries export through a single `index.ts` barrel (see barrel rule below).

### One module, one primary export

Components default-export from a file that shares the component name (`export default function UserCard()`). Utility modules use named exports; a `utils.ts` file exporting `formatDate`, `parseId`, and `slugify` is fine when they are one cohesive group, but `formatDate` and `parseCsv` do not belong in the same file.

### Import order

Four groups, separated by blank lines, enforced by `eslint-plugin-import` with `import/order`:

1. Built-in (`node:fs`, `node:path`).
2. External (`react`, `lodash`, `zod`).
3. Internal (project aliases and packages, e.g. `@app/shared`).
4. Relative (`./user-service`, `../lib/format`).

No wildcard imports (`import * as X from "y"`) outside type re-exports; no default imports for modules that export only named symbols.

### Barrel files

`index.ts` barrels are allowed only at **package boundaries** (a published package's `src/index.ts`, a feature's public surface). Internal barrels are forbidden because they defeat tree-shaking and create accidental cycles; an internal `components/index.ts` re-exporting ten components is a quick-fix finding.

### File length and complexity

- **File length**: ~400 lines is the ceiling. Above that, the module has more than one responsibility and should be split.
- **Cyclomatic complexity**: ESLint `complexity` rule with `max: 10`. Functions above the threshold are a quick-fix finding naming the function and the path.

Standardizer check: `eslint .` exits zero with `import/order` rule on; file length `wc -l` per file under `src/` is below the ceiling; ESLint `complexity` reports zero findings on `eslint .`; no `src/**/index.ts` barrel outside the package root or a feature's public surface.

## Architecture

ESLint's import plugin catches local cycles inside a file's import graph, but it cannot express layer rules or feature-isolation contracts across the project. Use **dependency-cruiser** for both: forbidden-import rules plus cycle detection. Layers for typical TS/JS projects follow the canonical split from `references/architecture.md`:

```
ui / presentation  ->  features  ->  data  ->  lib
```

`features` modules do not import from each other's internals (see feature-isolation rule in `architecture.md`). `lib` is shared utilities with no upward dependencies; `data` adapters depend on `lib` interfaces only.

### `dependency-cruiser` configuration

Pin in `devDependencies`. Config in `.dependency-cruiser.cjs` (or `.dependency-cruiser.json`):

```js
// .dependency-cruiser.cjs
module.exports = {
  forbidden: [
    {
      name: "no-circular",
      severity: "error",
      comment: "No cycles allowed between modules.",
      from: {},
      to: { circular: true },
    },
    {
      name: "no-cross-feature",
      severity: "error",
      comment: "Features must not import each other's internals.",
      from: { path: "^src/features/([^/]+)/.+" },
      to: { path: "^src/features/(?!$1/)[^/]+/.+" },
    },
    {
      name: "no-data-to-ui",
      severity: "error",
      comment: "data/ must not import from ui/ or features/.",
      from: { path: "^src/data/" },
      to: { path: "^src/(ui|features)/" },
    },
  ],
  options: {
    doNotFollow: { path: "node_modules" },
    tsConfig: { fileName: "tsconfig.json" },
    enhancedResolveOptions: {
      exportsFields: ["exports"],
      conditionNames: ["import", "require", "node", "default"],
    },
  },
};
```

Run the contract check before every commit:

```
depcruise src --config .dependency-cruiser.cjs
```

`depcruise` exits non-zero on a forbidden import or a cycle. The standardizer runs it after ESLint; both must be clean for the audit to pass.

### Boundary spec

For medium-or-larger TS/JS projects, declare the actual layer names and feature list in `.agents/architecture.md` (or the `## Architecture` section of `AGENTS.md`). The boundary spec is the source of truth for "what is the layer called here"; `dependency-cruiser` enforces the direction. Feature names in `depcruise` rules must match the names in the boundary spec.

Standardizer check: `command -v depcruise && depcruise src --config .dependency-cruiser.cjs` exits zero; `.dependency-cruiser.cjs` or `.dependency-cruiser.json` present; `.agents/architecture.md` or `AGENTS.md` `## Architecture` section exists for medium+ projects; layer labels in `depcruise` config match the labels in the boundary spec.

## Documentation

**TSDoc** on every exported TS symbol; **JSDoc** for plain JS. Exported means reachable from `index.ts` (the package boundary) or marked with the `export` keyword on a non-internal module.

Shape for TS:

```ts
/**
 * Load a user by id.
 * @param userId - Primary key of the user to load.
 * @param options - Fetch options.
 * @param options.includeDeleted - When true, include soft-deleted rows.
 * @returns The matching User, or null if no row matches.
 * @throws {AuthError} If the caller's session token is invalid.
 */
export function fetchUser(userId: UserId, options: FetchOptions = {}): User | null;
```

**Type annotations required on every public function signature**. The `strict` flag in `tsconfig.json` (`"strict": true`, which implies `noImplicitAny` and `strictNullChecks`) is the baseline; projects that need stricter checks add `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`. Plain JS files use JSDoc `@param` / `@returns` / `@typedef` to give editors the same signal.

Private doc comments are allowed but optional. When present, keep them to one line describing intent; save the long form for public surfaces. `// @ts-ignore` is forbidden; use `// @ts-expect-error` with a `TODO(name): ...` line describing the issue and a link to the issue or plan id, so a future run actually fails when the underlying type error is fixed.

Standardizer check: `eslint-plugin-tsdoc` (or `eslint-plugin-jsdoc`) is configured with the `tsdoc/syntax` or `jsdoc/require-jsdoc` rule enabled for exported symbols; `tsconfig.json` has `"strict": true`; `grep -rEn "// @ts-ignore" --include="*.ts" --include="*.tsx" .` returns empty on new files.

## Testing

**Vitest** preferred; **Jest** acceptable for legacy code. New TS/JS projects pick Vitest because it ships native ESM and TS support without `babel-jest` or `ts-jest` glue.

- **Location**: co-located with source (`src/user-service.test.ts` next to `src/user-service.ts`). A top-level `tests/` directory is allowed but discouraged for new projects because it doubles the navigation cost.
- **File naming**: `*.test.ts` (Vitest and Jest default). `*.spec.ts` is acceptable for projects that prefer BDD-style naming.
- **Structure**: `describe` per unit, `it` (or `test`) per behavior. One behavior per `it`. Arrange-act-assert, named after the behavior (`it('returns null when the user does not exist')`).
- **Fixtures**: `beforeEach` for setup, `afterEach` for cleanup. Shared fixtures in a `*.fixtures.ts` file co-located or under `src/__fixtures__/`.
- **Mocks**: mock at boundaries (HTTP, DB, filesystem, clock) with `vi.mock` (Vitest) or `jest.mock` (Jest). Do not mock internal helpers; test them through the public API.

```ts
import { describe, it, expect, vi } from "vitest";
import { fetchUser } from "./user-service";

describe("fetchUser", () => {
  it("returns null when no row matches", async () => {
    vi.spyOn(db, "query").mockResolvedValue([]);
    expect(await fetchUser("missing")).toBeNull();
  });

  it("throws AuthError when the session is invalid", async () => {
    vi.spyOn(auth, "verify").mockRejectedValue(new AuthError("expired"));
    await expect(fetchUser("alice")).rejects.toThrow(AuthError);
  });
});
```

Coverage is mandatory for public behavior (every exported function has at least one happy-path test) and error paths (every `throw` has a test). Internal helpers are tested through the public API when they have no independent surface.

Standardizer check: `vitest` (or `jest`) in `devDependencies`; `*.test.ts` or `*.spec.ts` files co-located with `src/**`; `eslint .` passes on tests (with `tests` overrides for `no-console` etc.); `vitest run` (or `jest`) resolves every collected test.

## Error handling

TS/JS uses **exceptions** for exceptional flow, with a small Result-pattern exception for domain boundaries that benefit from explicit success/failure types (parsers, validators, anything where errors are expected outcomes, not surprises).

- **Throw `Error` subclasses, never strings or plain objects**. `throw "boom"` is a quick-fix finding; `throw new Error("boom")` or `throw new AuthError("expired")` is the rule. Custom errors inherit from a project root (`class AuthError extends AppError`), not directly from `Error`.
- **Never silent swallow**. `try { ... } catch (e) {}` is a quick-fix finding. Either log with context (`logger.error({ err, userId }, "fetch failed")`) or re-raise (possibly wrapped: `throw new AuthError(...) from err`). Pino or the platform `console.error` is acceptable; `console.log` is not.
- **Async paths use `try/catch` or `.catch`**. Unhandled promise rejections crash the process in Node 15+ and are a quick-fix finding; lint with `@typescript-eslint/no-floating-promises` and `no-misused-promises`.
- **Domain boundaries may use Result**. Functions that return `Result<T, E>` (`{ ok: true, value } | { ok: false, error }`) are allowed where callers must handle failure explicitly. Reserve for parsers, validators, and explicit "this can fail in expected ways" cases; do not sprinkle across the codebase.
- **Logging**: structured logger (Pino, winston) for servers; `console.error` is fine for CLI scripts. Library code never logs; the caller decides what to log.

Standardizer check: `grep -rEn "throw ['\"]" --include="*.ts" --include="*.tsx" .` returns empty (no string throws); `grep -rEn "catch \([^)]*\) \{\s*\}" --include="*.ts" --include="*.tsx" .` returns empty (no silent swallow); `@typescript-eslint/no-floating-promises` enabled in `eslint.config.js`.

## Comments

- **Explain why, not what**. Code says what; comments say why. A comment that restates the next line is dead prose.
- **`ponytail:` markers for deliberate shortcuts**. When the implementation takes a known-shorter path with a documented ceiling (global lock, O(n^2) scan, naive heuristic, missing strict null checks), add a one-line comment naming the shortcut and the upgrade path: `// ponytail: O(n^2) scan, switch to a Map when n > 1000`.
- **TODO format**: `TODO(ruben): ...` (owner in parentheses, colon, brief description). TODOs without an owner are anonymous debt; the standardizer flags them. Reference an issue or plan id when one exists: `// TODO(ruben): retire shim, see docs/artifacts/plans/...`.
- **What does not need a comment**: type annotations (no `// userId: string` next to `userId: string`); TSDoc already covers the function (no `// fetch the user` above the doc comment); standard-library calls (no `// open the file` above `fs.readFile(path)`).
- **Commented-out code is forbidden**. Delete it; git remembers.

Standardizer check: `grep -rEn "^\s*//" --include="*.ts" --include="*.tsx" . | grep -vE "ponytail:|TODO\([a-zA-Z0-9_-]+\):"` returns zero findings on new files; `grep -rEn "TODO[^(]" --include="*.ts" --include="*.tsx" .` (anonymous TODOs without an owner) returns empty.
