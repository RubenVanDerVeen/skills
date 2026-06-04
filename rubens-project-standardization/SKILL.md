---
name: rubens-project-standardization
description: Use when bootstrapping or restructuring a project for Claude Code — creating `CLAUDE.md`, scaffolding `claude/`, choosing directory layout, setting up `docs/artifacts/` for specs/plans/reviews, seeding the cross-session memory directory, or applying the ISO/IEC/IEEE + industry standards stack (kebab-case paths, ISO 8601 dates, Conventional Commits, Keep a Changelog). Triggers: "set up Claude context", "scaffold project", "bootstrap project", "standardize this repo", "create CLAUDE.md", "project layout", "init repo structure", "where should X go". Covers three project-size tiers (small / medium / large) with separate references so the irrelevant guidance is not loaded. Replaces the older `project-standardization.md`.
---

# Ruben's project standardization skill

The user runs many projects of different sizes — single-script utilities, multi-component homelab infra, and full team school projects. Each tier needs a different amount of Claude scaffolding. **Loading large-project guidance into a small repo is the failure mode this skill exists to prevent.**

This skill provides:

1. A triage step that picks the right tier (small / medium / large).
2. A bootstrap checklist that scaffolds only what the chosen tier needs.
3. Tier-specific references (loaded on demand, not preloaded).
4. A shared standards layer (naming, dates, commits, changelog) that applies to **most** projects regardless of tier.

## Triage — pick the tier first

Before doing anything else, decide which tier this project is. Read `README.md`, list the top-level directory, and pick:

| Tier | Heuristics | Typical examples |
|------|-----------|------------------|
| **small** | One author. One language / runtime. <30 source files. No sprints, no team, no formal deliverables. Single `CLAUDE.md` is enough. | `Tools/synctool` (Tauri+Svelte desktop app), `Tools/TypstTools` (Typst package), any single-script utility |
| **medium** | One author or tiny team. Multiple subsystems or services. Persistent state (DBs, container hosts, infra). Benefits from `claude/<topic>.md` split + `@imports`. | `Hobby/Homelab` (Proxmox + ~10 VMs + containers + services) |
| **large** | Multi-person team. Sprints. Formal deliverables. Multi-discipline content (e.g. mechanical + electrical + software). Needs `docs/{source,deliverables,components,artifacts,project-management}/`. | `Schoolprojects/Aardbei-Plukkers` (NHL Stenden IDP), any team project with a graded portfolio |

When uncertain, **start one tier smaller**. Graduating up is cheap (move files into `claude/`); graduating down is wasted work.

Then read the matching reference and follow it:

- Small → `references/small.md`
- Medium → `references/medium.md`
- Large → `references/large.md`

## Bootstrap checklist

When the user asks to bootstrap a project ("set up Claude context", "scaffold", "init structure"), **create TodoWrite items for the following steps**, one per task, and mark them in progress / completed as you go.

1. **Triage** — pick the tier (small / medium / large) and state the choice to the user with the reasoning. Wait for confirmation if uncertain.
2. **Read the tier reference** — `references/<tier>.md` defines the exact directory layout, `CLAUDE.md` template, and what goes in `@imports` vs on-demand.
3. **Apply standards** — read `references/standards-stack.md` and decide which standards apply (most do; ISO 29119-3 test docs only if the project has formal tests; IEEE article format only if research output is expected).
4. **Scaffold `CLAUDE.md`** — copy the matching template from `templates/CLAUDE-<tier>.md`, fill in overview, key facts, git rules, reference table. Keep under 80 lines for small/medium, under 200 for large.
5. **Scaffold `claude/`** (medium + large only) — create `claude/todolist.md` from `templates/todolist.md`. For large, add per-domain `.md` files (one per major area; see `references/large.md`).
6. **Scaffold `docs/artifacts/`** (medium when there is any design history; large always) — create `specs/`, `plans/`, `reviews/` per `references/artifacts.md`.
7. **Seed cross-session memory** (always) — create `~/.claude/projects/<slug>/memory/MEMORY.md` and at minimum a `user.md` if not already present. See `references/memory.md`. The slug matches the working directory (e.g. `C--Users-ruben-projects-...`).
8. **Add `CHANGELOG.md`** (medium + large; small only if releases are versioned) — copy `templates/CHANGELOG.md`. Keep a Changelog 1.1.0 format.
9. **Add `STANDARDS.md`** (medium + large with collaborators or public visibility; skip for solo small) — copy `templates/STANDARDS.md` to the repo root. This file is the **human contract**: it lets contributors who don't use Claude or this skill still see which standards the project follows. Fill in the `yes/no` column per which standards actually apply. The skill remains the agent contract; `STANDARDS.md` is the contributor-facing summary, not a duplicate of the skill.
10. **Verify** — run `/context` to confirm auto-loaded context is under budget (see "Token budget" below). Prune `@imports` if the budget is blown.

For a **restructure** of an existing project rather than a fresh bootstrap: skip steps that already exist, but still create TodoWrite items so the gaps are visible.

## Standards stack — applies to most projects

Briefly: the user follows an explicit standards stack — formal ISO/IEC/IEEE norms plus four industry conventions. **Most projects adopt at least the conventions layer; the formal norms are opt-in per project (school deliverables → all of them; tools → just naming + commits + changelog).**

The four conventions every project should follow:

