# Small project pattern

Single-author utilities, libraries, tools. One language or runtime. Fewer than ~30 source files. No team, no sprints, no graded deliverables. Examples in the user's portfolio: `Tools/synctool` (Tauri+Svelte desktop app), `Tools/TypstTools` (Typst package).

The goal is **the smallest amount of Claude scaffolding that still makes sessions productive.** Everything goes in one `CLAUDE.md`. No `claude/` subdirectory. No `docs/artifacts/` until the project graduates.

## Directory layout

```
project-root/
├── CLAUDE.md                ← single context file, < 60 lines
├── README.md                ← user-facing
├── CHANGELOG.md             ← only if releases are versioned
├── .gitignore
└── <project files>          ← language-natural layout, no Claude-specific dirs
```

That is the whole structure. No `claude/`, no `docs/artifacts/`, no `specs/`, no `plans/`. Once any of those become useful, graduate to the medium pattern.

### When to use a CHANGELOG.md

For tools shipped to users (releases tagged, npm/cargo published, binaries distributed): yes. For internal experiments or learning repos: no.

## `CLAUDE.md` content

One file, lean. Must contain:

1. **Overview** — 2–3 sentences. What the project is, the stack, the user persona.
2. **Stack** — bulleted list of frameworks, runtimes, package manager.
3. **Critical conventions** — the non-obvious things Claude will get wrong without being told. Examples from real small projects:
   - "Files using Svelte 5 runes must be `.svelte` or `.svelte.ts`. Plain `.ts` fails silently."
   - "Compilation happens only in the Typst WebUI. Do not run `typst compile` locally."
4. **Build environment** — only if the build is non-standard. Most small projects can skip this.
5. **Git rules** — at minimum: "no commit/push unless user explicitly says to". Whatever else is project-specific (commit message style, hooks, branch policy).

### What to leave out

- Auto-generated facts: file tree, code patterns, language-natural conventions. Claude can read the source.
- "How to install" — that goes in `README.md`, not `CLAUDE.md`.
- Long architecture diagrams — keep `CLAUDE.md` text-only and short.
- Roadmap, todo lists, plans — small projects don't need a todolist file. Use chat history.

## What "small" looks like in practice — annotated examples

### synctool (Tauri 2 + Svelte 5 + Rust workspace)

```
synctool/
├── CLAUDE.md                ← 80 lines: overview, Tauri/Svelte/Rust stack, IPC pattern, MinGW build env
├── README.md
├── CHANGELOG.md
├── Cargo.toml + Cargo.lock
├── package.json + pnpm-lock.yaml
├── crates/                  ← synctool-core, synctool-cli
├── src/                     ← Svelte frontend
├── src-tauri/               ← Rust shell
├── tests/, e2e/, scripts/
```

`CLAUDE.md` is the only Claude file. No `claude/` directory. The critical conventions section (Svelte runes file extensions, IPC command registration pattern, Tauri 2 ACL, per-OS path tokens) is what makes this `CLAUDE.md` valuable — none of those are inferable from reading the code.

### TypstTools (Typst package, single language)

```
TypstTools/
├── CLAUDE.md                ← "no local compile — sync to WebUI", architecture, section-DB pattern, Dutch chapter numbering
├── README.md
├── lib.typ
├── typst.toml
├── src/                     ← types, templates, components, renderers, standards, styles, utils
├── assets/
├── docs/, examples/
```

Same shape: one `CLAUDE.md`, no `claude/` subdir. The valuable content is the **architecture** section (entrypoint, types vs templates vs components vs renderers, standards module, styles) plus the **key conventions** (section-DB pattern, Dutch heading numbering, translation file location). All of that would be slow to re-derive from source every session.

## Memory

Cross-session memory still lives at `~/.claude/projects/<slug>/memory/`, same as for larger projects. See `references/memory.md`. For a small project, the memory entries are usually just:

- `user.md` — user role, expertise.
- `feedback_*.md` — any project-specific behavioural rules learned over time.

No `project_*.md` needed for a small project; the project facts fit in `CLAUDE.md`.

## When to graduate to medium

Move to the medium pattern when **any** of these become true:

- More than one `claude/` topic file would naturally exist (e.g. you find yourself wanting both `claude/api.md` and `claude/db.md`).
- The `CLAUDE.md` exceeds ~120 lines.
- A todolist becomes useful — multiple pending tasks accumulate that don't fit in chat.
- Design decisions start needing written rationale (a spec or plan emerges).
- The project gains a second runtime, deployment target, or service.

To graduate: create `claude/`, split `CLAUDE.md` into `CLAUDE.md` + one or two `claude/<topic>.md` files, add `@imports` for the auto-loaded ones. See `references/medium.md`.

## Anti-patterns for small projects

- Creating `claude/` with one empty file "to match the pattern". The pattern is "as small as possible", not "always use `claude/`".
- Creating `docs/artifacts/{specs,plans,reviews}/` before there is a spec, plan, or review to put in them. Empty directories are noise.
- Copying a 200-line `CLAUDE.md` template from a larger project. The template should match the tier.
- Adding `claude/todolist.md` for a project with 0–2 pending tasks. Use chat / TodoWrite for that scale.
