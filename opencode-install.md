---
name: opencode-install
description: Use when installing the environment's external tools (graphify, markitdown, vercel-labs/agent-skills, opencode-see-image) or syncing this repo's vendored packs (caveman, stop-slop, ponytail, the superpowers leftovers) plus skills, commands, agents, and plugins into an agent's directories.
---

# opencode-install

## Overview

Install steps for the external tools (graphify, markitdown, vercel-labs/agent-skills, opencode-see-image) and for the packs that now ship from this repo (caveman, stop-slop, ponytail, the superpowers leftovers). For what each source is and when to use it, see `external-skills.md`.

## When to use

- Setting up opencode on a new machine or after a clean reinstall.
- "How do I install graphify / markitdown / vercel-labs / opencode-see-image?" (external tools)
- "How do I install caveman / stop-slop / ponytail / the superpowers leftovers?" (vendored in this repo, installed by the sync step)
- opencode is not seeing the personal skills in `C:\Users\ruben\Projects\Tools\skills`.

## Install

Run the commands below in order. They are all idempotent, re-running them is safe.

### 1. Caveman

Vendored in this repo: the skill in `skills/caveman/`, the six command files in `commands/caveman*.md`, and the minimal mode plugin in `plugins/caveman/`. Install it with the sync step (step 8):

```
bin/skillctl sync --agent opencode
```

Switch the active level with `/caveman <level>` (`off`, `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`). The command writes the level to `~/.config/opencode/.caveman-mode`; the plugin reads that file and injects the matching rules on each turn.

### 2. Graphify

Requires Python 3.10+ and `uv` (install uv with `winget install astral-sh.uv` on Windows).

Run the install from your home directory, not from a project folder. `graphify install --platform opencode` writes its plugin into `<cwd>/.opencode/`, so launching it from a project pollutes that project with runtime config.

```
cd ~
uv tool install graphifyy
graphify install --platform opencode
```

The installer leaves the plugin file at `~/.opencode/plugins/graphify.js`. The plugin is not registered: opencode v2 refuses it (`Plugin must export a default definition with an id and an effect or setup function`, the upstream file is a v1 shape). The graphify skill and CLI are untouched, so `/graphify` stays available through the skill.

### 3. Vercel-Labs Agent-Skills

