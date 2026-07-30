# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

<!--
Grouping for this repo: continuous-delivery content catalog. Use [YYYY-MM-DD] headings per content milestone.
-->

---

## [Unreleased]

### Added

- `STANDARDS.md`: human-readable standards summary at repo root.
- `CHANGELOG.md`: this file.
- `.gitignore`: minimal (editor swap, OS files).
- `CLAUDE.md`: one-line shim that `@import`s `AGENTS.md` for Claude Code compatibility.
- `deep-research/`: end-to-end research pipeline skill (Hermes research profile). Intake → parallel gather (arxiv + web + own vault) → synthesized dossier with citations → brainstorm or Typst draft. Catalogue rows added in `README.md` (Skills table + Layout block) and `AGENTS.md` (Current skills table).
- `agents/`: opencode agent definitions (`orchestrator`, `executor`, `reviewer`) with per-agent skill denylists; inactive in the repo, copied to `~/.config/opencode/agents/` to activate. `commands/execute-plan.md` now maps implementer tasks to `executor` and reviews to `reviewer`.
- `agents/planner.md`, `agents/writer.md`, `agents/oracle.md`: planner primary (GLM 5.2; brainstorm > spec > plan > handoff; file writes glob-scoped to `docs/**`), writer primary (unpinned; focused doc/Typst sessions, no ceremony), oracle subagent (GLM 5.2; read-only two-strike consult). Spec: `docs/artifacts/specs/agent-roster/2026-07-12-agent-roster-redesign-design.md`.
- feat(agents): `inventree` opencode agent, port of the Claude Code subagent; homelab MCP registered machine-locally, `homelab*` denied in all other agents
- Single-pass `/full-cycle`: the planner dispatches the `orchestrator` subagent to execute the plan in the same run (prompt to final report, no approval gates). `no brainstorm` skips brainstorming; `handoff` keeps the old fresh-session handoff. Requires machine-local `subagent_depth: 2`. Spec: `docs/artifacts/specs/single-pass-full-cycle/2026-07-30-single-pass-full-cycle-design.md`.

### Changed

- Repo re-scoped from skills catalog to agent environment monorepo: the eight skill folders moved into a top-level `skills/` directory (`git mv`, history preserved). Catalogs, layout trees, and sync instructions updated in `README.md`, `AGENTS.md`, `STANDARDS.md`, `opencode-install.md`, and the two `SKILL.md` files with self-referencing sync steps.
- `AGENTS.md`: branch model `master` → `main`; added `synctool-sync` row to the Current skills table.
- `typst-pro`: bumped `@local/typst-tools` baseline `0.1.2` → `0.1.8` across skill examples, imports, and install paths. Factual references (fixed-in bug notes, rename reset point, version-numbering example, `@preview` pins) kept at `0.1.2`.
- `project-standardization`: graphify wiring is now presence-driven, not tier/CLI-gated. The `## Knowledge graph` section is kept in `AGENTS.md` on all tiers (including small) whenever `graphify-out/graph.json` exists, instead of only when the graphify CLI is found at a medium/large bootstrap. Section wording sharpened to an explicit "query graphify BEFORE grep/glob/Read" rule so agents stop reaching for grep when a graph is present (the gap that let a session grep instead of querying graphify). `references/bootstrap.md` step 10 now splits "keep the section" (presence-driven) from "build + hook" (CLI-driven).
- `multi-plan-orchestration`: hardened from the first real run (klad). Foundation plan now names frozen interfaces in its per-task Interfaces blocks; manifest template gains worktree setup for parallel SPs, expected-conflict hints, no-remote local-merge fallback, richer dispatch prompt slots, an integration dispatch prompt (fresh session, ordered `--no-ff` merges, explicit merge-to-base step), and an SP start gate defined as "F complete, verification green".
- `docs/workflow.md`: Large feature section documents the full multi-plan flow (outline approval → per-part specs/plans → manifest handoff → fresh session per dispatch prompt, integration never returns to the planner). Snapshot 2026-07-17.
- `agents/`: models pinned in frontmatter (orchestrator + executor on `minimax-coding-plan/MiniMax-M3`; reviewer cross-model on `zai-coding-plan/glm-5.2`). Orchestrator re-scoped to execution-only (description no longer claims plan-writing) with explore recon and oracle escalation. `commands/full-cycle.md` runs as `planner`; `commands/execute-plan.md` gains the oracle escalation rule.
- `docs/workflow.md`: rewritten opencode-primary. opencode is now the sole active harness, running `zai-coding-plan/glm-5.2` (planning, review, consult) and `minimax-coding-plan/MiniMax-M3` (orchestration, implementation) in a cross-model split. Claude Code demoted to supported-but-unused (kept via the `CLAUDE.md` shim and the `~/.claude/` sync paths in the catalog tables, not in daily use). Environment sections rebuilt opencode-centric: the seven custom agents, the homelab MCP, and ponytail/caveman/stop-slop output styles replace the old Claude-Code-only Plugins/Hooks/Subagents/MCP blocks. Snapshot 2026-07-30.
- `skill-harvest`: now opencode-only. Dropped the Claude Code JSONL source from `SKILL.md` and `references/extraction.md` (the jq Linux digest variant went with it); the opencode SQLite source is the sole input. State file's `claude-code` key is vestigial and ignored. `/harvest` command description plus the `README.md` and `AGENTS.md` catalog rows updated.
- `agents/orchestrator.md`: `mode: primary` to `mode: all` (now dispatchable by the planner); added explicit `task` (executor/reviewer/oracle/explore) and `todowrite` permissions so the task tool does not auto-deny them when the orchestrator runs as a subagent.
- `agents/planner.md`: end of pipeline dispatches the orchestrator instead of handing off; single-pass, no gates; `no brainstorm` and `handoff` keywords.
- `commands/full-cycle.md`: rewritten for single-pass; removed the `at once` gate-collapse special-case (gates are gone, so it was equivalent to the new default).

### Fixed

- `multi-plan-orchestration`: SP branch scheme `feat/<slug>/sp-N-<name>` was impossible; git cannot hold it alongside `feat/<slug>` (ref file/dir conflict, `fatal: cannot lock ref`). Now `feat/<slug>-spN-<name>`. Also removed em-dashes the edit introduced and the stale "not a prefix of any other existing branch" constraint that contradicted the new scheme.
- `deep-research`: frontmatter now uses only `name` + `description` (dropped Hermes-only `title`, `version`, `author`, `license`, `platforms`, `metadata` fields that other agents cannot parse). Description rewritten to start with "Use when..." so it matches the trigger-only convention in `AGENTS.md` § `SKILL.md` frontmatter rules. Body now opens with `## Overview` per the same section. Frontmatter total: 539 chars (was 884).

### TODO (backfill)

- Historical entries prior to this standardization pass are not yet captured. Backfill from `git log --oneline` when this file stabilises.

---

[Unreleased]: #unreleased
