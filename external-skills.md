---
name: external-skills
description: Use when looking up which external skills/tools are available beyond the personal skills in this repo, or when deciding which of superpowers, caveman, claude-mem, or graphify to reach for.
---

# external-skills

## Overview

Catalog of external skills and tools installed alongside opencode in this environment. Personal skills live as folders in this repo; the sources below come from elsewhere and are listed here for discovery and reference.

For install commands, see `opencode-install.md`.

## When to use

- "What is claude-mem / graphify / caveman / superpowers?"
- Picking which tool to reach for when several could apply.
- Briefing a new agent session on what is available.

## Sources

| Source | Type | What it does |
|---|---|---|
| superpowers | Skill system | Process discipline skills (TDD, debugging, brainstorming, ...) loaded by opencode, Claude Code, and friends. |
| caveman | Skill pack | Auxiliary skills loaded via `npx github:...`. |
| claude-mem | Plugin | Persistent cross-session memory. Captures tool observations, compresses them, re-injects relevant context into future sessions. |
| graphify | CLI | Builds a queryable knowledge graph (HTML viewer + JSON + Markdown report) from a folder of code, SQL, scripts, docs, PDFs, images, or video. |

## Per-source notes

### superpowers

Process-discipline skills for AI agents. Loaded automatically by opencode once installed; provides the meta-skill layer (using-superpowers, brainstorming, TDD, debugging, ...) that other skills and workflows assume.

Source: https://github.com/obra/superpowers

### caveman

Auxiliary skill pack installed via `npx -y github:JuliusBrussee/caveman -- --only opencode`. Complements superpowers with additional agent workflows.

Source: https://github.com/JuliusBrussee/caveman

### claude-mem

Persistent memory across sessions. Lifecycle hooks capture tool observations, an AI compression step summarises them, and relevant context is re-injected into future sessions. Supports Claude Code, OpenCode, Codex, Gemini, Hermes, etc.

Triggers: "I forgot what we did last session", "the agent has no continuity between runs", "I need to search past project observations".

Source: https://github.com/thedotmack/claude-mem

### graphify

Builds a queryable knowledge graph (interactive HTML viewer + `graph.json` + `GRAPH_REPORT.md`) from a folder of code, SQL, scripts, docs, PDFs, images, or video. The CLI ships an `opencode` install target that registers a `/graphify` skill and a hook that nudges the assistant to query the graph before grepping.

Triggers: "I need an overview of this codebase", "find the connections between these modules", "which parts touch the auth flow", "rebuild the project wiki from source".

Source: https://github.com/safishamsi/graphify

## Install

See `opencode-install.md` for the install order and commands.

## Related

- `opencode-install.md` in this repo: install commands for the four sources above + the personal skills repo path.
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
