---
description: Academic soundness check on a file (lint script + judgment report, no edits)
---

Load the `academic-writing-pro` skill. If `$ARGUMENTS` is empty, ask for a file path before running anything. Otherwise run its full check workflow on that file: lint script first, passing `--format` for the file's extension and `--against <source>` when the user supplied a source; then the judgment pass per `references/judgment-pass.md`. End with the script's SUMMARY line plus the number of findings the judgment pass added. Report only: do not edit the text unless the user asks.