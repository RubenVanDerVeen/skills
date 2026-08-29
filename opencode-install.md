---
name: opencode-install
description: Use when installing the environment's external tools/skills (superpowers, caveman, graphify, markitdown, vercel-labs/agent-skills, stop-slop, ponytail, opencode-see-image) or syncing this repo's skills and commands into an agent's skills and commands directory.
---

# opencode-install

## Overview

Install steps for the external skill/tool sources (superpowers, caveman, graphify, markitdown, vercel-labs/agent-skills, stop-slop, ponytail, opencode-see-image) and the personal skills repo path. For what each source is and when to use it, see `external-skills.md`.

## When to use

- Setting up opencode on a new machine or after a clean reinstall.
- "How do I install superpowers / caveman / graphify / markitdown / vercel-labs / stop-slop / ponytail / opencode-see-image?"
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

### 3. Graphify

Requires Python 3.10+ and `uv` (install uv with `winget install astral-sh.uv` on Windows).

Run the install from your home directory, not from a project folder. `graphify install --platform opencode` writes its plugin into `<cwd>/.opencode/`, so launching it from a project pollutes that project with runtime config. The user-level install adds its plugin entry to the global opencode config under `~/.config/opencode/`; keep all plugin entries consolidated in `opencode.json` so they load reliably.

```
cd ~
uv tool install graphifyy
graphify install --platform opencode
```

### 4. Vercel-Labs Agent-Skills

Install the Vercel-curated React/Next.js/React Native/web-design skill pack. The installer is interactive and lets you pick which skills to include (deselect any you don't want, accept the defaults for the full pack):

```
npx skills add vercel-labs/agent-skills
```

The current environment has these five selected: `vercel-react-best-practices`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`, `vercel-composition-patterns`. See `external-skills.md` for what each does.

### 5. Stop-Slop

Single skill that strips AI writing patterns from prose. Aligned with this repo's house rule (no em-dashes), so it reinforces rather than contradicts `AGENTS.md`. The `--skill stop-slop` flag restricts the install to that one skill:

```
npx skills add hardikpandya/stop-slop --skill stop-slop
```

### 6. Ponytail

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

### 7. MarkItDown

Standalone Python CLI (not an opencode plugin) that converts PDF, Word, Excel, PowerPoint, EPUB, HTML, images, and audio to Markdown so the agent can `Read` the result instead of choking on a binary file. Install with `uv` (already on PATH from the graphify step):

```
uv tool install 'markitdown[all]'
```

Usage the agent follows: `markitdown <file> -o <file>.md`, then `Read` the `.md`. The `[all]` extra pulls every format converter; use `[pdf,docx,xlsx]` for a leaner install. See `external-skills.md` for the full format list and triggers.

### 8. opencode-see-image

Lets a text-only primary model (e.g. `zai-coding-plan/glm-5.3`) see images by routing them to a vision model. opencode normally rejects image attachments before a non-vision model ever runs; this plugin registers a `see_image` tool that sends the image to MiniMax-M3 and returns a text description the primary model reasons about.

```
opencode plugin opencode-see-image --global
```

Then set two persistent user env vars so the plugin reuses the existing `minimax-coding-plan` provider via opencode's SDK (auth handled automatically, no separate key):

```powershell
[Environment]::SetEnvironmentVariable('SEE_IMAGE_PROVIDER','minimax-coding-plan','User')
[Environment]::SetEnvironmentVariable('SEE_IMAGE_MODEL','MiniMax-M3','User')
```

Restart opencode from a fresh terminal so the new env vars are inherited. The plugin defaults to `opencode-go` (minimax-m3); setting `SEE_IMAGE_PROVIDER` overrides that. For the resolve order and other models, see `external-skills.md`.

### 9. Copy skills, commands, and agents into the agent's directories

The `skills/`, `commands/`, and `agents/` directories inside this repo are inactive by themselves; all three steps below are required per machine.

1. Copy each folder under `skills/` to the agent's skills directory (e.g. `~/.claude/skills/` for Claude Code, `~/.config/opencode/skills/` for opencode).
2. Copy each `commands/*.md` file to the agent's commands directory:

   | Agent | Global | Per-project |
   |---|---|---|
   | opencode | `~/.config/opencode/command/` (singular) | `.opencode/command/` |
   | Claude Code | `~/.claude/commands/` (plural) | `.claude/commands/` |

   opencode uses the singular `command/` directory; Claude Code uses plural `commands/`. Do not normalise across agents.

3. Copy each `agents/*.md` file (opencode agent definitions: `planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `doc-standardizer`, `code-standardizer`, `documenter`, `oracle`; `inventree` is optional and only on machines that register the homelab MCP server) to `~/.config/opencode/agents/` (global) or `.opencode/agents/` (per-project). opencode-only; Claude Code subagents use a different frontmatter format. Restart opencode afterwards; see `agents/README.md` for roles and tuning.


### 10. Enable the commit-msg hook

This repo ships a tracked `commit-msg` git hook (`.githooks/commit-msg`) that rejects non-Conventional-Commits messages, so agent-made and manual commits stay compliant. Git does not run hooks from a tracked directory until you point `core.hooksPath` at it. One-time per clone:

```
git config core.hooksPath .githooks
```

The hook is `sh` + `grep` only (no Node, no dependencies) and is tracked executable, so it works on Windows (via Git's bundled bash), macOS, and Linux. Emergency bypass: `git commit --no-verify`.

## Verify

After all nine steps, start a new opencode session and confirm each source is reachable:

- A superpowers skill (e.g. `test-driven-development`).
- A caveman skill.
- A graphify skill: type `/graphify .` in the assistant and confirm a `graphify-out/` folder is produced.
- A vercel-labs skill (e.g. `vercel-react-best-practices`): ask for a React/Next.js review and confirm Vercel-specific guidance shows up.
- The `stop-slop` skill: paste a paragraph of AI-flavored prose and ask for a slop review.
- The `ponytail` skill: ask for any coding task and confirm the response uses YAGNI/stdlib-first framing (the mode is active by default).
- `markitdown`: run `markitdown --help` and confirm it is on PATH (or convert a small `.pdf` and confirm Markdown output).
- The `opencode-see-image` plugin: attach an image to a GLM-5.3 session and confirm the `see_image` tool fires instead of a "does not support image input" rejection.
- A personal skill from this repo (e.g. `drawio-pro`).
- The custom agents: `opencode agent list` shows `planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `doc-standardizer`, `code-standardizer`, `documenter`, `oracle` (and `inventree` when the homelab MCP server is registered).

If a personal skill is missing, re-check step 9.

## Related

- `external-skills.md` in this repo: what each source is and when to reach for it.
- Working directory: `C:\Users\ruben\Projects\Tools\skills`
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\skills\<skill-name>\SKILL.md`
