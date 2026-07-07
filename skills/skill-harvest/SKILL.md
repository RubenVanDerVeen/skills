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
2. **Enumerate.** List sessions newer than the timestamp per source (commands in `references/extraction.md`), oldest first so the backlog drains FIFO and nothing is re-processed. Optional project argument filters by directory substring. Observer / synthetic dirs (`claude-mem-observer`, `observer-sessions`) and eval-harness dirs (`ai-harness-eval`, `.minimax` agent workspaces) are excluded by default; an explicit project filter overrides this. Cap 40 sessions per run; list the remainder in the report.
3. **Digest.** Run the extraction commands. Only user messages and interruption markers enter context (compaction summaries and subagent result blocks are dropped). Never read raw transcripts wholesale.
4. **Classify.** Keep a signal only if it appears in 2+ sessions, or is one explicit rule statement ("always X", "never Y", "stop doing Z").

| Type | Meaning | Action |
|---|---|---|
| fix-skill | repeated correction maps to an existing SKILL.md | propose concrete edit |
| new-skill | recurring friction, no skill matched | propose name + trigger description |
| memory | fact about user or project, not process | suggest memory write |
| config | "every time X" automation | flag for hook/settings, do not implement |

5. **Report.** Write `docs/artifacts/reviews/YYYY-MM-DD-harvest.md`: per finding its type, evidence quotes with session file references, target skill, sketched edit. Zero findings: short "nothing recurring" report.
6. **Approve, then apply.** Present findings as one multi-select question. Apply only chosen edits. New skills follow AGENTS.md "Adding or modifying a skill" in full. Ask before committing.
7. **Update state.** Set each source's timestamp to the mtime of the newest session processed in that batch (the FIFO cursor). Write even on zero-finding runs. If a source had no sessions to process, leave its timestamp unchanged.

## Hard rules

- Never bulk-read transcripts; digests only.
- Never auto-apply an edit, even a trivial one.
- Skipped source (e.g. opencode DB unreadable): note it in the report, do not advance that source's timestamp.
- Malformed JSONL lines: skip and report the count.

## Commands

| Command | Purpose |
|---|---|
| `/harvest [project]` | Run a harvest; optional project-name filter |

Sync: copy `commands/harvest.md` (top-level) to the agent commands directory (Claude Code `~/.claude/commands/`, OpenCode `~/.config/opencode/command/`). The file is dead weight inside the skills directory until copied.
