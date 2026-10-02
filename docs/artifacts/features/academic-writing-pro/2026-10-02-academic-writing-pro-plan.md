# academic-writing-pro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `academic-writing-pro` skill: a two-layer academic soundness checker (lint script + agent judgment pass) that also drafts academic text.

**Architecture:** Lean SKILL.md (~450 words) with the check workflow and writing mode; 4 load-on-demand reference files carry the rule banks; a stdlib-only Python lint script does deterministic surface checks; `/academic-check` command is the explicit entry point; catalog rows land in the same commit as the SKILL.md (repo pre-commit hook P6 requires this).

**Tech Stack:** Markdown (skill content), Python 3 stdlib only (script), bash for verification.

**Spec:** `docs/artifacts/features/academic-writing-pro/2026-10-02-academic-writing-pro-design.md`

**Versioning:** Unversioned, no bump. `AGENTS.md` declares no canonical version source.

## Global Constraints

- Branch: `feat/academic-writing-pro` off `main`. Create once in Task 1; all tasks commit to it.
- No em-dashes (U+2014) in any file. `bin/skillctl check` rule C1 must pass at every commit.
- Python: standard library only. No third-party imports.
- SKILL.md body under 500 words. Frontmatter: `name` matches folder, `description` starts "Use when..." and lists triggers only. No `## Skill` heading; body starts `## Overview`.
- Commit messages: Conventional Commits, type `feat(skills):`. Do NOT hardcode attribution trailers in this plan's messages; the executing agent appends its own true trailers per `STANDARDS.md` (its actual provider/model slug plus `Agent-Role: <role>`).
- New skill, its command file, and its catalog rows ship in ONE commit (AGENTS.md bundle rule, enforced by pre-commit hook P6): Task 3.
- Script output format (consumed by SKILL.md text): `<path>:<line>: [<error|warn|info>] <rule-id>: <message>`, sorted by line then rule. Exit 1 iff any `error` finding, else 0.
- Rule ids (stable contract, referenced by self-test and SKILL.md): `focsi-formal`, `focsi-impersonal`, `focsi-cautious`, `focsi-succinct`, `sentence-splice`, `sentence-length`, `citation-missing`, `quote-required`.

---

### Task 1: Lint script with self-test

**Files:**
- Create: `skills/academic-writing-pro/scripts/lint_academic.py`

**Depends:** none

**Interfaces:**
- Consumes: nothing (standalone).
- Produces: CLI `python3 skills/academic-writing-pro/scripts/lint_academic.py <file> [--against <source-file>] [--self-test]`. `analyze(text) -> list[tuple[int, str, str, str]]` returning `(line, severity, rule_id, message)`; `self_test() -> int` (0 pass, 1 fail); `overlap_findings(text, source) -> list[tuple[int, str, str, str]]`. Rule ids and exit codes per Global Constraints.

- [ ] **Step 1: Create branch**

```bash
git checkout main && git pull --ff-only && git checkout -b feat/academic-writing-pro
```

- [ ] **Step 2: Create the complete script**

Create `skills/academic-writing-pro/scripts/lint_academic.py` with exactly:

