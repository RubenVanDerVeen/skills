# commit-msg Hook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. The orchestrator dispatches one `executor` per task and a `reviewer` after each; escalates two-strike failures to `oracle`.

**Goal:** Ship a tracked, dependency-free `commit-msg` git hook that rejects non-Conventional-Commits subjects, activate it for this clone, and wire it into the repo docs.

**Architecture:** A single POSIX `sh` hook at `.githooks/commit-msg` (regex via `grep`) plus a repo-root `.gitattributes` pinning `.githooks/**` to LF (shebang safety on Windows checkouts). Git runs it once `core.hooksPath = .githooks` is set (machine-local, documented in `opencode-install.md` step 10). No Node, no `package.json`, no `node_modules`.

**Tech Stack:** POSIX `sh`, `grep`, git hooks, PowerShell (verification only), Markdown (docs). Conventional Commits 1.0.0.

**Spec:** `docs/artifacts/specs/commitlint/2026-08-01-commit-msg-hook-design.md`

## Global Constraints

- No em-dashes (U+2014) anywhere. Verify after each task: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty for edited files. Use ASCII `->` or `>` in prose, never Unicode arrows.
- Conventional Commits 1.0.0. Per-task commits are sanctioned by the plan-execution carve-out; do not pause to ask.
- No tooling introduced. The hook is `sh` + `grep` only. Do NOT add `package.json`, `node_modules`, `.husky`, or any npm dependency. If a step seems to need one, stop and re-read the spec's Rejected alternatives.
- The hook file MUST be tracked executable (mode `100755`) and LF-only. Both are verified before the Task 1 commit.
- Today is 2026-08-01 for any dated artifact paths.
- Isolated verification lives under `C:\Users\ruben\AppData\Local\Temp\opencode` (pre-approved). Do not pollute the repo with sample commits; test in a throwaway temp git repo.

## File Structure

Committed source-of-truth:

- Create `.githooks/commit-msg` (POSIX sh hook, tracked executable, LF).
- Create `.gitattributes` (repo root, one directive: `.githooks/** text eol=lf`).
- Modify `opencode-install.md` (append step 10 "Enable the commit-msg hook").
- Modify `AGENTS.md` `## Git & workflow` (reconcile type list + add enforcement bullet).
- Modify `STANDARDS.md` (add `revert` to types, add enforcement line, extend layout tree).
- Modify `CHANGELOG.md` (Unreleased / Added entry).

Machine-local (not committed):

- `git config core.hooksPath .githooks` (writes `.git/config`).
- `git update-index --chmod=+x .githooks/commit-msg` (stages mode bit into the Task 1 commit).

---

### Preflight: branch + commit the spec and plan

Follow `/execute-plan` conventions. Before Task 1:

- [ ] **Step 0a: Branch.** Run `git rev-parse --abbrev-ref HEAD`. If it returns `main`/`master`, create and switch to `feat/commit-msg-hook`. Re-run `git branch --show-current`; do not proceed until off the default branch.
- [ ] **Step 0b: First commit (artifacts).** `git add` the spec and this plan, then:
  ```powershell
  git commit -m "docs: add plan and spec for commit-msg-hook"
  ```
  Note: this commit is made BEFORE the hook exists, so it is not yet hook-enforced. That is expected; every subsequent task commit IS enforced (Task 1 activates the hook first).

---

### Task 1: Create, activate, and verify the hook

**Files:**
- Create: `.githooks/commit-msg`
- Create: `.gitattributes`

**Depends on:** Preflight. **Affects:** every later commit (all go through the live hook); Task 2 docs.

- [ ] **Step 1: Write the hook.** Create `.githooks/commit-msg` with EXACTLY this content (LF line endings; the `write` tool writes bytes as given, so no CRLF is introduced):

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

- [ ] **Step 2: Write `.gitattributes`.** Create `.gitattributes` at the repo root with EXACTLY:

```
.githooks/** text eol=lf
```

- [ ] **Step 3: Activate the hook for this clone (machine-local).** Run:

```powershell
git config core.hooksPath .githooks
git config --get core.hooksPath
```

Expected output of the second command: `.githooks`.

- [ ] **Step 4: Stage and set the executable bit.** Run:

```powershell
git add .githooks/commit-msg .gitattributes
git update-index --chmod=+x .githooks/commit-msg
```

- [ ] **Step 5: Verify mode and line endings.** Run both:

```powershell
git ls-files -s .githooks/commit-msg
git ls-files --eol .githooks/commit-msg
```

