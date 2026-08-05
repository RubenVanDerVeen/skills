# Agent roster redesign: planner, writer, oracle + model routing

Date: 2026-07-12
Status: approved (design approved in session, writer unpinned per user)

## Goal

Split the two jobs the `orchestrator` currently performs into dedicated agents, pin models per role so agent selection replaces manual model switching, and add two targeted specialists (`writer`, `oracle`). The flow becomes: Tab to `planner` (GLM 5.2) for spec + plan, hand off, fresh session runs `/execute-plan` as `orchestrator` (MiniMax M3) with `executor`/`reviewer`/`oracle` subagents. `writer` covers focused document sessions with no plan ceremony.

## Context (current state, 2026-07-12)

- `agents/` holds `orchestrator.md`, `executor.md`, `reviewer.md`; synced copies in `~/.config/opencode/agents/`. opencode 1.17.18.
- Mismatch: the orchestrator's body says "The plan is the spec; do not write a new one" while its frontmatter description claims "Brainstorms, writes plans", and the user in practice uses it for plan-writing sessions. Its edit/write/patch denies force plan files through bash redirects.
- No `model:` pins anywhere; the user manually switches GLM 5.2 (planning) and MiniMax M3 (execution) per session.
- opencode 1.17.18 ships a built-in read-only `explore` subagent (verified via `opencode agent list`); nothing dispatches it today. The `scout` built-in (external docs) is in newer releases, not this one.
- Model IDs available: `zai-coding-plan/glm-5.2`, `minimax-coding-plan/MiniMax-M3` (both flat-quota coding plans).
- Model rationale: GLM 5.2 (2026-06-13) leads on long-horizon planning benchmarks (SWE-bench Pro 62.1, MCP-Atlas 77.0); MiniMax M3 (2026-06-01) is near-par on execution (SWE-bench Pro 59.0), faster and cheaper, natively multimodal.

## Roster

| Agent | Mode | Model | Status | Job |
|---|---|---|---|---|
| `planner` | primary | `zai-coding-plan/glm-5.2` | new | brainstorm > spec > plan > handoff |
| `orchestrator` | primary | `minimax-coding-plan/MiniMax-M3` | edited | execute approved plan via subagents |
| `writer` | primary | unpinned (session model) | new | focused doc/Typst sessions, no ceremony |
| `executor` | subagent | `minimax-coding-plan/MiniMax-M3` | edited | implement one plan task |
| `reviewer` | subagent | `zai-coding-plan/glm-5.2` | edited | cross-model review of one task |
| `oracle` | subagent | `zai-coding-plan/glm-5.2` | new | read-only consult on 2-strike failures |
| `explore` | subagent | built-in, inherits | prompt-wired | codebase recon for planner/orchestrator |

## Agent requirements

### planner (new)

- Frontmatter: `mode: primary`, `color: accent`, `model: zai-coding-plan/glm-5.2`.
- Permissions: `edit`, `write`, `patch` as glob objects `{ "*": "deny", "docs/**": "allow" }` (last matching rule wins). Source code untouchable; spec/plan files under `docs/` writable directly, removing the bash-redirect workaround. `task`, `webfetch`, `bash` allowed. Do NOT set `tools: edit/write/patch: false` (that strips the schemas the docs globs need).
- Skills kept: `brainstorming`, `writing-plans`, `multi-plan-orchestration`, `deep-research`, `project-standardization`, ponytail suite.
- Skills denied: `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `finishing-a-development-branch`, `requesting-code-review`, `receiving-code-review`, `test-driven-development`, `skill-harvest`, `find-skills`, `stop-slop`, `synctool-sync`, `vercel-*`, `typst-pro`, `drawio-pro`, `altium-pro`, `web-design-guidelines`. Denying the execution suite mechanically enforces the plan-handoff-to-clean-session rule.
- Body (replaces default system prompt, same style/length as existing three): brainstorm intent, write spec to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-design.md`, gate, write plan to `docs/artifacts/features/<topic>/YYYY-MM-DD-<slug>-plan.md`, gate, then STOP and emit the handoff line `/execute-plan <plan-path>` for a fresh session. Dispatch `@explore` for codebase recon instead of self-grepping. Never implements; never continues into execution.

### writer (new)

