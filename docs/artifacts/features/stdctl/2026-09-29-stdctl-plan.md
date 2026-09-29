# stdctl Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `stdctl`, a general standards-check CLI for any standardized repo: new sibling project `~/projects/Tools/stdctl` with single-file `bin/stdctl check`, symlinked to `~/.local/bin/stdctl`, plus the standard docs fixes that make the convention match the tool.

**Architecture:** stdctl resolves the repo from cwd (`git rev-parse --show-toplevel`), gates on AGENTS.md presence, detects tier from AGENTS.md, then runs floor (G1-G7), structure (S1-S5), and skills-collection (K1-K2) rules. Single bash file, no dependencies. skills repo keeps skillctl untouched.

**Tech Stack:** Bash + coreutils only (git, grep, awk, sed, find, xargs, mktemp).

**Spec:** `docs/artifacts/features/stdctl/2026-09-29-stdctl-design.md` (in the skills repo, /home/ruben/projects/Tools/skills)

**Versioning:** both repos unversioned, no bump.

## Global Constraints

- Two repos involved: skills repo `/home/ruben/projects/Tools/skills` (branch `feat/stdctl-docs` for Tasks 5-6; spec/plan/report artifacts there) and NEW repo `/home/ruben/projects/Tools/stdctl` (its own `main`).
- Bash + coreutils only. No new dependencies anywhere.
- No em-dash (U+2014) in any file or commit message either repo.
- Exit contract: 0 = no FAIL, 1 = FAIL found or unstandardized repo, 2 = usage error / not a git repo. WARN never fails.
- Exception list (G3) is verbatim from the spec; if it must change, change spec + tool + `standards-stack.md` together.
- Do not modify `bin/skillctl`, `.githooks/`, or `commands/` in the skills repo.
- stdctl repo commits use Conventional Commits without scope (single-purpose repo), e.g. `feat: add floor rules`.

---

### Task 1: Bootstrap the stdctl repo (small tier)

**Files:**
- Create: `/home/ruben/projects/Tools/stdctl/` (AGENTS.md, CLAUDE.md, README.md, .gitignore, .gitattributes, .githooks/pre-commit, .githooks/commit-msg)

**Interfaces:**
- Consumes: templates from `/home/ruben/projects/Tools/skills/skills/rubens-project-standardization/templates/` (read them first).
- Produces: git repo on branch `main`, small-tier scaffold passing its own `stdctl check` later (Task 4 dogfood: AGENTS.md with `Tier: small` + Git section, CLAUDE.md shim, hooks activated).

**Depends:** none

- [ ] **Step 1: Scaffold**

```bash
mkdir -p /home/ruben/projects/Tools/stdctl && cd /home/ruben/projects/Tools/stdctl
git init -b main
```

Write `AGENTS.md`:

```markdown
# stdctl

## What this is

Single-file bash CLI that lints any repository against the project-standardization convention (source: the `project-standardization` skill in the skills repo). One subcommand: `check`. Rules: floor (G1-G7), structure + tier (S1-S5), skills-collection (K1-K2). Spec and history: `docs` artifacts live in the skills repo under `docs/artifacts/features/stdctl/`.

Tier: small

## Stack

Bash + coreutils only. One file: `bin/stdctl`. No dependencies, no build step.

## Git & workflow

- No commit/push without explicit user instruction, except while executing an approved spec+plan (commits at task boundaries).
- Conventional Commits 1.0.0, no scope. Branch naming Conventional Branch 1.1.0.
- Install: `ln -sf ~/projects/Tools/stdctl/bin/stdctl ~/.local/bin/stdctl` (single file, copy works too).
```

Write `CLAUDE.md` (shim): single line `@AGENTS.md` plus a blank line.

Write `README.md`:

```markdown
# stdctl

Standards check for repositories following the project-standardization convention. Run `stdctl check` inside any git repo; exit 0 means compliant, 1 means FAILs (or the repo is not standardized), 2 means invocation error. Rule IDs G1-G7 (floor), S1-S5 (structure/tier), K1-K2 (skills collections) are defined in the spec in the skills repo.

## AI assistance

This project is maintained with AI coding agents following the [agents.md](https://agents.md) convention. Skill source: RubenVanDerVeen/skills.
```

