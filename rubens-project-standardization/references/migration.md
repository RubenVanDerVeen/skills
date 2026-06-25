# Migration from older conventions

This skill evolved from an earlier Claude-Code-only version (`rubens-project-standardization`). Several existing projects (Homelab, IDP, others) still contain a `CLAUDE.md` that holds the actual guidance (not a shim), on-demand directories under `claude/` or `.claude/`, or references to the old skill name.

## Two paths

1. **Gradual**: keep the project's existing `CLAUDE.md` content, but add a thin `AGENTS.md` that defers to it (`Project guidance lives in @CLAUDE.md.`). On-demand files in `claude/` or `.claude/` keep working — register them in `AGENTS.md`'s on-demand table using whatever path the active tool expects.
2. **Full migration**: move actual guidance from `CLAUDE.md` to `AGENTS.md`, replace `CLAUDE.md` with the shim, rename the on-demand directory to `.agents/` (or the tool's preferred subdir). Use `references/tool-filenames.md` as the substitution map.

When working in a project that still references `rubens-project-standardization`, prefer this skill's guidance and propose one of the two paths.

## Older `project-standardization.md` copies

This skill also replaces `ContextMD/project-standardization.md`. Several existing projects (Homelab, IDP, others) contain copies of that older doc under `claude/project-standardization.md`. Those copies are stale. Prefer this skill's guidance over the local copy; propose deleting the local copy.