```python
#!/usr/bin/env python3
"""Deterministic surface checks for academic writing tone and citation hygiene.

Part of the academic-writing-pro skill. Regex heuristics catch obvious
violations only; tone, paragraph flow, quote necessity, and paraphrase
distance need the agent judgment pass described in SKILL.md.
# ponytail: regex heuristics; real parsing only if false positives hurt
"""

from __future__ import annotations

import argparse
import re
import sys

RULES = [
    ("focsi-formal", "error", re.compile(
        r"\b(?:don't|doesn't|didn't|can't|won't|wouldn't|couldn't|shouldn't|"
        r"isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|it's|that's|"
        r"there's|they're|we're|we've|you're|you've|i'm|i've|let's|ain't)\b",
        re.IGNORECASE),
     "Contraction: spell out both words."),
    ("focsi-formal", "error", re.compile(r"!"),
     "Exclamation mark: academic prose does not use exclamations."),
    ("focsi-impersonal", "warn", re.compile(
        r"\b(?:[Ii]|[Ww]e|[Oo]ur|[Uu]s|[Mm]y|[Yy]ou|[Yy]our)\b"),
     "First/second person: rewrite impersonally (allowed for goals, "
     "methodology steps, and section previews)."),
    ("focsi-formal", "warn", re.compile(
        r"\b(?:a lot of|lots of|stuff|kind of|sort of|really|pretty much|"
        r"huge|okay)\b", re.IGNORECASE),
     "Casual vocabulary: use a formal equivalent."),
    ("focsi-succinct", "warn", re.compile(
        r"\b(?:it is important to note that|it should be noted that|"
        r"in order to|due to the fact that|for the purpose of|"
        r"in the event that|the fact that)\b", re.IGNORECASE),
     "Throat-clearing: delete or shorten."),
    ("focsi-cautious", "warn", re.compile(
        r"\b(?:proves?|clearly|obviously|undoubtedly|always|never)\b",
        re.IGNORECASE),
     "Unhedged strong claim: hedge or justify (legit in math contexts)."),
    ("sentence-splice", "info", re.compile(
        r",\s+(?:this|these|those|it|they|however|therefore|moreover|"
        r"furthermore)\b", re.IGNORECASE),
     "Possible comma splice: verify the clauses are independent."),
]

SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
QUOTE_RE = re.compile(r'["\u201c]([^"\u201d]{2,})["\u201d]')
CITE_RE = re.compile(r"\[\d+\]|\([^()]*\b\d{4}\b[^()]*\)")
TOKEN_RE = re.compile(r"[A-Za-z0-9']+")


def analyze(text: str) -> list[tuple[int, str, str, str]]:
    findings: list[tuple[int, str, str, str]] = []
    lines = text.split("\n")
    for rule_id, severity, regex, message in RULES:
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                findings.append((i, severity, rule_id, message))
    for m in SENTENCE_RE.finditer(text):
        if len(m.group().split()) > 40:
            line = text.count("\n", 0, m.start()) + 1
            findings.append((line, "info", "sentence-length",
                             "Sentence over 40 words: split or restructure."))
    for m in QUOTE_RE.finditer(text):
        window = text[m.end():m.end() + 120]
        if not CITE_RE.search(window):
            line = text.count("\n", 0, m.start()) + 1
            findings.append((line, "warn", "citation-missing",
                             "Quoted text without a nearby citation "
                             "([n] or (Author, year))."))
    return sorted(findings, key=lambda f: (f[0], f[2]))


def overlap_findings(text: str, source: str) -> list[tuple[int, str, str, str]]:
    def tokens(s: str):
        return [(m.group().lower(), m.start(), m.end())
                for m in TOKEN_RE.finditer(s)]

    src_grams = {" ".join(t[0] for t in tokens(source)[i:i + 4])
                 for i in range(len(tokens(source)) - 3)}
    if not src_grams:
        return []
    tk = tokens(text)
    quote_spans = [(m.start(), m.end()) for m in QUOTE_RE.finditer(text)]
    hits = []
    for i in range(len(tk) - 3):
        gram = " ".join(tk[i + j][0] for j in range(4))
        if gram not in src_grams:
            continue
        start, end = tk[i][1], tk[i + 3][2]
        if any(s <= start and end <= q for s, q in quote_spans):
            continue
        hits.append((start, end))
    hits.sort()
    merged: list[list[int]] = []
    for start, end in hits:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    findings = []
    for start, end in merged:
        line = text.count("\n", 0, start) + 1
        phrase = text[start:end]
        findings.append((line, "error", "quote-required",
                         f"4+ consecutive words match the source: '{phrase}'. "
                         "Quote and cite, or paraphrase."))
    return findings


BAD = (
    "We don't observe this effect.\n"
    'It is important to note that the system shows "stable flow"\n'
    "in a lot of cases!\n"
    "The pump failed, this caused delays.\n"
    "The measurement setup for every experiment described in this section "
    "consisted of a syringe pump, a pressure sensor, a microfluidic chip "
    "with three integrated valves, a custom control board, a data "
    "acquisition unit, and a laptop computer, and every component was "
    "calibrated against a reference instrument before each measurement "
    "series was started.\n"
)
CLEAN = (
    "Previous studies suggest that valve geometry affects flow stability "
    "(Jansen, 2021).\n"
    "The results indicate a small pressure dependence [3].\n"
)
QUOTED = (
    'As noted earlier, "flow remains stable" (Jansen, 2021) under all '
    "tested conditions.\n"
)
OVERLAP_SRC = "Electronically actuated microfluidic valves for lab on chip systems"
OVERLAP_TGT = (
    "The design of electronically actuated microfluidic valves for lab on "
    "chip systems is reviewed."
)


def self_test() -> int:
    expected = {
        "focsi-formal", "focsi-impersonal", "focsi-succinct",
        "citation-missing", "sentence-splice", "sentence-length",
    }
    bad = {rule for _, _, rule, _ in analyze(BAD)}
    missing = expected - bad
    assert not missing, f"self-test FAIL, rules not detected: {sorted(missing)}"
    clean = analyze(CLEAN) + analyze(QUOTED)
    assert clean == [], f"self-test FAIL, false positives: {clean}"
    src_rules = {rule for _, _, rule, _ in analyze(OVERLAP_TGT)}
    assert "quote-required" not in src_rules, "quote-required without --against"
    ovl = overlap_findings(OVERLAP_TGT, OVERLAP_SRC)
    assert any(r == "quote-required" for _, _, r, _ in ovl), \
        f"self-test FAIL, overlap not detected: {ovl}"
    print("self-test OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Academic writing surface linter. Regex heuristics catch "
        "obvious cases only; tone, flow, and quote necessity need the "
        "judgment pass (see SKILL.md).")
    p.add_argument("file", nargs="?", help="text or markdown file to check")
    p.add_argument("--against", help="source file for 4+ word overlap check")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not a.file:
        p.error("a file is required unless --self-test")
    text = open(a.file, encoding="utf-8").read()
    findings = analyze(text)
    if a.against:
        findings.extend(overlap_findings(
            text, open(a.against, encoding="utf-8").read()))
        findings.sort(key=lambda f: (f[0], f[2]))
    for line, severity, rule_id, message in findings:
        print(f"{a.file}:{line}: [{severity}] {rule_id}: {message}")
    return 1 if any(s == "error" for _, s, _, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Run the self-test**

Run: `python3 skills/academic-writing-pro/scripts/lint_academic.py --self-test`
Expected: `self-test OK`, exit 0.

- [ ] **Step 4: Fixture check on a real file**

```bash
printf 'We don'\''t really know. It is important to note that the device "works well" under load!\n' > /tmp/opencode/acad-fixture.txt
python3 skills/academic-writing-pro/scripts/lint_academic.py /tmp/opencode/acad-fixture.txt; echo "exit=$?"
```
Expected output includes `focsi-formal`, `focsi-impersonal`, `focsi-succinct`, `citation-missing` lines and `exit=1`.

- [ ] **Step 5: Commit**

```bash
git add skills/academic-writing-pro/scripts/lint_academic.py
git commit -m "feat(skills): add academic-writing-pro lint script

