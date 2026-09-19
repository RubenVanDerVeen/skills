# Cheatsheet: images, width suffix, file embeds

## Images

Standard markdown image syntax; paths resolve relative to the note's own folder:

```markdown
![Alt text](.media/photo.jpg)
![Wiring](images/bench-shot.png)
```

- The console's paste/drop/paperclip upload lands files in the note folder's `.media/` directory and inserts `![alt](.media/<file>)`. Keep that path as inserted.
- Subfolders next to the note work too (`images/foo.png`).
- Absolute URLs (`https://`, `data:`, `blob:`) pass through unchanged.

## Width suffix `{N%}`

Append `{N%}` directly after the closing paren, no space, to scale an image:

```markdown
![Photo](.media/photo.jpg){40%}
![Chart](.media/results.png){37.5%}
```

- Accepts 1-3 digits with optional decimal (`{50%}`, `{37.5%}`). Valid range: greater than 0, at most 100.
- Anything else leaves the image unsized and the brace text literal - nothing breaks, the suffix just does not apply: `{150%}`, `{0%}`, `{50 %}` (space inside), `{half}`.
- The suffix also scales file embeds: `![sheet](.media/budget.xlsx){50%}`.
- PDF export honors the width.
- Write the suffix as shown; the live editor round-trips it byte-identical when it re-validates.

## File embeds (chips and viewers)

Image syntax pointing at a non-image file renders a file chip instead of a broken image:

```markdown
![Household budget](.media/budget.xlsx)
![Manual](.media/printer-manual.pdf)
```

| Extension | Renders as |
|---|---|
| `.xlsx`, `.xls` (any case) | Chip that opens the read-only sheet viewer (per-sheet tabs). |
| `.pdf` (any case) | Inline scrollable PDF viewer with a page counter; the chip stays inside as fallback. |
| Image extensions | The actual image (see above). |

- For any other file type (`.csv`, `.zip`, ...), use a normal link instead of image syntax: `[data export](.media/export.csv)`.
- Embeds are a viewer feature; they have no representation in PDF export. Do not rely on them in PDF-critical notes.

## Gotchas

- Alt text is required syntax (`![...](...)`); keep it short - it shows on hover and when the file is missing.
- A missing image file renders as broken image/chip, not as an error - check paths when a note looks wrong.
