# academic-writing-pro v2: design

Date: 2026-10-13
Status: approved for implementation
Supersedes: parts of `2026-10-02-academic-writing-pro-design.md` (non-goal 3, see below)
Input: research-agent spec (dossier at /tmp/opencode/dossier-academic-writing/), triaged by planner

## Context

The skill shipped 2026-10-02 (10 files, 387 lines) and has never been run on a real draft (dossier finding C20). Ruben's active draft (`local-ruben-draft-text.md`) already hit one concrete false negative: Typst `@key` citations are invisible to `CITE_RE`. The research spec proposed 12 architecture changes plus 9 bootstrapping changes. This design triages that spec: the skill must first run correctly and provably before it grows speculative detection with literature macro-F1 of 18-47 percent.

## Locked decisions carried from v1 (unchanged)

1. Two-layer architecture: mechanical lint + agent judgment; report only, never edit.
2. IEEE numbered default; venue styles override via parameter.
3. Writing mechanics only; PRISMA, methodology, RQ formulation, literature search stay out of scope.
4. Python 3 stdlib only; regex, no NLP libraries, no Vale binary, no LLM dependency.
5. Frontmatter contract per AGENTS.md / writing-skills; body under 500 words; no em-dashes anywhere.

## Superseded decision

v1 non-goal 3 said "no JSON output, no config file: phrase lists are edited in the script." Superseded in part: flat `vocab/accept.txt` and `vocab/reject.txt` data files (one phrase per line, `#` comments allowed) are added. Rationale: suppressing legitimate per-project phrases ("we describe" in a methodology section) cannot live in script constants. This is a data file, not a config system; no JSON, no TOML, no nested config. Everything else in non-goal 3 stands.

## Ship list

### S1. Severity, scoping, vocabulary (script)

