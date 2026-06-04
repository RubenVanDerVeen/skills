---
name: opencode-install
description: Use when installing superpowers or caveman for opencode, bootstrapping a fresh opencode environment, or configuring opencode to load the user's personal skills from C:\Users\ruben\Projects\Tools\skills.
---

# opencode-install

## Overview

Bootstrap script for a fresh opencode install on this machine. Installs the two external skill sources (superpowers, caveman) and registers the personal skills repo so the user's own skills (`drawio-pro`, `typst-pro`, `rubens-project-standardization`, etc.) are picked up.

## When to use

- Setting up opencode on a new machine or after a clean reinstall.
- "How do I install superpowers / caveman?"
- opencode is not seeing the personal skills in `C:\Users\ruben\Projects\Tools\skills`.

## Install

Run the three commands below in order. They are all idempotent — re-running them is safe.

### 1. Superpowers

```
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

Source: https://github.com/obra/superpowers

### 2. Caveman

```
npx -y github:JuliusBrussee/caveman -- --only opencode
```

Source: https://github.com/JuliusBrussee/caveman

### 3. Point opencode at the personal skills repo

After both installs, make sure opencode loads skills from this repo's root:

```
C:\Users\ruben\Projects\Tools\skills
```

This is the location of the user's personally authored skills (`drawio-pro`, `typst-pro`, `rubens-project-standardization`, this one, ...). Without this entry, opencode will only see the globally installed superpowers + caveman skills and not the personal ones.

The exact configuration step depends on how opencode is set up to discover skills on Windows (check `~/.config/opencode/` or the opencode docs for the current skills-path mechanism). The directory above is the value that must end up registered.

## Verify

After all three steps, start a new opencode session and ask for a skill by name from each source:

- A superpowers skill (e.g. `test-driven-development`).
- A caveman skill.
- A personal skill from this repo (e.g. `drawio-pro`).

All three should resolve. If a personal skill is missing, re-check step 3.

## Related

- Working directory: `C:\Users\ruben\Projects\Tools\skills`
- Personal skills live in: `C:\Users\ruben\Projects\Tools\skills\<skill-name>\SKILL.md`
