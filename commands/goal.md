---
description: Work toward a goal until a verifier passes
---

Goal: $ARGUMENTS

1. Detect the project's verifier (Makefile, package.json `test` script, pyproject.toml, Cargo.toml, etc.). If ambiguous, ask the user.
2. Iterate: implement, run the verifier, fix failures.
3. When green, summarise what changed.
4. If still red after several focused attempts, stop and report the blockers (not the obvious ones, the actual root cause).

The agent does the work. The command is just the entry point.
