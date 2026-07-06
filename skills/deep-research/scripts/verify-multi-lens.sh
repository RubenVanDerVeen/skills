#!/usr/bin/env bash
# verify-multi-lens.sh — run after writing the three self-passes + dossier
# to confirm the verification checklist from multi-lens-synthesis SKILL.md is satisfied.
#
# Usage: bash verify-multi-lens.sh <dossier_dir>
# Example: bash verify-multi-lens.sh ~/research/dossiers/diffusion-policies-2025
#
# Exit 0 = all checks pass. Exit 1 = at least one check failed.

set -u

if [ $# -lt 1 ]; then
  echo "Usage: $0 <dossier_dir>"
  exit 2
fi

DIR="$1"
ARTIFACTS="$DIR/artifacts"
pass=0
fail=0

check() {
  local label="$1"
  local path="$2"
  if [ -e "$path" ]; then
    echo "  PASS  $label"
    pass=$((pass + 1))
  else
    echo "  FAIL  $label  (missing: $path)"
    fail=$((fail + 1))
  fi
}

check_grep() {
  local label="$1"
  local path="$2"
  local pattern="$3"
  if [ -e "$path" ] && grep -qE "$pattern" "$path"; then
    echo "  PASS  $label"
    pass=$((pass + 1))
  else
    echo "  FAIL  $label  (missing pattern '$pattern' in $path)"
    fail=$((fail + 1))
  fi
}

echo "Multi-lens synthesis verification: $DIR"
echo

# Existence checks
check "Pass 1 file exists"      "$ARTIFACTS/self-pass-1-academic.md"
check "Pass 2 file exists"      "$ARTIFACTS/self-pass-2-industry.md"
check "Pass 3 file exists"      "$ARTIFACTS/self-pass-3-synthesis.md"
check "Final dossier exists"    "$DIR/dossier.md"

# Pass 1 content
check_grep "Pass 1 has 'push back' section" \
  "$ARTIFACTS/self-pass-1-academic.md" \
  "[Pp]ush [Bb]ack|[Pp]ushback"

# Pass 2 content
check_grep "Pass 2 has CEO/end-user memo" \
  "$ARTIFACTS/self-pass-2-industry.md" \
  "## 8\\. What I would tell|CEO memo|memo"

# Pass 3 content
check_grep "Pass 3 has 'what nobody said' or 'honest gaps' section" \
  "$ARTIFACTS/self-pass-3-synthesis.md" \
  "[Ww]hat nobody said|[Hh]onest gaps"

# Dossier references the passes
check_grep "Dossier references self-passes in Methodology" \
  "$DIR/dossier.md" \
  "self-pass|Multi-lens|three sequential"

# Optional: A/B model task produces the comparison artifact
if [ -e "$ARTIFACTS/model-comparison.md" ] || [ -e "$ARTIFACTS/model-judgement.md" ]; then
  echo "  PASS  A/B model task produced model-comparison.md or model-judgement.md"
  pass=$((pass + 1))
else
  echo "  INFO  No A/B model artifact found (expected for non-A/B tasks)"
fi

echo
echo "Result: $pass passed, $fail failed"
exit $fail
