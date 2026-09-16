# Vitest cwd and targeted-scope discipline: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: run via the `/execute-plan` conventions (subagent-driven: `executor` per task, `reviewer` after each). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop plan-run agents from invoking test runners from bare repo roots and from full-suite runs per task, by encoding the cwd rule, package-manifest guard, and targeted-first scope into the executor/reviewer agent definitions and the execute-plan command, then syncing them live.

**Spec:** `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-design.md` (read it first; it contains the exact new wording and the user decision).

**Architecture:** Text-only change in this repo: one bullet replacement each in `agents/executor.md` and `commands/execute-plan.md`, one inserted paragraph in `agents/reviewer.md`, one commit. Activation is a machine-local copy of the three files into `~/.config/opencode/` (no commit, hash-verified). No hermes-console changes.

**Tech Stack:** Markdown, PowerShell 5.1, git, opencode CLI (validation only).

## Global Constraints

- No em-dash characters (U+2014) in any file written or edited.
- YAML frontmatter of agent files stays byte-identical; bodies only. Descriptions are public interface.
- Conventional Commits 1.0.0; this repo's plan-execution carve-out sanctions commits without asking.
- If a git hook rejects a commit, fix the named issue and re-commit; never use `--no-verify` for a content rejection.
- Skip verification commands that do not exist on the machine; note them, do not invent substitutes.
- Repo: `C:\Users\ruben\Projects\Tools\skills`; shell is PowerShell 5.1 (copy/hash steps), git via the bash tool.

---

### Task 1: Encode the rule in the three instruction files

**Files:**
- Modify: `agents/executor.md:35` (verify bullet)
- Modify: `agents/reviewer.md:43-45` (insert paragraph after the two passes)
- Modify: `commands/execute-plan.md:16` (verify bullet)

**Interfaces:**
- Produces: the final wording the reviewer checks in Task 2 and the sync sources for Task 3. No code interfaces.

- [ ] **Step 1: Edit `agents/executor.md`**

Replace this exact bullet (line 35):

```markdown
- Verify beyond unit tests: run lint, typecheck, tests, then exercise the real behavior path if the task has one. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

with:

```markdown
- Verify beyond unit tests: run lint, typecheck, tests, then exercise the real behavior path if the task has one. Copy test commands and their working directory from the project's AGENTS.md; never run a test runner from a directory that lacks its package manifest (package.json, pyproject.toml): a bare-root run crawls sibling packages and worktrees and reports false failures. Scope: targeted tests covering the files you changed, not the full suite; broader scope is the reviewer's call. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

- [ ] **Step 2: Edit `agents/reviewer.md`**

Replace:

```markdown
2. Code quality: correctness, error handling at trust boundaries, tests covering the new logic, ponytail violations (reinvented standard library, unneeded dependencies, speculative abstraction, dead flexibility).

Return short actionable findings
```

with:

```markdown
2. Code quality: correctness, error handling at trust boundaries, tests covering the new logic, ponytail violations (reinvented standard library, unneeded dependencies, speculative abstraction, dead flexibility).

Test runs: take the command, working directory, and scope from the project's AGENTS.md (where a reviewer fast-path is documented, e.g. `npx vitest run --changed main` from `frontend/`, use it). Targeted-first: re-check tests covering the diff; run the full suite only when targeted coverage is unclear or the branch is about to merge. Never run a test runner from a directory that lacks its package manifest.

Return short actionable findings
```

- [ ] **Step 3: Edit `commands/execute-plan.md`**

Replace this exact bullet (line 16):

