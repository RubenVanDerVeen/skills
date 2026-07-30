# extraction: session source and commands

Verified on Windows 11 with PowerShell 5.1 and sqlite3 (msys64 ucrt64), 2026-07-02. Run the sql via the `sqlite3` CLI.

## State file

`~/.skill-harvest-state.json`:

```json
{ "opencode": "2026-07-02T12:00:00Z" }
```

Read (missing file: fall back to 30-day lookback):

```powershell
$statePath = "$env:USERPROFILE\.skill-harvest-state.json"
$since = if (Test-Path $statePath) { [datetime]::Parse((Get-Content $statePath -Raw | ConvertFrom-Json).opencode) } else { (Get-Date).AddDays(-30) }
```

Write (after a run; set the value to the mtime of the NEWEST session processed in the batch, not `now`). With oldest-first enumeration this is the natural cursor: it advances past exactly what was processed, never re-processing, never orphaning. If no sessions were processed, leave the timestamp unchanged:

```powershell
@{ opencode = $newestOc } | ConvertTo-Json | Set-Content $statePath -Encoding utf8
```

Note: older state files also carry a `claude-code` key from when Claude Code was mined; that key is vestigial now and ignored. Safe to delete on next write.

## Source: opencode

Storage is SQLite: `~/.local/share/opencode/opencode.db`. Tables: `session` (id, parent_id, directory, title), `message` (session_id, time_created ms-epoch, data JSON with `role`), `part` (message_id, data JSON with `type`, `text`, `synthetic`).

User messages since a ms-epoch timestamp (top-level sessions only; `parent_id IS NULL` excludes subagent dispatch prompts, `synthetic` excludes injected content, the `NOT LIKE` filters drop eval/synthetic dirs and an explicit project filter overrides them):

```sql
SELECT s.directory, m.session_id, json_extract(p.data,'$.text')
FROM part p
JOIN message m ON p.message_id = m.id
JOIN session s ON m.session_id = s.id
WHERE json_extract(m.data,'$.role') = 'user'
  AND json_extract(p.data,'$.type') = 'text'
  AND json_extract(p.data,'$.synthetic') IS NOT 1
  AND s.parent_id IS NULL
  AND s.directory NOT LIKE '%ai-harness-eval%'
  AND s.directory NOT LIKE '%.minimax%'
  AND m.time_created > :since_ms
ORDER BY m.time_created ASC;
```

Run:

```powershell
sqlite3 "$env:USERPROFILE\.local\share\opencode\opencode.db" "<query with :since_ms replaced by a number>"
```

Compute `:since_ms` from the state timestamp:

```powershell
[long](([datetime]::Parse($state.opencode).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds)
```

Project filter: add `AND s.directory LIKE '%<project>%'`.

Record `$newestOc` = the ISO timestamp derived from the largest `time_created` in the batch (the cursor to write). DB missing or locked: skip the source, note it in the report, do not advance the timestamp.

## Defensive text filter

`synthetic IS NOT 1` plus `parent_id IS NULL` already drop most non-user content. Apply this filter to the returned text rows anyway, since tool/synthetic blocks occasionally leak through as user-role text. It drops command wrappers, compaction-summary markers, and subagent `<task-notification>`/`<result>`/`<usage>` blocks:

```powershell
$rows | Where-Object {
  $_ -and $_ -notmatch '^(Base directory for this skill|<system-reminder>|<command-name>|<local-command|This session is being continued|Continue the conversation from where it left off|If you need specific details|Caveat:|Summary:|<task-notification>|</task-notification>|<result>|</result>|<usage>|<note>|<status>|<summary>|<task-id>|<tool-use-id>|<output-file>)'
}
```

Interruption markers (corrections; they arrive as user messages starting with `[Request interrupted by user`) survive this filter on purpose: an interruption immediately followed by a redirecting message is a strong correction signal.