- Frontmatter: `mode: primary`, `color: secondary`, no `model:` line (user picks per doc type).
- Permissions: full edit/write (documents are the deliverable, including school repos), `bash` allowed (typst compile/watch), `webfetch` allowed (citations), `task` allowed (`@explore` when a doc describes code).
- Skills kept: `typst-pro`, `drawio-pro`, `stop-slop`, `deep-research`, `synctool-sync`, `verification-before-completion`, ponytail suite.
- Skills denied: `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `multi-plan-orchestration`, `finishing-a-development-branch`, `requesting-code-review`, `receiving-code-review`, `test-driven-development`, `using-git-worktrees`, `systematic-debugging`, `skill-harvest`, `find-skills`, `project-standardization`, `vercel-*`, `altium-pro`, `web-design-guidelines`. Fat denylist is the token win: doc sessions stop paying for the full skill listing.
- Body: focused document work (Typst reports, README/docs, papers). Read context, write, verify: `typst compile` must pass for `.typ`; links resolve for `.md`. No spec/plan ceremony, no handoff, direct edits.

### oracle (new)

- Frontmatter: `mode: subagent`, `color: error`, `model: zai-coding-plan/glm-5.2`.
- Permissions: read-only plus bash (tests, git log); `edit`/`write`/`patch`/`task` denied (tools false + permission deny, same pattern as reviewer); `webfetch` ALLOWED (differs from reviewer: consults may need docs).
- Skills kept: `systematic-debugging` (core), ponytail suite (advice stays ponytail-aligned).
- Skills denied: planning suite, execution-process suite, review-workflow skills, domain skills (`typst-pro`, `drawio-pro`, `altium-pro`, `vercel-*`, `web-design-guidelines`, `stop-slop`, `synctool-sync`), `test-driven-development`, `skill-harvest`, `find-skills`, `deep-research`, `project-standardization`.
- Body: consult, not fixer. Input: failure context or architecture question. Output: ranked root-cause hypotheses, recommended approach, risks. Investigates read-only (run tests, read code, git history). Never edits, never dispatches.

### orchestrator (edit)

- Add `model: minimax-coding-plan/MiniMax-M3`.
- Description: drop "Brainstorms, writes plans"; it executes approved plans only.
- Body additions: dispatch `@explore` for codebase recon instead of self-grepping; escalation rule: when the same task fails verification twice or the reviewer rejects it twice, dispatch `oracle` with the full failure context and fold its recommendation into the next executor dispatch. Everything else unchanged.

### executor (edit)

- Add `model: minimax-coding-plan/MiniMax-M3`. Nothing else changes.

### reviewer (edit)

- Add `model: zai-coding-plan/glm-5.2`. Nothing else changes. Cross-model rationale: a different model family reviewing M3 diffs does not share the executor's blind spots; read-only + short output keeps quota impact small.

## Commands and docs sync

- `commands/full-cycle.md`: add one line mapping the command to the `planner` agent when available (mirrors execute-plan's agent-mapping line).
- `commands/execute-plan.md`: extend the agent-mapping paragraph with the oracle escalation rule (2-strike dispatch, read-only consult).
- `agents/README.md`: add planner/writer/oracle rows to the set table; note that the 2026-07-05 token measurements predate the new agents.
- `AGENTS.md`: update the agent names in the repo-layout comment and the "Agent definitions" section.
- `CHANGELOG.md`: entry under the current unreleased section.
- Sync: copy `agents/*.md` to `~/.config/opencode/agents/`, restart opencode, validate with `opencode agent list` (parses, all six custom agents present) and `opencode debug agent planner` (glob permissions resolved).

## Risks and fallbacks

- Edit-permission glob objects are documented for the current opencode release; 1.17.18 support is unverified. Validate via `opencode debug agent planner`; if globs are not honored, fall back to plain `allow` on edit/write/patch plus a hard body constraint ("only files under docs/"), and note the fallback in the commit message.
- GLM quota exhaustion mid-execution stalls reviewer/oracle; per-session model override remains the escape hatch.
- A non-empty agent body replaces opencode's default system prompt entirely; new bodies must carry full role identity, matching the style and length of the existing three.

## Out of scope (deliberately skipped)

- `librarian` (external docs subagent): the upcoming `scout` built-in covers it; adding it now creates a file to delete on upgrade.
- `designer` (frontend/UI subagent): no recurring frontend workload in this environment.
- Temperature tuning and `steps` caps: no observed problem to fix.
- Council/vision agents: M3 is natively multimodal already.
