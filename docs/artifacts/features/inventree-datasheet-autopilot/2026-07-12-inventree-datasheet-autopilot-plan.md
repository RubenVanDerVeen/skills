# InvenTree Datasheet Autopilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Part with an MPN -> datasheet PDF found on the web, verified, attached to the InvenTree part; three triggers (on-demand, batch backfill, during CSV import).

**Architecture:** Two new MCP tools (`inventree_list_attachments`, `inventree_upload_attachment`) in the homelab MCP server give the agent attachment access. The sourcing itself is agent-driven bash (curl search + download + verify), documented as a new "Datasheet workflow" section in the inventree agent. No new services, no new dependencies.

**Tech Stack:** Python (FastMCP + httpx, existing server), bash/curl, opencode + Claude Code agent markdown.

**Spec:** `docs/artifacts/features/inventree-datasheet-autopilot/2026-07-12-inventree-datasheet-autopilot-design.md`

**Depends on:** the `opencode-inventree-agent` plan being executed (agent file exists, MCP registered in opencode).

## Global Constraints

- Two repos + one machine-local file. Commit separately per repo, Conventional Commits 1.0.0:
  - Homelab repo: `C:\Users\ruben\projects\Hobby\Homelab` (Tasks 1-3)
  - Skills repo: `C:\Users\ruben\projects\Tools\skills` (Task 4)
  - Machine-local, never committed: `~/.claude/agents/inventree.md` (Task 5)
- No em-dashes (U+2014) in any repo file.
- No secrets in repo files or in this plan's outputs; API keys come from env/config at runtime.
- MCP server changes require restarting the client (opencode / Claude Code) to reload tool schemas.

---

### Task 1: Probe the attachment endpoint shape (live instance)

**Files:** none (read-only probe; records a fact for Task 2)

**Interfaces:**
- Produces: decision `MODERN` (generic `/api/attachment/`) or `LEGACY` (`/api/part/attachment/`).

- [ ] **Step 1: Probe** (keys read from `~/.claude.json`, not typed):

```bash
python - <<'EOF'
import json, os, httpx
env = json.load(open(os.path.expanduser("~/.claude.json")))["mcpServers"]["homelab"]["env"]
base = env.get("INVENTREE_BASE_URL", "http://192.168.178.208:8000").rstrip("/")
hdr = {"Authorization": f"Token {env['INVENTREE_API_KEY']}"}
r = httpx.get(f"{base}/api/attachment/", params={"model_type": "part", "model_id": 1}, headers=hdr, timeout=10)
print("modern /api/attachment/:", r.status_code)
r2 = httpx.get(f"{base}/api/part/attachment/", params={"part": 1}, headers=hdr, timeout=10)
print("legacy /api/part/attachment/:", r2.status_code)
EOF
```

Expected: one of the two returns `200`. `200` on the first -> MODERN; otherwise `200` on the second -> LEGACY. Record which for Task 2. (Run with the Homelab mcp venv python if system python lacks httpx: `C:\Users\ruben\projects\Hobby\Homelab\mcp\.venv\Scripts\python.exe`.)

---

### Task 2: Add the two MCP tools (Homelab repo)

**Files:**
- Modify: `mcp/server.py` (append at the end of the "InvenTree tools" section, before the next section divider)
- Modify: `mcp/README.md` (only if it catalogs tools by name; add the two new ones in the same style)

**Interfaces:**
- Consumes: `inventree_request(method, path, **kwargs)` helper at `mcp/server.py:53` (httpx passthrough, Token auth, `raise_for_status`, returns parsed JSON).
- Produces: MCP tools `inventree_list_attachments(part_id)` and `inventree_upload_attachment(part_id, file_path, comment="")`, surfaced to opencode as `homelab_inventree_list_attachments` / `homelab_inventree_upload_attachment` and to Claude Code as `mcp__homelab__inventree_list_attachments` / `mcp__homelab__inventree_upload_attachment`.

- [ ] **Step 1: Add the tools.** MODERN variant (from Task 1):