Write `.gitattributes`:

```
* text=auto
.githooks/** text eol=lf
```

Write `.gitignore`: `graphify-out/` on one line.

Copy the hook templates from the skills repo and strip the skills-specific P2-P6 block from `pre-commit` (stdctl has no `skills/` dir; keep P1 em-dash + P7 forbidden paths):

```bash
cp /home/ruben/projects/Tools/skills/skills/rubens-project-standardization/templates/pre-commit .githooks/pre-commit
cp /home/ruben/projects/Tools/skills/skills/rubens-project-standardization/templates/commit-msg .githooks/commit-msg
chmod +x .githooks/pre-commit .githooks/commit-msg
git config core.hooksPath .githooks
```

Then edit `.githooks/pre-commit`: delete the skills machinery entirely: the `check_skill_md` function definition (it sits above the P1 loop in the template), the stale `# Checks:` header comment listing P2-P6, and the P2-P6 sections between the P1 block and P7. Keep P1 (em-dash) and P7 (forbidden paths) intact and renumber the header comment accordingly.

- [ ] **Step 2: Verify scaffold**

Run: `git add -A && git status --short`
Expected: the files above, nothing else. `grep -c 'Tier: small' AGENTS.md` returns 1.

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: bootstrap stdctl repo (small tier)"
```

---

### Task 2: `bin/stdctl` skeleton + unstandardized gate + floor rules G1-G7

**Files:**
- Create: `/home/ruben/projects/Tools/stdctl/bin/stdctl` (executable)

**Interfaces:**
- Consumes: Task 1 repo.
- Produces: `stdctl check [--quiet]` running G1-G7 after the AGENTS.md gate. Output `PASS|FAIL|WARN <id> ...` + `checks: <n> fail, <n> warn`; exit 0/1/2. Structure rules S1-S5 and K1-K2 are NOT wired yet (Task 3 adds them; the dispatch case already routes only `check`).

**Depends:** Task 1

- [ ] **Step 1: Write the script**

Create `bin/stdctl` with exactly this content:

```bash
#!/usr/bin/env bash
# stdctl: standards check for any standardized repo. Bash + coreutils only.
set -u

FAILS=0
WARNS=0
QUIET=0

usage() {
  cat <<'EOF'
usage: stdctl check [--quiet]

check   lint the current repo: floor rules G1-G7, structure S1-S5,
        skills-collection K1-K2. Exit 0 clean, 1 on FAIL or unstandardized
        repo, 2 on usage error or not a git repo.
EOF
  exit 2
}

pass() { [ "$QUIET" -eq 1 ] || echo "PASS  $1"; }
fail() { echo "FAIL  $1"; FAILS=$((FAILS + 1)); }
warn() { echo "WARN  $1"; WARNS=$((WARNS + 1)); }

REPO=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "ERROR not a git repo: stdctl lints the repo you are standing in" >&2
  exit 2
}
cd "$REPO" || exit 2

EM=$'\u2014'
EXCEPTIONS="README.md AGENTS.md CLAUDE.md CHANGELOG.md STANDARDS.md LICENSE LICENSE.md Makefile Dockerfile SKILL.md Cargo.toml Cargo.lock package.json package-lock.json pnpm-lock.yaml yarn.lock pyproject.toml poetry.lock go.mod go.sum composer.json tauri.conf.json .release-notes.md AGENTS-small.md AGENTS-medium.md AGENTS-large.md README-ai-assistance.md"

g1() {
  local hits
  hits=$(git ls-files -z -- '*.md' | xargs -0 -r grep -lF -- "$EM" 2>/dev/null)
  if [ -n "$hits" ]; then
    fail "G1 em-dash in: $(printf '%s' "$hits" | tr '\n' ' ')"
  else
    pass "G1 no em-dashes in tracked markdown"
  fi
}

g2() {
  # ponytail: worktree find with dependency-dir pruning; tracked-only scan
  # would miss untracked forbidden dirs, full find would flag node_modules
  local bad="" d
  while IFS= read -r d; do bad="$bad ${d#./}/"; done < <(
    find . \( -name .git -o -name node_modules \
      -o -name target -o -name dist -o -name build \) -prune -o \
      -type d \( -name temp -o -name old -o -name archive \
      -o -name .planning -o -path '*/docs/superpowers' \) -print
  )
  if [ -n "$bad" ]; then
    fail "G2 forbidden paths:$bad"
  else
    pass "G2 no forbidden paths"
  fi
}

