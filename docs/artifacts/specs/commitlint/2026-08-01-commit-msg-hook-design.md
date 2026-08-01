# commit-msg hook: Conventional Commits enforcement, no dependencies

Date: 2026-08-01
Status: approved (single-pass run, no gate)

## Goal

Enforce Conventional Commits 1.0.0 on every commit made in this repo, without adding the npm toolchain (`@commitlint/cli` + husky + `package.json` + `node_modules`) that the linked project ships. The enforcement must catch the agent-made commits of the `/execute-plan` and `/full-cycle` workflows, where an executor or orchestrator subagent runs `git commit` on its own. A misbehaving or forgetful agent should have its bad message rejected at the git layer, not just advised against in agent docs.

## Context (current state, 2026-08-01)

- This repo is Markdown-only by design. `AGENTS.md` Stack section: "Content: Markdown only. No build step, no tooling, no runtime." There is no `package.json`, no `node_modules`, no `.husky`, no `.github/workflows`, and no git hooks at all (`core.hooksPath` unset, no non-sample hooks in `.git/hooks`).
- `.gitignore` is minimal (editor swap files, OS files). No `.gitattributes` exists.
- Every commit is made by an AI agent (executor/orchestrator subagents) following the `AGENTS.md` rule. Last 20 commits: 100% clean Conventional Commits. There is no historical violation problem; the hook is guardrails for the future, not a fix for the present.
- The Conventional Commits rule is stated in three places that slightly disagree on the type list:
  - `AGENTS.md` line 180: "`chore:`, `docs:`, `feat:`, `fix:`, `refactor:` are the common types" (the 5 most used).
  - `STANDARDS.md` line 73: "`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`" (the fuller set, missing `revert`).
  - Conventional Commits 1.0.0 + `@commitlint/config-conventional` default: the 11-type set including `revert`.
- Commit workflow lives in `AGENTS.md` `## Git & workflow` (lines 175-182) and the per-machine setup lives in `opencode-install.md` (9 numbered install steps; no step enables a git hook today).

## Decisions (locked with user)

1. **Approach A: tracked `commit-msg` git hook, no dependencies.** Set `core.hooksPath = .githooks/`, ship a POSIX `sh` hook that regex-checks the commit subject. This is commitlint's actual function (commit-msg enforcement) done with git's built-in hook system instead of a JS dependency.
2. **Rejected: npm `@commitlint/cli` + husky (Approach B).** Would introduce `package.json` + `node_modules` + a JS toolchain into a repo that explicitly forbids tooling, for marginal gain over a regex hook when commits are agent-made and already conform.
3. **Rejected: agent-side validation step (Approach C).** Advisory only (the agent that writes a bad message polices it; can be skipped; covers nothing for manual commits). Strictly weaker than a git hook.
4. **Type allow-list:** the full `@commitlint/config-conventional` 11-type set (`feat fix docs style refactor perf test build ci chore revert`). More permissive than either current doc list, so it never false-rejects. This reconciles the two lists and adds `revert`, which Conventional Commits 1.0.0 includes.
5. **Enforcement scope: subject line only.** No subject-case, no header-max-length, no body-line-length rules. Those are `config-conventional` opinions the repo does not currently rely on; adding them is scope creep (YAGNI).
6. **Bypass:** `git commit --no-verify` remains the documented emergency exit. Agents will not use it (they follow `AGENTS.md`); humans can in a pinch.

## Design

### The hook

A single file, `.githooks/commit-msg` (no extension), POSIX `sh`, executable. Git invokes it with `$1` = path to a temp file holding the proposed commit message. Git for Windows runs `sh` hooks via its bundled bash; the same file is portable to macOS/Linux.

Logic:

1. Read the subject = the first line of the message file that is neither blank nor a `#` comment (commit-msg files append `#`-prefixed status/template lines after the subject).
2. Skip git-internal messages the workflow does not rewrite into Conventional Commits: subjects starting with `Merge `, `Revert `, `fixup! `, `squash! `.
3. Match the subject against the Conventional Commits regex. On failure, print a helpful stderr message (expected format, type list, example, the `--no-verify` escape hatch) and exit 1. On success, exit 0.

Regex: `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: .+`

- `type` from the fixed 11-type set.
- `(scope)` optional; if present, must contain at least one character (rejects the malformed `feat(): ...` form).
- `!` optional (breaking-change marker).
- `: ` required, followed by at least one character of description.

Full script (this is the deliverable; the plan reproduces it verbatim):

