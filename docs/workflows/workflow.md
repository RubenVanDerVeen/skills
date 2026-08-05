# AI Workflow

How Ruben works with AI coding agents: the harness, the skill stack, the plugins and agents around it, and the flow a task follows from idea to commit. Snapshot date: 2026-08-04.

## Harness

opencode is the active harness, running two flat-quota coding-plan models in a cross-model split:

| Model | Carries |
|---|---|
| `zai-coding-plan/glm-5.2` | Planning, review, consult: long-horizon reasoning (`planner`, `reviewer`, `oracle`, `standardizer`, `documenter`) |
| `minimax-coding-plan/MiniMax-M3` | Orchestration and implementation: near-par execution, faster and cheaper (`orchestrator`, `executor`, `inventree`) |

Config lives in `~/.config/opencode/` and `~/.opencode/opencode.json`; install steps in `opencode-install.md`. The `opencode-see-image` plugin routes image attachments from the text-only GLM 5.2 primary to MiniMax-M3 and returns a text description.

The repo follows the [agents.md](https://agents.md) convention and still works with other harnesses (Claude Code via the `CLAUDE.md` shim and the `~/.claude/` sync paths, plus Codex, Cursor, Aider, etc.), but Claude Code is no longer in daily use. The sync tables in `AGENTS.md` and `opencode-install.md` keep those paths as a documented capability.

Personal skills live in this repo (`C:\Users\ruben\projects\tools\skills`) and sync to `~/.config/opencode/skills/`. Slash commands sync to `~/.config/opencode/command/` (singular). The Claude Code equivalents (`~/.claude/skills/`, `~/.claude/commands/` plural) stay documented for that harness.

## Skill stack

Four layers, from personal to generic.

### 1. Personal skills and commands (this repo)

**Skills** (auto-load by frontmatter description match):

| Skill | Covers |
|---|---|
| `altium-pro` | Altium Designer: PCB rooms, polygon pours, design rules, troubleshooting log |
| `drawio-pro` | Personal draw.io style: pastel grouped containers, BPMN flowcharts, legend boxes |
| `typst-pro` | Typst documents: NHL Stenden reports, IEEE templates, Dutch project layout |
| `synctool-sync` | NAS sync jobs via the `synctool` CLI, dry-run first |
| `deep-research` | End-to-end research pipeline: intake, parallel gather (arxiv + web + own vault), synthesized dossier with citations, then hand off to brainstorm or Typst draft |
| `code-standardization` | Source-code structure standard: formatter/linter/hooks, per-language naming, module organization, architecture boundaries. Sister to `project-standardization` (which covers repo/docs layout). Covers Python, TS/JS, C/C++, Go, Rust. Flat. Pairs with `standardizer` agent. |
| `project-standardization` | Bootstraps any repo for AI agents: AGENTS.md, `docs/artifacts/`, standards stack |
| `multi-plan-orchestration` | Splits oversized tasks into foundation + N parallel sub-plans |
| `skill-harvest` | Mines recent opencode sessions for repeated corrections and skill gaps; report, approve, apply loop |

**Commands** (explicit entry points in `commands/`, synced to `~/.config/opencode/command/`; Claude Code path `~/.claude/commands/`):

| Command | Parent skill | Purpose |
|---|---|---|
| `/standardize` | `project-standardization` | Bootstrap or restructure a project |
| `/standardize-migrate` | `project-standardization` | Migrate an older layout to the standard |
| `/standardize-code` | `code-standardization` | Run the 4 agent checks (formatter/linter presence, documentation, consistency, boundaries) against a path, language, or the current branch diff. Optional `$ARGUMENTS` for scoping. |
| `/multi-plan` | `multi-plan-orchestration` | Start multi-plan orchestration |
| `/goal` | orphan | Iterate a build loop until a verifier passes |
| `/execute-plan` | orphan | Subagent-driven execution of an approved plan (delegates per-task loop to `subagent-driven-development`, layers on `feat`/`fix` branch naming, docs-first commit, ponytail, behavior verification) |
| `/iterate-skill` | orphan | Refine a skill by dispatching subagents, inspecting real output, editing the repo copy across N iterations |
| `/full-cycle` | orphan | Single-pass: brainstorm > spec > plan > dispatch the orchestrator in the same run (no approval gates). `no brainstorm` skips brainstorming; `handoff` prints the `/execute-plan` line for a fresh session instead |
| `/harvest` | `skill-harvest` | Mine recent sessions for skill gaps |

Skills cover what loads automatically; commands are the explicit escape hatch for when the description match is missed.

### 2. Process discipline: superpowers (plugin)

The gatekeeper layer. `using-superpowers` loads at session start and forces a skill check before any action. The skills used most:

- `brainstorming` before any creative work (features, components, new skills)
- `writing-plans` and `executing-plans` for multi-step work
- `test-driven-development` and `systematic-debugging` during implementation
- `requesting-code-review`, `receiving-code-review`, `verification-before-completion` before claiming done
- `writing-skills` when authoring skills for this repo
- `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees` for parallel or isolated work

### 3. Output style

- **ponytail** (plugin): YAGNI-first "lazy senior dev" mode plus over-engineering review/audit skills. Auto-active at level `full` every session; governs what gets built, not how the agent talks.
- **caveman** (plugin): terse chat register, roughly 75% fewer output tokens. Available for long sessions or when output is too verbose; code, commits, and docs stay normal. Ships `/caveman-commit` and `/caveman-review`. Pair with ponytail (ponytail builds, caveman talks).
- **stop-slop** (skill): strips AI tells from prose (banned phrases, structural cliches, no em-dashes). Loaded whenever drafting or editing text. Reinforces the repo-wide no-em-dash rule.

### 4. Domain packs and utilities

- **vercel-labs/agent-skills**: `vercel-react-best-practices`, `vercel-composition-patterns`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`
- **find-skills**: discovers and installs new skills on demand
- **markitdown** (CLI): converts PDF/Office/EPUB/images/audio to Markdown so the agent can read them
- **graphify** (CLI): builds a queryable knowledge graph per repo (`graphify-out/`). Economics: a ~1-2K-token `graphify query` replaces a 10-40K-token grep/read exploration whose residue gets re-billed on every later prompt; phrase queries with concrete filenames/symbols, since abstract questions anchor on doc headings instead of code. Harness-agnostic via a "Knowledge graph" section in each graphed repo's AGENTS.md (wired by `/standardize` step 10 at medium/large tiers). Freshness needs no LLM: `graphify update .` is pure AST (~30 s), run by a debounced post-commit hook (`templates/post-commit-graphify` in the standardization skill) and as an end step of `/execute-plan`. opencode also has a `/graphify` skill plus a nudge hook; on other harnesses the AGENTS.md section carries it.

## Agents (opencode)

Nine custom agents cover the plan/execute/review split plus inventory. Source of truth in `agents/` (copy to `~/.config/opencode/agents/` to activate); full roster, model pins, denylists, and token measurements in `agents/README.md`.

| Agent | Mode | Model | Role |
|---|---|---|---|
| `planner` | primary | `glm-5.2` | Brainstorm > spec > plan, then dispatch the orchestrator subagent in the same run (single-pass); `handoff` prints the `/execute-plan` line for a fresh session |
| `orchestrator` | all | `MiniMax-M3` | Executes approved plans: dispatches executor/reviewer per task, oracle on two-strike failures, commits at boundaries. Session agent for standalone `/execute-plan`, and dispatchable by the planner for single-pass `/full-cycle` |
| `writer` | primary | unpinned | Focused doc/Typst sessions: direct edits, compile-verify, no ceremony |
| `inventree` | primary | `MiniMax-M3` | InvenTree inventory via the homelab MCP: AliExpress CSV import, parts/stock/POs, naming convention |
| `executor` | subagent | `MiniMax-M3` | Implements one plan task: TDD, edit, verify, report |
| `reviewer` | subagent | `glm-5.2` | Spec-compliance and code-quality review of one task (cross-model on purpose) |
| `oracle` | subagent | `glm-5.2` | Read-only consult after two failed attempts |
| `standardizer` | subagent | `glm-5.2` | Repo-wide standardization audit after a plan's task loop in a merged pass: kebab-case paths, AGENTS.md sections, docs/artifacts/ layout, changelog, catalog rows (from `project-standardization`), plus formatter/linter config presence, per-language naming/module-organization rules, and architecture boundary adherence (from `code-standardization`). Returns findings tagged quick-fix or recommendation. Read-only. |
| `documenter` | subagent | `glm-5.2` | Closes out a completed plan: writes the execution report to `docs/artifacts/features/`, updates every catalog/doc touched, commits as docs. Write-scoped to `docs/**` + root markdown. |

`/full-cycle` runs as `planner` and, by default, dispatches the `orchestrator` subagent (mode `all`) to execute the plan in the same run, prompt to final report, no approval gates. This needs `subagent_depth >= 2` in opencode config so the orchestrator can in turn dispatch executor/reviewer; the `handoff` keyword skips the dispatch and prints the `/execute-plan` line for a fresh session instead. `/execute-plan` itself runs as `orchestrator` and dispatches implementer tasks to `executor`, reviews to `reviewer`, two-strike failures to `oracle`, post-implementation structure review to `standardizer`, and the documentation/report phase to `documenter`. Both paths fall back to the general subagent when a named one is missing.

## MCP (opencode)

- **homelab** (stdio, Python, machine-local): self-hosted services on the home server. Tools for InvenTree (inventory), Plane (project management), and Nextcloud. The `inventree` agent wraps the InvenTree tools with a pre-loaded category map; `homelab*` schemas are denied in every other agent.

## Flow

Which path a task takes depends on size.

### Small task (bugfix, doc edit, one-file change)

1. Ask in chat; ponytail keeps the exchange short.
2. Relevant skills auto-trigger on their frontmatter descriptions (`using-superpowers` enforces the check).
3. Bugs go through `systematic-debugging`; features through `brainstorming`, then TDD.
4. `verification-before-completion` before any "done" claim. Commits wait for explicit instruction, Conventional Commits format.

### Medium feature (one plan)

1. `/full-cycle <request>` runs the whole pipeline in one pass as the `planner`: `brainstorming` produces a design doc in `docs/artifacts/features/<topic>/YYYY-MM-DD-<topic>-design.md`, then `writing-plans` turns it into `docs/artifacts/features/<topic>/YYYY-MM-DD-<topic>-plan.md`, with no approval gates between phases. `no brainstorm` skips straight to the spec when the request is explicit enough.
2. At the end of the pipeline the planner dispatches the `orchestrator` subagent (mode `all`) in the same run, instead of stopping at a handoff. The orchestrator branches as `<type>/<plan-slug>` (`feat` for features, `fix` for bug fixes), commits the plan and spec first, then runs its 8-step loop: `executor` per task, `reviewer` after each, `oracle` on two-strike failures, `standardizer` structure review (repo structure: kebab-case, AGENTS, docs/artifacts, catalogs; code structure: formatter/linter, per-language rules, architecture boundaries) with quick-fix `executor` passes, then `documenter` writes the execution report and updates catalogs. It commits at task boundaries, often works in a worktree, and returns the final report for the planner to relay.
3. The `handoff` keyword opts out of single-pass: the planner prints the spec and plan paths plus `/execute-plan <plan-path>` for a fresh session. `/execute-plan` runs the same execution loop as `orchestrator` (standalone), and is also the path on harnesses without `subagent_depth >= 2` (the planner's dispatch needs it so the orchestrator can in turn dispatch executor/reviewer).
4. Once spec and plan are approved, the agent commits on its own at plan-defined boundaries (the one carve-out from the no-unprompted-commit rule).
5. Code review skills close the loop before merge.

### Large feature (multiple modules)

1. `/multi-plan` (during brainstorming) writes a decomposition outline to `docs/artifacts/features/<topic>/`: one shared foundation plus N independently buildable sub-projects. User approves the outline before any spec is written.
2. The orchestrator then runs the normal brainstorm + plan cycle per part, foundation first. The foundation plan marks its frozen interfaces in the per-task Interfaces blocks: the exact signatures SPs consume and may never change. SP specs reference those by name. Specs and plans land in the usual `docs/artifacts/features/<topic>/` locations.
3. The manifest (`docs/artifacts/features/<topic>/YYYY-MM-DD-<topic>-manifest.md`) is the handoff artifact: plan table, execution order with expected merge conflicts, per-agent dispatch prompts, an integration dispatch prompt, and the integration checklist. The orchestrator STOPs there. It never executes, never merges.
4. User pastes each dispatch prompt into a fresh session: foundation on `feat/<slug>`; after the foundation is complete and verified, the SPs in parallel on `feat/<slug>-spN-<name>` branches (separate worktrees when on one machine, each with its own dependency install); finally the integration prompt on `feat/<slug>`: `git merge --no-ff` per SP in manifest order, test suite between merges, checklist, then merge to base.
5. Branch scheme uses dashes, never nesting: `feat/<slug>` and `feat/<slug>/sp-1` cannot coexist (git ref file/dir conflict). Without a GitHub remote, local merges replace PRs; the rest of the flow is identical.
6. Integration always goes to a fresh session, never back to the planner. By integration time the planner's context is stale plan-era assumptions about code it never saw; the manifest's expected-conflict hints carry everything the merge agent needs. Same principle as the plan handoff: planning sessions never implement.

### New repo

`/standardize` bootstraps AGENTS.md + CLAUDE.md shim, `docs/artifacts/`, and the standards stack (Conventional Commits, Keep a Changelog, ISO 8601 dates, kebab-case paths) at one of three size tiers. At medium/large tiers it also wires the graphify knowledge graph: gitignored `graphify-out/`, initial `graphify update .` build, debounced post-commit refresh hook, and the query-before-grep section in AGENTS.md. `/standardize` covers repo/docs/process layout only. To audit the source code itself (formatter/linter config, per-language conventions, architecture boundaries), run `/standardize-code` instead; it loads the `code-standardization` skill and runs the 4 agent checks.

## Diagrams

Visual companions to this document, in the same `docs/workflows/` folder:

| File | Shows |
|---|---|
| `stack.drawio` | The AI stack: opencode harness (cross-model split), the four skill layers, nine custom opencode agents, and the homelab MCP |
| `plan-flow.drawio` | Single-plan lifecycle: `/full-cycle` single-pass (planner dispatches the orchestrator in the same run) with the `handoff` escape to a fresh-session `/execute-plan`; orchestrator dispatches executor/reviewer/oracle, then runs structure review and documentation phases |
| `multi-plan-flow.drawio` | Multi-plan orchestration: decomposition outline, foundation + N parallel sub-plans, manifest handoff, fresh-session integration |

All three follow the `drawio-pro` style; their `tbSrc` / `Sources` fields point back to this document.

## House conventions

- AGENTS.md is the single source of project context; CLAUDE.md is a one-line shim pointing at it.
- Specs, plans, and reviews from any framework land in `docs/artifacts/`.
- No em-dashes anywhere: repo files or chat.
- Skill descriptions are a public interface; changing one breaks description-match loading.
- New skills update every catalog (README.md, AGENTS.md) in the same commit.

## Related

- `AGENTS.md`: repo conventions and skill-authoring rules
- `external-skills.md`: full catalog of external sources with triggers
- `opencode-install.md`: install order for the opencode side
