# skill-harvest Skill Design

**Date:** 2026-07-02
**Status:** Approved (design sections reviewed and accepted in brainstorming session)
**Target location:** `skill-harvest/` in this repo

## Overview

A meta-skill that mines recent agent sessions (Claude Code and opencode) for repeated corrections, recurring friction, and unmet needs, then turns them into concrete maintenance actions on this skills repo: edits to existing `SKILL.md` files, new-skill candidates, memory suggestions, or config/hook flags. It systematizes the iterate-after-testing loop the user already runs by hand (see commit history: "after 3 test iterations", "corrections from 10 iterations of testing").

**Core principle:** the skill is instruction-only markdown (approach A). Extraction commands live as code blocks in a reference file; the agent runs them via shell. No shipped scripts, no runtime, per repo convention.

## Approved decisions

| Decision | Choice |
|---|---|
| Target gap | Skill-harvest loop (over harness-eval, firmware, agent-sync) |
| Data sources | Claude Code session JSONL + opencode session storage |
| Output model | Report first, user approves per finding, then apply |
| Run scoping | Incremental: since-last-harvest state file |
| Implementation | Instruction-only skill, extraction commands embedded as code blocks |

## Package shape

```
skill-harvest/
├── SKILL.md                  <- lean flow, under 500 words
├── references/
│   └── extraction.md         <- per-source session paths, discovery notes, jq/PowerShell extraction commands
└── commands/
    └── harvest.md            <- /harvest slash command, optional project-name argument as filter
```

Catalogs updated in the same commit: `README.md` Skills table, `AGENTS.md` Current skills table, Layout blocks. Frontmatter `description` starts with "Use when...", triggers on: "harvest sessions", "mine sessions for lessons", "update skills from usage", "what keeps going wrong", "/harvest".

## Flow (what SKILL.md instructs)

1. **Read state.** `~/.skill-harvest-state.json` holds a last-run ISO 8601 timestamp per source. File missing: default lookback of 30 days, say so in the report.
2. **Enumerate sessions.** Claude Code: `~/.claude/projects/*/*.jsonl` with mtime newer than last run. opencode: session storage directory (exact path discovered at run time; documented in `references/extraction.md`). Optional `/harvest <project>` argument filters to matching project directories. Cap roughly 40 sessions per run; list the remainder in the report so the next run picks them up.
3. **Digest, never bulk-read.** Run the extraction commands from `references/extraction.md` to pull only: user messages, interruption events, and tool permission denials. Raw transcripts are never read wholesale; the agent analyzes the compact digest.
4. **Classify findings.** Threshold: a signal must appear in 2 or more sessions, or be one explicit rule statement from the user ("always X", "never Y", "stop doing Z"). Four types:
   - `fix-skill`: repeated correction maps to an existing SKILL.md; propose a concrete edit.
   - `new-skill`: recurring friction with no matching skill; propose candidate name plus trigger description.
   - `memory`: a fact about the user or a project, not a process rule; suggest a memory write instead of a skill change.
   - `config`: "every time X do Y" automation; belongs in a hook or settings, flag only, do not implement.
5. **Write report.** `docs/artifacts/reviews/YYYY-MM-DD-harvest.md`. Per finding: type, evidence quotes with session references, target skill (if any), sketched edit. Zero findings: short "nothing recurring" report.
6. **Approve, then apply.** Present findings via structured question (one batch, multi-select). Apply only chosen edits. New skills follow the full "Adding or modifying a skill" rule in `AGENTS.md` (catalogs, frontmatter checks). Ask before committing; the repo default (no commit without explicit user instruction) applies.
7. **Update state.** Write the new timestamp per source, including after zero-finding runs.

## Error handling

- opencode storage missing or unreadable: skip that source, note the skip in the report, still update the Claude Code timestamp only.
- Session cap exceeded: process newest first, list unprocessed sessions in the report, leave state timestamp at the oldest unprocessed session so nothing is silently dropped.
- Malformed JSONL lines: skip the line, count skips in the report.

## Out of scope

- No automation or scheduled runs; `/harvest` is always user-initiated.
- No auto-applied edits, even trivial ones.
- No mining of claude-mem observations or skills-repo git history (considered, cut: lossy or redundant with session data).
- The skill edits skills; it does not execute or test them. Verifying an edited skill stays the user's existing test-iteration loop.

## Testing

First real run against the current backlog (hermes-console 57 sessions, aardbei-plukkers 18, homelab 13, skills 11, synctool 8) is the acceptance test. Expected outcome: at least one plausible `fix-skill` or `new-skill` finding with real evidence, report readable, state file written. Iterate SKILL.md afterwards, matching the user's usual pattern.