Deterministic surface checks (FOCSI, splices, citations, 4-word overlap)
with embedded self-test. Judgment checks stay in the skill body."
```

---

### Task 2: Reference files (all four)

**Files:**
- Create: `skills/academic-writing-pro/references/quoting-plagiarism.md`
- Create: `skills/academic-writing-pro/references/tone-terminology.md`
- Create: `skills/academic-writing-pro/references/sentences-paragraphs.md`
- Create: `skills/academic-writing-pro/references/ieee-citations.md`

**Depends:** Task 1 (branch `feat/academic-writing-pro` must exist before Task 2 commits)

**Interfaces:**
- Consumes: nothing.
- Produces: the four reference files at exactly these paths; SKILL.md (Task 3) cites them verbatim in its References table.

- [ ] **Step 1: Write `references/quoting-plagiarism.md`**

Create with exactly:

````markdown
# Quoting and plagiarism

Source: ARS course, lecture 2 (Leedy & Ormrod 2016) and lecture 6 writing workshop; reformatted for this skill.

## Quote or paraphrase

| Form | Example | When |
|---|---|---|
| Direct quote | Strunk (1995) asserts that "Too many programmes are already underfinanced" (p. 87). | Only when the exact wording is the point. Rare. |
| Paraphrase | Most forefoot problems in women are caused by footwear that does not match the shape of the foot (Frey et al., 1993). | Default: own wording, credit the source. |

## The 4-word rule

Four or more consecutive words matching the source text must be a quotation: put them in quotes with a citation, or reword. Paraphrasing too close to the original is still plagiarism even with a citation.

## What counts as plagiarism

- Presenting another person's work as your own.
- Word-for-word reproduction without credit.
- Insignificant changes without credit (swapping a few words while keeping the structure).
- Insufficient acknowledgement or identification of sources.

## Acceptable citation phrasings for direct quotes

1. Author (year) asserts that "..." (p. 87).
2. Author (year) asserts: "..." (p. 87).
3. The author's assertion (year) that "..." is based on questionable assumptions.

The reporting verb is paraphrasable: asserts, argues, claims, notes, found. Pick the verb that matches the source's actual strength.

## Principles

- Give credit where credit is due.
- Minimize quotations; paraphrasing is the preferred choice.
- Summarize in your own words.
- Every quote and every paraphrase carries a citation.
- A first draft is not the last draft: re-check quote/paraphrase balance on revision.
````

- [ ] **Step 2: Write `references/tone-terminology.md`**

Create with exactly:

````markdown
# Tone (FOCSI) and terminology

Source: ARS course, lecture 6 academic writing workshop; reformatted for this skill.

## FOCSI

| Letter | Rule | Means |
|---|---|---|
| F | Formal | No contractions, no exclamation marks, no casual or colloquial vocabulary. |
| O | Objective | No generalizations, no personal bias, no emotive language. |
| C | Cautious | Hedge claims; avoid proving language. |
| S | Succinct | No redundancy, no throat-clearing. |
| I | Impersonal | No "you/we" for general statements; no "I/we" for opinions. |

Impersonal exception: use I/we freely for goals, methodology steps, and section previews ("In this section, we describe...").

## Hedging

| Unhedged | Hedged |
|---|---|
| These results point to the indispensability of X. | These findings suggest that X is necessary for Y. |
| The data proves the model. | The data indicate that the model holds under these conditions. |

Hedge verbs and phrases: suggest, indicate, appear to, tend to, point to, are consistent with, may, likely.
Avoid: proves, clearly, obviously, undoubtedly, always, never (outside mathematics).

## Reporting verbs (starter set)

asserts, argues, claims, notes, reports, found, observed, suggested, demonstrated, proposed.

Match the verb to the source's actual strength: "demonstrated" claims more than "suggested".

[expand: full reporting-verb taxonomy, pending Ruben's research.]

## Vocabulary precision

- Vague: "The task was performed properly." Precise: "...before the deadline", "...without errors", "...to completion".
- "positively correlated" implies causation; write "positively related" unless causation is established.
- Formal is not archaic: avoid "hitherto", "heretofore", "aforementioned".

## Throat-clearing to delete

"it is important to note that", "it should be noted that", "in order to" (write "to"), "due to the fact that" (write "because"), "the fact that".

[expand: field terminology consistency rules for microfluidics/EE vocabulary, pending Ruben's research.]
````

- [ ] **Step 3: Write `references/sentences-paragraphs.md`**

Create with exactly:

````markdown
# Sentences and paragraphs

Source: ARS course, lecture 6 academic writing workshop; reformatted for this skill.

## Readability master rule (Wallwork 2023)

Readers prefer text they can read once, read quickly, and understand immediately. If the interpretation only becomes clear at the end of the sentence or paragraph, rewrite.

## Paragraph model

1. Topic sentence: presents the main idea. Always first, never mid-paragraph.
2. Body sentences: develop and explain, present details, examples, arguments.
3. Concluding sentence (optional): summarizes or bridges to the next paragraph.

## Flow: old before new

Old information first, new information last, applied at paper, paragraph, and sentence level. Each sentence links back to the previous one.

| Function | Linking words |
|---|---|
| Listing | first, second, furthermore, moreover, finally |
| Reinforcement | also, in addition, similarly, likewise |
| Examples | for example, for instance, namely |
| Results | therefore, consequently, as a result, thus |
| Highlighting | in particular, notably, especially |

## Word order

Standard SVO: subject, verb, object. Do not bury the subject behind front-loaded modifiers; the reader should hit the subject early.

## Pitfalls

| Pitfall | Definition |
|---|---|
| Fragment | No verb; not a complete sentence. |
| Comma splice | Two independent clauses joined by a comma only. |
| Run-on | Two independent clauses with no punctuation between them. |

Use a balanced mix of simple and complex sentences; all-complex and all-simple both read badly.

## Revision: reverse outline

1. Extract one line per paragraph: its topic sentence.
2. Check each paragraph: topic sentence first? Old-new flow followed? Linking words present where ideas connect?
````

- [ ] **Step 4: Write `references/ieee-citations.md`**

Create with exactly:

````markdown
# IEEE citations (default style)

Source: locked course decision (IEEE Editorial Style Manual, ch. 5); reformatted for this skill.

## In-text

- Number sources in order of first citation: [1], [2], [3].
- Place the number before sentence punctuation: "...as shown in [1]."
- Multiple sources: [1], [2] or a range of three or more: [1]-[3].
- Every cited source appears in the reference list exactly once, and every reference list entry is cited in the text.

## Direct quotes

Use the bracket with page: Strunk states that "..." [1, p. 87].

## Reference list

- Heading "References"; entries in first-citation order, numbered.
- Author initials first: A. Author, B. Author.
- Journal article shape: [1] A. Author, "Title of paper," Journal Name, vol. x, no. y, pp. zz-zz, Year.
- When in doubt, consult the IEEE Editorial Style Manual; do not guess entry shapes.

## Style is a parameter

IEEE is the default (course literature review and research proposal). When a target venue fixes a citation style (Q2 paper), follow the venue style instead and apply the quoting rules from `quoting-plagiarism.md` unchanged.
````

- [ ] **Step 5: Stage, verify, then commit**

```bash
git add skills/academic-writing-pro/references/
bin/skillctl check
git commit -m "feat(skills): add academic-writing-pro references

