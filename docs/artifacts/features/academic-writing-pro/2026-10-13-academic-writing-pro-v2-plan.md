# Plan: academic-writing-pro v2

Date: 2026-10-13
Spec: `docs/artifacts/features/academic-writing-pro/2026-10-13-academic-writing-pro-v2-design.md`
Branch: `feat/academic-writing-pro-v2` (Conventional Branch; create from `main` before Task 1)
Versioning: AGENTS.md has no `### Versioning` section and the repo has no version source file: unversioned, no bump. CHANGELOG `[Unreleased]` bullet only (Task 6).

## Conventions every task follows

- Python 3 stdlib only. No new dependencies, no NLP libraries.
- No em-dashes (U+2014) in any file. Verify at the end with `bin/skillctl check`.
- All skill paths are relative to `skills/academic-writing-pro/`.
- Commit style: Conventional Commits 1.0.0 with trailers:

```
Co-Authored-By: zai-coding-plan/glm-5.3-flash
Agent-Role: executor
```

- The lint script's existing rule regexes must be ported verbatim from the current `scripts/lint-academic.py` into the new `RULES` structure. Do not invent replacement regexes; the self-test fixtures depend on them. Where a regex is genuinely new (Typst citation, vocab, masking), this plan gives it in full.

## File structure

| File | Action | Responsibility |
|---|---|---|
| `skills/academic-writing-pro/scripts/lint-academic.py` | rewrite in place | rule table, CLI, masking, vocab, summary, self-test |
| `skills/academic-writing-pro/vocab/accept.txt` | create | default suppressed phrases |
| `skills/academic-writing-pro/vocab/reject.txt` | create | default escalated phrases (empty starter) |
| `skills/academic-writing-pro/SKILL.md` | edit in place | description, overview invariant, quick start, workflow, references table |
| `commands/academic-check.md` | edit in place | strict argument handling |
| `skills/academic-writing-pro/references/hedging.md` | create | 3-way hedge classification |
| `skills/academic-writing-pro/references/judgment-pass.md` | create | four roles, caps, advisory checklist |
| `skills/academic-writing-pro/references/reporting-verbs.md` | create | verb | strength | example table |
| `skills/academic-writing-pro/references/field-terminology-microfluidics.md` | create | consistency vocabulary starter |
| `skills/academic-writing-pro/references/well-known-entities.txt` | create | entities that always need a citation |
| `skills/academic-writing-pro/references/tone-terminology.md` | edit in place | swap `[expand]` markers for pointers |
| `skills/academic-writing-pro/tests/pressure-scenarios/` | create | 4 runnable scenario fixtures |
| `CHANGELOG.md` | edit in place | one `[Unreleased]` bullet |

---

### Task 1: Lint script core: levels, vocab, masking, Typst citations, summary

**Files:**
- Modify: `skills/academic-writing-pro/scripts/lint-academic.py` (full restructure, keep filename)
- Create: `skills/academic-writing-pro/vocab/accept.txt`
- Create: `skills/academic-writing-pro/vocab/reject.txt`

**Depends:** none

**Interfaces:**
- Consumes: nothing.
- Produces (used by Tasks 4 and 5): CLI flags `--against SOURCE`, `--format {plain,markdown,typst,latex}` (auto-detect from `.typ`/`.tex`/`.md` extension), `--min-level {error,warning,info}` (default `warning`), `--enable id,id`, `--disable id,id`, `--vocab DIR`, `--self-test`. Rule ids unchanged: `focsi-formal`, `focsi-impersonal`, `focsi-succinct`, `focsi-cautious`, `sentence-splice`, `sentence-length`, `citation-missing`, `quote-required`; new id `readability`. `--enable`/`--disable` scope RULES-table ids only; `citation-missing` and `quote-required` are always-on context checks. Finding tuple: `(line, level, rule_id, message)` with `level in {"error", "warning", "info"}`. Last output line: `SUMMARY: <path>: N errors, M warnings, K infos`. Exit 0 iff no `error` findings. `analyze(text)` keeps working with one positional arg (self-test compat).

- [ ] **Step 1: Run the existing self-test to record the green baseline**

Run: `python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test`
Expected: `self-test OK`. If this fails before any edit, stop and report.

- [ ] **Step 2: Restructure the script**

Rewrite `scripts/lint-academic.py` to this architecture. Port each existing rule's regex string verbatim from the current file into the matching `RULES` entry (the `"regex"` lines marked PORT below). Everything else is given complete.