- Replace ad-hoc severity tuples with structured `RULES = [{id, level, regex, message}, ...]`; levels: `error`, `warning`, `info` (Vale's suggestion tier; named `info` to match v1 output vocabulary and existing rule messages).
- CLI: `--min-level {error,warning,info}` (default `warning`), `--enable id,id`, `--disable id,id`.
- Level changes: `focsi-impersonal` warn to suggestion; `focsi-cautious` warn to suggestion with message pointing at `references/hedging.md`. Errors unchanged.
- Vocab: line-granular; a finding is suppressed when an `accept.txt` phrase appears anywhere on the finding's line (case-insensitive) and escalated to error when a `reject.txt` phrase appears on that line. Loaded from skill `vocab/` by default; `--vocab <dir>` overrides for per-project lists.
- `SUMMARY: <file>: N errors, M warnings, K infos` line at end of output. Exit code unchanged: 1 iff any error.

### S2. Markup-aware scope (script)

- Pre-pass that masks regions before rule matching: fenced code blocks, inline backtick code, HTML comments, URLs (`http://`, `https://`, `doi:`), LaTeX `\command{...}`, Typst `#command(...)`, Typst math `$...$`.
- `--format {plain,markdown,typst,latex}`; default auto-detect from extension (`.typ`, `.tex`, `.md`, else plain).
- `CITE_RE` gains Typst `@key` form: `\[\d+\]|\([^()]*\b\d{4}\b[^()]*\)|@[A-Za-z][A-Za-z0-9_-]+`.
- Self-test extended: Typst-citation sentence must NOT fire `citation-missing`; code block containing "don't" must NOT fire `focsi-formal`; accept.txt suppression case.

### S3. Readability summary line (script, minimal)

One info-level finding per run: median and p90 words per sentence, median words per paragraph. Guideline, never a failure. Replaces nothing; the existing 40-word sentence rule stays.

### S4. Hedging reference

`references/hedging.md`: three-way classification (hedge / non-hedge / context-dependent), examples per class, instruction that judgment pass suppresses `focsi-cautious` in math and universal-quantifier contexts and flags it only for claims about results.

### S5. Judgment-pass decomposition

`references/judgment-pass.md` (lean, ~100 lines): four roles (planner, investigator, reviewer, controller), hard caps (rationale max 2 sentences, fix max 1 sentence, any finding over 80 words gets rewritten by controller), findings advisory-only (never error), report-only reminder. Checklist includes one named advisory id `claim-overclaim` (evidence vs claim strength: suggests < demonstrates < proves) plus folded checklist bullets: framing names stakeholders, claim vs background reporting verb, discourse-role transitions, limitation hedging, well-known entity uncited (list in `references/well-known-entities.txt`).

### S6. Ruben's declared gaps (appendices)

- `references/reporting-verbs.md`: verb | claim strength | example table (16 rows shipped, extensible toward ~30). Closes the `[expand]` marker in `tone-terminology.md` (marker replaced by a pointer).
- `references/field-terminology-microfluidics.md`: starter consistency vocabulary (working principle, integration approach, pressure range, switching time, biocompatibility, pros/cons) keyed to the microfluidics literature review.

### S7. Bootstrapping text edits

- SKILL.md description rewritten: `/academic-check` early, keeps "literature review, research proposal" triggers, no em-dashes.
- Overview gets the two-pass invariant line plus a 3-command quick start block.
- Check workflow states `--against` semantics explicitly and points judgment pass at `references/judgment-pass.md`.
- References table gains the new files (load-on-demand).
- `commands/academic-check.md`: empty `$ARGUMENTS` asks for a path instead of guessing session context; `--against` passthrough; `--format` from extension.

### S8. Pressure scenarios (trimmed)

`tests/pressure-scenarios/` inside the skill folder, 4 mechanical scenarios as runnable fixtures (scenario file + EXPECTED.md: exact rule ids and severities):

1. `01-known-bad-draft`: contractions, throat-clearing, exclamation, uncited quote, long sentence. Script must report exactly the expected set, exit 1.
2. `02-typst-citation`: Typst `@key` prose; `citation-missing` must NOT fire on them; `--against` overlap still fires.
3. `03-first-person`: "we describe" in methodology context; with default accept vocab, `focsi-impersonal` must NOT fire on it.
4. `04-hedging-context`: "must" as requirement; `focsi-cautious` fires at suggestion level only, and the hedging reference classifies it non-hedge (manual judgment check).

RED evidence: scenario 02's failure already documented against Ruben's real draft (dossier C5). Scenarios double as the script's file-based regression suite; judgment scenarios (claim-overclaim) run manually against a synced skill via a fresh subagent once at close-out.

### S9. CHANGELOG

One `[Unreleased]` Changed bullet per AGENTS.md convention. Repo is unversioned (no `### Versioning` section in AGENTS.md, no version source file): no version bump.

## Explicitly deferred (with trigger)

- Tortured-phrase table (spec A4): laundering detection is not Ruben's use case; FP-prone data-entry chore. Trigger: reviewing others' submissions.
- APA and Chicago citation appendices (spec A11): speculative until a non-IEEE venue exists; keeps v1 non-goal "no style other than IEEE default". Trigger: next non-IEEE venue draft.
- `paraphrase-distance` percentage rule (spec A9): sentence-level overlap percentages need real parsing; contradicts the stdlib ceiling. Trigger: if quote-with-citation false negatives show up in practice.
- Salami publication, selective-reporting, citing-unread checks (spec A9): peer-review tasks, not own-draft checks.
- Named advisory rule ids for framing, claim-vs-background, discourse-role, limitation-statement (spec A8): folded into the judgment-pass checklist instead; rule-id proliferation on a never-run skill is YAGNI.

## Cut with rationale

- Self-plagiarism as a new rule id (spec A4/A5): `--against` mode already reports 4+ word overlap; the message gains one clause noting text recycling when the source is the author's own prior draft. No new id.
- CI gating for scenarios: personal repo, no CI. Scenarios are runnable fixtures plus one manual subagent run.

## Success criteria

1. `bin/skillctl check` passes (C1-C8) on the worktree.
2. `python3 scripts/lint-academic.py --self-test` passes, including the new Typst, masking, and vocab cases.
3. All 4 pressure scenarios match their EXPECTED files when run mechanically.
4. Running the skill end to end on a paragraph of Ruben's draft produces a merged two-pass report with no `focsi-impersonal` noise on accepted phrases and no false `citation-missing` on Typst citations.
5. SKILL.md body stays under 500 words; frontmatter under 1024 bytes; zero em-dashes in all new markdown.
