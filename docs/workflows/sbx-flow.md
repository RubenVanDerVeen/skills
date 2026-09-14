# sbx workflow: Plane to PR

The OpenCode Runner daemon (`daemon/opencode_runner.py` in the hermes-console repo) turns
Plane issues assigned to the `agent` user into sandboxed opencode runs and reports the
outcome back to the board: clone, run in an sbx sandbox, push a branch, open an
agent-authored PR, stop the sandbox for review. The opencode machinery inside the run
(planner, orchestrator, executor/reviewer/oracle subagents) is the standard AI workflow
and is documented in [workflow.md](workflow.md); this page covers only the Plane-to-PR
shell around it. Snapshot date: 2026-09-13.

## Board contract

| Thing | Rule |
|---|---|
| Poll | Every 30 s per configured project: issues whose assignees include `agent_assignee` (default `agent`) and whose state group is ready (default `started`; live board uses `unstarted`). |
| Type labels | `code`, `research`, `docs` set the task type and dispatch path. Other labels can select a model or an agent override. |
| Claim | PATCH to `In Progress` at run start, best-effort (a Plane hiccup never blocks execution). |
| Success | PATCH to `In Review` + a result comment. |
| Failure | PATCH to `Blocked` + a failure comment. Re-run is human-driven: move the issue back into the ready group and the next poll re-queues it (failed tasks are only skipped while they sit in `Blocked`). |
| Crash recovery | At boot, `startup_sweep` PATCHes orphan `In Progress` issues (from a crashed run) back to the ready group, so the next poll re-claims them. |

## Flow

1. **Poll.** `poll_tasks` queries the Plane issues API per project and hydrates each hit
   from the detail endpoint (the list API returns an empty description).
2. **Claim.** `claim_task` PATCHes the issue to `In Progress`, then the dispatch split
   below picks a path.
3. **Provision.** Shallow `git clone --depth 1` (300 s timeout) into
   `<workspace_root>/<issue-id>` (stale dir removed first), copy the `.opencode` bundle
   in, write `.base-sha` (clone HEAD, used later for the diff).
4. **Sandbox.** `sbx create --name oc-<id8> -m <sandbox_memory>` (`oc-` + first 8 chars of
   the task uuid; memory default `6g`), then prepare: allow-listed network egress (sbx is
   default-deny), provider keys into `auth.json`, git identity, and a pinned
   `npm install -g opencode-ai@<opencode_version>` (never `@latest`; a bad release must
   not roll into every new provisioning). Blocking calls run in threads so the poll loop
   stays responsive.
5. **Run.** `opencode run` via CLI (serve mode cannot resolve partner providers). The
   prompt travels as `.task-prompt.md` and ends with the contract: write an uncommitted
   `PR_DESCRIPTION.md` at repo root, never merge. `opencode.json` gets
   `permission: allow` for unattended runs. A daemon thread holds an attached `sbx exec`
   session for the run lifetime (sbx idle-stops sandboxes with no attached exec) and a
   45 s heartbeat touches `.run-output.txt` (silent attaches are dropped, and the stall
   watchdog must not fire during long silent reasoning). The inner script appends
   `EXIT:$RC` to `.run-output.txt` as the completion marker.
6. **Watchdog + self-heal.** The host polls for `EXIT:` every 15 s. If `.run-output.txt`
   goes idle past `stall_timeout` (default 600 s) the run is stalled. One in-place retry
   per task: kill opencode, relaunch `opencode run --continue` in the same sandbox
   (same session, context survives), reset the wall-clock budget. An exec death
   (exit 255/137: dropped attach or host OOM) counts as a stall and retries immediately.
   A second stall fails the task; the wall-clock cap `task_timeout` fails it regardless.
7. **Collect + PR.** Collect the branch, last 5 commits, and `diff --stat` against
   `.base-sha`. A pre-push guard amends an agent-committed `PR_DESCRIPTION.md` out of the
   push (untracked + `commit --amend`), then `git push -u origin HEAD`. The PR is
   agent-authored: `gh pr create --title <first line> --body-file PR_DESCRIPTION.md`
   (fallback `--fill`). `merge_on_complete` defaults to `false`: merging is human-only
   via the GitHub PR queue; the daemon pushes and opens the PR, nothing more.
8. **Report.** Comment on the issue and PATCH the state. Success: branch, commits, diff,
   a `sbx run --name oc-<id8>` review hint, and `PR: <url>`. Gateway-dispatched sessions
   reply with a `PR: <url>` or `FAILED: <reason>` line in their final message; the daemon
   extracts the last `PR:` line. No PR from a gateway code run means `Blocked`.
9. **Stop, not rm.** The sandbox is stopped and kept so reviews resume in the agent chat
   (`sbx run --name oc-<id8>`); `sbx rm` only when explicitly done. The retention sweep
   reaps terminal bridge sandboxes older than `sandbox_retention_days` (default 7,
   `0` disables) at boot; the boot sweep reaps orphan `oc-*` runtimes unknown to registry
   and daemon state.

