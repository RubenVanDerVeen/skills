---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment.
---

## Overview

Adapted from obra/superpowers (MIT).

Skill authoring is Test-Driven Development applied to process documentation. Write a failing test (pressure scenario run against a subagent), write the skill, watch the test pass, refactor to close loopholes. If you have not watched an agent fail without the skill, you do not know whether the skill teaches the right thing.

Heavy reference material lives under `references/`:

- `references/anthropic-best-practices.md`: concise authoring, degrees of freedom, structure, anti-patterns.
- `references/persuasion-principles.md`: Cialdini / Meincke research on why bright-line rules and commitment framing raise LLM compliance.
- `references/testing-skills-with-subagents.md`: the full RED-GREEN-REFACTOR cycle for skills, pressure-scenario recipes, meta-testing.

In this repo, `AGENTS.md` rules win on points where upstream guidance disagrees: kebab-case `name` matching the folder, `description` starting with "Use when...", under 1024 bytes of frontmatter, body opening with `## Overview`, no em-dashes (U+2014).

## What a Skill Is

A skill is a reference guide for a proven technique, pattern, or tool. Skills are reusable techniques, patterns, and reference docs. Skills are not narratives about solving one problem once. If the lesson only applies to a single project, put it in `AGENTS.md` or a project README, not a skill.

## Frontmatter

```markdown
---
name: kebab-case-name
description: Use when [specific triggering conditions, symptoms, tools, error messages].
---
```