```sh
#!/bin/sh
# commit-msg hook: enforce Conventional Commits 1.0.0 on the subject line.
# ponytail: this is commitlint's job done with stdlib (git hooks + grep).
# Ceiling: no automated test; no config-conventional extras (subject-case,
# header-max-length, body-max-line-length). Re-verify with the sample messages
# in the plan/spec if the regex changes. Upgrade path: swap for @commitlint/cli
# + husky if those rule sets are needed (adds node_modules to this repo).

msg_file="$1"

# Subject = first line that is not blank and not a '#' comment.
subject=$(grep -vE '^[#[:space:]]*$' "$msg_file" | head -n 1)

# Skip git-internal messages we do not rewrite into Conventional Commits.
case "$subject" in
  "Merge "*|"Revert "*|"fixup! "*|"squash! "*) exit 0 ;;
esac

# Conventional Commits: <type>(<scope>)!: <description>
regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: .+'

if ! printf '%s\n' "$subject" | grep -qE "$regex"; then
  cat >&2 <<EOF
commit-msg: rejected, not Conventional Commits 1.0.0

  $subject

Expected: <type>(<scope>)!: <description>
Types:   feat fix docs style refactor perf test build ci chore revert
Scope:   optional, e.g. (skills)
Example: feat(skills): add commitlint hook

Bypass (emergencies only): git commit --no-verify
EOF
  exit 1
fi
```

### Activation and portability

Three things must be true or the hook silently does nothing or breaks:

1. **`core.hooksPath`.** Git must be told to look in the tracked dir. One-time per clone: `git config core.hooksPath .githooks`. This is a machine-local config write (`.git/config`), not committed. The setup step goes into `opencode-install.md` as a new step 10.
2. **Executable bit.** On Windows the filesystem has no Unix mode bit, so the tracked blob would land non-executable and break macOS/Linux clones. Fix at commit time: `git update-index --chmod=+x .githooks/commit-msg` before committing, so the index records mode `100755`.
3. **LF line endings.** Git runs the working-tree copy of the hook. If `core.autocrlf=true` (a common Windows default), a fresh checkout would rewrite the hook to CRLF and the `#!/bin/sh` shebang becomes `#!/bin/sh\r`, which bash cannot exec. Fix: a repo-root `.gitattributes` pinning `.githooks/** text eol=lf`, which forces LF in the working tree regardless of `autocrlf`.

### Where it is documented

- `opencode-install.md`: new step 10, "Enable the commit-msg hook" (`git config core.hooksPath .githooks`), plus a note that the hook ships tracked and executable.
- `AGENTS.md` `## Git & workflow`: one new bullet stating commits are hook-enforced and pointing at `.githooks/commit-msg` and the activation step. Reconcile the type list to the full 11-type set so the doc matches the hook.
- `STANDARDS.md` `## Commit messages`: add `revert` to the type list (reconcile with the hook), and add one line noting enforcement is a tracked `commit-msg` hook. Add `.githooks/` and `.gitattributes` to the Repository layout tree.
- `CHANGELOG.md` `## [Unreleased]` -> `### Added`: one entry describing the hook and the activation step.

## Required changes

Committed source-of-truth edits:

- Create `.githooks/commit-msg` (the script above), tracked as executable (`git update-index --chmod=+x`).
- Create `.gitattributes` at repo root with `.githooks/** text eol=lf` (one directive; if a `.gitattributes` already existed we would append, but none exists).
- Modify `opencode-install.md`: append step 10 "Enable the commit-msg hook".
- Modify `AGENTS.md` `## Git & workflow`: add the enforcement bullet; reconcile the type list.
- Modify `STANDARDS.md` `## Commit messages`: add `revert`; add the enforcement line; extend the layout tree with `.githooks/commit-msg` and `.gitattributes`.
- Modify `CHANGELOG.md`: add the Unreleased/Added entry.

Machine-local (not committed):

- `git config core.hooksPath .githooks` (writes `.git/config`).
- `git update-index --chmod=+x .githooks/commit-msg` (stages the mode bit into the commit).

## Verification

The plan proves the hook works by feeding it sample messages through git's real hook path (not a re-implementation):

- `feat(skills): add commitlint hook` -> commit succeeds (exit 0).
- `updated stuff` -> commit rejected (exit 1) with the help message.
- `Merge branch 'x'` -> commit succeeds (skip rule).
- `docs: ` (empty description) -> rejected.
- A real `git commit` on the task branch goes through the hook and is accepted (the per-task commits of this very plan exercise it live).

Line-ending and mode checks:

- `git ls-files --eol .githooks/commit-msg` shows `eol=lf` (no CRLF in working tree).
- `git ls-files -s .githooks/commit-msg` shows mode `100755`.

## Out of scope (YAGNI)

- npm `@commitlint/cli` / husky / `package.json` / `node_modules` (Approach B).
- CI-side commit check on push (`.github/workflows`). Local hook covers the stated goal; add CI only if remote enforcement is later required.
- `config-conventional` extras: subject-case, header-max-length, body-max-line-length.
- Automated test harness for the regex. The hook is a single regex; the plan's sample-message checks prove it now, and the `ponytail:` ceiling comment documents that the regex has no standing test and must be re-verified by hand if edited.
- Folding this hook into the `project-standardization` skill's offer to other projects. That is a separate feature (the skill gains a commitlint track); out of scope here.
