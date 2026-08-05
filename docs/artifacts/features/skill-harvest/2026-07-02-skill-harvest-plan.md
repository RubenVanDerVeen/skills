# skill-harvest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `skill-harvest` skill to this repo: an instruction-only meta-skill that mines recent Claude Code and opencode sessions for repeated corrections and skill gaps, reports findings, and applies approved edits.

**Architecture:** Pure markdown skill per approved spec (`docs/artifacts/specs/skill-harvest/2026-07-02-skill-harvest-design.md`). `SKILL.md` holds the lean flow, `references/extraction.md` holds verified extraction commands (PowerShell for Claude Code JSONL, sqlite3 for the opencode DB), `commands/harvest.md` is the `/harvest` entry point. No scripts, no runtime.

**Tech Stack:** Markdown, PowerShell 5.1 (extraction commands), sqlite3 CLI (opencode DB queries).

## Global Constraints

- No em-dashes (U+2014) in any file. Verify: `(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))` returns empty.
- Frontmatter: `name: skill-harvest` (kebab, matches folder), `description` starts with "Use when...", describes triggers only (never workflow), frontmatter total under 1024 chars.
- SKILL.md body starts with `## Overview`, body under 500 words.
- Skill files and catalog updates (README.md table + layout, AGENTS.md table) land in ONE commit (AGENTS.md rule: a skill absent from catalogs is incomplete). This overrides the frequent-commits default for Tasks 2-5.
- Commits: Conventional Commits 1.0.0. Plan-boundary commits are authorized by the approved spec + plan (repo carve-out).
- Extraction commands in Task 3 are verified against real data on this machine (2026-07-02); copy them verbatim.

---

### Task 1: Commit spec and plan artifacts

**Files:**
- Existing: `docs/artifacts/specs/skill-harvest/2026-07-02-skill-harvest-design.md`
- Existing: `docs/artifacts/plans/skill-harvest/2026-07-02-skill-harvest-plan.md` (this file)

**Interfaces:**
- Consumes: nothing.
- Produces: committed spec + plan that authorize later plan-boundary commits.

- [ ] **Step 1: Commit both docs**

```bash
git add docs/artifacts/specs/skill-harvest/ docs/artifacts/plans/skill-harvest/
git commit -m "docs(skill-harvest): add spec and plan artifacts"
```

Expected: 1 commit, 2 files added. Precedent: commit `0b6900c` did the same for multi-plan-orchestration.

---

### Task 2: Create `skill-harvest/SKILL.md`

**Files:**
- Create: `skill-harvest/SKILL.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the skill flow. Task 3 file is referenced as `references/extraction.md`; Task 4 command is documented in the `## Commands` section. State file contract: `~/.skill-harvest-state.json` with keys `claude-code` and `opencode`, ISO 8601 UTC values.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
---
name: skill-harvest
description: Use when the user wants to mine agent session history for lessons or skill improvements. Triggers: "/harvest", "harvest sessions", "mine sessions for lessons", "update skills from usage", "what keeps going wrong", "which skills need fixing", or after a stretch of heavy AI use when skills feel stale.
---

## Overview

Mines recent Claude Code and opencode sessions for repeated corrections, recurring friction, and unmet needs, then turns approved findings into edits to this skills repo. Instruction-only: every extraction command lives in `references/extraction.md`, run them via shell.

## When to use

- `/harvest` or any trigger above.
- Not for verifying a single skill after an edit; that stays the manual test-iteration loop.

## Flow

1. **State.** Read `~/.skill-harvest-state.json` (per-source ISO 8601 UTC timestamp of last run). Missing file: use a 30-day lookback and say so in the report.
2. **Enumerate.** List sessions newer than the timestamp per source (commands in `references/extraction.md`). Optional project argument filters by directory substring. Cap 40 sessions per run, newest first; list the remainder in the report.
3. **Digest.** Run the extraction commands. Only user messages and interruption markers enter context. Never read raw transcripts wholesale.
4. **Classify.** Keep a signal only if it appears in 2+ sessions, or is one explicit rule statement ("always X", "never Y", "stop doing Z").

