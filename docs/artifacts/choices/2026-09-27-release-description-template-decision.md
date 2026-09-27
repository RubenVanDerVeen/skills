# release-description: one template, three copy sites

- Date: 2026-09-27
- Status: active
- Source: `docs/artifacts/features/release-description/2026-09-27-release-description-design.md` (## Approaches considered)

## Choice

One skill (`skills/release-description/`) is the single source of truth for every release-body surface: the `chore(release): vX.Y.Z` commit body, the `git tag -a` annotation, and the GitHub or GitLab Release description. All three surfaces copy the same text character-for-character from one body (written to `.release-notes.md` at close-out by the documenter).

## Alternatives rejected

- Bake the template into `agents/documenter.md`: copies drift across documenter edits, and it pulls `versioning.md` policy into one agent body that already references it by pointer.
- Three separate templates (commit body, tag annotation, Release page): drift vector between the tag annotation and the Release page; the exact two-sources-of-truth failure mode the `pr-description` skill exists to prevent.

## Revisit when

A surface genuinely needs platform-specific structure one shared body cannot serve (e.g. a Release-page-only assets or migration section), or the documenter stops being the sole writer of release bodies.
