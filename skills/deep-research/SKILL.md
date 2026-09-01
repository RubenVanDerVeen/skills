---
name: deep-research
description: Use when the user wants end-to-end research on a topic for writing: paper, thesis, literature review, state-of-the-art summary, dossier, or brainstorm. Triggers: 'research X', 'paper on Y', 'literature review', 'investigate', 'synthesize', 'dossier', 'state of the art', 'what do we know about'. Produces a multi-stream dossier (arxiv + web + own vault) with citations, then hands off to brainstorm or Typst draft. Hermes research profile; load `artifacts` + `research-output-conventions` in the same turn.
---

# Deep Research Workflow

## Overview

The core skill of the research profile. Turns a fuzzy question into a durable research artifact, then optionally hands it off to Typst for paper drafting.

This is **not a single search query**. It is a three-phase pipeline that the agent drives end-to-end, with the user in the loop only at intake and at the final brainstorm/draft handoff.

## When To Use This Skill

**Prerequisite**: this skill assumes the `research` Hermes profile is already set up with its own Telegram bot, isolated memory, and DeepSeek as the default model. If you are NOT running in the `research` profile (i.e. you got loaded in the `default` profile by mistake), say so and ask the user to message the research bot instead, OR load the `hermes-multi-profile` skill to set it up. The full profile setup recipe (s6 HOME override, API server port, Telegram config schema, Discord token bleed) is in that skill - do not improvise.

Use this skill when the user:
- Asks to "research X" / "investigate Y" / "what do we know about Z"
- Wants a literature review or state-of-the-art summary
- Is starting a paper, thesis, blog post, or report
- Wants to brainstorm ideas grounded in real sources
- Says "give me a dossier" / "make me a research brief" / "I need sources for…"
- Wants the existing `research-paper-writing` skill but for a *new* topic, not an existing codebase

Skip this skill for:
- Quick factual questions (just answer them)
- Coding tasks (use `subagent-driven-development`)
- File ops, todos, calendar, etc. (use the underlying tools directly)

## Co-Trigger Skills - Load These At The Same Time

This skill owns the 4-phase pipeline. It does **not** own the per-session pointer or the source-provenance file, and it does **not** own the canonical file layout. **Before running this pipeline, also load these two skills in the same turn:**

- `artifacts` - owns `/mnt/nas/workspace/artifacts/YYYY/MM/<session_id>/SUMMARY.md` and `sources.json`. MANDATORY.
- `research-output-conventions` - owns the canonical citation grammar, the per-source provenance rules, and the subagent-delegation patterns used by `deep-research`.

**Loading order (mandatory, all in the same turn as the first `skill_view('deep-research')`):**

```python
skill_view(name='deep-research')              # this skill (pipeline)
skill_view(name='artifacts')                  # SUMMARY.md + sources.json at /mnt/nas/workspace/artifacts/
skill_view(name='research-output-conventions')  # citation grammar + provenance rules
```

If you only have the `research-skill-load-order` skill available, load that - it lists these three and explains the failure mode. Do NOT start phase 1 (intake) until all three are loaded. Do NOT defer `artifacts` to "after the dossier is written" - its job is to write the per-session pointer, which must exist before the dossier is referenced anywhere.

**Failure mode this prevents (verified 2026-06-12, car-photo-spots dossier + 2026-06-11 improving-research-methods + 2026-06-15 llm-subscription-plans-2026):** the agent loads `deep-research`, follows the older pipeline pattern from memory, writes the dossier without `SUMMARY.md` and a misfiled `sources.json`, and only fixes it when the user asks "and `artifacts` applied?" - fully avoidable by loading all three skills at the start.

## Core Philosophy

1. **A dossier is the deliverable.** The output of every research request is a real file the user keeps and reuses - not a chat reply that vanishes. Default location: `/mnt/nas/notes/research/dossiers/<dossier-name>/dossier.md` (the dossier-name is kebab-case, e.g. `e-ink-tablet-for-papers-dossier`), plus a `sources/` folder next to it for raw extracts. The dossier dir itself holds plan, stream summaries, optional self-pass files, and the dossier; the artifacts skill owns the separate per-session pointer at `/mnt/nas/workspace/artifacts/YYYY/MM/<session_id>/SUMMARY.md`.
2. **Parallel > sequential.** Three independent research streams (academic / web / personal vault) run in parallel via `delegate_task`. This is 3x faster and 3x broader than serial search.
3. **Citations are non-negotiable.** Every claim in the dossier links to a source file in `sources/` or an arxiv ID / URL. No floating claims. If a claim can't be sourced, mark it `[UNVERIFIED]` explicitly.
4. **Intake before work.** Don't start gathering until the user has confirmed: scope, depth, target output, and deadline (if any). The intake is short - 4 questions - but it shapes the whole pipeline.
5. **The user is the editor, the agent is the researcher.** Deliver drafts, not questions. But always expose the source pile so the user can correct, add, or remove sources.

