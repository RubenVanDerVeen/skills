# Single-commit fixes land directly on `main`

- Date: 2026-11-16
- Status: active
- Source: user rule (2026-11-16)

## Choice
A fix that ships as exactly one commit and carries no spec and no plan lands directly on the default branch (`main`): one commit, no feature branch, no worktree, no PR, no shipper, no tag or release. The full path (spec plus plan) keeps its feature branch and the shipper tail (PR, merge question, tag and release). The quick path in `agents/planner.md` (step 3), `agents/executor.md`, and `commands/full-cycle.md` (step 2) drops the branch from the executor brief and stops after the relay; the shipper dispatch stays a full-path step (`agents/planner.md` step 8, `commands/full-cycle.md` step 7).

## Rationale
A PR for a one-commit fix costs a branch, a push, a PR body, a merge, and a review pass to deliver one commit that could land on `main` directly. The branch and the shipper earn their keep on work that needs a review trail (a spec, a plan, more than one commit); on a single-commit fix they are ceremony around a diff the user reads in git log anyway. The quick path already runs without a reviewer, so the PR review pass was the only review the shipper added, and the scope-creep stop remains the quick path's safety valve.

## Alternatives rejected
- Keep the branch and the shipper on the quick path: preserves a uniform tail, but pays branch plus push plus PR plus merge for a fix that ships as one commit.
- Branch but no PR: leaves a one-commit branch nobody merges, and the branch still has to be cleaned up later.
- Push the single commit to `main` directly from a side branch: the branch adds nothing over committing on `main` and still needs a delete.

## Supersedes
- `2026-11-13-quick-path-single-executor-no-reviewer-decision.md`: it stated that the shipper tail runs after the relay on both paths.
- `2026-11-13-plan-file-implies-full-path-decision.md`: it stated that the shipper runs identically on both paths.

Both records keep their bodies; only their status lines change.

## Revisit when
The quick path starts producing fixes that need a real review before landing, or a single-commit fix turns out to be routinely wrong in a way a PR review would have caught.
