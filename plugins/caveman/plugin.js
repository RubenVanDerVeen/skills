// Minimal caveman mode reinforcement plugin.
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
// Requires opencode >= 1.15.x (experimental.chat.system.transform hook).

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

export const CavemanPlugin = async (_ctx) => {
  return {
    // Hook contract mirrors upstream (plugin.js:183-214): output.system is a
    // string ARRAY, mutated in place; the return value is discarded.
    "experimental.chat.system.transform": async (_input, output) => {
      try {
        const mode = readMode()
        if (mode === null) return
        const line = LINE[mode]
        const target = output && typeof output === "object" ? output : {}
        if (!Array.isArray(target.system)) target.system = []
        if (target.system.length === 0) target.system.push(line)
        else target.system[target.system.length - 1] += "\n\n" + line
      } catch {
        // never break a session over caveman
      }
    },
  }
}

export default CavemanPlugin
