# open-code-review spike: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. In this repo the dispatch convention is `/execute-plan`: orchestrator dispatches one `executor` + one `reviewer` per task, escalates two-strike failures to `oracle`, then `doc-standardizer` and `code-standardizer` before the final report.

**Goal:** Catalog Alibaba's `open-code-review` (`ocr`) CLI in the repo's external-tools docs and produce a measured go/no-go spike report on this repo.

**Architecture:** Two doc-only deliverables: (1) catalog entries in `external-skills.md` + `README.md`, (2) a spike report in `docs/artifacts/reviews/` with local measurements of `ocr` (install, config, scan, review on this repo). No workflow wiring; all integration is deferred behind the report's verdict.

**Tech stack:** Markdown only. External CLI: `ocr` via npm. Spec: [2026-09-16-open-code-review-spike-design.md](./2026-09-16-open-code-review-spike-design.md).

## Global constraints

- No em-dash (U+2014) in any committed markdown. Verify before each commit: `(Get-ChildItem <changed .md files> | Select-String -Pattern ([char]0x2014))` must return empty.
- Conventional Commits 1.0.0 subjects, enforced by `.githooks/commit-msg`.
- No API keys, tokens, or raw provider responses in any committed file. Raw CLI output stays under `C:\Users\ruben\AppData\Local\Temp\opencode\ocr-spike\`.
- Only these tracked files may change: `external-skills.md`, `README.md`, `docs/artifacts/reviews/2026-09-16-open-code-review-spike.md`. Anything else discovered mid-execution goes in the final report as a finding, not a change.
- Work happens on branch `feat/ocr-spike`, created from `main` before Task 1. Never commit to `main` directly.
- This repo is markdown-only; ocr's code ruleset will likely yield few findings here. A near-zero findings result is a valid measurement, not a failure. Do not detour into other repos.
- Windows / PowerShell 5.1 environment. Use `;` or `if ($?)` chaining, not `&&`.

---

### Task 1: Catalog entries for open-code-review

**Files:**
- Modify: `external-skills.md` (Sources table, When to use list, new `### open-code-review` note)
- Modify: `README.md` (one bullet under `## External skills`)

**Interfaces:**
- Consumes: nothing.
- Produces: the catalog commit that gives Task 2's `ocr review` a real diff to review. Exact commit subject: `docs(ocr): add open-code-review to external tools catalog`.

- [ ] **Step 1: Create the feature branch**

```powershell
git status --short   # confirm clean tree (artifacts dir additions are expected and untracked; leave them)
if ($?) { git checkout -b feat/ocr-spike }
```

Expected: `Switched to a new branch 'feat/ocr-spike'`.

- [ ] **Step 2: Append row to the Sources table in external-skills.md**

Read the file first. In the `## Sources` table, append after the last row (currently `opencode-see-image`), matching column format:

```markdown
| open-code-review | CLI | Alibaba's AI code-review CLI: hybrid deterministic pipeline + LLM agent, diff or full-file review, line-level comments, OpenAI-compatible endpoints. |
```

- [ ] **Step 3: Add trigger bullet to the When to use section**

Append to the `## When to use` bullet list:

```markdown
- You want a cheap deterministic first pass over a diff or unfamiliar directory before reviewing it by hand (the `ocr` CLI).
```

- [ ] **Step 4: Add the per-source note**

Read the `### opencode-see-image` entry, then append after it, matching the existing note format (paragraphs, `Install:` line, `Source:` line):

```markdown
### open-code-review

Alibaba's `ocr` CLI: an AI code-review tool built as a hybrid of deterministic engineering (file selection, file bundling, template-based rule matching) and an LLM agent for dynamic context gathering. Two modes matter here: `ocr review` for diffs (workspace, branch range, or single commit) and `ocr scan` for whole files, no git history needed. Comments come back with line-level positioning and JSON output, which makes the results consumable by an agent.

It also has a delegation mode (`ocr delegate preview|rule`) that runs only the deterministic layer and hands the actual review to the host coding agent, no separate API key required, plus an official native OpenCode plugin. Spike measured on this repo 2026-09-16: see `docs/artifacts/reviews/2026-09-16-open-code-review-spike.md` for the verdict before wiring it into any workflow.

Install: `npm install -g @alibaba-group/open-code-review` (Git >= 2.41 required)
Source: https://github.com/alibaba/open-code-review
```

If the spike report does not exist yet at commit time (Task 1 commits first), keep the sentence but phrase it as "spike running 2026-09-16, report lands in `docs/artifacts/reviews/`". Task 2's review step will see the final text via the branch diff; if the wording needs the report path, amend only if the report is committed in the same branch, otherwise leave the forward reference as written.

- [ ] **Step 5: Add README bullet**

In `README.md` under `## External skills`, append after the last bullet (do not touch the pre-existing stale entries):

```markdown
- **open-code-review** - Alibaba's AI code-review CLI (deterministic pipeline + LLM agent)
```

- [ ] **Step 6: Verify and commit**

```powershell
Get-Content external-skills.md, README.md | Select-String -Pattern ([char]0x2014)   # expect empty
git add external-skills.md README.md
git commit -m "docs(ocr): add open-code-review to external tools catalog"
```

Expected: em-dash check empty; commit-msg hook accepts the subject.

---

### Task 2: Spike execution and go/no-go report

