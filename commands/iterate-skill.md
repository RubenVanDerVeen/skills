---
description: Refine a skill by running subagents with it, reviewing the real output, and editing the repo copy across N iterations
---

Iterate the `$ARGUMENTS` skill. Parse the skill name (first token) and an optional iteration count N (second token, default 3).

1. Load the target skill from THIS repo (the working copy under the skills directory), not the machine-installed copy.
2. For each of N iterations: dispatch a subagent that uses the skill to do its real job (compile a `.typ`, export a `.drawio` to `.png`/`.pdf`, run the skill's actual task). Give the subagent only the skill text and the task.
3. Inspect the artifact yourself (rendered PDF, exported image, generated file). Do not trust the subagent's self-report; look at the real output for mistakes.
4. From the observed failures, propose concrete edits to the skill's `SKILL.md` / `references/`, then apply them.
5. Feed the UPDATED repo copy of the skill to the next iteration's subagent. Never let the subagent discover the installed copy.
6. Summarise what changed across all iterations and which failure each edit fixes.

The repo copy is the source of truth. The installed copy lags, so it must never be the one iterated on.
