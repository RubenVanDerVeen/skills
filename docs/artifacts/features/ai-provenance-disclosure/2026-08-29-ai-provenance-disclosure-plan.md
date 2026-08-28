# AI-Provenance Disclosure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every project standardized with the `project-standardization` skill discloses its AI-involvement level in README.md and carries the research-paper link in STANDARDS.md, with retro-fit for existing projects.

**Architecture:** Template-stamping, matching the skill's existing pattern: a new snippet template is the content source, a new bootstrap sub-step (9.1) appends it to target READMEs with verification predicates, and the restructure flow picks it up for existing projects via those predicates. The paper URL lands in exactly two files.

**Tech Stack:** Markdown only. No build step, no runtime. Verification is PowerShell one-liners.

**Spec:** `docs/artifacts/features/ai-provenance-disclosure/2026-08-29-ai-provenance-disclosure-design.md`

## Global Constraints

- All work happens in `C:\Users\ruben\Projects\Tools\skills` on branch `feat/ai-provenance-disclosure` (create from `main` before Task 1).
- No em-dashes (U+2014) in any touched file. Commas, colons, parentheses, or hyphens only.
- The paper URL constant, verbatim: `https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project`
- The skills-repo link constant, verbatim: `https://github.com/RubenVanDerVeen/skills`
- The workflow deep link, verbatim: `https://github.com/RubenVanDerVeen/skills/blob/main/docs/workflows/workflow.md`
- Do not renumber the 12 bootstrap steps. The new step is sub-step 9.1 (pattern matches existing 8.1).
- Do not touch other README content in target projects; this repo's own README/AGENTS.md need no changes (catalog rule applies only to the SKILL.md Templates table).
- Conventional Commits per task; the repo's `commit-msg` hook is active (`.githooks/commit-msg`). Spec + plan ship as the docs-first branch commit per `/execute-plan` setup, before Task 1.
- Skill files live under `skills/rubens-project-standardization/` (folder keeps the legacy name on purpose; do not rename).

---

### Task 1: Snippet template + SKILL.md catalog row

**Files:**
- Create: `skills/rubens-project-standardization/templates/README-ai-assistance.md`
- Modify: `skills/rubens-project-standardization/SKILL.md:71-83` (Templates table)

Note: per `/execute-plan` setup, the orchestrator makes the docs-first branch commit (`docs: add plan and spec for ai-provenance-disclosure`) before this task; this commit covers only the template + table row.

**Interfaces:**
- Produces: the literal section content that Task 3's bootstrap step 9.1 copies into target READMEs, and the heading `## AI assistance` that all verification predicates grep for.

- [ ] **Step 1: Create the snippet template**

Write `skills/rubens-project-standardization/templates/README-ai-assistance.md` with exactly this content (9 lines, trailing newline):

```markdown
## AI assistance

- **AI involvement:** <level>
  <!-- human-written | AI-assisted | AI-driven | fully vibecoded -->
- **Method:** AI work is organized and professionally executed via a personal
  skill system: brainstorm > spec > plan > subagent execution > review.
  See the [skills repo](https://github.com/RubenVanDerVeen/skills) and
  [how the workflow is organized](https://github.com/RubenVanDerVeen/skills/blob/main/docs/workflows/workflow.md).
```

`<level>` stays as a literal placeholder in the template; the filling happens per target project at bootstrap.

- [ ] **Step 2: Add the Templates table row in SKILL.md**

In `skills/rubens-project-standardization/SKILL.md`, after the `templates/STANDARDS.md` row (line 81), insert:

```markdown
| `templates/README-ai-assistance.md` | AI-assistance section appended to the project README: involvement level + skills-repo and workflow links |
```

- [ ] **Step 3: Verify**

Run (from repo root):
`Test-Path skills/rubens-project-standardization/templates/README-ai-assistance.md`
Expected: `True`
`Select-String -Pattern 'RubenVanDerVeen/skills/blob/main/docs/workflows/workflow.md' skills/rubens-project-standardization/templates/README-ai-assistance.md`
Expected: 1 hit
`Select-String -Pattern 'README-ai-assistance' skills/rubens-project-standardization/SKILL.md`
Expected: 1 hit

- [ ] **Step 4: Commit**

```powershell
git add skills/rubens-project-standardization/templates/README-ai-assistance.md skills/rubens-project-standardization/SKILL.md
git commit -m "feat(skills): add README AI-assistance snippet template to project-standardization"
```

### Task 2: Research-paper URL in STANDARDS.md template and standards-stack reference

**Files:**
- Modify: `skills/rubens-project-standardization/templates/STANDARDS.md:188`
- Modify: `skills/rubens-project-standardization/references/standards-stack.md:3`

**Interfaces:**
- Produces: the paper URL in its two (and only two) homes. Task 3's STANDARDS.md predicate greps for `portfolio.rvdv-lab.nl`.

- [ ] **Step 1: Replace the rationale line in templates/STANDARDS.md**

Replace line 188:

