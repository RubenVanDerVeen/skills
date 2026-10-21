---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

# Skill: Using Superpowers

Adapted from obra/superpowers (MIT).

## Overview

Skills carry the accumulated lessons of this environment. Invoking the right one before acting is mandatory, not optional.

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** - including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first - they set the approach, then implementation skills carry it out. Brainstorming and systematic-debugging are the most common process skills, but the rule holds for any of them.

- "Let's build X" -> brainstorming first, then implementation skills.
- "Fix this bug" -> systematic-debugging first, then domain skills.

## Red Flags

These thoughts mean STOP - you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent it. |
| "I know what that means" | Knowing the concept is not using the skill. Invoke it. |

## Tool Mapping for OpenCode

When skills request actions, substitute OpenCode equivalents:
- Create or update todos -> OpenCode v2 has no todo tool; track the plan in a markdown file (or the harness's plan facility) instead
- Subagent (general-purpose) -> subagent tool with agent "general" (description, prompt, optional background; sessionID continues a previous subagent)
- Invoke a skill -> OpenCode's native skill tool
- Read files -> read
- Create, edit, or delete files -> write to create or overwrite, edit for targeted changes, shell for deletion
- Run shell commands -> shell (command, workdir, timeout, background)
- Search files -> grep, glob
- Fetch a URL -> webfetch
- Search the web -> websearch
