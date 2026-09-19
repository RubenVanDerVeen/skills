# Cheatsheet: columns fence

Side-by-side layout. A `columns` fence wraps N parts; every part is parsed as markdown.

````markdown
```columns
## Left

Regular markdown here: **bold**, [[wikilinks]], math like $x^2$,
images with widths: ![photo](.media/p.jpg){40%}
||
## Right

Second column. Lists, tables and links all work per column.
```
````

## Rules

- The separator is a line containing exactly `||` (trailing spaces/tabs allowed). Not `|^|`, not `| |`, not `|||`.
- No `||` in the fence: the whole body renders as a single column (graceful, nothing lost).
- More than one `||` gives more parts. Parts flow into a 2-across grid on desktop and stack to one column on phones. Two or four parts make tidy layouts; three leaves an odd cell.
- Each part is fully parsed markdown: wikilinks, sized images, math, citations, emphasis, lists, tables.

## Limits

- **No nested triple-backtick fences.** The first inner ``` line terminates the columns fence, so a ` ```mermaid `, ` ```plot `, ` ```columns ` or code fence inside a part breaks the layout. Put fences below the columns block.
- A lone `||` is reserved as separator; do not use it as visible text inside a column.
- Column widths are equal by layout; the `{N%}` suffix only sizes images, not columns.