```markdown
- Full standards-stack rationale: `docs/research/<paper>.pdf` <or omit if no paper exists>.
```

with:

```markdown
- Full standards-stack rationale: research paper <https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project> (local copy at `docs/research/<paper>.pdf` when present).
```

- [ ] **Step 2: Add the URL to the citation in references/standards-stack.md**

In line 3, replace:

```markdown
The full justification: with citations and design-decision history: lives in the research paper `Project standaarden pakket voor het IDP-project` (v1.0, Ruben van der Veen, 2026-05-11).
```

with:

```markdown
The full justification, with citations and design-decision history, lives in the research paper `Project standaarden pakket voor het IDP-project` (v1.0, Ruben van der Veen, 2026-05-11): <https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project>.
```

(This also fixes the double-colon typo in the same sentence; one sentence, one edit.)

- [ ] **Step 3: Verify the URL lives in exactly two files**

Run from repo root:
`(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern 'portfolio\.rvdv-lab\.nl').Path`
Expected: exactly the two paths from this task (plus any docs/artifacts spec/plan files mentioning it; those are fine, they are process documents, not shipped skill files). The two skill files must both appear.

- [ ] **Step 4: Commit**

```powershell
git add skills/rubens-project-standardization/templates/STANDARDS.md skills/rubens-project-standardization/references/standards-stack.md
git commit -m "feat(skills): default research-paper link in STANDARDS.md and standards-stack reference"
```

### Task 3: Bootstrap step 9.1 + STANDARDS.md predicate

**Files:**
- Modify: `skills/rubens-project-standardization/references/bootstrap.md:33` (insert after step 9 block, before step 10)
- Modify: `skills/rubens-project-standardization/references/bootstrap.md:33` (extend step 9's Verification)
- Modify: `skills/rubens-project-standardization/SKILL.md:58` (bootstrap summary line)

**Interfaces:**
- Consumes: `templates/README-ai-assistance.md` from Task 1; the URL predicate from Task 2's grep.
- Produces: bootstrap step 9.1 with runnable predicates; the restructure flow's verify phase re-runs these predicates on existing projects (retro-fit mechanism, no extra code needed).

- [ ] **Step 1: Extend step 9's Verification in bootstrap.md**

In `references/bootstrap.md`, step 9's Verification line currently ends with:

```markdown
    - Verification: `Test-Path STANDARDS.md` returns True AND no data row in the standards table has a blank or `?` cell in the yes/no column (column 2). The header row contains `Applied here?` with a literal `?`; skip the first two lines (header + separator) so the header is not flagged. Runnable: `(Get-Content STANDARDS.md | Select-String -Pattern '^\|' | Select-Object -Skip 2 | ForEach-Object { ($_.Line -split '\|')[2].Trim() } | Where-Object { $_ -in @('', '?') }).Count -eq 0`.
```

Append one more sentence to that same line (after `-eq 0`.):

```markdown
AND `Select-String -Pattern 'portfolio\.rvdv-lab\.nl' STANDARDS.md` returns at least one hit.
```

- [ ] **Step 2: Insert sub-step 9.1 after the step 9 block**

Insert a new block between step 9's Verification line and step 10, exactly:

```markdown
9.1. **Add the AI assistance section to README.md** (all tiers, always): append the `## AI assistance` section from `templates/README-ai-assistance.md` to the project's README.md. If README.md does not exist, create a minimal one: `# <Project Name>`, blank line, then the section. Fill `<level>` with the user, vocabulary: `human-written` (little or no AI generation), `AI-assisted` (human writes the majority, AI drafts parts), `AI-driven` (AI generates most of the output, human directs and reviews everything), `fully vibecoded` (AI generated, light human review). When the heading already exists, keep the current level and only repair missing or stale links; never touch other README content.
    - Verification: `Select-String -Pattern '^## AI assistance' README.md` returns at least one hit AND `Select-String -Pattern 'RubenVanDerVeen/skills' README.md` returns at least one hit.
```

- [ ] **Step 3: Update the bootstrap summary line in SKILL.md**

In `SKILL.md` line 58, replace:

```markdown
| `references/bootstrap.md` | The 12-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS → commit hook → graphify → verify) |
```

with:

```markdown
| `references/bootstrap.md` | The 12-step bootstrap checklist (triage → AGENTS.md → `.agents/` → artifacts → memory → CHANGELOG → STANDARDS + README AI section → commit hook → graphify → verify) |
```

- [ ] **Step 4: Verify**

Run from repo root:
`Select-String -Pattern '^9\.1\.' skills/rubens-project-standardization/references/bootstrap.md`
Expected: 1 hit
`Select-String -Pattern 'portfolio\.rvdv-lab' skills/rubens-project-standardization/references/bootstrap.md`
Expected: 1 hit
`Select-String -Pattern 'README AI section' skills/rubens-project-standardization/SKILL.md`
Expected: 1 hit
Count check: `(Select-String -Pattern '^\d+\.' skills/rubens-project-standardization/references/bootstrap.md).Count`
Expected: 12 (sub-steps 8.1/9.1 use `N.1` so they must not match `^\d+\.`; if the count is not 12, the step numbering got broken).

- [ ] **Step 5: Commit**

```powershell
git add skills/rubens-project-standardization/references/bootstrap.md skills/rubens-project-standardization/SKILL.md
git commit -m "feat(skills): bootstrap step 9.1 stamps AI-assistance section into README"
```

### Task 4: Tier references expect the section

**Files:**
- Modify: `skills/rubens-project-standardization/references/small.md:14`
- Modify: `skills/rubens-project-standardization/references/medium.md:16`
- Modify: `skills/rubens-project-standardization/references/large.md:11`

**Interfaces:**
- Consumes: the `## AI assistance` heading from Task 1.
- Produces: tier layout trees that name the section, so the restructure flow's explore phase treats a missing README section as a gap.

