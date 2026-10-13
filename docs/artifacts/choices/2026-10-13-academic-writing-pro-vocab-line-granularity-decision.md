# academic-writing-pro vocab suppression is line-granular; flat vocab data files partially supersede v1 non-goal 3

- Date: 2026-10-13
- Status: active
- Source: `docs/artifacts/features/academic-writing-pro/2026-10-13-academic-writing-pro-v2-report.md` (spec: `docs/artifacts/features/academic-writing-pro/2026-10-13-academic-writing-pro-v2-design.md`, final semantics in its plan Task 1; implementation: `skills/academic-writing-pro/scripts/lint-academic.py` `_regex_findings`)

## Choice

Per-project vocabulary suppression in the academic-writing-pro linter is line-granular: a regex finding is suppressed when an `accept.txt` phrase appears anywhere on the line containing the finding, and escalated to error when a `reject.txt` phrase appears on that line. Not match-prefix, not whole-match. The finding's matched text alone is irrelevant; the whole line is the context.

Second, linked fact: this mechanism partially supersedes non-goal 3 of the v1 design (`2026-10-02-academic-writing-pro-design.md`, "no JSON output, no config file"). Flat `vocab/*.txt` data files (one phrase per line, `#` comments) are allowed; no JSON, no TOML, no nested config. Cross-reference: the v2 design's "Superseded decision" section records the same partial supersession.

## Why

- `focsi-impersonal` matches the single word "we". Match-prefix or whole-match semantics would let the accept entry "we describe" suppress only findings whose matched text is exactly that phrase, so every other first-person hit ("we", "our", "us") on a legitimate methodology line would still fire. Line context is what distinguishes "we describe the pipeline" (fine) from "we think" (flag).
- A line is the cheapest context unit that preserves line numbers and needs no sentence segmentation; sentence splitting already exists only in the readability path and drags in abbreviation and citation-adjacency edge cases the regex pass does not want.
- Phrase lists cannot live in script constants: legitimate per-project phrases ("we describe" in a methodology section) vary per draft, which is why flat data files replaced the v1 script-constant stance without opening the door to a config system.

## Alternatives rejected

- Match-prefix semantics (accept entry must prefix the matched text): "we describe" would never prefix the bare "we" match, so suppression would almost never fire for the rule that motivated the feature.
- Whole-match semantics (matched text must equal an accept entry): same failure, plus "we" equals no useful phrase at all.
- Sentence- or span-scoped context: more precise, but requires reliable sentence segmentation in the regex pass; deferred as the upgrade path, not the v2 baseline.

## Consequence if wrong

Known ceiling: an accept phrase also suppresses unrelated findings that share its line, for example a contraction on the same line as "we describe" goes unreported. Long typeset lines (Typst/LaTeX paragraphs on one source line) widen this blind spot: one accept phrase can silence every other finding in the whole paragraph. If this bites in practice, suppression is silently under-reporting rather than noisily over-reporting, which is the harder failure to notice.

## Revisit when

The shared-line blind spot causes a missed real error (then move to sentence- or span-scoped context, accepting the segmentation cost), or vocab files start wanting structure beyond one phrase per line (then reconsider the config-file stance, which would fully supersede v1 non-goal 3 instead of partially).
