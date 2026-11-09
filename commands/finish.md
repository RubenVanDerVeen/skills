---
description: Finish a feature branch: dispatches the shipper subagent to open the PR, ask merged/pull/abort, and cut the tag and release on merge
---

Dispatch the `shipper` subagent with $ARGUMENTS (optional branch name, PR number, or report path; default: the current branch). When it returns a `DECISION NEEDED` block instead of having asked the user directly, ask the user the same 3 options (merged: create tag and release / merged: pull locally only / not merged: abort), then re-dispatch the shipper with the chosen `decision` (`release`, `pull`, or `abort`). Relay its final report: PR URL, version, tag, release URL. If the `shipper` agent is not installed, follow the flow in `agents/shipper.md` inline in this session instead.