- [ ] **Step 1: Update the three layout-tree comments**

`references/small.md` line 14, replace:

```markdown
├── README.md                  ← user-facing
```

with:

```markdown
├── README.md                  ← user-facing, carries the AI assistance section
```

`references/medium.md` line 16, replace:

```markdown
├── README.md                  ← user-facing
```

with:

```markdown
├── README.md                  ← user-facing, carries the AI assistance section
```

`references/large.md` line 11, replace:

```markdown
├── README.md                          ← user-facing, English, references standards stack
```

with:

```markdown
├── README.md                          ← user-facing, English, references standards stack, carries the AI assistance section
```

(Other README.md occurrences in those files are example trees or prose; leave them.)

- [ ] **Step 2: Verify**

Run from repo root:
`Select-String -Pattern 'carries the AI assistance section' skills/rubens-project-standardization/references/small.md, skills/rubens-project-standardization/references/medium.md, skills/rubens-project-standardization/references/large.md`
Expected: exactly 1 hit per file (small also has later example trees at lines 62/79 that must stay untouched; if they matched too, the edit hit the wrong line).

- [ ] **Step 3: Commit**

```powershell
git add skills/rubens-project-standardization/references/small.md skills/rubens-project-standardization/references/medium.md skills/rubens-project-standardization/references/large.md
git commit -m "docs(skills): note README AI-assistance section in tier layout trees"
```

### Task 5: End-to-end smoke test of step 9.1 + final sweep

**Files:**
- No repo files modified. Scratch work in `C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke\` (delete after).

**Interfaces:**
- Consumes: everything from Tasks 1-4.

- [ ] **Step 1: Simulate step 9.1 on a project without a README**

```powershell
$d = 'C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke'; New-Item -ItemType Directory -Force -Path $d | Out-Null; Set-Content -Path "$d\README.md" -Value "# Smoke Project`n"; Add-Content -Path "$d\README.md" -Value (Get-Content -Raw 'skills/rubens-project-standardization/templates/README-ai-assistance.md')
```

- [ ] **Step 2: Run the step 9.1 predicates against the scratch project**

```powershell
Select-String -Pattern '^## AI assistance' 'C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke\README.md'; Select-String -Pattern 'RubenVanDerVeen/skills' 'C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke\README.md'
```

Expected: both return at least one hit. If either fails, the template content and the predicates disagree (fix the template, not the predicate).

- [ ] **Step 3: Clean up scratch dir**

```powershell
Remove-Item -Recurse -Force 'C:\Users\ruben\AppData\Local\Temp\opencode\ai-provenance-smoke'
```

- [ ] **Step 4: Repo-wide em-dash sweep**

Run from repo root:
`(Get-ChildItem -Recurse -Include *.md | Select-String -Pattern ([char]0x2014))`
Expected: empty output. Any hit in a file this feature touched is a blocker.

- [ ] **Step 5: Catalog red-flag check (repo rule)**

Run from repo root:
`Select-String -Pattern 'README-ai-assistance' skills/rubens-project-standardization/SKILL.md; git status --short`
Expected: 1 hit (Templates table row). `git status` clean except untracked scratch (none should remain). The skill needs no README.md/AGENTS.md catalog rows at repo level: it modifies an existing skill, and repo catalogs list skills, not templates.

- [ ] **Step 6: No commit**

No files changed in this task; nothing to commit. Report results in the execution report.

---

## Self-Review (completed during planning)

1. **Spec coverage:** D1/D3 (README section + links) → Tasks 1, 3, 4. D2 (vocabulary) → Task 1 template comment + Task 3 step 9.1 text. D4 (paper URL, two homes) → Task 2. Retro-fit → Task 3 predicates (restructure flow re-runs bootstrap predicates by existing design). Verification sweep → Task 5. No gaps.
2. **Placeholder scan:** the only placeholder is `<level>`, intentional per spec; `<Project Name>` appears only inside instruction text describing what an agent writes into a target project, not in shipped template content. No TODO/TBD.
3. **Consistency:** heading `## AI assistance`, grep patterns `'^## AI assistance'` and `'RubenVanDerVeen/skills'`, and the URL constants are identical across spec, template, and predicates.
