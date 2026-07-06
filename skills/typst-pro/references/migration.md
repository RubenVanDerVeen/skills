# Migration: `academic-tools:0.1.29` → `typst-tools`

The library was renamed from `academic-tools` → `typst-tools` during the migration to the `EmbeddedDynamics/TypstTools` repo (clean slate, version reset to `0.1.2`).

- New repo on disk: `C:\Users\ruben\Projects\Tools\TypstTools\`
- Old dir still on disk for reference: `C:\Users\ruben\Projects\Tools\Typst-Docs-Tools(to-be-updated)\` (pre-migration `academic-tools` v0.1.29).
- Existing user projects that import `@local/academic-tools:0.1.29` (e.g. `IDP/docs/typst/`) need their imports updated to `@local/typst-tools:0.x.x` (most relevant version) and a few API tweaks below.

When updating an existing project that imported `@local/academic-tools`:

1. **Update imports**: `@local/academic-tools:0.1.29` → `@local/typst-tools:0.1.8` (current baseline; or the project's relevant version) everywhere (including `_Imports.typ`, `GeneralConfig.typ`, every standalone `Onderzoek_*.typ`).
2. **Internal lib paths changed** (only relevant if you used granular imports):
   - `src/elements/<name>` → `src/components/<name>` (version-history, role-calculations).
   - `src/styling/base.typ` → `src/styles/base.typ`.
   - `src/styling/ieee.typ` → `src/standards/ieee/ieee.typ`.
   - `src/components/ieee-journal.typ` → `src/standards/ieee/ieee-journal.typ`.
   - `src/components/ieee-test-report.typ` → `src/standards/ieee/ieee-test-report.typ`.
   - `src/components/moscow.typ` → **deleted**, replaced by `src/renderers/moscow-renderer.typ`.
   - `src/assets/NHL_logo.jpg` → `assets/logos/nhl_logo.jpg` (top-level `assets/`, lowercase).
   - `src/assets/langs.yaml` → `assets/langs.yaml`.
3. **Type rename**: `version(committee: ..., description: ..., date: ..., level: ...)` → `version-entry(contributors: ..., department: ..., description: ..., date: ..., level: ...)`. `committee` → `contributors`; `department` is new and required.
4. **Template rename**: `IEEE-academic-test-repport` → `IEEE-academic-test-report` (typo fixed).
5. **Version baseline shift**: First level-1 entry now produces `1.0.0` (was `2.0.0`). Adjust first-entry level or document the change.
6. **DB key**: section-DB rows now use **lowercase `id:`** (was uppercase `ID:`). The `slice-db` helper, the typed `moscow-category.id`, and `moscow-slice-categories` all key off `id`. Sweep `*_DB.typ` and any examples.
7. **DB helpers rename** (snake → kebab):
   - `slice_db` → `slice-db`
   - `pve_render(db, lvl)` / `pve_range(db, a, b, lvl)` → `section-render(db, header-level: lvl)` / `section-range-render(db, a, b, header-level: lvl)`
   - `moscow_range(db, a, b)` → `moscow-range(db, a, b, cells: pc)` *(now from `moscow-renderer`; pass `cells:` explicitly)*
   - `bom_range(db, a, b)` → `bom-range(db, a, b, colors: (...))` (colors are params, no implicit `COL.*` dependency)
   - `contract_render(db, lvl)` → `section-range-render(db, ..., header-level: lvl)` with `style:` per section
   - `bom_table` / `bom_render` → `bom-table` / `bom-render`; `show_subtotals` → `show-subtotals`
8. **MoSCoW priority cells signature change**: `make-priority-cells()` is now in `src/renderers/moscow-renderer.typ`, accepts `theme:` (defaults to `default-theme`) and per-priority overrides (`must:`, `should:`, `could:`, `wont:`, `unknown:`). Returns a dict with both semantic keys (`must / should / could / wont / unknown`) and numeric aliases (`p1 / p2 / p3 / p4`). The IDP pattern is to bind it once and expose `let p1 = pc.p1` aliases for legacy item dicts.
9. **Manual MoSCoW legend**: hand-rolled "Prioritisering / Uitleg / Indicatie" tables in subdocuments → replace with `moscow-legend(cells: pc, show-indicator: true)`.
10. **Footer config**: `footer-config: ([#title], ...)` literal-text bug is fixed; pass `auto` to use the smart default, or supply a full dict.
11. **Database files in `Config/`**: drop the helper bodies (`slice_db`, `pve_render`, `moscow_*`, `bom_*`, `contract_render`, `_render_item`). Keep only the `_db` arrays plus project-specific palette / metadata. The bind for `pc = make-priority-cells(...)` and `bom-colors = (...)` typically lives in `Config/PvE_MoSCoW.typ` and `Config/BOM_DB.typ` respectively.
12. **Commenting unused features**: when a feature isn't used in the migrated document (e.g. version history on a sub-document), keep it as a commented-out block with the new API shape so the next person can re-enable it without re-deriving the call signature.

For folder/file renames under the kebab/English convention, see the migration cheat-sheet in `project-layout.md`.
