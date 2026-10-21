---
description: Switch caveman output level (lite, full, ultra, wenyan-lite, wenyan-full, wenyan-ultra, off)
---

Load the caveman skill first. Argument: $ARGUMENTS

- With a level: run `printf '%s' "<level>" > ~/.config/opencode/.caveman-mode`, then reply with exactly `CAVEMAN MODE SET: <level>` plus a one-line description of the level from the skill table.
- With `off`: run `printf '%s' "off" > ~/.config/opencode/.caveman-mode` (the plugin then injects an override line neutralizing the always-on base block), reply `CAVEMAN MODE OFF`, then write normal prose.
- Without argument: read the file if present, report the active level and the full level list, one line each.
