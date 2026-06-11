# Medium project pattern

Multi-component projects: infra, multi-service stacks, multi-runtime tools, anything with multiple distinct subsystems that each need separate notes. Examples in the user's portfolio: `Hobby/Homelab` (Proxmox + ~10 VMs + dozens of containers + Cloudflare + DNS + reverse proxy + backups).

The goal is **a slim auto-loaded core plus on-demand depth**. Most facts live in `agents/<topic>.md` files. Only the few that are referenced every session are auto-imported.

> Tool-specific notes for the on-demand subdirectory:
>
> - **opencode / Codex / Cursor / Aider / GitHub Copilot / Hermes**: `agents/<topic>.md` is read automatically when the file name or path is mentioned (the `AGENTS.md` convention is honoured at any depth). Substitute the syntax your active agent recognises for auto-imports.

## Directory layout

```
project-root/
├── AGENTS.md                  ← slim entry, always loaded
├── README.md                  ← user-facing
├── CHANGELOG.md               ← grouped by release or milestone
├── .gitignore
│
├── agents/                    ← on-demand context sub-files
│   ├── todolist.md            ← pending tasks (open on demand)
│   ├── <topic>.md             ← per major area (auto-loaded or on-demand)
│   └── <topic>/               ← sub-directory when a topic has 3+ sub-files
│       ├── <sub>.md
│       └── <sub>.md
│
├── docs/
│   └── artifacts/             ← optional, only if design history exists
│       ├── specs/
│       ├── plans/
│       └── reviews/
│
└── <project files>            ← stack-natural layout
```

`docs/artifacts/` is **optional** at this tier. Create it only when there is a design history worth committing. See `references/artifacts.md`.

## `AGENTS.md` content

Slim entry point. Target ~120 lines, ~2k tokens. Must contain:

1. **Overview**: what this project is, the stack, who runs it.
2. **Key facts table**: IPs, URLs, conventions, constraints. The non-obvious things an agent must know baseline.
3. **Git & workflow rules**: repo URL(s), commit/push policy, any branch model.
4. **One reference table**: services, endpoints, VMs, components, or whatever the central "what lives where" table is. Slim version only; full detail in `agents/<topic>.md`.
5. **Auto-imports**: the few `agents/<file>.md` that are needed every session.
6. **On-demand table**: every other `agents/` file with one-line purpose.

Skeleton:

```markdown
# <Project>: Agent Context

## Overview
<2-3 sentences>

## Key Facts
<bullets: IPs, conventions, constraints>

## Git & Workflow
- Repo: <url>
- No commit/push unless user explicitly says to.

## <Central reference table>
<one table: e.g. services, VMs, endpoints>

@agents/<auto-loaded-1>.md
@agents/<auto-loaded-2>.md

## On-demand Context
| File | Purpose |
|------|---------|
| `agents/todolist.md` | Pending improvements |
| `agents/<topic>.md`  | <what it covers> |
```

> Adjust the imports section to the syntax your active tool recognises. opencode and Codex honour `agents/<file>.md` automatically; Cursor includes the file when its name is referenced; some tools read all `AGENTS.md` files unconditionally and need no explicit import.

## Picking what goes in auto-imports vs on-demand

Rule of thumb: **if you reference it in more than 50% of sessions, auto-import it. Otherwise on-demand.**

| Always auto-import | On-demand |
|--------------------|-----------|
| Service / endpoint quick-reference tables | Full container or dependency lists |
| Censoring / public-repo rules | Per-component deep-dives |
| MCP server tooling notes (if MCP is in active use) | Detailed runbooks |
| Critical "do not break X" rules | Setup / install / troubleshooting notes |
| _(keep the todolist on-demand: it can grow large)_ | |

Watch the token budget. Total auto-loaded ≤ 4k tokens. Use the tool's context-usage indicator (opencode: `/context` or `tokens` panel) after scaffolding; if over, demote one of the imports.

## Naming convention for `agents/<topic>.md`

