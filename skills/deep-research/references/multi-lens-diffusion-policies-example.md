# Worked example: diffusion-policies-2025 dossier

**Date:** 2025-06-07
**Task:** A/B comparison of deepseek-v4-flash (subagent) vs MiniMax-M3 (synthesis) on a diffusion-policy research task
**Slug:** diffusion-policies-2025

This is the session that produced the multi-lens-synthesis skill. Use it as a worked example when the pattern is unfamiliar.

## What the three passes actually produced

### Pass 1 - strict-academic (`artifacts/self-pass-1-academic.md`)
- Read 5 of 11 academic papers in full (Chi 2023, DP3, DPPO, EquivDP, ScaleDP, ManiCM)
- Per-paper grades: A, A-, B+, B+, A-, A-, A, A-, A-, A, B
- "Claims I would push back on": four specific items, including the "46.9% improvement is the high end of the variance band" call
- Reviewer summary paragraph that would be sent to an editor
- Score: 7.2/10

### Pass 2 - industry-skeptical (`artifacts/self-pass-2-industry.md`)
- Read 1 web source in full (Penn π₀ eval)
- Per-source grades with explicit "marketing load" and "independent signal" columns
- Three claims to put in front of an engineering team: "don't believe the laundry-folding demo", "the dual-system architecture is real consensus", "synthetic data is the escape hatch but vendor-biased"
- CEO memo: "Diffusion policies are real and impressive in narrow settings. They are not yet a foundation for a general-purpose robot product in 2025."
- Score: 4.4/10

### Pass 3 - synthesis-judge (`artifacts/self-pass-3-synthesis.md`)
- Read all three stream summaries in full, plus the 6-7 source notes already covered in Pass 1/2
- 5 final claims ranked by strength with confidence levels
- 3 cross-pass conflicts explicitly resolved (46.9% headline, Levine as a source, action chunking as feature vs crutch)
- "The most important claim that NO source explicitly made": the field is preparing for a transition away from diffusion
- "The honest gaps in my own 3 passes" section
- Score: 7.9/10 on the research effort overall, 7.5/10 reliability on the final dossier

## The non-obvious outputs

These are the things that would not have appeared in a single-pass synthesis:

1. **The "46.9% is high end of variance band" call.** Single-pass synthesis tends to either cite the number or omit it. Multi-lens makes the meta-claim about the number's reliability a first-class output.

2. **The "corporate blogs as upper bound, Penn eval as deployed reality" rule.** Pass 2 made this a heuristic. Pass 3 elevated it to a ranking principle in the dossier's Methodology Notes.

3. **The "field trajectory" claim.** This was Pass 3's "claim no source made" - diffusion is maturing, flow matching is the successor, the field is in transition. Single-pass synthesis would have flattened this into "diffusion is current SOTA" and missed the trajectory.

4. **The bias-aware grading columns.** Pass 2's per-source table with "marketing load" and "independent signal" columns is the most reusable artifact in the session. Adopted as a template for any industry-adjacent research task.

5. **The "honest gaps" self-critique.** Pass 3's section listing "I trusted subagent citations without verifying", "I read 5/11 papers in full", "the field trajectory claim is narrative" - this is what makes the dossier trustworthy as a deliverable, not just confident prose.

## File layout produced (corrected)

```
~/research/
├── artifacts/20260607_093018_3412dfbb/   ← per-session, console reads from here
│   ├── SUMMARY.md
│   ├── self-pass-1-academic.md
│   ├── self-pass-2-industry.md
│   ├── self-pass-3-synthesis.md
│   └── model-comparison.md
└── dossiers/diffusion-policies-2025/     ← per-dossier, human reads from here
    ├── _stream-a-summary.md         (deepseek-v4-flash, academic)
    ├── _stream-b-summary.md         (deepseek-v4-flash, industry)
    ├── _stream-c-summary.md         (deepseek-v4-flash, critique)
    ├── dossier.md                   (final, composed after Pass 3)
    └── sources/                     (27 source notes)
```

**What was actually produced in the original run** (and what the user had to fix):

The self-passes and `SUMMARY.md` were first written to `dossiers/diffusion-policies-2025/`
and `dossiers/diffusion-policies-2025/artifacts/` - *wrong*. The user caught this on the
next turn ("did you create /artifacts/<session_id>/SUMMARY.md?") and had me move them
to `artifacts/<session_id>/`. The layout above reflects the corrected form. Do not
reproduce the original mistake: per-session artifacts go in `artifacts/<session_id>/`,
never in the dossier dir. The console and the dossier have different readers; respect
the contract. See `research-artifacts/SKILL.md` for the producer/consumer split.

## Lessons for the next multi-lens run

- The bias-aware grading template from Pass 2 is reusable. Keep it.
- "What nobody said" is a high-value Pass 3 section. Don't skip it.
- Coverage target is 30-50% in full, not 100%. The diminishing returns hit hard past 50%.
- The CEO memo in Pass 2 is the highest-signal output of that lens. Always produce one.
- The model-comparison artifact (`artifacts/model-comparison.md`) is the right deliverable for A/B tasks. It is the user's actual question, not the dossier itself.
