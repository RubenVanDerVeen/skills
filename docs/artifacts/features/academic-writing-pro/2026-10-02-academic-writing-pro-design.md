# academic-writing-pro: design spec

- Date: 2026-10-02
- Status: approved design, ready for planning
- Source material: `/home/ruben/projects/Schoolwork/pre-master/p1/academic-research-skills` (UT pre-master ARS course notes; not a skill, raw content only)

## Problem

Ruben writes academic text (literature review, research proposal, Q2 paper) and needs a repeatable check for academic soundness: tone, sentence construction, quoting/citation hygiene. Second use: the agent writes academic text following the same rules. Course rules currently live in scattered lecture notes that violate this repo's conventions and are not agent-loadable.

## Decisions (locked in brainstorm)

1. **Checker shape:** skill + small lint script. Script does deterministic surface checks; agent does judgment checks.
2. **Citation style:** IEEE numbered default (matches the locked decision in `literature-review-methodology.md`), overridable per venue (Q2 paper is venue-fixed).
3. **Scope:** writing mechanics only. Tone, sentences, quoting, citation formatting, terminology. Out of scope: PRISMA/methodology, RQ formulation, literature search.
4. **Entry point:** skill + slash command `/academic-check` (checking on demand is the main use).
5. **Architecture:** lean body (~450 words) + 4 `references/` files, load-on-demand table.
6. **Script language:** Python 3, stdlib only.

## Carried constraints

