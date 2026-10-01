# stdctl out-of-tree with PATH-symlink distribution

- Date: 2026-09-29
- Status: active
- Source: `docs/artifacts/features/stdctl/2026-09-29-stdctl-report.md` (spec: `docs/artifacts/features/stdctl/2026-09-29-stdctl-design.md`)

## Choice

The general standards check CLI lives outside the skills repo as sibling project `~/projects/Tools/stdctl`, distributed machine-wide via symlink `~/.local/bin/stdctl -> ~/projects/Tools/stdctl/bin/stdctl`; the skills repo markdown-only rule is preserved.

## Why

- Skills repo stack is markdown-only by prior decision (2026-09 AGENTS.md); a bash CLI inside it would break the rule for a second exception.
- Single bash file + symlink = one-line install, and sbx distribution is copying one file. stdctl resolves the repo from cwd (`git rev-parse --show-toplevel`), never its own location, so symlink and copy both work.
- `skillctl` stays in the skills repo: it does skills-repo-specific work (sync, catalog checks C6/C7, folder-name match). stdctl is the general checker (G1-G7 floor, S1-S5 structure/tier, K1-K2 skills-collection) for any standardized repo. Different concerns, different homes; no `bin/skillctl` rewiring.

## Alternatives rejected

- stdctl inside the skills repo next to `skillctl`: breaks the markdown-only stack rule, couples a general tool to one repo.
- Rewire `skillctl` into the general checker: merges two rule sets and two audiences; skills-repo sync logic does not belong in a universal linter.
- Copy the script into every repo: drifts immediately, no single source.
- Package-manager install: overkill for one dependency-free bash file.

## Consequence if wrong

Two tools exist where one might have sufficed; if stdctl ever needs skills-repo awareness or skillctl needs general rules, the split becomes friction and a merge is forced. If stdctl outgrows a single bash file or needs to reach machines without `~/projects/Tools`, symlink distribution breaks.

## Revisit when

stdctl grows beyond one bash file, needs non-Linux portability, or distribution to machines that do not mount `~/projects/Tools` (then vendor the file or package it). Or the skillctl/stdctl rule sets need merging.
