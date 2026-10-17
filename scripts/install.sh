#!/usr/bin/env bash
# Copy skills from this repo into a Claude Code or Codex skills folder.
#
# Usage:
#   scripts/install.sh --list
#   scripts/install.sh [--target claude|codex] [--project DIR] [--force] <skill>... | --all
#
# Targets:  claude -> ~/.claude/skills     codex -> ~/.agents/skills
# --project DIR installs into DIR/.claude/skills or DIR/.agents/skills instead.
# Existing skill folders are skipped unless --force is given.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target=claude
project=""
force=0
all=0
list=0
skills=()

usage() { sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --target) target="${2:?--target needs claude or codex}"; shift 2 ;;
    --project) project="${2:?--project needs a directory}"; shift 2 ;;
    --force) force=1; shift ;;
    --all) all=1; shift ;;
    --list) list=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "unknown option: $1" >&2; usage >&2; exit 1 ;;
    *) skills+=("$1"); shift ;;
  esac
done

available=()
for d in "$ROOT"/plugins/*/skills/*/; do
  [ -f "$d/SKILL.md" ] && available+=("$(basename "$d")")
done

if [ "$list" -eq 1 ]; then
  printf '%s\n' "${available[@]}"
  exit 0
fi

case "$target" in
  claude) sub=".claude/skills"; home_dir="$HOME/.claude/skills" ;;
  codex)  sub=".agents/skills"; home_dir="$HOME/.agents/skills" ;;
  *) echo "unknown target: $target (use claude or codex)" >&2; exit 1 ;;
esac
dest="$home_dir"
[ -n "$project" ] && dest="$project/$sub"

[ "$all" -eq 1 ] && skills=("${available[@]}")
if [ "${#skills[@]}" -eq 0 ]; then
  echo "no skills given; use --all or name skills (see --list)" >&2
  exit 1
fi

mkdir -p "$dest"
status=0
for s in "${skills[@]}"; do
  case "$s" in
    ""|*[!A-Za-z0-9._-]*|.|..|-*) echo "invalid skill name: $s" >&2; status=1; continue ;;
  esac
  src=$(compgen -G "$ROOT/plugins/*/skills/$s" | head -n 1 || true)
  if [ -z "$src" ] || [ ! -f "$src/SKILL.md" ]; then
    echo "not found: $s" >&2; status=1; continue
  fi
  if [ -e "$dest/$s" ] && [ "$force" -ne 1 ]; then
    echo "skip $s (exists in $dest; use --force to replace)"; continue
  fi
  rm -rf "${dest:?}/$s"
  cp -R "$src" "$dest/$s"
  echo "installed $s -> $dest/$s"
done
exit "$status"