Expected: first command shows mode `100755` (NOT `100644`). Second command shows `i/lf` and `w/lf` (index and working tree both LF; no `crlf`). If mode is `100644`, re-run Step 4's `git update-index --chmod=+x` and re-check. If eol shows `crlf`, run `git add --renormalize .githooks/commit-msg` and re-check.

- [ ] **Step 6: Verify the hook logic through git's real path (isolated temp repo).** Run this whole block; it builds a throwaway git repo under the pre-approved temp dir, copies the hook in, and feeds sample messages:

```powershell
$tmp = Join-Path $env:TEMP 'opencode\hook-test'
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "$tmp\.githooks" | Out-Null
Copy-Item '.githooks\commit-msg' "$tmp\.githooks\commit-msg"
git init -q "$tmp"
git -C "$tmp" config core.hooksPath .githooks
git -C "$tmp" config user.email "t@t"
git -C "$tmp" config user.name "t"

function Try-Commit([string]$msg) {
  git -C "$tmp" commit --allow-empty -q -m "$msg" 2>$null
  if ($LASTEXITCODE -eq 0) { "PASS(committed): $msg" } else { "REJECT:         $msg" }
}

Try-Commit 'feat(skills): add commitlint hook'   # expect PASS
Try-Commit 'fix: correct a typo'                 # expect PASS (no scope)
Try-Commit 'feat!: break the thing'              # expect PASS (breaking marker)
Try-Commit 'updated stuff'                       # expect REJECT (no type)
Try-Commit 'Feature: capital type'               # expect REJECT (case mismatch)
Try-Commit 'Merge branch x into main'            # expect PASS (skip)
Try-Commit 'Revert "previous"'                   # expect PASS (skip)

"--- accepted commits (expect 5) ---"
git -C "$tmp" log --oneline
```

Expected counts: **5 PASS(committed)** (`feat(skills): add commitlint hook`, `fix: correct a typo`, `feat!: break the thing`, `Merge branch x into main`, `Revert "previous"`) and **2 REJECT** (`updated stuff`, `Feature: capital type`). `git log --oneline` shows exactly **5 commits**. If the counts differ, the regex is wrong: re-read the spec's regex, fix the hook, re-run Steps 4-6.

- [ ] **Step 7: Commit (this commit goes through the LIVE hook in the main repo).** Run:

```powershell
git add .githooks/commit-msg .gitattributes
git commit -m "feat: add commit-msg hook enforcing Conventional Commits 1.0.0"
```

Expected: commit succeeds (the message is valid; the hook is now active in this clone, so this is the first real enforcement). If the hook rejects this message, the message itself is malformed and must be fixed, not bypassed with `--no-verify`.

- [ ] **Step 8: Reviewer gate.** Dispatch the `reviewer` against `.githooks/commit-msg` + `.gitattributes` + the verification output. Acceptance: hook content matches the spec verbatim, mode `100755`, LF confirmed, 5 PASS / 2 REJECT observed.

---

### Task 2: Wire the hook into the repo docs

**Files:**
- Modify: `opencode-install.md` (append step 10, before `## Verify`)
- Modify: `AGENTS.md` (`## Git & workflow`, line 180)
- Modify: `STANDARDS.md` (types list line 73, new enforcement line after the Scope paragraph ~line 83, layout tree ~lines 107-109)
- Modify: `CHANGELOG.md` (Unreleased / Added, after line 26)

**Depends on:** Task 1 (hook exists and is active, so this task's commit exercises it live). **Affects:** nothing downstream.

- [ ] **Step 1: `opencode-install.md` - add step 10.** Find the line `## Verify` (around line 128). Insert this new section immediately BEFORE `## Verify`:

```markdown
### 10. Enable the commit-msg hook

This repo ships a tracked `commit-msg` git hook (`.githooks/commit-msg`) that rejects non-Conventional-Commits messages, so agent-made and manual commits stay compliant. Git does not run hooks from a tracked directory until you point `core.hooksPath` at it. One-time per clone:

```
git config core.hooksPath .githooks
```

The hook is `sh` + `grep` only (no Node, no dependencies) and is tracked executable, so it works on Windows (via Git's bundled bash), macOS, and Linux. Emergency bypass: `git commit --no-verify`.
```

- [ ] **Step 2: `AGENTS.md` - reconcile types and add enforcement.** In `## Git & workflow`, replace this line:

```
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`). `chore:`, `docs:`, `feat:`, `fix:`, `refactor:` are the common types.
```

with:

```
- Commit messages: Conventional Commits 1.0.0 (`<type>(<scope>): <description>`). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Enforced by a tracked `commit-msg` hook (`.githooks/commit-msg`); activate once per clone with `git config core.hooksPath .githooks` (see `opencode-install.md` step 10). Bypass: `git commit --no-verify`.
```

- [ ] **Step 3a: `STANDARDS.md` - add `revert` to the type list.** Replace:

```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`.
```