Quoting/plagiarism, FOCSI tone and terminology, sentence construction,
IEEE citations. Rule banks from the ARS course notes."
```

Expected: `bin/skillctl check` reports PASS on C1 with the staged reference files included (staging first puts them in the index that C1 scans); no C6 impact (SKILL.md absent, folder skipped).

---

### Task 3: SKILL.md, command, catalog rows (one commit)

**Files:**
- Create: `skills/academic-writing-pro/SKILL.md`
- Create: `commands/academic-check.md`
- Modify: `README.md` (## Skills table, insert as the first data row, above `drawio-pro`)
- Modify: `AGENTS.md` (## Current skills table, insert as the first data row, above `altium-pro`)

**Depends:** Task 1 (Step 3 verifies the script CLI the SKILL.md cites), Task 2 (references must exist for the References table to be truthful)

**Interfaces:**
- Consumes: script CLI and rule ids from Task 1; reference file paths from Task 2.
- Produces: the complete, cataloged skill; skill name `academic-writing-pro` and command `/academic-check` become the public interface.

- [ ] **Step 1: Write SKILL.md**

Create `skills/academic-writing-pro/SKILL.md` with exactly:

````markdown
---
name: academic-writing-pro
description: Use when writing or reviewing academic text for academic soundness: checking tone, sentence construction, quoting, paraphrasing, or citations, drafting a literature review, research proposal, or paper, deciding quote vs paraphrase, or on /academic-check.
---

## Overview

Two-mode skill. Check mode is the main use: review written academic text on two layers, a mechanical lint script plus an agent judgment pass, and report severity-ranked findings. Write mode drafts academic text under the same rules. Citation style defaults to IEEE numbered; venue styles override.

## When to use

- Check a draft (literature review, research proposal, paper section) for academic soundness.
- Check quoting and paraphrasing against source texts.
- Draft academic text in any of those document types.

## Check workflow

1. **Mechanical pass.** Run `python3 scripts/lint_academic.py <file>` (paths relative to this skill's folder; add `--against <source-file>` when the source text is available). Errors must be fixed; warns must be verified.
2. **Judgment pass.** Read the full text yourself and check what regex cannot: FOCSI tone, paragraph structure (topic sentence first), old-new flow, quote necessity (sparingly, 4-word rule), paraphrase distance, citation integration phrasing, terminology consistency. Load references as needed.
3. **Report.** Merge both passes into one severity-ranked list (error, warn, info). Each finding names the violated rule, the location, and a concrete fix. Report only: do not edit unless asked.

Never pass a text on script output alone; the script catches obvious surface violations, the judgment pass catches everything contextual.

## Writing mode

Load `tone-terminology.md`, `sentences-paragraphs.md`, and `quoting-plagiarism.md` before drafting, plus `ieee-citations.md` unless the venue fixes another style. Run the check workflow on the draft before declaring the task done.

## References

| File | Load when |
|---|---|
| `references/quoting-plagiarism.md` | Checking quotes, paraphrases, or plagiarism risk |
| `references/tone-terminology.md` | Checking tone, hedging, or terminology |
| `references/sentences-paragraphs.md` | Checking paragraph structure, flow, or sentence construction |
| `references/ieee-citations.md` | Formatting or checking citations |

## Commands

| Command | Purpose |
|---|---|
| `/academic-check` | Explicit check pass on a file or selection |

Source: `commands/academic-check.md` (top-level `commands/` directory). Dead weight inside this folder until synced to the agent's commands directory.
````

- [ ] **Step 2: Write the command file**

Create `commands/academic-check.md` with exactly:

````markdown
---
description: Academic soundness check on a file or selection (lint script + judgment report, no edits)
---

Load the `academic-writing-pro` skill and run its full check workflow on `$ARGUMENTS`. `$ARGUMENTS` is a file path; when omitted, check the file or selection from the current session context. Produce the unified severity-ranked report (errors, warns, infos, each with rule and concrete fix). Report only: do not edit the text unless the user asks for fixes.
````

- [ ] **Step 3: Insert README row**

In `README.md`, insert this line as the first data row of the `## Skills` table, directly below the `|---|---|` separator (joining the pro-family cluster at the top):