## Dispatch split

| Path | When | What happens |
|---|---|---|
| Direct sandbox (default) | `code` label, no gateway config | The full Flow above: provision, sbx, opencode run, push, PR. |
| Profile gateway | `research` / `docs` labels; `code` when `code_dispatch: "gateway"` | A hermes-agent gateway session on the matching profile (research, note-taker, coder); no sandbox. Research/docs answers are posted as comments; gateway code runs must end with `PR: <url>` / `FAILED:`. |
| Space-linked | Project carries `workspace_id` and `console_base` is set | The console BFF creates the session inside the Workspace Space (`X-Console-Profile`, context injected on the first turn); reporting reuses the gateway tails. BFF session-create failure falls back to the direct gateway path; mid-turn failures surface as task timeouts. |

## Interactive path (make-sandbox)

The coder profile can spawn sandboxes on demand through the daemon's serve bridge instead
of waiting for Plane: `bash sandbox-task.sh create "<prompt>" [repo-url]`, `status <id>`,
`stop <id>` (skill `make-sandbox`). Verbs map to `POST /sandbox`, `GET /sandbox/{id}`
(carries a `stalled` flag), and `DELETE /sandbox/{id}` on `serve_host:serve_port`, auth is
a Bearer `BRIDGE_TOKEN` (refuses to bind if unset; constant-time compare). `create`
returns in milliseconds because provisioning runs as a background task; the 60 s curl cap
is defence-in-depth. State persists to `bridge-registry.json` (atomic write-through);
ghost or stale entries are reconciled at boot.

## Failure paths

- **Direct-path failure:** warning comment + debug hint, issue to `Blocked`, sandbox
  stopped and retained (stop-not-rm, so the run stays inspectable).
- **Bridge provisioning failure:** entry flips to `failed` with the error in `output`,
  partial sandbox stopped. A `DELETE` during provisioning tears down mid-flight work.
- **Gateway code run without a PR:** failure comment + output tail, issue to `Blocked`.
- **Daemon crash mid-run:** task ids are bucketed in `daemon-state.json`; `startup_sweep`
  resets the board so the next poll retries cleanly.
- **Bridge entry over wall-clock budget:** lazily marked failed and best-effort stopped.

## Config

Secrets are env-var *names* in `daemon/config.json`, resolved at runtime. Keys that matter:

| Key | Default | Meaning |
|---|---|---|
| `plane_base_url`, `plane_api_key` | - | Plane API (`PLANE_API_KEY`). |
| `agent_assignee`, `ready_state_group`, `in_progress_state`, `review_state`, `blocked_state` | `agent`, `started`, `In Progress`, `In Review`, `Blocked` | Board mapping. |
| `code_dispatch` | direct sandbox | `"gateway"` routes code tasks through the coder profile session. |
| `console_base` + project `workspace_id` | unset | Space-linked dispatch through the console BFF. |
| `merge_on_complete` | `false` | Human-only merging when false; ff-merge to `integration_branch` only when explicitly true. |
| `sandbox_memory` | `6g` | `sbx create -m` cap (empty string disables). |
| `stall_timeout`, `task_timeout` | `600` s, `600` s (live config ships `3600` for task_timeout) | Idle-watchdog and wall-clock caps. |
| `sandbox_retention_days` | `7` | Reap terminal bridge sandboxes older than this (`0` disables). |
| `opencode_version` | `1.18.29` | Pinned npm install during provisioning. |
| `serve_host`, `serve_port`, `bridge_token` | `172.21.0.1:4096`, `BRIDGE_TOKEN` | Serve bridge (used by make-sandbox). |
| `projects.<id>.repo_url`, `branch_prefix`, `git_remote`, `workspace_id` | - | Per-project wiring. |

## Infra

- `daemon/opencode-runner.service`: systemd **system** unit on the GeneralDock host (not in
  a container), `EnvironmentFile=/home/ruben/hermes-console/.env`, `Restart=on-failure`.
- `daemon/sbx-daemon.service`: systemd **user** unit wrapping `sbx daemon start`; needs
  `loginctl enable-linger`. The unit shows `inactive (dead)` after ~20 s because sbx forks;
  it is a boot-starter, not a monitor. If it is down, bridge creates stall.
- `daemon/nas-repos-fetch.{service,timer}`: 15-minute ff-only pulls of the NAS clones
  (the `.opencode` bundle comes from there); escalates to the capture inbox after 2
  consecutive failures.
- `daemon/setup-github-auth.sh`: one-time PAT wiring for `git push` + `gh pr create`
  (credential helper + `gh auth login`); idempotent for rotation.

## Related

- [workflow.md](workflow.md): the AI workflow itself. The planner, orchestrator, and
  executor/reviewer/oracle subagent flow that runs inside `opencode run` is documented
  there, not here.
