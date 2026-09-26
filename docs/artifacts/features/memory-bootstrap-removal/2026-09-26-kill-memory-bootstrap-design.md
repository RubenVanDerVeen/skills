# Design: remove the cross-session memory bootstrap from project-standardization

Date: 2026-09-26
Status: approved (user picked "kill the bootstrap" during brainstorm)

## Problem

The `project-standardization` skill seeds a `MEMORY.md` (plus optional typed memory files) into every project it bootstraps, but no mechanism ever loads it afterwards:

- Generated `AGENTS.md` templates contain zero memory references, so the auto-loaded context file never points at it.
- No agent definition in `agents/` reads or updates memory.
- opencode has no native memory directory (the skill's own tool table says so).
- The only read-policy ("When to access memory") lives in `references/memory.md`, a file agents open only during bootstrap.
- The skill's anti-pattern rule forbade pointing to memory from `AGENTS.md`, blocking the one loader that exists.

Result: orphaned files. Evidence: `/home/ruben/projects/Tools/klad/MEMORY.md` serves no purpose, and it is the only `MEMORY.md` across all standardized projects.

## Decision

Remove the memory mechanism from the skill entirely. No replacement mechanism.

- Durable project-stable facts already belong in `AGENTS.md` (auto-loaded).
- On-demand content already belongs in `.agents/` (the existing on-demand subdirectory, e.g. `.agents/todolist.md`).
- Cross-session memory stays out of scope until opencode grows a native memory feature. Revisit then.

User quote: "no memory at all. opencode shares this. only thing that agent should do is put on demand content in .agents/"

## Scope: deletions and edits

All paths relative to repo root `/home/ruben/projects/Tools/skills`.

1. **Delete** `skills/rubens-project-standardization/references/memory.md` (whole file).
2. **Edit** `skills/rubens-project-standardization/references/bootstrap.md`: remove step 7 ("Seed cross-session memory") and its verification predicate. Renumber later steps if they are numbered.
3. **Edit** `skills/rubens-project-standardization/references/small.md`, `medium.md`, `large.md`: remove each `## Memory` section.
4. **Edit** `skills/rubens-project-standardization/references/todolist.md`: remove the memory-vs-todolist disambiguation rows/lines (around lines 98-104).
5. **Edit** `skills/rubens-project-standardization/references/artifacts.md`: remove the "reviews are not memory" and "choices vs memory" disambiguation lines (around lines 160 and 243).
6. **Edit** `skills/rubens-project-standardization/SKILL.md`: remove the `references/memory.md` row from the references table and every memory mention in the body, including the frontmatter `description` phrase "seeding cross-session memory" (description change is an accepted breaking change; the trigger conditions must still read naturally). Also update step-number cross-references (hooks step 10 becomes step 9).
6a. **Edit** `skills/rubens-project-standardization/templates/STANDARDS.md`: "bootstrap, step 10" becomes "bootstrap, step 9" (renumbering fallout). The other templates contain no step references.
7. **Edit** `commands/standardize.md`: remove "memory" from the description line ("apply AGENTS.md, .agents/, docs/artifacts/, memory, CHANGELOG, STANDARDS").
8. **Edit** `skills/skill-harvest/SKILL.md`: remove the "suggest memory write" row from the harvest table (around line 26). Do not add a replacement target; `.agents/todolist.md` and AGENTS.md already exist as targets where relevant.
9. **Check** `README.md` and `AGENTS.md` (repo root): if the `project-standardization` row or any live guidance mentions cross-session memory or MEMORY.md, remove that wording. History mentions in `docs/artifacts/` stay untouched.

## Out of scope

- `/home/ruben/projects/Tools/klad/`: untouched per user choice. Known consequence: its `MEMORY.md` links to the deleted `references/memory.md` URL (dead link) and is never loaded. User cleans it up separately.
- `docs/artifacts/features/**` history documents: history stays as written.
- Installed copies under `~/.config/opencode/skills/`: repo is source of truth; the user re-copies manually (existing sync pattern, see AGENTS.md "Sync pattern").

## End state and verification

- `grep -ri "memory" skills/rubens-project-standardization/ commands/ README.md AGENTS.md agents/` returns no hits describing the memory mechanism. Unrelated English-word usage survives by design (e.g. `references/restructure-flow.md` line 7, "the verifying agent has no memory of what the patching agent did").
- No template under `skills/rubens-project-standardization/templates/` mentions memory (already true, verify only).
- Frontmatter still valid: `name` kebab-case, `description` starts with "Use when...", under 1024 chars, no em-dashes anywhere in the repo's markdown.
- Git hooks pass (`git config core.hooksPath .githooks` already active).

## Commit

Single commit, type `feat` (behavioral removal of a feature from the skill): `feat(standardization): remove unused cross-session memory bootstrap` or equivalent Conventional Commits message on a `feat/remove-memory-bootstrap` branch. Catalog rows only change wording if they mentioned memory; no new skill is added.
