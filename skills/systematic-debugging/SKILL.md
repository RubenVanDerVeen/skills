---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

## Overview

Adapted from obra/superpowers (MIT).

Quick fixes mask underlying issues and create new bugs. Find the root cause before attempting any fix.

**Iron law:** no fixes without root cause investigation first. Violating the letter of this process is violating the spirit of debugging.

## When to Use

Use for any technical issue:

- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

Use it especially when:

- Under time pressure (emergencies make guessing tempting).
- "Just one quick fix" seems obvious.
- Multiple fixes already tried.
- The previous fix did not work.
- The issue is not fully understood.

Do not skip because:

- The issue seems simple (simple bugs have root causes too).
- There is a rush (rushing guarantees rework).
- A quick fix is demanded (systematic is faster than thrashing).

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

BEFORE attempting any fix.

**Read errors carefully:**

- Do not skip past errors or warnings (they often contain the exact solution).
- Read stack traces completely.
- Note line numbers, file paths, error codes.

**Reproduce consistently:**

- Can the bug be triggered reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible, gather more data. Do not guess.

**Check recent changes:**

- What changed that could cause this? `git diff`, recent commits.
- New dependencies, config changes, environmental differences.

**Multi-component systems:** add diagnostic instrumentation at every component boundary (log data entering and exiting each layer, verify environment/config propagation) BEFORE proposing fixes. Run once to gather evidence showing WHERE it breaks, then analyze.

```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"
```

See `references/root-cause-tracing.md` for the backward tracing technique when the error is deep in the call stack.

**Trace data flow:**

- Where does the bad value originate?
- What called this with the bad value?
- Keep tracing up until the source is found.
- Fix at the source, not at the symptom.

### Phase 2: Pattern Analysis

Find the pattern before fixing.

1. Find working examples (similar working code in the same codebase).
2. Compare against references (read reference implementations COMPLETELY, not skimmed).
3. Identify differences (list every difference, however small).
4. Understand dependencies (settings, config, environment, assumptions).

### Phase 3: Hypothesis and Testing

Scientific method.

1. Form a single hypothesis: "I think X is the root cause because Y." Write it down. Be specific.
2. Test minimally: smallest possible change, one variable at a time.
3. Verify before continuing. If it works, move to Phase 4. If not, form a NEW hypothesis. Do not stack fixes.
4. When the cause is unknown, say "I do not understand X." Ask for help or research more.

### Phase 4: Implementation

Fix the root cause, not the symptom.

1. Create a failing test case (simplest possible reproduction, automated if possible). Have it BEFORE fixing.
2. Implement a single fix addressing the root cause. One change at a time, no "while I'm here" improvements or bundled refactors.
3. Verify the fix: passes now, no other tests broken, issue resolved.
4. If the fix does not work: STOP. Count fixes tried. If under 3, return to Phase 1 with new information. If 3 or more, question the architecture (below). Do NOT attempt Fix #4 without architectural discussion.

**Three or more failed fixes: question the architecture.**

Pattern indicating an architectural problem:

- Each fix reveals new shared state, coupling, or problems in different places.
- Fixes require "massive refactoring" to implement.
- Each fix creates new symptoms elsewhere.

STOP and question fundamentals:

- Is the pattern fundamentally sound?
- Is it being continued through sheer inertia?
- Should the architecture be refactored instead of fixing symptoms?

Discuss with the user before attempting more fixes. This is not a failed hypothesis; it is a wrong architecture.

After the fix, see `references/defense-in-depth.md` for adding validation at every layer the data passes through, so the bug becomes structurally impossible.

## Red Flags

STOP and return to Phase 1 if any of these thoughts appear:

- "Quick fix for now, investigate later."
- "Just try changing X and see if it works."
- "Add multiple changes, run tests."
- "Skip the test, I'll manually verify."
- "It's probably X, let me fix that."
- "I do not fully understand but this might work."
- "Pattern says X but I'll adapt it differently."
- "Here are the main problems: [lists fixes without investigation]."
- Proposing solutions before tracing data flow.
- "One more fix attempt" when already tried 2 or more.
- Each fix reveals a new problem in a different place.

**Three or more fixes failed:** question the architecture.

## User Signals You Are Doing It Wrong

Watch for these redirections:

- "Is that not happening?" (assumed without verifying).
- "Will it show us...?" (needed evidence gathering).
- "Stop guessing." (proposing fixes without understanding).
- "Ultra-think this." (question fundamentals, not just symptoms).
- "We're stuck?" (frustrated; the approach is not working).

When these appear: STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process." | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process." | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate." | The first fix sets the pattern. Do it right from the start. |
| "I'll write the test after confirming the fix works." | Untested fixes do not stick. Test first proves it. |
| "Multiple fixes at once saves time." | Cannot isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern." | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it." | Seeing symptoms is not understanding root cause. |
| "One more fix attempt" after 2+ failures. | Three or more failures = architectural problem. Question the pattern, do not fix again. |

## When Process Reveals "No Root Cause"

If systematic investigation reveals the issue is truly environmental, timing-dependent, or external:

1. The process has been completed.
2. Document what was investigated.
3. Implement appropriate handling (retry, timeout, error message).
4. Add monitoring or logging for future investigation.

But: 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

See `references/` for the full material on each:

- `references/root-cause-tracing.md`: trace bugs backward through the call stack to the original trigger.
- `references/defense-in-depth.md`: add validation at multiple layers after finding the root cause.
- `references/condition-based-waiting.md`: replace arbitrary timeouts with condition polling.

## Quick Reference

| Phase | Key activities | Success criteria |
|-------|---------------|------------------|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

## Real-World Impact

From debugging sessions:

- Systematic approach: 15-30 minutes to fix.
- Random fixes approach: 2-3 hours of thrashing.
- First-time fix rate: 95% vs 40%.
- New bugs introduced: near zero vs common.