```markdown
| [`academic-writing-pro`](./skills/academic-writing-pro/SKILL.md) | Academic writing checks and drafting. FOCSI tone, sentence construction, quoting and plagiarism rules, IEEE citations, lint script. Slash command: `/academic-check`. |
```

- [ ] **Step 4: Insert AGENTS.md row**

In `AGENTS.md`, insert this line as the first data row of the `## Current skills` table, directly below its table separator:

```markdown
| `skills/academic-writing-pro/` | `academic-writing-pro` | Academic writing checks and drafting. FOCSI tone, sentence construction, quoting and plagiarism rules, IEEE citations, lint script. Slash command: `/academic-check`. |
```

- [ ] **Step 5: Full check**

Run: `bin/skillctl check`
Expected: PASS with zero findings (C1-C8). C6 passes because the catalog rows are staged in this same task; C7 passes because the SKILL.md Commands section names `commands/academic-check.md`, created in Step 2.

- [ ] **Step 6: Commit (single bundle commit)**

```bash
git add skills/academic-writing-pro/SKILL.md commands/academic-check.md README.md AGENTS.md
git commit -m "feat(skills): add academic-writing-pro skill, command, catalogs

Two-mode academic writing skill: lint + judgment check workflow, writing
mode, four references, /academic-check command, README/AGENTS rows."
```

