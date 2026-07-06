---
description: Reviews one completed task's changes against the plan or spec and for code quality. Read-only plus bash for running tests and verification; cannot edit files or dispatch subagents. Returns short actionable findings, not a redesign. Dispatch after each executor task for spec-compliance and code-quality review.
mode: subagent
color: warning
tools:
  write: false
  edit: false
  patch: false
  task: false
  webfetch: false
permission:
  edit: deny
  write: deny
  patch: deny
  task: deny
  webfetch: deny
  skill:
    "*": allow
    "brainstorming": deny
    "writing-plans": deny
    "executing-plans": deny
    "subagent-driven-development": deny
    "dispatching-parallel-agents": deny
    "multi-plan-orchestration": deny
    "finishing-a-development-branch": deny
    "using-git-worktrees": deny
    "requesting-code-review": deny
    "receiving-code-review": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
    "synctool-sync": deny
---