```python
@mcp.tool()
def inventree_list_attachments(part_id: int) -> str:
    """List file attachments on a part (pk, filename, comment). Use before uploading to avoid duplicates."""
    data = inventree_request("GET", "attachment/", params={"model_type": "part", "model_id": part_id})
    results = data.get("results", data) if isinstance(data, dict) else data
    return json.dumps([{
        "pk": a["pk"],
        "filename": os.path.basename(a.get("attachment") or ""),
        "attachment": a.get("attachment", ""),
        "comment": a.get("comment", ""),
    } for a in results], indent=2)


@mcp.tool()
def inventree_upload_attachment(part_id: int, file_path: str, comment: str = "") -> str:
    """Upload a local file as an attachment on a part. Put the source URL in comment."""
    with open(file_path, "rb") as fh:
        data = inventree_request(
            "POST", "attachment/",
            data={"model_type": "part", "model_id": str(part_id), "comment": comment},
            files={"attachment": (os.path.basename(file_path), fh)},
        )
    return json.dumps({"pk": data.get("pk"), "attachment": data.get("attachment", "")}, indent=2)
```

LEGACY variant (only if Task 1 said LEGACY): same two functions, with `"attachment/"` replaced by `"part/attachment/"` and the `data=`/`params=` dicts replaced by `{"part": str(part_id), "comment": comment}` / `{"part": part_id}` (no `model_type`/`model_id` keys).

- [ ] **Step 2: Syntax check**

Run: `C:\Users\ruben\projects\Hobby\Homelab\mcp\.venv\Scripts\python.exe -m py_compile mcp/server.py`
Expected: exit 0, no output.

- [ ] **Step 3: Commit (Homelab repo)**

```bash
git -C ~/projects/Hobby/Homelab add mcp/server.py mcp/README.md
git -C ~/projects/Hobby/Homelab commit -m "feat(mcp): inventree attachment tools (list, upload) for datasheet workflow"
```

---

### Task 3: Live verification of the tools (Homelab repo, no file changes)

**Interfaces:**
- Consumes: the two functions from Task 2, called directly (bypasses MCP transport; same code path as the tools).

- [ ] **Step 1: Round-trip test** (upload scrap PDF to a real part, list it, delete it):

```bash
cd ~/projects/Hobby/Homelab/mcp
python - <<'EOF'
import json, os, sys
env = json.load(open(os.path.expanduser("~/.claude.json")))["mcpServers"]["homelab"]["env"]
os.environ.update(env)
import server  # noqa: E402  (env must be set before import)

# scrap one-page PDF
pdf = os.path.join(os.environ.get("TEMP", "/tmp"), "scrap-test.pdf")
open(pdf, "wb").write(b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\nxref\n0 4\ntrailer<</Size 4/Root 1 0 R>>\n%%EOF\n" + b"0" * 11000)

parts = json.loads(server.inventree_list_parts(limit=1))
pk = parts[0]["pk"]
print("target part:", pk, parts[0]["name"])
up = json.loads(server.inventree_upload_attachment(pk, pdf, comment="round-trip test"))
print("uploaded pk:", up["pk"])
lst = json.loads(server.inventree_list_attachments(pk))
assert any(a["pk"] == up["pk"] for a in lst), "uploaded attachment not listed"
server.inventree_request("DELETE", f"attachment/{up['pk']}/")  # cleanup (LEGACY: part/attachment/{pk}/)
print("cleanup ok; round-trip PASS")
EOF
```

Expected: `round-trip PASS`. (`inventree_request` raises on JSON-less DELETE responses in some versions; if it does, wrap the DELETE in try/except and verify deletion via a second `inventree_list_attachments` call instead.)

- [ ] **Step 2: Restart clients** so schemas reload: restart opencode; Claude Code picks the server up next session.

---

### Task 4: Datasheet workflow section in the opencode agent (skills repo)

**Files:**
- Modify: `agents/inventree.md` (append new section before "## Behaviour Rules")
- Modify: `agents/README.md` (inventree roster row: append "datasheet fetch/attach" to the role description)

**Interfaces:**
- Consumes: `homelab_inventree_list_attachments`, `homelab_inventree_upload_attachment` (Task 2), existing part/category tools.

- [ ] **Step 1: Append this section** (exact content) to `agents/inventree.md`:

