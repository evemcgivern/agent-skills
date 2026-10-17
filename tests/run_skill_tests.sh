#!/usr/bin/env bash
# Run every skill's bundled unit tests (plugins/*/skills/*/tests and
# plugins/*/skills/*/scripts/tests). Fails if any suite fails or finds 0 tests.
# Run from anywhere:  bash tests/run_skill_tests.sh
set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
suites=0
failed=0

for dir in "$root"/plugins/*/skills/*/tests "$root"/plugins/*/skills/*/scripts/tests; do
  [ -d "$dir" ] || continue
  found=0
  for file in "$dir"/test_*.py; do
    [ -f "$file" ] && found=1
  done
  [ "$found" -eq 1 ] || continue

  suites=$((suites + 1))
  rel="${dir#"$root"/}"
  echo "== $rel"
  if ! output="$(cd "$dir" && python3 -m unittest discover -s . -t . 2>&1)"; then
    printf '%s\n' "$output"
    echo "FAIL: $rel"
    failed=$((failed + 1))
    continue
  fi
  printf '%s\n' "$output" | tail -n 3
  ran="$(printf '%s\n' "$output" | sed -n 's/^Ran \([0-9][0-9]*\) tests\{0,1\} .*/\1/p' | tail -n 1)"
  if [ -z "$ran" ] || [ "$ran" -eq 0 ]; then
    echo "FAIL: $rel discovered 0 tests"
    failed=$((failed + 1))
  fi
done

if [ "$suites" -eq 0 ]; then
  echo "FAIL: no skill test suites found"
  exit 1
fi
if [ "$failed" -ne 0 ]; then
  echo "FAIL: $failed of $suites skill test suite(s) failed"
  exit 1
fi
echo "OK: $suites skill test suite(s) passed"
