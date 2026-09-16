# open-code-review spike: design

- Date: 2026-09-16
- Status: approved for planning (single-pass /full-cycle)
- Topic: adopt, ignore, or defer Alibaba's `open-code-review` (`ocr`) CLI as a review layer under the existing skills pipeline
- Input: external research summary (user-provided) + repo recon + upstream README verification

## Problem

Research recommends `ocr` as a deterministic pre-scan / per-PR review layer under the `standardizer` / `reviewer` agents, with a spike before any integration. The claims (1/9 tokens, higher F1, OpenAI-compat) are vendor-bench numbers and unverified locally. A decision artifact is needed before any workflow wiring happens.

## Verified facts (corrections to the research summary)

Checked against the upstream README (github.com/alibaba/open-code-review) and this repo:

1. Install is npm: `npm install -g @alibaba-group/open-code-review`. Windows supported (native `install.ps1` also exists). Apache-2.0. Requires Git >= 2.41.
2. CLI surface: `ocr review` (workspace mode, `--from/--to` merge-base mode, `--commit`), `ocr scan` (full-file, `--path`), `ocr config provider|model` (interactive), `ocr session list/--resume`, `--format json --output <file>`.
3. Missed by research: an official **native OpenCode plugin** exists (`plugins/open-code-review/opencode/` upstream) providing native review tools and slash commands.
4. Missed by research: **delegation mode** (`ocr delegate preview|rule`) runs the deterministic layer (file selection, rule resolution) using the host coding agent's own LLM. No OCR-side API key needed.
5. Correction: this repo has **no CI** (`.github/` absent, no workflow files). The research's CI-hook integration point is moot today.
6. Correction: this repo is **markdown-only**. ocr's built-in ruleset targets code languages (NPE, thread-safety, XSS, SQL injection). The only code here is `.githooks/*.sh`. A spike on this repo validates operability, markdown handling, token/time cost, and integration ergonomics. It cannot reproduce AACR-Bench precision claims; that needs a real code repo and stays deferred.

## Goals

1. Make `ocr` discoverable: catalog entries in the repo's external-tools docs.
2. Run a measured spike on this repo: operability on Windows/PowerShell, behavior on markdown, token and wall-clock cost, sample output quality, config friction.
3. Produce a go/no-go report with an explicit deferred list, so any integration work starts from local numbers, not vendor claims.

## Non-goals (deferred until the spike verdict says go)

- Modifying `commands/standardize-code.md`, the `code-standardization` skill, or any agent definition.
- Installing the upstream OpenCode plugin into `~/.config/opencode/`.
- Any CI setup (none exists).
- Benchmarking `ocr` against the `standardizer` agent or reproducing AACR-Bench.
- Adopting project-specific review rules files (`.opencodereview/`).

## Approaches considered

- **A. Catalog + spike only (chosen).** Smallest reversible step. The research itself recommended "add to external-skills.md and do a spike before committing." If the verdict is no-go, the catalog row stays as a record and nothing else changed.
- **B. A + wire OpenCode plugin and /standardize-code pre-scan now.** Rejected: wires a tool before measuring, and the markdown-only repo may well prove ocr irrelevant here (its ruleset targets code).
- **C. Full: B + CI hook + benchmark vs standardizer.** Rejected: no CI exists to hook, and the benchmark needs a code repo. Both are follow-ups gated on A's verdict.

## Design (approach A)

### 1. Catalog entries (docs only)

- `external-skills.md`: append a `| open-code-review | CLI | ... |` row to the `## Sources` table, a `### open-code-review` note after `### opencode-see-image` (list is chronological-by-adoption, not alphabetical), and one `## When to use` trigger bullet. Follow the existing per-source note format exactly (paragraphs, `Source:` line, `Install:` line).
- `README.md`: one bullet under `## External skills`. Do not fix the list's pre-existing staleness (missing markitdown, ponytail, opencode-see-image) in this change; that is unrelated.

### 2. Spike protocol

Environment: this repo, Windows, PowerShell. Model pinned to the user's existing GLM provider (OpenAI-compatible z.ai endpoint) for comparability.

Steps, in order:

1. Install: `npm install -g @alibaba-group/open-code-review`; record version. Verify `ocr --help`.
2. Configure LLM, first path that works wins:
   - a. Reuse an existing key already present in the environment (`ZAI_API_KEY`, `Z_AI_API_KEY`, `OPENAI_API_KEY` pointing at z.ai, or similar). Consult https://open-codereview.ai/docs/configuration for the env-var / custom-provider setup; avoid the interactive `ocr config` UI where possible.
   - b. If no key exists, use **delegation mode** (`ocr delegate preview`, `ocr delegate rule`) to validate the deterministic layer and record that the LLM layer is unmeasured.
3. `ocr scan --path .githooks` (the only real code) and `ocr scan --path skills/typst-pro` (representative markdown folder). Record: completion, wall-clock time, token usage from output, findings count and a sample of findings verbatim.
4. `ocr review --from main --to <spike-branch> --format json --output <temp>` on the spike's own diff (catalog commit from step 1 gives it a real diff). Record the same metrics plus whether line-level positioning works on markdown.
5. Note integration ergonomics: config friction, PowerShell quirks, whether output is easy for an agent to consume (JSON shape).

Hard rules: no API keys or tokens in any committed file; raw outputs stay in temp, only distilled numbers and short verbatim samples go in the report.

### 3. Report and decision gate

- Location: `docs/artifacts/reviews/2026-09-16-open-code-review-spike.md` (flat chronological reviews dir, matches convention).
- Contents: environment (ocr version, model, endpoint type), what ran, measured numbers (time, tokens, findings), sample findings, markdown-handling verdict, ergonomics notes, then a clear **go / no-go / go-with-caveats** recommendation and the deferred follow-up list (plugin install, /standardize-code pre-scan section, benchmark on a code repo, CI hook if CI ever exists).
- The follow-ups are **not** part of this plan. Each becomes its own feature only after the user reads the verdict.

## Success criteria

- Catalog entries land in the same commit, consistent with existing formats (pre-commit P6-style sync discipline applied to docs).
- Spike report committed with measured numbers, not restated vendor claims.
- Hooks pass: Conventional Commits subject, no U+2014 in any committed markdown, no forbidden paths.
- Verdict is actionable: a reader can decide go/no-go from the report alone.

## Risks

- No API key in the environment: fall back to delegation mode; the report then measures only the deterministic layer and says so.
- Interactive-only config would block headless use: mitigation is the documented env-var path; if that also fails, that itself is a spike finding (no-go for agent integration).
- ocr may emit near-zero findings on a markdown repo: that is a valid result, record it as the markdown-handling verdict rather than forcing a code-repo detour.
- Vendor numbers may not reproduce: out of scope by design; report only local numbers.
