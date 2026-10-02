# academic-writing-pro: execution report

Date: 2026-10-02
Report path: `docs/artifacts/features/academic-writing-pro/2026-10-02-academic-writing-pro-report.md`
Branch: `feat/academic-writing-pro` (local only, not pushed)

## Summary

Shipped the `academic-writing-pro` skill: a two-layer academic soundness checker (stdlib-only Python lint script for deterministic surface checks, agent judgment pass for everything contextual) that also drafts academic text under the same rules. The skill is complete and cataloged: lean `SKILL.md` (43 lines, ~319 body words), four load-on-demand reference files carrying the FOCSI/quoting/sentence/IEEE rule banks, `/academic-check` as the explicit entry point, `lint-academic.py` (185 lines, Python 3 stdlib only, embedded self-test), and catalog rows in `README.md`, `AGENTS.md`, plus a `CHANGELOG.md` [Unreleased] bullet. All verification gates pass: `bin/skillctl check` (0 fail), script self-test, fixture check, sync smoke test. Spec components 1-8 all landed.

## Branch and commits

Base: `main`. Five commits, oldest first:

| Hash | Subject | One-liner |
|---|---|---|
| `53ce87d` | `feat(skills): add academic-writing-pro lint script` | `scripts/lint-academic.py` (then `lint_academic.py`), 10 deterministic rules, self-test |
| `3246d77` | `feat(skills): add academic-writing-pro references` | Four rule-bank files from ARS course notes, reformatted (no em-dashes) |
| `f90947d` | `feat(skills): add academic-writing-pro skill, command, catalogs` | SKILL.md + `commands/academic-check.md` + README/AGENTS rows, one bundle commit (hook P6) |
| `38a75c1` | `fix(skills): rename academic-writing-pro lint script to kebab-case` | Doc-standardizer quick-fix: `lint_academic.py` to `lint-academic.py`, SKILL.md reference updated |
| `89c0294` | `docs: add academic-writing-pro to CHANGELOG Unreleased` | Doc-standardizer quick-fix: [Unreleased] Added bullet (amended once for US spelling of "catalog") |

All commits carry `Co-Authored-By: minimax-coding-plan/MiniMax-M3` + `Agent-Role: executor`, except `89c0294` carries `Agent-Role: orchestrator`. One known inconsistency: `3246d77` uses the slug `MiniMax/MiniMax-M3`; a squash-merge normalizes it (see Recommendations).

## Files changed

Net diff vs `main`: 10 files, +387 lines, 0 deletions.

| File | Status | Lines |
|---|---|---|
| `skills/academic-writing-pro/SKILL.md` | new | 43 |
| `skills/academic-writing-pro/scripts/lint-academic.py` | new | 185 |
| `skills/academic-writing-pro/references/quoting-plagiarism.md` | new | 37 |
| `skills/academic-writing-pro/references/tone-terminology.md` | new | 44 |
| `skills/academic-writing-pro/references/sentences-paragraphs.md` | new | 43 |
| `skills/academic-writing-pro/references/ieee-citations.md` | new | 24 |
| `commands/academic-check.md` | new | 5 |
| `README.md` | modified | +1 (Skills table, first data row) |
| `AGENTS.md` | modified | +1 (Current skills table, first data row) |
| `CHANGELOG.md` | modified | +1 ([Unreleased] Added bullet) |

`opencode-install.md`: intentionally unchanged; its Verify section does not list skills by name.

## Verification evidence

All gates PASS on the committed tree. Outputs as run:

`bin/skillctl check`:

```text
0 fail. 3 pre-existing C7 warns (commands/full-cycle.md, commands/goal.md,
commands/iterate-skill.md not referenced by any SKILL.md).
C1 PASS (no em-dashes), C2-C5 PASS for academic-writing-pro, C6 PASS
(skill in both catalogs), C7 PASS (commands/academic-check.md referenced),
C8 PASS.
```

Script self-test:

```bash
$ python3 skills/academic-writing-pro/scripts/lint-academic.py --self-test
self-test OK
$ echo $?
0
```

Fixture check (known-violation text):

```bash
$ printf 'We don'\''t really know. It is important to note that the device "works well" under load!\n' > /tmp/opencode/acad-fixture.txt
$ python3 skills/academic-writing-pro/scripts/lint-academic.py /tmp/opencode/acad-fixture.txt
# findings include: focsi-formal (contraction, exclamation), focsi-impersonal (We),
# focsi-succinct (throat-clearing), focsi-formal casual-vocab (really),
# citation-missing ("works well" uncited)
$ echo $?
1
```

Expected rule ids all present, exit 1 (errors found), matching the spec's verification item 3.

Sync smoke test:

```text
bin/skillctl sync          -> 70 items synced, incl. skill folder (SKILL.md,
                              references/, scripts/) and commands/academic-check.md
                              to ~/.claude/skills/ and ~/.claude/commands/
bin/skillctl sync --check  -> no MISSING/STALE for academic-writing-pro
```

## Standardization review

Doc-standardizer (post-implementation, concurrent with code-standardizer):

- QUICK-FIX applied: script filename `lint_academic.py` violated kebab-case path convention; renamed to `lint-academic.py`, SKILL.md Check workflow reference updated. Commit `38a75c1`.
- QUICK-FIX applied: `CHANGELOG.md` was missing the [Unreleased] Added bullet. Commit `2249e90`, amended to `89c0294` (US spelling "catalog", 10:3 dominance in repo).
- RECOMMENDATION logged, not applied: five commits could squash to one logical change at merge; one trailer slug differs (`MiniMax/MiniMax-M3` in `3246d77` vs `minimax-coding-plan/MiniMax-M3` elsewhere). Squash-merge normalizes both.

Code-standardizer:

- CONDITIONAL QUICK-FIX waived by orchestrator: `pyproject.toml` with ruff for the Python script. Conflicts with AGENTS.md "Markdown only. No build step, no tooling, no runtime. Single exception: `bin/skillctl`". The script is stdlib-only skill content (same carve-out the spec's carried constraints use for skill-folder scripts), not repo tooling. Logged as accepted deviation.
- All other checks PASS.

## Documentation updates

- `README.md`: one row, `## Skills` table, first data row (joins the pro-family cluster per plan).
- `AGENTS.md`: one row, `## Current skills` table, first data row.
- `CHANGELOG.md`: [Unreleased] Added bullet (commit `89c0294`).
- `opencode-install.md`: no change needed (Verify section lists no skills by name; verified).
- This report; no choices-registry entry (see Choices below).

Catalog verification: folder name, frontmatter `name`, and both table entries all read `academic-writing-pro`; the row is the first data row in both tables, exactly as the plan specified.

## Choices

No `docs/artifacts/choices/` entry written. Judgment on each candidate:

- Lint-script-vs-judgment split: user-locked in the spec (Decision 1), not a new constraining choice.
- Ruff/pyproject waiver: application of the existing markdown-only rule (2026-09-29 stdctl decision territory), an explicit waive, not a new decision.
- Not squashing history: routine close-out choice, not registry-worthy.

## Dispatch log

| Task | Dispatch | Result |
|---|---|---|
| 1. Lint script | dispatched: executor + reviewer | PASS first try |
| 2. References (4 files) | dispatched: executor (+ reviewer on retry) | First attempt failed mid-output (files created, no commit; communication failure, not verification/review, so two-strike rule not engaged). Retry succeeded, byte-for-byte verified against plan content |
| 3. Skill bundle (SKILL.md, command, catalogs) | dispatched: executor + reviewer | PASS first try |
| 4. End-to-end verification | self-implemented: read-only gate (no files, no commits), run directly via orchestrator bash | All gates PASS |
| Doc-standardizer + code-standardizer | dispatched: concurrent post-implementation | Findings above; 2 quick-fixes applied, 1 waived, 1 recommendation |
| Quick-fix executor + reviewer | dispatched | PASS, plus one trivial follow-up amend (CHANGELOG spelling) |

## Defaults taken

- Trailing newline at EOF missing on 3 of 4 reference files: plan content was verbatim, so left as-is; cosmetic, not worth a fix commit.
- CHANGELOG bullet spelling defaulted to US "catalog" (10:3 dominance in repo); applied via amend `89c0294`.

## ponytail: deferrals

- `lint-academic.py` regex heuristics with a `# ponytail: regex heuristics; real parsing only if false positives hurt` ceiling comment in the file header. Upgrade path: real parsing only when false positives measurably hurt.
- 4-gram overlap check is O(n*m) token scanning: fine at document scale; revisit only if multi-document corpora go through `--against`.
- Three pre-existing C7 warns (`full-cycle`, `goal`, `iterate-skill` commands unreferenced by any SKILL.md): pre-date this feature, not addressed here.

## Unverified items

None. All spec verification items 1-6 have passing evidence above.

## Versioning

Unversioned/no bump: `AGENTS.md` declares no canonical version source; the [Unreleased] CHANGELOG bullet is the correct terminal state. No release cut.

## Follow-ups

- `[expand]` markers in `references/tone-terminology.md` (reporting-verb taxonomy, field terminology) await Ruben's research; tracked in the spec's Open items.
- Optional at merge: squash to normalize the one differing trailer slug and collapse the two quick-fix commits.