- **Markdown-only repo rule vs skill scripts:** the 2026-09-29 stdctl decision keeps *general tooling* out of this repo. Scripts bundled inside a skill folder are skill content, not repo tooling; precedent is `skills/deep-research/scripts/verify-multi-lens.sh`. `bin/skillctl check` ignores extra files in skill folders; `sync` copies them recursively. The lint script must therefore be dependency-free (Python 3 stdlib only) so it works from any synced location.
- **writing-skills rules:** frontmatter `name` matches folder, kebab-case; `description` starts "Use when...", triggers only, no workflow summary; body starts `## Overview`; no em-dashes anywhere (C1); body under 500 words (frequently-loaded budget).
- **Catalog rule:** new skill needs rows in `README.md` (## Skills) and `AGENTS.md` (## Current skills) in the same commit; `bin/skillctl check` must pass; commit type `feat(skills):`.
- **Source content reformatted, never copied verbatim:** course notes use em-dashes and non-canonical heading structure.
- **Agent attribution and Conventional Commits** per `AGENTS.md` Git section.

## Components

### 1. `skills/academic-writing-pro/SKILL.md` (~450 words)

- Frontmatter: `name: academic-writing-pro`; description triggers: writing or reviewing academic text, checking academic soundness, quoting sources, academic tone, literature review / research proposal / paper text, `/academic-check`.
- Body sections: `## Overview`, `## When to use`, `## Check workflow` (main use), `## Writing mode`, `## References` (load-on-demand table), `## Commands`.
- **Check workflow (3 steps):**
  1. Run `python3 scripts/lint_academic.py <file>` (add `--against <source>` when source text available).
  2. Agent judgment pass on the full text, loading references as needed: FOCSI tone, paragraph structure (topic sentence first), old-new flow, quote necessity (sparingly), paraphrase distance, citation integration phrasing, terminology consistency.
  3. Unified report: severity-ranked findings (error / warn / info), each with the violated rule and a concrete fix. Script findings and judgment findings merged, duplicates collapsed.
- **Writing mode:** load `tone-terminology.md`, `sentences-paragraphs.md`, `quoting-plagiarism.md` before writing; IEEE citation style unless the target venue specifies otherwise; run the check workflow on the draft before declaring done.

### 2. `references/quoting-plagiarism.md`

From lecture-2 + lecture-6: quote vs paraphrase decision table (quote only when exact wording is the point, rare), the 4+-consecutive-words rule (4+ matching words = must be a quotation with citation), plagiarism criteria (word-for-word without credit, insignificant changes without credit, insufficient acknowledgement), the three acceptable citation phrasings (`Strunk (1995) asserts that "..." (p. 87)` / `Strunk (1995) asserts: "..." (p. 87)` / `Strunk's assertion (1995) that "..." (p. 87)`), minimize-quotations principle.

### 3. `references/tone-terminology.md`

From lecture-6: FOCSI table (Formal: no contractions/exclamations/casual vocab; Objective: no generalisations/emotive language; Cautious: hedging; Succinct: no redundancy; Impersonal: no you/we for general statements) with the impersonal exception (I/we allowed for goals, methodology, section previews). Hedging bank (point to -> suggest that; demonstrably -> appear to). Reporting verbs starter set (asserts, suggests, argues, found, reported). Formal vocabulary substitutions (performed properly -> without errors / to completion; positively correlated -> positively related when causation unproven). Formal-not-archaic warning (hitherto = archaic). `[expand]` markers where Ruben will add researched definitions later (full reporting-verb taxonomy, field terminology consistency rules).

### 4. `references/sentences-paragraphs.md`

From lecture-6: paragraph model (topic sentence first, body sentences, optional concluding sentence; topic sentence never mid-paragraph), readability master rule (readable once, quickly, understood immediately), SVO order (front-loaded subject burying = bad), old-new information flow at paper/paragraph/sentence level, linking-word table by function, pitfall definitions (fragment: no verb; comma splice: two independent clauses joined by comma only; run-on: no punctuation), balanced simple/complex sentence mix, reverse-outline revision procedure (extract each paragraph's topic sentence, check topic-first + flow).

### 5. `references/ieee-citations.md`

IEEE numbered style basics from the locked methodology decision: in-text `[1]` before punctuation, multiple `[1], [2]`, quote citation format, reference-list entry shape. Explicit note: style is a parameter; follow the target venue when one is specified; IEEE is the default for course LR/RP work.

### 6. `scripts/lint_academic.py` (Python 3, stdlib only)

Deterministic checks only, each reported as `<path>:<line>: [error|warn|info] <rule>: <message>`:

| Check | Severity | Rule |
|---|---|---|
| Contractions (don't, can't, it's, ...) | error | focsi-formal |
| Exclamation marks in prose | error | focsi-formal |
| First/second person (I, we, you, our, us, my) outside methodology/preview context | warn | focsi-impersonal (message notes the exception) |
| Casual vocabulary list (a lot of, stuff, kind of, really, big, get, ...) | warn | focsi-formal |
| Throat-clearing / redundancy phrases (it is important to note that, in order to, due to the fact that, ...) | warn | focsi-succinct |
| Unhedged strong claims (proves, clearly, obviously, always, never, undoubtedly) | warn | focsi-cautious |
| Comma-splice heuristic (comma followed by this/it/they/these/those/however/therefore + verb) | info | sentence-splice |
| Sentence over 40 words | info | sentence-length |
| Quoted text (double quotes) with no citation marker ([N] or (Author, year)) within ~120 chars after | warn | citation-missing |
| `--against <source>`: 4+-word verbatim overlap not inside quotes | error | quote-required |

- Exit code 1 when any error, else 0. Findings sorted by line number.
- `--self-test`: embedded fixture with known violations; asserts expected rule ids are found; exit 0/1. Ships with the skill so any machine can verify it.
- No JSON/machine output (YAGNI). Lists kept small and editable at top of file.
- Known ceiling (documented in `--help` and SKILL.md): regex heuristics catch obvious cases only; fragments, splices, and tone need the agent judgment pass. Marked with a `# ponytail:` comment.

### 7. `commands/academic-check.md`

Frontmatter `description` (one line: explicit academic soundness check of a file or selection). Body: load the `academic-writing-pro` skill, run the check workflow on `$ARGUMENTS` (file path or selection; current file when omitted). Follows `commands/standardize.md` format pattern.

### 8. Catalog updates (same commit)

- `README.md` ## Skills table row (alphabetical).
- `AGENTS.md` ## Current skills table row (alphabetical).
- `opencode-install.md`: no change (verify section does not list skills by name).

## Non-goals

- No methodology/PRISMA/RQ checks (stays in course notes).
- No natural-language parsing (spacy etc.): stdlib regex only.
- No JSON output, no config file: phrase lists are edited in the script.
- No style other than IEEE default; venue styles are followed ad hoc via the parameter note.
- No `.bib`/Zotero/Typst integration: typst-pro already owns Typst rendering.

## Verification

1. `bin/skillctl check` passes (C1-C7).
2. `python3 skills/academic-writing-pro/scripts/lint_academic.py --self-test` exits 0.
3. Fixture check: a sample text with known violations (contraction, exclamation, "we", throat-clearing, long sentence, uncited quote) produces the expected rule ids; a clean academic paragraph produces no errors.
4. `--against` mode: source pair with 4+-word overlap flags `quote-required`.
5. `/academic-check` frontmatter parses; body references the skill correctly.
6. Catalog rows present in README.md + AGENTS.md; skill folders sync cleanly (`bin/skillctl sync --check` shows no MISSING for the new skill).

## Open items (Ruben will research; skill ships with `[expand]` markers)

1. Full reporting-verb taxonomy for `tone-terminology.md`.
2. Field-terminology consistency rules (microfluidics/EE vocabulary).
3. Optional: hedging-strength scale (must/may/might gradient) if course rubric demands it.
