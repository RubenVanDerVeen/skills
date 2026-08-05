# InvenTree datasheet autopilot: fetch and attach datasheets via the inventree agent

Date: 2026-07-12
Status: approved (design approved in session)

## Goal

Given a part with an identifiable manufacturer part number (MPN), find its datasheet PDF on the web, verify it, and attach it to the InvenTree part. Three triggers, same machinery: on-demand ("fetch datasheet for X"), batch backfill ("fill missing datasheets"), and opportunistic during AliExpress CSV import when the MPN is obvious (ICs, transistors, regulator modules). Kills repeated datasheet hunting during design work.

## Context (current state, 2026-07-12)

- Homelab MCP server (`C:\Users\ruben\projects\Hobby\Homelab\mcp\server.py`, 986 lines, single file) has a generic `inventree_request(method, path, **kwargs)` helper and ~25 inventree tools. No attachment tools exist.
- InvenTree instance `http://192.168.178.208:8000` supports file attachments on parts via its REST API.
- Depends on spec #1 (`opencode-inventree-agent`): the workflow section lands in that agent. The Claude Code copy (`~/.claude/agents/inventree.md`) gets the same section so both harnesses can run it.
- AliExpress generic parts often have no real MPN; the workflow must skip these without noise.

## Design

### 1. Two new MCP tools (Homelab repo, `mcp/server.py`)

- `inventree_list_attachments(part_id)`: list existing attachments (filename, pk, comment). Used for dedup and for finding parts missing a datasheet.
- `inventree_upload_attachment(part_id, file_path, comment)`: multipart POST through `inventree_request`. Comment stores the source URL.

Implementation note for the plan: InvenTree moved from `/api/part/attachment/` (legacy) to a generic `/api/attachment/` endpoint (`model_type="part"`, `model_id`). First plan task probes the live instance and targets whichever shape it serves.

### 2. Sourcing machinery (agent-driven, no new services)

Bash only, no new dependencies:

1. Extract MPN from part name/description (naming convention puts chip/model first for ICs, buck/boost, BMS, chargers, dev boards). No MPN: skip, report as skipped.
2. Dedup: `inventree_list_attachments` first; existing `.pdf` attachment means done.
3. Search: `curl` against a search endpoint (DuckDuckGo HTML) for `<MPN> datasheet filetype:pdf`; prefer manufacturer domains (ti.com, st.com, onsemi.com, nxp.com, microchip.com, diodes.com, ...) over aggregators. The model judges candidates; no hardcoded scraper logic.
4. Download to scratch, verify: starts with `%PDF`, size above 10 KB.
5. Upload via `inventree_upload_attachment`, comment = source URL. Also set the part `link` field to the datasheet URL when `link` is empty.

### 3. Agent integration (skills repo, `agents/inventree.md`)

New "Datasheet workflow" section covering the three triggers:

- On-demand: single part by name or pk.
- Batch backfill: iterate parts (optionally per category), list attachments, process those missing a PDF; report found/skipped/failed table at the end.
- Import hook: the AliExpress CSV import workflow gains one optional step: after creating a part in an MPN-carrying category (ICs & Logic, Transistors & MOSFETs, Power & Regulation, Microcontrollers & SBCs), attempt the datasheet fetch; soft-fail silently into the final report.

Same section is added to the Claude Code agent copy, plus the two new MCP tool names in its `tools:` frontmatter line (machine-local file, not in a repo; noted here so it is not forgotten).

## Execution layout (cross-repo)

- Homelab repo: the two MCP tools + `mcp/README.md` update. Own commit(s), Conventional Commits.
- Skills repo: agent workflow section + `agents/README.md` note. Own commit.
- Machine-local: Claude Code agent copy update; opencode restart to reload MCP schemas.

One plan may cover all three targets with clearly separated tasks per repo.

## Verification

1. Tool-level: upload a scrap PDF to a test part on the live instance; attachment visible in the InvenTree web UI; `inventree_list_attachments` returns it.
2. On-demand e2e: one known IC part (e.g. an NE555 or a buck converter chip already in inventory) goes from no attachment to verified PDF attached.
3. Batch: dry-run listing on one category reports correct missing/present split before any fetch.
4. Import hook: sample CSV with one IC row attaches a datasheet during import; one no-MPN row is skipped without error.

## Out of scope

- Parsing/OCR of datasheet contents.
- Octopart/LCSC/Mouser APIs (keys, registration); revisit only if search hit-rate is poor.
- Non-PDF datasheets, application notes, 3D models.

## Risks / notes

- Search endpoint fragility (DuckDuckGo HTML may throttle): fallback is the user pasting a URL, the workflow continues from the download step unchanged.
- Hit-rate on AliExpress generics is low by design; the skip rule keeps noise down.
- Attachment endpoint shape (legacy vs modern) resolved by the first plan task against the live instance.
