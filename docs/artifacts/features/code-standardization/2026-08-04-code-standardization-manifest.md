# code-standardization Multi-Plan Manifest

## Plans

| ID | Name | Branch | Plan file | Spec file | Depends on | Status |
|----|------|--------|-----------|-----------|------------|--------|
| F  | Foundation | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-foundation-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-foundation-design.md` | - | ready |
| SP-1 | Python | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-sp1-python-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-sp1-python-design.md` | F complete | blocked on F |
| SP-2 | TS/JS | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-sp2-typescript-javascript-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-sp2-typescript-javascript-design.md` | F complete | blocked on F |
| SP-3 | C/C++ | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-sp3-c-cpp-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-sp3-c-cpp-design.md` | F complete | blocked on F |
| SP-4 | Go | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-sp4-go-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-sp4-go-design.md` | F complete | blocked on F |
| SP-5 | Rust | `feat/code-std` | `docs/artifacts/features/code-standardization/2026-08-04-sp5-rust-plan.md` | `docs/artifacts/features/code-standardization/2026-08-04-sp5-rust-design.md` | F complete | blocked on F |

## Frozen contract

The frozen per-language template (8 sections) is defined in `2026-08-04-foundation-design.md` § "Frozen per-language template". All five SPs instantiate it; none redefine the section set.

## Execution order

0. **Plan commit (first)**: the orchestrator commits these planning artifacts (specs + plans + this manifest) to `feat/code-std` as a single `docs:` commit before any implementation. Base branch is `main` (NOT the current `docs/workflow-docs-new-agents` branch, which carries unrelated in-progress workflow-docs work).

1. **F (foundation)** on `feat/code-std`. Branch from `main`. Commits land directly on `feat/code-std`. Per-task Conventional Commits.
2. **After F is complete and verified**: SP-1 through SP-5. Each SP writes exactly one new additive file (`references/<lang>.md`). No shared file is touched by more than one SP.
3. **Integration**: none required. The five SP outputs are independent additive files with zero overlap. The lean branch model (see outline § "Deviation note") lands all SPs directly on `feat/code-std`. Integration risk is zero; the foundation's SKILL.md dispatch-table links resolve once the files exist.
4. **Final**: `feat/code-std` merges to base (PR if the repo has a remote, local merge otherwise).

## Lean branch model (deviation from pure multi-plan)

Pure multi-plan-orchestration prescribes per-SP branches + worktrees + an integration merge pass. This run skips them because:
- Each SP output is a single new file with a unique path.
- No two SPs touch the same file.
- The foundation's SKILL.md forward-links to each SP file; those links resolve once each SP lands.
- There is no shared mutable state to merge-conflict over.

Per-SP plans and per-SP Conventional Commits are preserved (the coordination value), only the git ceremony is dropped.

## Per-unit dispatch instructions (for the orchestrator)

The orchestrator executes this manifest as a single runbook on `feat/code-std`, in order:

### Foundation (F)
- Branch: create `feat/code-std` from `main` (NOT from the current `docs/workflow-docs-new-agents` branch). The working tree currently has unrelated uncommitted changes under `docs/workflows/` and an untracked `docs/workflow-docs-new-agents` entry from another task. **Leave those alone. Stage only files under `docs/artifacts/features/code-standardization/`.**
- First commit: `docs(plans): add code-standardization specs, plans, and manifest` with the planning artifacts above.
- Read `docs/artifacts/features/code-standardization/2026-08-04-foundation-plan.md`; execute tasks F1-F7 with executor/reviewer per task; commit after every task with the Conventional Commit message each task names.
- Gate: do not start any SP until F1-F7 are complete and F7 verification is green.

### Sub-projects (SP-1 .. SP-5)
- Stay on `feat/code-std`. No new branches, no worktrees.
- Dispatch one executor per SP (parallel is fine; the files are independent). Each executor reads its `docs/artifacts/features/code-standardization/2026-08-04-spN-<lang>-plan.md` and writes exactly `skills/code-standardization/references/<lang>.md`.
- Each SP consumes the frozen template from `2026-08-04-foundation-design.md` § "Frozen per-language template"; it must NOT add, remove, or reorder sections.
- Reviewer checks each SP against its plan + the frozen template + em-dash scan.
- Commit per SP with the message its plan names.

### Final
- Run a repo-wide em-dash scan and a catalog cross-check (folder name = frontmatter name = README row = AGENTS row).
- Verify `feat/code-std` is clean and all 10 implementation files exist (SKILL.md, 2 cross-language refs, 5 lang guides, command, standardizer edit).
- Report status. Leave `feat/code-std` for the user to merge to base (or merge if instructed).

## Integration checklist (final)

- [ ] F1-F7 complete on `feat/code-std`.
- [ ] SP-1..SP-5 complete; all 5 `references/<lang>.md` files exist.
- [ ] Em-dash scan empty across all new/changed files.
- [ ] Catalog cross-check: `skills/code-standardization/` folder, `code-standardization` frontmatter name, `README.md` row, `AGENTS.md` row all identical.
- [ ] SKILL.md dispatch-table links all resolve.
- [ ] `standardizer.md` parses (`opencode agent list` or YAML eye-check).
- [ ] `commands/standardize-code.md` present, `description`-only frontmatter.
