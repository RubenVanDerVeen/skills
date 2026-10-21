// Minimal caveman mode reinforcement plugin for opencode v2.
// Adapted from JuliusBrussee/caveman (per-turn state handling concept, heavily slimmed).
// Own version: no command parsing, no manifests, no session heuristics.
// Switching happens via /caveman (commands/caveman.md) writing the state file directly.
//
// State: ~/.config/opencode/.caveman-mode
// Values: off | lite | full | ultra | wenyan-lite | wenyan-full | wenyan-ultra
// Absent or invalid file -> no injection; the always-on base rules in
// ~/.config/opencode/AGENTS.md (full) apply on their own.
// Explicit "off" -> inject an override line so the static block is neutralized.
//
// opencode v2 plugin API: default export {id, setup(ctx)}.
// The session "context" hook runs right before every agent-loop model call and
// hands over the assembled system instructions, so the mode line is pushed as
// one more system part. Verified on opencode v2.0.32.

import { readFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const MODES = new Set([
  "off", "lite", "full", "ultra",
  "wenyan-lite", "wenyan-full", "wenyan-ultra",
])

const LINE = {
  lite:
    "CAVEMAN MODE ACTIVE (lite): no filler or hedging; keep articles and full sentences. Professional but tight.",
  full:
    "CAVEMAN MODE ACTIVE (full): drop articles, fragments OK, short synonyms. No tool-call narration, no decorative tables or emoji, no long raw error-log dumps unless asked.",
  ultra:
    "CAVEMAN MODE ACTIVE (ultra): strip conjunctions when unambiguous, one word when one word is enough, state each fact once. No prose abbreviations, no arrows. Code symbols, function names, API names, error strings: never touch.",
  "wenyan-lite":
    "CAVEMAN MODE ACTIVE (wenyan-lite): semi-classical register. Drop filler and hedging, keep grammar structure.",
  "wenyan-full":
    "CAVEMAN MODE ACTIVE (wenyan-full): fully 文言文, maximum classical terseness. Classical particles (之/乃/為/其), subjects often omitted.",
  "wenyan-ultra":
    "CAVEMAN MODE ACTIVE (wenyan-ultra): extreme abbreviation, classical Chinese feel, maximum compression.",
  off:
    "CAVEMAN MODE OFF: write in normal, complete, professional prose. Ignore all terseness rules for the rest of this reply.",
}

function readMode() {
  try {
    const raw = readFileSync(join(homedir(), ".config", "opencode", ".caveman-mode"), "utf8").trim()
    return MODES.has(raw) ? raw : null
  } catch {
    return null
  }
}

export default {
  id: "caveman",
  async setup(ctx) {
    try {
      const session = ctx && ctx.session
      if (!session || typeof session.hook !== "function") return
      await session.hook("context", (event) => {
        try {
          const mode = readMode()
          if (mode === null) return
          const system = event && event.system
          if (!Array.isArray(system)) return
          system.push({ type: "text", text: LINE[mode] })
        } catch {
          // never break a session over caveman
        }
      })
    } catch {
      // never break a session over caveman
    }
  },
}
