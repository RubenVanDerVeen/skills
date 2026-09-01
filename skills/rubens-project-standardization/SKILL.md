---
name: project-standardization
description: Use when bootstrapping or restructuring a project for AI coding agents (opencode, Codex, Cursor, Aider, GitHub Copilot, Hermes, plus Claude Code via a CLAUDE.md shim): creating AGENTS.md + CLAUDE.md shim, scaffolding the on-demand subdirectory at `.agents/`, choosing directory layout, setting up `docs/artifacts/` for specs/plans/reviews/reports from any framework, seeding cross-session memory, or applying the ISO/IEC/IEEE + industry standards stack. Triggers: "set up agent context", "scaffold project", "bootstrap project", "standardize this repo", "create AGENTS.md", "create CLAUDE.md", "project layout", "init repo structure", "where should X go". Three project-size tiers (small/medium/large) with separate references so irrelevant guidance is not loaded.
---

## Overview

The user runs projects of different sizes: single-script utilities, multi-component homelab infra, full team school projects. Each tier needs a different amount of agent scaffolding. **Loading large-project guidance into a small repo is the failure mode this skill exists to prevent.**

This skill is **tool-agnostic**. It targets the [agents.md](https://agents.md) convention: `AGENTS.md` at the repo root, read on startup by most agents (opencode, Codex, Cursor, Aider, GitHub Copilot, Hermes). **Claude Code is the major exception**: it reads `CLAUDE.md` plus `@import`s, not `AGENTS.md` natively. Every bootstrap ships a one-line `CLAUDE.md` shim that `@import`s `AGENTS.md` so the cross-agent content is visible to Claude Code too. Tool filename lookup: `references/tool-filenames.md`.

## Triage: pick the tier first

Read `README.md`, list the top level, pick:

| Tier | Heuristics | Examples |
|------|-----------|----------|
| **small** | One author. One language / runtime. <30 source files. No sprints, no team. Single `AGENTS.md` is enough. | `Tools/synctool`, `Tools/TypstTools`, any single-script utility |
| **medium** | One author or tiny team. Multiple subsystems / services. Persistent state (DBs, containers, infra). Benefits from `.agents/<topic>.md` split + auto-imports. | `Hobby/Homelab` (Proxmox + ~10 VMs + containers + services) |
| **large** | Multi-person team. Sprints. Formal deliverables. Multi-discipline content. Needs `docs/{source,deliverables,components,artifacts,project-management}/`. | `Schoolprojects/Aardbei-Plukkers` (NHL Stenden IDP) |

When uncertain, **start one tier smaller**. Graduating up is cheap (move files into `.agents/`); graduating down is wasted work. Then read `references/<tier>.md`.

## Standards stack: the floor

Most projects adopt the conventions layer. Formal ISO/IEC/IEEE norms are opt-in per project (school deliverables → all of them; tools → just naming + commits + changelog).

- **kebab-case ASCII-only paths**: lowercase, hyphens, no spaces / underscores / PascalCase / non-ASCII. `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `STANDARDS.md` are conventional exceptions.
- **English structural paths**: dir / file names in English. Document *content* may be Dutch where the deliverable requires it.
- **ISO 8601 date prefix**: `YYYY-MM-DD-` first, e.g. `2026-05-08-standup.md`.
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0 + SemVer 2.0.0** (shipped-software projects): commits, changelog, and version numbers form one coherent floor. `<type>(<scope>): <description>`; `CHANGELOG.md` grouped by version or sprint; versions follow SemVer 2.0.0 strict (during 0.x, `0.X+1.0` MAY break, `0.X.Y+1` is backwards-compatible only). Commits are enforced by the `commit-msg` hook installed in bootstrap step 10. Version policy, bump triggers, and multi-source sync: `references/versioning.md`.

Rationale: `references/standards-stack.md`.

## Core rules

- **Auto-loaded budget**: `AGENTS.md` + auto-imports ≤ 5k tokens. **Minimize auto-imports to what every session actually needs**: when in doubt, on-demand table, not `@import`. Auto-imports fire every session whether the topic is relevant or not.
- **One authoritative source per deliverable** (ISO 10007): source in `docs/source/`, generated in `docs/deliverables/`. Never siblings.
- **No `temp/`, no `old/`, no `archive/`**: git history is the archive.
- **No secrets in any tracked file**: `.env`, tokens, passwords out of git. Memory included.
- **Specs and plans live in the repo**: `docs/artifacts/features/<feature>/` (specs, plans, manifests, reports) plus `docs/artifacts/reviews/` (flat log), committed alongside the code. **Override clause**: this wins over any per-framework default (superpowers, GSD, `.planning/`). See `references/artifacts.md` § Per-framework redirect for the redirect mechanics; redirect before files land elsewhere.
- **Memory ≠ plans ≠ tasks**: memory = cross-session facts; plans = committed artefacts; tasks = per-session in-tool items.

## Token budget

| Tier | `AGENTS.md` | auto-imports (when needed) | Total auto-loaded |
|------|-------------|----------------------------|--------------------|
| small | < 60 lines, ~1k tokens | none | < 1k tokens |
| medium | < 120 lines, ~2k tokens | < 2k tokens, every-session only | < 4k tokens |
| large | < 200 lines, ~3k tokens | < 2k tokens, every-session only | < 5k tokens |

Soft targets. Goal: small enough that an unrelated session still fits.

## References

| File | When to read |
|------|--------------|
| `references/bootstrap.md` | The 12-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS + README AI section → commit hook → graphify → verify) |
| `references/small.md` | Small project layout, AGENTS.md content, graduation triggers |
| `references/medium.md` | Medium project layout, auto-import vs on-demand, Homelab example |
| `references/large.md` | Large project layout, `docs/{source,deliverables,components,project-management}/`, sprint workflow |
| `references/standards-stack.md` | Standards application, ISO/IEC/IEEE rationale, Diátaxis decision |
| `references/artifacts.md` | `docs/artifacts/` setup, filename grammar, redirecting per-framework defaults |
| `references/versioning.md` | When the project ships versions (Tauri apps, CLIs, libraries, installers): SemVer 2.0.0 policy, bump triggers, multi-source sync, release-cut recipe |
| `references/memory.md` | Cross-session memory, `MEMORY.md` index, tool paths |
| `references/todolist.md` | `.agents/todolist.md` format, Plane sync |
| `references/tool-filenames.md` | Tool-specific filename / subdir aliases |
| `references/migration.md` | Migration from older `CLAUDE.md` / `claude/` / `rubens-project-standardization` |
| `references/restructure-flow.md` | Three-subagent explore-patch-verify dispatch protocol for `/standardize` on the restructure path (existing `AGENTS.md` detected) |

## Templates

| File | Purpose |
|------|---------|
| `templates/AGENTS-small.md` | Minimal context file (overview + key facts + **Git**) |
| `templates/AGENTS-medium.md` | Context file with auto-imports + on-demand table + **Git** |
| `templates/AGENTS-large.md` | Full context file + **Git** |
| `templates/CLAUDE.md` | One-line shim that `@import`s `AGENTS.md`. Copy to project root. |
| `templates/todolist.md` | Seed `.agents/todolist.md` |
| `templates/CHANGELOG.md` | Seed `CHANGELOG.md` |
| `templates/STANDARDS.md` | Human-readable standards summary |
| `templates/README-ai-assistance.md` | AI-assistance section appended to the project README: involvement level + skills-repo and workflow links |
| `templates/post-commit-graphify` | Debounced git hook: refresh `graphify-out/` graph after commits (AST-only, no LLM). Copy to `.git/hooks/post-commit`. |
| `templates/commit-msg` | Conventional Commits 1.0.0 enforcement hook (sh + grep, no deps). Copy to `.githooks/commit-msg`; see bootstrap step 10. |

## Commands

Slash commands associated with this skill. Source files live in the top-level `commands/` directory and are inactive until copied to the agent's commands directory.

| Command | Purpose |
|---------|---------|
| `/standardize` | Bootstrap or restructure a project. Triage the tier, then apply the full bootstrap checklist. |
| `/standardize-migrate` | Migrate an older project layout to the current agents.md convention. |

### Sync pattern

Agents do not auto-discover commands from the skills directory. Two-step sync:

1. Copy the `skills/rubens-project-standardization/` folder to the agent's skills directory (e.g. `~/.claude/skills/rubens-project-standardization/`).
2. Copy `commands/standardize.md` and `commands/standardize-migrate.md` to the agent's commands directory:

| Agent | Global | Per-project |
|-------|--------|-------------|
| OpenCode | `~/.config/opencode/command/` | `.opencode/command/` |
| Claude Code | `~/.claude/commands/` | `.claude/commands/` |

The command files are dead weight inside the skills directory until step 2.

## Anti-patterns

- Do not invent fields in `AGENTS.md` outside the template.
- Do not create `.agents/<file>.md` "just in case". Each must be referenced by auto-import or on-demand table.
- Do not put generated binaries (PDF, DOCX) next to sources. Source → `docs/source/`. Output → `docs/deliverables/`.
- Do not use Diátaxis as primary structure. See `references/standards-stack.md` §Diátaxis.
- Do not skip triage. Loading large guidance into a small repo is the documented failure mode.
- Do not duplicate this skill into `.agents/project-standardization.md`. Reference it.
- Do not write skill internals (bootstrap, triage, anti-patterns) into `STANDARDS.md`. That's for contributors.
- Do not let `CLAUDE.md` carry cross-agent content. It's a shim; duplicating creates two sources of truth.
- Do not let any planning framework (superpowers, GSD) drop artefacts outside `docs/artifacts/`. Redirect before files land elsewhere (see `references/artifacts.md` § Per-framework redirect).
- Do not let new modules, components, or skills land in the source tree without updating every catalog or table that lists the existing set. The template ships an "Adding features" section with red flags; fill it in at bootstrap with the project's actual catalogs. A new item that is not in the catalogs is incomplete.

- Do not bump a version source without also bumping every declared sync target in the same commit, and do not bump at all without a corresponding CHANGELOG entry.
- Do not adopt a release-automation tool that redefines the SemVer policy. The policy lives in `references/versioning.md`; the tool only applies it.

Older `rubens-project-standardization` / `project-standardization.md` projects: see `references/migration.md`.
