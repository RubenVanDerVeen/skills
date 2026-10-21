// Smoke test for the opencode v2 caveman plugin (node stdlib only).
// Builds a fake plugin context, captures the session "context" hook callback
// and checks that the mode line reaches the system instructions of a model call.

import { rmSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

const state = join(homedir(), ".config", "opencode", ".caveman-mode")
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

rmSync(state, { force: true })
