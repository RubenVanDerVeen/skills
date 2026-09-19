---
name: note-syntax
description: Use when writing or editing notes in the Hermes Console notes vault (Nextcloud 06_notes) - note YAML frontmatter, wikilinks, images and the {N%} width suffix, columns fences, plot fences, mermaid diagrams, KaTeX math, or file embeds. Triggers write/edit/format/scaffold a note, journal, meeting note, recipe, wiki page, console markdown syntax.
---

## Overview

Hermes Console notes are GitHub-flavored Markdown with YAML frontmatter plus a small set of console-specific constructs. Everything documented here renders in the console's notes viewer, live editor, chat transcripts, and (mostly) PDF export. This SKILL.md covers day-to-day writing; `cheatsheets/` holds exact grammar, edge cases, and copy-paste examples.

## Anatomy of a note

Frontmatter, then one `# Title`, then the body:

```markdown
---
title: NS to Blauwnet transfer
date: 2026-09-13
type: journal
tags:
  - train
related: []
---

# NS to Blauwnet transfer

Body text with [[wikilinks]], images, tables, task lists.
```

Keys the console consumes: `title` (display title; falls back to the first `# ` heading, then the filename), `aliases` (extra wikilink targets), `tags` (list; lowercase kebab-case). Vault conventions often add `date`, `type`, `related`, `topic`.

House style: kebab-case ASCII paths, ISO 8601 dates, regular hyphens only (never em or en dashes), English structural paths, Dutch content where needed. Cross-link with wikilinks, do not duplicate.

## Quick reference

| I want to... | Write |
|---|---|
| Link a note | `[[target]]`, `[[target#Heading]]`, `[[target\|Label]]` |
| Embed an image | `![alt](.media/photo.jpg)` |
| Resize an image | `![alt](.media/photo.jpg){40%}` |
| Embed a PDF or spreadsheet | `![label](.media/budget.pdf)` |
| Two-column layout | ` ```columns ` fence, columns split on a lone `\|\|` line |
| Diagram | ` ```mermaid ` fence |
| Interactive function plot | ` ```plot ` fence with function-plot JSON |
| Inline math | `$E = mc^2$` |
| Block math | `$$` fence on its own lines |

## Cheatsheets

| File | Contents |
|---|---|
| `cheatsheets/frontmatter-and-links.md` | Frontmatter keys, wikilink grammar and resolution, aliases, tags |
| `cheatsheets/images-and-files.md` | Image paths and `.media/`, width suffix rules, PDF/xlsx file embeds |
| `cheatsheets/columns.md` | The columns fence, the `||` separator, nesting limits |
| `cheatsheets/plots.md` | Plot fence JSON: axes, curves, points, colors, interaction |
| `cheatsheets/mermaid.md` | Mermaid fences, diagram quick reference, theme and PDF behavior |
| `cheatsheets/math-and-misc.md` | Inline math guards, block math, citations, PDF export parity |

Read the relevant cheatsheet before writing non-trivial markup; they are short.

## Common mistakes

- `{150%}`, `{0%}`, `{50 %}` do not resize: the image renders unsized and the brace text stays literal. Only `0 < pct <= 100` (decimals allowed) applies.
- The columns separator is a line containing exactly `||` - not `|^|`, not `| |`.
- Fences cannot nest: a ` ```mermaid ` or ` ```plot ` block inside ` ```columns ` terminates the columns fence.
- `$100$` stays literal currency text by design (pure amounts never become math). Escape a literal dollar with `\$`.
- Raw HTML is stripped by the sanitizer; use markdown constructs only.
- Lowercase fence names (`mermaid`, `plot`, `columns`) - the live editor round-trip is case-sensitive on them.