- `name`: letters, numbers, hyphens only. Must match the folder name.
- `description`: third person, starts with "Use when...", describes only when to load the skill, under ~500 characters. Max 1024 bytes of frontmatter total (this repo's hard rule).
- Both fields are pre-loaded for every skill, so wording is the agent's primary signal for whether to load the body.

## Description as Trigger (SDO)

The description is what the agent reads to decide whether to load the skill right now. Treat it as a trigger specification, not a summary.

- Start with "Use when..." and list concrete triggers: error messages, symptoms, tool names, file extensions, user phrases.
- Describe the problem, not the language-specific symptom (race condition, not `setTimeout`).
- Third person (it is injected into the system prompt).
- NEVER summarise the skill's process or workflow. A description that summarises the workflow creates a shortcut the agent will take instead of reading the body.

```yaml
# bad: summarises workflow, agent may follow this instead of reading the skill
description: Use when executing plans and dispatching subagents with code review between tasks

# bad: process detail in the description
description: Use for TDD, write test first, watch it fail, write minimal code, refactor

# good: triggering conditions only
description: Use when executing implementation plans with independent tasks in the current session

# good: triggers by symptom
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

## Body Structure

```markdown
## Overview
1-2 sentences: what this is, core principle.

## When to use
Bulleted symptoms and use cases. When NOT to use.

## Core pattern (techniques/patterns)
Before/after comparison or contract.

## Implementation
Inline code for simple patterns. Link to file for heavy reference.

## Common mistakes
What goes wrong + fixes.
```

Rules:

- Body starts with `## Overview`. No top-level `## Skill` heading.
- One excellent example beats many mediocre ones. TypeScript or shell is fine; the reader can port.
- Lean skills target under 200 words; frequently-loaded skills under 500. Heavy reference goes to `references/<file>.md` and is linked from the body.
- Flowcharts only for non-obvious decisions. Tables for reference material. Code in markdown blocks.

## Match the Form to the Failure

Before writing guidance, classify the baseline failure. The form that bulletproofs one failure type measurably backfires on another.

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Skips a rule under pressure (knows better, does it anyway) | Prohibition + rationalization table + red flags | Soft guidance ("prefer...", "consider...") |
| Complies, but output has the wrong shape | Positive recipe: state what the output IS, in parts and order | Prohibition list ("don't restate", "never narrate") |
| Omits a required element from something already produced | REQUIRED slot in the template they fill in | Prose reminders near the template |
| Behaviour should depend on a condition | Conditional keyed to an observable predicate | Unconditional rule with exemption clauses |

For wrong-shaped output or omitted elements, prohibition-based bulletproofing backfires: under a competing incentive ("make the prompt self-contained"), agents negotiate with "don't X". In head-to-head wording tests on dispatch-prompt guidance, the prohibition arm produced clearly more of the unwanted content than the recipe arm, and trended worse than even the no-guidance control. A recipe leaves nothing to negotiate.

Rules for whichever form you pick:

- No nuance clauses. "Don't X unless it matters" reopens the negotiation. Express a real exception as its own conditional on an observable predicate.
- Exemption clauses do not scope. If part of the output must be exempt, restructure so the rule cannot reach it.

## Token Efficiency

- Move heavy reference to `references/<file>.md`. The agent loads the body on trigger; it loads referenced files only as needed.
- Compress examples: a 20-word worked example beats a 42-word narrative.
- Cross-reference, do not duplicate. "REQUIRED: use `other-skill` for the workflow" with a one-line summary beats re-stating the workflow.
- One excellent example per skill. Multi-language dilution produces five mediocre versions.

## Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to new skills and edits to existing skills. Writing a skill before testing it is the same violation as writing code before its test. Edit without testing: same violation. No exceptions for "simple additions", "just adding a section", "documentation updates". Delete means delete.

## RED-GREEN-REFACTOR for Skills

### RED: Baseline (Watch It Fail)

Run pressure scenarios without the skill. Document verbatim what the agent chose and how it rationalised the choice. This is "watch the test fail": you must see what agents naturally do before writing the skill. Without this step you are documenting your guess at the failure, not the actual failure.

### GREEN: Write the Minimal Skill

Write the skill addressing those specific rationalisations. Do not add content for hypothetical cases. Re-run the same scenarios with the skill loaded. The agent should now comply.

### REFACTOR: Close Loopholes

Agent found a new rationalisation? Add an explicit counter, an entry to the rationalisation table, and a red flag. Re-test until bulletproof. Signs of a bulletproof skill:

1. Agent chooses the correct option under maximum pressure.
2. Agent cites skill sections as justification.
3. Agent acknowledges the temptation but follows the rule.
4. Meta-test reveals "skill was clear, I should follow it".

### Micro-Test Wording Before Full Scenarios

Full pressure-scenario runs are the final gate but slow and expensive per iteration. Verify the wording itself first with micro-tests:

1. One fresh-context sample per call (raw API call or single-shot subagent). System prompt = the realistic context the guidance will live in (the full skill or prompt template, not the guidance in isolation). User message = a task that tempts the failure.
2. Always include a no-guidance control. If the control does not exhibit the failure, there is nothing to fix.
3. 5+ reps per variant. Single samples lie.
4. Read every flagged match manually. Template echoes and quoted counter-examples masquerade as hits; automated counts alone overstate both failure and success.
5. Variance is a metric. When guidance lands, reps converge on the same shape. Five different interpretations across five reps means the wording is not binding; tighten the form before adding words.

Micro-tests verify wording; they do not replace pressure scenarios for discipline skills.

See `references/testing-skills-with-subagents.md` for pressure-scenario recipes, the pressure-types table, and meta-testing.

## Bulletproofing Discipline Skills

This toolkit is for discipline failures (an agent that knows the rule and skips it under pressure). For wrong-shaped output or omitted elements, prohibition-based bulletproofing backfires; use the forms in Match the Form to the Failure instead.

### Rationalisation Table

Capture rationalisations from baseline testing. Every excuse goes in the table with the reality.

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

### Red Flags

A short list an agent can self-check when rationalising. Each red flag means "STOP, start over".

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."
```

### Foundational Principle

Add a one-line principle early in the skill that cuts off the "spirit vs letter" class of rationalisations:

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Update Description for Violation Symptoms

Add the symptoms of being about to violate the rule to the description so it loads earlier in the temptation:

```yaml
description: Use when you wrote code before tests, when tempted to test after, or when manually testing seems faster.
```

The research foundation for why authority, commitment, scarcity, social proof, and unity framing raise LLM compliance lives in `references/persuasion-principles.md`.

## Anti-Patterns

- Narrative example. "In session 2025-10-03, we found..." Too specific, not reusable.
- Multi-language dilution. example-js.js, example-py.py, example-go.go. Mediocre quality, maintenance burden.
- Code in flowcharts. dot blocks with `step1 [label="import fs"]`. Cannot copy-paste, hard to read.
- Generic labels. helper1, helper2, step3, pattern4. Labels should have semantic meaning.
- Windows-style paths in cross-platform skills. `scripts\helper.py` over `scripts/helper.py`.
- Too many options. "You can use pypdf, or pdfplumber, or PyMuPDF, or...". One default, named escape hatch for the exceptional case.

## Skill Authoring Checklist (TDD Adapted)

Run this checklist for every new skill and every meaningful edit.

**RED phase:**

- [ ] Pressure scenarios drafted (3+ combined pressures for discipline skills).
- [ ] Scenarios run without skill, baseline behaviour captured verbatim.
- [ ] Rationalisation patterns identified.

**GREEN phase:**

- [ ] `name` is kebab-case and matches folder.
- [ ] Frontmatter is valid YAML, total under 1024 bytes (this repo).
- [ ] `description` starts with "Use when...", is third person, lists triggers, no workflow summary.
- [ ] Body opens with `## Overview` and the credit line if adapted from upstream.
- [ ] One excellent example, not multi-language.
- [ ] Heavy reference moved to `references/<file>.md`.
- [ ] No em-dashes (this repo's pre-commit hook).
- [ ] Scenarios re-run with skill loaded, agent complies.

**REFACTOR phase:**

- [ ] New rationalisations captured, counters added.
- [ ] Rationalisation table updated.
- [ ] Red flags list updated.
- [ ] Description updated with violation symptoms if relevant.
- [ ] Re-tested, still complies, bulletproof.

## Bottom Line

Skill creation is TDD. Same iron law: no skill without a failing test first. Same cycle: RED, GREEN, REFACTOR. If you follow TDD for code, follow it for skills; it is the same discipline applied to documentation.