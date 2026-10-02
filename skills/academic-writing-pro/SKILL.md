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
