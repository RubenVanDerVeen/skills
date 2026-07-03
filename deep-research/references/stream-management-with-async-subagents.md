# Stream Management With Async Subagents

The user complaint "the stream is not left open" / "you closed the turn again" almost always traces to one of three patterns. Capture them so the next session starts already knowing.

## Symptom 1: Short "still waiting" ticks between subagent completions

**What it looks like in the conversation log.** After dispatching 3 subagents, the parent replies with one-line "still waiting on subagents 1/2/3" messages between subagent completions. Each one ends a turn. The user sees a series of short replies with no substance and concludes "the stream closed again."

**Why the user reads it that way.** From Telegram / chat perspective, every reply is a turn. A reply that says "still waiting" is functionally a closed turn — there is no work in it, no tool calls, no new content. Even when framed as a "tick," it ends the user's reading window.

**Fix.** Do not send tick messages. Either (a) wait silently — don't reply at all — and let the subagent results arrive as their own new messages in the stream, or (b) cancel the parallel dispatch and do the work inline (see deep-research skill pitfall "If the user is actively waiting, don't dispatch in parallel"). Pick (a) if the user can disengage; pick (b) if they are sitting at Telegram waiting.

## Symptom 2: Wrap-up reply after a tool-call batch

**What it looks like.** Agent does a batch of tool calls (e.g. five parallel searches), then writes "OK, give me a minute while I think" or "now writing the dossier." The user reads it as the turn ending before the dossier exists.

**Why it reads that way.** "Now writing the dossier" without an actual `write_file` call is a promise, not a delivery. The user can't tell whether the next reply will be the dossier or another tick.

**Fix.** After a batch of searches, the next reply must be the synthesis itself, not a meta-message about the synthesis. If you need more searches before you can write, do those searches in the same batch and only reply once with the actual write at the end. Never write a "wait" message between read-only searches and the final write_file.

## Symptom 3: Apology + correction reply after a stream-management mistake

**What it looks like.** Agent dispatched subagents, user said "you closed the stream," agent replies "Sorry, switching to inline now." Turn ends. User waits. Agent does tool calls next turn, replies with findings. But the apology itself was a closed turn.

**Why it reads that way.** The apology is a reply with no tool calls. Same problem as Symptom 1 — a closed turn with no work in it.

**Fix.** When the user says "you closed the stream" / "don't end the turn" / "keep it open," the correct response is to IMMEDIATELY do tool calls (more searches, dossier writes, source fetches) in the same reply. Do not write an apology paragraph — the work itself is the apology. If you must acknowledge, make the acknowledgment a single inline sentence attached to a tool call, not a standalone reply.

## Operating models in practice

These are the three shapes a research session can take, ranked by user-engagement level:

1. **Background mode (user can disengage).** "Run the deep-research on topic X, ping me when it's done." Subagents dispatched in parallel. Parent waits silently with no further replies until ALL subagents return. Final reply is the dossier + handoff. Use for cron jobs, "let me know when ready," any time the user does not need to see intermediate work.

2. **Inline mode (user is actively waiting).** "Research X for me." Subagents NOT dispatched. Parent runs the same end-to-end pipeline inline: intake → searches (batched in one turn) → synthesis → dossier write → handoff. All in one or two replies. The tool calls themselves keep the stream visibly alive — the user sees reads, searches, writes happen, and they can interject corrections between tool results.

3. **Skeleton-and-fill mode (user can step in mid-flight).** "Research X. I'll let you know if I want to redirect." Parent writes a dossier skeleton (TL;DR placeholder, empty sections, methodology footer) inline in the FIRST reply. Subagents dispatched in background to fill specific sections. Parent waits silently. Subagent results arrive as new messages. Parent fills the skeleton in place. Use when the topic is broad and the user might want to scope-shift before deep work.

Model 3 is the one the user explicitly proposed in the 2026-06-27 cheap-claude-orchestrator session ("If you write the skeleton and let the agents write their findings in there, I could call up on you to continue to finish the research"). It is NOT a substitute for model 2; it's the right shape when the user wants to retain steering control. The dossier skeleton is the parent's contribution; the subagent fills are scoped narrowly to specific sections (e.g. "fill the Pricing Comparison table," "fill the Benchmark section") so the parent can integrate without redoing work.

## Failure modes verified

- 2026-06-27 cheap-claude-orchestrator dossier — agent dispatched 3 parallel subagents, then sent 2-3 short tick messages while user waited. User pushback: "the stream is not left open" / "you closed the turn again." Fix path: switch to model 2 (inline) or model 3 (skeleton + scoped subagent fills), never model 1 with ticks.