## Pitfall - Default write path is `/mnt/nas/notes/research/`, never `/opt/data/home/research/` (verified 2026-06-27)

The system prompt's `cwd` defaults to `/opt/data/home/research/`, which is **scratch space**, not the canonical research vault. Dossier content always goes to `/mnt/nas/notes/research/dossiers/<slug>/...`. See `research-output-conventions` SKILL.md top-of-file pitfall for the rule + embedded fix.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1 - INTAKE (synchronous, ~2 min)                      │
│  Topic, scope, depth, target output, deadline                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2 - PARALLEL GATHER (~3-15 min)                       │
│  Stream A: arxiv + academic  (use arxiv skill)               │
│  Stream B: web + blogs       (use blogwatcher + web_search)  │
│  Stream C: own vault + local PDFs (use search_files + obsidian)│
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3 - SYNTHESIS + DOSSIER (synchronous, ~3-5 min)       │
│  Write dossier.md with claims, sources, gaps, outline        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4 - HANDOFF (user chooses)                            │
│  /brainstorm     → Socratic dialogue on the dossier          │
│  /draft-typst    → load typst-pro and start the paper        │
│  /more-research  → re-gather on a specific gap               │
│  /export         → copy dossier to Obsidian / share link     │
└─────────────────────────────────────────────────────────────┘
```

## PHASE 1 - Intake

When the user asks for research, do **not** start gathering. Run this intake first. If the user is impatient and says "just do it", ask only the two most critical questions (topic + target output) and use sensible defaults for the rest.

**Step 0 (mandatory, before intake questions):** If you have not already loaded `artifacts` and `research-output-conventions` in this turn, load them NOW via `skill_view(name=...)`. Do not proceed to intake until both are loaded. `artifacts` will be writing the per-session pointer; if it isn't loaded, the dossier will be retrofitted and the user will notice (verified 2026-06-12, car-photo-spots dossier + 2026-06-15 llm-subscription-plans-2026). If those skills are not available in this profile, load `research-skill-load-order` instead - it lists them and explains the failure mode.

**Intake template (use `clarify` with 4 multi-choice questions, or just ask inline):**

1. **Topic & scope** - what specifically? (free text)
2. **Depth** -
   - *Quick scan* (3-5 sources, 1-page dossier, 5 min)
   - *Standard* (10-20 sources, 3-5 page dossier, 15 min) ← default
   - *Deep* (30+ sources, comprehensive dossier, 30+ min)
3. **Target output** -
   - *Dossier only* (markdown file)
   - *Dossier + brainstorm session* (then we talk through it)
   - *Dossier + Typst paper draft* (then `typst-pro` takes over)
4. **Deadline & context** - when is this for? (paper, blog, IDP project, work, just curious)

Defaults if the user skips: depth=standard, target=dossier+brainstorm, no deadline.

**After intake**, write a one-paragraph research plan to `/mnt/nas/notes/research/dossiers/<dossier-name>/_plan.md` so the user can see the direction before phase 2 starts. The dossier-name is derived from the topic (kebab-case, English, max 5 words).

## PHASE 2 - Parallel Gather

Spawn three subagents via `delegate_task` (parallel, `tasks=[...]` shape). Each subagent has a focused goal and a tight scope to avoid overlap.

> **GATEWAY WORKAROUND (2026-06, until async re-entry is fixed):** background
> subagent re-entry is currently broken - a turn that ENDS after dispatch is
> never resumed, so the dossier never gets written. After dispatching the
> streams (still in parallel, in one delegate_task call), DO NOT end your
> turn. Stay in the loop and WAIT for ALL streams to finish, then synthesize.
> Ignore the tool's "do not wait or poll - just continue" note; on this
> gateway it causes a permanent stall.

### Stream A - Academic / arxiv (delegation)

Goal: find peer-reviewed and preprint sources, extract key claims, return a structured list.

Prompt template (passed via `delegate_task`):
```
You are the academic-stream research agent. Topic: <TOPIC>. Scope: <SCOPE>.
Use the MCP tools (mcp_arxiv_*, mcp_openalex_*, mcp_semantic_scholar_*) to find papers.
Prefer OpenAlex for broad coverage (270M+ works across journals/books/patents),
arXiv MCP for arxiv-specific depth,
and Semantic Scholar for citation counts, author profiles, and recommendations.
Find 5-15 relevant sources from the last 5 years (older only if foundational).
For each paper, capture: arxiv_id, title, authors, year, abstract, 2-3 key claims relevant to our topic, and a 1-line "why it matters" note.