g3() {
  local bad
  bad=$(git ls-files | EXC=" $EXCEPTIONS " awk '
    {
      base = $0
      sub(/^.*\//, "", base)
      if (base ~ /^\./) next
      if (index(ENVIRON["EXC"], " " base " ") > 0) next
      if (base !~ /^[a-z0-9][a-z0-9.-]*$/) print $0
    }')
  if [ -n "$bad" ]; then
    fail "G3 non-kebab paths: $(printf '%s\n' "$bad" | head -3 | tr '\n' ' ') (+ $(printf '%s\n' "$bad" | wc -l) total)"
  else
    pass "G3 all tracked paths kebab-case or exempt"
  fi
}

g4() {
  local bad
  bad=$(git ls-files -- 'docs/artifacts/*.md' 'docs/project-management/*.md' \
    | awk '{ base = $0; sub(/^.*\//, "", base)
             if (base == "index.md") next
             if (base !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\.md$/) print $0 }')
  if [ -n "$bad" ]; then
    fail "G4 non-ISO-8601 artifact names: $(printf '%s\n' "$bad" | tr '\n' ' ')"
  else
    pass "G4 artifact filenames ISO 8601 (or none present)"
  fi
}

g5() {
  local br
  br=$(git rev-parse --abbrev-ref HEAD)
  case "$br" in
    main|master|develop|trunk)
      pass "G5 branch '$br' is exempt trunk" ;;
    feat/*|fix/*|docs/*|style/*|refactor/*|perf/*|test/*|build/*|ci/*|chore/*|revert/*)
      if printf '%s' "$br" | grep -Eq '^[a-z]+/[a-z0-9][a-z0-9-]*$'; then
        pass "G5 branch '$br' conventional"
      else
        fail "G5 branch '$br' has a bad description part (kebab, no nested slash)"
      fi ;;
    *)
      fail "G5 branch '$br' is not Conventional Branch <type>/<desc>" ;;
  esac
}

g6() {
  local hp
  if [ ! -d .githooks ]; then
    pass "G6 no .githooks dir, nothing to activate"
    return
  fi
  hp=$(git config core.hooksPath)
  if [ "$hp" != ".githooks" ]; then
    warn "G6 core.hooksPath is '${hp:-unset}', run: git config core.hooksPath .githooks"
  elif ! grep -qF '.githooks/** text eol=lf' .gitattributes 2>/dev/null; then
    warn "G6 .gitattributes missing '.githooks/** text eol=lf'"
  else
    pass "G6 hooks activated"
  fi
}

g7() {
  local total bad_n
  total=$(git rev-list --count HEAD 2>/dev/null || echo 0)
  if [ "$total" -eq 0 ]; then pass "G7 empty history"; return; fi
  bad_n=$(git log --format=%s | grep -Ecv \
    '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: .+|^[Mm]erge |^[Rr]evert |^fixup! |^squash! ')
  if [ "${bad_n:-0}" -eq 0 ]; then
    pass "G7 all $total commit subjects Conventional"
  else
    warn "G7 $bad_n of $total commit subjects non-Conventional (legacy history allowed)"
  fi
}

cmd_check() {
  if [ ! -f AGENTS.md ]; then
    echo "FAIL not standardized: no AGENTS.md at repo root (bootstrap via project-standardization, then re-run)"
    exit 1
  fi
  g1; g2; g3; g4; g5; g6; g7
  echo "---"
  echo "checks: $FAILS fail, $WARNS warn"
  [ "$FAILS" -eq 0 ]
}

case "${1:-}" in
  check)
    shift
    while [ $# -gt 0 ]; do
      case "$1" in
        --quiet) QUIET=1; shift ;;
        *) usage ;;
      esac
    done
    cmd_check
    ;;
  *) usage ;;
esac
```

Then `chmod +x bin/stdctl` (the marker comment above the `echo "---"` line is gone; Task 3 inserts structure rules right after the `g7` call line).

- [ ] **Step 2: Verify in the stdctl repo**

Run from `/home/ruben/projects/Tools/stdctl`: `bin/stdctl check; echo "exit=$?"`
Expected: G1-G7 run, G5 passes on `main`, G6 passes, G7 possibly WARN (`chore: bootstrap...` is Conventional, expect 0), exit 0.

- [ ] **Step 3: Verify gate + usage**

```bash
cd /tmp/opencode && mkdir -p stdctl-gate && cd stdctl-gate && git init -q -b main
/home/ruben/projects/Tools/stdctl/bin/stdctl check; echo "exit=$?"
cd /home/ruben/projects/Tools/stdctl && bin/stdctl bogus; echo "exit=$?"
```
Expected: gate prints the not-standardized FAIL, exit 1; bogus prints usage, exit 2.

- [ ] **Step 4: Verify fixtures (dirty floor)**

```bash
cd /tmp/opencode && rm -rf stdctl-dirty && mkdir stdctl-dirty && cd stdctl-dirty
git init -q -b main && printf '# x\n\nTier: small\n' > AGENTS.md
printf 'broken \u2014 dash\n' > note.md && mkdir -p temp docs/artifacts/features
printf 'x\n' > docs/artifacts/features/myplan.md && git add -A
/home/ruben/projects/Tools/stdctl/bin/stdctl check; echo "exit=$?"
```
Expected: FAIL G1 (em-dash, file is tracked), FAIL G2 (`temp/`), FAIL G4 (`myplan.md` not ISO-dated), exit 1. Then cleanup: `cd /tmp/opencode && rm -rf stdctl-dirty stdctl-gate`.

- [ ] **Step 5: Commit**

```bash
git add bin/stdctl && git commit -m "feat: add check with floor rules G1-G7"
```

---

### Task 3: Structure S1-S5 + skills-collection K1-K2

**Files:**
- Modify: `/home/ruben/projects/Tools/stdctl/bin/stdctl`

**Interfaces:**
- Consumes: Task 2 script (helpers `pass/fail/warn`, `cmd_check` body, `EXCEPTIONS`).
- Produces: full rule set per spec. `TIER` global (`small|medium|large|""`) detected from AGENTS.md by `s1`; `s3`/`s4` branch on it.

**Depends:** Task 2

- [ ] **Step 1: Add tier detection + structure + skills checks above cmd_check**

Insert before `cmd_check()`:

```bash
TIER=""

detect_tier() {
  TIER=$(grep -Eo 'Tier:[[:space:]]*(small|medium|large)' AGENTS.md \
    | head -1 | grep -Eo '(small|medium|large)')
}

s1() {
  if [ -z "$TIER" ]; then
    fail "S1 AGENTS.md declares no 'Tier: small|medium|large'"
  else
    pass "S1 tier declared: $TIER"
  fi
  if grep -Eq '^#+ .*\<Git\>' AGENTS.md; then
    pass "S1 AGENTS.md has a Git section"
  else
    fail "S1 AGENTS.md has no Git section heading"
  fi
}

s2() {
  if [ -f CLAUDE.md ] && grep -qF '@AGENTS.md' CLAUDE.md; then
    pass "S2 CLAUDE.md shim present"
  else
    fail "S2 CLAUDE.md shim missing or lacks '@AGENTS.md'"
  fi
}

s3() {
  local n
  if [ -d .agents ]; then
    n=$(find .agents -maxdepth 1 -name '*.md' | wc -l)
    if [ "$n" -ge 1 ]; then
      if [ "$TIER" = small ]; then
        warn "S3 .agents/ present at small tier (graduation trigger?)"
      else
        pass "S3 .agents/ present with $n topic file(s)"
      fi
    else
      fail "S3 .agents/ exists but holds no .md files"
    fi
  else
    case "$TIER" in
      medium|large) fail "S3 .agents/ required at $TIER tier" ;;
      small) pass "S3 no .agents/ (fine at small tier)" ;;
      *) fail "S3 no .agents/ and no tier declared" ;;
    esac
  fi
}

s4() {
  if [ -f CHANGELOG.md ]; then
    if grep -qF 'Keep a Changelog' CHANGELOG.md; then
      pass "S4 CHANGELOG.md follows Keep a Changelog"
    else
      fail "S4 CHANGELOG.md exists but lacks 'Keep a Changelog' header"
    fi
  else
    case "$TIER" in
      medium|large) fail "S4 CHANGELOG.md required at $TIER tier" ;;
      small) warn "S4 no CHANGELOG.md (fine at small tier unless versioned releases)" ;;
      *) fail "S4 no CHANGELOG.md and no tier declared" ;;
    esac
  fi
}

s5() {
  [ -d docs/artifacts ] || { pass "S5 no docs/artifacts/ yet (created on first artifact)"; return; }
  local missing="" legacy=""
  [ -d docs/artifacts/features ] || missing="$missing features/"
  [ -d docs/artifacts/reviews ] || missing="$missing reviews/"
  [ -d docs/artifacts/choices ] || warn "S5 docs/artifacts/choices/ not created yet (fine until first decision)"
  local d
  for d in specs plans multi-plans; do
    [ -d "docs/artifacts/$d" ] && legacy="$legacy $d/"
  done
  [ -n "$legacy" ] && warn "S5 legacy artifact siblings present:$legacy (migrate per restructure-flow)"
  if [ -n "$missing" ]; then
    fail "S5 docs/artifacts/ missing subdirs:$missing"
  else
    pass "S5 docs/artifacts/ layout ok"
  fi
}

# frontmatter field extractor (single-line values only)
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

k_check() { # skills/<name>/SKILL.md
  local f="$1" dir name desc closing fmsize before
  dir=$(basename "$(dirname "$f")")
  before=$FAILS
  [ "$(head -n 1 "$f")" = "---" ] || { fail "K1 $dir: missing frontmatter"; return; }
  name=$(fm_field "$f" name)
  desc=$(fm_field "$f" description)
  closing=$(awk '/^---[[:space:]]*$/ { c++; if (c == 2) { print NR; exit } }' "$f")
  if [ -z "$closing" ]; then fail "K1 $dir: unterminated frontmatter"; return; fi
  fmsize=$(head -n "$closing" "$f" | wc -c)
  printf '%s' "$name" | grep -Eq '^[a-z0-9][a-z0-9-]*$' \
    || fail "K1 $dir: name '$name' not kebab-case (must start alphanumeric)"
  case "$desc" in
    "Use when"*) : ;;
    *) fail "K1 $dir: description must start with 'Use when'" ;;
  esac
  [ "$fmsize" -le 1024 ] || fail "K1 $dir: frontmatter is ${fmsize} bytes, over 1024"
  grep -q '^## Overview' "$f" || fail "K2 $dir: missing '## Overview' heading"
  grep -qE '^## Skill[[:space:]]*$' "$f" && fail "K2 $dir: has '## Skill' heading, use '## Overview'"
  [ "$FAILS" -eq "$before" ] && pass "K1-K2 $dir: frontmatter and body ok"
}
```

And in `cmd_check`, after the `g7` line, replace the marker area so the body reads:

```bash
  g1; g2; g3; g4; g5; g6; g7
  detect_tier
  s1; s2; s3; s4; s5
  local kf
  for kf in skills/*/SKILL.md; do
    [ -f "$kf" ] || continue
    k_check "$kf"
  done
```

- [ ] **Step 2: Verify self-repo**

Run: `bin/stdctl check; echo "exit=$?"` from `/home/ruben/projects/Tools/stdctl`
Expected: S1 pass (tier small + Git section heading `## Git & workflow`), S2 pass, S3 pass (no `.agents/`), S4 WARN (no CHANGELOG at small tier, acceptable), S5 pass, no K output (no `skills/`), exit 0.

- [ ] **Step 3: Verify structure fixtures**

```bash
cd /tmp/opencode && rm -rf stdctl-struct && mkdir stdctl-struct && cd stdctl-struct
git init -q -b main
printf '# x\n' > AGENTS.md
printf 'x\n' > CLAUDE.md
/home/ruben/projects/Tools/stdctl/bin/stdctl check; echo "exit=$?"
printf '# x\n\nTier: medium\n' > AGENTS.md
/home/ruben/projects/Tools/stdctl/bin/stdctl check; echo "exit=$?"
```
Expected: first run (no Tier line) produces 5 FAILs: S1 no tier, S1 no Git heading, S2 no @AGENTS.md, S3 (no-tier branch: 'no .agents/ and no tier declared'), S4 (no-tier branch), exit 1; second run (Tier: medium) keeps the S1-Git and S2 failures and adds FAIL S3 (medium requires `.agents/`) + FAIL S4 (medium requires CHANGELOG), exit 1.

- [ ] **Step 4: Verify skills-collection via the real skills repo**

```bash
cd /home/ruben/projects/Tools/skills
/home/ruben/projects/Tools/stdctl/bin/stdctl check; echo "exit=$?"
```
Expected: K1-K2 pass for all 18 skills (frontmatter clean per skillctl), S1/S2 pass (AGENTS.md has tier? if the skills repo AGENTS.md declares no `Tier:` line, S1 FAILs with that reason: acceptable and EXPECTED output, note it; the skills repo predates tier lines). Record actual output. Then `cd /tmp/opencode && rm -rf stdctl-struct`.

- [ ] **Step 5: Commit**

```bash
git add bin/stdctl && git commit -m "feat: add structure, tier, and skills-collection checks"
```

---

### Task 4: Install + cross-repo smoke

**Files:**
- Modify: `~/.local/bin/stdctl` (symlink, outside both repos)

**Interfaces:**
- Consumes: finished `bin/stdctl` (Tasks 1-3).
- Produces: machine-wide `stdctl` on PATH working from any cwd.

**Depends:** Task 3

- [ ] **Step 1: Symlink**

```bash
mkdir -p ~/.local/bin
ln -sf ~/projects/Tools/stdctl/bin/stdctl ~/.local/bin/stdctl
command -v stdctl || echo 'PATH missing ~/.local/bin'
```
Expected: `command -v stdctl` prints the symlink path. If PATH misses it, report it; do not edit shell configs.

- [ ] **Step 2: Smoke matrix**

```bash
cd /home/ruben/projects/Tools/stdctl && stdctl check; echo "self=$?"
cd /home/ruben/projects/Tools/skills && stdctl check --quiet; echo "skills=$?"
cd /tmp/opencode && rm -rf stdctl-nogit && mkdir stdctl-nogit && cd stdctl-nogit
stdctl check; echo "nogit=$?"
```
Expected: `self=0` (WARNs allowed), `skills=0` or 1 (if S1 FAILs on the missing tier line, record it; Task 5 decides whether the skills repo AGENTS.md gains a tier line, see Step 3), `nogit=2`.

- [ ] **Step 3: Record skills repo state; commit only if fix-forward was needed**

If `skills=1` in Step 2, record which rules failed; the fixes land in Task 5 on branch `feat/stdctl-docs` (tier line, CLAUDE.md shim if missing). Do not edit the skills repo in this task. If Tasks 2-3 needed fixes during smoke, commit them here with `fix: ...`. Otherwise no commit.

---

### Task 5: Standard docs fixes + stdctl wiring (skills repo)

**Files:**
- Modify: `/home/ruben/projects/Tools/skills/skills/rubens-project-standardization/references/standards-stack.md`
- Modify: `/home/ruben/projects/Tools/skills/skills/rubens-project-standardization/references/bootstrap.md`
- Modify: `/home/ruben/projects/Tools/skills/skills/rubens-project-standardization/references/versioning.md`
- Modify: `/home/ruben/projects/Tools/skills/skills/rubens-project-standardization/templates/` (STANDARDS.md template, AGENTS.md template if present)
- Modify: `/home/ruben/projects/Tools/skills/AGENTS.md` (frontmatter rule line + `Tier: small` line, Task 5 item 4)

**Interfaces:**
- Consumes: spec section "Standard docs fixes"; working `stdctl check` (Task 3) for verification.
- Produces: convention docs consistent with the shipped tool; `stdctl check` named as the standard verification command.

**Depends:** Task 3, Task 4 (Step 3 runs `stdctl` via the Task 4 symlink)

- [ ] **Step 1: Branch + read**

In the skills repo: `git checkout -b feat/stdctl-docs main`. Read every file listed above before editing.

- [ ] **Step 2: Apply the five fixes from the spec**

1. Kebab exception list (verbatim from spec): add to `standards-stack.md` kebab rule and the STANDARDS.md template's forbidden/kebab section: exception list `README.md, AGENTS.md, CLAUDE.md, CHANGELOG.md, STANDARDS.md, LICENSE, LICENSE.md, Makefile, Dockerfile, SKILL.md, Cargo.toml, Cargo.lock, package.json, package-lock.json, pnpm-lock.yaml, yarn.lock, pyproject.toml, poetry.lock, go.mod, go.sum, composer.json, tauri.conf.json, .release-notes.md, AGENTS-small.md, AGENTS-medium.md, AGENTS-large.md, README-ai-assistance.md, dotfiles (any basename starting with a dot)`.
2. Line budget: `bootstrap.md` step 4 `<80` corrected to the tier table values (small <60, medium <120, large <200). Do not touch the SKILL.md tier table.
3. `versioning.md` bump-table row "New feature, backwards-compatible": fix both malformed cells, `0.X+1.0` to `0.(X+1).0` (pre-1.0 column) and `0.Y+1.0` to `X.(Y+1).0` (>=1.0 column).
4. Skills-repo root `AGENTS.md`: frontmatter rules line "`name`: letters, numbers, hyphens only." gains "Must start with a letter or number." Add `Tier: small` right after the `## What this is` intro paragraph: rationale, the repo has no `.agents/` dir while `docs/artifacts/{features,reviews,choices}/` all exist, and `Tier: small` is the honest declaration (one author, single AGENTS.md suffices, graduation trigger is wanting 2+ `.agents/` topic files). With `Tier: small`: S3 passes (no `.agents/` is fine), S4 passes (CHANGELOG.md exists with Keep a Changelog), S5 passes (all three subdirs exist). Note in the commit body: the skills repo AGENTS.md exceeds the line budgets by design (catalog-heavy doc, the tier table budgets target lean agent context, not the convention source repo); the budget is guidance for target projects, not a hard rule enforced by stdctl. Verify root `CLAUDE.md` shim exists; if absent create it with `@AGENTS.md` plus a blank line (S2 requires it).
5. Wiring: in the AGENTS.md template (or STANDARDS.md template where a Git/verification section lives) and at the end of `bootstrap.md`, add one line: after bootstrap, the standing verification command is `stdctl check` (expects exit 0; tool source: `~/projects/Tools/stdctl`, symlinked at `~/.local/bin/stdctl`).

- [ ] **Step 3: Verify**

```bash
cd /home/ruben/projects/Tools/skills && bin/skillctl check; echo "skillctl=$?"
stdctl check; echo "stdctl=$?"
git diff --stat
```
Expected: `skillctl=0`; `stdctl=0` after the tier line lands (K rules pass, S rules pass); diff touches only the listed files; no em-dash in the diff (`git diff | grep -c $'\u2014'` empty).

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md skills/rubens-project-standardization
git commit -m "docs(standardization): kebab exceptions, tier line, line-budget fix, stdctl wiring"
```

---

### Task 6: Final verification + close-out

**Files:**
- Create: `/home/ruben/projects/Tools/skills/docs/artifacts/features/stdctl/2026-09-29-stdctl-report.md` (documenter)

**Interfaces:**
- Consumes: everything above.
- Produces: execution report + choices entry (documenter): general check CLI lives outside the skills repo as `Tools/stdctl`, symlink distribution, markdown-only rule preserved.

**Depends:** Task 4, Task 5

- [ ] **Step 1: Full matrix re-run**

`stdctl check` in: stdctl repo (exit 0), skills repo on `feat/stdctl-docs` (exit 0), /tmp/opencode non-git dir (exit 2), fresh unstandardized git dir (exit 1). Record outputs.

- [ ] **Step 2: Structure review**

Dispatch doc-standardizer + code-standardizer concurrently over both repos' diffs (skills repo: `feat/stdctl-docs` vs main; stdctl repo: full history).

- [ ] **Step 3: Documenter close-out**

Report at the path above; choices decision entry + index update in the skills repo; both committed on `feat/stdctl-docs` (`docs: add stdctl execution report`). No catalog rows (stdctl is not a skill). No push on either repo.
