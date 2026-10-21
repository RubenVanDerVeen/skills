---
description: Compressed code review, one line per finding
---

Review the given diff or branch (default `git diff main...HEAD`; or $ARGUMENTS). One line per finding, format: `path:line problem -> fix`. Order by severity. No summary paragraphs, no praise, no restating the diff. End with `PASS` when there are no findings.
