# skillctl Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `bin/skillctl`, a dependency-free bash CLI with two subcommands: `check` (worktree-wide lint, superset of pre-commit rules) and `sync` (mirror skills/commands/agents to agent directories).

**Architecture:** One executable bash script, subcommand dispatch via `case`, repo root resolved from script location. Check logic ported from `.githooks/pre-commit` patterns but reads the worktree (not the index); hooks stay untouched. Sync uses mirror semantics (repo is source of truth).

**Tech Stack:** Bash + coreutils only (grep, sed, awk, find, cp, rm, mkdir, diff). No new dependencies.

**Spec:** `docs/artifacts/features/skillctl/2026-09-29-skillctl-design.md`

**Versioning:** unversioned, no bump. Repo AGENTS.md declares no canonical version source.

## Global Constraints

- Bash + coreutils only. No python, no rsync, no node, no new dependencies of any kind.
- No em-dash (U+2014) in any file this plan creates or edits, including code comments and docs.
- Exit contract: 0 = clean, 1 = FAIL found (WARN does not fail), 2 = usage/invocation error.
- Destination mapping is exact: opencode commands go to `~/.config/opencode/command/` (singular), Claude Code commands to `~/.claude/commands/` (plural), agents to `~/.config/opencode/agents/` ONLY (never to any Claude directory).
- Do not modify `.githooks/*`. skillctl duplicates check logic against the worktree by design.
- `--check` modes never mutate anything outside `/tmp` (temp files via `mktemp`, cleaned up).
- Commit messages: Conventional Commits 1.0.0. Branch: `feat/skillctl`.
- Bash portability: target GNU bash + GNU coreutils on linux (matches this machine and `.githooks`).

---

### Task 1: `bin/skillctl` skeleton + `check` subcommand

**Files:**
- Create: `bin/skillctl` (executable)

**Interfaces:**
- Consumes: none
- Produces: executable `bin/skillctl` with `check` subcommand; output lines `PASS <id> ...`, `FAIL <id> ...`, `WARN <id> ...` where id is C1..C8; summary line `checks: <n> fail, <n> warn`; exit 0/1 per Global Constraints. `sync` is NOT wired yet (usage text lists only `check`).

**Depends:** none

- [ ] **Step 1: Create the script with full check implementation**

Create `bin/skillctl` with exactly this content:

```bash
#!/usr/bin/env bash
# skillctl: repo maintenance CLI. Bash + coreutils only, no dependencies.
# Subcommands: check (worktree-wide lint), sync (mirror to agent dirs).
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILS=0
WARNS=0

usage() {
  cat <<'EOF'
usage: skillctl check
       skillctl sync [--agent opencode|claude] [--check]

check  lint the whole worktree (rules C1..C8), exit 1 on any FAIL
sync   mirror skills/, commands/, agents/ to agent directories
EOF
  exit 2
}

pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; FAILS=$((FAILS + 1)); }
warn() { echo "WARN  $1"; WARNS=$((WARNS + 1)); }

# frontmatter field extractor: prints value of the given key from the
# first --- block, or nothing when absent.
fm_field() { # file key
  awk -v k="$2" '
    NR == 1 { if ($0 !~ /^---[[:space:]]*$/) exit; next }
    /^---[[:space:]]*$/ { exit }
    index($0, k ":") == 1 {
      sub("^[^:]*:[[:space:]]*", "")
      gsub(/^"|"$/, "")
      print
      exit
    }
  ' "$1"
}

skill_check() { # path/to/skills/<name>/SKILL.md
  local f="$1" dir name desc closing fmsize before
  dir=$(basename "$(dirname "$f")")
  before=$FAILS

  [ "$(head -n 1 "$f")" = "---" ] || { fail "C2 $dir: missing frontmatter"; return; }

  name=$(fm_field "$f" name)
  desc=$(fm_field "$f" description)
  closing=$(awk '/^---[[:space:]]*$/ { c++; if (c == 2) { print NR; exit } }' "$f")
  if [ -z "$closing" ]; then fail "C2 $dir: unterminated frontmatter"; return; fi
  fmsize=$(head -n "$closing" "$f" | wc -c)

  if ! printf '%s' "$name" | grep -Eq '^[a-z0-9][a-z0-9-]*$'; then
    fail "C2 $dir: name '$name' not kebab-case"
  fi
  if [ "$name" != "$dir" ] && [ "$dir" != "rubens-project-standardization" ]; then
    fail "C2 $dir: frontmatter name '$name' does not match folder"
  fi

  case "$desc" in
    "Use when"*) : ;;
    *) fail "C3 $dir: description must start with 'Use when'" ;;
  esac

  [ "$fmsize" -le 1024 ] || fail "C4 $dir: frontmatter is ${fmsize} bytes, over 1024"

  grep -q '^## Overview' "$f" || fail "C5 $dir: missing '## Overview' heading"
  if grep -qE '^## Skill[[:space:]]*$' "$f"; then
    fail "C5 $dir: has '## Skill' heading, use '## Overview'"
  fi

  [ "$FAILS" -eq "$before" ] && pass "C2-C5 $dir: frontmatter and body ok"
}

cmd_check() {
  local hits em s c base
  # C1: em-dash scan over tracked markdown only (untracked scratch files
  # such as .superpowers/ reports are out of scope, matching hook scope)
  em=$'\u2014'
  hits=$(mktemp)
  if git -C "$REPO_ROOT" ls-files -z -- '*.md' | xargs -0 -r grep -lF -- "$em" >"$hits" 2>/dev/null; then
    fail "C1 em-dash in: $(tr '\n' ' ' <"$hits")"
  else
    pass "C1 no em-dashes in tracked markdown"
  fi
  rm -f "$hits"

  # C2..C5: per-skill frontmatter and body
  for s in "$REPO_ROOT"/skills/*/SKILL.md; do
    [ -f "$s" ] || continue
    skill_check "$s"
  done

  # C6: catalog rows for every skill (README.md + AGENTS.md tables).
  # README rows link `./skills/<name>/SKILL.md`, AGENTS rows name
  # `skills/<name>/`; the common substring is `skills/<name>/`.
  for s in "$REPO_ROOT"/skills/*/; do
    [ -f "${s}SKILL.md" ] || continue
    base=$(basename "$s")
    grep -q "skills/$base/" "$REPO_ROOT/README.md" \
      || fail "C6 $base: missing from README.md skills table"
    grep -q "skills/$base/" "$REPO_ROOT/AGENTS.md" \
      || fail "C6 $base: missing from AGENTS.md current-skills table"
  done
  [ "$FAILS" -gt 0 ] || pass "C6 all skills present in both catalogs"

  # C7: every command file is referenced by some SKILL.md (warn-level;
  # universal commands without a parent skill may legitimately warn)
  for c in "$REPO_ROOT"/commands/*.md; do
    [ -f "$c" ] || continue
    base=$(basename "$c")
    if ! grep -rqF "commands/$base" "$REPO_ROOT"/skills --include='SKILL.md'; then
      warn "C7 commands/$base not referenced by any SKILL.md"
    fi
  done
  [ "$WARNS" -gt 0 ] || pass "C7 every command referenced by a SKILL.md"

  # C8: forbidden paths
  for s in temp old archive docs/superpowers .planning; do
    [ -e "$REPO_ROOT/$s" ] && fail "C8 forbidden path exists: $s/"
  done
  [ "$FAILS" -gt 0 ] || pass "C8 no forbidden paths"

  echo "---"
  echo "checks: $FAILS fail, $WARNS warn"
  [ "$FAILS" -eq 0 ]
}

case "${1:-}" in
  check) shift; [ $# -eq 0 ] || usage; cmd_check ;;
  *) usage ;;
esac
```

Then: `chmod +x bin/skillctl`

- [ ] **Step 2: Verify clean repo passes**

Run: `bin/skillctl check; echo "exit=$?"`
Expected: all PASS lines (C7 may WARN for universal commands, that is fine), `checks: 0 fail`, `exit=0`.

