# extraction: session sources and commands

Verified on Windows 11 with PowerShell 5.1 and sqlite3 (msys64 ucrt64), 2026-07-02. Run PowerShell blocks in PowerShell, sql via the `sqlite3` CLI.

## State file

`~/.skill-harvest-state.json`:

```json
{ "claude-code": "2026-07-02T12:00:00Z", "opencode": "2026-07-02T12:00:00Z" }
```

Read (missing file: fall back to 30-day lookback):

```powershell
$statePath = "$env:USERPROFILE\.skill-harvest-state.json"
$since = if (Test-Path $statePath) { [datetime]::Parse((Get-Content $statePath -Raw | ConvertFrom-Json).'claude-code') } else { (Get-Date).AddDays(-30) }
```

Write (after a run; use the oldest-unprocessed-session time instead of now when the 40-session cap was hit):

```powershell
@{ 'claude-code' = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'); 'opencode' = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') } | ConvertTo-Json | Set-Content $statePath -Encoding utf8
```

## Source 1: Claude Code

Sessions: `~/.claude/projects/<encoded-project-dir>/<session-id>.jsonl`. Project dirs encode the working directory (`C--Users-ruben-projects-hobby-homelab`), so a project filter is a wildcard on the folder name.

Enumerate (newest first, capped):

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\projects\*\*.jsonl" | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime -Descending | Select-Object -First 40
```

With project filter: replace the first `*` with `*<project>*`.

Digest one file (user messages only; drops sidechains, skill payloads, system reminders, command wrappers; counts malformed lines):

```powershell
$skipped = 0
$digest = Get-Content $f.FullName | ForEach-Object {
  try { $j = $_ | ConvertFrom-Json } catch { $skipped++; return }
  if ($j.type -ne 'user' -or $j.isSidechain) { return }
  $t = if ($j.message.content -is [string]) { $j.message.content } else { ($j.message.content | Where-Object { $_.type -eq 'text' } | ForEach-Object { $_.text }) -join ' ' }
  if (-not $t) { return }
  if ($t -match '^(Base directory for this skill|<system-reminder>|<command-name>|<local-command)') { return }
  $t
}
```

Interruption markers (corrections; they arrive as user messages starting with `[Request interrupted by user`) survive these filters on purpose: an interruption immediately followed by a redirecting message is a strong correction signal.

## Source 2: opencode

Storage is SQLite: `~/.local/share/opencode/opencode.db`. Tables: `session` (id, parent_id, directory, title), `message` (session_id, time_created ms-epoch, data JSON with `role`), `part` (message_id, data JSON with `type`, `text`, `synthetic`).

User messages since a ms-epoch timestamp (top-level sessions only; `parent_id IS NULL` excludes subagent dispatch prompts, `synthetic` excludes injected content):

```sql
SELECT s.directory, m.session_id, json_extract(p.data,'$.text')
FROM part p
JOIN message m ON p.message_id = m.id
JOIN session s ON m.session_id = s.id
WHERE json_extract(m.data,'$.role') = 'user'
  AND json_extract(p.data,'$.type') = 'text'
  AND json_extract(p.data,'$.synthetic') IS NOT 1
  AND s.parent_id IS NULL
  AND m.time_created > :since_ms
ORDER BY m.time_created DESC;
```

Run:

```powershell
sqlite3 "$env:USERPROFILE\.local\share\opencode\opencode.db" "<query with :since_ms replaced by a number>"
```

Compute `:since_ms` from the state timestamp:

```powershell
[long](([datetime]::Parse($state.opencode).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds)
```

Project filter: add `AND s.directory LIKE '%<project>%'`. Apply the same `^Base directory for this skill` text filter defensively. DB missing or locked: skip the source, note it in the report, do not advance its timestamp.

## Linux variant (secondary)

Claude Code digest with jq, same filters:

```bash
jq -r 'select(.type=="user" and (.isSidechain|not)) | .message.content | if type=="string" then . else (map(select(.type=="text")|.text)|join(" ")) end' "$f" | grep -vE '^(Base directory for this skill|<system-reminder>|<command-name>|<local-command)'
```