---

### Task 4: End-to-end verification and sync smoke test

**Files:**
- none (read-only verification)

**Depends:** Task 1, Task 2, Task 3

**Interfaces:**
- Consumes: the completed, committed skill from Tasks 1-3.
- Produces: verification evidence for the final report.

- [ ] **Step 1: Full check on the committed tree**

Run: `bin/skillctl check`
Expected: PASS with zero findings (C1-C8).

- [ ] **Step 2: Script self-test on the committed tree**

Run: `python3 skills/academic-writing-pro/scripts/lint_academic.py --self-test`
Expected: `self-test OK`, exit 0.

- [ ] **Step 3: Sync smoke test**

Run: `bin/skillctl sync && bin/skillctl sync --check | grep academic-writing-pro || echo "new skill synced clean"`
Expected: sync copies the folder (including `references/` and `scripts/`); output is `new skill synced clean` (no MISSING/STALE lines naming the new skill).

---

## Self-Review (done at plan time, updated after lazy-dev gate)

- Spec coverage: spec components 1-8 map to Tasks 1-3 (script; four references; SKILL.md + command + catalogs). Spec Verification section maps to Task 1 Steps 3-4, Task 3 Step 5, Task 4.
- No placeholders: every content file ships verbatim in this plan.
- Type consistency: rule ids, CLI surface, output format, and file names match Global Constraints and are cited identically in Tasks 1, 3, 4.
- Lazy-dev findings folded: catalog rows moved into the Task 3 bundle commit (P6); C6/C7 expected outputs corrected; AGENTS row placement wording fixed; argparse description carries the ceiling; dead `path` param and None-regex RULES rows removed; hardcoded model trailers dropped (executor appends its own); duplicate fixture step removed; sync grep exit trap fixed; Task 2 stages before `bin/skillctl check` (C1 scans the index, not the worktree); Task 2 depends on Task 1 so its commits never race branch creation.
