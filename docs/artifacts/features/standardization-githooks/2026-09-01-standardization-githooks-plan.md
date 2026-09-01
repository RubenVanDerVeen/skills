# Standardization Git Hooks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce the machine-checkable subset of the repo's standardization rules at commit time via a new `.githooks/pre-commit` hook, so agents cannot commit wrong docs. The existing `commit-msg` hook stays untouched.

**Architecture:** One new POSIX-sh `pre-commit` file containing checks P1..P7 as small functions (em-dash ban, SKILL.md frontmatter rules, catalog sync, forbidden paths), all validated against staged index content. Day-one scrub tasks remove the 25 existing violations first so the hook never fails on untouched files. Zero new dependencies; `sh` + `grep` + `sed` + `awk` + `git` plumbing only.

**Tech Stack:** POSIX sh (runs under Git for Windows' bundled bash), git plumbing (`diff --cached`, `show :path`, `cat-file`), grep/sed/wc. PowerShell 5.1 for the executor's shell commands; git itself invokes the hooks.

**Spec:** `docs/artifacts/features/standardization-githooks/2026-09-01-standardization-githooks-design.md`

## Global Constraints

- No new dependencies. No Node, no pre-commit framework, no Python. POSIX sh builtins + grep/sed/awk/wc + git only.
- No literal U+2014 byte may appear in ANY tracked file, ever, including code samples in this plan's commits and doc edits. Build em-dash bytes with `printf '\342\200\224'` (POSIX octal escapes).
- Hooks validate staged index content (`git show ":path"`), never the working tree.
- New/edited hook files must be LF and mode 100755: after every write/edit run the CRLF-normalization step, then `git update-index --chmod=+x <file>`. `.gitattributes` already pins `.githooks/**` to `text eol=lf`.
- Every rejection message ends with the bypass line: `Bypass (emergencies only): git commit --no-verify`.
- Checks report ALL violations (no early exit); hook exits 1 if any check failed.
- Word-splitting on path lists is a documented ceiling: safe because the kebab-case path rule bans spaces. Mark it with a `ponytail:` comment in each hook.
- All commits on this plan: Conventional Commits, per-task commits, feature branch `plan-standardization-githooks` off `main`.
- Do not "fix" unrelated drift (stale CHANGELOG paths, non-alphabetical catalog tables, reviews filename drift) while in these files; out of scope per spec.
- The repo bans em-dashes in chat output too: executor/reviewer communication must not use U+2014.

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `.githooks/pre-commit` | Create | Checks P1..P7 on staged files; exits 1 on any violation |
| `skills/deep-research/SKILL.md` | Modify (Task 1) | Remove 16 em-dashes |
| `skills/deep-research/templates/dossier-template.md` | Modify (Task 1) | Remove 1 em-dash |
| `docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-skill-artifacts-per-feature-cleanup-plan.md` | Modify (Task 1) | Remove 6 em-dashes |
| `docs/artifacts/reviews/2026-07-12-harvest.md` | Modify (Task 1) | Remove 1 em-dash |
| `skills/rubens-project-standardization/SKILL.md` | Modify (Task 2) | Add `## Overview` heading |
| `AGENTS.md`, `STANDARDS.md`, `opencode-install.md`, `CHANGELOG.md` | Modify (Task 5) | Document the hook set |

---

### Task 1: Scrub existing em-dashes (day-one fix)

**Files:**
- Modify: `skills/deep-research/SKILL.md` (16 hits: lines 147, 194, 204, 207, 222, 223, 236, 246, 255, 262, 302, 318, 322, 323, 502, 503)
- Modify: `skills/deep-research/templates/dossier-template.md` (1 hit: line 52)
- Modify: `docs/artifacts/features/skill-artifacts-per-feature-cleanup/2026-08-05-skill-artifacts-per-feature-cleanup-plan.md` (6 hits: lines 27, 40, 55, 68, 88, 101)
- Modify: `docs/artifacts/reviews/2026-07-12-harvest.md` (1 hit: line 80)

**Interfaces:**
- Consumes: nothing.
- Produces: a repo with zero U+2014 bytes in tracked `*.md`, prerequisite for check P1 going live.

- [ ] **Step 1: Locate every hit with line content**

Run (PowerShell, from repo root):

```powershell
Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014) | ForEach-Object { "$($_.Path):$($_.LineNumber): $($_.Line)" }
```

Expected: exactly the 24 hits listed above (line numbers may drift by a line or two; trust the scan, not the list).

- [ ] **Step 2: Replace each em-dash in context**

Read each listed line with the Read tool. Replace the U+2014 character only (never ASCII hyphens) with whichever of `, `, `: `, `(`...`)`, or ` - ` preserves the sentence's meaning. Typical patterns: `X - Y` separators become `X: Y` or `X, Y`. In the old plan doc, some hits may sit inside quoted shell commands or heredocs; still replace the em-dash character with a plain hyphen there, since those are prose quotes of a command that historically contained it.

- [ ] **Step 3: Verify zero hits repo-wide**

```powershell
(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014)).Count
```

Expected: `0`.

- [ ] **Step 4: Commit**

```powershell
git add -A
git commit -m "docs: scrub em-dashes from markdown files"
```

---

### Task 2: Add missing `## Overview` heading to project-standardization

**Files:**
- Modify: `skills/rubens-project-standardization/SKILL.md` (first lines)

**Interfaces:**
- Consumes: nothing.
- Produces: every `skills/*/SKILL.md` contains an `## Overview` heading, prerequisite for check P5.

- [ ] **Step 1: Fix the heading**

Read the first 10 lines. The file opens with `# Project standardization skill` followed by an intro paragraph. Replace the H1 line with `## Overview` (precedent: `skills/code-standardization/SKILL.md`, `skills/inventree-naming/SKILL.md`, and `skills/skill-harvest/SKILL.md` all start directly with `## Overview`; the frontmatter `name` carries the identity). Keep the intro paragraph text unchanged, directly under the new heading.

- [ ] **Step 2: Verify**

```powershell
Select-String -Path "skills\*\SKILL.md" -Pattern '^## Overview' -SimpleMatch:$false | Measure-Object | Select-Object -ExpandProperty Count
```

Expected: `10` (one per skill folder).

- [ ] **Step 3: Commit**

```powershell
git add skills/rubens-project-standardization/SKILL.md
git commit -m "docs(skills): add Overview heading to project-standardization"
```

---

### Task 3: Create `.githooks/pre-commit` (checks P1..P7)

**Files:**
- Create: `.githooks/pre-commit`

**Interfaces:**
- Consumes: repo rules from `AGENTS.md` (em-dash ban, frontmatter rules, catalog sync, forbidden dirs).
- Produces: `.githooks/pre-commit`, executable, POSIX sh. Task 4's verification matrix depends on the exact `reject` message format (`pre-commit: rejected by <check>`) and the check ids `P1`..`P7` used below.

- [ ] **Step 1: Write the hook**

Create `.githooks/pre-commit` with exactly this content:

```sh
#!/bin/sh
# pre-commit hook: enforce repo doc standards on staged files.
# Checks P1..P7 per docs/artifacts/features/standardization-githooks/ design.
# ponytail: eight grep checks, no dependencies. Ceiling: validates staged
# content only, word-splits path lists (safe: kebab-case rule bans spaces in
# paths), and treats a repo's very first commit as a new-skill commit.
# Re-verify with the matrix in the feature plan if a check changes.

staged=$(git diff --cached --name-only --diff-filter=ACMR)
fail=0

reject() {
  printf 'pre-commit: rejected by %s\n  file: %s\n  rule: %s\n' "$1" "$2" "$3" >&2
  fail=1
}

# U+2014 as UTF-8 bytes; octal escapes are POSIX, no literal char in this file.
EM_DASH=$(printf '\342\200\224')

# SKILL.md checks (P2 name, P3 description, P4 size, P5 headings).
check_skill_md() {
  f=$1
  content=$(git show ":$f")
  first=$(printf '%s\n' "$content" | head -n 1)
  if [ "$first" != "---" ]; then
    reject "P2 frontmatter" "$f" "SKILL.md must start with YAML frontmatter (---)"
    return
  fi
  fm=$(printf '%s\n' "$content" | sed -n '2,/^---$/p' | sed '$d')

  name=$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -n 1)
  folder=$(basename "$(dirname "$f")")
  if [ -z "$name" ]; then
    reject "P2 name" "$f" "missing name in frontmatter"
  else
    if ! printf '%s\n' "$name" | grep -qE '^[a-z0-9-]+$'; then
      reject "P2 name" "$f" "name '$name' must be kebab-case (letters, digits, hyphens only)"
    fi
    if [ "$name" != "$folder" ]; then
      case "$f" in
        # Sanctioned legacy exception (AGENTS.md: backwards compatibility).
        skills/rubens-project-standardization/*) ;;
        *) reject "P2 name" "$f" "name '$name' must match folder '$folder'" ;;
      esac
    fi
  fi

  desc=$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -n 1)
  desc=${desc#\"}
  case "$desc" in
    "Use when"*) ;;
    *) reject "P3 description" "$f" "description must start with 'Use when'" ;;
  esac

  fm_len=$(printf '%s' "$fm" | wc -c)
  if [ "$fm_len" -gt 1024 ]; then
    reject "P4 frontmatter-size" "$f" "frontmatter is $fm_len bytes (max 1024)"
  fi

  if printf '%s\n' "$content" | grep -qE '^## Skill[[:space:]]*$'; then
    reject "P5 skill-heading" "$f" "no top-level '## Skill' heading; body starts with '## Overview'"
  fi
  if ! printf '%s\n' "$content" | grep -q '^## Overview'; then
    reject "P5 overview" "$f" "body must contain an '## Overview' heading"
  fi
}

# P1: no em-dashes in staged markdown (index content, not worktree).
for f in $staged; do
  case "$f" in
    *.md)
      if git show ":$f" | grep -qF "$EM_DASH"; then
        reject "P1 em-dash" "$f" "U+2014 found; use comma, colon, parentheses, or hyphen"
      fi
      ;;
  esac
done

# P2..P5: SKILL.md standards.
for f in $staged; do
  case "$f" in
    skills/*/SKILL.md) check_skill_md "$f" ;;
  esac
done

# P6: a brand-new skill must land with both catalog rows (same commit).
for f in $staged; do
  case "$f" in
    skills/*/SKILL.md)
      if ! git cat-file -e "HEAD:$f" 2>/dev/null; then
        folder=$(basename "$(dirname "$f")")
        git show ":README.md" | grep -q "skills/$folder/" || \
          reject "P6 catalog-sync" "$f" "new skill missing from README.md ## Skills table"
        git show ":AGENTS.md" | grep -q "skills/$folder/" || \
          reject "P6 catalog-sync" "$f" "new skill missing from AGENTS.md ## Current skills table"
      fi
      ;;
  esac
done

# P7: forbidden directories, any depth.
for f in $staged; do
  case "$f" in
    temp/*|*/temp/*|old/*|*/old/*|archive/*|*/archive/*|docs/superpowers/*|.planning/*)
      reject "P7 forbidden-path" "$f" "no temp/, old/, archive/, docs/superpowers/, or .planning/ paths" ;;
  esac
done

if [ "$fail" -ne 0 ]; then
  printf '\nBypass (emergencies only): git commit --no-verify\n' >&2
  exit 1
fi
exit 0
```

- [ ] **Step 2: Normalize line endings to LF (Windows write may emit CRLF, which breaks the shebang)**

```powershell
$p = ".githooks\pre-commit"
$t = [IO.File]::ReadAllText($p) -replace "`r`n", "`n"
[IO.File]::WriteAllText($p, $t, [Text.UTF8Encoding]::new($false))
```

- [ ] **Step 3: Stage, set the executable bit, confirm mode**

```powershell
git add .githooks/pre-commit
git update-index --chmod=+x .githooks/pre-commit
git ls-files -s .githooks/pre-commit
```

Expected output starts with `100755`.

- [ ] **Step 4: Commit (this commit itself exercises the new hook; only the non-md hook file is staged, so all checks no-op and it must pass)**

```powershell
git commit -m "feat(githooks): enforce doc standards in pre-commit hook"
```

Expected: commit succeeds.

---

### Task 4: Verification matrix in a scratch clone

**Files:**
- Test: scratch clone at `C:\Users\ruben\AppData\Local\Temp\opencode\hook-verify\scratch` (pre-approved temp dir; delete afterwards). No tracked files change in this task.

**Interfaces:**
- Consumes: the pre-commit hook from Task 3, as committed.
- Produces: PASS/REJECT evidence for every matrix row. If any row misbehaves, fix the hook in the real repo (new `fix(githooks): ...` commit), re-clone, and re-run the full matrix.

- [ ] **Step 1: Clone and activate hooks (clones do not inherit core.hooksPath)**

```powershell
$repo = "C:\Users\ruben\Projects\Tools\skills"
$scratch = "C:\Users\ruben\AppData\Local\Temp\opencode\hook-verify\scratch"
New-Item -ItemType Directory -Force (Split-Path $scratch) | Out-Null
git clone $repo $scratch
git -C $scratch config core.hooksPath .githooks
```

- [ ] **Step 2: Run each case and record the exit code**

Helper (defines a reusable commit attempt; `$LASTEXITCODE` after each call is the verdict):

```powershell
function Test-Commit {
  param([string]$Message)
  git -C $scratch add -A 2>$null
  git -C $scratch commit -m $Message 2>&1 | Out-String
  $LASTEXITCODE
}
function Reset-Scratch { git -C $scratch reset --hard HEAD 2>$null; git -C $scratch clean -fdq }
```

Run these cases in order, resetting between each (`Reset-Scratch`). Expected verdicts:

| Case | Setup after reset | Message | Expected |
|---|---|---|---|
| M0 baseline clean | touch nothing | n/a | `git -C $scratch commit --allow-empty -m "docs: baseline"` exits 0 |
| M1 em-dash | `Set-Content "$scratch/bad.md" "a $( [char]0x2014 ) b" -Encoding UTF8` | `docs: m1` | 1, output contains `P1 em-dash` |
| M2 name mismatch | mkdir `skills/bad-skill`; write SKILL.md frontmatter `name: wrong-name`, `description: Use when testing`, body `## Overview` | `docs: m2` | 1, `P2 name` |
| M3 description | same but `name: bad-skill`, description `Testing things` | `docs: m3` | 1, `P3 description` |
| M4 frontmatter size | same but description is a 1100-char `Use when ...` string | `docs: m4` | 1, `P4 frontmatter-size` |
| M5a `## Skill` heading | same valid skill but body has `## Skill` and `## Overview` | `docs: m5a` | 1, `P5 skill-heading` |
| M5b missing Overview | same valid skill, body has neither heading | `docs: m5b` | 1, `P5 overview` |
| M6 new skill, no catalog rows | valid `skills/fresh-skill/SKILL.md` (name matches, `Use when`, `## Overview`, under 1024) | `docs: m6` | 1, `P6 catalog-sync` (both messages) |
| M6-pass same skill with rows | add `skills/fresh-skill/` row to README `## Skills` table and AGENTS `## Current skills` table | `docs: m6 pass` | 0 |
| M7 forbidden dir | `New-Item "$scratch/docs/superpowers" -ItemType Directory -Force`; add `x.md` inside | `docs: m7` | 1, `P7 forbidden-path` |

Note for M1: PowerShell 5.1 `Set-Content -Encoding UTF8` writes a BOM; harmless here, the em-dash bytes are mid-file. For M4, build the string: `$long = "Use when " + ("x" * 1100)`.

- [ ] **Step 3: Confirm baseline repo still passes its own hooks**

```powershell
git -C "C:\Users\ruben\Projects\Tools\skills" status --short
```

Expected: clean. Then `git -C "C:\Users\ruben\Projects\Tools\skills" commit --allow-empty --dry-run` exits 0 (hook chain healthy on the real repo).

- [ ] **Step 4: Clean up scratch clone**

```powershell
Remove-Item -Recurse -Force (Split-Path $scratch)
```

No commit in this task (verification only). If fixes were needed, they were committed as `fix(githooks): ...` per the Interfaces note.

---

### Task 5: Documentation wiring

**Files:**
- Modify: `AGENTS.md` (Git & workflow section, enforcement sentence)
- Modify: `STANDARDS.md` (enforcement sentence, around line 85)
- Modify: `opencode-install.md` (step 10, lines 129-137)
- Modify: `CHANGELOG.md` (Added entries)

**Interfaces:**
- Consumes: the shipped hook set and check ids P1..P7 from Task 3.
- Produces: docs that name the full hook set; future readers of any of the four files learn activation and bypass.

- [ ] **Step 1: Update the enforcement sentence in `AGENTS.md`**

Find this sentence in the Git & workflow section:

```
Enforced by a tracked `commit-msg` hook (`.githooks/commit-msg`) that rejects non-Conventional-Commits messages, so agent-made and manual commits stay compliant.
```

Replace with:

```
Enforced by tracked git hooks (`.githooks/`): `commit-msg` rejects non-Conventional-Commits messages; `pre-commit` rejects em-dashes in markdown, bad SKILL.md frontmatter (name, description, size, headings), new skills missing from the README/AGENTS catalogs, and forbidden paths (`temp/`, `old/`, `archive/`, `docs/superpowers/`, `.planning/`). Activate once per clone with `git config core.hooksPath .githooks` (see `opencode-install.md` step 10). Bypass: `git commit --no-verify`.
```

Keep the surrounding sentences (the Conventional Commits sentence and branch-model text) as they are; only swap the enforcement sentence and keep one `Bypass:` mention.

- [ ] **Step 2: Update the enforcement line in `STANDARDS.md`**

Find the sentence beginning `Enforcement: a tracked `commit-msg` hook` and replace the clause naming only `commit-msg` with: `Enforcement: tracked git hooks in `.githooks/` (commit-msg for Conventional Commits; pre-commit for markdown and skill-structure rules)`. Keep the activation/bypass instructions that follow it.

- [ ] **Step 3: Update `opencode-install.md` step 10**

Change the heading `### 10. Enable the commit-msg hook` to `### 10. Enable the git hooks`. In the body paragraph, replace "a tracked `commit-msg` git hook (`.githooks/commit-msg`) that rejects non-Conventional-Commits messages" with "tracked git hooks (`.githooks/`) that reject non-Conventional-Commits messages, em-dashes in markdown, malformed SKILL.md frontmatter, new skills missing from the catalogs, and forbidden paths". Keep the `git config core.hooksPath .githooks` command block, the sh+grep note, and the bypass line.

- [ ] **Step 4: Add CHANGELOG entries**

Read `CHANGELOG.md` and follow its existing format (Keep a Changelog). Under the current Unreleased/Added section, append:

```
- Standardization git hooks: new `pre-commit` hook enforcing markdown em-dash ban, SKILL.md frontmatter rules, catalog sync for new skills, and forbidden paths. Activate with `git config core.hooksPath .githooks`.
```

- [ ] **Step 5: Verify no em-dashes entered the docs and commit**

```powershell
(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014)).Count
```

Expected: `0`. Then:

```powershell
git add AGENTS.md STANDARDS.md opencode-install.md CHANGELOG.md
git commit -m "docs: wire standardization git hooks into repo documentation"
```

Expected: commit passes the hooks (`docs:` type, mixed doc files).

---

## Completion checklist

- [ ] All 5 tasks committed on `plan-standardization-githooks`
- [ ] Repo-wide em-dash scan returns 0
- [ ] Full verification matrix green (M0..M7)
- [ ] `git ls-files -s .githooks/` shows the hook at mode 100755
- [ ] Docs name both hooks, activation, and bypass
