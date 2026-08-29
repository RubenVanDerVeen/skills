# Design: AI-provenance disclosure in `project-standardization`

Date: 2026-08-29
Status: approved (interactive brainstorm session)
Scope: the `project-standardization` skill in this repo (`skills/rubens-project-standardization/`)

## Problem

Standardized projects carry no disclosure of how much of the work is AI-generated ("vibecoded"), no pointer to the skills repo that explains how AI work is organized, and no link to the research paper backing the standards stack. Readers (collaborators, graders, portfolio visitors) cannot tell what a project's AI involvement is or that the AI work follows a professional process.

## Requirements

1. Every project bootstrapped or restructured with the skill gets an AI-assistance disclosure in its README, including a fixed-vocabulary AI-involvement level.
2. The disclosure links to the skills repo and to the existing workflow explainer at `docs/workflows/workflow.md` in this repo.
3. The research-paper URL (`https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project`) becomes the default standards-rationale link in `STANDARDS.md` for standardized projects. The URL will change in the future; it must live in as few places as possible so a future swap is one edit plus a restructure pass.
4. Existing projects retro-fit via the normal restructure flow (template comparison + verification predicates). No manual per-project fix.

## Decisions

### D1: Disclosure lives in a README section, not a separate file (all tiers)

Options considered:

- Own root file (`AI-PROVENANCE.md`): survives README rewrites, trivial to verify, but invisible to actual readers and heavy for ~6 lines.
- Section in README: maximum visibility, no new file, matches the skill's placement doctrine ("human-facing declarations go in README.md; AGENTS.md is agent operating notes").
- Own file + pointer: worst of both.

Chosen: `## AI assistance` section in README.md. The skill currently never edits README, so this introduces a light README-editing mechanism (snippet template + append-or-create instruction + verification predicate).

### D2: Fixed level vocabulary, no percentage

Self-declared at bootstrap by the user. One word plus optional one-line note:

| Level | Meaning |
|---|---|
| `human-written` | Little or no AI generation; AI at most used for questions |
| `AI-assisted` | Human writes the majority; AI drafts parts |
| `AI-driven` | AI generates most of the output; human directs and reviews everything |
| `fully vibecoded` | AI generated; light human review |

Percentage estimates rejected: fake precision, drifts as the project evolves.

### D3: Workflow explanation stays in this repo, target projects link to it

Options considered: short block + link (chosen), per-project `docs/ai-workflow.md` (drifts, duplicated), landing doc in skills repo (already exists: `docs/workflows/workflow.md`). Target READMEs get 2-3 lines plus two links: repo root and the workflow.md blob URL on GitHub. Zero per-project duplication.

### D4: Paper URL defaults into `STANDARDS.md` template

Current placeholder line ("Full standards-stack rationale: `docs/research/<paper>.pdf` <or omit if no paper exists>") gains the portfolio URL as the default rationale link, keeping the local-PDF pointer as optional. The URL constant appears in exactly two places: `templates/STANDARDS.md` and `references/standards-stack.md` (which already cites the paper by title without a link).

## Changes

### 1. New snippet template `templates/README-ai-assistance.md`

```markdown
## AI assistance

- **AI involvement:** <level>
  <!-- human-written | AI-assisted | AI-driven | fully vibecoded -->
- **Method:** AI work is organized and professionally executed via a personal
  skill system: brainstorm > spec > plan > subagent execution > review.
  See the [skills repo](https://github.com/RubenVanDerVeen/skills) and
  [how the workflow is organized](https://github.com/RubenVanDerVeen/skills/blob/main/docs/workflows/workflow.md).
```

The agent fills `<level>` with the user at bootstrap (or leaves the current value untouched when refreshing an existing section).

### 2. `references/bootstrap.md`: new step + predicates

New step (after AGENTS.md scaffolding, before verification pass): append the `## AI assistance` section to README.md from the snippet template; if no README.md exists, create a minimal stub (`# <Project Name>` plus the section). Refresh the section if the heading exists but the links are missing or stale; never touch other README content.

Verification predicates (hard rule: every step has one):

- `Select-String -Pattern '^## AI assistance' README.md` hits
- `Select-String -Pattern 'RubenVanDerVeen/skills' README.md` hits
- `Select-String -Pattern 'portfolio.rvdv-lab.nl' STANDARDS.md` hits (checked when STANDARDS.md is part of the stamp)

The step text also carries the one-line-per-level vocabulary from D2 so the agent never needs another file to fill the template.

### 3. `templates/STANDARDS.md`: default rationale link

Replace the rationale line with:

```markdown
Full standards-stack rationale: research paper
<https://portfolio.rvdv-lab.nl/research.html?id=project-standaardenpakket-voor-het-idp-project>
(local copy at `docs/research/<paper>.pdf` when present).
```

### 4. `references/standards-stack.md`: URL next to the existing citation

The paper is already cited by title at the top of the file; add the URL to that citation. Second and final home of the constant.

### 5. Catalog sync in the skill

SKILL.md `## Templates` table gains the `README-ai-assistance.md` row. Tier references (`small.md`, `medium.md`, `large.md`) mention the README section in their layout/output lists so the restructure flow's template-comparison pass treats it as expected output.

## Retro-fit

Existing projects: restructure flow compares stamped output against current templates and re-runs verification predicates; a project whose README lacks the section or whose STANDARDS.md lacks the URL gets both added. No migration tooling beyond what exists.

## Out of scope

- No pointer in target projects' AGENTS.md (agents do not need the provenance level).
- No percentage or auto-computed metric.
- No per-project workflow explainer docs.
- No README templates beyond the snippet (full README scaffolding stays out).
- No changes to other skills or to this repo's own README/AGENTS.md beyond catalog requirements.

## Verification (per repo rules)

- No em-dashes in any touched file (`Select-String -Pattern ([char]0x2014)` returns empty).
- Snippet template matches this spec's block verbatim.
- Predicates in bootstrap.md are runnable PowerShell one-liners.
