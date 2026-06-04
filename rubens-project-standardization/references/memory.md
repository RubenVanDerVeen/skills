# Cross-session memory

Memory lives at `~/.claude/projects/<project-slug>/memory/`. The slug is derived from the working directory path — e.g. `C:\Users\ruben\projects\hobby\homelab` → `C--Users-ruben-projects-hobby-homelab`.

Memory persists across Claude Code sessions. The `MEMORY.md` index is auto-loaded into context; individual memory files are loaded on demand when relevant.

## Layout

```
~/.claude/projects/<slug>/memory/
├── MEMORY.md                      ← index, always loaded, ≤ 200 lines, one line per entry
├── user.md                        ← user role, expertise, preferences
├── feedback_<topic>.md            ← behavioural rules — what to do / avoid and why
├── reference_<topic>.md           ← pointers to external systems
└── project_<topic>.md             ← decisions, constraints, deadlines not visible in code
```

`MEMORY.md` is an **index**, not a memory itself. One line per entry, links to the corresponding `.md` file. Never put memory content directly in `MEMORY.md`.

## Memory types

### `user.md`

User role, expertise, ongoing focus. Information that helps tailor Claude's communication to this specific user.

**When to write:** when you learn something about the user that affects how you collaborate — their level of expertise, their primary language, their current focus area.

**Example content:**

```markdown
---
name: user
description: User role and expertise — Ruben, second-year HBO student
type: user
---

Ruben is a second-year HBO student at NHL Stenden (Embedded Systems Engineering track). Strong on hardware-software boundary work — Tauri / Rust / embedded firmware / Typst. Newer to deep front-end framework patterns. Dutch native; reads English fluently; prefers terse technical communication.
```

### `feedback_<topic>.md`

Guidance the user gave about how to approach work — corrections AND confirmations. Record from failure and success. Without confirmations the memory drifts toward over-cautious behaviour.

**When to write:**
- User corrects the approach ("don't do X", "stop doing Y").
- User confirms an unusual approach worked ("yes, single bundled PR was right").

**Body structure:** rule first, then `**Why:**` and `**How to apply:**`.

```markdown
---
name: feedback_database_tests
description: Integration tests must hit real DB, not mocks
type: feedback
---

Integration tests for this project hit a real database. Do not mock the DB layer in integration tests.

**Why:** Q3 incident — mocked tests passed, prod migration failed because the mocks did not capture a real schema constraint.

**How to apply:** when adding integration tests, spin up a real test DB (Docker-compose `test-db` service). Unit tests at the function level may still mock — the rule is for `tests/integration/` only.
```

### `project_<topic>.md`

Decisions, constraints, deadlines, ongoing work-state that is not visible in code or git history.

**When to write:** when learning who is doing what, by when, or why. Also when the user gives motivation for a decision that is hard to recover by reading the diff.

**Convert relative dates to absolute** when saving. "Thursday" → "2026-05-14". Memory persists; "Thursday" decays.

```markdown
---
name: project_merge_freeze
description: Merge freeze for mobile release cut on 2026-05-14
type: project
---

Non-critical PRs are frozen after 2026-05-14 until 2026-05-21 — mobile team is cutting a release branch.

**Why:** mobile release window depends on a stable backend; PR churn during the cut burns oncall.

**How to apply:** flag any non-critical PR work targeting the affected modules between those dates. Suggest deferring to 2026-05-22+.
```

### `reference_<topic>.md`

Pointers to external systems. Where information lives outside this repo.

**When to write:** when the user mentions a tracking system, dashboard, or external resource that future sessions will need.

```markdown
---
name: reference_plane_workspace
description: Plane workspace for project tracking
type: reference
---

Project tasks for this repo live in Plane at `plane.rvdv-lab.nl/workspace`. Workspace slug: `homelab`. Project ID: `8d2c4f1e-...`.

**Why:** task management is mirrored between `claude/todolist.md` and Plane. Plane is source of truth for assignees, priorities, due dates.

**How to apply:** when adding a `[ ]` entry to `todolist.md`, also create a Plane issue. When marking `[x]`, move the Plane issue to Done.
```

