# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

<!--
Grouping for this repo: continuous-delivery content catalog. Use [YYYY-MM-DD] headings per content milestone.
-->

---

## [Unreleased]

Project standardization pass.

### Added

- `STANDARDS.md`: human-readable standards summary at repo root.
- `CHANGELOG.md`: this file.
- `.gitignore`: minimal (editor swap, OS files).
- `CLAUDE.md`: one-line shim that `@import`s `AGENTS.md` for Claude Code compatibility.

### Changed

- `AGENTS.md`: branch model `master` → `main`; added `synctool-sync` row to the Current skills table.

### TODO (backfill)

- Historical entries prior to this standardization pass are not yet captured. Backfill from `git log --oneline` when this file stabilises.

---

[Unreleased]: #unreleased
