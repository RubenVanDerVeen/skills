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