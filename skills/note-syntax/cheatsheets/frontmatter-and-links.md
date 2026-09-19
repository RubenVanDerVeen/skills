# Cheatsheet: frontmatter, wikilinks, tags

## YAML frontmatter

Optional but standard. Opens the file, delimited by `---` lines, plain YAML:

```yaml
---
title: Cloudflare Tunnel
type: entity
date: 2026-09-13
tags: [cloudflare, tunnel, ingress]
aliases: [cloudflare, cf-tunnel]
related:
  - "[[homelab]]"
  - "[[topics/insumo/README|Insumo]]"
---
```

- Quote wikilinks inside lists (`"[[...]]"`): safe YAML, no bracket-parsing surprises.
- Lists may be inline (`tags: [a, b]`) or block (`tags:` plus `- a` lines). Both fine.
- Frontmatter is optional; a note without it still works.

### Keys the console consumes

| Key | Effect |
|---|---|
| `title` | Display title in lists, search, tabs. Fallbacks: first `# ` heading, then filename stem. |
| `aliases` | Extra names this note answers to in wikilink resolution. List of strings. |
| `tags` | Tags for the tag index and graph. List of strings. |

### Vault convention keys (free-form, common)

`type` (journal, meeting, topic, entity, concept, recipe, ...), `date`, `related` (wikilinks to connected notes), `topic`, `source`, `confidence`, `created`, `last_reviewed`. Unknown keys are harmless.

## Wikilinks

Grammar: `[[target]]`, `[[target#Heading]]`, `[[target|Label]]`, `[[target#Heading|Label]]`.

| Example | Meaning |
|---|---|
| `[[homelab]]` | Note whose basename or alias is `homelab` |
| `[[topics/insumo/README\|Insumo]]` | Vault-root-relative path with a display label |
| `[[homelab#Network]]` | Jump to the `## Network` heading in that note |
| `[[wiki/index\|Wiki Index]]` | Path plus label |

Resolution rules:

- Case-insensitive; the `.md` extension is optional (`[[homelab]]` equals `[[homelab.md]]`).
- A bare name matches a basename or a frontmatter alias; a target containing `/` is matched as a path.
- Duplicate basenames: the shortest path wins.
- Use vault-root-relative paths or bare names. Avoid `../` relative targets; they do not resolve.
- Unresolved links stay literal text. The console builds `<vault>/.index/links.json` with backlinks, unresolved targets, orphans, and the tag map; the Links panel surfaces them for fixing.

## Tags

Two ways to tag; both feed the same index:

1. Frontmatter (preferred): `tags: [homelab, proxmox]` - bare values, no `#` prefix.
2. Inline in the body: `#homelab` - works when the `#` starts the word (preceded by whitespace or line start); letters first, then letters/digits/`-`/`_`/`/`. Code spans and fences are ignored.

Tag rules (lint-enforced in the vault): lowercase, singular, ASCII, kebab-case, no `#` prefix in frontmatter values. Reuse an existing tag before inventing one; the canonical inventory lives in the vault's `tag-taxonomy.md`.

## Note body conventions

- One `# Title` at the top, `## Sections` below.
- GFM throughout: tables, task lists (`- [ ]`), strikethrough, fenced code blocks.
- Regular hyphens only; never em or en dashes.
- Link to existing notes instead of duplicating their content.