**Citation-graph traversal step (added 2026-08-02, deep-research-pipeline-2026 dossier):**
For each top-3 paper, also fetch the forward citation graph (papers citing it) via
mcp_openalex_openalex_search_entities with filters={"cites": "W..."} (OpenAlex ID for the work)
or via mcp_arxiv_citation_graph. Surface the 2-3 most-cited follow-up papers as additional
sources, they often cover the same claim from a different angle or refute it. Note in the
source note's "Citation graph" section which follow-ups you added and why.

Save individual paper notes to /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/sources/arxiv-<id>.md using the source note template (see references/source-note-template.md).
Also write /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/_stream-a-summary.md with the ranked list of papers and the 3-5 strongest claims backed by them.
Do NOT write to the main dossier - only the stream summary + source notes.
```

### Stream B - Web / industry / blogs (delegation)

Goal: find industry posts, blog analyses, conference talks, GitHub repos, and authoritative web pages.

Prompt template:
```
You are the web-stream research agent. Topic: <TOPIC>. Scope: <SCOPE>.
Use web_search + web_extract + the blogwatcher skill to find 5-15 high-quality non-academic sources: industry blogs, conference talks (YouTube transcripts via youtube-content), GitHub READMEs, well-known company engineering posts, established analyst reports.
Skip random SEO content. Prefer sources with named authors and real institutions.
For each source, capture: url, title, author, date, 2-3 key claims, 1-line "why it matters".
Save individual notes to /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/sources/web-<slug>.md.
Also write /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/_stream-b-summary.md with the ranked list and strongest claims.
```

### Stream C - Own vault / local PDFs / prior projects (delegation)

Goal: leverage what the user already has. Search Obsidian, Nextcloud notes, local PDF libraries, prior Hermes session_search.

Prompt template:
```
You are the local-stream research agent. Topic: <TOPIC>. Scope: <SCOPE>.
Search the user's existing knowledge using three methods:
1. RAG pipeline: run `python3 /mnt/nas/ruben-projects/Hermes/research/rag/query.py query "<topic>" --top-k 10 --show-paths`
2. Obsidian vault (use the obsidian skill)
3. Past Hermes sessions (use session_search)
Find 3-8 existing notes / papers / discussions that are relevant. The user is more likely to trust a claim if they remember writing about it themselves.
For each match, capture: source path, title, date, 1-2 relevant excerpts, 1-line "why it matters" (especially "connects to <what>").
Save to /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/sources/local-<slug>.md and write /mnt/nas/notes/research/dossiers/<DOSSIER_NAME>/_stream-c-summary.md.
```

### Why three streams and not one big agent

- Each subagent has tighter context, so it actually finishes the task
- They can run truly in parallel
- The dossier phase gets three pre-organized summaries it can weave together
- Easier to debug a weak stream

## PHASE 2.5 - Compressed Synthesis Brief (RECOMMENDED for standard+ depth)

> **Added 2026-08-02 (deep-research-pipeline-2026 dossier).** Phase 2.5 + Phase 2.6 together add ~1 extra LLM call each to the pipeline. Recommended for `depth=standard` and `depth=deep`; skip for `depth=quick` to save the round-trip. **Why:** LangChain's context-engineering lesson ([web:langchain-thinking-about-frameworks] "the hard part is ensuring the LLM has the right context at each step"): Phase 3 reads a 1-page brief instead of 3 stream summaries + 54 raw source notes, which is what the literature says is the lever for scaling DR. Anthropic's separate Citation Agent role (see Phase 2.6) is the other half of this pattern.

After all three streams finish (Phase 2), the **parent session** runs a short LLM call that takes:

- The three `_stream-{a,b,c}-summary.md` files
- The top 5 source notes from each stream (read by relevance, not exhaustively)

…and writes `_synthesis-brief.md` to the dossier dir with this structure:

```markdown
# Synthesis Brief: <dossier-name>

## Ranked Claims (load-bearing first)
1. **<claim>**: supported by [arxiv:xxxx] [web:slug] [local:slug]. Confidence: high/medium/low.
   - Why it matters: <1 sentence>
   - Counter-evidence: <if any>
2. ...

## Cross-Source Conflicts
- <claim X>: stream A says Y, stream B says Z. The brief picks Y because <reason>.
- ...

