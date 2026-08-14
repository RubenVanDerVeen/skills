# Bootstrap checklist

When the user asks to bootstrap a project ("set up agent context", "scaffold", "init structure"), **create an in-session task list with the following steps**, one per task. Every major agent has its own task-list primitive (TodoWrite, todos, plan mode, etc.); use whichever the active tool exposes.

## Branch: fresh vs restructure

This checklist runs on two paths, decided by triage in step 1:

- **Fresh bootstrap** (`Test-Path AGENTS.md` returns False): walk the 12 steps linearly in a single agent. Run each step's `Verification:` predicate inline before moving on.
- **Restructure** (`Test-Path AGENTS.md` returns True): dispatch the three-subagent explore-patch-verify flow in `references/restructure-flow.md`. The explore and verify phases run these same predicates; the verify phase re-runs them with a fresh context.

When adding a requirement to any step below, add or update its `Verification:` predicate in the same edit. A step without a runnable predicate is a step the restructure flow cannot confirm.

1. **Triage**: pick the tier (small / medium / large). State the choice with reasoning. Wait for confirmation if uncertain.
    - Verification: reasoning step, no grep predicate. The tier choice is recorded in the AGENTS.md overview line.
2. **Read the tier reference**: `references/<tier>.md` for the exact directory layout, `AGENTS.md` template, and what goes in auto-imports vs on-demand.
    - Verification: agent-internal, no project footprint. Not audited by the restructure flow.
3. **Apply standards**: read `references/standards-stack.md` and decide which apply (most do; ISO 29119-3 test docs only if formal tests; IEEE article format only if research output expected).
    - Verification: decision step. The application is verified via step 9 (every adopted standard has a non-empty yes/no cell in STANDARDS.md).
4. **Scaffold `AGENTS.md` + `CLAUDE.md` shim**: copy `templates/AGENTS-<tier>.md` to root as `AGENTS.md`. Fill in overview, key facts, **Git** (mandatory, see below), reference table, and the **Adding features** checklist with the project's actual catalogs. Then create `CLAUDE.md` with one line: `Project guidance lives in @AGENTS.md.` Claude Code requires this shim. Keep `AGENTS.md` under 80 lines for small/medium, under 200 for large.
    - Verification: `Test-Path AGENTS.md` AND `Test-Path CLAUDE.md` both return True, AND `Select-String -Pattern '@AGENTS\.md' CLAUDE.md` returns at least one hit.
5. **Scaffold `.agents/`** (medium + large): at project root. For medium, add `.agents/todolist.md` from `templates/todolist.md`. For large, add per-domain `.md` files (see `references/large.md`). Subdirs (e.g. `.agents/homelab/`) only when a topic needs non-markdown assets or many files.
    - Verification: for small tier, skip. For medium/large, `Test-Path .agents` returns True AND `Get-ChildItem .agents -Filter *.md` returns at least one file.
6. **Scaffold `docs/artifacts/`** (small when design history exists; medium when design history exists; large always): create `features/` and `reviews/` per `references/artifacts.md` (per-feature layout: one folder per feature under `features/<feature>/`, flat review log under `reviews/`). At small and medium tiers, only create it the moment the first artefact is being written; never pre-create empty. **This is the canonical location for plan/spec/review output regardless of which framework created it.** superpowers, GSD, and any other planning tool that drops files in `.planning/` or similar must redirect here.
    - Verification: `Get-ChildItem -Path docs/artifacts -Directory` returns `features` and `reviews`. Legacy siblings (`specs`, `plans`, `multi-plans`) are a flag to the user, not a fail; their resolution is `/standardize-migrate`.
7. **Seed cross-session memory** (always): every major agent has a memory mechanism; consult the tool's docs for the path. At minimum, create a `MEMORY.md` index and a `user.md` if not present. See `references/memory.md`. Substitute the tool's path.
    - Verification: `Test-Path MEMORY.md` (or the tool-specific memory path) returns True AND the file is non-empty.
8. **Add `CHANGELOG.md`** (default: yes. Skip for sub-projects): copy `templates/CHANGELOG.md`. Keep a Changelog 1.1.0 format. A **sub-project** is a library or dependency versioned through a parent, not shipped directly. Detection hints: no own `.git`, listed as a dependency of another repo, mentioned in the parent's CHANGELOG. When in doubt, include it; the cost is one short file.
    - Verification: `Test-Path CHANGELOG.md` returns True AND `Select-String -Pattern 'Keep a Changelog' CHANGELOG.md` returns at least one hit.
    8.1. **If the project ships versions** (Tauri apps, CLIs, libraries, installers): fill in the `### Versioning` subsection of `AGENTS.md`. Declare the canonical source, the sync targets, and the policy pointer (policy source: `references/versioning.md`). Verify the CHANGELOG header line names SemVer 2.0.0 alongside Keep a Changelog and Conventional Commits. Verify `STANDARDS.md` has the SemVer row in its stack table. Skip 8.1 entirely for sub-projects versioned through a parent.
    - Verification: `Select-String -Pattern 'SemVer 2\.0\.0' AGENTS.md, CHANGELOG.md, STANDARDS.md` returns at least one hit in EACH file. Skip entirely for sub-projects versioned through a parent.
