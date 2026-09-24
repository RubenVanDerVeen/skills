# Superpowers Fork Execution Report

Date: 2026-09-24
Plan: `docs/artifacts/features/superpowers-fork/2026-09-24-superpowers-fork-plan.md`
Spec: `docs/artifacts/features/superpowers-fork/2026-09-24-superpowers-fork-design.md`

## Summary

Branch `feat/superpowers-fork` vendored the five superpowers process skills (`brainstorming`, `writing-plans`, `using-git-worktrees`, `systematic-debugging`, `writing-skills`) into `skills/`, tailored to repo conventions, repointed every live reference away from the `superpowers:` namespace, and removed the superpowers plugin from machine config. HEAD at close-out start: `55352f9`; this commit adds the report plus two reviewer cosmetic fixes. Repo is unversioned (no `### Versioning` in AGENTS.md): no bump.

## Commits

8 commits on the branch (1 bootstrap + 5 vendor + 1 docs ref + 1 quick-fix):

| Hash | Task | Subject |
|---|---|---|
| `f32d020` | bootstrap | docs: add plan and spec for superpowers-fork |
| `e3cb6a5` | 1 | feat(skills): vendor brainstorming from superpowers, tailored to repo conventions |
| `a9c5455` | 2 | feat(skills): vendor writing-plans from superpowers, native artifact paths |
| `0b52afd` | 3 | feat(skills): vendor using-git-worktrees from superpowers |
| `3a951c0` | 4 | feat(skills): vendor systematic-debugging from superpowers |
| `9339f9a` | 5 | feat(skills): vendor writing-skills from superpowers, examples moved to references |
| `9b0d4c4` | 6 | docs(skills): point live flows at vendored process skills, drop superpowers namespace |
| `55352f9` | quick-fix | docs: structure-review quick-fix batch (catalogs, install refs, changelog) |

## Files changed

Aggregate: 22 files, +3597 / -41 lines (`git diff --stat main..HEAD`). Grouped by task:

- Bootstrap (`f32d020`): `2026-09-24-superpowers-fork-design.md` (+120), `2026-09-24-superpowers-fork-plan.md` (+422).
- Task 1 brainstorming: `skills/brainstorming/SKILL.md` (+107); catalog rows in `README.md`, `AGENTS.md`.
- Task 2 writing-plans: `skills/writing-plans/SKILL.md` (+125); catalog rows.
- Task 3 using-git-worktrees: `skills/using-git-worktrees/SKILL.md` (+200); catalog rows.
- Task 4 systematic-debugging: `SKILL.md` (+209), `references/root-cause-tracing.md` (+169), `references/defense-in-depth.md` (+122), `references/condition-based-waiting.md` (+115); catalog rows.
- Task 5 writing-skills: `SKILL.md` (+240), `references/anthropic-best-practices.md` (+1150), `references/testing-skills-with-subagents.md` (+382), `references/persuasion-principles.md` (+187); catalog rows.
- Task 6 live references (8 files): `skills/multi-plan-orchestration/SKILL.md`, `skills/rubens-project-standardization/references/artifacts.md`, `AGENTS.md`, `opencode-install.md`, `external-skills.md`, `README.md`, `docs/workflows/workflow.md`, `docs/workflows/stack.drawio`.
- Quick-fix batch: `AGENTS.md`, `CHANGELOG.md`, `README.md`, `opencode-install.md`.
- Task 7 machine config (no commit, outside repo): `~/.config/opencode/opencode.json` plugin array, `npm uninstall superpowers`, skill folders synced to both agent dirs.

## Verification evidence

Actual outputs, run 2026-09-24 at close-out:

1. Em-dash byte scan over the whole repo (pre-commit hook's POSIX approach, U+2014 as UTF-8 bytes via pattern file):

   ```
   $ printf "\342\200\224" > /tmp/emdash.bin
   $ git grep -nF -f /tmp/emdash.bin
   exit:1
   ```

   Empty (git grep exit 1 = no matches in tracked files).

2. Live namespaced references:

   ```
   $ git grep -in "superpowers:" -- ':!docs/artifacts'
   (no output, exit 1)
   ```

3. Catalog completeness (all 5 in both tables, folder = frontmatter name):

   ```
   brainstorming readme=True agents=True frontmatter-name=brainstorming
   writing-plans readme=True agents=True frontmatter-name=writing-plans
   using-git-worktrees readme=True agents=True frontmatter-name=using-git-worktrees
   systematic-debugging readme=True agents=True frontmatter-name=systematic-debugging
   writing-skills readme=True agents=True frontmatter-name=writing-skills
   ```

4. Package removed:

   ```
   $ npm ls superpowers --prefix ~\.config\opencode
   opencode@ C:\Users\ruben\.config\opencode
   └── (empty)
   ```

5. `opencode.json` validity: `node -e "JSON.parse(...)"` printed `valid`.

6. Sync targets (folder with `SKILL.md` present in both agent dirs): 5 of 5 in `~\.claude\skills\` and 5 of 5 in `~\.config\opencode\skills\` (per-skill `Test-Path` all True).

7. Pre-commit hook accepted every commit above; `git commit --no-verify` was never used (per dispatch log).

## Skills loaded

- `executing-plans`: per-task executor + reviewer dispatch, sequential Tasks 1-5 (shared catalog files), Task 7 last so nothing resolved a missing skill mid-run.
- `writing-skills`: repo frontmatter and body rules applied while tailoring each vendored `SKILL.md` (Use when... description, `## Overview`, no em-dashes, references split).

## Dispatch Log

- Task 1: dispatched: executor + reviewer
- Task 2: dispatched: executor + reviewer
- Task 3: dispatched: executor + reviewer
- Task 4: dispatched: executor + reviewer
- Task 5: dispatched: executor + reviewer + amend
- Task 6: dispatched: executor + reviewer
- Task 7 (machine config, no commit): dispatched: executor + reviewer
- Structure review: doc-standardizer + code-standardizer, concurrent
- Quick-fix batch (commit `55352f9`): executor + reviewer
- Close-out: documenter (this report + two cosmetic fixes, one commit)

## Accepted losses

Per spec, accepted by design:

- No upstream superpowers updates; the flow has diverged and updates were drift risk, not value.
- The `using-superpowers` bootstrap injection is gone for sessions outside this repo.
- `verification-before-completion` was never referenced anywhere and is not vendored.

## Open items

- Branch is ready for user review. Not pushed, not merged (plan Task 8 Step 4).
- `ponytail:` deferrals flagged by executors, all accepted as-is:
  - `skills/systematic-debugging/references/root-cause-tracing.md:101-104` still references `find-polluter.sh`, which was not vendored (dangling pointer into the removed `*.sh` set).
  - `systematic-debugging` body is 1249 words, over the lean-skill budget; trim candidate for a later pass.
  - All five bodies exceed the 500-word "frequently-loaded" budget (979 / 859 / 1103 / 1249 / 1836 words); the plan sanctioned bodies up to ~2000 words, so only `writing-skills` is near its ceiling.
- Cosmetic follow-ups from the quick-fix reviewer, fixed in this commit: CHANGELOG `feat(skills)` bullets now backtick only the skill name (matching existing entries), and `AGENTS.md` git-hooks pointer corrected from `opencode-install.md` step 10 to step 9 (the doc has nine numbered steps since Task 6 removed the superpowers install step).
- Same stale "step 10" reference exists at `STANDARDS.md:86`; outside this dispatch's edit scope (report, CHANGELOG, AGENTS only), left for a follow-up commit. `CHANGELOG.md:29` also says step 10 but is a historical record of the original commit-msg entry: intentionally untouched.

## Spec/plan not modified

`2026-09-24-superpowers-fork-design.md` and `2026-09-24-superpowers-fork-plan.md` are untouched since bootstrap commit `f32d020`. This report is the only new artifact in `docs/artifacts/features/superpowers-fork/`.