## Gaps the streams left open
- <what no source covered>
- <what 2+ sources disagreed on>
- ...

## Candidate Outline
1. <section> - hook: <claim N>
2. <section> - strongest claims section-by-section
3. ...

## Stream Convergence Note
- <1 line: did A/B/C converge on the headline, or diverge?>
```

The brief is the input to Phase 3 (parent reads brief, not raw streams) and the input to Phase 2.6 (Citation Agent checks brief claims against source notes).

**Skip Phase 2.5 only if:** (a) `depth=quick`, (b) the streams' summaries already converge so hard that re-summarizing is redundant (rare; the brief is usually sharper than the concatenation), or (c) the parent session is short on context budget and the streams each returned <5 source notes.

## PHASE 2.6 - Citation Agent Pass (RECOMMENDED for standard+ depth)

> **Added 2026-08-02 (deep-research-pipeline-2026 dossier).** Anthropic's research architecture has three roles (Lead Researcher, Sub-agents, **Citation Agent**, a separate verifier that checks every claim against its source before anything reaches the user). Our pipeline currently lacks the third role; Phase 2.6 adds it. Recommended for standard+ depth when source quality matters.

After Phase 2.5 (the brief exists), the parent session runs a Citation Agent pass:

1. **Read** `_synthesis-brief.md` ranked claims.
2. **For each top-3 claim:** open the cited source note(s) and verify the claim is actually supported (or noted as paraphrased / extrapolated). If unsupported, mark `FAILED` and emit a one-line correction.
3. **For each citation in the brief:** check that the cited source file exists in `sources/` (no phantom citations).
4. **Write** `_citation-check.md` to the dossier dir:

```markdown
# Citation Check: <dossier-name>

## Summary
- Total claims checked: N
- Pass: N-pass
- Fail: N-fail (corrected inline)
- Phantom citations: 0

## Per-claim verdicts
1. **<claim>**: PASS / FAIL. Notes: <if FAIL, what the source actually says>.
2. ...

## Corrections Applied
- <if any claims needed correction; list before/after>
```

Phase 3 then incorporates any corrections before writing the dossier. If Citation Agent finds >30% failures, treat that as a flag in the dossier's Methodology Notes: the stream-gather had a quality problem worth investigating.

**Skip Phase 2.6 only if:** (a) `depth=quick`, (b) the dossier is for personal use and citation accuracy is not critical, or (c) the streams returned <10 sources total (manual spot-check is cheaper than the agent pass).

## PHASE 3 - Synthesis & Dossier

After all three streams finish (Phase 2) and the optional Phase 2.5 brief + Phase 2.6 citation-check have run, **synchronously** write the master dossier. **Read `_synthesis-brief.md` (Phase 2.5 output) and `_citation-check.md` (Phase 2.6 output) FIRST; fall back to `_stream-{a,b,c}-summary.md` and individual source notes only if those are absent** (quick-scan depth or Phase 2.5/2.6 skipped). Then:

1. Open `/mnt/nas/notes/research/dossiers/<dossier-name>/dossier.md`
2. Structure (use this exact layout - the user can paste it into a paper or read it standalone):

```markdown
# <Topic> - Research Dossier

**Date:** <ISO date>      **Dossier-name:** <dossier-name>      **Depth:** <quick|standard|deep>
**Sources:** <N> arxiv / <N> web / <N> local      **Status:** draft | reviewed | final

## TL;DR
<3-5 sentences. The single most important takeaway + the 2-3 strongest supporting claims, each cited [arxiv:xxxx] or [web:slug].>

## The Question
<The original question, restated precisely.>

## Key Claims (ranked by strength)
1. **<claim>** - supported by [arxiv:xxxx], [web:slug]. Confidence: high/medium/low.
2. ...

## Open Questions & Gaps
- <what we couldn't find, what the sources disagreed on, what would need a primary source>

## Source Index
### Academic
- [arxiv:2401.xxxxx] Title - Authors, Year - why it matters
### Web
- [web:slug] Title - Author, Date - why it matters
### Local
- [local:slug] Path - date - why it matters

## Multi-Pass Synthesis
<REQUIRED for standard+ depth (see PHASE 3.5 above). Embed a digest of the 2-3
self-passes inline: what each lens found that the others missed, where they
disagreed, and what the synthesis-judge pass promoted to a load-bearing claim.
For quick-scan depth, mark this section as "skipped (quick-scan depth)" with a
one-line rationale. Cite the raw per-pass files (`_self-pass-{1,2,3}-*.md`) for
full content.>

