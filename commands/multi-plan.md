---
description: Trigger multi-plan orchestration during brainstorming: split a too-large task into foundation + N parallel sub-plans
---

Load the `multi-plan-orchestration` skill and start the flow.

1. Take the topic or scope from the user's current request.
2. Check the trigger criteria from the skill's "When to use" section. Confirm with the user before proceeding if the fit is ambiguous.
3. If triggered, identify the shared foundation (or note that none exists).
4. Propose a split: foundation + N sub-projects.
5. Write the decomposition outline to `docs/artifacts/features/<topic>/YYYY-MM-DD-<topic>-outline.md`.
6. Stop and get user approval before writing any specs.

Do NOT dispatch execution agents. The orchestrator hands off at the manifest.