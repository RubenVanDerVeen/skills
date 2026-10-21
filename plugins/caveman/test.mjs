import { readFileSync, rmSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const state = join(homedir(), ".config", "opencode", ".caveman-mode")
const mod = await import("./plugin.js")
const plugin = await mod.default({})
const hook = plugin["experimental.chat.system.transform"]

async function inject() {
  const out = { system: ["BASE"] }
  await hook({}, out)
  return out.system.length ? out.system[out.system.length - 1] : ""
}

// absent file: base rules apply, plugin stays silent
rmSync(state, { force: true })
console.log("absent:", (await inject()) === "BASE" ? "PASS" : "FAIL")

// ultra: reinforcement line appended
writeFileSync(state, "ultra")
const up = await inject()
console.log("ultra:", up.startsWith("BASE") && up.includes("CAVEMAN MODE ACTIVE (ultra)") ? "PASS" : "FAIL")

// off: override line neutralizes static block
writeFileSync(state, "off")
const off = await inject()
console.log("off:", off.includes("CAVEMAN MODE OFF") ? "PASS" : "FAIL")

// garbage value: treated as absent, silent
writeFileSync(state, "banana")
console.log("garbage:", (await inject()) === "BASE" ? "PASS" : "FAIL")

rmSync(state, { force: true })
