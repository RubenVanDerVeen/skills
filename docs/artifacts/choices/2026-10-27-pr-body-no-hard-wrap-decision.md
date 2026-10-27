# PR body single-line paragraphs and linked commits

- Date: 2026-10-27
- Status: active
- Source: user preference, recorded while fixing the pr-description and release-description templates

## Choice
Agent-written PR and release description bodies write every paragraph and bullet as one single source line, leaving the wrapping to the renderer, and PR bodies reference commits as explicit markdown links ([`abc1234`](https://github.com/<owner>/<repo>/commit/abc1234)), never bare or backticked shas.

## Alternatives rejected
- Hard-wrapped source lines: EmbeddedDynamics/matrium PR #3 broke sentences across lines; the renderer wraps long lines anyway, so a source wrap only added noise and merge friction.
- Backticked shas: backticks block GitHub autolinking, so the commit references in PR #3 rendered as dead text.
- Bare shas without a link: GitHub autolinks a bare sha only when it matches a known commit, so an explicit markdown link is the reliable form.
- Commit links in release bodies: the release-description template keeps commit hashes out of the Summary and Highlights, hashes only in the Full changelog section. That design stands.

## Revisit when
The renderer stops wrapping long lines, OR GitHub changes how bare or backticked commit references are linked.