## Suggested Paper / Writeup Outline
1. Introduction - hook: <claim 1>
2. Background - what the user already knows
3. State of the Art - the strongest claims section-by-section
4. ...
5. Open Problems - the gaps above

## Methodology Notes
<Three required blocks:>
<(1) How the research was done: which streams ran, any limits, any source quality flags.>
<(2) Cost / latency / model line (REQUIRED, see "Cost line" pitfall below):>
  - Tokens: <per-stream in/out, total>  Wall time: <per-stream, total>
  - Models: <subagent model(s) used per stream; parent synthesis model>
  - For budget projections: label any extrapolation explicitly
    (e.g. "extrapolated from per-token pricing, verify with one real session before committing").
<(3) Verifier + planner notes (only when Phase 2.5/2.6 ran, see patches below):
  - _synthesis-brief.md (Phase 2.5): <path, 1-line summary>
  - _citation-check.md (Phase 2.6): <path, pass/fail count, any failed claims>
```

3. Save it. Then **always** end the response with a short user-facing summary:
   - Path to dossier
   - Top 3 claims
   - "Next: /brainstorm, /draft-typst, /more-research, or /export?"

4. **Emit `/mnt/nas/workspace/artifacts/<session_id>/SUMMARY.md` AND `/mnt/nas/notes/research/dossiers/<dossier-name>/sources.json` + `/mnt/nas/workspace/artifacts/<session_id>/sources.json` in the SAME turn as the dossier write.** This is owned by `artifacts`; consult that skill for the schemas. The console reads these for clickable source provenance. If you skip this step here, it gets retrofitted later and the user will notice (verified 2026-06-12, car-photo-spots dossier + 2026-06-15 llm-subscription-plans-2026).

## PHASE 3.5 - Multi-Lens Self-Pass Pattern (DEFAULT for standard+ depth, opt-in for quick scan)

> **Default changed 2026-08-02 (deep-research-pipeline-2026 dossier).** Was
> `(OPTIONAL)`; now runs by default for `depth=standard` and `depth=deep`. For
> `depth=quick`, skip the multi-lens pass and use the basic Phase 3 single-shot
> synthesis. **Why:** the 2025-2026 deep-research literature (SciSage +32%
> citation F1, Agentic AutoSurvey 8.18 vs 4.77) and our own diffusion-policies-2025
> run both put the evaluator / reflector layer at the top of the ROI curve.
> Promotion from OPTIONAL to default is the single highest-confidence upgrade.

For `depth=standard` and `depth=deep`, add 2-3 sequential self-passes (running in the parent session,
not as subagents) with **deliberately different lenses**. This is most useful when:
- The topic is contentious or has strong commercial PR / vendor bias
- The user wants an opinionated deliverable, not a neutral summary
- The research will inform a deployment or product decision

### Pattern

After writing the basic dossier, do N additional passes (N=2 or 3, not more) where each
pass reads the source notes again through a different lens. Embed a digest of the
multi-pass content inline in the dossier as a "Multi-Pass Synthesis" section. Save the
Save the raw per-pass files as `/mnt/nas/notes/research/dossiers/<dossier-name>/_self-pass-{1,2,3}-<lens-name>.md` (leading
underscore marks them as supporting, the dossier is the canonical read).

### Lens options

- **strict-academic** - per-paper grades (A/B/C), reviewer-style pushback, methodological
  gaps, citation hygiene
- **industry-skeptical** - per-source grades with bias flagging, deployment-relevant
  claims, what NOT to put in front of an engineering team, a "CEO memo" deliverable
- **synthesis-judge** - cross-source conflict resolution, the most important claim no
  source made explicitly, honest gaps in the prior passes
- **counter-argument** - dedicated red-team pass: what would a hostile reviewer say?
- **scaling-or-bust** - does this approach scale? At what cost? With what failure modes?

### When NOT to use

- Quick scan depth (use the basic 3-stream pipeline)
- Topics where the source material is already adversarial (skepticism is baked in)
- The user explicitly wants a neutral summary

### Lens templates (copy from this skill's templates/ directory)

For each lens, copy the corresponding template into the dossier dir and fill it in:

| Lens | Template | Notes |
|------|----------|-------|
| `strict-academic` | `templates/self-pass-1-academic.md` | Per-paper grades, "Claims I would push back on", methodological gaps, reviewer summary. |
| `industry-skeptical` | `templates/self-pass-2-industry.md` | "Marketing load" vs "independent signal", CEO / end-user memo, what NOT to put in front of an engineering team. |
| `synthesis-judge` | `templates/self-pass-3-synthesis.md` | Cross-pass conflicts, ranked claim list with confidence levels, "what nobody said" / honest gaps. |

A worked example (the 2026-06 diffusion-policies A/B run) is in `references/multi-lens-diffusion-policies-example.md`. After writing the three passes and the dossier, run `scripts/verify-multi-lens.sh <dossier_dir>` to confirm the verification checklist at the bottom of this file is satisfied.

### File layout for multi-lens runs

```
/mnt/nas/notes/research/dossiers/<dossier-name>/
├── _plan.md
├── _stream-a-summary.md
├── _stream-b-summary.md
├── _stream-c-summary.md
├── _synthesis-brief.md             ← Phase 2.5 output (standard+ depth); brief that Phase 3 reads
├── _citation-check.md              ← Phase 2.6 output (standard+ depth); Citation Agent verdicts
├── _self-pass-1-academic.md        ← raw pass 1 (lens: academic)
├── _self-pass-2-industry.md         ← raw pass 2 (lens: industry-skeptical)
├── _self-pass-3-synthesis.md        ← raw pass 3 (lens: synthesis-judge)
├── _model-comparison.md             ← OPTIONAL: A/B model verdict (if the run was a model A/B)
├── dossier.md                       ← embeds "Multi-Pass Synthesis" section with digest
└── sources/
    ├── arxiv-2401.xxxxx.md
    ├── web-<slug>.md
    └── local-<slug>.md
