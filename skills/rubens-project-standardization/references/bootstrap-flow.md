# Fresh bootstrap flow: explore, patch, verify

When `/standardize` finds no `AGENTS.md` (fresh bootstrap), the run dispatches this protocol instead of walking the 11 steps in a single agent. Run it as the `orchestrator` agent: edit/write/patch denied, bash for reading state and running predicates only.

## Why three agents

The linear walk loads every tier reference, every template, and every predicate into one context, then writes the whole scaffold from it. Anything missed there is invisible, because the same context that made the edit believes it exists. Splitting recon, patch, and verify means the verifying agent has no memory of the patching agent and must re-run the literal predicate. This is the same failure mode `references/restructure-flow.md` exists for; the fresh path had no such protection.

## Explore (dispatch to `explore`, read-only)

Input: the project path, `references/bootstrap.md`, and the tier the orchestrator triaged. Action:

1. Read `references/<tier>.md` and `references/standards-stack.md`. Return the standards decision (which apply, which do not, with the one-line reason each), applying steps 2 and 3.
2. Recon the project: existing top-level layout, README, `docs/`, `.agents/`, `.git`, whether the project is a sub-project (no own `.git`, listed as a dependency elsewhere), and whether `graphify-out/graph.json` exists.
3. Return a per-step table (`step | action | existing state`) for steps 4 through 10, naming for each whether it creates a file, edits one, or has nothing to do.

The explore agent does not edit the project. Its output is the whole input to the patch phase: the executor should not need to re-read the tier reference to know what to write.

## Patch (dispatch to `executor`, one cluster at a time)

Clusters, sequential. They share one worktree and one git index, and step 9 mutates `git config`, so never dispatch two at once.

| Cluster | Steps | Content |
|---|---|---|
| C1 identity | 4, 7, 7.1, 8, 8.1 | `AGENTS.md` + `CLAUDE.md` shim, `CHANGELOG.md`, the `### Versioning` subsection, `STANDARDS.md`, the README `## AI assistance` section |
| C2 context dirs | 5, 6 | `.agents/` (medium and large), `docs/artifacts/{features,reviews}/` |
| C3 hooks and graph | 9, 10 | `.githooks/` + `.gitattributes` + `core.hooksPath`, then graphify hook and `.gitignore` entry |

Rules for the executor:

- Copy from `templates/`, fill in the project's real values. No placeholders left behind, no `TODO`.
- Stop and confirm with the user before any destructive step: overwriting an existing file with different content, replacing `core.hooksPath`, moving or deleting files.
- Skip what explore reported as already correct, but upgrade a stale file against the current template rather than skipping it.
- `docs/artifacts/` is created only when the first artefact is being written (small, medium), always at large tier. Never pre-create empty dirs.
- Apply `ponytail`: shortest working diff, no speculative scaffolding, `ponytail:` comments on deliberate shortcuts.
- One commit per cluster, Conventional Commits 1.0.0: `docs(agents): scaffold AGENTS.md and CLAUDE.md shim`, `docs(context): add artifacts and .agents dirs`, `chore(hooks): install commit-msg and pre-commit hooks`. Only commit when the user asked, or when a plan sanctions it.

## Verify (dispatch to `reviewer`, read-only)

Input: the explore table and the project path. Action: re-run every `Verification:` predicate from `references/bootstrap.md` for the steps that were dispatched, and report each `closed` or `still-fail` with the literal command output. Fresh context: do not trust the executor's report, only the command you run yourself.

Failure loop: any `still-fail` goes back to `executor` for that step. Two strikes on the same step escalates to `oracle` (read-only consult), same convention as the restructure flow.

## Steps that stay with the orchestrator

- **Step 1 triage** (branch and tier): inline, before any dispatch, because the tier decides what the executors read and the user may want to override it. Ask when unsure.
- **Step 11 verify** (context usage indicator): inline after the reviewer passes. It needs the interactive tool's `/context` or token panel, not a grep, so a subagent cannot run it. Report the token count against the tier budget from `SKILL.md` and prune auto-imports if blown.

## Cross-platform predicates

Same note as `references/restructure-flow.md`: the predicates in `bootstrap.md` are written for Windows PowerShell. On POSIX the explore and reviewer agents translate `Select-String` to `grep`, `Test-Path` to `test -f` / `test -d`, `Get-ChildItem` to `ls` / `find`. Paste the command you actually ran into the report.