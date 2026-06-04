# Medium project pattern

Multi-component projects: infra, multi-service stacks, multi-runtime tools, anything with multiple distinct subsystems that each need separate notes. Examples in the user's portfolio: `Hobby/Homelab` (Proxmox + ~10 VMs + dozens of containers + Cloudflare + DNS + reverse proxy + backups).

The goal is **a slim auto-loaded core plus on-demand depth**. Most facts live in `claude/<topic>.md` files. Only the few that are referenced every session get `@import`-ed.

## Directory layout

```
project-root/
├── CLAUDE.md                  ← slim entry — always loaded
├── README.md                  ← user-facing
├── CHANGELOG.md               ← grouped by release or milestone
├── .gitignore
│
├── claude/                    ← Claude context sub-files
│   ├── todolist.md            ← pending tasks (open-on-demand)
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

## `CLAUDE.md` content

Slim entry point. Target ~120 lines, ~2k tokens. Must contain:

1. **Overview** — what this project is, the stack, who runs it.
2. **Key facts table** — IPs, URLs, conventions, constraints. The non-obvious things Claude must know baseline.
3. **Git & workflow rules** — repo URL(s), commit/push policy, any branch model.
4. **One reference table** — services, endpoints, VMs, components, or whatever the central "what lives where" table is. Slim version only; full detail in `claude/<topic>.md`.
5. **`@imports`** — the few `claude/<file>.md` that are needed every session.
6. **On-demand table** — every other `claude/` file with one-line purpose.

Skeleton:

```markdown
# <Project> — Claude Context

## Overview
<2-3 sentences>

## Key Facts
<bullets — IPs, conventions, constraints>

## Git & Workflow
- Repo: <url>
- No commit/push unless user explicitly says to.

## <Central reference table>
<one table — e.g. services, VMs, endpoints>

@claude/<auto-loaded-1>.md
@claude/<auto-loaded-2>.md

## On-demand Context
| File | Purpose |
|------|---------|
| `claude/todolist.md` | Pending improvements |
| `claude/<topic>.md`  | <what it covers> |
```

## Picking what goes in `@imports` vs on-demand

Rule of thumb: **if you reference it in more than 50 % of sessions, `@import` it. Otherwise on-demand.**

| Always `@import` | On-demand |
|------------------|-----------|
| Service / endpoint quick-reference tables | Full container or dependency lists |
| Censoring / public-repo rules | Per-component deep-dives |
| MCP server tooling notes (if MCP is in active use) | Detailed runbooks |
| Critical "do not break X" rules | Setup / install / troubleshooting notes |
| Todo list | _(actually: keep todolist on-demand — it can grow large)_ |

Watch the token budget. Total auto-loaded ≤ 4k tokens. Run `/context` after scaffolding; if over, demote one of the imports.

## Naming convention for `claude/<topic>.md`

| Filename | Use |
|----------|-----|
| `claude/todolist.md` | Always named `todolist`. Pending improvements. |
| `claude/censoring.md` | Public/private repo split rules. |
| `claude/mcp.md` | MCP server tools + setup. |
| `claude/services.md` | Slim service/endpoint table — auto-loaded. |
| `claude/<name>.md` | Domain file — name matches the topic (`api.md`, `db.md`, `auth.md`). |
| `claude/<domain>/<sub>.md` | Sub-dir when a domain has 3+ distinct sub-topics (e.g. `claude/vms/remotedock.md`). |

## What "medium" looks like in practice — Homelab annotated

```
Homelab/
├── CLAUDE.md                 ← hardware, Proxmox node, IP convention, VM table, Docker version, git workflow, key services summary
│                              ends with: @claude/services.md @claude/censoring.md @claude/mcp.md
│                              + on-demand table for containers, todolist, vms/*
├── README.md
├── claude/
│   ├── services.md            ← @import — Cloudflare tunnel + DNS quick ref
│   ├── censoring.md           ← @import — public-repo sanitization rules
│   ├── mcp.md                 ← @import — MCP servers + tools available
│   ├── containers.md          ← on-demand — full container list per VM
│   ├── todolist.md            ← on-demand — pending improvements
│   └── vms/                   ← on-demand — per-VM deep-dives
│       ├── remotedock.md
│       ├── generaldock.md
│       ├── mediadock.md
│       └── ...
├── generaldock/  remotedock/  mediadock/  truenas/  …
│                              ← per-VM operational files (compose, configs)
```

Key observations:

- `CLAUDE.md` ends with three `@imports` for the always-needed quick references. Everything else is in an on-demand HTML comment block (`<!-- Load on demand ... -->`).
- The VM table lives in `CLAUDE.md` (one line per VM, ~20 rows). Per-VM detail lives in `claude/vms/<name>.md`.
- The `claude/vms/` sub-directory is used because there are 5+ VMs — the "3+ sub-topics → sub-directory" threshold applies.

## When to add `docs/artifacts/`

Create `docs/artifacts/{specs,plans,reviews}/` the first time any of these become true:

- A non-trivial feature warrants a design spec (via `superpowers:brainstorming` skill).
- An implementation plan is being written (via `superpowers:writing-plans` skill).
- A review / audit of the repo is being committed.

Until then, the directory is just noise. See `references/artifacts.md` for the full convention.

## Memory

Cross-session memory at `~/.claude/projects/<slug>/memory/`. Medium projects typically have:

- `user.md` — user role.
- `feedback_<topic>.md` — behavioural rules learned per area.
- `project_<topic>.md` — decisions, constraints not captured in code (e.g. "Docker pinned to 28.2.2 because v29 broke Watchtower").
- `reference_<topic>.md` — pointers to external systems (Plane workspace, dashboards, ticketing).

See `references/memory.md`.

## When to graduate to large

Graduate to the large pattern when **any** of these become true:

- A team of more than the user is committing.
- Sprints or formal milestones exist with graded deliverables.
- Multi-discipline content arrives (e.g. mechanical CAD alongside software).
- `docs/source/` and `docs/deliverables/` start splitting (editable vs generated).
- A formal standards stack (ISO/IEC/IEEE) is being adopted explicitly.

See `references/large.md`.

## Anti-patterns for medium projects

- Auto-importing everything in `claude/`. The on-demand list exists for a reason; if it is empty, the auto-load budget is being blown.
- Putting a full container list in `CLAUDE.md` "for convenience". Slim summary in `CLAUDE.md`; full list in `claude/containers.md`.
- Mirroring the source tree under `claude/` (e.g. `claude/src/api/auth/...`). `claude/<topic>.md` is one file per topic, not a parallel directory tree.
- Creating `claude/<topic>.md` for things already obvious from source (e.g. `claude/file-tree.md`). If a directory listing answers it, no `claude/` file is needed.
- Using `claude/notes.md` as a junk drawer. Each `claude/` file has a single named purpose.
