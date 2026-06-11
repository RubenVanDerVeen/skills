---
name: opencode-install
description: Use when installing superpowers, caveman, claude-mem, or graphify for opencode, or when configuring opencode to load the user's personal skills from C:\Users\ruben\Projects\Tools\skills.
---

# opencode-install

## Overview

Install steps for the external skill/tool sources (superpowers, caveman, claude-mem, graphify) and the personal skills repo path. For what each source is and when to use it, see `external-skills.md`.

## When to use

- Setting up opencode on a new machine or after a clean reinstall.
- "How do I install superpowers / caveman / claude-mem / graphify?"
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

```
npx claude-mem install --ide opencode
```

### 4. Graphify

Requires Python 3.10+ and `uv` (install uv with `winget install astral-sh.uv` on Windows).

```
uv tool install graphifyy
graphify opencode install
```

### 5. Point opencode at the personal skills repo

Make sure opencode loads skills from this repo's root:

```
C:\Users\ruben\Projects\Tools\skills
```

Without this entry, opencode will only see the globally installed superpowers + caveman skills and not the personal ones.

The exact configuration step depends on how opencode is set up to discover skills on Windows (check `~/.config/opencode/` or the opencode docs for the current skills-path mechanism). The directory above is the value that must end up registered.

## Verify

After all five steps, start a new opencode session and confirm each source is reachable:

- A superpowers skill (e.g. `test-driven-development`).
- A caveman skill.
- claude-mem context: ask "what did we do last session?" and confirm past observations appear.
- A graphify skill: type `/graphify .` in the assistant and confirm a `graphify-out/` folder is produced.
- A personal skill from this repo (e.g. `drawio-pro`).

If a personal skill is missing, re-check step 5.

## Related

- `external-skills.md` in this repo: what each source is and when to reach for it.
- Working directory: `C:\Users\ruben\Projects\Tools\skills`
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
