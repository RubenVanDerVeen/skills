---
description: Planning and dispatch only. Brainstorms, writes plans, dispatches executor subagents per task, reviews their results, manages the todo list. Cannot write, edit, or patch files; all implementation must go through subagents.
mode: primary
color: info
tools:
  write: false
  edit: false
  patch: false
permission:
  edit: deny
  write: deny
  patch: deny
  skill:
    "*": allow
    "vercel-*": deny
    "typst-pro": deny
    "drawio-pro": deny
    "altium-pro": deny
    "web-design-guidelines": deny
    "stop-slop": deny
    "synctool-sync": deny
    "test-driven-development": deny
---
