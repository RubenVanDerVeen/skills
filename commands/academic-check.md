---
description: Academic soundness check on a file or selection (lint script + judgment report, no edits)
---

Load the `academic-writing-pro` skill and run its full check workflow on `$ARGUMENTS`. `$ARGUMENTS` is a file path; when omitted, check the file or selection from the current session context. Produce the unified severity-ranked report (errors, warns, infos, each with rule and concrete fix). Report only: do not edit the text unless the user asks for fixes.
