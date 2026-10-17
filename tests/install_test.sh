#!/usr/bin/env bash
# Exercise scripts/install.sh against throwaway directories.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$ROOT/scripts/install.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail() { echo "FAIL: $*" >&2; exit 1; }

n=$("$INSTALL" --list | wc -l | tr -d ' ')
[ "$n" -ge 20 ] || fail "--list returned $n skills"

"$INSTALL" --target claude --project "$tmp/a" cdf clearly >/dev/null
[ -f "$tmp/a/.claude/skills/cdf/SKILL.md" ] || fail "claude project install missing deploy"
[ -f "$tmp/a/.claude/skills/clearly/SKILL.md" ] || fail "claude project install missing pr-wait"

"$INSTALL" --target codex --project "$tmp/b" --all >/dev/null
count=$(find "$tmp/b/.agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
[ "$count" -eq "$n" ] || fail "codex --all installed $count of $n"

out=$("$INSTALL" --target claude --project "$tmp/a" cdf)
echo "$out" | grep -q "skip cdf" || fail "existing skill was not skipped"
touch "$tmp/a/.claude/skills/cdf/stale"
"$INSTALL" --target claude --project "$tmp/a" --force cdf >/dev/null
[ ! -e "$tmp/a/.claude/skills/cdf/stale" ] || fail "--force did not replace the folder"

for bad in nope "../x" "*" "a/b"; do
  if "$INSTALL" --project "$tmp/c" --force "$bad" >/dev/null 2>&1; then fail "bad name $bad should exit non-zero"; fi
done
if "$INSTALL" --project "$tmp/c" nope >/dev/null 2>&1; then fail "unknown skill should exit non-zero"; fi
if "$INSTALL" --target bogus --all >/dev/null 2>&1; then fail "bad target should exit non-zero"; fi
echo "OK: install script"