9. **Add `STANDARDS.md`** (default: yes, always): copy `templates/STANDARDS.md` to repo root. The **human contract**: lets contributors who don't use an agent still see which standards apply. Fill in the `yes/no` column per actual application. The skill is the agent contract; `STANDARDS.md` is the contributor-facing summary. Even solo projects benefit: you'll forget which standards apply without it.
    - Verification: `Test-Path STANDARDS.md` returns True AND every standards row has a non-empty yes/no cell (no `?` or blank cells).

10. **Install the commit-msg hook** (all tiers; default yes; skip only when the project has no `.git`). Enforces Conventional Commits 1.0.0 on every commit subject, agent-made or manual. Different install target from the graphify hook: this one is shared policy that travels with the repo, so it uses a tracked `.githooks/` dir (graphify is local-cache tooling and stays in `.git/hooks/`).
    1. Copy `templates/commit-msg` to `.githooks/commit-msg` in the project.
    2. Create `.gitattributes` at the project root with one line: `.githooks/** text eol=lf` (keeps the `#!/bin/sh` shebang valid on Windows checkouts).
    3. Stage as executable: `git add .githooks/commit-msg .gitattributes` then `git update-index --chmod=+x .githooks/commit-msg`.
    4. Activate for this clone: `git config core.hooksPath .githooks`. Machine-local (`.git/config`); each clone repeats this one line to enable the hook.
    The hook is `sh` + `grep` only (no Node, no deps). Emergency bypass: `git commit --no-verify`.
        - Verification: `Test-Path .githooks/commit-msg` returns True AND `git config core.hooksPath` returns `.githooks`.
11. **Wire the knowledge graph (graphify)**: make sessions query the graph instead of grepping. Two independent parts.
    - **Keep the Knowledge graph section** (ships in the small/medium/large `AGENTS.md` templates) whenever `graphify-out/graph.json` already exists **or** you build it in this step. Applies to **all tiers, including small**: a graph the user built manually must still steer the agent. Delete the section only when no graph exists or will exist; pointing an agent at a missing graph is a dead end. The section is presence-driven on purpose. Agents default to grep/glob for code questions, and the explicit "query graphify BEFORE grep" line in `AGENTS.md` (auto-loaded every session, every agent) is the reliable nudge. The `graphify` skill description and the opencode hook help, but do not cover every agent or every reflex.
    - **Build + refresh hook** (skip when `command -v graphify` finds no CLI; at small tier, skip unless the user asked for a graph):
        1. Add `graphify-out/` to `.gitignore` (multi-MB `graph.json`/`graph.html`, all regenerable).
        2. Build the graph: `graphify update .` (AST-only, no LLM, works with no existing graph, ~30 s per few hundred files).
        3. Install the refresh hook: copy `templates/post-commit-graphify` to `.git/hooks/post-commit` (keep the executable bit on POSIX). It is debounced and backgrounded; commits stay fast.
        - Verification: conditional. IFF `Test-Path graphify-out/graph.json` OR `command -v graphify` succeeds: AGENTS.md contains a Knowledge graph section AND `.gitignore` contains `graphify-out/`. Otherwise skip.
12. **Verify**: check the tool's context-usage indicator (opencode: `/context` or `tokens` panel). Prune auto-imports if budget blown: move anything not needed every session to the on-demand table.
    - Verification: soft. Run the tool's context indicator (opencode: `/context`), report the token count, confirm under the tier budget from SKILL.md.

### Git section in `AGENTS.md` (mandatory)

`AGENTS.md` **must** include a Git section. Default rule: **no commit/push without explicit user instruction**. Carve-out: **during spec/plan-driven development and execution thereof (e.g. GSD-style phase plans), commits happen on the agent's own volition at the boundaries the plan specifies**: the agent commits each task or phase as it lands, and pushes if the plan says so. State both rules in `AGENTS.md`, not just the default. The carve-out only applies when the project has an approved spec and plan pair to execute; otherwise the default rule covers everything.

For a **restructure** rather than fresh bootstrap: skip scaffolding that already exists and is current, but still create task-list items so gaps are visible. **Upgrade stale sections, do not just skip them.** Compare each existing `AGENTS.md` section against the current template; if it references a superseded layout, rewrite it to match the template before moving on. Worked example: an Artifacts section that points specs/plans at `docs/artifacts/{specs,plans,reviews}/` (the old type-bucket layout) is stale; rewrite it to `docs/artifacts/features/<feature>/` (per-feature) plus flat `docs/artifacts/reviews/`, matching the Artifacts section in `templates/AGENTS-<tier>.md`. This step is doc-only: update the section text, do **not** move files inline (file moves are a separate, confirmable migration). After upgrading a section, flag any filesystem mismatch to the user (e.g. "AGENTS.md now says `features/<feature>/` but `docs/artifacts/specs/` still holds files") so they can run the migration deliberately.
