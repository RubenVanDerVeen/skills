---
name: opencode-install
description: Use when installing the environment's external tools/skills (superpowers, caveman, claude-mem, graphify, markitdown, vercel-labs/agent-skills, stop-slop, gsd-core, ponytail) or configuring opencode to load the user's personal skills from C:\Users\ruben\Projects\Tools\skills.
---

# opencode-install

## Overview

Install steps for the external skill/tool sources (superpowers, caveman, claude-mem, graphify, markitdown, vercel-labs/agent-skills, stop-slop, gsd-core, ponytail) and the personal skills repo path. For what each source is and when to use it, see `external-skills.md`.

## When to use

- Setting up opencode on a new machine or after a clean reinstall.
- "How do I install superpowers / caveman / claude-mem / graphify / markitdown / vercel-labs / stop-slop / gsd-core / ponytail?"
- opencode is not seeing the personal skills in `C:\Users\ruben\Projects\Tools\skills`.

## Install

Run the commands below in order. They are all idempotent, re-running them is safe.

### 1. Superpowers

```
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

### 2. Caveman

```
npx -y github:JuliusBrussee/caveman -- --only opencode
```

### 3. Claude-Mem

The installer is interactive. Run it from your home directory, pick `opencode` from the IDE list, and follow the prompts:

```
cd ~
npx claude-mem install
```

### 4. Graphify

Requires Python 3.10+ and `uv` (install uv with `winget install astral-sh.uv` on Windows).

Run the install from your home directory, not from a project folder. `graphify install --platform opencode` writes its plugin into `<cwd>/.opencode/`, so launching it from a project pollutes that project with runtime config. The user-level install lands in `~/.config/opencode/opencode.jsonc`, alongside the `superpowers` plugin entry that is already there.

```
cd ~
uv tool install graphifyy
graphify install --platform opencode
```

### 5. Vercel-Labs Agent-Skills

Install the Vercel-curated React/Next.js/React Native/web-design skill pack. The installer is interactive and lets you pick which skills to include (deselect any you don't want, accept the defaults for the full pack):

```
npx skills add vercel-labs/agent-skills
```

The current environment has these five selected: `vercel-react-best-practices`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`, `vercel-composition-patterns`. See `external-skills.md` for what each does.

### 6. Stop-Slop

Single skill that strips AI writing patterns from prose. Aligned with this repo's house rule (no em-dashes), so it reinforces rather than contradicts `AGENTS.md`. The `--skill stop-slop` flag restricts the install to that one skill:

```
npx skills add hardikpandya/stop-slop --skill stop-slop
```

### 7. GSD Core

A spec-driven phase-loop framework (Discuss, Plan, Execute, Verify, Ship) with fresh-context subagents and cross-session state. Heavy install: ~60 `gsd-*` skills plus agents, hooks, and commands. The installer is interactive, pick `opencode` from the runtime list and choose `global` so the skills are available across all projects:

```
npx @opengsd/gsd-core@latest
```

See `external-skills.md` for what gsd-core does, the per-skill breakdown, and the overlap note with `superpowers`.

### 8. Ponytail

Lazy-dev philosophy + six skills (`ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`). Ponytail does not yet have an opencode installer; install is `git clone` + plugin-path entry.

```
git clone https://github.com/DietrichGebert/ponytail.git C:/tools/ponytail
```

Then register the opencode plugin in `~/.opencode/opencode.json` (the global one, not `~/.config/opencode/opencode.json`; opencode reads from both, the global plugin array lives in `~/.opencode/`). Add the plugin path to the `plugin` array:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "C:/tools/ponytail/.opencode/plugins/ponytail.mjs"
  ]
}
```

The plugin auto-activates `ponytail` at level `full` every session. Change the default via the env var `PONYTAIL_DEFAULT_MODE` (set to `lite`, `full`, `ultra`, or `off`) or via `~/.config/ponytail/config.json` (`{"defaultMode": "lite"}`). See `C:/tools/ponytail/skills/ponytail-help/SKILL.md` for the full reference.

### 9. MarkItDown

Standalone Python CLI (not an opencode plugin) that converts PDF, Word, Excel, PowerPoint, EPUB, HTML, images, and audio to Markdown so the agent can `Read` the result instead of choking on a binary file. Install with `uv` (already on PATH from the graphify step):

```
uv tool install 'markitdown[all]'
```

Usage the agent follows: `markitdown <file> -o <file>.md`, then `Read` the `.md`. The `[all]` extra pulls every format converter; use `[pdf,docx,xlsx]` for a leaner install. See `external-skills.md` for the full format list and triggers.

### 10. Point opencode at the personal skills repo

Make sure opencode loads skills from this repo's root:

```
C:\Users\ruben\Projects\Tools\skills
```

Without this entry, opencode will only see the globally installed superpowers + caveman skills and not the personal ones.

The exact configuration step depends on how opencode is set up to discover skills on Windows (check `~/.config/opencode/` or the opencode docs for the current skills-path mechanism). The directory above is the value that must end up registered.

## Verify

After all ten steps, start a new opencode session and confirm each source is reachable:

- A superpowers skill (e.g. `test-driven-development`).
- A caveman skill.
- claude-mem context: ask "what did we do last session?" and confirm past observations appear.
- A graphify skill: type `/graphify .` in the assistant and confirm a `graphify-out/` folder is produced.
- A vercel-labs skill (e.g. `vercel-react-best-practices`): ask for a React/Next.js review and confirm Vercel-specific guidance shows up.
- The `stop-slop` skill: paste a paragraph of AI-flavored prose and ask for a slop review.
- A gsd-core skill: invoke `gsd-new-project` (or `gsd-help`) and confirm the phase-loop workflow is reachable.
- The `ponytail` skill: ask for any coding task and confirm the response uses YAGNI/stdlib-first framing (the mode is active by default).
- `markitdown`: run `markitdown --help` and confirm it is on PATH (or convert a small `.pdf` and confirm Markdown output).
- A personal skill from this repo (e.g. `drawio-pro`).

If a personal skill is missing, re-check step 10.

## Related

- `external-skills.md` in this repo: what each source is and when to reach for it.
- Working directory: `C:\Users\ruben\Projects\Tools\skills`
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