- [ ] **Step 3: Verify dirty fixtures fail**

```bash
printf 'broken \u2014 dash\n' > "$PWD/emdash-fixture.md"
git add -N "$PWD/emdash-fixture.md"
mkdir -p skills/zz-fixture && printf -- '---\nname: ZZ Bad\ndescription: does things\n---\n\n## Body\n' > skills/zz-fixture/SKILL.md
bin/skillctl check; echo "exit=$?"
git reset -q -- "$PWD/emdash-fixture.md"
rm -f "$PWD/emdash-fixture.md" && rm -rf skills/zz-fixture
bin/skillctl check; echo "exit=$?"
```
Expected: first run FAILs (C1 em-dash, visible because the fixture is intent-to-add so `ls-files` lists it; C2 name not kebab-case + name/folder mismatch; C3 description; C5 missing Overview; C6 fixture missing from catalogs), `exit=1`. Cleanup run: `exit=0`. The fixture files MUST be removed and unstaged before commit.

- [ ] **Step 3: Verify usage error**

Run: `bin/skillctl bogus; echo "exit=$?"` and `bin/skillctl check extra; echo "exit=$?"`
Expected: usage text, `exit=2` both times.

- [ ] **Step 4: Commit**

```bash
git add bin/skillctl
git commit -m "feat(skillctl): add check subcommand for worktree-wide lint"
```

---

### Task 2: `sync` subcommand

**Files:**
- Modify: `bin/skillctl`

**Interfaces:**
- Consumes: Task 1 script skeleton (`usage`, `pass/fail/warn`, `REPO_ROOT`, dispatch `case`).
- Produces: `bin/skillctl sync [--agent opencode|claude] [--check]`. Output lines `SYNCED <dest>`, `MISSING <dest>`, `STALE  <dest>`, `EXTRA  <dest>`; final `sync: <n> synced` or `sync: <n> missing, <n> stale` in check mode; exit 1 when check mode finds MISSING/STALE; post-run reminder line "restart opencode to reload agents" when agents were mirrored in a real (non-dry) run.

**Depends:** Task 1

- [ ] **Step 1: Add mirror helper and cmd_sync above the dispatch case**

Insert before the `case "${1:-}" in` block:

```bash
SYNCED_N=0
MISSING_N=0
STALE_N=0

mirror() { # repo_kind_dir src_path dest_dir
  local kind="$1" src="$2" dest_dir="$3" name base e
  name=$(basename "$src")
  base="$dest_dir/$name"
  if [ "$DRY" -eq 1 ]; then
    if [ ! -e "$base" ]; then
      echo "MISSING $base"; MISSING_N=$((MISSING_N + 1))
    elif ! diff -rq "$src" "$base" >/dev/null 2>&1; then
      echo "STALE  $base"; STALE_N=$((STALE_N + 1))
    fi
    for e in "$dest_dir"/*; do
      [ -e "$e" ] || continue
      [ -e "$REPO_ROOT/$kind/$(basename "$e")" ] \
        || { echo "EXTRA  $e"; WARNS=$((WARNS + 1)); }
    done
  else
    mkdir -p "$dest_dir"
    rm -rf "$base"
    cp -r "$src" "$base"
    echo "SYNCED $base"
    SYNCED_N=$((SYNCED_N + 1))
  fi
}

cmd_sync() {
  local agent="all" DRY=0 a agents oc s c g touched_agents=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --agent)
        [ $# -ge 2 ] || usage
        agent="$2"; shift 2
        ;;
      --check) DRY=1; shift ;;
      *) usage ;;
    esac
  done
  case "$agent" in
    opencode|claude|all) ;;
    *) usage ;;
  esac
  case "$agent" in
    all) agents="opencode claude" ;;
    *) agents="$agent" ;;
  esac

  for a in $agents; do
    case "$a" in
      opencode)
        oc="$HOME/.config/opencode"
        for s in "$REPO_ROOT"/skills/*/; do
          [ -e "$s" ] || continue
          mirror skills "$s" "$oc/skills"
        done
        for c in "$REPO_ROOT"/commands/*.md; do
          [ -e "$c" ] || continue
          mirror commands "$c" "$oc/command"
        done
        for g in "$REPO_ROOT"/agents/*.md; do
          [ -e "$g" ] || continue
          # README.md is the roster doc, not an agent definition
          [ "$(basename "$g")" = README.md ] && continue
          mirror agents "$g" "$oc/agents"
        done
        touched_agents=1
        ;;
      claude)
        for s in "$REPO_ROOT"/skills/*/; do
          [ -e "$s" ] || continue
          mirror skills "$s" "$HOME/.claude/skills"
        done
        for c in "$REPO_ROOT"/commands/*.md; do
          [ -e "$c" ] || continue
          mirror commands "$c" "$HOME/.claude/commands"
        done
        # agents are opencode-only, never copied for Claude Code
        ;;
    esac
  done

  if [ "$DRY" -eq 1 ]; then
    echo "---"
    echo "sync: $MISSING_N missing, $STALE_N stale, $WARNS extra (dry run, nothing changed)"
    [ "$((MISSING_N + STALE_N))" -eq 0 ]
  else
    echo "---"
    echo "sync: $SYNCED_N synced"
    [ "$touched_agents" -eq 1 ] && echo "reminder: restart opencode to reload agents"
    return 0
  fi
}
```

