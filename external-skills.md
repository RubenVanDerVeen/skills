# external-skills

## Overview

Catalog of external skills and tools installed alongside opencode in this environment. Personal skills live as folders in this repo; the sources below come from elsewhere and are listed here for discovery and reference.

For install commands, see `opencode-install.md`.

## When to use

- "What is claude-mem / graphify / caveman / superpowers / vercel-* / stop-slop / gsd-core?"
- Picking which tool to reach for when several could apply.
- Briefing a new agent session on what is available.

## Sources

| Source | Type | What it does |
|---|---|---|
| superpowers | Skill system | Process discipline skills (TDD, debugging, brainstorming, ...) loaded by opencode, Claude Code, and friends. |
| caveman | Skill pack | Auxiliary skills loaded via `npx github:...`. |
| claude-mem | Plugin | Persistent cross-session memory. Captures tool observations, compresses them, re-injects relevant context into future sessions. |
| graphify | CLI | Builds a queryable knowledge graph (HTML viewer + JSON + Markdown report) from a folder of code, SQL, scripts, docs, PDFs, images, or video. |
| vercel-labs/agent-skills | Skill pack | Curated React/Next.js/React Native/web-design skills maintained by Vercel Engineering. |
| stop-slop | Single skill | Removes AI tells from prose: banned phrases, structural clichés, and sentence-level rules (no em-dashes, no Wh- starters, active voice). |
| gsd-core | Skill pack | Meta-prompting and spec-driven development framework. Runs a five-step phase loop (Discuss, Plan, Execute, Verify, Ship) with fresh-context subagents to avoid context rot. |

## Per-source notes

### superpowers

Process-discipline skills for AI agents. Loaded automatically by opencode once installed; provides the meta-skill layer (using-superpowers, brainstorming, TDD, debugging, ...) that other skills and workflows assume.

Source: https://github.com/obra/superpowers

### caveman

Cuts down output token usage and rewrites assistant prose in a terse, caveman style (short words, dropped articles, simple sentences). Useful when output is too verbose, when you want to minimise tokens on long sessions, or when you deliberately want the rough register. Installed via `npx -y github:JuliusBrussee/caveman -- --only opencode`. Complements superpowers with additional agent workflows.

Source: https://github.com/JuliusBrussee/caveman

### claude-mem

Persistent memory across sessions. Lifecycle hooks capture tool observations, an AI compression step summarises them, and relevant context is re-injected into future sessions. Supports Claude Code, OpenCode, Codex, Gemini, Hermes, etc.

Install: run `npx claude-mem install` from your home directory and select `opencode` from the interactive IDE list. See `opencode-install.md` for the full step.

Triggers: "I forgot what we did last session", "the agent has no continuity between runs", "I need to search past project observations".

Source: https://github.com/thedotmack/claude-mem

### graphify

Builds a queryable knowledge graph (interactive HTML viewer + `graph.json` + `GRAPH_REPORT.md`) from a folder of code, SQL, scripts, docs, PDFs, images, or video. The CLI ships an `opencode` install target that registers a `/graphify` skill and a hook that nudges the assistant to query the graph before grepping.

Install path note: run `graphify install --platform opencode` from your home directory (`~`), not from a project folder. The installer writes its plugin into `<cwd>/.opencode/`, so launching it from a project pollutes that project with runtime config. The user-level install lands in `~/.config/opencode/opencode.jsonc` alongside the `superpowers` plugin entry.

Triggers: "I need an overview of this codebase", "find the connections between these modules", "which parts touch the auth flow", "rebuild the project wiki from source".

Source: https://github.com/safishamsi/graphify

### vercel-labs/agent-skills

Curated skill pack from Vercel Engineering for building production React, Next.js, and React Native apps, plus web-design review. Installed via `npx skills add vercel-labs/agent-skills`; the installer drops selected skills into the opencode skills directory (the five listed below are the ones currently installed in this environment).

| Skill | What it covers |
|---|---|
| `vercel-react-best-practices` | React/Next.js performance rules: waterfalls, bundle size, server vs client data fetching, etc. Load when writing or reviewing React/Next.js code. |
| `vercel-react-native-skills` | React Native and Expo best practices for mobile: list performance, animations, native modules. |
| `vercel-react-view-transitions` | React View Transition API (`<ViewTransition>`, `addTransitionType`, CSS pseudo-elements). Load when adding page/element transitions. |
| `web-design-guidelines` | UI review against Web Interface Guidelines (accessibility, design, UX). Invoke on "review my UI", "audit design", "check accessibility". |
| `vercel-composition-patterns` | Scalable React composition patterns; refactors for boolean-prop proliferation, compound components, React 19 API changes. |

Triggers: "review my UI", "audit this React app", "how do I do view transitions in Next.js", "improve this React component's composition".

Source: https://github.com/vercel-labs/agent-skills

### stop-slop

Removes AI writing patterns from prose. Catches banned phrases (throat-clearing openers, business jargon, lazy adverbs, meta-commentary), structural clichés (binary contrasts, dramatic fragmentation, rhetorical setups, passive voice), and sentence-level rules (no Wh- starters, no em-dashes, no lazy extremes, active voice required). Ships a 1-10 scoring rubric across five dimensions (Directness, Rhythm, Trust, Authenticity, Density); below 35/50 means revise.

Triggers: "make this sound less like AI", "strip the AI tells from this draft", "review this prose for slop", "tighten this writing", "edit for natural voice".

Source: https://github.com/hardikpandya/stop-slop

### gsd-core

Context-engineering and spec-driven development framework. Solves "context rot" by running all heavy research, planning, and execution work in fresh-context subagents while keeping the main session lean. Each milestone repeats a five-step phase loop:

1. **Discuss** (`gsd-discuss-phase`) - capture decisions before planning.
2. **Plan** (`gsd-plan-phase`) - research, decompose, verify the plan fits one context.
3. **Execute** (`gsd-execute-phase`) - run plans in parallel waves, each executor starts with a clean 200k-token context.
4. **Verify** (`gsd-verify-work`) - walk through what was built, diagnose and fix before declaring done.
5. **Ship** (`gsd-ship`) - create the PR, archive the phase, repeat.

Survives session boundaries via structured artifacts (`STATE.md`, `CONTEXT.md`). Ships ~60 `gsd-*` skills for common sub-flows (`gsd-debug`, `gsd-add-tests`, `gsd-code-review`, `gsd-map-codebase`, `gsd-health`, `gsd-settings`, etc.). Entry point: `gsd-new-project` for greenfield, `gsd-new-milestone` for ongoing work.

Note on overlap: gsd-core's process discipline sits in the same slot as `superpowers`. They are largely compatible (both value TDD, planning, verification), but gsd-core is heavier and opinionated. Use gsd-core when you want the full phase loop with state files; fall back to superpowers for lighter, per-task discipline.

Triggers: "drive this project from spec to PR", "plan and ship a milestone", "I want fresh-context subagents for this work", "set up a spec-driven workflow", "verify and ship what we built".

Source: https://github.com/open-gsd/gsd-core
Install: `npx @opengsd/gsd-core@latest` (interactive, picks runtime + global/local).

## Install

See `opencode-install.md` for the install order and commands.

## Related

- `opencode-install.md` in this repo: install commands for the sources above + the personal skills repo path.
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
