# code-standardization Foundation Plan

## References

- Spec: `docs/artifacts/features/code-standardization/2026-08-04-foundation-design.md`
- Outline: `docs/artifacts/features/code-standardization/2026-08-04-code-standardization-outline.md`

## Branch

`feat/code-std`, created from current base. All foundation work lands here.

## Conventions

Conventional Commits per task. `feat(skills):` for the skill scaffolding and references; `feat(agents):` for the standardizer edit; `feat(commands):` for the command; `docs(skills):` for catalog rows. Ponytail active (full): no speculative content, no boilerplate sections, each file only what the spec names.

---

## Task F1: Scaffold the skill skeleton

Create `skills/code-standardization/` with `SKILL.md`.

- Frontmatter `name: code-standardization`, `description:` exactly as in spec § "Skill identity".
- Body sections per spec § "`SKILL.md` body structure": Overview, The 4 agent checks, The per-language guides (dispatch table with 5 rows, each row linking to the *planned* `references/<lang>.md` even though the files don't exist yet, link will resolve after SPs), Cross-language references (links to `references/tooling.md` and `references/architecture.md`), How the standardizer uses this skill, Commands (pointing to `commands/standardize-code.md` with the sync pattern table), Anti-patterns.
- Target <120 lines.
- The dispatch table rows: Python → `references/python.md`, TypeScript/JavaScript → `references/typescript-javascript.md`, C/C++ → `references/c-cpp.md`, Go → `references/go.md`, Rust → `references/rust.md`.

**Verify**: frontmatter `name` is kebab-case and matches folder; description starts "Use when..."; no em-dashes; body starts with `## Overview`; the file is <2k tokens.

**Commit**: `feat(skills): scaffold code-standardization skill skeleton`

---

## Task F2: Write `references/tooling.md`

Cross-language standardization-infra reference per spec § "`references/tooling.md`".

- The three-piece kit (formatter / linter / import sorter).
- Config discovery table (one row per language: Python, TS/JS, C/C++, Go, Rust).
- Hook wiring patterns (pre-commit framework, husky+lint-staged, native `.githooks/`).
- The "pin it" rule.
- The "don't re-implement the tool in the agent" rule.

**Verify**: no em-dashes; every language in the dispatch table has a config-discovery row; links to the per-language guides use the exact filenames from the dispatch table.

**Commit**: `feat(skills): add cross-language tooling reference`

---

## Task F3: Write `references/architecture.md`

Cross-language boundary reference per spec § "`references/architecture.md`".

- Layering and canonical dependency direction.
- No circular dependencies + the per-language arch tool (named, one line each).
- Feature/module isolation.
- Boundary spec: where it lives, what the agent checks vs. what the tool checks.

**Verify**: no em-dashes; the per-language arch-tool names are consistent with what each SP will specify (Python: `import-linter`; TS/JS: `dependency-cruiser`; C/C++: include-guard discipline + include-what-you-use; Go: layering linters; Rust: clippy module rules).

**Commit**: `feat(skills): add cross-language architecture reference`

---

## Task F4: Widen the `standardizer` agent

Edit `agents/standardizer.md` per spec § "Standardizer agent edit".

- Append to `description`: the code-standardization load + merged audit + code-structure scope sentence. Keep under the 1024-char frontmatter limit; trim if needed.
- In the body, after the repo-structure audit paragraph, add the code-structure audit paragraph (load `code-standardization`, 4 agent checks per language in the diff, run pinned tool in check mode if installed else quick-fix finding, same PASS/findings format).

**Verify**: `opencode agent list` parses (if the CLI is available; else validate YAML frontmatter by eye); no em-dashes; description still starts with the existing lead-in (the standardizer is still the repo-structure auditor, now also code-structure).

**Commit**: `feat(agents): widen standardizer to audit code structure`

---

## Task F5: Add the `/standardize-code` command

Create `commands/standardize-code.md` per spec § "Command file".

- Frontmatter `description:` only (no `name`).
- Body: load `code-standardization`, run the 4 agent checks against `$ARGUMENTS` (a path or language, optional; defaults to current branch diff), report PASS or numbered findings.

**Verify**: filename is `standardize-code.md`; frontmatter has `description` only; no em-dashes; body references loading the skill, not reimplementing it.

**Commit**: `feat(commands): add standardize-code slash command`

---

## Task F6: Update catalogs

Per repo `AGENTS.md` "Adding or modifying a skill" rules, the new skill must land in every catalog in the same commit.

- `README.md` `## Skills` table: add one row for `code-standardization` (alphabetical order).
- `AGENTS.md` `## Current skills` table: add one row for `code-standardization` (alphabetical order).
- Both rows: folder `skills/code-standardization/`, frontmatter name `code-standardization`, one-line "what it does".

**Verify**: both tables have the row; the folder name, frontmatter `name`, and table entries match exactly; no em-dashes; no other catalog drift introduced.

**Commit**: `docs(skills): catalog code-standardization skill`

---

## Task F7: Foundation verification

Run the repo's standard checks against the new files.

- Em-dash scan over the new/changed files returns empty.
- Frontmatter validity (name kebab-case, description starts "Use when...", <1024 chars).
- `SKILL.md` has `## Commands` section.
- Catalog cross-check: skill folder, frontmatter name, README row, AGENTS row all identical strings.
- `SKILL.md` token budget (<2k).
- The 5 per-language `references/<lang>.md` files do NOT exist yet (they belong to SP-1..SP-5); the SKILL.md links to them are intentional forward links.

**Commit**: none (verification only). If fixes are needed, fold them into the originating task's commit with `--amend` (single-pass; no separate fixup commit).

---

## Definition of done

All F1-F7 committed on `feat/code-std`. SKILL.md, both cross-language references, the standardizer edit, the command, and both catalog rows land together. The frozen 8-section template in the spec is the contract SP-1..SP-5 will consume. The 5 per-language reference files are intentionally absent.
