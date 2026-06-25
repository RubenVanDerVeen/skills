# Bootstrap checklist

When the user asks to bootstrap a project ("set up agent context", "scaffold", "init structure"), **create an in-session task list with the following steps**, one per task. Every major agent has its own task-list primitive (TodoWrite, todos, plan mode, etc.); use whichever the active tool exposes.

1. **Triage**: pick the tier (small / medium / large). State the choice with reasoning. Wait for confirmation if uncertain.
2. **Read the tier reference**: `references/<tier>.md` for the exact directory layout, `AGENTS.md` template, and what goes in auto-imports vs on-demand.
3. **Apply standards**: read `references/standards-stack.md` and decide which apply (most do; ISO 29119-3 test docs only if formal tests; IEEE article format only if research output expected).
4. **Scaffold `AGENTS.md` + `CLAUDE.md` shim**: copy `templates/AGENTS-<tier>.md` to root as `AGENTS.md`. Fill in overview, key facts, **Git** (mandatory, see below), reference table. Then create `CLAUDE.md` with one line: `Project guidance lives in @AGENTS.md.` Claude Code requires this shim. Keep `AGENTS.md` under 80 lines for small/medium, under 200 for large.
5. **Scaffold `.agents/`** (medium + large): at project root. For medium, add `.agents/todolist.md` from `templates/todolist.md`. For large, add per-domain `.md` files (see `references/large.md`). Subdirs (e.g. `.agents/homelab/`) only when a topic needs non-markdown assets or many files.
6. **Scaffold `docs/artifacts/`** (medium when design history exists; large always): create `specs/`, `plans/`, `reviews/` per `references/artifacts.md`. **This is the canonical location for plan/spec/review output regardless of which framework created it.** superpowers, GSD, and any other planning tool that drops files in `.planning/` or similar must redirect here.
7. **Seed cross-session memory** (always): every major agent has a memory mechanism; consult the tool's docs for the path. At minimum, create a `MEMORY.md` index and a `user.md` if not present. See `references/memory.md`. Substitute the tool's path.
8. **Add `CHANGELOG.md`** (default: yes. Skip for sub-projects): copy `templates/CHANGELOG.md`. Keep a Changelog 1.1.0 format. A **sub-project** is a library or dependency versioned through a parent, not shipped directly. Detection hints: no own `.git`, listed as a dependency of another repo, mentioned in the parent's CHANGELOG. When in doubt, include it; the cost is one short file.
9. **Add `STANDARDS.md`** (default: yes, always): copy `templates/STANDARDS.md` to repo root. The **human contract**: lets contributors who don't use an agent still see which standards apply. Fill in the `yes/no` column per actual application. The skill is the agent contract; `STANDARDS.md` is the contributor-facing summary. Even solo projects benefit: you'll forget which standards apply without it.
10. **Verify**: check the tool's context-usage indicator (opencode: `/context` or `tokens` panel). Prune auto-imports if budget blown — move anything not needed every session to the on-demand table.

### Git section in `AGENTS.md` (mandatory)

`AGENTS.md` **must** include a Git section. Default rule: **no commit/push without explicit user instruction**. Carve-out: **during plan execution (e.g. GSD-style phase plans), commit-per-phase is expected** — the agent commits each phase as it lands, and pushes if the plan says so. State both in `AGENTS.md`, not just one.

For a **restructure** rather than fresh bootstrap: skip steps that already exist, but still create task-list items so gaps are visible.