with:

```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
```

- [ ] **Step 3b: `STANDARDS.md` - add the enforcement line.** Immediately AFTER the existing Scope paragraph (the one ending "...(`typst-pro`, `drawio-pro`, `readme`, `agents`).") and BEFORE the `---` separator, add:

```
Enforcement: a tracked `commit-msg` hook (`.githooks/commit-msg`) rejects non-conforming subjects. Activate once per clone: `git config core.hooksPath .githooks` (see `opencode-install.md` step 10).
```

- [ ] **Step 3c: `STANDARDS.md` - extend the layout tree.** Find these lines in the Repository layout block:

```
├── docs/                                  <- workflow notes and artifacts
├── .gitignore
├── .claude/                               <- Claude Code tool settings (project)
```

Replace with:

```
├── docs/                                  <- workflow notes and artifacts
├── .gitattributes                         <- forces LF on .githooks/* (shebang safety)
├── .gitignore
├── .githooks/
│   └── commit-msg                         <- Conventional Commits enforcement hook
├── .claude/                               <- Claude Code tool settings (project)
```

- [ ] **Step 4: `CHANGELOG.md` - add the Unreleased/Added entry.** Under `## [Unreleased]` -> `### Added`, immediately AFTER the existing single-pass `/full-cycle` bullet (the one ending "...Spec: `docs/artifacts/specs/single-pass-full-cycle/2026-07-30-single-pass-full-cycle-design.md`."), add:

```
- `commit-msg` git hook (`.githooks/commit-msg`): enforces Conventional Commits 1.0.0 on commit subjects with no dependencies (sh + grep). Tracked executable; activate per clone via `git config core.hooksPath .githooks` (documented in `opencode-install.md` step 10). A repo-root `.gitattributes` pins `.githooks/**` to LF so the shebang survives Windows checkouts. Replaces the npm `@commitlint/cli` + husky approach the repo's "no tooling" principle rules out. Spec: `docs/artifacts/specs/commitlint/2026-08-01-commit-msg-hook-design.md`.
```

- [ ] **Step 5: Em-dash + heading check.** Run:

```powershell
Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014)
```

Expected: no output (empty). If any match appears in a file this task edited, remove the em-dash and re-run. Confirm no top-level `## Skill` heading was introduced anywhere.

- [ ] **Step 6: Read-back the four edits.** Spot-check each modified file shows the new content and rendered correctly (code fences intact, no broken table borders). Fix any rendering issue.

- [ ] **Step 7: Commit (through the live hook).** Run:

```powershell
git add opencode-install.md AGENTS.md STANDARDS.md CHANGELOG.md
git commit -m "docs: wire commit-msg hook into install, standards, agents, changelog"
```

Expected: succeeds (valid message). If rejected, fix the message, do not bypass.

- [ ] **Step 8: Reviewer gate.** Dispatch the `reviewer` against the four doc edits. Acceptance: all four edits match the spec's Required changes, types reconciled to the 11-type set in both `AGENTS.md` and `STANDARDS.md`, layout tree shows `.gitattributes` + `.githooks/commit-msg`, no em-dashes, CHANGELOG entry present.

---

## Final report (orchestrator)

After Task 2 passes its reviewer gate, stop. Do NOT merge, open a PR, or invoke branch-finishing unless the user asks. Report:

- Branch name (`feat/commit-msg-hook`).
- Commits with hashes and one-line descriptions (expect: the artifacts commit, Task 1 hook commit, Task 2 docs commit).
- Files changed with diff stats.
- Verification output: the 5 PASS / 2 REJECT sample table, `git ls-files -s` showing `100755`, `git ls-files --eol` showing `i/lf w/lf`.
- The hook's `ponytail:` ceiling noted (no standing test; re-verify by hand if the regex changes).
- Anything Unverified or Deferred.
- A one-line reminder for the user: on any other clone of this repo, run `git config core.hooksPath .githooks` once to enable the hook (machine-local, not committed).