```

**Critical layout rule:** self-pass files live in `/mnt/nas/notes/research/dossiers/<dossier-name>/_self-pass-*.md`,
**not** in `/mnt/nas/workspace/artifacts/<session_id>/`. The console reads `/mnt/nas/workspace/artifacts/<session_id>/`
for the per-session pointer; the human reads `/mnt/nas/notes/research/dossiers/<dossier-name>/` for the content.
Mixing them breaks both readers (verified 2026-06-07, diffusion-policies A/B run).

## PHASE 4 - Handoff

Listen for one of these commands (the user types it; this is the only phase where the user drives):

### `/brainstorm <question>`
Load the dossier, then run a Socratic brainstorm. Use the dossier's claims as anchors. Push back on weak claims. Ask "what would change your mind?" for each contested point. Always end with a new question or a "if we add X, the dossier updates to Y" suggestion.

### `/draft-typst [section]`
- If section is empty: draft a full paper skeleton in Typst from the dossier's suggested outline. Load `typst-pro` skill first.
- If section is given (e.g. "intro", "related work", "methodology"): draft just that section, then loop.
- Use `rubens-project-standardization` if the project context is one Ruben has worked on.
- Output goes to `/mnt/nas/notes/research/papers/<slug>/main.typ` plus assets.
- **Critical**: hand off cleanly - load `typst-pro`, write the file, then *stop and let the user steer*. The dossier is the source of truth, the user is the editor.

### `/more-research <gap>`
Spawn a new subagent to dig into one specific gap from the dossier's "Open Questions" section. Append results back into the same dossier with a dated changelog entry.

### `/export`
- Copy dossier to Obsidian vault (use `obsidian` skill, default folder: `Research/Dossiers/`)
- Or send a Telegram link / file
- Or save PDF via pandoc

## File Layout Convention

```
/mnt/nas/notes/research/
├── dossiers/
│   └── <dossier-name>/
│       ├── _plan.md
│       ├── _stream-a-summary.md
│       ├── _stream-b-summary.md
│       ├── _stream-c-summary.md
│       ├── _self-pass-1-<lens>.md     ← OPTIONAL, multi-lens runs (see PHASE 3.5)
│       ├── _self-pass-2-<lens>.md     ← OPTIONAL
│       ├── _self-pass-3-<lens>.md     ← OPTIONAL
│       ├── _model-comparison.md       ← OPTIONAL, when the run was a model A/B
│       ├── dossier.md                  ← canonical synthesis; embeds "Multi-Pass
│       │                                 Synthesis" digest when multi-lens was used
│       └── sources/
│           ├── arxiv-2401.xxxxx.md
│           ├── web-<slug>.md
│           └── local-<slug>.md
├── papers/
│   └── <slug>/
│       ├── main.typ
│       ├── refs.bib
│       └── assets/
└── templates/
    ├── dossier-template.md
    ├── source-note-template.md
    └── paper-skeleton.typ

/mnt/nas/workspace/artifacts/                       ← OWNED BY `artifacts` SKILL
└── YYYY/MM/<session_id>/                          ← console reads this for per-conversation page
    ├── SUMMARY.md                                  ← only pointer file in here
    └── sources.json
