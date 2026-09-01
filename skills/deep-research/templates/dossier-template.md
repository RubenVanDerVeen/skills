# <TOPIC> - Research Dossier

**Date:** <ISO_DATE>      **Slug:** <SLUG>      **Depth:** <quick|standard|deep>
**Sources:** <N_ARXIV> arxiv / <N_WEB> web / <N_LOCAL> local      **Status:** draft

## TL;DR

<3-5 sentences. The single most important takeaway + the 2-3 strongest supporting claims, each cited [arxiv:xxxx] or [web:slug].>

## The Question

<Restate the original research question precisely.>

## Key Claims (ranked by strength)

1. **<claim>** - supported by [arxiv:xxxx], [web:slug]. Confidence: high | medium | low.
   - Counter-evidence: <if any>
   - Open caveat: <if any>
2. ...

## Open Questions & Gaps

- <what we couldn't find, what the sources disagreed on, what would need a primary source>
- ...

## Source Index

### Academic
- [arxiv:XXXX.XXXXX] **Title** - Authors, Year - *why it matters*

### Web
- [web:slug] **Title** - Author, Date - *why it matters*

### Local
- [local:slug] **Path** - date - *why it matters*

## Suggested Paper / Writeup Outline

1. **Introduction** - hook: <claim 1>
2. **Background** - what the reader already needs to know
3. **State of the Art** - strongest claims, section by section
4. **Open Problems** - the gaps above
5. **Conclusion** - the one-sentence contribution

## Methodology Notes
<Three required blocks:>
<(1) How the research was done: which streams ran, any limits, any source quality flags.>
<(2) Cost / latency / model line (REQUIRED since 2026-08-02):>
  - Tokens: <per-stream in/out, total>  Wall time: <per-stream, total>
  - Models: <subagent model(s) used per stream; parent synthesis model>
  - For budget projections: label any extrapolation explicitly
    (e.g. "extrapolated from per-token pricing, verify with one real session before committing").
<(3) Verifier + planner notes (only when Phase 2.5/2.6 ran):
  - _synthesis-brief.md (Phase 2.5): <path, 1-line summary>
  - _citation-check.md (Phase 2.6): <path, pass/fail count, any failed claims>