```python
#!/usr/bin/env python3
"""Surface linter for academic prose. Stdlib only. Reports, never edits.

Mechanical pass of the academic-writing-pro two-pass workflow. The judgment
pass (references/judgment-pass.md) covers everything contextual.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

# Lower number = more severe. --min-level filters: show level <= min.
LEVEL_RANK = {"error": 0, "warning": 1, "info": 2}

RULES = [
    # (id, level, regex, message). Port the regex from the current script
    # verbatim; only the wrapper structure below is new.
    {"id": "focsi-formal", "level": "error",
     "regex": None,  # PORT: contraction regex (word list: don't, it's, ...)
     "message": "Contraction: spell out both words."},
    {"id": "focsi-formal", "level": "error",
     "regex": None,  # PORT: exclamation mark regex
     "message": "Exclamation mark: academic prose does not use exclamations."},
    {"id": "focsi-impersonal", "level": "info",  # was warn; methodology and
     # goals phrasing is legitimate, so demote (design S1)
     "regex": None,  # PORT: first/second person regex
     "message": "First/second person: rewrite impersonally (allowed for goals, "
                "methodology steps, and section previews)."},
    {"id": "focsi-formal", "level": "warning",
     "regex": None,  # PORT: casual vocabulary regex
     "message": "Casual wording: use a formal equivalent."},
    {"id": "focsi-succinct", "level": "warning",
     "regex": None,  # PORT: throat-clearing regex
     "message": "Throat-clearing: delete or shorten."},
    {"id": "focsi-cautious", "level": "info",  # was warn; see hedging.md:
     # only some of these words are unhedged claims in context
     "regex": re.compile(
         r"\b(?:proves?|clearly|obviously|undoubtedly|always|never|must)\b", re.I),
     "message": "Possible unhedged claim: hedge or justify; see "
                "references/hedging.md (legit in math contexts)."},
    {"id": "sentence-splice", "level": "info",
     "regex": None,  # PORT: comma splice regex
     "message": "Possible comma splice: verify the clauses are independent."},
    {"id": "sentence-length", "level": "info",
     "regex": None,  # PORT: long sentence logic becomes a check function,
     # kept as a rule entry for --enable/--disable; see long_sentence() below
     "message": "Sentence over 40 words: split or restructure."},
]

# Regions the linter must never flag. Newlines are preserved so line
# numbers stay correct.
SKIP_PATTERNS = {
    "plain":    [r"https?://\S+|\bdoi:\S+"],
    "markdown": [r"```.*?```", r"`[^`\n]+`", r"<!--.*?-->",
                 r"https?://\S+|\bdoi:\S+", r"\$[^$\n]+\$"],
    "typst":    [r"```.*?```", r"`[^`\n]+`", r"//[^\n]*",
                 r"#[A-Za-z][A-Za-z0-9_-]*\([^)]*\)", r"\$[^$\n]+\$",
                 r"https?://\S+|\bdoi:\S+"],
    "latex":    [r"%[^\n]*",
                 r"\\begin\{(verbatim|lstlisting|equation|align)\*?\}.*?\\end\{\1\*?\}",
                 r"\\[A-Za-z]+\*?(\[[^\]]*\])?\{[^{}]*\}",
                 r"https?://\S+|\bdoi:\S+", r"\$[^$\n]+\$"],
}

CITE_BASE = r"\[\d+\]|\([^()]*\b\d{4}\b[^()]*\)"


def cite_re(fmt: str):
    """Citation forms per format; Typst adds @key."""
    extra = r"|@[A-Za-z][A-Za-z0-9_-]+" if fmt == "typst" else ""
    return re.compile(CITE_BASE + extra)


def mask_regions(text: str, fmt: str) -> str:
    out = text
    for pat in SKIP_PATTERNS[fmt]:
        out = re.sub(pat, lambda m: re.sub(r"[^\n]", " ", m.group(0)),
                     out, flags=re.DOTALL)
    return out


def load_vocab(directory: Path) -> tuple[list[str], list[str]]:
    def read(name: str) -> list[str]:
        p = directory / name
        if not p.exists():
            return []
        return [ln.strip().lower() for ln in
                p.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.strip().startswith("#")]
    return read("accept.txt"), read("reject.txt")
```

Then the analyze pipeline. Keep the current script's citation-missing and quote-required (`overlap_findings`) logic bodies, adapted only to receive masked text and the format-aware citation regex:

```python
def analyze(text: str, fmt: str = "plain", accept: list[str] = (),
            reject: list[str] = (), enabled: set[str] | None = None,
            disabled: set[str] | None = None) -> list[tuple]:
    """Returns (line, level, rule_id, message) tuples, sorted by line."""
    findings: list[tuple] = []
    masked = mask_regions(text, fmt)
    for rule in RULES:
        if enabled is not None and rule["id"] not in enabled:
            continue
        if disabled and rule["id"] in disabled:
            continue
        if rule["regex"] is not None:
            findings += _regex_findings(rule, masked, accept, reject)
        else:
            findings += _check_findings(rule, text, masked, fmt, accept, reject)
    if not (disabled and "readability" in disabled) and \
            (enabled is None or "readability" in enabled):
        findings += readability_finding(text)
    findings.sort(key=lambda f: f[0])
    return findings


