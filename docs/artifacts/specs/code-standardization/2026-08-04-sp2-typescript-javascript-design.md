# SP-2 TypeScript/JavaScript Design

## Status

Sub-project of the code-standardization multi-plan. Depends on F complete. Consumes the frozen 8-section template.

## Goal

Write `skills/code-standardization/references/typescript-javascript.md` for the combined TS/JS guide (shared toolchain).

## Language-specific picks

- **Toolchain (§1):** Prettier (format, opinionated) + ESLint or oxlint (lint, pick one and pin). Import sort via `eslint-plugin-import` or oxlint's import rules. Config `eslint.config.js` (flat) or `.eslintrc.*` (legacy) + `.prettierrc`; pin via lockfile. Check `prettier --check . && eslint .`. Hook: husky + lint-staged, or pre-commit framework.
- **Naming (§2):** files `kebab-case.ts` for modules, `PascalCase.tsx` for React components; functions/variables `camelCase`; classes/interfaces/types `PascalCase` (interfaces no `I` prefix); constants `UPPER_SNAKE`; test files `*.test.ts` / `*.spec.ts`.
- **Module/file org (§3):** one default or primary export per module for components; named exports for utils; import order (builtin → external → internal → relative) enforced by lint; barrel files (`index.ts`) only at package boundaries.
- **Architecture (§4):** `dependency-cruiser` for layers and no-cycles; layers per project (e.g. `ui → features → data → lib`); features don't import each other's internals.
- **Documentation (§5):** TSDoc for TS public API (`/** ... */`), JSDoc for JS; document params, returns, thrown errors.
- **Testing (§6):** Vitest preferred (Jest acceptable); `*.test.ts` co-located; describe/it naming; mock at boundaries.
- **Error handling (§7):** throw `Error` subclasses; never swallow; async uses `try/catch` or Result at domain boundaries; no unhandled rejections.
- **Comments (§8):** explain why; `ponytail:` markers; `TODO(ruben): ...`.

Each section ends with the one-line "what the standardizer checks" note.

## Out of scope

Any other file. No SKILL.md edit.
