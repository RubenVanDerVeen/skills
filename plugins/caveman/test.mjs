// Smoke test for the opencode v2 caveman plugin (node stdlib only).
// Builds a fake plugin context, captures the session "context" hook callback
// and checks that the mode line reaches the system instructions of a model call.
//
// Hermetic: HOME is pointed at a temp dir before the plugin is imported, so the
// plugin resolves its state file inside the temp dir and the real
// ~/.config/opencode/.caveman-mode is never read, written or removed.

import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs"
import { homedir, tmpdir } from "node:os"
import { join } from "node:path"

const tmp = mkdtempSync(join(tmpdir(), "caveman-test-"))
process.env.HOME = tmp

const state = join(tmp, ".config", "opencode", ".caveman-mode")
mkdirSync(join(tmp, ".config", "opencode"), { recursive: true })

// The plugin resolves its state path at call time via os.homedir(), which on
// POSIX follows $HOME. Assert the override took effect before importing it.
if (homedir() !== tmp) throw new Error(`HOME override failed: homedir()=${homedir()}`)
if (!state.startsWith(tmp)) throw new Error(`state path escapes temp dir: ${state}`)

const { default: plugin } = await import("./index.js")

async function request(mode) {
  if (mode === null) rmSync(state, { force: true })
  else writeFileSync(state, mode)

  let callback = null
  let hookName = null
  const ctx = {
    session: {
      hook(name, cb) {
        hookName = name
        callback = cb
        return Promise.resolve({ dispose: async () => {} })
      },
    },
  }

  await plugin.setup(ctx)
  if (hookName !== "context" || !callback) throw new Error("context hook not registered")

  const event = {
    sessionID: "ses_test",
    agent: "build",
    model: { providerID: "test", id: "test-model" },
    system: [{ type: "text", text: "BASE" }],
    messages: [],
    options: {},
    tools: {},
  }
  await callback(event)

  return {
    registered: hookName === "context",
    parts: event.system.length,
    system: event.system.map((part) => part.text).join("\n"),
  }
}

function report(label, ok) {
  console.log(`${label}: ${ok ? "PASS" : "FAIL"}`)
  if (!ok) process.exitCode = 1
}

// absent file: base rules apply, plugin stays silent
const absent = await request(null)
report("absent", absent.registered && absent.parts === 1 && !absent.system.includes("CAVEMAN"))

// ultra: reinforcement line appended to the system instructions
const ultra = await request("ultra")
report(
  "ultra",
  ultra.registered &&
    ultra.parts === 2 &&
    ultra.system.startsWith("BASE") &&
    ultra.system.includes("CAVEMAN MODE ACTIVE (ultra)"),
)

// off: override line neutralizes the static block
const off = await request("off")
report("off", off.registered && off.parts === 2 && off.system.includes("CAVEMAN MODE OFF"))

// garbage value: treated as absent, silent
const garbage = await request("banana")
report("garbage", garbage.registered && garbage.parts === 1 && !garbage.system.includes("CAVEMAN"))

rmSync(tmp, { recursive: true, force: true })