And extend the dispatch case:

```bash
case "${1:-}" in
  check) shift; [ $# -eq 0 ] || usage; cmd_check ;;
  sync) shift; cmd_sync ;;
  *) usage ;;
esac
```

Note: `mirror` reads `DRY` from `cmd_sync`'s locals (bash dynamic scoping); EXTRA increments `WARNS` to reuse the shared counters.

- [ ] **Step 2: Verify dry-run reports and mutates nothing**

Run: `bin/skillctl sync --check; echo "exit=$?"`
Expected: MISSING/STALE/EXTRA report lines (EXTRA for foreign skills like externally installed ones is expected), dry-run summary, `exit=1` if anything is missing or stale, `exit=0` if fully synced. Verify nothing changed: destinations listed as MISSING/STALE still exist in their prior state.

- [ ] **Step 3: Verify real sync and idempotence**

```bash
bin/skillctl sync; echo "exit=$?"
bin/skillctl sync --check; echo "exit=$?"
```
Expected: first run SYNCED lines + `sync: <n> synced` + opencode restart reminder, `exit=0`. Second run: no MISSING/STALE, `exit=0`. Spot-check one unit: `diff -rq skills/brainstorming ~/.config/opencode/skills/brainstorming` (or any synced folder) returns empty. Confirm `~/.claude/agents/` was NOT created: `ls ~/.claude/agents 2>&1` may show anything, but no file from this repo's `agents/` may appear there.

- [ ] **Step 4: Verify flags**

Run: `bin/skillctl sync --agent claude --check; echo "exit=$?"` (only claude lines) and `bin/skillctl sync --agent bogus; echo "exit=$?"` (usage, `exit=2`).

- [ ] **Step 5: Regression**

Run: `bin/skillctl check; echo "exit=$?"`: Expected `exit=0`.

- [ ] **Step 6: Commit**

```bash
git add bin/skillctl
git commit -m "feat(skillctl): add sync subcommand mirroring to agent dirs"
```

---

### Task 3: Document skillctl in repo docs

**Files:**
- Modify: `AGENTS.md` (Stack section, "Slash commands" sync subsection, SKILL.md body rules, "Adding or modifying a skill" steps 4-5)
- Modify: `opencode-install.md` (sync step)

**Interfaces:**
- Consumes: spec section "Docs changes"; command syntax `bin/skillctl check` and `bin/skillctl sync [--agent X] [--check]` as produced by Tasks 1-2.
- Produces: docs consistent with shipped CLI.

