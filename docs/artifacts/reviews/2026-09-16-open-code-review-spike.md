# open-code-review spike report

- Date: 2026-09-16
- ocr version: open-code-review v1.12.4 (f1101fd7f) windows/amd64, built 2026-09-16T09:58:39Z
- Model / endpoint type: deepseek-chat, built-in provider `deepseek` (OpenAI-compatible) at https://api.deepseek.com. Note: `ocr llm test` reported the test transport as `deepseek-flash`, while actual scan/review runs reported `deepseek-chat` in the JSON `llm.model` field; recording both for traceability, the run-time model is `deepseek-chat`.
- Branch reviewed: feat/ocr-spike vs main

## What ran

- `ocr config set provider deepseek` then `ocr config set model deepseek-chat` then `ocr config set providers.deepseek.api_key "$DEEPSEEK_API_KEY"` then `ocr llm test` (connectivity ok).
- `Measure-Command { ocr scan --path .githooks --format json --output <temp>/scan-githooks.json --audience agent }` (workdir: repo root).
- `Measure-Command { ocr scan --path skills/typst-pro --format json --output <temp>/scan-typst.json --audience agent }` (workdir: repo root).
- `Measure-Command { ocr review --from main --to feat/ocr-spike --format json --output <temp>/review-diff.json --audience agent }` (workdir: repo root).

## Measurements

| Run | Wall clock | Tokens | Findings |
|---|---|---|---|
| scan .githooks | 34.09s | 90534 total (83251 input, 7283 output, 59520 cache_read) | 16 comments across 2 files |
| scan skills/typst-pro | 0.80s | 0 (no LLM call) | 0, status `skipped` ("No supported files changed.") |
| review main..feat/ocr-spike | 1.29s | 0 (no LLM call) | 0, status `skipped` ("Review skipped: no items were selected.") |

## Sample findings

(verbatim, one line each, from `scan-githooks.json`)

- `.githooks/pre-commit` line 9-10: "`git diff --cached --name-only` quotes any path containing spaces, quotes or non-ASCII bytes (core.quotePath defaults to true), so `for f in $staged` yields mangled names like `"weird\040name.md"` ... severity high, category bug."
- `.githooks/commit-msg` line 12: "Comment character is hardcoded to '#', but git allows it to be changed via `core.commentChar`. If a repository sets a different comment char, comment lines will be treated as the subject ... severity medium, category bug."
- `.githooks/pre-commit` line 92-95: "If `README.md`/`AGENTS.md` are not in the index ... `git show ":README.md"` fails, the pipeline's left side is empty, and both rejections fire, blocking a legitimate commit-check workflow ... severity high, category bug."

All three sample comments are substantive shell-script bugs with concrete fix suggestions, correct line numbers against the actual files, and realistic severity/category tags.

## Markdown handling

Line positions on the .sh findings hold: the file paths and `start_line`/`end_line` numbers line up against the real `.githooks/commit-msg` and `.githooks/pre-commit` content (line 12 of commit-msg is the subject-extraction block; line 9-10 of pre-commit is the `staged=...` assignment). On markdown: `ocr rules check README.md` and `ocr rules check external-skills.md` both return a valid rule pattern, so markdown is not unrecognised by the rules engine. However, `ocr scan --path skills/typst-pro` (a folder with only .md files) returns `skipped: No supported files changed`, and `ocr review --from main --to feat/ocr-spike` (a diff that is entirely `README.md` + `external-skills.md`) returns `skipped: no items were selected`. The diff selector itself resolves the merge-base correctly (manifest shows `resolved_base` = `0a6d96e..`, `resolved_head` = `988c5785..`, `exact_range` populated), but then emits zero items because the changed files are markdown. Verdict: the diff/scan pipeline's file-type allowlist does not currently select markdown, despite rules existing for it.

## Ergonomics

- Install: `npm install -g @alibaba-group/open-code-review` worked on Windows / PowerShell 5.1 in ~6s; `ocr` on PATH after install. No friction.
- Provider setup: three non-interactive `ocr config set` calls and a `ocr llm test` is enough. API-key value is auto-redacted by ocr in stdout (the value appears as a masked token, never the cleartext secret), so it never lands in a tee'd output file in cleartext.
- PowerShell quirks: the npm shim wraps the binary in PowerShell, so non-zero exit codes get re-thrown as `NativeCommandError` via the `2>&1` stream and surface as stderr noise even on success. Cosmetic only; the JSON output is correct. The PowerShell `Get-Content | Select-String` em-dash check false-positives on multibyte UTF-8 (ANSI decode); the `.githooks/pre-commit` hook is the source of truth for em-dash cleanliness.
- JSON output: `ocr scan --format json` and `ocr review --format json` produce a structured document with `status`, `summary.{files_reviewed,comments,total_tokens,input_tokens,output_tokens,cache_read_tokens,elapsed}`, `tool_calls.{total,by_tool,failure,...}`, `comments[]` (each with `path`, `content`, `existing_code`, optional `suggestion_code`, `start_line`, `end_line`, `category`, `severity`), and a `manifest` block. Review adds a `coverage.{selected,completed,reused,failed,waived}` array and full git `input.{resolved_base,resolved_head,exact_range}` provenance.
- Token visibility: scan emits per-run totals including `cache_read_tokens`; review emits the same fields when not skipped. No separate `ocr session` lookup needed for the basic numbers.
- `--format json --output <path>` writes a UTF-8 file directly; `--audience agent` suppresses progress lines so the JSON file is the only stdout payload. Clean automation story.
- Diff selector behaviour on a docs-only branch: the merge-base resolves correctly and the manifest is fully populated, but `coverage.selected` is empty, so the run short-circuits to `skipped` in ~1 second without calling the LLM. That is fast and honest (no hallucinated reviews), but it means a "review every PR" hook would do nothing on this repo.

## Verdict: go-with-caveats

`ocr scan` works end-to-end against this repo's shell code: 16 substantive comments on `.githooks/commit-msg` + `.githooks/pre-commit`, ~90k tokens with cache breakdown visible, ~34 seconds wall clock on a 2-file scan, JSON output with correct line positions and severity tags, and a working DeepSeek provider configured in three non-interactive commands. However, two of the three spike commands (`scan skills/typst-pro` and `review main..feat/ocr-spike`) returned `skipped` because this repo's diff content is markdown and ocr's diff/scan file-type selector does not pick up markdown changes despite `ocr rules check` knowing a rule pattern for `.md`. Because the repo is markdown-only by design (`AGENTS.md` says "Content: Markdown only. No build step, no tooling, no runtime."), blanket adoption would produce zero-review runs on every PR. A targeted use, e.g. a `/standardize-code` opt-in section that runs `ocr scan --path .githooks` against shell/hook changes, is plausible; a repo-wide pre-merge hook is not. The verdict is `go-with-caveats`, not `go`, because the headline ergonomics story is "no findings on a markdown diff" and that has to be communicated honestly to anyone wiring this in.

## Deferred follow-ups (each needs its own feature after the user reads this)

- Install the upstream native OpenCode plugin (if go)
- Add an ocr pre-scan section to /standardize-code (if go)
- Benchmark on a real code repo, not this markdown-only one
- CI hook (blocked: repo has no CI)