**Files:**
- Create: `docs/artifacts/reviews/2026-09-16-open-code-review-spike.md`
- Create (untracked, temp): outputs under `C:\Users\ruben\AppData\Local\Temp\opencode\ocr-spike\`

**Interfaces:**
- Consumes: Task 1's commit on `feat/ocr-spike` (the diff that `ocr review` measures).
- Produces: the spike report. This is the plan's final deliverable; nothing depends on it inside this plan. The report's verdict gates all future integration work (out of scope here).

- [ ] **Step 1: Install and record version**

```powershell
New-Item -ItemType Directory -Force -Path "$env:TEMP\opencode\ocr-spike" | Out-Null
npm install -g @alibaba-group/open-code-review
ocr --version 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\version.txt"
ocr --help 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\help.txt"
```

Expected: version string recorded. If npm install fails on this platform, that is a spike finding: document the error, skip to Step 5, write a no-go report.

- [ ] **Step 2: Configure the LLM, first path that works wins**

a. Probe for an existing key (do NOT print the value):

```powershell
Get-ChildItem env: | Where-Object { $_.Name -match 'ZAI|Z_AI|OPENAI|DASHSCOPE|API_KEY' } | Select-Object -ExpandProperty Name
```

If a plausible key exists, fetch https://open-codereview.ai/docs/configuration and set up the custom OpenAI-compatible provider via env vars or config file (z.ai endpoint for GLM). Pin the model to the GLM variant the key provides; record the model name and endpoint type (not the key) for the report.

b. If no key: use delegation mode instead:

```powershell
ocr delegate preview 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\delegate-preview.txt"
```

Record in the report: LLM layer unmeasured, deterministic layer only. Do not prompt the user for a key; the fallback chain is in the spec.

If config fails entirely, that is a finding (no-go for agent integration ergonomics): document, skip to Step 5.

- [ ] **Step 3: Run scans (from repo root, workdir = repo)**

```powershell
Measure-Command { ocr scan --path .githooks 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\scan-githooks.txt" } | Select-Object -ExpandProperty TotalSeconds | Tee-Object "$env:TEMP\opencode\ocr-spike\scan-githooks-seconds.txt"
Measure-Command { ocr scan --path skills/typst-pro 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\scan-typst.txt" } | Select-Object -ExpandProperty TotalSeconds | Tee-Object "$env:TEMP\opencode\ocr-spike\scan-typst-seconds.txt"
```

If `--format json` is supported for scan, prefer it (`--format json --output <temp>.json`) and note the JSON shape. Record for each: wall-clock seconds, findings count, 2-3 verbatim sample findings (trimmed to one line each), token usage if ocr reports it (session list, JSON output, or stdout summary). If tokens are not exposed anywhere, record that as an ergonomics finding.

- [ ] **Step 4: Run diff review over Task 1's commit**

```powershell
Measure-Command { ocr review --from main --to feat/ocr-spike --format json --output "$env:TEMP\opencode\ocr-spike\review-diff.json" 2>&1 | Tee-Object "$env:TEMP\opencode\ocr-spike\review-diff.txt" } | Select-Object -ExpandProperty TotalSeconds | Tee-Object "$env:TEMP\opencode\ocr-spike\review-diff-seconds.txt"
```

Record: completion, seconds, token usage, findings count, whether comments carry correct line positions on markdown (check one against the actual diff), and one verbatim sample comment. Note whether `--from/--to` merge-base mode works on a branch whose only change is a docs commit.

- [ ] **Step 5: Write the spike report**

Create `docs/artifacts/reviews/2026-09-16-open-code-review-spike.md` with exactly this skeleton, every field filled from Steps 1-4 (delete the N/A lines only if truly measured):

```markdown
# open-code-review spike report

- Date: 2026-09-16
- ocr version: <from version.txt>
- Model / endpoint type: <pinned model, or "delegation mode (no LLM layer measured)">
- Branch reviewed: feat/ocr-spike vs main

## What ran

<scan commands + review command, one line each>

## Measurements

| Run | Wall clock | Tokens | Findings |
|---|---|---|---|
| scan .githooks | <s> | <n or "not exposed"> | <n> |
| scan skills/typst-pro | <s> | <n or "not exposed"> | <n> |
| review main..feat/ocr-spike | <s> | <n or "not exposed"> | <n> |

## Sample findings

<2-3 verbatim, one line each, or "none produced">

## Markdown handling

<did line positions hold? did rules fire at all on .md? short verdict>

## Ergonomics

<config friction, PowerShell quirks, JSON output shape, token visibility>

## Verdict: <go | go-with-caveats | no-go>

<one paragraph justification grounded only in the numbers above>

## Deferred follow-ups (each needs its own feature after the user reads this)

- Install the upstream native OpenCode plugin (if go)
- Add an ocr pre-scan section to /standardize-code (if go)
- Benchmark on a real code repo, not this markdown-only one
- CI hook (blocked: repo has no CI)
```

- [ ] **Step 6: Verify and commit**

```powershell
Get-Content docs\artifacts\reviews\2026-09-16-open-code-review-spike.md | Select-String -Pattern ([char]0x2014)   # expect empty
Select-String -Path docs\artifacts\reviews\2026-09-16-open-code-review-spike.md -Pattern 'sk-[A-Za-z0-9]'   # expect empty (no secrets)
git add docs/artifacts/reviews/2026-09-16-open-code-review-spike.md
git commit -m "docs(ocr): add open-code-review spike report"
```

Expected: both checks empty; hook accepts subject.

- [ ] **Step 7: Leave the branch unmerged**

Do not merge to `main`, do not push. The user reads the verdict and decides. Report branch name, commits, and report path in the executor summary.
