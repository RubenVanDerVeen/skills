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
