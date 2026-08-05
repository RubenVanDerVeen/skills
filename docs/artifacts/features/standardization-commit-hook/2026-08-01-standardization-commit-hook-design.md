# Bake the commit-msg hook into project-standardization

Date: 2026-08-01
Status: approved (single-pass run, no gate)

## Goal

Make every project bootstrapped or restructured by the `project-standardization` skill ship and activate the same dependency-free `commit-msg` hook this skills repo now uses, so newly-initialized projects enforce Conventional Commits 1.0.0 from their first commit. The hook is one of the skill's templates; the bootstrap checklist installs and activates it. The enforcer itself already exists (this repo's `.githooks/commit-msg`); this spec is about distribution through the skill, not re-designing the hook.

## Context (current state, 2026-08-01)

- This repo's `.githooks/commit-msg` (sh + grep, no deps) was just shipped and is active via `core.hooksPath = .githooks`, with `.gitattributes` pinning `.githooks/**` to LF. Spec: `docs/artifacts/specs/commitlint/2026-08-01-commit-msg-hook-design.md`.
- The `project-standardization` skill already ships one executable hook template: `templates/post-commit-graphify` (debounced graph refresh). It is applied by `references/bootstrap.md` step 10.3: "copy `templates/post-commit-graphify` to `.git/hooks/post-commit` (keep the executable bit on POSIX)". That hook installs to `.git/hooks/` (untracked, per-clone).
- The skill structure: `SKILL.md` (body with Templates + References tables), `references/{bootstrap,small,medium,large,standards-stack,artifacts,memory,todolist,tool-filenames,migration}.md`, `templates/{AGENTS-small,AGENTS-medium,AGENTS-large,CLAUDE,STANDARDS,CHANGELOG,todolist}.md` + `templates/post-commit-graphify`.
- The three `AGENTS-*.md` templates each have a Git section. All three contain the line `- Commit messages: Conventional Commits 1.0.0 (\`<type>(<scope>): <description>\`).` (small: `## Git & workflow`, line 51; medium: `## Git & Workflow`, line 21; large: `## Git & Workflow`, line 49).
- `templates/STANDARDS.md` has a `## Commit messages: Conventional Commits 1.0.0` section whose type list (line 73) is the 10-type set missing `revert` (same gap this repo's own STANDARDS had before today's edit).
- `references/bootstrap.md` is an 11-step checklist. Step 10 = graphify, step 11 = verify. The "For a restructure rather than fresh bootstrap" note (line 26) says "skip steps that already exist, but still create task-list items so gaps are visible", so a restructure picks up any new step automatically.
- `references/migration.md` covers Claude→AGENTS content relocation only; it does not enumerate bootstrap steps. The hook flows through the bootstrap checklist on any fresh bootstrap or restructure; migration.md needs no change.
- The tier references (`small.md` / `medium.md` / `large.md`) describe directory layout and which AGENTS sections to include; they do not enumerate per-file creation (graphify is not enumerated there either). They need no change.
- Catalogs (`README.md`, `AGENTS.md` Current skills table) describe what the skill does, not its template inventory. Adding a template does not change the skill's identity; no catalog row change.
- `/standardize` (`commands/standardize.md`) already instructs "apply the full bootstrap checklist", so the new step is picked up with no command edit.

## Decisions (locked with user)

1. **Install pattern: tracked `.githooks/` + `core.hooksPath` + `.gitattributes` LF pin** (Approach A). Matches what this repo just shipped. The hook travels with the repo, so every clone gets enforcement after a one-time `git config core.hooksPath .githooks`. Rejected: Approach B (`.git/hooks/`, matches graphify but not shared across clones, undermines enforcement on team projects). Rejected: Approach C (unify graphify to `.githooks/` too) as scope creep that rewrites a working flow.
2. **All tiers, always-on.** Conventional Commits is already part of the skill's standards floor that every project adopts. The hook is default-on like `STANDARDS.md`, not conditional like graphify.
3. **Skip only when there is no `.git`** (sub-project). Otherwise moot.
4. **One canonical hook script.** `templates/commit-msg` is byte-identical to this repo's `.githooks/commit-msg`. The repo's instance and the template are kept in sync manually; no tooling is added to enforce that (YAGNI).
5. **New bootstrap step 10**, graphify bumps to 11, verify to 12. Kept as its own step (a reviewer can accept/reject the hook install independently of STANDARDS or graphify); not folded into another step.
6. **Divergence from graphify is intentional** and documented in bootstrap.md: graphify = local-cache tooling -> `.git/hooks/`; commit policy = shared -> tracked `.githooks/`. Not unified now.
7. **No catalog row change, no command change, no tier-reference change, no migration.md change.** The template + bootstrap step + AGENTS/STANDARDS template mentions + SKILL.md table are the full surface.

## Design

### New template: `templates/commit-msg`

