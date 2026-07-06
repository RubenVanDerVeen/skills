# Tool-specific filenames

Canonical: `AGENTS.md` + `CLAUDE.md` shim + `.agents/<topic>.md`. Most tools honour these. Where they do not, substitute from this table.

| Tool | Context file (root) | On-demand subdir | Notes |
|------|--------------------|------------------|-------|
| `AGENTS.md` convention (opencode, Codex, Cursor, Aider, GitHub Copilot, Hermes, etc.) | `AGENTS.md` | `.agents/<topic>.md` | Baseline. |
| opencode | `AGENTS.md` | `.agents/<topic>.md` | `AGENTS.md` honoured at any depth. |
| Codex | `AGENTS.md` | `AGENTS.md` files at any path | No subdir convention; one file per scope. |
| Cursor | `AGENTS.md` (or `.cursorrules`) | `.cursor/rules/` | `.cursorrules` is the older single-file format. |
| **Claude Code** | `CLAUDE.md` (must `@import AGENTS.md`) | `.claude/` (project) + `~/.claude/` (global) | Does **not** read `AGENTS.md` natively. The `@AGENTS.md` shim is what makes cross-agent guidance visible. |
