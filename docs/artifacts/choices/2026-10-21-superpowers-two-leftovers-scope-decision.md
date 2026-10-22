# Superpowers scope: two leftover skills

- Date: 2026-10-21
- Status: active
- Source: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-report.md` (spec: `docs/artifacts/features/vendor-external-packs/2026-10-21-vendor-external-packs-design.md`)

## Choice

Only `using-superpowers` and `verification-before-completion` were vendored from the superpowers remainder. Own process-skill set: 5 existing + 2 new = 7 of the 15 upstream skills. The other 8 upstream siblings stay unvendored and left with the plugin.

## Why

- The two are the actively used leftovers; the run discipline (invoke skills before responding, evidence before "done") depends on them.
- The other 8 (test-driven-development, executing-plans, requesting/receiving-code-review, subagent-driven-development, dispatching-parallel-agents, find-skills, condition-based-waiting) are unused here; every registered skill costs startup context and frontmatter budget.

## Alternatives rejected

- Vendor all 15: unused skills pollute the skill listing and denylists.
- Vendor none: both are load-bearing for the execute-plan discipline.

## Revisit when

An unvendored sibling becomes part of the daily flow; then vendor it with the same adaptation rules (attribution line, house frontmatter, references split).