```markdown
## Datasheet Workflow

Attach manufacturer datasheet PDFs to parts. Three triggers, same steps 2-6:

1. **Scope.** On-demand: the named part. Batch ("fill missing datasheets"): iterate `homelab_inventree_list_parts` (optionally one category); process parts whose attachments contain no `.pdf`. Import hook: after creating a part in an MPN-carrying category (ICs & Logic 29, Transistors & MOSFETs 30, Power & Regulation 11, Microcontrollers & SBCs 5), attempt once, soft-fail into the import report.
2. **MPN.** Extract from the part name (naming convention puts chip/model first: `LM2596 - Buck - ...`, `Dev Board - ESP32-C3 - ...`). No identifiable MPN: mark skipped, continue.
3. **Dedup.** `homelab_inventree_list_attachments(part_id)`: an existing `.pdf` means done.
4. **Find.** Bash: `curl -sL "https://html.duckduckgo.com/html/?q=<MPN>+datasheet+filetype%3Apdf"`, pick candidate URLs preferring manufacturer domains (ti.com, st.com, onsemi.com, nxp.com, microchip.com, diodes.com, infineon.com, vishay.com) over aggregators. Judge candidates yourself; no hardcoded scraping.
5. **Verify.** Download to a temp file with curl. Accept only: file starts with `%PDF` and is larger than 10 KB. Reject and try the next candidate otherwise (max 3 candidates, then mark failed).
6. **Attach.** `homelab_inventree_upload_attachment(part_id, file_path, comment=<source URL>)`. If the part's `link` field is empty, set it to the datasheet URL via `homelab_inventree_update_part`.
7. **Report.** One table: part, MPN, result (attached / skipped: no MPN / failed: no candidate), source domain.

Search endpoint throttled or blocked: ask for a URL, continue from step 5.
```

- [ ] **Step 2: Verify**

Run: `grep -c 'homelab_inventree_upload_attachment' agents/inventree.md` -> Expected: `>= 1`
Run: `grep -cP '\x{2014}' agents/inventree.md` -> Expected: `0`

- [ ] **Step 3: Sync + commit (skills repo)**

```bash
cp agents/inventree.md ~/.config/opencode/agents/
git add agents/inventree.md agents/README.md
git commit -m "feat(agents): datasheet workflow in inventree agent (fetch, verify, attach)"
```

---

### Task 5: Mirror into the Claude Code agent (machine-local)

**Files:**
- Modify: `~/.claude/agents/inventree.md` (not in a repo; no commit)

- [ ] **Step 1: Frontmatter `tools:` line**: append `, mcp__homelab__inventree_list_attachments, mcp__homelab__inventree_upload_attachment` to the end of the existing tools list.

- [ ] **Step 2: Body**: insert the same "## Datasheet Workflow" section as Task 4 before "## Behaviour Rules", with tool names de-prefixed to the Claude naming used in that file's prose (`inventree_list_attachments`, `inventree_upload_attachment`, `inventree_update_part`, `inventree_list_parts`). Em-dashes stay banned here too.

- [ ] **Step 3: Verify**: `grep -c 'inventree_upload_attachment' ~/.claude/agents/inventree.md` -> Expected: `2` (tools line + body).

---

### Task 6: End-to-end smoke tests

**Files:**
- Create (scratch only): `%TEMP%\datasheet-smoke.csv`

- [ ] **Step 1: On-demand.** In an opencode inventree session: "Fetch the datasheet for <an IC part already in inventory, e.g. an LM2596 or NE555 based part>". Expected: report row "attached", PDF visible on the part in the InvenTree web UI (`http://192.168.178.208:8000`).

- [ ] **Step 2: Batch dry-run.** "List which parts in ICs & Logic are missing datasheets, do not fetch yet." Expected: correct missing/present split (spot-check 2 parts in the web UI).

- [ ] **Step 3: Import hook.** Write the scrap CSV:

```csv
"Qty","Product ID","SKU ID","Attributes","Title"
"1","1005001234567","12345678901234","Package: 5PCS","NE555 Timer IC DIP-8 5pcs"
"2","1005007654321","43210987654321","Size: M3x10 50pcs","M3x10 cap head hex socket screws 50pcs"
```

Import it in an inventree session. Expected: NE555 part created (or stock added) with a datasheet attempt in the report; the screws land in Bolts & Screws (14) with NO datasheet attempt (category filter working); no errors. Clean up: remove the test part/stock created from the scrap CSV afterwards (delete via agent), since it is fake order data.

- [ ] **Step 4: Report**: commits (both repos) with hashes, verification outputs, anything Unverified.