```markdown
- Verify beyond unit tests: run the project's lint / typecheck / unit tests, then, if the task has a user-facing or integration behavior, exercise the actual path (start the dev server, hit the endpoint, open the route); passing unit tests are necessary, not sufficient. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

with:

```markdown
- Verify beyond unit tests: run the project's lint / typecheck / unit tests (commands, working directory, and scope per the project's AGENTS.md; targeted tests covering the changed files, never a runner invoked from a directory that lacks its package manifest), then, if the task has a user-facing or integration behavior, exercise the actual path (start the dev server, hit the endpoint, open the route); passing unit tests are necessary, not sufficient. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
```

- [ ] **Step 4: Em-dash scan on the three files**

Run: `Select-String -Path agents\executor.md,agents\reviewer.md,commands\execute-plan.md -Pattern ([char]0x2014)`
Expected: no output.

- [ ] **Step 5: Diff sanity check**

Run: `git diff --stat`
Expected: exactly 3 files changed, insertions/deletions consistent with the edits above; `git diff` shows no frontmatter changes.

- [ ] **Step 6: Commit**

```bash
git add agents/executor.md agents/reviewer.md commands/execute-plan.md
git commit -m "docs(skills): enforce test cwd and targeted scope in plan-run instructions"
```

### Task 2: Review the diff and validate the agent files parse

Dispatched to `reviewer` (read-only; runs the validation commands).

- [ ] **Step 1: Spec-compliance review**

Compare `git diff HEAD~1` against the spec's "Changes (exact new wording)" section. All three replacements verbatim; nothing else changed; frontmatter untouched.

- [ ] **Step 2: Parse validation**

Run: `opencode agent list` then `opencode debug agent executor` then `opencode debug agent reviewer`
Expected: both agents listed and resolved without errors. If the CLI is missing, note it and fall back to a YAML-fence check (file starts `---`, second `---` present, frontmatter byte-identical to `git show HEAD~1:agents/<file>`).

- [ ] **Step 3: Verdict**

Return PASS, or numbered findings (file:line, problem, fix). Findings route back to an executor re-dispatch; only re-review the fixed items.

### Task 3: Activate on this machine (sync, no commit)

Runs only after Task 2 PASS, so a rejected wording never gets synced.

- [ ] **Step 1: Copy the three files**

```powershell
$repo = "C:\Users\ruben\Projects\Tools\skills"
Copy-Item "$repo\agents\executor.md", "$repo\agents\reviewer.md" "$env:USERPROFILE\.config\opencode\agents\" -Force
Copy-Item "$repo\commands\execute-plan.md" "$env:USERPROFILE\.config\opencode\command\" -Force
```

- [ ] **Step 2: Hash-verify all three pairs**

```powershell
$pairs = @(
  @("$repo\agents\executor.md", "$env:USERPROFILE\.config\opencode\agents\executor.md"),
  @("$repo\agents\reviewer.md", "$env:USERPROFILE\.config\opencode\agents\reviewer.md"),
  @("$repo\commands\execute-plan.md", "$env:USERPROFILE\.config\opencode\command\execute-plan.md")
)
foreach ($p in $pairs) { $h = Get-FileHash $p; if ($h[0].Hash -eq $h[1].Hash) { "OK  $($p[0])" } else { "MISMATCH  $($p[0])" } }
```

Expected: three `OK` lines. Any MISMATCH: re-run Step 1, re-verify.

- [ ] **Step 3: Record activation caveat**

No commit (targets are outside the repo). Note for the report: activation requires an opencode restart; already-running sessions keep the old agent bodies.

---

## Closing phase (orchestrator, per execute-plan conventions)

1. `doc-standardizer` then `code-standardizer` against the branch diff (markdown-only; expect pass or trivial findings).
2. `documenter`: write `docs/artifacts/features/vitest-cwd-discipline/2026-09-16-vitest-cwd-discipline-report.md` (include: commits, diff stats, validation outputs, sync hashes OK, restart caveat, and the Unverified-in-advance item: behavioral effect observable only in the next hermes-console plan run, whose logs should show `cd frontend` test invocations and no bare-root `npx vitest run`); commit as docs. No catalog updates needed (no new skills or commands).
3. Final report per `commands/execute-plan.md` step 7.