**Depends:** Task 1, Task 2 (Step 7 runs `bin/skillctl check` from Task 1; replacement text references `sync` behavior from Task 2; files stay disjoint from Tasks 1-2)

- [ ] **Step 1: Read current text of both files**

Read `AGENTS.md` and `opencode-install.md` in full to anchor edit locations.

- [ ] **Step 2: Amend AGENTS.md Stack section**

Find the Stack bullet: `**Content:** Markdown only. No build step, no tooling, no runtime.`
Append one sentence so the bullet reads:

```markdown
- **Content:** Markdown only. No build step, no tooling, no runtime. Single exception: `bin/skillctl`, a dependency-free bash maintenance CLI (`check`, `sync`); no other tooling.
```

- [ ] **Step 3: Replace the manual sync two-step in AGENTS.md**

In the "Slash commands" section, keep the destination table and the "dead weight until synced" warning, but replace the numbered manual copy instructions with:

```markdown
Run `bin/skillctl sync` from the clone root to perform both steps plus the agents sync in one command. `bin/skillctl sync --check` reports drift (MISSING / STALE) without changing anything. Mappings are encoded there; the table stays as reference. Manual equivalent (if the CLI is unavailable): copy each folder under `skills/` to the agent's skills directory, then `commands/*.md` to the commands directory per the table below.
```

Keep the existing table and the singular/plural warning below it untouched.

- [ ] **Step 4: Replace the PowerShell em-dash verification in AGENTS.md**

In the `SKILL.md` body rules section, replace the sentence containing the `Get-ChildItem ... Select-String` incantation with:

```markdown
Verify with `bin/skillctl check` (rule C1) reporting no em-dashes.
```

- [ ] **Step 5: Point skill-verification steps at skillctl in AGENTS.md**

In "Adding or modifying a skill", steps 4 and 5 say "Verify the frontmatter passes: ..." and "Verify the body: ...". Prepend to each: `Run `bin/skillctl check` (rules C2-C5);` keeping the rule text as explanation, e.g. "Verify the frontmatter passes: run `bin/skillctl check` (rules C2-C5). `name` in kebab-case, ...".

- [ ] **Step 6: Update opencode-install.md sync step**

Find the step that copies commands and agents to `~/.config/opencode/` (step 8 in current numbering). Replace the manual copy commands with `bin/skillctl sync` run from the clone, noting `--check` for a dry run. Keep the restart note.

- [ ] **Step 7: Verify**

Run: `bin/skillctl check; echo "exit=$?"`: Expected `exit=0` (docs edits contain no em-dash). Read back every edited section; confirm no em-dash, no contradiction with CLI behavior.

- [ ] **Step 8: Commit**

```bash
git add AGENTS.md opencode-install.md
git commit -m "docs(skillctl): document skillctl, add stack exception"
```

---

### Task 4: Final verification

**Files:**
- Modify: none (verification only; fix-forward trivial regressions in the owning file if found, as a `fix(skillctl):` commit)

**Interfaces:**
- Consumes: finished `bin/skillctl` (Tasks 1-2), docs (Task 3).
- Produces: verification evidence for the execution report.

**Depends:** Task 1, Task 2, Task 3

- [ ] **Step 1: Full check**

Run: `bin/skillctl check; echo "exit=$?"`: Expected `exit=0`.

- [ ] **Step 2: Sync state**

Run: `bin/skillctl sync --check; echo "exit=$?"`: Expected `exit=0` after Task 2's real sync (or run `bin/skillctl sync` first if Task 2 ran more than a commit ago and nothing changed since).

- [ ] **Step 3: No cross-contamination**

Run: `ls ~/.claude/agents/ 2>/dev/null | grep -E 'planner|orchestrator|executor|reviewer|lazy-dev|documenter|explore|oracle|inventree'`: Expected: empty (agents never sync to Claude Code).

- [ ] **Step 4: Hook coexistence**

Run: `git log --oneline -4`: Expected: three Conventional Commits from Tasks 1-3. Run: `bash -n bin/skillctl`: Expected: no syntax errors.
