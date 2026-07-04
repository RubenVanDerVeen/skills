# external-skills

## Overview

Catalog of external skills and tools installed alongside opencode in this environment. Personal skills live as folders in this repo; the sources below come from elsewhere and are listed here for discovery and reference.

For install commands, see `opencode-install.md`.

## When to use

- "What is graphify / caveman / superpowers / markitdown / vercel-* / stop-slop / ponytail?"
- Picking which tool to reach for when several could apply.
- Briefing a new agent session on what is available.

## Sources

| Source | Type | What it does |
|---|---|---|
| superpowers | Skill system | Process discipline skills (TDD, debugging, brainstorming, ...) loaded by opencode, Claude Code, and friends. |
| caveman | Skill pack | Auxiliary skills loaded via `npx github:...`. |
| graphify | CLI | Builds a queryable knowledge graph (HTML viewer + JSON + Markdown report) from a folder of code, SQL, scripts, docs, PDFs, images, or video. |
| markitdown | CLI | Converts PDF/Word/Excel/PowerPoint/EPUB/HTML/images/audio to Markdown so the agent can read binary files. Standalone tool, called via Bash, not an opencode plugin. |
| vercel-labs/agent-skills | Skill pack | Curated React/Next.js/React Native/web-design skills maintained by Vercel Engineering. |
| stop-slop | Single skill | Removes AI tells from prose: banned phrases, structural clichés, and sentence-level rules (no em-dashes, no Wh- starters, active voice). |
| ponytail | Skill pack | Lazy-dev philosophy + six skills that force the laziest solution that works. Default mode (`full`) ships YAGNI-first output and bakes itself into every response. |

## Per-source notes

### superpowers

Process-discipline skills for AI agents. Loaded automatically by opencode once installed; provides the meta-skill layer (using-superpowers, brainstorming, TDD, debugging, ...) that other skills and workflows assume.

Source: https://github.com/obra/superpowers

### caveman

Cuts down output token usage and rewrites assistant prose in a terse, caveman style (short words, dropped articles, simple sentences). Useful when output is too verbose, when you want to minimise tokens on long sessions, or when you deliberately want the rough register. Installed via `npx -y github:JuliusBrussee/caveman -- --only opencode`. Complements superpowers with additional agent workflows.

Source: https://github.com/JuliusBrussee/caveman

### graphify

Builds a queryable knowledge graph (interactive HTML viewer + `graph.json` + `GRAPH_REPORT.md`) from a folder of code, SQL, scripts, docs, PDFs, images, or video. The CLI ships an `opencode` install target that registers a `/graphify` skill and a hook that nudges the assistant to query the graph before grepping.

Install path note: run `graphify install --platform opencode` from your home directory (`~`), not from a project folder. The installer writes its plugin into `<cwd>/.opencode/`, so launching it from a project pollutes that project with runtime config. The user-level install lands in `~/.config/opencode/opencode.jsonc` alongside the `superpowers` plugin entry.

Triggers: "I need an overview of this codebase", "find the connections between these modules", "which parts touch the auth flow", "rebuild the project wiki from source".

Source: https://github.com/safishamsi/graphify

### markitdown

Microsoft's lightweight Python CLI that converts files to Markdown for LLM consumption: PDF, Word, Excel, PowerPoint, EPUB, HTML, CSV/JSON/XML, images (EXIF + OCR), audio (transcription), and ZIP contents. Standalone tool, not an opencode plugin or skill; the agent calls it directly via Bash and then `Read`s the `.md` output.

Install: `uv tool install 'markitdown[all]'` (the `[all]` extra pulls every format converter; narrower extras like `[pdf,docx,xlsx]` are available).

Usage:

```
markitdown report.pdf -o report.md   # then Read report.md
```

Triggers: "read this PDF/Word/Excel deck", "summarise this PowerPoint", "convert this document to text", any time a binary office or PDF file needs to enter the agent's context.

Source: https://github.com/microsoft/markitdown

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

### ponytail

Lazy-dev philosophy + six skills. The base `ponytail` skill flips the assistant into a "lazy senior dev" mode by default (level: `full`) that pushes every response toward the smallest correct solution: YAGNI first, stdlib next, native platform features next, already-installed dependencies next, one line before fifty, and only then the minimum code that works. Five sibling skills cover the recurring workflows:

| Skill | What it does |
|---|---|
| `ponytail` | The mode itself. Auto-active by default; switch levels with `/ponytail lite|full|ultra`, deactivate with "stop ponytail". |
| `ponytail-review` | Diff-scoped over-engineering review. One finding per line: `<tag> <what to cut>. <replacement>.` Tags: `delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`. |
| `ponytail-audit` | Whole-repo over-engineering scan. Same tag vocabulary, ranked biggest cut first. |
| `ponytail-debt` | Harvests every `ponytail:` comment in the codebase into a debt ledger with ceiling + upgrade path per row. |
| `ponytail-gain` | One-shot benchmark scoreboard (code lines, cost, speed). Honest boundary: never reports a per-repo number. |
| `ponytail-help` | Quick-reference card: levels, commands, deactivate, update, configure default mode. |

Ponytail governs what gets built, not how the assistant talks (pair with `caveman` for terse prose). Never simplifies away trust-boundary validation, error handling that prevents data loss, security, accessibility basics, or anything explicitly requested.

Triggers: "make this less over-engineered", "simplify this", "I want a lazy review", "is this over-engineered?", "review for over-engineering", "audit this codebase for bloat", "what can I delete from this repo", "show ponytail debt", "what did we defer", "show ponytail impact", "ponytail help".

Source: https://github.com/DietrichGebert/ponytail
Install: see `opencode-install.md` step 6. Manual install (current setup) is `git clone https://github.com/DietrichGebert/ponytail.git C:/tools/ponytail` and add `"C:/tools/ponytail/.opencode/plugins/ponytail.mjs"` to the `plugin` array in `~/.opencode/opencode.json`.

## Install

See `opencode-install.md` for the install order and commands.

## Related

- `opencode-install.md` in this repo: install commands for the sources above + the personal skills repo path.
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