## `MEMORY.md` index format

One line per entry. Under ~150 characters. No frontmatter on `MEMORY.md` itself.

```markdown
- [User profile](user.md) — Ruben, HBO ESE, prefers terse technical
- [DB tests](feedback_database_tests.md) — integration tests must hit real DB
- [Merge freeze](project_merge_freeze.md) — non-critical PR freeze 2026-05-14 → 2026-05-21
- [Plane workspace](reference_plane_workspace.md) — task tracking at plane.rvdv-lab.nl
```

**Keep under 30 entries.** Prune stale entries (older than ~1 month and no longer relevant). `MEMORY.md` is always loaded into context — every line costs tokens every session.

## Memory file format

Frontmatter is required:

```markdown
---
name: <short identifier>
description: <one-line — used to judge relevance in future sessions>
type: user | feedback | project | reference
---

<content>

**Why:** <reason this rule / fact exists>
**How to apply:** <when this kicks in>
```

The `**Why:**` and `**How to apply:**` footer is **required for `feedback` and `project` types**. Optional for `user` and `reference` types.

## What NOT to save in memory

These belong elsewhere:

- **Code patterns, architecture, file paths, project structure** — derivable by reading the current project state.
- **Git history, recent changes, who-changed-what** — `git log` / `git blame` are authoritative.
- **Debugging solutions or fix recipes** — the fix is in the code; the commit message has the context.
- **Anything already documented in `CLAUDE.md`** — duplicates rot independently.
- **Ephemeral task details** — in-progress work is TodoWrite, not memory.
- **Plan content** — plans live in `docs/artifacts/plans/`, not memory.

The exclusions apply **even when the user explicitly asks you to save**. If the user asks to save a PR list or activity summary, ask what was *surprising* or *non-obvious* about it — that is the part worth keeping.

## When to access memory

- When memories seem relevant to the current task.
- When the user references prior-conversation work.
- When the user explicitly asks ("what do you remember about", "check memory for").
- If the user says "ignore memory" or "don't use memory": do not apply, cite, or mention memory content this turn.

## Verifying memory before recommending

A memory that names a specific function, file, or flag is a claim about a moment in time. Before acting on it:

- If the memory names a file path: confirm the file exists.
- If the memory names a function or flag: grep for it.
- If the user is about to act on the recommendation (not just asking about history): verify first.

"The memory says X exists" is not the same as "X exists now."

## Memory vs other persistence

- **Memory** — cross-session facts. Lives in `~/.claude/projects/<slug>/memory/`.
- **Plans** — committed implementation steps with checkpoints. Lives in `docs/artifacts/plans/`.
- **Specs** — committed design rationale. Lives in `docs/artifacts/specs/`.
- **TodoWrite tasks** — per-session work tracking. Lives in the harness, not on disk.
- **`CLAUDE.md`** — project-specific session context. Auto-loaded.
- **`claude/<topic>.md`** — on-demand session context. Loaded by Claude when relevant.

If unsure which mechanism to use: cross-session = memory; this-conversation only = TodoWrite; design rationale = spec; implementation steps = plan; baseline project context = `CLAUDE.md` or `claude/`.

## Anti-patterns

- Writing `feedback_*.md` content directly into `MEMORY.md`. `MEMORY.md` is the index — one line per entry.
- Skipping `**Why:**` on feedback / project memories. Without the reason, the memory cannot be applied to edge cases — it can only be followed blindly.
- Writing memories using relative dates ("next Thursday", "yesterday"). Convert to absolute dates at save time.
- Saving a memory and then writing the same fact into `CLAUDE.md`. Pick one. Memory is for things that span projects or change frequently; `CLAUDE.md` is for project-stable facts.
- Letting `MEMORY.md` grow past 200 lines. Truncate / prune. Stale memory silently shapes new sessions.