def _regex_findings(rule, masked, accept, reject):
    out = []
    for m in rule["regex"].finditer(masked):
        # Vocab is line-granular: the matched word ("we") is judged against
        # the phrases on the line it appears in ("we describe ...").
        line_start = masked.rfind("\n", 0, m.start()) + 1
        line_end = masked.find("\n", m.end())
        ctx = masked[line_start:len(masked) if line_end < 0 else line_end].lower()
        if any(r in ctx for r in reject):
            level = "error"
        elif any(a in ctx for a in accept):
            continue  # suppressed by vocab
        else:
            level = rule["level"]
        line = masked.count("\n", 0, m.start()) + 1
        out.append((line, level, rule["id"], rule["message"]))
    return out


def _check_findings(rule, text, masked, fmt, accept, reject):
    """Context rules: sentence-length and citation-missing.
    Verbatim port of the current script's matching and window logic with
    exactly two changes: (1) every severity literal 'warn' becomes
    'warning' (a LEVEL_RANK key; the ported literal would KeyError),
    (2) citation detection runs cite_re(fmt) over masked text."""
    ...  # port from current script, applying those two changes only


def readability_finding(text: str):
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    words = sorted(len(re.findall(r"[A-Za-z0-9']+", s)) for s in sentences)
    paras = [len(re.findall(r"[A-Za-z0-9']+", p))
             for p in text.split("\n\n") if p.strip()]
    if not words:
        return []
    p90 = words[min(len(words) - 1, round(0.9 * (len(words) - 1)))]
    med = words[len(words) // 2]
    pmed = sorted(paras)[len(paras) // 2] if paras else 0
    msg = (f"Guideline only: median sentence {med} words, p90 {p90}; "
           f"median paragraph {pmed} words. High numbers: consider splitting.")
    return [(1, "info", "readability", msg)]
```

CLI and output:

```python
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--against", metavar="SOURCE")
    ap.add_argument("--format", choices=("plain", "markdown", "typst", "latex"))
    ap.add_argument("--min-level", choices=("error", "warning", "info"),
                    default="warning")
    ap.add_argument("--enable", default="", help="comma-separated rule ids (default: all)")
    ap.add_argument("--disable", default="", help="comma-separated rule ids to skip")
    ap.add_argument("--vocab", type=Path, default=SKILL_DIR / "vocab",
                    help="dir with accept.txt / reject.txt")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.file:
        ap.error("a file is required unless --self-test")
    path = Path(args.file)
    fmt = args.format or {"typ": "typst", "tex": "latex", "md": "markdown",
                          "markdown": "markdown"}.get(path.suffix.lstrip("."), "plain")
    accept, reject = load_vocab(args.vocab)
    enabled = {s for s in args.enable.split(",") if s} or None
    disabled = {s for s in args.disable.split(",") if s}
    text = path.read_text(encoding="utf-8")
    findings = analyze(text, fmt, accept, reject, enabled, disabled)
    if args.against:
        # quote-required; port from the current script, with the message
        # gaining: 'if the source is your own prior draft, this is text
        # recycling'
        findings += overlap_findings(text, Path(args.against).read_text(encoding="utf-8"))
    findings = [f for f in findings if LEVEL_RANK[f[1]] <= LEVEL_RANK[args.min_level]]
    findings.sort(key=lambda f: (f[0], LEVEL_RANK[f[1]]))
    for line, level, rule, msg in findings:
        print(f"{path}:{line}: [{level.upper()}] {rule}: {msg}")
    n_err = sum(1 for f in findings if f[1] == "error")
    n_warn = sum(1 for f in findings if f[1] == "warning")
    n_info = sum(1 for f in findings if f[1] == "info")
    print(f"SUMMARY: {path}: {n_err} errors, {n_warn} warnings, {n_info} infos")
    return 1 if n_err else 0
```

Self-test additions (keep every existing assert and fixture; append):

```python
TYPST = 'Prior work "established the baseline" @noauthor_literature_nodate.\n'
QUOTED_NOCITE = 'The "baseline result" is disputed by recent measurements.\n'
MARKUP_CLEAN = ("The `don't` token stays in code.\n\n"
                "```\ndon't panic\n```\n\nSee https://example.com/x.\n")

def self_test() -> int:
    # ... existing asserts over BAD, CLEAN, QUOTED, OVERLAP_SRC/OVERLAP_TGT,
    # with this one reworded so the always-on readability info line does
    # not count as a false positive:
    clean = [f for f in analyze(CLEAN) + analyze(QUOTED)
             if f[2] != "readability"]
    assert clean == [], f"self-test FAIL, false positives: {clean}"
    # ... then the new asserts:
    typ = analyze(TYPST, fmt="typst")
    assert not [f for f in typ if f[2] == "citation-missing"], \
        "self-test FAIL: Typst @key citation not recognized"
    assert any(f[2] == "citation-missing" for f in analyze(QUOTED_NOCITE, fmt="typst")), \
        "self-test FAIL: quoted text without a citation went unflagged"
    assert not [f for f in analyze(MARKUP_CLEAN, fmt="markdown")
                if f[2] != "readability"], \
        "self-test FAIL: markup regions produced findings"
    acc = ("we describe",)
    line = "We describe the pipeline in this section.\n"
    assert not [f for f in analyze(line, accept=list(acc))
                if f[2] == "focsi-impersonal"], "self-test FAIL: vocab accept"
    assert [f for f in analyze(line) if f[2] == "focsi-impersonal"], \
        "self-test FAIL: vocab accept suppressed too much"
    print("self-test OK")
    return 0
```

Note: `MARKUP_CLEAN` asserts that nothing except the always-on `readability` info line fires. If masking works, `focsi-formal` never sees the three `don't` occurrences inside code regions.

- [ ] **Step 3: Create vocab files**

`skills/academic-writing-pro/vocab/accept.txt`:

```
# One phrase per line. When a phrase appears on the line of a finding,
# that finding is suppressed. Line granularity is deliberate: "we" next
# to "we describe" is fine, "we" alone on a line is not. Override per
# project with --vocab DIR.
we describe
we propose
we present
we adopt
```

`skills/academic-writing-pro/vocab/reject.txt`:

```
# One phrase per line. When a phrase appears on the line of a finding,
# that finding is escalated to error. Empty by default.
```

- [ ] **Step 4: Verify**

Run: `python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test`
Expected: `self-test OK`

Run: `python3 skills/academic-writing-pro/scripts/lint-academic.py --format typst /dev/null 2>&1 | tail -1`
Expected: `SUMMARY: /dev/null: 0 errors, 0 warnings, 0 infos` (readability finding absent on empty text; command exits 0)

- [ ] **Step 5: Commit**

```bash
git add skills/academic-writing-pro/scripts/lint-academic.py skills/academic-writing-pro/vocab/
git commit -m "feat(skills): tiered levels, vocab suppression, markup-aware scanning in academic-writing-pro linter"
```

---

### Task 2: SKILL.md bootstrap edits

**Files:**
- Modify: `skills/academic-writing-pro/SKILL.md`

**Depends:** none

**Interfaces:**
- Consumes: nothing (file names referenced in the References table are fixed by this plan; Tasks 4 creates them).
- Produces: the canonical skill text Tasks 4 and 5 point at (workflow step names, references table).

- [ ] **Step 1: Rewrite SKILL.md to exactly this content**

Keep the frontmatter `name` unchanged. New `description` (no em-dash, `/academic-check` early, LR/RP triggers kept):

```
description: Use when checking or drafting academic text for soundness (FOCSI tone, sentence construction, quoting, paraphrase, citations), drafting a literature review, research proposal, or paper, or on /academic-check. IEEE numbered citations default; venue styles override.
```

Body (must stay under 500 words; this draft is ~380):

```markdown
## Overview

Two passes, always both. The lint script catches what regex can catch. Anything contextual (paragraph flow, claim strength, hedging in context, paraphrase distance) needs the judgment pass. Never pass on script output alone. Report only: findings go to the writer; edit nothing unless asked.

Quick start (paths relative to this skill's folder):

~~~bash
python3 skills/academic-writing-pro/scripts/lint-academic.py paper.tex
python3 skills/academic-writing-pro/scripts/lint-academic.py --against source.md paper.md
python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test
~~~

Pass `--against <source>` whenever a source text exists; without it the script cannot detect verbatim overlap. `--format` is auto-detected from the extension.

## When to use

Checking a draft or published text for academic soundness, or drafting one. Loads references on demand; IEEE numbered citations unless the venue says otherwise.

## Check workflow

1. **Mechanical pass.** Run the script (quick start above). Errors must be fixed; warnings verified; infos are guidelines. Add `--enable`/`--disable` and `--min-level` when the venue or section demands it.
2. **Judgment pass.** Load `references/judgment-pass.md` and run its four roles: planner, investigator, reviewer, controller. It covers FOCSI tone in context (hedging calls: `references/hedging.md`), paragraph flow, quote necessity, paraphrase distance, citation integration, terminology, and advisory claim checks (`claim-overclaim` and the checklist).
3. **Report.** One merged, severity-ranked list (error, warning, info). Each finding: rule id, location, one-sentence fix. Report only.

## Writing mode

Same references, drafting instead of checking: FOCSI tone from `references/tone-terminology.md`, paragraph model from `references/sentences-paragraphs.md`, IEEE citation placement from `references/ieee-citations.md`, reporting verbs from `references/reporting-verbs.md`, field vocabulary from `references/field-terminology-microfluidics.md` when writing microfluidics or EE text.

## References

| File | Load when |
|---|---|
| `references/quoting-plagiarism.md` | Checking quotes, paraphrases, or plagiarism risk |
| `references/tone-terminology.md` | Checking tone or terminology |
| `references/sentences-paragraphs.md` | Checking paragraph structure, flow, or sentence construction |
| `references/ieee-citations.md` | Formatting or checking citations |
| `references/hedging.md` | Deciding whether a claim needs hedging |
| `references/judgment-pass.md` | Running the judgment pass (step 2) |
| `references/reporting-verbs.md` | Picking a reporting verb by claim strength |
| `references/field-terminology-microfluidics.md` | Writing or checking microfluidics or EE text |
| `references/well-known-entities.txt` | Judgment pass: named methods that always need a citation |

## Commands

| Command | Purpose |
|---|---|
| `/academic-check` | Explicit check pass on a file or selection |

Source: `commands/academic-check.md` (top-level `commands/` directory). Dead weight inside this folder until synced to the agent's commands directory.
```

(The plan uses tilde fences so the nested block survives rendering; the real SKILL.md uses a normal triple-backtick fence.)

- [ ] **Step 2: Verify**

Run: `bin/skillctl check`
Expected: no FAIL mentioning `academic-writing-pro` (frontmatter, Overview heading, catalogs unchanged).

Run: `wc -w skills/academic-writing-pro/SKILL.md`
Expected: body under 500 words.

- [ ] **Step 3: Commit**

```bash
git add skills/academic-writing-pro/SKILL.md
git commit -m "docs(skills): bootstrap edits to academic-writing-pro (quick start, judgment-pass entry, references)"
```

---

### Task 3: Command file tightening

**Files:**
- Modify: `commands/academic-check.md`

**Depends:** none

**Interfaces:**
- Consumes: nothing.
- Produces: the `/academic-check` entry point.

- [ ] **Step 1: Replace the body with**

```markdown
---
description: Academic soundness check on a file (lint script + judgment report, no edits)
---

Load the `academic-writing-pro` skill. If `$ARGUMENTS` is empty, ask for a file path before running anything. Otherwise run its full check workflow on that file: lint script first, passing `--format` for the file's extension and `--against <source>` when the user supplied a source; then the judgment pass per `references/judgment-pass.md`. End with the script's SUMMARY line plus the number of findings the judgment pass added. Report only: do not edit the text unless the user asks.
```

- [ ] **Step 2: Verify**

Run: `bin/skillctl check`
Expected: no FAIL (C7 still satisfied: the file is referenced from SKILL.md).

- [ ] **Step 3: Commit**

```bash
git add commands/academic-check.md
git commit -m "docs(commands): strict argument handling for /academic-check"
```

---

### Task 4: References: hedging, judgment pass, reporting verbs, field terms, entities

**Files:**
- Create: `skills/academic-writing-pro/references/hedging.md`
- Create: `skills/academic-writing-pro/references/judgment-pass.md`
- Create: `skills/academic-writing-pro/references/reporting-verbs.md`
- Create: `skills/academic-writing-pro/references/field-terminology-microfluidics.md`
- Create: `skills/academic-writing-pro/references/well-known-entities.txt`
- Modify: `skills/academic-writing-pro/references/tone-terminology.md` (replace the two `[expand: ...]` markers with pointers to the new files)

**Depends:** Task 1 (consumes rule ids, level names, vocab behavior, and the `focsi-cautious` message that points here)

**Interfaces:**
- Consumes: Task 1's rule ids (`focsi-cautious`, `claim-overclaim` naming in judgment-pass.md) and `references/hedging.md` path referenced by the script message.
- Produces: reference files named in SKILL.md's References table (Task 2).

- [ ] **Step 1: Write `references/hedging.md`**

```markdown
# Hedging: three-way classification

Regex cannot tell these apart. When a `focsi-cautious` finding fires, classify the word in context:

| Class | Signals | Verdict |
|---|---|---|
| Hedge | suggest, indicate, appear to, may, might, likely, tend to, generally | Fine in a claim context; info note at most outside one |
| Non-hedge | can (ability), must (requirement), should (recommendation), cannot | Fine as-is; never flag |
| Context-dependent | proves, clearly, obviously, undoubtedly, always, never, demonstrates | Flag only when the sentence asserts a result claim; suppress in math, definitions, and universal-quantifier statements |

Examples:

- "The valve must close within 10 ms." Non-hedge (requirement). Keep.
- "This proves the model is correct." Context-dependent result claim. Suggest "These results indicate..." unless the proof is formal.
- "Always, the pressure drops." Universal quantifier in a math claim. Suppress.

Rule of thumb: hedge strength should match evidence strength. One experiment rarely proves anything; it suggests or demonstrates.
```

- [ ] **Step 2: Write `references/judgment-pass.md`**

```markdown
# Judgment pass: four roles

The lint script is pass one. This is pass two. All judgment findings are advisory (info level), never errors. You report; the writer revises. Never edit the text.

Hard caps: rationale max 2 sentences, fix max 1 sentence. Any finding longer than 80 words is rewritten before output.

## Roles

1. **Planner.** Read the full text. List suspect spans, each with a one-line category: context, quote, claim, framing, citation, terminology, structure, consistency.
2. **Investigator.** Per category, run the check below, loading the matching reference file. Name the rule id or checklist item you are applying.
3. **Reviewer.** Per finding: severity (always info), one-sentence rationale, one-sentence concrete fix.
4. **Controller.** De-duplicate overlapping findings, sort by line, merge with script output into one severity-ranked report (errors first). Enforce the caps.

## Checklist (advisory)

- `claim-overclaim`: does claim strength exceed the evidence? Scale: suggests < demonstrates < proves < proves unequivocally. Load the supporting result the text cites; judge proportionality.
- Framing: in introduction or abstract, are stakeholder, user, or application named? If an effect is claimed without who benefits, suggest naming the audience.
- Claim vs background: does the sentence assert the author's own finding, or summarize prior work? Mixed up: suggest a reporting verb plus citation (load `references/reporting-verbs.md`).
- Discourse role: does each paragraph do what its position promises (background, approach, outcome)? Flag unexpected transitions, e.g. results mid-methods.
- Limitation statements: when a paragraph ends on a limitation or future work, is it hedged properly?
- Well-known entities: a named established method (see `references/well-known-entities.txt`) with no citation gets an info note.
- Paraphrase distance: with a source available, is the paraphrase structurally too close even when quoted verbatim is avoided? Load `references/quoting-plagiarism.md`.
```

- [ ] **Step 3: Write `references/reporting-verbs.md`**

```markdown
# Reporting verbs by claim strength

Pick the verb whose strength matches the evidence. Order: evaluate < suggest < indicate < show < demonstrate < prove.

| Verb | Strength | Example |
|---|---|---|
| speculate | weakest | "We speculate that the offset stems from..." |
| hypothesize | weak | "We hypothesize that pressure governs the response." |
| propose | weak | "We propose a two-stage model." |
| suggest | weak | "Results suggest a nonlinear relation." |
| indicate | moderate | "The data indicate a shift in..." |
| reveal | moderate | "The measurements reveal a hysteresis loop." |
| find | moderate | "We find that switching time scales with..." |
| observe | moderate | "We observe bubble formation at 2 bar." |
| report | moderate | "Prior work reports efficiencies near 60 percent." |
| describe | neutral | "This section describes the setup." |
| demonstrate | strong | "Section 4 demonstrates robustness across..." |
| show | strong | "Figure 3 shows the calibration curve." |
| establish | strong | "We establish feasibility at the component level." |
| confirm | strong | "The replication confirms the earlier trend." |
| verify | strong | "We verify the model against the analytic solution." |
| prove | strongest, formal proof only | "Lemma 1 proves boundedness." |

Avoid: obviously, clearly, undoubtedly as verb substitutes; they assert instead of report.
```

- [ ] **Step 4: Write `references/field-terminology-microfluidics.md`**

```markdown
# Field terminology: microfluidics and EE (starter)

Use these terms consistently; one concept, one term, across abstract to conclusion. When the text introduces a synonym, flag it in the judgment pass.

| Concept | Preferred term | Do not mix with |
|---|---|---|
| How a part works | working principle | "functionality", "mechanism of operation" |
| How it is built into a system | integration approach | "implementation", "embedding" |
| Operating window | pressure range | "pressure regime", "pressure span" |
| Actuation delay | switching time | "response time", "latency" (reserve latency for compute) |
| Fluid-body interaction | biocompatibility | "bio-compatibility", "tissue friendly" |
| Trade-off summary | pros and cons | "advantages and disadvantages" (pick one and keep it) |

When a term is specific to the target venue (Q2 journal conventions), follow the venue over this table.
```

- [ ] **Step 5: Write `references/well-known-entities.txt`**

```
# Named entities that a sentence must cite when used. One per line.
# Judgment pass reads this; the lint script does not.
BERT
GPT
CRISPR
Levenshtein
Foucault
Kalman filter
PID controller
PCA
Monte Carlo
Navier-Stokes
PDMS
soft lithography
Lagrangian
Reynolds number
```

- [ ] **Step 6: Edit `references/tone-terminology.md`**

Replace the `[expand: ...]` marker on reporting verbs with: `See `references/reporting-verbs.md` for the full verb-by-strength table.` Replace the field-terminology `[expand: ...]` marker with: `See `references/field-terminology-microfluidics.md` for the starter vocabulary.` Keep everything else in the file byte-identical.

- [ ] **Step 7: Verify**

Run: `bin/skillctl check`
Expected: no FAIL (C1 em-dash scan included).

Run: `grep -c "expand" skills/academic-writing-pro/references/tone-terminology.md`
Expected: `0`

- [ ] **Step 8: Commit**

```bash
git add skills/academic-writing-pro/references/
git commit -m "feat(skills): judgment-pass roles, hedging taxonomy, reporting verbs, field terminology for academic-writing-pro"
```

---

### Task 5: Pressure scenarios (runnable fixtures)

**Files:**
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/01-known-bad-draft/scenario.md`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/01-known-bad-draft/EXPECTED.txt`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/02-typst-citation/scenario.typ`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/02-typst-citation/source.md`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/02-typst-citation/EXPECTED.txt`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/03-first-person/scenario.md`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/03-first-person/EXPECTED.txt`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/04-hedging-context/scenario.md`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/04-hedging-context/EXPECTED.txt`
- Create: `skills/academic-writing-pro/tests/pressure-scenarios/run.sh`

**Depends:** Task 1, Task 2 (runs the script built in Task 1; expects SKILL.md workflow to exist for the manual judgment scenario notes)

**Interfaces:**
- Consumes: the Task 1 CLI and rule ids.
- Produces: the regression suite `tests/pressure-scenarios/run.sh` (exit 0 = all mechanical scenarios match EXPECTED).

- [ ] **Step 1: Scenario 01, known-bad draft**

`01-known-bad-draft/scenario.md`:

```markdown
We don't think this is hard. In order to evaluate the approach, we take a very
long sentence that keeps going and going, stacking clause after clause after
clause, adding one more subordinate loop for good measure, until the reader has
completely lost track of what the subject even was, which is a problem for any
reviewer attempting to follow the argument that we are trying to make here
about the method and its evaluation and the results. It's great!
```

`01-known-bad-draft/EXPECTED.txt`:

```
focsi-formal
focsi-succinct
focsi-impersonal
sentence-length
readability
```

One `focsi-formal` line covers contraction and exclamation (same id; EXPECTED lists ids, not occurrences). Extraction (identical to what `run.sh` uses):

```bash
python3 ... scenario.md --min-level info | grep -oE '\[(ERROR|WARNING|INFO)\] [a-z-]+' | awk '{print $2}' | sort -u
```

Diff against `EXPECTED.txt`. Also assert exit code 1.

- [ ] **Step 2: Scenario 02, Typst citations**

`02-typst-citation/scenario.typ`:

```typst
Prior work @noauthor_literature_nodate established the baseline efficiency.
The valve "actuates in under ten milliseconds", as @valve_bench_2024 showed.
No source is given for the claim that all fluids are Newtonian.
```

`02-typst-citation/source.md` (the `--against` fixture; shares a 4+ word run with line 1 of the scenario):

```markdown
Earlier work on droplet microfluidics established the baseline efficiency for pneumatic valve actuation.
```

`02-typst-citation/EXPECTED.txt`:

```
readability
```

`citation-missing` is quote-based: it must NOT fire on lines 1 and 2 (Typst `@key` citations present) and there is no quoted text on line 3, so the plain run's only finding is `readability`. The overlap half of this scenario is asserted separately by `run.sh`: with `--against source.md`, exactly one `quote-required` fires on line 1.

- [ ] **Step 3: Scenario 03, first person with accept vocab**

`03-first-person/scenario.md`:

```markdown
We describe the pipeline in three stages. The stages are: acquisition, calibration, and evaluation.
```

`03-first-person/EXPECTED.txt`:

```
readability
```

The default accept vocab suppresses `we describe`; no other rule fires except the always-on `readability` info line.

- [ ] **Step 4: Scenario 04, hedging context**

`04-hedging-context/scenario.md`:

```markdown
The valve must close within ten milliseconds at the rated pressure.
```

`04-hedging-context/EXPECTED.txt`:

```
focsi-cautious
readability
judgment: non-hedge (requirement); do not revise
```

Mechanical assertion: `focsi-cautious` fires at INFO level only (the Task 1 regex includes `must`). The `judgment:` line is the manual expectation for the judgment pass (checked once against a synced skill via a fresh subagent at close-out, per writing-skills discipline; RED evidence for the judgment gap is the documented false-positive history of `focsi-cautious`).

- [ ] **Step 5: Write `run.sh`**

```bash
#!/usr/bin/env bash
# Regression suite for the academic-writing-pro linter.
set -euo pipefail
cd "$(dirname "$0")/../../../.."
LINT=skills/academic-writing-pro/scripts/lint-academic.py
BASE=skills/academic-writing-pro/tests/pressure-scenarios
fail=0

check() {
  local dir="$1" file="$2" fmt="$3"
  local got want
  got=$(python3 "$LINT" "$BASE/$dir/$file" --format "$fmt" --min-level info 2>/dev/null \
        | grep -oE '\[(ERROR|WARNING|INFO)\] [a-z-]+' | awk '{print $2}' | sort -u) || true
  want=$(sort -u "$BASE/$dir/EXPECTED.txt" | grep -v '^$' | grep -v '^judgment:')
  if [ "$got" != "$want" ]; then
    echo "FAIL $dir"; echo "got:"; echo "$got"; echo "want:"; echo "$want"; fail=1
  else
    echo "PASS $dir"
  fi
}

check 01-known-bad-draft scenario.md markdown
if python3 "$LINT" "$BASE/01-known-bad-draft/scenario.md" >/dev/null 2>&1; then
  echo "FAIL 01: expected exit code 1"; fail=1
fi
check 02-typst-citation scenario.typ typst
check 03-first-person scenario.md markdown
check 04-hedging-context scenario.md markdown

# 04 must be info level, never error
if python3 "$LINT" "$BASE/04-hedging-context/scenario.md" --min-level error 2>/dev/null | grep -q focsi; then
  echo "FAIL 04 fired above info"; fail=1
fi

# 02a: @key lines stay clean (no citation-missing anywhere)
n=$(python3 "$LINT" "$BASE/02-typst-citation/scenario.typ" --format typst 2>/dev/null | grep -c citation-missing || true)
if [ "$n" != "0" ]; then echo "FAIL 02: citation-missing on @key lines ($n)"; fail=1; fi
# 02b: --against overlap still fires: exactly one quote-required on line 1
q=$(python3 "$LINT" "$BASE/02-typst-citation/scenario.typ" --format typst \
    --against "$BASE/02-typst-citation/source.md" 2>/dev/null | grep -c quote-required || true)
if [ "$q" != "1" ]; then echo "FAIL 02: expected 1 quote-required, got $q"; fail=1; fi

exit $fail
```

Make it executable: `chmod +x .../run.sh`.

- [ ] **Step 6: Verify**

Run: `bash skills/academic-writing-pro/tests/pressure-scenarios/run.sh`
Expected: `PASS` on all four, exit 0. If scenario 01 diff fails on `readability` presence, recheck the extraction, not the rule.

- [ ] **Step 7: Commit**

```bash
git add skills/academic-writing-pro/tests/
git commit -m "test(skills): runnable pressure scenarios for academic-writing-pro linter"
```

---

### Task 6: CHANGELOG and close-out checks

**Files:**
- Modify: `CHANGELOG.md`

**Depends:** Task 1, Task 2, Task 3, Task 4, Task 5

**Interfaces:**
- Consumes: all shipped changes.
- Produces: the changelog record.

- [ ] **Step 1: Add one bullet under `## [Unreleased]` / `### Changed`**

(Use `### Added` for the new files if the section layout distinguishes; keep it to at most one bullet per subsection.)

```markdown
- academic-writing-pro: tiered finding levels with `--min-level`/`--enable`/`--disable`, vocab accept/reject suppression, markup-aware scanning with `--format` (Typst `@key` citations now recognized), judgment-pass roles reference, hedging taxonomy, reporting-verb and microfluidics terminology appendices, and runnable pressure scenarios under `tests/`.
```

- [ ] **Step 2: Full verification**

Run: `bin/skillctl check`
Expected: exit 0, no FAIL.

Run: `python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test && bash skills/academic-writing-pro/tests/pressure-scenarios/run.sh`
Expected: `self-test OK`, all scenarios PASS, exit 0.

Run: `bin/skillctl sync --check`
Expected: report drift (expected; user syncs deliberately). Do not run plain `sync` unless the user asked.

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog entry for academic-writing-pro v2"
```

---

## Verification matrix

| Check | Command | Gate |
|---|---|---|
| Repo conventions | `bin/skillctl check` | exit 0 |
| Script regression | `lint-academic.py --self-test` | `self-test OK` |
| Scenario regression | `tests/pressure-scenarios/run.sh` | all PASS |
| Body budget | `wc -w skills/academic-writing-pro/SKILL.md` | < 500 |
| Sync state | `bin/skillctl sync --check` | report only |

## Self-review notes

- Spec coverage: S1-S3 to Task 1, S4-S6 to Task 4, S7 to Tasks 2-3, S8 to Task 5, S9 to Task 6. Deferred items are absent by design.
- Type consistency: finding tuple `(line, level, rule_id, message)` used everywhere; levels `error|warning|info` everywhere (design records the suggestion-to-info naming).
- Parallel readiness: Tasks 1, 2, 3 have disjoint file sets and `Depends: none`. Task 4 consumes Task 1's naming; Task 5 runs Task 1's script. Task 6 is last.
