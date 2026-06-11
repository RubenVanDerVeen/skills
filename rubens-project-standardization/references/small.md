# Small project pattern

Single-author utilities, libraries, tools. One language or runtime. Fewer than ~30 source files. No team, no sprints, no graded deliverables. Examples in the user's portfolio: `Tools/synctool` (Tauri+Svelte desktop app), `Tools/TypstTools` (Typst package).

The goal is **the smallest amount of agent scaffolding that still makes sessions productive.** Everything goes in one `AGENTS.md` (or the tool's preferred filename; see the "Tool-specific filenames" table in the main skill). No on-demand subdirectory. No `docs/artifacts/` until the project graduates.

## Directory layout

```
project-root/
├── AGENTS.md                  ← single context file, < 60 lines
├── README.md                  ← user-facing
├── CHANGELOG.md               ← only if releases are versioned
├── .gitignore
└── <project files>            ← language-natural layout, no agent-specific dirs
```

That is the whole structure. No `agents/`, no `docs/artifacts/`, no `specs/`, no `plans/`. Once any of those become useful, graduate to the medium pattern.

> Tool alias: this reference assumes the canonical `AGENTS.md` name. For tools that read a different filename, see the "Tool-specific filenames" table in the main skill.

### When to use a CHANGELOG.md

For tools shipped to users (releases tagged, npm/cargo published, binaries distributed): yes. For internal experiments or learning repos: no.

## `AGENTS.md` content

One file, lean. Must contain:

1. **Overview**: 2–3 sentences. What the project is, the stack, the user persona.
2. **Stack**: bulleted list of frameworks, runtimes, package manager.
3. **Critical conventions**: the non-obvious things an agent will get wrong without being told. Examples from real small projects:
   - "Files using Svelte 5 runes must be `.svelte` or `.svelte.ts`. Plain `.ts` fails silently."
   - "Compilation happens only in the Typst WebUI. Do not run `typst compile` locally."
4. **Build environment**: only if the build is non-standard. Most small projects can skip this.
5. **Git rules**: at minimum: "no commit/push unless user explicitly says to". Whatever else is project-specific (commit message style, hooks, branch policy).

### What to leave out

- Auto-generated facts: file tree, code patterns, language-natural conventions. The agent can read the source.
- "How to install": that goes in `README.md`, not `AGENTS.md`.
- Long architecture diagrams: keep `AGENTS.md` text-only and short.
- Roadmap, todo lists, plans: small projects don't need a todolist file. Use chat history.

## What "small" looks like in practice: annotated examples

### synctool (Tauri 2 + Svelte 5 + Rust workspace)

```
synctool/
├── AGENTS.md                  ← 80 lines: overview, Tauri/Svelte/Rust stack, IPC pattern, MinGW build env
├── README.md
├── CHANGELOG.md
├── Cargo.toml + Cargo.lock
├── package.json + pnpm-lock.yaml
├── crates/                    ← synctool-core, synctool-cli
├── src/                       ← Svelte frontend
├── src-tauri/                 ← Rust shell
├── tests/, e2e/, scripts/
```

`AGENTS.md` is the only context file. No `agents/` directory. The critical conventions section (Svelte runes file extensions, IPC command registration pattern, Tauri 2 ACL, per-OS path tokens) is what makes this `AGENTS.md` valuable: none of those are inferable from reading the code.

### TypstTools (Typst package, single language)

```
TypstTools/
├── AGENTS.md                  ← "no local compile: sync to WebUI", architecture, section-DB pattern, Dutch chapter numbering
├── README.md
├── lib.typ
├── typst.toml
├── src/                       ← types, templates, components, renderers, standards, styles, utils
├── assets/
├── docs/, examples/
```

Same shape: one `AGENTS.md`, no `agents/` subdir. The valuable content is the **architecture** section (entrypoint, types vs templates vs components vs renderers, standards module, styles) plus the **key conventions** (section-DB pattern, Dutch heading numbering, translation file location). All of that would be slow to re-derive from source every session.

## Memory

Cross-session memory is provided by the active tool. The location and format depend on the tool (opencode: typically `<project>/.opencode/memory/` or a tool-defined path; the path differs per tool). See `references/memory.md` for the universal structure (the `MEMORY.md` index + `user.md` / `feedback_*.md` / `project_*.md` / `reference_*.md` files) and tool-specific paths.

For a small project, the memory entries are usually just:

- `user.md`: user role, expertise.
- `feedback_*.md`: any project-specific behavioural rules learned over time.

No `project_*.md` needed for a small project; the project facts fit in `AGENTS.md`.

## When to graduate to medium

Move to the medium pattern when **any** of these become true:

- More than one on-demand topic file would naturally exist (e.g. you find yourself wanting both `agents/api.md` and `agents/db.md`).
- The `AGENTS.md` exceeds ~120 lines.
- A todolist becomes useful: multiple pending tasks accumulate that don't fit in chat.
- Design decisions start needing written rationale (a spec or plan emerges).
- The project gains a second runtime, deployment target, or service.

To graduate: create `agents/`, split `AGENTS.md` into `AGENTS.md` + one or two `agents/<topic>.md` files, list the auto-loaded ones in the imports section. See `references/medium.md`.

## Anti-patterns for small projects

- Creating `agents/` with one empty file "to match the pattern". The pattern is "as small as possible", not "always use `agents/`".
- Creating `docs/artifacts/{specs,plans,reviews}/` before there is a spec, plan, or review to put in them. Empty directories are noise.
- Copying a 200-line `AGENTS.md` template from a larger project. The template should match the tier.
- Adding `agents/todolist.md` for a project with 0–2 pending tasks. Use chat / in-tool task list for that scale.
