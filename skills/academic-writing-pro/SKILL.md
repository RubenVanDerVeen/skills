---
name: academic-writing-pro
description: Use when checking or drafting academic text for soundness (FOCSI tone, sentence construction, quoting, paraphrase, citations), drafting a literature review, research proposal, or paper, or on /academic-check. IEEE numbered citations default; venue styles override.
---

## Overview

Two passes, always both. The lint script catches what regex can catch. Anything contextual (paragraph flow, claim strength, hedging in context, paraphrase distance) needs the judgment pass. Never pass on script output alone. Report only: findings go to the writer; edit nothing unless asked.

Quick start (paths relative to this skill's folder):

```bash
python3 skills/academic-writing-pro/scripts/lint-academic.py paper.tex
python3 skills/academic-writing-pro/scripts/lint-academic.py --against source.md paper.md
python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test
```

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