```

**Producer/consumer split** (verified 2026-06-07, diffusion-policies A/B run):

- `/mnt/nas/notes/research/dossiers/<dossier-name>/` is for **content** - the dossier, sources, raw self-pass files, plan.
  The human reader goes here. Owned by this skill.
- `/mnt/nas/workspace/artifacts/<session_id>/` is for the **per-session pointer** - one `SUMMARY.md` that
  tells the console which dossier(s) this session produced. Owned by the
  `artifacts` skill. Nothing else goes here.

If you find yourself writing self-pass files, model-comparison files, or any substantial
research content into `/mnt/nas/workspace/artifacts/<session_id>/`, stop and write them in
`/mnt/nas/notes/research/dossiers/<dossier-name>/` with a `_` prefix instead.

Create the skeleton directory on first run if missing. Use `terminal` to mkdir.

## Pitfalls

- **Don't run phase 2 before intake.** "Research X" with no scope = wasted arxiv calls. Always intake first, even if the user says "just go".
- **GATEWAY: wait for background subagents in-turn.** The `delegate_task` tool description says "do not wait or poll - just continue". On this gateway that advice is WRONG (2026-06, async re-entry broken): a turn that ends after dispatch never gets the result back, so the dossier stalls. Dispatch the streams in parallel, then keep the turn open and synthesize once all results are in. See PHASE 2 GATEWAY WORKAROUND. (DISABLED 2026-06 - see GATEWAY WORKAROUND in PHASE 2; you MUST wait in-turn until re-entry is fixed.)
- **If the user is actively waiting, don't dispatch in parallel - go inline (verified 2026-06-27, cheap-claude-orchestrator dossier).** The parallel-dispatch pattern works when the user can leave the session and come back (e.g. cron-style background work, "let me know when it's done"). When the user is sitting at Telegram waiting for the dossier, the "wait in-turn" rule above is necessary but NOT sufficient: short tick messages between subagent completions ("still waiting on subagents 1/2/3") read to the user as a closed loop, and a closed loop without end = frustration ("the stream is not left open", "you just did end the turn"). The fix: when the user is actively waiting, **cancel the parallel split and run all four phases inline in one go.** Inline work costs more tokens per turn but the dossier lands in a single reply, the stream stays visibly alive via the tool calls themselves, and the user can interject corrections between tool results. Use parallel only when the user can disengage (cron, "background me when ready", "I don't need the answer this hour"). For the three operating models and the failure-mode catalog, see `references/stream-management-with-async-subagents.md`.
- **Don't write the dossier from the summaries alone.** Always read at least the top 3 source notes from each stream before synthesizing. Summaries compress nuance.
- **Cite by source ID, not by URL in body text.** `[arxiv:2401.xxxxx]` is more stable than `https://arxiv.org/abs/...` mid-sentence. URLs go in the source index.
- **Skip Stream C if the vault is empty.** Don't fabricate "local sources" - just log `Stream C: skipped (no vault)`.
- **For very narrow topics, drop Stream B and double-up on arxiv.** E.g. "what's the latest on GRPO loss variants" - the academic stream is enough. Default is 3 streams; override per topic.
- **The dossier is a living document.** When the user adds a source or corrects a claim in `/brainstorm`, patch the dossier in place - never overwrite.
- **Don't load `typst-pro` until `/draft-typst` is invoked.** Loading it during phase 2-3 wastes context.
- **Mind the budget.** Standard depth on a 3-stream pipeline can be 30+ LLM calls. Default to standard, not deep.
- **Multi-lens self-pass files go in `/mnt/nas/notes/research/dossiers/<dossier-name>/_self-pass-*.md`, NOT in `/mnt/nas/workspace/artifacts/<session_id>/`** (verified 2026-06-07, diffusion-policies A/B run). The `artifacts` skill owns `/mnt/nas/workspace/artifacts/<session_id>/` and only the `SUMMARY.md` lives there. If you put self-pass files in the artifacts dir, the console and the human both lose. The dossier's "Multi-Pass Synthesis" section embeds a digest inline; the raw files are kept next to the dossier for transparency.
- **Default write path is `/mnt/nas/notes/research/`, never `/opt/data/home/research/`** (verified 2026-06-27). See top-of-file pitfall.
- **Cost projections from per-token pricing are extrapolations, not facts - flag them as such** (verified 2026-06-27, cheap-claude-orchestrator dossier). When a dossier estimates monthly cost for a subscription plan (e.g. "opencode Go at $10/mo gives 9,250 Kimi requests, so Scenario B = ~$9/mo"), the math combines (a) per-token list pricing from vendor docs, (b) per-request token counts the agent guessed, and (c) usage frequency the user described in vague terms ("3-5 heavy sessions/month"). All three legs are uncertain, and they multiply. If the dossier presents a point estimate ("$9/mo") and the user later reveals real usage data showing 10x more spend per session, the recommendation has to be retracted. The fix: in any cost-projection section, present a **range with explicit assumptions** ("$9-30/mo depending on session length, assuming 1-2K tokens/request and 5-15 sessions/month"), label the estimate `extrapolated - verify with one real session before committing`, and recommend the user run a single push session against the new vendor before the dossier's recommendation is acted on. Concrete trigger: any dossier section that says "saves X EUR/month" must either (a) cite a real bill, or (b) be in the extrapolated-range format. A "saves 342 EUR/yr" line with no error bar is a flag that the math has been over-claimed.
- **Cost / latency / model line in Methodology Notes is REQUIRED (verified 2026-08-02, deep-research-pipeline-2026 dossier).** Three numbers every dossier should record: (a) tokens in/out per stream and total, (b) wall time per stream and total, (c) the model used per stream and for parent synthesis. Without these, future-you can't budget-match an A/B against an alternative pipeline (LangChain ODR, Anthropic Research, etc.) and the dossier becomes unfalsifiable. For budget projections from per-token pricing: present a *range* with explicit assumptions ("$9-30/mo depending on session length, assuming 1-2K tokens/request and 5-15 sessions/month"), label as `extrapolated - verify with one real session before committing`, and recommend the user run a single push session against the new path before the recommendation is acted on. A point estimate without error bars ("saves 342 EUR/yr") is a flag the math has been over-claimed.
- **Production DR agent counts are 1-10, never 25+; the "many agents" press impression is marketing or runaway recursion (verified 2026-08-02, deep-research-pipeline-2026 dossier).** Documented counts: OpenAI/Gemini/Perplexity/HF smolagents are single-agent; Anthropic Research is 1 lead + 3-5 default, **10+ for "complex research problems"** (their own explicit tier) + 1 Citation Agent; LangChain ODR is supervisor + bounded N sub-agents; Manus is 3 roles. Anthropic explicitly treats spawning ~50 sub-agents as a failure mode they guard-railed against. If you ever see claims of 25+ agents in a Claude/Manus session, it's likely the runaway-recursion bug (GitHub issue anthropics/claude-code#68110: sub-agents with `Agent` tool access spawn children with no depth/count limit; useful research complete in 3-4, rest redundant, ~1.5M tokens burned). The 2026 agent-scaling literature (SIMAS, Ringelmann, Agent Scaling via Diversity) finds an inverted-U / hard-ceiling with knee at ~4-8 agents: marginal value past that comes from role specialization, evaluator/reflector presence, and structured handoff, not headcount. **Conclusion:** don't chase 25 agents. Our 3-stream parallel gather + parent one-shot synthesis already matches the proven production pattern (LangChain ODR's "isolated sub-agents in research, single-shot write" is structurally identical).
- **Phase 2.5 / 2.6 add depth but cost ~1 extra LLM call each (verified 2026-08-02, deep-research-pipeline-2026 dossier).** Phase 2.5 = `_synthesis-brief.md` (compress 3 stream summaries + top 5 source notes per stream into ranked claims + conflicts + gaps; parent reads the brief, not raw streams, LangChain's context-engineering lesson). Phase 2.6 = Citation Agent pass (validate every claim against its source file post-gather, pre-synthesis; the third Anthropic role we don't have). Both are recommended for standard+ depth when stakes justify the ~2x synthesis-side token cost.

## Verification

After writing the dossier, run a quick self-check:
- [ ] All claims have at least one citation
- [ ] No `[UNVERIFIED]` claims in the TL;DR
- [ ] "Open Questions" is non-empty (if it's empty, you didn't look hard enough)
- [ ] Source Index has at least N entries (N = depth threshold)
- [ ] Suggested Outline has at least 3 sections
- [ ] For standard+ depth: `_synthesis-brief.md` exists (Phase 2.5) and `Multi-Pass Synthesis` section in dossier embeds the 2-3 self-pass digests (Phase 3.5 default since 2026-08-02)
- [ ] For standard+ depth: `_citation-check.md` exists (Phase 2.6); any FAIL claims were corrected in dossier before write
- [ ] Methodology Notes contains the cost / latency / model line (per-stream tokens, wall time, model used; extrapolations explicitly labeled)

If any check fails, fix the dossier before showing it to the user.