- **kebab-case ASCII-only paths** — lowercase, hyphens for word boundaries, no spaces, no underscores, no PascalCase, no non-ASCII characters. `README.md`, `CLAUDE.md`, `CHANGELOG.md` are conventional exceptions.
- **English structural paths** — directory and file names in English. Document *content* may be Dutch where the deliverable requires it. Dutch acronyms that are the proper name of a deliverable (`pve`, `top`) are permitted.
- **ISO 8601 date prefix** — time-based records start with `YYYY-MM-DD-`, e.g. `2026-05-08-standup.md`, never `Standup_2026-05-08.md`. The prefix must come first so sort-by-filename is chronological.
- **Conventional Commits 1.0.0 + Keep a Changelog 1.1.0** — `<type>(<scope>): <description>` for commits; `CHANGELOG.md` grouped by version or sprint.

For the full standards stack (ISO 26515 agile docs, ISO 26514 user docs, ISO 29119-3 test docs, ISO 15289 lifecycle info items, ISO 10007 config management, ISO 8601, IEEE article format) and rationale for each, read **`references/standards-stack.md`**. That reference also includes the Diátaxis-evaluated-but-rejected note and the worked rationale for kebab-case + monorepo layout.

## Core rules — one-liner each

- **Auto-loaded context budget**: `CLAUDE.md` + `@imports` ≤ 5k tokens total. Anything bigger goes on-demand.
- **One authoritative source per deliverable** (ISO 10007): a `.docx` and its Typst source do not coexist as siblings. Source in `docs/source/`, generated in `docs/deliverables/`.
- **No `temp/`, no `old/`, no `archive/`** — git history is the archive. Delete obsolete files, don't shelve them in named dirs.
- **No secrets in any tracked file** — `.env`, tokens, passwords stay out of git. Memory files included.
- **Specs and plans live in the repo, not in memory** — `docs/artifacts/{specs,plans,reviews}/` are committed alongside the code that implements them.
- **Memory ≠ plans ≠ tasks** — memory is cross-session facts; plans are committed artefacts in `docs/artifacts/plans/`; tasks are per-session TodoWrite items.

## Token budget (auto-loaded context)

| Tier | `CLAUDE.md` | `@imports` total | Total auto-loaded |
|------|-------------|------------------|-------------------|
| small | < 60 lines, ~1k tokens | none | < 1k tokens |
| medium | < 120 lines, ~2k tokens | < 2k tokens | < 4k tokens |
| large | < 200 lines, ~3k tokens | < 2k tokens | < 5k tokens |

Check with `/context`. If over budget, move auto-loaded `@import` files to the on-demand table.

## References (read on demand)

| File | When to read |
|------|--------------|
| `references/small.md` | Bootstrapping or restructuring a small project (single utility, library, tool) |
| `references/medium.md` | Bootstrapping or restructuring a medium project (multi-component, infra, multi-service) |
| `references/large.md` | Bootstrapping or restructuring a large project (team, sprints, deliverables) |
| `references/standards-stack.md` | Picking standards to apply, naming convention questions, ISO/IEC/IEEE rationale, Diátaxis decision |
| `references/artifacts.md` | Setting up `docs/artifacts/{specs,plans,reviews}/`, naming review/spec/plan files, multi-file review directories |
| `references/memory.md` | Setting up cross-session memory, picking memory type (user / feedback / project / reference), `MEMORY.md` index |
| `references/todolist.md` | Creating `claude/todolist.md`, Plane sync rules, how TodoWrite interacts with the file |

## Templates (copy when scaffolding)

| File | Purpose |
|------|---------|
| `templates/CLAUDE-small.md` | Minimal `CLAUDE.md` — overview + key facts + git rules |
| `templates/CLAUDE-medium.md` | `CLAUDE.md` with `@imports` + on-demand table |
| `templates/CLAUDE-large.md` | Full `CLAUDE.md` with multi-domain `@imports`, standards stack, sprint structure |
| `templates/todolist.md` | Seed `claude/todolist.md` with checkbox format + optional Plane sync block |
| `templates/CHANGELOG.md` | Seed `CHANGELOG.md` per Keep a Changelog 1.1.0, sprint grouping |
| `templates/STANDARDS.md` | Human-readable standards summary at repo root — for contributors not using this skill |

## Anti-patterns — do not do these

- Do not invent fields in `CLAUDE.md` that aren't in the template. The template is the contract.
- Do not create `claude/<file>.md` "just in case". Each `claude/` file must be referenced by either `@import` or the on-demand table.
- Do not put generated binaries (PDF, DOCX, exports) next to their sources. Source → `docs/source/`. Output → `docs/deliverables/`.
- Do not write Diátaxis-style `docs/{tutorials,how-to,reference,explanation}/` as the primary structure. The standards stack rejects this — see `references/standards-stack.md` §Diátaxis.
- Do not skip the triage step. Loading large-project guidance into a small repo is the documented failure mode.
- Do not duplicate this skill's content into `claude/project-standardization.md` inside the project. The skill itself is the source of truth. Reference it, do not copy it.
- Do not write the skill's bootstrap checklist, triage table, or anti-patterns into `STANDARDS.md`. `STANDARDS.md` is for **contributors**; the agent-facing parts of the skill stay in the skill only.

## Note on the older `project-standardization.md`

This skill replaces `ContextMD/project-standardization.md`. Several existing projects (Homelab, IDP, others) contain copies of the old spec under `claude/project-standardization.md`. Those copies are now stale references. When working in such a project, prefer this skill's guidance over the local copy, and propose deleting the local copy.
