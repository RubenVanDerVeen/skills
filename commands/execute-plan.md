---
description: Execute an approved implementation plan via the full subagent-driven-development skill (implementer + spec + quality review per task): branch, ponytail, per-task commits, final report
---

Execute the plan at `$ARGUMENTS` using the `subagent-driven-development` skill: fresh implementer subagent per task, then spec-compliance review, then code-quality review, then a final whole-implementation review. Follow the skill's process; the items below are project-specific defaults and conventions the skill does not cover.

Setup:
1. Read the plan. If it references a spec (e.g. under `docs/artifacts/specs/`), read that too. Default to inferring; ask only if the plan path is unresolvable or the plan contradicts itself. A missing detail is not a blocker, pick the obvious choice, note it, proceed. The plan you were given is the spec; do not write a new one.
2. Branch first, before any edit. Run `git rev-parse --abbrev-ref HEAD`; if it returns `main`, `master`, or the repo default, create and switch to `<type>/<plan-slug>`. Pick `<type>` from what the plan does: `feat` for a new feature, `fix` for a bug fix, `refactor` / `chore` / `docs` for those (match the dominant Conventional Commit type the plan will produce). `<plan-slug>` = the plan filename stem with any leading date stripped (e.g. `2026-07-04-add-auth.md` → `add-auth`). Re-run `git branch --show-current` and do not proceed until you are off the default branch. Worktree or plain branch both fine; pick per the `using-git-worktrees` skill. As the first commit on the branch, `git add` the plan and any spec it references, commit as `docs: add plan and spec for <plan-slug>`; the artifacts describing the work ship with the work.
3. If the invocation includes an exclusion line (e.g. `skip the X/Y/Z steps`), honor it and verify at the end that those paths were untouched (`git diff --name-only <base>..HEAD` against the exclusion list).

Per-task instructions to fold into every implementer subagent dispatch (the skill's prompt template is the spine; add these):
- Apply the `ponytail` skill: stdlib and native first, shortest working diff, no speculative abstraction. Before creating a new file, grep for an existing one that already serves the purpose (deploy scripts, registries, configs, index files) and extend it instead. Mark deliberate shortcuts with `ponytail:` comments.
- Verify beyond unit tests: run the project's lint / typecheck / unit tests, then, if the task has a user-facing or integration behavior, exercise the actual path (start the dev server, hit the endpoint, open the route); passing unit tests are necessary, not sufficient. If a behavior cannot be verified here (browser, hardware, external service), do not claim it works, list it as Unverified. Skip commands that do not exist; do not invent new ones.
- Commit with Conventional Commits 1.0.0 (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, ...). The repo's plan-execution carve-out sanctions per-task commits; do not pause to ask. If the task touched a sibling repo (deploy scripts, compose files), commit there too, separately.

End:
4. After the skill's final whole-implementation review, stop. Do NOT invoke `finishing-a-development-branch` or offer merge/PR unless the user asks. Instead report: branch name; commits with hashes and one-line descriptions; files changed with diff stats; verifier output (test counts, build/typecheck result); skills loaded across the run (name + one line on how each shaped the work); any `ponytail:` deferrals; anything Unverified.
