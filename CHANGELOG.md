# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

<!--
Grouping for this repo: continuous-delivery content catalog. Use [YYYY-MM-DD] headings per content milestone.
-->

---

## [Unreleased]

### Added

- `STANDARDS.md`: human-readable standards summary at repo root.
- `CHANGELOG.md`: this file.
- `.gitignore`: minimal (editor swap, OS files).
- `CLAUDE.md`: one-line shim that `@import`s `AGENTS.md` for Claude Code compatibility.
- `deep-research/`: end-to-end research pipeline skill (Hermes research profile). Intake → parallel gather (arxiv + web + own vault) → synthesized dossier with citations → brainstorm or Typst draft. Catalogue rows added in `README.md` (Skills table + Layout block) and `AGENTS.md` (Current skills table).

### Changed

- `AGENTS.md`: branch model `master` → `main`; added `synctool-sync` row to the Current skills table.
- `typst-pro`: bumped `@local/typst-tools` baseline `0.1.2` → `0.1.8` across skill examples, imports, and install paths. Factual references (fixed-in bug notes, rename reset point, version-numbering example, `@preview` pins) kept at `0.1.2`.

### Fixed

- `deep-research`: frontmatter now uses only `name` + `description` (dropped Hermes-only `title`, `version`, `author`, `license`, `platforms`, `metadata` fields that other agents cannot parse). Description rewritten to start with "Use when..." so it matches the trigger-only convention in `AGENTS.md` § `SKILL.md` frontmatter rules. Body now opens with `## Overview` per the same section. Frontmatter total: 539 chars (was 884).

### TODO (backfill)

- Historical entries prior to this standardization pass are not yet captured. Backfill from `git log --oneline` when this file stabilises.

---

[Unreleased]: #unreleased