| Type | Meaning | Action |
|---|---|---|
| fix-skill | repeated correction maps to an existing SKILL.md | propose concrete edit |
| new-skill | recurring friction, no skill matched | propose name + trigger description |
| memory | fact about user or project, not process | suggest memory write |
| config | "every time X" automation | flag for hook/settings, do not implement |

5. **Report.** Write `docs/artifacts/reviews/YYYY-MM-DD-harvest.md`: per finding its type, evidence quotes with session file references, target skill, sketched edit. Zero findings: short "nothing recurring" report.
6. **Approve, then apply.** Present findings as one multi-select question. Apply only chosen edits. New skills follow AGENTS.md "Adding or modifying a skill" in full. Ask before committing.
7. **Update state.** Write new timestamps, including on zero-finding runs. If the session cap was hit, set the timestamp to the oldest unprocessed session instead of now.

## Hard rules

- Never bulk-read transcripts; digests only.
- Never auto-apply an edit, even a trivial one.
- Skipped source (e.g. opencode DB unreadable): note it in the report, do not advance that source's timestamp.
- Malformed JSONL lines: skip and report the count.

## Commands

| Command | Purpose |
|---|---|
| `/harvest [project]` | Run a harvest; optional project-name filter |

Sync: copy `commands/harvest.md` to the agent commands directory (Claude Code `~/.claude/commands/`, OpenCode `~/.config/opencode/command/`). The subfolder is dead weight until copied.
````

- [ ] **Step 2: Verify frontmatter and body rules**

Run:

```powershell
$fm = (Get-Content skill-harvest\SKILL.md -Raw) -split '---'
$fm[1].Length
(Get-Content skill-harvest\SKILL.md | Select-Object -Skip 5 | Measure-Object -Word).Words
Select-String -Path skill-harvest\SKILL.md -Pattern ([char]0x2014)
```

Expected: frontmatter length under 1024; word count under 500; em-dash search returns nothing. Body starts with `## Overview`. Do not commit yet (single-commit rule, Task 6).

---

### Task 3: Create `skill-harvest/references/extraction.md`

**Files:**
- Create: `skill-harvest/references/extraction.md`

**Interfaces:**
- Consumes: state file contract from Task 2 (`~/.skill-harvest-state.json`, keys `claude-code`, `opencode`).
- Produces: runnable extraction commands referenced by SKILL.md step 2 and 3.

- [ ] **Step 1: Write the file with exactly this content**

````markdown
# extraction: session sources and commands

Verified on Windows 11 with PowerShell 5.1 and sqlite3 (msys64 ucrt64), 2026-07-02. Run PowerShell blocks in PowerShell, sql via the `sqlite3` CLI.

## State file

`~/.skill-harvest-state.json`:

```json
{ "claude-code": "2026-07-02T12:00:00Z", "opencode": "2026-07-02T12:00:00Z" }
```

Read (missing file: fall back to 30-day lookback):

```powershell
$statePath = "$env:USERPROFILE\.skill-harvest-state.json"
$since = if (Test-Path $statePath) { [datetime]::Parse((Get-Content $statePath -Raw | ConvertFrom-Json).'claude-code') } else { (Get-Date).AddDays(-30) }
```

Write (after a run; use the oldest-unprocessed-session time instead of now when the 40-session cap was hit):

```powershell
@{ 'claude-code' = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'); 'opencode' = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') } | ConvertTo-Json | Set-Content $statePath -Encoding utf8
```

## Source 1: Claude Code

Sessions: `~/.claude/projects/<encoded-project-dir>/<session-id>.jsonl`. Project dirs encode the working directory (`C--Users-ruben-projects-hobby-homelab`), so a project filter is a wildcard on the folder name.