Install the Vercel-curated React/Next.js/React Native/web-design skill pack. The installer is interactive and lets you pick which skills to include (deselect any you don't want, accept the defaults for the full pack):

```
npx skills add vercel-labs/agent-skills
```

The current environment has these five selected: `vercel-react-best-practices`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`, `vercel-composition-patterns`. See `external-skills.md` for what each does.

### 4. Stop-Slop

Vendored in this repo as `skills/stop-slop/`: one skill that strips AI writing patterns from prose. Aligned with this repo's house rule (no em-dashes), so it reinforces rather than contradicts `AGENTS.md`. It arrives with the sync step (step 8), so there is no separate install to run.

### 5. Ponytail

Vendored in this repo as `skills/ponytail/`: the lazy-dev lens (YAGNI, standard library first, shortest working diff) that `agents/lazy-dev.md` points at. It arrives with the sync step (step 8), so there is no clone to make and no plugin to register; the ponytail plugin and the `C:/tools/ponytail` clone are retired.

The skill loads on demand for coding work, and the `lazy-dev` agent applies it as a plan gate. There is no default mode and no auto-activation.

### 6. MarkItDown

Standalone Python CLI (not an opencode plugin) that converts PDF, Word, Excel, PowerPoint, EPUB, HTML, images, and audio to Markdown so the agent can `Read` the result instead of choking on a binary file. Install with `uv` (already on PATH from the graphify step):

```
uv tool install 'markitdown[all]'
```

Usage the agent follows: `markitdown <file> -o <file>.md`, then `Read` the `.md`. The `[all]` extra pulls every format converter; use `[pdf,docx,xlsx]` for a leaner install. See `external-skills.md` for the full format list and triggers.

### 7. opencode-see-image

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

### 8. Sync skills, commands, agents, and plugins into the agent's directories

The `skills/`, `commands/`, `agents/`, and `plugins/` directories inside this repo are inactive by themselves; sync them to the agent's directories with the shipped CLI. Run from the clone root:

```
bin/skillctl sync
```

Use `bin/skillctl sync --check` for a dry run that reports drift without changing anything, and `--agent opencode` or `--agent claude` to sync one agent only. The CLI mirrors skills, commands, agents, and plugins to the correct directories for opencode (`~/.config/opencode/skills/`, `~/.config/opencode/command/` singular, `~/.config/opencode/agents/`, `~/.config/opencode/plugins/`) and skills plus commands to Claude Code (`~/.claude/skills/`, `~/.claude/commands/` plural). opencode-only agents and plugins are never copied to Claude Code. Restart opencode afterwards so the new agents and plugins load; see `agents/README.md` for roles and tuning.

#### Windows notes

The CLI is a bash script written on Linux; on this Windows machine it runs under Git Bash with these verified differences (verified 2026-10-20):

- PowerShell cannot run `./bin/skillctl` directly: `bash` is not on PATH and the extensionless file has no launcher. Invoke it through Git Bash's full path, adjusting the clone path if needed:

  ```powershell
  & "C:\Program Files\Git\bin\bash.exe" -c "cd /c/Users/ruben/projects/tools/skills && ./bin/skillctl sync"
  ```

- The checkout has CRLF line endings (`core.autocrlf=true`, no `.gitattributes`). This is tolerated: MSYS2 bash translates line endings transparently, so the script and the `check` rules (C1 em-dash scan included) behave exactly as on Linux. Do not hand-convert the endings; git rewrites them on checkout anyway.
- `$HOME` inside Git Bash resolves to `C:\Users\ruben`, so the sync lands in `C:\Users\ruben\.config\opencode\` and `C:\Users\ruben\.claude\`, matching the Linux layout.
- Behavior verified identical to Linux: `sync` mirrored 70 items, `sync --check` reported 0 missing / 0 stale / 0 extra, `check` passed with 0 fail and only the 3 expected C7 warns (universal commands without a parent skill).


### 9. Enable the git hooks

This repo ships tracked git hooks (`.githooks/`) that reject non-Conventional-Commits messages, em-dashes in markdown, malformed SKILL.md frontmatter, new skills missing from the catalogs, and forbidden paths, so agent-made and manual commits stay compliant. Git does not run hooks from a tracked directory until you point `core.hooksPath` at it. One-time per clone:

```
git config core.hooksPath .githooks
```

The hook is `sh` + `grep` only (no Node, no dependencies) and is tracked executable, so it works on Windows (via Git's bundled bash), macOS, and Linux. Emergency bypass: `git commit --no-verify`.

## Plugin registration

All opencode plugin entries live in one file: `~/.config/opencode/opencode.jsonc`. The legacy `~/.opencode/opencode.json` is retired, it only carried the superpowers and ponytail registrations.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "subagent_depth": 3,
  "experimental": {
    "subagent_depth": 3
  },
  "plugin": [
    "opencode-see-image@1.4.0"
  ]
}
```

The caveman plugin needs no config entry. opencode auto-discovers every folder under `~/.config/opencode/plugins/` and resolves it as `server.js` or `index.js`, so the sync step (step 8) drops it at `~/.config/opencode/plugins/caveman/index.js` and opencode loads it from there. Adding a config entry for it would load it twice.

Restart opencode after editing the config, the plugin set reloads on start.

## Verify

After all nine steps, start a new opencode session and confirm each source is reachable:

- A vendored process skill (e.g. `brainstorming`).
- A caveman skill.
- A graphify skill: type `/graphify .` in the assistant and confirm a `graphify-out/` folder is produced.
- A vercel-labs skill (e.g. `vercel-react-best-practices`): ask for a React/Next.js review and confirm Vercel-specific guidance shows up.
- The `stop-slop` skill: paste a paragraph of AI-flavored prose and ask for a slop review.
- The `ponytail` skill: ask for any coding task and confirm the response uses YAGNI/stdlib-first framing (the skill loads on demand, there is no ponytail plugin and no default mode).
- `markitdown`: run `markitdown --help` and confirm it is on PATH (or convert a small `.pdf` and confirm Markdown output).
- The `opencode-see-image` plugin: attach an image to a GLM-5.3 session and confirm the `see_image` tool fires instead of a "does not support image input" rejection.
- A personal skill from this repo (e.g. `drawio-pro`).
- The custom agents: `opencode agent list` shows `planner`, `orchestrator`, `writer`, `executor`, `reviewer`, `doc-standardizer`, `code-standardizer`, `documenter`, `oracle` (and `inventree` when the homelab MCP server is registered).

If a personal skill is missing, re-check step 8.

## Related

- `external-skills.md` in this repo: what each source is and when to reach for it.
- Working directory: `C:\Users\ruben\Projects\Tools\skills`
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\skills\<skill-name>\SKILL.md`
