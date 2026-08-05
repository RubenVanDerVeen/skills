# `.agents/todolist.md`: pending tasks

A flat markdown file with GitHub-flavoured checkboxes. One pending improvement / open task per line. Lives at `.agents/todolist.md` (medium and large tiers; small tier usually skips this).

Distinct from the in-tool task list (the agent's own task primitive: TodoWrite, todos, plan mode, etc.). The in-tool task list is per-session work tracking that lives in the harness; `todolist.md` is a persistent, committed-to-the-repo backlog that survives across sessions and across people.

## Format

GitHub-flavoured markdown. One task per line. No sub-bullets, no nesting.

```markdown
- [ ] Pending task description
- [x] Completed task description
- [ ] Another pending task
```

| Marker | Meaning |
|--------|---------|
| `[ ]` | Open / not done |
| `[x]` | Done, kept in the file so history is visible |

## Rules

- One task per line. No sub-bullets, no nested checklists.
- Keep completed (`[x]`) items in the file. They are the record of what shipped.
- Order: priority descending (most important first), or grouped by area with a heading.
- Tasks are concise: one sentence. If a task needs paragraphs of context, it should be a spec in `docs/artifacts/features/<feature>/`, not a todo line.

## Interaction with the in-tool task list

When the user asks "what is on the todo list", or asks the agent to work through pending items:

1. Read `.agents/todolist.md`.
2. **Filter to open items** (lines with `[ ]`, not `[x]`).
3. Create one in-tool task per open item (the agent's own task primitive).
4. As each item is completed, **update `.agents/todolist.md` in place**: change `[ ]` to `[x]` on the corresponding line.
5. Do not delete completed lines.

The in-tool task list is per-session and disappears. `todolist.md` is the persistent record.

## Example

```markdown
# Pending improvements

- [ ] Make changes to the Typst library
- [x] Make backup of Teams documents
- [ ] Finish Practicum Regeltechniek2 deel 2
- [ ] Make all embedded programming tasks from year 1
- [x] Set up Plane workspace for IDP
- [ ] Migrate Word PvE to Typst source
```

A `#` heading at the top is fine. No deeper structure needed.

### Grouped variant (large projects with many items)

```markdown
# Pending improvements

## Sprint 2: sub-function demo (2026-05-13)
- [ ] Component test plan: remote-controller
- [ ] Sprint 1 design-proposal PDF export

## Standardization
- [ ] Rename remaining naming violations (audit §3.1)
- [x] Rename standups to ISO 8601 prefix
- [ ] Add CHANGELOG.md

## Research
- [ ] Compile updated standards stack paper
```

Sub-headings allowed. Sub-bullets per item still not allowed.

## Plane sync (optional)

If the project mirrors `todolist.md` to a Plane workspace, add a sync note at the very top:

```markdown
> **Plane sync**: Mirrored in **<Project>** at `plane.rvdv-lab.nl/workspace`.
> Add/complete items here → create or move to Done in Plane.
> Workspace: `<slug>`, project ID: `<uuid>`.

- [ ] Task 1
- [ ] Task 2
```

### Plane sync rules

- **Adding** a `[ ]` item → also create a Plane issue in the mirrored project.
- **Marking `[x]`** → move the corresponding Plane issue to Done.
- **Plane is the source of truth** for assignees, due dates, priority. `todolist.md` tracks existence + status only.
- If no Plane workspace exists for this project, omit the sync note entirely.

The Plane MCP tools (`mcp__homelab__plane_*`) are available when MCP is configured for the project. Use the dedicated `plane` subagent for bulk operations; for single-task sync, direct tool calls are fine.

## When to use `todolist.md` vs in-tool task list vs memory

| Use this | For |
|----------|-----|
| `.agents/todolist.md` | Persistent backlog. Survives sessions and authors. Committed. |
| In-tool task list (TodoWrite / todos / plan mode) | Per-session work tracking. Disappears at end of session. |
| Memory (`project_*.md`) | Cross-session facts, decisions, deadlines. NOT tasks. |
| `docs/artifacts/features/<feature>/` | Multi-step implementation plans with checkpoints. NOT a backlog. |

A new feature request from the user that will take several sessions to land: `todolist.md` entry + (when starting) an in-tool task per step.

## When to skip `todolist.md`

Skip on small projects. With 0–2 pending tasks, chat history and the in-tool task list are enough. Create `todolist.md` only when:

- More than 3 pending items have accumulated.
- The same items are being re-derived session after session.
- Multiple authors need to see the backlog.

## Anti-patterns

- Deleting completed `[x]` lines to "keep the file clean". The completed lines are the history: keep them.
- Nesting sub-bullets under a task (`  - [ ] sub-task`). One line per task. If a task has sub-tasks, it should be split into separate top-level items.
- Putting design rationale or paragraph-long context inside a task. Move that to a spec; the todo line just references the spec.
- Mirroring `todolist.md` to Plane without setting up the sync note. Future readers cannot tell the two are mirrored.
- Adding tasks that are already done as `[x]` for "completeness". `todolist.md` tracks work that was on this list before being completed: not historical pre-list work.
