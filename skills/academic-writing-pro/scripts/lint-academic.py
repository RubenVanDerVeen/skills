#!/usr/bin/env python3
"""Surface linter for academic prose. Stdlib only. Reports, never edits.

Mechanical pass of the academic-writing-pro two-pass workflow. The judgment
pass (references/judgment-pass.md) covers everything contextual.
# ponytail: regex heuristics; real parsing only when false positives hurt.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

# Lower number = more severe. --min-level filters: show level <= min.
LEVEL_RANK = {"error": 0, "warning": 1, "info": 2}

# Always-on context check ids. --enable/--disable do not toggle them.
ALWAYS_ON = {"citation-missing", "quote-required", "readability"}

RULES = [
    {"id": "focsi-formal", "level": "error",
     "regex": re.compile(
         r"\b(?:don't|doesn't|didn't|can't|won't|wouldn't|couldn't|shouldn't|"
         r"isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|it's|that's|"
         r"there's|they're|we're|we've|you're|you've|i'm|i've|let's|ain't)\b",
         re.IGNORECASE),
     "message": "Contraction: spell out both words."},
    {"id": "focsi-formal", "level": "error",
     "regex": re.compile(r"!"),
     "message": "Exclamation mark: academic prose does not use exclamations."},
    {"id": "focsi-impersonal", "level": "info",
     "regex": re.compile(
         r"\b(?:[Ii]|[Ww]e|[Oo]ur|[Uu]s|[Mm]y|[Yy]ou|[Yy]our)\b"),
     "message": "First/second person: rewrite impersonally (allowed for goals, "
                "methodology steps, and section previews)."},
    {"id": "focsi-formal", "level": "warning",
     "regex": re.compile(
         r"\b(?:a lot of|lots of|stuff|kind of|sort of|really|pretty much|"
         r"huge|okay)\b", re.IGNORECASE),
     "message": "Casual wording: use a formal equivalent."},
    {"id": "focsi-succinct", "level": "warning",
     "regex": re.compile(
         r"\b(?:it is important to note that|it should be noted that|"
         r"in order to|due to the fact that|for the purpose of|"
         r"in the event that|the fact that)\b", re.IGNORECASE),
     "message": "Throat-clearing: delete or shorten."},
    {"id": "focsi-cautious", "level": "info",
     "regex": re.compile(
         r"\b(?:proves?|clearly|obviously|undoubtedly|always|never|must)\b", re.I),
     "message": "Possible unhedged claim: hedge or justify; see "
                "references/hedging.md (legit in math contexts)."},
    {"id": "sentence-splice", "level": "info",
     "regex": re.compile(
         r",\s+(?:this|these|those|it|they|however|therefore|moreover|"
         r"furthermore)\b", re.IGNORECASE),
     "message": "Possible comma splice: verify the clauses are independent."},
    {"id": "sentence-length", "level": "info",
     "regex": None,
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
SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
QUOTE_RE = re.compile(r'["\u201c]([^"\u201d]{2,})["\u201d]')


def cite_re(fmt: str):
    """Citation forms per format; Typst adds @key."""
    extra = r"|@[A-Za-z][A-Za-z0-9_-]+" if fmt == "typst" else ""
    return re.compile(CITE_BASE + extra)


def mask_regions(text: str, fmt: str) -> str:
    """Replace markup regions with spaces; newlines survive so line
    numbers stay aligned with the source."""
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


def overlap_findings(text: str, source: str) -> list[tuple]:
    """4+ word overlap detection; called from --against mode.

    When the source is your own prior draft, this is text recycling.
    """
    TOKEN_RE = re.compile(r"[A-Za-z0-9']+")

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
                         "Quote and cite, or paraphrase; if the source is "
                         "your own prior draft, this is text recycling."))
    return findings


def _regex_findings(rule, masked, accept, reject):
    """Apply a regex rule to masked text; vocab scoping is line-granular:
    the matched token ("we") is judged against the phrases on the line it
    appears in ("we describe ...")."""
    out = []
    for m in rule["regex"].finditer(masked):
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
    """Context checks: sentence-length (rule-driven via RULES) and
    citation-missing (always-on). Ports matching and window logic from
    the original script with two changes: every severity literal 'warn'
    becomes 'warning', and citation detection runs cite_re(fmt) over
    masked text. Vocab scoping does not currently apply to these
    context checks; the parameters are kept for forward compatibility.
    """
    del text, accept, reject  # context checks (currently) ignore vocab
    out = []
    for m in SENTENCE_RE.finditer(masked):
        if len(m.group().split()) > 40:
            line = masked.count("\n", 0, m.start()) + 1
            out.append((line, "info", "sentence-length", rule["message"]))
    cite = cite_re(fmt)
    for m in QUOTE_RE.finditer(masked):
        window = masked[m.end():m.end() + 120]
        if not cite.search(window):
            line = masked.count("\n", 0, m.start()) + 1
            out.append((line, "warning", "citation-missing",
                        "Quoted text without a nearby citation "
                        "([n] or (Author, year))."))
    return out


def readability_finding(text: str):
    """One info-level guideline per file: sentence and paragraph stats.

    Always-on by default; --disable readability silences it. Empty input
    or input without sentence terminators produces no finding.
    """
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    words = sorted(len(re.findall(r"[A-Za-z0-9']+", s)) for s in sentences)
    if not words:
        return []
    paras = [len(re.findall(r"[A-Za-z0-9']+", p))
             for p in text.split("\n\n") if p.strip()]
    p90 = words[min(len(words) - 1, round(0.9 * (len(words) - 1)))]
    med = words[len(words) // 2]
    pmed = sorted(paras)[len(paras) // 2] if paras else 0
    msg = (f"Guideline only: median sentence {med} words, p90 {p90}; "
           f"median paragraph {pmed} words. High numbers: consider splitting.")
    return [(1, "info", "readability", msg)]


def analyze(text: str, fmt: str = "plain", accept=(),
            reject=(), enabled=None, disabled=None):
    """Return (line, level, rule_id, message) tuples sorted by line.

    Backward compatible: analyze(text) keeps the original one-positional
    signature for self-test use.
    """
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--against", metavar="SOURCE")
    ap.add_argument("--format", choices=("plain", "markdown", "typst", "latex"))
    ap.add_argument("--min-level", choices=("error", "warning", "info"),
                    default="warning")
    ap.add_argument("--enable", default="",
                    help="comma-separated rule ids (default: all)")
    ap.add_argument("--disable", default="",
                    help="comma-separated rule ids to skip")
    ap.add_argument("--vocab", type=Path, default=SKILL_DIR / "vocab",
                    help="dir with accept.txt / reject.txt")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.file:
        ap.error("a file is required unless --self-test")
    path = Path(args.file)
    fmt = args.format or {"typ": "typst", "tex": "latex",
                          "md": "markdown",
                          "markdown": "markdown"}.get(
        path.suffix.lstrip("."), "plain")
    accept, reject = load_vocab(args.vocab)
    enabled = {s for s in args.enable.split(",") if s} or None
    disabled = {s for s in args.disable.split(",") if s}
    text = path.read_text(encoding="utf-8")
    findings = analyze(text, fmt, accept, reject, enabled, disabled)
    if args.against:
        findings += overlap_findings(
            text, Path(args.against).read_text(encoding="utf-8"))
    findings = [f for f in findings
                if LEVEL_RANK[f[1]] <= LEVEL_RANK[args.min_level]]
    findings.sort(key=lambda f: (f[0], LEVEL_RANK[f[1]]))
    for line, level, rule, msg in findings:
        print(f"{path}:{line}: [{level.upper()}] {rule}: {msg}")
    n_err = sum(1 for f in findings if f[1] == "error")
    n_warn = sum(1 for f in findings if f[1] == "warning")
    n_info = sum(1 for f in findings if f[1] == "info")
    print(f"SUMMARY: {path}: {n_err} errors, {n_warn} warnings, {n_info} infos")
    return 1 if n_err else 0


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
TYPST = 'Prior work "established the baseline" @noauthor_literature_nodate.\n'
QUOTED_NOCITE = 'The "baseline result" is disputed by recent measurements.\n'
MARKUP_CLEAN = ("The `don't` token stays in code.\n\n"
                "```\ndon't panic\n```\n\nSee https://example.com/x.\n")


def self_test() -> int:
    expected = {"focsi-formal", "focsi-impersonal", "focsi-succinct",
                "citation-missing", "sentence-splice", "sentence-length"}
    bad = {rule for _, _, rule, _ in analyze(BAD)}
    missing = expected - bad
    assert not missing, f"self-test FAIL, rules not detected: {sorted(missing)}"
    # Always-on readability fires on every input; filter it out so the
    # "no false positives" assertion does not count it.
    clean = [f for f in analyze(CLEAN) + analyze(QUOTED)
             if f[2] != "readability"]
    assert clean == [], f"self-test FAIL, false positives: {clean}"
    src_rules = {rule for _, _, rule, _ in analyze(OVERLAP_TGT)}
    assert "quote-required" not in src_rules, "quote-required without --against"
    ovl = overlap_findings(OVERLAP_TGT, OVERLAP_SRC)
    assert any(r == "quote-required" for _, _, r, _ in ovl), \
        f"self-test FAIL, overlap not detected: {ovl}"
    typ = analyze(TYPST, fmt="typst")
    assert not [f for f in typ if f[2] == "citation-missing"], \
        "self-test FAIL: Typst @key citation not recognized"
    assert any(f[2] == "citation-missing" for f in
               analyze(QUOTED_NOCITE, fmt="typst")), \
        "self-test FAIL: quoted text without a citation went unflagged"
    assert not [f for f in analyze(MARKUP_CLEAN, fmt="markdown")
                if f[2] != "readability"], \
        "self-test FAIL: markup regions produced findings"
    acc = ("we describe",)
    line = "We describe the pipeline in this section.\n"
    assert not [f for f in analyze(line, accept=list(acc))
                if f[2] == "focsi-impersonal"], \
        "self-test FAIL: vocab accept"
    assert [f for f in analyze(line) if f[2] == "focsi-impersonal"], \
        "self-test FAIL: vocab accept suppressed too much"
    print("self-test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
