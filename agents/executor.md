---
description: Implements exactly one delegated task from an approved plan. Reads the relevant files, follows TDD where applicable, edits code, runs verification, and reports what changed and what was verified. Dispatch one executor per plan task. Cannot dispatch further subagents.
mode: subagent
color: success
tools:
  task: false
  webfetch: false
permission:
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
    "requesting-code-review": deny
    "skill-harvest": deny
    "find-skills": deny
    "deep-research": deny
    "project-standardization": deny
---