Enumerate (newest first, capped):

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\projects\*\*.jsonl" | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime -Descending | Select-Object -First 40
```

With project filter: replace the first `*` with `*<project>*`.

Digest one file (user messages only; drops sidechains, skill payloads, system reminders, command wrappers; counts malformed lines):

```powershell
$skipped = 0
$digest = Get-Content $f.FullName | ForEach-Object {
  try { $j = $_ | ConvertFrom-Json } catch { $skipped++; return }
  if ($j.type -ne 'user' -or $j.isSidechain) { return }
  $t = if ($j.message.content -is [string]) { $j.message.content } else { ($j.message.content | Where-Object { $_.type -eq 'text' } | ForEach-Object { $_.text }) -join ' ' }
  if (-not $t) { return }
  if ($t -match '^(Base directory for this skill|<system-reminder>|<command-name>|<local-command)') { return }
  $t
}
```

Interruption markers (corrections; they arrive as user messages starting with `[Request interrupted by user`) survive these filters on purpose: an interruption immediately followed by a redirecting message is a strong correction signal.

## Source 2: opencode

Storage is SQLite: `~/.local/share/opencode/opencode.db`. Tables: `session` (id, parent_id, directory, title), `message` (session_id, time_created ms-epoch, data JSON with `role`), `part` (message_id, data JSON with `type`, `text`, `synthetic`).

User messages since a ms-epoch timestamp (top-level sessions only; `parent_id IS NULL` excludes subagent dispatch prompts, `synthetic` excludes injected content):

```sql
SELECT s.directory, m.session_id, json_extract(p.data,'$.text')
FROM part p
JOIN message m ON p.message_id = m.id
JOIN session s ON m.session_id = s.id
WHERE json_extract(m.data,'$.role') = 'user'
  AND json_extract(p.data,'$.type') = 'text'
  AND json_extract(p.data,'$.synthetic') IS NOT 1
  AND s.parent_id IS NULL
  AND m.time_created > :since_ms
ORDER BY m.time_created DESC;
```

Run:

```powershell
sqlite3 "$env:USERPROFILE\.local\share\opencode\opencode.db" "<query with :since_ms replaced by a number>"
```

Compute `:since_ms` from the state timestamp:

```powershell
[long](([datetime]::Parse($state.opencode).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds)
```

Project filter: add `AND s.directory LIKE '%<project>%'`. Apply the same `^Base directory for this skill` text filter defensively. DB missing or locked: skip the source, note it in the report, do not advance its timestamp.

## Linux variant (secondary)

Claude Code digest with jq, same filters:

```bash
jq -r 'select(.type=="user" and (.isSidechain|not)) | .message.content | if type=="string" then . else (map(select(.type=="text")|.text)|join(" ")) end' "$f" | grep -vE '^(Base directory for this skill|<system-reminder>|<command-name>|<local-command)'
```
````

- [ ] **Step 2: Smoke-test both extractions against real data**

Run the enumerate + digest PowerShell against the newest hermes-console session, and the sqlite3 query with `:since_ms` = `1750000000000`.

Expected: digest returns real user prompts (no skill payload text, no `<system-reminder>` blocks); sqlite3 returns rows whose first column is a project directory path. If either returns polluted or empty output, fix the command in the file, not in chat.

- [ ] **Step 3: Verify no em-dashes**

```powershell
Select-String -Path skill-harvest\references\extraction.md -Pattern ([char]0x2014)
```

Expected: no output. Do not commit yet.

---

### Task 4: Create `skill-harvest/commands/harvest.md`

**Files:**
- Create: `skill-harvest/commands/harvest.md`

**Interfaces:**
- Consumes: SKILL.md flow (Task 2).
- Produces: `/harvest` slash command after sync to the agent commands dir.

- [ ] **Step 1: Write the file with exactly this content**

```markdown
---
description: Mine recent Claude Code + opencode sessions for repeated corrections and skill gaps, then propose and apply approved skill edits
---

Load the `skill-harvest` skill from the personal skills repo and follow its Flow end to end.

1. Optional argument: `$ARGUMENTS` is a project-name filter (substring match on session project directories). Empty means all projects.
2. Deliverable: findings report at `docs/artifacts/reviews/YYYY-MM-DD-harvest.md`, approved edits applied, state file updated.
3. Do not skip the approval step; never auto-apply edits.
```

- [ ] **Step 2: Verify command file format**

Frontmatter has `description` only (no `name`). Body points at the skill, does not reimplement it. Matches the pattern of `rubens-project-standardization/commands/standardize.md`. Do not commit yet.

---

### Task 5: Update catalogs

**Files:**
- Modify: `README.md` (Skills table, after the `multi-plan-orchestration` row; Layout block)
- Modify: `AGENTS.md` (Current skills table, after the `multi-plan-orchestration` row)

**Interfaces:**
- Consumes: skill name + description from Task 2.
- Produces: discoverability; satisfies the AGENTS.md same-commit catalog rule.

- [ ] **Step 1: Add README.md Skills table row**

After the `multi-plan-orchestration` row, add:

```markdown
| [`skill-harvest`](./skill-harvest/SKILL.md) | Mines recent Claude Code + opencode sessions for repeated corrections and skill gaps; report, approve, apply. Slash command: `/harvest`. |
```

- [ ] **Step 2: Add README.md Layout entry**

In the Layout code block, after the `multi-plan-orchestration` entry, add:

```
└── skill-harvest/
    ├── SKILL.md
    ├── references/extraction.md
    └── commands/harvest.md
```

(Adjust the tree characters so only the last entry uses `└──`.)

- [ ] **Step 3: Add AGENTS.md Current skills table row**

After the `multi-plan-orchestration` row (before the two top-level doc rows), add:

```markdown
| `skill-harvest/` | `skill-harvest` | Mines recent Claude Code + opencode sessions for repeated corrections and skill gaps. Report, approve, apply loop with incremental state. Slash command: `/harvest`. |
```

- [ ] **Step 4: Cross-check catalog consistency**

```powershell
Select-String -Path README.md,AGENTS.md -Pattern 'skill-harvest' | Measure-Object | Select-Object -ExpandProperty Count
```

Expected: 4 or more matches spread over both files (red flag in AGENTS.md: skill in one catalog but not the other).

---

### Task 6: Repo-wide checks and single feat commit

**Files:**
- Commit: `skill-harvest/` (3 files), `README.md`, `AGENTS.md`

**Interfaces:**
- Consumes: Tasks 2-5 outputs.
- Produces: the shipped skill.

- [ ] **Step 1: Em-dash sweep over the whole repo**

```powershell
(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))
```

Expected: no output (pre-existing files were already clean).

- [ ] **Step 2: Commit everything together**

```bash
git add skill-harvest/ README.md AGENTS.md
git commit -m "feat(skills): add skill-harvest session-mining skill"
```

Expected: 1 commit, 5 files (3 new, 2 modified).

---

### Task 7: Acceptance run

**Files:**
- Create: `docs/artifacts/reviews/<run-date>-harvest.md` (by running the skill; use the actual run date)
- Create: `~/.skill-harvest-state.json` (outside repo)

**Interfaces:**
- Consumes: the shipped skill (Task 6).
- Produces: first real harvest report; validation per spec Testing section.

- [ ] **Step 1: Execute the SKILL.md Flow end to end, no project filter**

First run means no state file: use the 30-day lookback, note it in the report. Respect the 40-session cap (backlog: hermes-console 57, aardbei-plukkers 18, homelab 13, skills 11, synctool 8).

- [ ] **Step 2: Verify acceptance criteria from the spec**

- Report exists at `docs/artifacts/reviews/<run-date>-harvest.md` and contains at least one plausible `fix-skill` or `new-skill` finding with real evidence quotes, or an explicit "nothing recurring" statement.
- `~/.skill-harvest-state.json` exists with both source keys; timestamp reflects the cap rule if the cap was hit.
- No raw transcript was read wholesale during the run (digest commands only).

- [ ] **Step 3: Present findings for approval, apply chosen edits**

Follow SKILL.md steps 6-7. Skill edits from findings are new work items, not part of this plan.

- [ ] **Step 4: Commit the report**

```bash
git add docs/artifacts/reviews/<run-date>-harvest.md
git commit -m "docs(skill-harvest): first harvest report"
```

Expected: 1 commit. If findings were approved and applied to other skills, commit those separately per skill (`fix(<skill>): ...`), only with user approval per SKILL.md step 6.
