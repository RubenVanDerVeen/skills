# Plan: Vendor external skill packs

- **Date:** 2026-10-21
- **Spec:** `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`
- **Branch:** `feat/vendor-external-packs` (create before Task 1; worktree optional per using-git-worktrees)
- **Versioning:** repo unversioned, no bump.
- **Conventions:** Conventional Commits per repo AGENTS.md; agent commits carry Co-Authored-By and Agent-Role trailers per STANDARDS.md. Pre-commit hook requires same-commit catalog rows for every new skill. No em-dashes anywhere (rule C1).

Execution is near-serial: Tasks 1-4 share `README.md`, `AGENTS.md`, `external-skills.md` (catalog files), so they chain. Task 5 needs Task 2's state-file contract and Task 4's AGENTS.md changes. Tasks 6-7 finish machine state and verify.

---

### Task 1: Vendor superpowers leftovers (using-superpowers, verification-before-completion)

**Files:**
- Create: `skills/using-superpowers/SKILL.md`
- Create: `skills/verification-before-completion/SKILL.md`
- Modify: `README.md` (## Skills table), `AGENTS.md` (## Current skills table), `external-skills.md` (superpowers entry)

**Depends:** none

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: two vendored skills present in both catalog tables; downstream tasks assume the catalog-row pattern shown here.

- [ ] **Step 1: Write `skills/using-superpowers/SKILL.md`** (full content, no upstream reference files kept):

````markdown
---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

# Skill: Using Superpowers

Adapted from obra/superpowers (MIT).

## Overview

Skills carry the accumulated lessons of this environment. Invoking the right one before acting is mandatory, not optional.

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** - including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first - they set the approach, then implementation skills carry it out. Brainstorming and systematic-debugging are the most common process skills, but the rule holds for any of them.

- "Let's build X" -> brainstorming first, then implementation skills.
- "Fix this bug" -> systematic-debugging first, then domain skills.

## Red Flags

These thoughts mean STOP - you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent it. |
| "I know what that means" | Knowing the concept is not using the skill. Invoke it. |

## Tool Mapping for OpenCode

When skills request actions, substitute OpenCode equivalents:
- Create or update todos -> OpenCode v2 has no todo tool; track the plan in a markdown file (or the harness's plan facility) instead
- Subagent (general-purpose) -> subagent tool with agent "general" (description, prompt, optional background; sessionID continues a previous subagent)
- Invoke a skill -> OpenCode's native skill tool
- Read files -> read
- Create, edit, or delete files -> write to create or overwrite, edit for targeted changes, shell for deletion
- Run shell commands -> shell (command, workdir, timeout, background)
- Search files -> grep, glob
- Fetch a URL -> webfetch
- Search the web -> websearch
````

- [ ] **Step 2: Copy and adapt `verification-before-completion` from the superpowers cache**

```bash
mkdir -p skills/verification-before-completion
cp ~/.cache/opencode/npm/git-superpowers-0958a5557860/*/node_modules/superpowers/skills/verification-before-completion/SKILL.md \
   skills/verification-before-completion/SKILL.md
```

Then edit the copy:
1. Directly under the `# Verification Before Completion` heading, insert: `Adapted from obra/superpowers (MIT).`
2. Frontmatter stays as-is (description already starts with "Use when...", house-compliant).
3. Scan and fix em-dashes: `grep -nP '\x{2014}' skills/verification-before-completion/SKILL.md` -> replace any hits with commas, colons, or hyphens.

- [ ] **Step 3: Add catalog rows** to `README.md` `## Skills` table AND `AGENTS.md` `## Current skills` table (alphabetical position, same 3-column format):

```markdown
| `skills/using-superpowers/` | `using-superpowers` | Skill discipline: invoke relevant skills before any response. Priority rules, red flags, opencode tool mapping. |
| `skills/verification-before-completion/` | `verification-before-completion` | Evidence before assertions: run verification commands and confirm output before claiming done. |
```

- [ ] **Step 4: Update `external-skills.md`** superpowers entry: replace the existing `Status:` line with:

```markdown
Status: fully forked into this repo 2026-10-21 (5 skills 2026-09-24 plus using-superpowers, verification-before-completion), upstream plugin registration removed. Upstream ships 15 skills total; remaining 8 not vendored (not used here).
```

- [ ] **Step 5: Verify**

Run: `bin/skillctl check`
Expected: all rules pass (C2-C5 frontmatter/body, C6 catalog rows, no em-dash findings for the new files).

Run: `test -f skills/using-superpowers/SKILL.md && test -f skills/verification-before-completion/SKILL.md && echo OK`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add skills/using-superpowers skills/verification-before-completion README.md AGENTS.md external-skills.md
git commit -m "feat(skills): vendor using-superpowers and verification-before-completion from obra/superpowers"
```

---

### Task 2: Vendor caveman skill and command pack

**Files:**
- Create: `skills/caveman/SKILL.md`
- Create: `commands/caveman.md`, `commands/caveman-commit.md`, `commands/caveman-compress.md`, `commands/caveman-review.md`, `commands/caveman-stats.md`, `commands/caveman-help.md`
- Modify: `README.md`, `AGENTS.md`, `external-skills.md` (caveman entry)

**Depends:** Task 1

**Interfaces:**
- Consumes: catalog-row pattern from Task 1.
- Produces: state-file contract consumed by Task 5 - commands write `~/.config/opencode/.caveman-mode` containing exactly one of: `off`, `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`. Absent file means base rules (full, from the global AGENTS.md caveman block) apply.

- [ ] **Step 1: Write `skills/caveman/SKILL.md`** (full content):

````markdown
---
name: caveman
description: Use when the user asks for caveman mode, terse output, fewer tokens, any /caveman switching or /caveman-* command, or says stop caveman for normal prose
---

# Skill: Caveman

Adapted from JuliusBrussee/caveman.

## Overview

Terse-output mode system. The base ruleset (full) is always on via the caveman block in `~/.config/opencode/AGENTS.md`. This skill controls intensity levels. The minimal plugin (`plugins/caveman/plugin.js`, synced into opencode) reads `~/.config/opencode/.caveman-mode` and reinforces the active level every turn.

## Levels

| Level | What changes |
|-------|--------------|
| lite | No filler or hedging. Keep articles and full sentences. Professional but tight |
| full | Drop articles, fragments OK, short synonyms. Classic caveman. No tool-call narration, no decorative tables or emoji, no long raw error-log dumps unless asked. Standard acronyms OK; no invented abbreviations |
| ultra | Strip conjunctions when cause and effect stay unambiguous. One word when one word is enough. State each fact once. NO prose abbreviations (cfg, impl, req, res, fn, auth), NO arrows (X -> Y): zero token saving, cost decode clarity. Code symbols, function names, API names, error strings: never touch |
| wenyan-lite | Semi-classical. Drop filler and hedging but keep grammar structure, classical register |
| wenyan-full | Maximum classical terseness, fully 文言文. Classical sentence patterns, verbs precede objects, subjects often omitted, classical particles (之, 乃, 為, 其) |
| wenyan-ultra | Extreme abbreviation while keeping classical Chinese feel. Maximum compression |
| off | Normal prose. Neutralizes the always-on base rules |

## Auto-Clarity

Every level drops to normal prose for: security warnings, irreversible actions, confused user. Resume the mode after.

Code, commits, and PRs are always written normal, at every level.

## Switching

`/caveman <level>` writes the level (including `off`) to `~/.config/opencode/.caveman-mode`; the plugin picks it up next turn. Without the file, base rules (full) apply.

## Commands

| Command | Purpose | Source |
|---------|---------|--------|
| /caveman | Switch level or show current | commands/caveman.md |
| /caveman-commit | Conventional Commit message compressed to intent | commands/caveman-commit.md |
| /caveman-compress | Compress a memory file to caveman format | commands/caveman-compress.md |
| /caveman-review | Diff review, one line per finding | commands/caveman-review.md |
| /caveman-stats | Token usage and savings estimate | commands/caveman-stats.md |
| /caveman-help | Cheat card for modes and commands | commands/caveman-help.md |
````

- [ ] **Step 2: Write the six command files**

`commands/caveman.md`:

```markdown
---
description: Switch caveman output level (lite, full, ultra, wenyan-lite, wenyan-full, wenyan-ultra, off)
---

Load the caveman skill first. Argument: $ARGUMENTS

- With a level: run `printf '%s' "<level>" > ~/.config/opencode/.caveman-mode`, then reply with exactly `CAVEMAN MODE SET: <level>` plus a one-line description of the level from the skill table.
- With `off`: run `printf '%s' "off" > ~/.config/opencode/.caveman-mode` (the plugin then injects an override line neutralizing the always-on base block), reply `CAVEMAN MODE OFF`, then write normal prose.
- Without argument: read the file if present, report the active level and the full level list, one line each.
```

`commands/caveman-commit.md`:

```markdown
---
description: Write a Conventional Commits message compressed to intent only
---

Inspect the staged diff or the changes given as $ARGUMENTS. Output one Conventional Commits 1.0.0 message (`<type>(<scope>): <description>`), intent only, no padding. Body only when necessary, one line. Follow the repo's STANDARDS.md or AGENTS.md commit rules where present (allowed types, attribution trailers). No preamble, no explanation, just the message.
```

`commands/caveman-compress.md`:

```markdown
---
description: Compress a memory file (AGENTS.md, CLAUDE.md, todo list) to caveman format
---

Target file: $ARGUMENTS (ask if absent). Load the caveman skill. Back up first: `cp <file> <file>.bak`. Rewrite the file caveman-full style: keep every rule, table, command, and path; keep frontmatter and fenced code blocks intact; drop prose. Report old and new line counts and a rough token estimate.
```

`commands/caveman-review.md`:

```markdown
---
description: Compressed code review, one line per finding
---

Review the given diff or branch (default `git diff main...HEAD`; or $ARGUMENTS). One line per finding, format: `path:line problem -> fix`. Order by severity. No summary paragraphs, no praise, no restating the diff. End with `PASS` when there are no findings.
```

`commands/caveman-stats.md`:

```markdown
---
description: Show token usage and estimated caveman savings for this session
---

Estimate current session token usage from the newest log under `~/.local/share/opencode/sessions/`; when unavailable, say so and skip the guess. Report three lines: approximate input and output tokens so far; rough output-token share saved by caveman style (terse output typically cuts 30-60 percent of prose tokens); current caveman level. No tables.
```

`commands/caveman-help.md`:

```markdown
---
description: Cheat card for caveman modes and commands
---

Load the caveman skill, then print: the level table (level plus one-line effect), the six /caveman-* commands with a one-line purpose each, and how to stop (/caveman off, or "stop caveman"). Plain list, no decoration.
```

- [ ] **Step 3: Add catalog rows** to `README.md` and `AGENTS.md` (same tables as Task 1, alphabetical):

```markdown
| `skills/caveman/` | `caveman` | Terse-output levels (lite/full/ultra plus wenyan variants), auto-clarity carve-outs, /caveman switching, six /caveman-* commands. |
```

- [ ] **Step 4: Update `external-skills.md`** caveman entry: replace the install sentence and add a status line (keep Source line):

```markdown
Status: forked into this repo 2026-10-21 (skill + 6 commands + minimal own plugin at plugins/caveman/plugin.js); upstream npx pack uninstalled. Cavecrew dropped: roles covered by own explore/executor/reviewer agents.
```

- [ ] **Step 5: Verify**

Run: `bin/skillctl check`
Expected: pass, including C7 (commands referenced by the skill's ## Commands section).

Run: `grep -c 'caveman' README.md AGENTS.md external-skills.md`
Expected: each file >= 1 (rows and status present).

- [ ] **Step 6: Commit**

```bash
git add skills/caveman commands/caveman.md commands/caveman-commit.md commands/caveman-compress.md commands/caveman-review.md commands/caveman-stats.md commands/caveman-help.md README.md AGENTS.md external-skills.md
git commit -m "feat(skills): vendor caveman skill and command pack"
```

---

### Task 3: Vendor stop-slop

**Files:**
- Create: `skills/stop-slop/SKILL.md`, `skills/stop-slop/references/phrases.md`, `skills/stop-slop/references/structures.md`, `skills/stop-slop/references/examples.md`
- Modify: `README.md`, `AGENTS.md`, `external-skills.md` (stop-slop entry)
- Machine: remove symlink `~/.config/opencode/skills/stop-slop`, then re-sync (own copy takes the location)

**Depends:** Task 2

**Interfaces:**
- Consumes: catalog-row pattern.
- Produces: own `stop-slop` skill replacing the `~/.agents` symlink; Task 6 assumes no symlink remains.

- [ ] **Step 1: Copy upstream content** (symlinked from `~/.agents/skills/stop-slop`):

```bash
mkdir -p skills/stop-slop/references
cp ~/.agents/skills/stop-slop/SKILL.md skills/stop-slop/SKILL.md
cp ~/.agents/skills/stop-slop/references/phrases.md skills/stop-slop/references/phrases.md
cp ~/.agents/skills/stop-slop/references/structures.md skills/stop-slop/references/structures.md
cp ~/.agents/skills/stop-slop/references/examples.md skills/stop-slop/references/examples.md
ls ~/.agents/skills/stop-slop/LICENSE && head -3 ~/.agents/skills/stop-slop/LICENSE
```

Do not copy README.md, CHANGELOG.md, LICENSE (attribution line covers provenance; note the license name shown by `head` in the attribution line, expected MIT).

- [ ] **Step 2: Adapt `skills/stop-slop/SKILL.md`**

1. Replace frontmatter with:

```markdown
---
name: stop-slop
description: Use when drafting, editing, or reviewing prose to remove AI writing patterns - banned phrases, structural cliches, sentence-level rules - and to score text on five dimensions; below 35/50 means revise
---
```

2. Directly under the `# Stop Slop` heading insert an `## Overview` section (rule C5 requires it): attribution line `Adapted from hardikpandya/stop-slop (MIT).` (adjust license name if Step 1 showed otherwise) plus the existing one-line intro if the file has one.
3. Delete the `## License` section (the LICENSE file is intentionally not copied; the attribution line carries provenance).
4. Keep sections `## Core Rules`, `## Quick Checks`, `## Scoring`, `## Examples`; keep reference links relative (`references/phrases.md` etc.).
5. Scan and fix em-dashes in all four files: `grep -rnP '\x{2014}' skills/stop-slop/` -> replace hits with commas, colons, or hyphens.

- [ ] **Step 3: Add catalog rows** (both tables):

```markdown
| `skills/stop-slop/` | `stop-slop` | Removes AI writing patterns from prose: banned phrases, structural cliches, sentence rules, 5-dimension scoring below 35/50 revise. |
```

- [ ] **Step 4: Update `external-skills.md`** stop-slop entry, add status line:

```markdown
Status: forked into this repo 2026-10-21; ~/.agents symlink removed, skillctl sync owns the location.
```

- [ ] **Step 5: Swap the live location**

```bash
rm ~/.config/opencode/skills/stop-slop   # symlink only; verify with ls -la first
bin/skillctl sync --agent opencode
ls ~/.config/opencode/skills/stop-slop/SKILL.md
```

Expected: last command prints the synced own copy path.

- [ ] **Step 6: Verify and commit**

Run: `bin/skillctl check` -> pass.

```bash
git add skills/stop-slop README.md AGENTS.md external-skills.md
git commit -m "feat(skills): vendor stop-slop prose-control skill"
```

---

### Task 4: Vendor ponytail core skill, repoint lazy-dev

**Files:**
- Create: `skills/ponytail/SKILL.md`
- Modify: `agents/lazy-dev.md` (and any other `agents/*.md`, `commands/*.md` referencing the external ponytail), `README.md`, `AGENTS.md`, `external-skills.md` (ponytail entry)

**Depends:** Task 3

**Interfaces:**
- Consumes: catalog-row pattern.
- Produces: `skills/ponytail/` skill; repo agent files cite the own copy (Task 6 deletes the external clone safely).

- [ ] **Step 1: Copy and adapt the core skill**

```bash
mkdir -p skills/ponytail
cp /home/ruben/tools/ponytail/skills/ponytail/SKILL.md skills/ponytail/SKILL.md
```

Only the core `ponytail` skill is vendored (spec: max 2, one suffices; ponytail-audit/debt/gain/help/review stay behind with the clone).

Edits to the copy:
1. Replace the frontmatter description with (keeps triggers, house format):

```markdown
---
name: ponytail
description: Use when writing, adding, refactoring, fixing, reviewing, or designing code, choosing libraries or dependencies, or when the user says ponytail, be lazy, lazy mode, simplest solution, minimal solution, yagni, do less, shortest path, or complains about over-engineering, bloat, boilerplate, or unnecessary dependencies. Forces the laziest solution that actually works. Not for non-coding requests.
---
```

2. Directly under the `# Ponytail` heading insert an `## Overview` section (rule C5 requires it): attribution line `Adapted from DietrichGebert/ponytail.` plus the existing one-line intro if the file has one.
3. Keep sections `## Persistence`, `## The ladder`, `## Rules`, `## Output`, `## Intensity`, `## When NOT to be lazy`, `## Boundaries`.
4. Em-dash scan and fix: `grep -nP '\x{2014}' skills/ponytail/SKILL.md`.

- [ ] **Step 2: Guard repo references**

```bash
grep -rn "tools/ponytail\|DietrichGebert/ponytail.git" agents/ commands/ README.md AGENTS.md
```

Expected: no hits. Only change references that actually name the external clone path or repo URL; `Lens: ponytail.` in `agents/lazy-dev.md` already resolves to the own skill by name once vendored, and the inlined ladder below it is standalone, so no rewrite is mandated.

- [ ] **Step 3: Add catalog rows** (both tables):

```markdown
| `skills/ponytail/` | `ponytail` | Forces the laziest solution that works: YAGNI ladder, standard library before custom code, minimal output. Lens for the lazy-dev plan gate. |
```

- [ ] **Step 4: Update `external-skills.md`** ponytail entry: add status line AND replace the stale `Install:` line (it still instructs cloning to `C:/tools/ponytail` and registering in `~/.opencode/opencode.json`, both retired by Task 6) with:

```markdown
Install: arrives via `bin/skillctl sync --agent opencode` (vendored skill).
```

Status line:

```markdown
Status: core philosophy skill forked into this repo 2026-10-21; clone at ~/tools/ponytail and plugin registration removed (delegation mechanics covered by own agents).
```

- [ ] **Step 5: Verify and commit**

Run: `bin/skillctl check` -> pass. Run: `grep -rn "tools/ponytail\|DietrichGebert/ponytail.git" agents/ commands/ | grep -v external-skills` -> no hits.

```bash
git add skills/ponytail agents/ README.md AGENTS.md external-skills.md
git commit -m "feat(skills): vendor ponytail core philosophy skill, repoint lazy-dev lens"
```

---

### Task 5: Minimal caveman plugin + skillctl plugins sync

**Files:**
- Create: `plugins/caveman/plugin.js`
- Modify: `bin/skillctl` (plugins sync loop), `AGENTS.md` (Stack section + file-layout tree)

**Depends:** Task 2, Task 4

**Interfaces:**
- Consumes: state-file contract from Task 2 (`~/.config/opencode/.caveman-mode`, values `off|lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra`, absent = base rules).
- Produces: `plugins/caveman/plugin.js` (ESM, exports `CavemanPlugin` default, hook `experimental.chat.system.transform`); `skillctl sync` mirrors `plugins/*/` into `~/.config/opencode/plugins/` (Task 6 relies on both).

- [ ] **Step 1: Write the failing test** `plugins/caveman/test.mjs` (kept in repo as the plugin's smoke test):

```js
import { readFileSync, rmSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const state = join(homedir(), ".config", "opencode", ".caveman-mode")
const mod = await import("./plugin.js")
const plugin = await mod.default({})
const hook = plugin["experimental.chat.system.transform"]

async function inject() {
  const out = { system: ["BASE"] }
  await hook({}, out)
  return out.system.length ? out.system[out.system.length - 1] : ""
}

// absent file: base rules apply, plugin stays silent
rmSync(state, { force: true })
console.log("absent:", (await inject()) === "BASE" ? "PASS" : "FAIL")

// ultra: reinforcement line appended
writeFileSync(state, "ultra")
const up = await inject()
console.log("ultra:", up.startsWith("BASE") && up.includes("CAVEMAN MODE ACTIVE (ultra)") ? "PASS" : "FAIL")

// off: override line neutralizes static block
writeFileSync(state, "off")
const off = await inject()
console.log("off:", off.includes("CAVEMAN MODE OFF") ? "PASS" : "FAIL")

// garbage value: treated as absent, silent
writeFileSync(state, "banana")
console.log("garbage:", (await inject()) === "BASE" ? "PASS" : "FAIL")

rmSync(state, { force: true })
```

- [ ] **Step 2: Run it, expect failure**

Run: `node plugins/caveman/test.mjs`
Expected: module-not-found error (`./plugin.js` does not exist yet).

- [ ] **Step 3: Write `plugins/caveman/plugin.js`** (full content):

```js
// Minimal caveman mode reinforcement plugin.
// Adapted from JuliusBrussee/caveman (per-turn state handling concept, heavily slimmed).
// Own version: no command parsing, no manifests, no session heuristics.
// Switching happens via /caveman (commands/caveman.md) writing the state file directly.
//
// State: ~/.config/opencode/.caveman-mode
// Values: off | lite | full | ultra | wenyan-lite | wenyan-full | wenyan-ultra
// Absent or invalid file -> no injection; the always-on base rules in
// ~/.config/opencode/AGENTS.md (full) apply on their own.
// Explicit "off" -> inject an override line so the static block is neutralized.
//
// Requires opencode >= 1.15.x (experimental.chat.system.transform hook).

import { readFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const MODES = new Set([
  "off", "lite", "full", "ultra",
  "wenyan-lite", "wenyan-full", "wenyan-ultra",
])

const LINE = {
  lite:
    "CAVEMAN MODE ACTIVE (lite): no filler or hedging; keep articles and full sentences. Professional but tight.",
  full:
    "CAVEMAN MODE ACTIVE (full): drop articles, fragments OK, short synonyms. No tool-call narration, no decorative tables or emoji, no long raw error-log dumps unless asked.",
  ultra:
    "CAVEMAN MODE ACTIVE (ultra): strip conjunctions when unambiguous, one word when one word is enough, state each fact once. No prose abbreviations, no arrows. Code symbols, function names, API names, error strings: never touch.",
  "wenyan-lite":
    "CAVEMAN MODE ACTIVE (wenyan-lite): semi-classical register. Drop filler and hedging, keep grammar structure.",
  "wenyan-full":
    "CAVEMAN MODE ACTIVE (wenyan-full): fully 文言文, maximum classical terseness. Classical particles (之/乃/為/其), subjects often omitted.",
  "wenyan-ultra":
    "CAVEMAN MODE ACTIVE (wenyan-ultra): extreme abbreviation, classical Chinese feel, maximum compression.",
  off:
    "CAVEMAN MODE OFF: write in normal, complete, professional prose. Ignore all terseness rules for the rest of this reply.",
}

function readMode() {
  try {
    const raw = readFileSync(join(homedir(), ".config", "opencode", ".caveman-mode"), "utf8").trim()
    return MODES.has(raw) ? raw : null
  } catch {
    return null
  }
}

export const CavemanPlugin = async (_ctx) => {
  return {
    // Hook contract mirrors upstream (plugin.js:183-214): output.system is a
    // string ARRAY, mutated in place; the return value is discarded.
    "experimental.chat.system.transform": async (_input, output) => {
      try {
        const mode = readMode()
        if (mode === null) return
        const line = LINE[mode]
        const target = output && typeof output === "object" ? output : {}
        if (!Array.isArray(target.system)) target.system = []
        if (target.system.length === 0) target.system.push(line)
        else target.system[target.system.length - 1] += "\n\n" + line
      } catch {
        // never break a session over caveman
      }
    },
  }
}

export default CavemanPlugin
```

- [ ] **Step 4: Run the test, expect all PASS**

Run: `node plugins/caveman/test.mjs`
Expected: `absent: PASS`, `ultra: PASS`, `off: PASS`, `garbage: PASS`.

Also syntax gate: `node --check plugins/caveman/plugin.js` -> no output (clean).

- [ ] **Step 5: Extend `bin/skillctl` sync with a plugins loop**

Read `bin/skillctl` `cmd_sync` (the opencode branch, after the agents loop ending around line 196). Insert directly after that loop, matching house style:

```bash
        # plugins are opencode-only, mirror each plugin folder
        mkdir -p "$oc/plugins"
        for g in "$REPO_ROOT"/plugins/*/; do
          [ -e "$g" ] || continue
          mirror plugins "${g%/}" "$oc/plugins"
        done
```

Notes:
- `mirror` is the generic copy/diff engine; `DRY=1` (--check) gives MISSING/STALE reporting for free.
- Do NOT add plugins to the Claude Code branch (opencode-only, like agents).
- Real `mirror` does `rm -rf` dest first: running sync now replaces the upstream caveman plugin directory with ours. That is intended.
- `test.mjs` syncs along with the plugin folder; that is accepted (it is the smoke test, runnable from either location, and `mirror` has no exclude parameter).

- [ ] **Step 6: Update `AGENTS.md`**

1. Stack section, `**Content:**` bullet: append after "Single exception: `bin/skillctl`...": ` and one minimal opencode plugin (`plugins/caveman/plugin.js`, no dependencies)`.
2. File-layout tree: add a `plugins/` line between `bin/` and `commands/`:

```
├── plugins/                                  <- opencode plugins (caveman mode injector)
```

- [ ] **Step 7: Verify**

```bash
bin/skillctl check                                  # expected: pass
bin/skillctl sync --agent opencode                  # real sync; replaces upstream plugin dir
ls ~/.config/opencode/plugins/caveman/plugin.js     # expected: own plugin present
node plugins/caveman/test.mjs                       # expected: all PASS (repo copy; synced copy is identical)
bin/skillctl sync --check --agent opencode          # expected: no MISSING/STALE
```

- [ ] **Step 8: Commit**

```bash
git add plugins/caveman bin/skillctl AGENTS.md
git commit -m "feat(plugin): add minimal caveman mode plugin and skillctl plugins sync"
```

---

### Task 6: Config consolidation, external teardown, install doc

**Files:**
- Modify: `opencode-install.md` (repo); `~/.config/opencode/opencode.jsonc` (machine)
- Machine: copy graphify plugin, delete `~/.opencode/opencode.json`, `/home/ruben/tools/ponytail`, superpowers cache, stale caveman artifacts, cavecrew

**Depends:** Task 5

**Interfaces:**
- Consumes: own plugin at `~/.config/opencode/plugins/caveman/plugin.js` (Task 5 sync), own ponytail skill (Task 4), symlink-free stop-slop location (Task 3).
- Produces: single consolidated config; Task 7 verifies against it.

- [ ] **Step 1: Migrate graphify plugin and consolidate config**

```bash
cp ~/.opencode/plugins/graphify.js ~/.config/opencode/plugins/graphify.js
```

Edit `~/.config/opencode/opencode.jsonc` to final content:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "subagent_depth": 3,
  "experimental": {
    "subagent_depth": 3
  },
  "plugin": [
    "opencode-see-image@1.4.0",
    "./plugins/caveman/plugin.js",
    "./plugins/graphify.js"
  ]
}
```

- [ ] **Step 2: Validate config parses**

Run: `opencode models` (or `opencode --version` then start-and-quit if models is not a subcommand on this build).
Expected: model list or version output, no JSON parse error, no plugin load error mentioning caveman/graphify/see-image.

- [ ] **Step 3: Tear down external registrations and files** (config validated first)

```bash
rm ~/.opencode/opencode.json                      # drops superpowers + ponytail + old graphify reg
rm -rf /home/ruben/tools/ponytail                 # clone; own skill vendored in Task 4
rm -rf ~/.cache/opencode/npm/git-superpowers-*    # stale superpowers package cache
rm -f ~/.config/opencode/.caveman-active ~/.config/opencode/.caveman-opencode-ownership.json
rm -rf ~/.config/opencode/skills/cavecrew         # broken pack leftover
rm -rf ~/.config/opencode/skills/caveman-{commit,compress,help,review,stats}   # upstream pack skill dirs (own versions are commands, never skills; mirror cannot remove them)
rm -f ~/.config/opencode/commands/caveman*.md 2>/dev/null   # plural dir leftover, if it exists
ls ~/.config/opencode/command/ | grep caveman     # expected: own six command files only
ls ~/.config/opencode/skills/ | grep -i 'caveman\|cavecrew' # expected: caveman (own), no cavecrew
```

Leave `~/.opencode/package.json` and `node_modules/` in place (harmless npm artifacts; removal is a follow-up, not this task).

- [ ] **Step 4: Rewrite `opencode-install.md`**

Read it fully, then:
1. Replace the caveman npx install step with: own pack ships from this repo, `bin/skillctl sync --agent opencode` installs skill + commands + plugin; mode switching via `/caveman <level>`.
2. Replace the ponytail clone step (step 6 per external-skills.md note) with: vendored, arrives via `skillctl sync`.
3. Plugin registration section: single config `~/.config/opencode/opencode.jsonc` with the three entries from Step 1; note `~/.opencode/opencode.json` is retired.
4. Drop stale mentions of the superpowers plugin install if present; process skills come from this repo.
5. Em-dash scan: `grep -nP '\x{2014}' opencode-install.md`.

- [ ] **Step 5: Verify**

```bash
bin/skillctl check
bin/skillctl sync --check --agent opencode        # expected: no MISSING/STALE, exit 0; EXTRA warns for external skills (graphify, vercel-*, web-design-guidelines) and plugins/graphify.js are tolerated
grep -rn "superpowers\|ponytail\|cavecrew" ~/.config/opencode/opencode.jsonc   # expected: no hits
test ! -e ~/.opencode/opencode.json && echo "old config gone"
test ! -e /home/ruben/tools/ponytail && echo "clone gone"
```

- [ ] **Step 6: Commit**

```bash
git add opencode-install.md
git commit -m "docs(skills): consolidate opencode config to one file, retire external pack installs"
```

---

### Task 7: Final verification battery

**Files:** none (verification only; report findings, no commit unless a fix lands under the owning task)

**Depends:** Task 6

**Interfaces:**
- Consumes: everything landed in Tasks 1-6.
- Produces: verification report for the final execution report.

- [ ] **Step 1: Repo-side checks**

```bash
bin/skillctl check                          # expected: all pass
bin/skillctl sync --check --agent opencode  # expected: no MISSING/STALE
git log --oneline feat/vendor-external-packs ^main   # expected: 6 task commits
```

(Catalog cross-check is redundant: `skillctl check` rule C6 already fails on any skill missing from either catalog.)

- [ ] **Step 2: Machine-state checks**

```bash
cat ~/.config/opencode/opencode.jsonc                     # expected: 3 plugin entries as speced
ls ~/.config/opencode/plugins/                            # expected: caveman/ graphify.js
node plugins/caveman/test.mjs                             # expected: 4x PASS
ls ~/.config/opencode/skills/ | sort                      # expected: own set incl. caveman, stop-slop, ponytail, using-superpowers, verification-before-completion; no cavecrew
ls ~/.config/opencode/command/ | grep caveman | wc -l     # expected: 6
grep -rn "cavecrew" ~/.config/opencode/ 2>/dev/null       # expected: no hits
```

- [ ] **Step 3: Fresh-session checklist (hand to user in final report)**

Cannot be checked from inside a running session. User restarts opencode and confirms:
1. Skill list shows `caveman`, `stop-slop`, `ponytail`, `using-superpowers`, `verification-before-completion`; no superpowers-pack skills (test-driven-development, executing-plans etc. gone).
2. `/caveman ultra` then a reply: terse; `/caveman off`: normal prose.
3. Attach an image: `see_image` still works (see-image registration survived).
4. `/graphify` still available (plugin migrated).

---

## Self-review notes

- Spec coverage: spec components 1-7 map to Tasks 1-6 (+7 verification); superpowers plugin removal and clone deletion live in Task 6 as speced.
- No placeholders: every created file carries full content; modify-steps carry exact old/new text or exact commands with expected output.
- Interface consistency: state file, mode values, hook name, export shape, sync paths identical across Tasks 2, 5, 6, 7.
- Parallel readiness: catalog-file contention forces the serial chain 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7; only Task 1 has `Depends: none`, so the disjoint-files constraint is trivially satisfied.
