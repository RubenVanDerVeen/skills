---
description: Run the 4 code-structure agent checks against a path, language, or the current branch diff; report PASS or numbered findings
---

Load the `code-standardization` skill and run the 4 agent checks from it (presence, documentation, consistency, boundaries).

Scope comes from `$ARGUMENTS` when supplied:

- a path: restrict the audit to that path
- a language: restrict the audit to that language's guide
- empty: audit the current branch diff

Default scope is the current branch diff (`git diff <base>...HEAD`). If `$ARGUMENTS` is empty and there is no diff, audit the whole repo.

For each language present in scope, run the matching per-language guide and the pinned formatter/linter in check mode if installed (`command -v <tool> && <tool> --check`); if absent, emit a quick-fix finding naming the tool and the config file to add. Never re-lint in the agent body.

Report `PASS` or a numbered findings list with `quick-fix:` and `recommendation:` tags, same format as the `standardizer` agent. Stay read-only.
