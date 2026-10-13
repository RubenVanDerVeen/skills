#!/usr/bin/env bash
# Regression suite for the academic-writing-pro linter.
set -euo pipefail
cd "$(dirname "$0")/../../../.."
LINT=skills/academic-writing-pro/scripts/lint-academic.py
BASE=skills/academic-writing-pro/tests/pressure-scenarios
fail=0

check() {
  local dir="$1" file="$2" fmt="$3"
  local got want
  got=$(python3 "$LINT" "$BASE/$dir/$file" --format "$fmt" --min-level info 2>/dev/null \
        | grep -oE '\[(ERROR|WARNING|INFO)\] [a-z-]+' | awk '{print $2}' | sort -u) || true
  want=$(sort -u "$BASE/$dir/EXPECTED.txt" | grep -v '^$' | grep -v '^judgment:')
  if [ "$got" != "$want" ]; then
    echo "FAIL $dir"; echo "got:"; echo "$got"; echo "want:"; echo "$want"; fail=1
  else
    echo "PASS $dir"
  fi
}

check 01-known-bad-draft scenario.md markdown
if python3 "$LINT" "$BASE/01-known-bad-draft/scenario.md" >/dev/null 2>&1; then
  echo "FAIL 01: expected exit code 1"; fail=1
fi
check 02-typst-citation scenario.typ typst
check 03-first-person scenario.md markdown
check 04-hedging-context scenario.md markdown

# 04 must be info level, never error
if python3 "$LINT" "$BASE/04-hedging-context/scenario.md" --min-level error 2>/dev/null | grep -q focsi; then
  echo "FAIL 04 fired above info"; fail=1
fi

# 02a: @key lines stay clean (no citation-missing anywhere)
n=$(python3 "$LINT" "$BASE/02-typst-citation/scenario.typ" --format typst 2>/dev/null | grep -c citation-missing || true)
if [ "$n" != "0" ]; then echo "FAIL 02: citation-missing on @key lines ($n)"; fail=1; fi
# 02b: --against overlap still fires: exactly one quote-required on line 1
q=$(python3 "$LINT" "$BASE/02-typst-citation/scenario.typ" --format typst \
    --against "$BASE/02-typst-citation/source.md" 2>/dev/null | grep -c quote-required || true)
if [ "$q" != "1" ]; then echo "FAIL 02: expected 1 quote-required, got $q"; fail=1; fi

exit $fail