| Filename | Use |
|----------|-----|
| `agents/todolist.md` | Always named `todolist`. Pending improvements. |
| `agents/censoring.md` | Public/private repo split rules. |
| `agents/mcp.md` | MCP server tools + setup. |
| `agents/services.md` | Slim service/endpoint table, auto-loaded. |
| `agents/<name>.md` | Domain file. Name matches the topic (`api.md`, `db.md`, `auth.md`). |
| `agents/<domain>/<sub>.md` | Sub-dir when a domain has 3+ distinct sub-topics (e.g. `agents/vms/remotedock.md`). |

## What "medium" looks like in practice: Homelab annotated

```
Homelab/
├── AGENTS.md                  ← hardware, Proxmox node, IP convention, VM table, Docker version, git workflow, key services summary
│                              ends with: @agents/services.md @agents/censoring.md @agents/mcp.md
│                              + on-demand table for containers, todolist, vms/*
├── README.md
├── agents/
│   ├── services.md            ← @import: Cloudflare tunnel + DNS quick ref
│   ├── censoring.md           ← @import: public-repo sanitization rules
│   ├── mcp.md                 ← @import: MCP servers + tools available
│   ├── containers.md          ← on-demand: full container list per VM
│   ├── todolist.md            ← on-demand: pending improvements
│   └── vms/                   ← on-demand: per-VM deep-dives
│       ├── remotedock.md
│       ├── generaldock.md
│       ├── mediadock.md
│       └── ...
├── generaldock/  remotedock/  mediadock/  truenas/  ...
│                              ← per-VM operational files (compose, configs)
```

Key observations:

- `AGENTS.md` ends with three `@imports` for the always-needed quick references. Everything else is in an on-demand HTML comment block (`<!-- Load on demand ... -->`).
- The VM table lives in `AGENTS.md` (one line per VM, ~20 rows). Per-VM detail lives in `agents/vms/<name>.md`.
- The `agents/vms/` sub-directory is used because there are 5+ VMs: the "3+ sub-topics → sub-directory" threshold applies.

## When to add `docs/artifacts/`

Create `docs/artifacts/{specs,plans,reviews}/` the first time any of these become true:

- A non-trivial feature warrants a design spec (via `brainstorming` skill).
- An implementation plan is being written (via `writing-plans` skill).
- A review / audit of the repo is being committed.

Until then, the directory is just noise. See `references/artifacts.md` for the full convention.

## Memory

Cross-session memory at the tool's default memory location (opencode: `<project>/.opencode/memory/` or tool-defined; the path differs per tool). Medium projects typically have:

- `user.md`: user role.
- `feedback_<topic>.md`: behavioural rules learned per area.
- `project_<topic>.md`: decisions, constraints not captured in code (e.g. "Docker pinned to 28.2.2 because v29 broke Watchtower").
- `reference_<topic>.md`: pointers to external systems (Plane workspace, dashboards, ticketing).

See `references/memory.md` for the universal structure and tool-specific paths.

## When to graduate to large

Graduate to the large pattern when **any** of these become true:

- A team of more than the user is committing.
- Sprints or formal milestones exist with graded deliverables.
- Multi-discipline content arrives (e.g. mechanical CAD alongside software).
- `docs/source/` and `docs/deliverables/` start splitting (editable vs generated).
- A formal standards stack (ISO/IEC/IEEE) is being adopted explicitly.

See `references/large.md`.

## Anti-patterns for medium projects

- Auto-importing everything in `agents/`. The on-demand list exists for a reason; if it is empty, the auto-load budget is being blown.
- Putting a full container list in `AGENTS.md` "for convenience". Slim summary in `AGENTS.md`; full list in `agents/containers.md`.
- Mirroring the source tree under `agents/` (e.g. `agents/src/api/auth/...`). `agents/<topic>.md` is one file per topic, not a parallel directory tree.
- Creating `agents/<topic>.md` for things already obvious from source (e.g. `agents/file-tree.md`). If a directory listing answers it, no `agents/` file is needed.
- Using `agents/notes.md` as a junk drawer. Each `agents/` file has a single named purpose.
