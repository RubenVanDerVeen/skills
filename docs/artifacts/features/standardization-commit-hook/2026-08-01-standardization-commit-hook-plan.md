# Standardization commit-msg Hook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. The orchestrator dispatches one `executor` per task and a `reviewer` after each; escalates two-strike failures to `oracle`.

**Goal:** Make the `project-standardization` skill ship and activate the dependency-free `commit-msg` hook on every project it bootstraps, by adding a template + a bootstrap step and documenting it in the skill's templates and tables.

**Architecture:** Add `templates/commit-msg` (byte-identical copy of this repo's canonical `.githooks/commit-msg`). Add bootstrap step 10 "Install the commit-msg hook" to `references/bootstrap.md` (tracked `.githooks/` + `.gitattributes` LF pin + `--chmod=+x` + `core.hooksPath`); graphify -> 11, verify -> 12. Document enforcement in the three `AGENTS-*.md` template Git sections, the `STANDARDS.md` template, and `SKILL.md`'s tables. Same install pattern as this repo's own hook; intentionally divergent from the graphify hook (`.git/hooks/`, local-cache tooling).

**Tech Stack:** Markdown skill content, POSIX `sh` + `grep` hook, PowerShell (verification only). Conventional Commits 1.0.0. No Node, no build.

**Spec:** `docs/artifacts/features/standardization-commit-hook/2026-08-01-standardization-commit-hook-design.md`

## Global Constraints

- No em-dashes (U+2014) anywhere. This is the only character ban; Unicode arrows (→) are fine and are house style in `SKILL.md` / `bootstrap.md` tables. Verify after each task: `(Get-ChildItem -Recurse -Include *.md skills\rubens-project-standardization | Select-String -Pattern ([char]0x2014))` returns empty for edited files. When editing a table row that already uses →, keep → so the column stays consistent.
- Conventional Commits 1.0.0. Per-task commits are sanctioned by the plan-execution carve-out; do not pause to ask.
- No tooling introduced. The hook is `sh` + `grep` only. Do NOT add npm scripts, package.json, or any dependency anywhere in the skill.
- The template MUST be byte-identical to this repo's `.githooks/commit-msg`. Verify with `git diff --no-index .githooks/commit-msg skills\rubens-project-standardization\templates\commit-msg` (expect no output, exit 0).
- Today is 2026-08-01 for any dated artifact paths.
- Isolated verification lives under `C:\Users\ruben\AppData\Local\Temp\opencode` (pre-approved). Do not pollute the repo.

## File Structure

Committed source-of-truth edits (all under `skills/rubens-project-standardization/`):

- Create `templates/commit-msg` (copy of repo's `.githooks/commit-msg`).
- Modify `references/bootstrap.md` (insert step 10, renumber graphify 10->11, verify 11->12).
- Modify `SKILL.md` (Templates table row; References table "11-step" -> "12-step" + chain; Standards-stack enforcement note).
- Modify `templates/AGENTS-small.md`, `templates/AGENTS-medium.md`, `templates/AGENTS-large.md` (Git section enforcement bullet).
- Modify `templates/STANDARDS.md` (add `revert`; enforcement line).

Deliberately NOT modified (per spec): `README.md`, repo-root `AGENTS.md`, `commands/standardize.md`, tier references, `references/migration.md`, catalogs.

---

### Preflight: branch + commit the spec and plan

- [ ] **Step 0a: Branch.** Run `git rev-parse --abbrev-ref HEAD`. If it returns `main`/`master`, create and switch to `feat/standardization-commit-hook`. Re-run `git branch --show-current`; do not proceed until off the default branch. (Note: the repo's own `commit-msg` hook is already active on this clone from the earlier run, so every commit in this plan IS hook-enforced, including the preflight commit.)
- [ ] **Step 0b: First commit (artifacts).** `git add` the spec and this plan, then:
  ```powershell
  git commit -m "docs: add plan and spec for standardization-commit-hook"
  ```

---

### Task 1: Add the hook template and verify it

**Files:**
- Create: `skills/rubens-project-standardization/templates/commit-msg`

**Depends on:** Preflight. **Affects:** Task 2 (bootstrap step references this template).

- [ ] **Step 1: Copy the canonical hook into the template path.** Do NOT retype the script; copy the existing canonical file so byte-identity is guaranteed:

```powershell
Copy-Item '.githooks\commit-msg' 'skills\rubens-project-standardization\templates\commit-msg' -Force
```

For the reviewer's readability, the template's content is exactly this (source of truth: `.githooks/commit-msg`, shipped earlier today):

```sh
#!/bin/sh
# commit-msg hook: enforce Conventional Commits 1.0.0 on the subject line.
# ponytail: this is commitlint's job done with stdlib (git hooks + grep).
# Ceiling: no automated test; no config-conventional extras (subject-case,
# header-max-length, body-max-line-length). Re-verify with the sample messages
# in the plan/spec if the regex changes. Upgrade path: swap for @commitlint/cli
# + husky if those rule sets are needed (adds node_modules to this repo).

msg_file="$1"

# Subject = first line that is not blank and not a '#' comment.
subject=$(grep -vE '^[#[:space:]]*$' "$msg_file" | head -n 1)

# Skip git-internal messages we do not rewrite into Conventional Commits.
case "$subject" in
  "Merge "*|"Revert "*|"fixup! "*|"squash! "*) exit 0 ;;
esac

# Conventional Commits: <type>(<scope>)!: <description>
regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: .+'

if ! printf '%s\n' "$subject" | grep -qE "$regex"; then
  cat >&2 <<EOF
commit-msg: rejected, not Conventional Commits 1.0.0

  $subject

Expected: <type>(<scope>)!: <description>
Types:   feat fix docs style refactor perf test build ci chore revert
Scope:   optional, e.g. (skills)
Example: feat(skills): add commitlint hook

Bypass (emergencies only): git commit --no-verify
EOF
  exit 1
fi
```

- [ ] **Step 2: Verify byte-identity with the canonical hook.** Run:

```powershell
git diff --no-index .githooks/commit-msg skills/rubens-project-standardization/templates/commit-msg
"exit=$LASTEXITCODE"
```

Expected: no diff output, `exit=0`. If anything differs, delete the template and re-run Step 1.

- [ ] **Step 3: Verify the TEMPLATE works through git's real path (isolated temp repo).** Run this whole block; it builds a throwaway git repo under the pre-approved temp dir, copies the TEMPLATE file in, and feeds sample messages:

```powershell
$tmp = Join-Path $env:TEMP 'opencode\std-template-test'
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "$tmp\.githooks" | Out-Null
Copy-Item 'skills\rubens-project-standardization\templates\commit-msg' "$tmp\.githooks\commit-msg"
git init -q "$tmp"
git -C "$tmp" config core.hooksPath .githooks
git -C "$tmp" config user.email "t@t"
git -C "$tmp" config user.name "t"

function Try-Commit([string]$msg) {
  git -C "$tmp" commit --allow-empty -q -m "$msg" 2>$null
  if ($LASTEXITCODE -eq 0) { "PASS(committed): $msg" } else { "REJECT:         $msg" }
}

Try-Commit 'feat(skills): add commitlint hook template'   # expect PASS
Try-Commit 'fix: correct a typo'                          # expect PASS (no scope)
Try-Commit 'feat!: break the thing'                       # expect PASS (breaking marker)
Try-Commit 'updated stuff'                                # expect REJECT (no type)
Try-Commit 'Feature: capital type'                        # expect REJECT (case mismatch)
Try-Commit 'Merge branch x into main'                     # expect PASS (skip)
Try-Commit 'Revert "previous"'                            # expect PASS (skip)

"--- accepted commits (expect 5) ---"
git -C "$tmp" log --oneline
```

Expected counts: **5 PASS(committed)** and **2 REJECT**; `git log --oneline` shows exactly **5 commits**. If counts differ, the template is not byte-identical or the hook logic changed; re-run Steps 1-2.

- [ ] **Step 4: Commit (through the live repo hook).** Run:

```powershell
git add skills/rubens-project-standardization/templates/commit-msg
git commit -m "feat(skills): add commit-msg hook template to project-standardization"
```

Expected: succeeds (valid message; the repo's own hook is active on this clone and accepts it).

- [ ] **Step 5: Reviewer gate.** Dispatch the `reviewer` against the new template + the Step 2/3 output. Acceptance: template exists, byte-identical to `.githooks/commit-msg`, 5 PASS / 2 REJECT observed.

---

### Task 2: Wire the hook into the skill docs and smoke-test the bootstrap

**Files:**
- Modify: `skills/rubens-project-standardization/references/bootstrap.md`
- Modify: `skills/rubens-project-standardization/SKILL.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-small.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-medium.md`
- Modify: `skills/rubens-project-standardization/templates/AGENTS-large.md`
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md`

**Depends on:** Task 1 (template exists). **Affects:** nothing downstream.

- [ ] **Step 1: `bootstrap.md` - insert new step 10 and renumber.** The file currently has 11 steps: step 10 = graphify ("Wire the knowledge graph (graphify)"), step 11 = Verify. Make two edits:

  1. Renumber the existing graphify step heading from `10.` to `11.`, and the existing Verify step heading from `11.` to `12.`.
  2. Insert this new step BETWEEN current step 9 (`Add STANDARDS.md`) and the (now renumbered) graphify step:

```markdown
10. **Install the commit-msg hook** (all tiers; default yes; skip only when the project has no `.git`). Enforces Conventional Commits 1.0.0 on every commit subject, agent-made or manual. Different install target from the graphify hook: this one is shared policy that travels with the repo, so it uses a tracked `.githooks/` dir (graphify is local-cache tooling and stays in `.git/hooks/`).
    1. Copy `templates/commit-msg` to `.githooks/commit-msg` in the project.
    2. Create `.gitattributes` at the project root with one line: `.githooks/** text eol=lf` (keeps the `#!/bin/sh` shebang valid on Windows checkouts).
    3. Stage as executable: `git add .githooks/commit-msg .gitattributes` then `git update-index --chmod=+x .githooks/commit-msg`.
    4. Activate for this clone: `git config core.hooksPath .githooks`. Machine-local (`.git/config`); each clone repeats this one line to enable the hook.
    The hook is `sh` + `grep` only (no Node, no deps). Emergency bypass: `git commit --no-verify`.
```

- [ ] **Step 2: `SKILL.md` - Templates table.** In the `## Templates` table, immediately AFTER the existing `templates/post-commit-graphify` row, add:

```
| `templates/commit-msg` | Conventional Commits 1.0.0 enforcement hook (sh + grep, no deps). Copy to `.githooks/commit-msg`; see bootstrap step 10. |
```

- [ ] **Step 3: `SKILL.md` - References table + step count.** In the `## References` table, the `bootstrap.md` row currently reads:

```
| `references/bootstrap.md` | The 11-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS → graphify → verify) |
```

Replace with (note: `11-step` -> `12-step`, and `STANDARDS -> commit hook -> graphify` in the chain; keep the existing arrow character convention used elsewhere in that table):

```
| `references/bootstrap.md` | The 12-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS → commit hook → graphify → verify) |
```

- [ ] **Step 4: `SKILL.md` - Standards-stack enforcement note.** In the `## Standards stack: the floor` section, the Conventional Commits bullet currently reads:

```
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0**: `<type>(<scope>): <description>`; `CHANGELOG.md` grouped by version or sprint.
```

Replace with:

```
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0**: `<type>(<scope>): <description>`; `CHANGELOG.md` grouped by version or sprint. Commits are enforced by the `commit-msg` hook installed in bootstrap step 10.
```

- [ ] **Step 5: `AGENTS-small.md` - Git section enforcement bullet.** Find the line `- Commit messages: Conventional Commits 1.0.0 (\`<type>(<scope>): <description>\`).` (in `## Git & workflow`). Immediately AFTER it, add:

```
- Commits are enforced by a tracked `commit-msg` hook (`.githooks/commit-msg`); activate per clone with `git config core.hooksPath .githooks`. Bypass: `git commit --no-verify`.
```

- [ ] **Step 6: `AGENTS-medium.md` - Git section enforcement bullet.** Same edit as Step 5, in its `## Git & Workflow` section (note the capital W), after the same `Commit messages: Conventional Commits 1.0.0` line.

- [ ] **Step 7: `AGENTS-large.md` - Git section enforcement bullet.** Same edit as Step 5, in its `## Git & Workflow` section, after the same `Commit messages: Conventional Commits 1.0.0` line.

- [ ] **Step 8: `STANDARDS.md` template - add `revert` to the type list.** Find:

```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`.
```

Replace with:

```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
```

- [ ] **Step 9: `STANDARDS.md` template - add the enforcement line.** Immediately AFTER the existing Scope paragraph (ending "...`feat(remote-controller)` not `feat(electrical)`.") and BEFORE the `---` separator, add:

```
Enforcement: a tracked `commit-msg` hook (`.githooks/commit-msg`) rejects non-conforming subjects. Activate once per clone: `git config core.hooksPath .githooks` (installed by the `project-standardization` bootstrap, step 10).
```

- [ ] **Step 10: Em-dash audit on the skill subtree.** Run:

```powershell
Get-ChildItem -Recurse -Include *.md skills\rubens-project-standardization | Select-String -Pattern ([char]0x2014)
```

Expected: no output. If a match appears in a file this task edited, remove it and re-run. (Pre-existing em-dashes elsewhere in the repo are out of scope for this plan.)

- [ ] **Step 11: Verify step numbering.** Run:

```powershell
Select-String -Path skills\rubens-project-standardization\references\bootstrap.md -Pattern '^\d+\. '
```

Expected: 12 matches, numbered 1 through 12 in order, with `10.` = "Install the commit-msg hook", `11.` = graphify, `12.` = Verify. If numbering is off, fix it before committing.

- [ ] **Step 12: End-to-end bootstrap smoke test (isolated temp project).** Run this whole block; it executes the four sub-steps of the new bootstrap step 10 against the TEMPLATE, then proves the result enforces commits:

```powershell
$proj = Join-Path $env:TEMP 'opencode\std-smoke'
Remove-Item -Recurse -Force $proj -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "$proj\.githooks" | Out-Null

# 10.1 copy template
Copy-Item 'skills\rubens-project-standardization\templates\commit-msg' "$proj\.githooks\commit-msg"
# 10.2 .gitattributes LF pin
".githooks/** text eol=lf`n" | Set-Content -NoNewline "$proj\.gitattributes" -Encoding ascii

git init -q "$proj"
git -C "$proj" config user.email "t@t"
git -C "$proj" config user.name "t"
# 10.3 stage as executable
git -C "$proj" add .githooks/commit-msg .gitattributes
git -C "$proj" update-index --chmod=+x .githooks/commit-msg
# 10.4 activate
git -C "$proj" config core.hooksPath .githooks

# verify mode + eol
git -C "$proj" ls-files -s .githooks/commit-msg    # expect 100755
git -C "$proj" ls-files --eol .githooks/commit-msg # expect i/lf w/lf

# the scaffolding commit goes through the live hook; valid message -> accepted
git -C "$proj" commit -q -m "chore: bootstrap scaffolding"
"commit1 exit=$LASTEXITCODE (expect 0)"

# bad message -> rejected, no commit created
git -C "$proj" commit --allow-empty -q -m "bad message" 2>$null
"commit2 exit=$LASTEXITCODE (expect non-zero)"

"--- log (expect 1 commit) ---"
git -C "$proj" log --oneline
```

Expected: `commit1 exit=0`, `commit2 exit` non-zero, mode `100755`, `i/lf w/lf`, and the log shows exactly **1 commit**. This proves the bootstrap instructions as written produce a working, activated hook from the template.

- [ ] **Step 13: Read-back the edits.** Spot-check each modified file shows the new content and renders correctly (table rows aligned, code fences intact, no broken numbering). Fix any rendering issue.

- [ ] **Step 14: Commit (through the live repo hook).** Run:

```powershell
git add skills/rubens-project-standardization/references/bootstrap.md skills/rubens-project-standardization/SKILL.md skills/rubens-project-standardization/templates/AGENTS-small.md skills/rubens-project-standardization/templates/AGENTS-medium.md skills/rubens-project-standardization/templates/AGENTS-large.md skills/rubens-project-standardization/templates/STANDARDS.md
git commit -m "docs(skills): wire commit-msg hook into standardization bootstrap and templates"
```

Expected: succeeds. If the repo hook rejects this message, fix the message; do not bypass.

- [ ] **Step 15: Reviewer gate.** Dispatch the `reviewer` against the six doc edits + the Step 11 numbering output + the Step 12 smoke-test output. Acceptance: bootstrap has 12 steps with the hook at step 10; SKILL.md says "12-step" and lists the template; all three AGENTS templates carry the enforcement bullet; STANDARDS template has `revert` + the enforcement line; smoke test shows `commit1 exit=0` / `commit2` rejected / `100755` / `i/lf w/lf`; no em-dashes in edited files.

---

## Final report (orchestrator)

After Task 2 passes its reviewer gate, stop. Do NOT merge, open a PR, or invoke branch-finishing unless the user asks. Report:

- Branch name (`feat/standardization-commit-hook`).
- Commits with hashes and one-line descriptions (expect 3: the artifacts commit, the Task 1 template commit, the Task 2 docs commit).
- Files changed with diff stats.
- Verification evidence: the `git diff --no-index` byte-identity result (exit 0), the Task 1 template sample run (5 PASS / 2 REJECT), the Step 11 numbering (1-12), and the Task 2 Step 12 smoke-test output (`commit1 exit=0`, `commit2` rejected, `100755`, `i/lf w/lf`, 1 commit in log).
- The intentional divergence noted: graphify hook stays at `.git/hooks/` (step 11), commit-msg hook uses tracked `.githooks/` (step 10). Not unified.
- The `ponytail:` ceiling carried by the template (no standing test; manual sync with the repo's `.githooks/commit-msg`).
- Any Unverified or Deferred items.
- A one-line reminder: projects bootstrapped with this skill after the merge get the hook automatically; existing projects need a re-run of `/standardize` (restructure path) to pick up step 10.