A flat file in `templates/` (matching `templates/post-commit-graphify`'s placement; no `hooks/` subdir). Content is byte-identical to this repo's `.githooks/commit-msg` (the canonical script shipped earlier today). The plan reproduces it verbatim and the verification step diffs the two files to prove they match.

### New bootstrap step 10 (in `references/bootstrap.md`)

Insert between current step 9 (STANDARDS) and current step 10 (graphify). Graphify renumbers 10 -> 11, verify 11 -> 12. New step text:

```markdown
10. **Install the commit-msg hook** (all tiers; default yes; skip only when the project has no `.git`). Enforces Conventional Commits 1.0.0 on every commit subject, agent-made or manual. Different install target from the graphify hook: this one is shared policy that travels with the repo, so it uses a tracked `.githooks/` dir (graphify is local-cache tooling and stays in `.git/hooks/`).
    1. Copy `templates/commit-msg` to `.githooks/commit-msg` in the project.
    2. Create `.gitattributes` at the project root with one line: `.githooks/** text eol=lf` (keeps the `#!/bin/sh` shebang valid on Windows checkouts).
    3. Stage as executable: `git add .githooks/commit-msg .gitattributes` then `git update-index --chmod=+x .githooks/commit-msg`.
    4. Activate for this clone: `git config core.hooksPath .githooks`. Machine-local (`.git/config`); each clone repeats this one line to enable the hook.
    The hook is `sh` + `grep` only (no Node, no deps). Emergency bypass: `git commit --no-verify`.
```

### AGENTS template Git sections (3 files)

In each of `templates/AGENTS-small.md`, `templates/AGENTS-medium.md`, `templates/AGENTS-large.md`, immediately after the existing line:

```
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`).
```

add a fixed (non-placeholder) bullet:

```
- Commits are enforced by a tracked `commit-msg` hook (`.githooks/commit-msg`); activate per clone with `git config core.hooksPath .githooks`. Bypass: `git commit --no-verify`.
```

### `templates/STANDARDS.md`

- Line 73 type list: add `revert`. `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build` -> add `, \`revert\`` so the full 11-type set matches the hook.
- After the Scope paragraph (line 83, ending "...`feat(remote-controller)` not `feat(electrical)`.") and before the `---` separator, add:

```
Enforcement: a tracked `commit-msg` hook (`.githooks/commit-msg`) rejects non-conforming subjects. Activate once per clone: `git config core.hooksPath .githooks` (installed by the `project-standardization` bootstrap, step 10).
```

### `SKILL.md`

- Templates table: add a row for `templates/commit-msg` (place it near `templates/post-commit-graphify`):
  `| \`templates/commit-msg\` | Conventional Commits 1.0.0 enforcement hook (sh + grep, no deps). Copy to \`.githooks/commit-msg\`; see bootstrap step 10. |`
- References table, `bootstrap.md` row (line 58): change "11-step" to "12-step" and extend the summary chain: "(triage -> AGENTS.md -> `.agents/` -> artifacts -> memory -> CHANGELOG -> STANDARDS -> **commit hook** -> graphify -> verify)".
- "Standards stack: the floor" section, Conventional Commits bullet (line 31): append "; enforced by the `commit-msg` hook installed in bootstrap step 10".

## Required changes

Committed source-of-truth edits (all under `skills/rubens-project-standardization/`):

- Create `templates/commit-msg` (byte-identical to repo's `.githooks/commit-msg`).
- Modify `references/bootstrap.md` (insert step 10, renumber 10->11 and 11->12).
- Modify `SKILL.md` (Templates table row, References table "12-step" + chain, Standards-stack enforcement note).
- Modify `templates/AGENTS-small.md` (Git section enforcement bullet).
- Modify `templates/AGENTS-medium.md` (Git section enforcement bullet).
- Modify `templates/AGENTS-large.md` (Git section enforcement bullet).
- Modify `templates/STANDARDS.md` (add `revert`; enforcement line).

No changes to: `README.md`, `AGENTS.md` (repo root), `commands/standardize.md`, the tier references, `references/migration.md`, the catalogs.

## Verification

1. **Byte-identity:** `git diff --no-index .githooks/commit-msg skills/rubens-project-standardization/templates/commit-msg` returns no diff (the two files are identical).
2. **Template works:** run the same 5 PASS / 2 REJECT sample-message suite from the earlier plan against `skills/rubens-project-standardization/templates/commit-msg` in a throwaway temp git repo. Expect identical results.
3. **End-to-end bootstrap smoke test:** under `C:\Users\ruben\AppData\Local\Temp\opencode\std-smoke`, `git init` a temp project and execute the four sub-steps of new bootstrap step 10 using the template file. Then feed sample commits through the real hook path: `feat: ok` accepted, `bad message` rejected. Proves the bootstrap instructions actually produce a working, activated hook.
4. **Numbering:** `references/bootstrap.md` has exactly 12 numbered top-level steps; `SKILL.md` References table says "12-step".
5. **Em-dash audit:** `(Get-ChildItem -Recurse -Include *.md skills\rubens-project-standardization | Select-String -Pattern ([char]0x2014))` returns empty for edited files.

## Out of scope (YAGNI)

- Unifying the graphify hook onto tracked `.githooks/` (Approach C). Would rewrite a working flow; defer until there's a reason.
- Tooling to auto-keep `templates/commit-msg` and the repo's `.githooks/commit-msg` in sync. Manual sync is fine for one 36-line file.
- A standing test suite for the hook (same ceiling as the repo hook: the 5/2 sample set is the manual verification).
- Changes to catalogs, the `/standardize` command, tier references, or `migration.md`. None needed; the template + bootstrap step + template mentions carry the feature.
- Folding the hook into any future "standardization CI bundle". Separate concern.
