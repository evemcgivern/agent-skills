#!/usr/bin/env bash
# exposure-scan: match installed packages against bumblebee threat-intel exposure catalogs.
#
# Usage:
#   scan.sh                 # quick scan (baseline roots, ~13s) — DEFAULT
#   scan.sh quick           # same as above
#   scan.sh deep            # thorough $HOME walk (slower, broader)
#   scan.sh project <path>  # scan one project/dir tree
#   scan.sh refresh         # pull latest catalogs from GitHub main into local cache
#   scan.sh catalogs        # show which catalogs would be used and their entry counts
#
# Exit codes: 0 = clean, 2 = findings present, 1 = setup/usage error.

set -euo pipefail

REPO="perplexityai/bumblebee"
LOCAL_CAT="${BUMBLEBEE_CATALOG_DIR:-$HOME/.config/bumblebee/threat_intel}"

# --- ensure bumblebee is reachable (go install drops it in GOPATH/bin) ---
export PATH="$(go env GOPATH 2>/dev/null || echo "$HOME/go")/bin:$PATH"
if ! command -v bumblebee >/dev/null 2>&1; then
  echo "ERROR: 'bumblebee' not on PATH. Install with:" >&2
  echo "  go install github.com/${REPO}/cmd/bumblebee@latest" >&2
  echo "  export PATH=\"\$HOME/go/bin:\$PATH\"   # add to ~/.zshrc" >&2
  exit 1
fi

# --- resolve which catalog directory to use ---
# Prefer the refreshable local cache; fall back to the version-pinned module cache.
resolve_catalogs() {
  if [ -d "$LOCAL_CAT" ] && ls "$LOCAL_CAT"/*.json >/dev/null 2>&1; then
    echo "$LOCAL_CAT"; return 0
  fi
  local gomod bundled
  gomod="$(go env GOMODCACHE 2>/dev/null || echo "$HOME/go/pkg/mod")"
  # highest installed bumblebee version that ships a threat_intel dir
  bundled="$(ls -d "$gomod"/github.com/perplexityai/bumblebee@*/threat_intel 2>/dev/null | sort -V | tail -1 || true)"
  if [ -n "$bundled" ] && ls "$bundled"/*.json >/dev/null 2>&1; then
    echo "$bundled"; return 0
  fi
  return 1
}

# --- verify all catalogs share one schema_version (merge requirement) ---
validate_catalogs() {
  local dir="$1"
  python3 - "$dir" <<'PY'
import json, sys, glob, os
d = sys.argv[1]
schemas, total, files = set(), 0, 0
for f in sorted(glob.glob(os.path.join(d, "*.json"))):
    try:
        c = json.load(open(f))
    except Exception as e:
        print(f"  ! unreadable: {os.path.basename(f)} ({e})"); continue
    files += 1
    schemas.add(c.get("schema_version"))
    n = len(c.get("entries", []))
    total += n
    print(f"  - {os.path.basename(f):40} schema {c.get('schema_version')}  {n:>4} entries")
print(f"  = {files} catalogs, {total} known-compromised entries")
if len(schemas) > 1:
    print(f"  ! WARNING: mixed schema_versions {schemas} — bumblebee merge will reject. "
          f"Refresh or remove the odd file out.")
    sys.exit(3)
PY
}

# --- refresh catalogs from GitHub main (auto-discovers new catalog files) ---
refresh() {
  echo "Refreshing exposure catalogs from github.com/${REPO} (branch: main) -> $LOCAL_CAT"
  mkdir -p "$LOCAL_CAT"
  local api="https://api.github.com/repos/${REPO}/contents/threat_intel"
  local urls
  urls="$(curl -fsSL "$api" \
    | python3 -c "import json,sys; [print(f['download_url']) for f in json.load(sys.stdin) if f['name'].endswith('.json')]")" \
    || { echo "ERROR: could not list catalogs (offline or GitHub rate-limited). Bundled catalogs still work." >&2; exit 1; }
  local n=0
  while IFS= read -r url; do
    [ -z "$url" ] && continue
    curl -fsSL "$url" -o "$LOCAL_CAT/$(basename "$url")" && n=$((n+1))
  done <<< "$urls"
  echo "Pulled $n catalog file(s)."
  validate_catalogs "$LOCAL_CAT" || true
}

# --- pretty-print findings, loud banner on hits ---
report() {
  local findings_file="$1"
  python3 - "$findings_file" <<'PY'
import json, sys
hits, summary = [], None
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    r = json.loads(line)
    if r.get("record_type") == "scan_summary":
        summary = r; continue
    hits.append(r)
if summary:
    c = summary.get("counts", {})
    print(f"  scanned: {summary.get('files_considered'):,} files | "
          f"matched packages: {c.get('package', 0)} | duration: {summary.get('duration_ms')}ms")
if not hits:
    print("\n  ✅ CLEAN — no installed package matches a known-compromised release.\n")
    sys.exit(0)
order = {"critical": 0, "high": 1, "medium": 2, "low": 3, None: 4}
hits.sort(key=lambda r: order.get(r.get("severity"), 5))
print(f"\n  \U0001f6a8 {len(hits)} EXPOSURE FINDING(S) — known-compromised packages installed:\n")
for r in hits:
    sev = (r.get("severity") or "?").upper()
    print(f"  [{sev}] {r.get('ecosystem')}:{r.get('package_name')}@{r.get('version')}")
    print(f"        campaign : {r.get('catalog_name') or r.get('catalog_id')}")
    print(f"        evidence : {r.get('evidence')}")
    print(f"        found in : {r.get('source_file')}\n")
print("  Action: remove/downgrade these packages, rotate any exposed credentials,")
print("  and review the campaign report for the named catalog.\n")
sys.exit(2)
PY
}

# --- run a scan ---
do_scan() {
  local mode="$1"; shift || true
  local cat
  if ! cat="$(resolve_catalogs)"; then
    echo "ERROR: no exposure catalogs found. Run: scan.sh refresh" >&2
    exit 1
  fi
  echo "Catalogs: $cat"
  local tmp; tmp="$(mktemp -t exposure-findings.XXXXXX.ndjson)"
  # EXIT traps fire in global scope where `tmp` (local) is gone — guard with ${tmp:-} under set -u.
  trap 'rm -f "${tmp:-}"' EXIT

  local -a args=(scan --exposure-catalog "$cat" --findings-only)
  case "$mode" in
    quick) args+=(--profile baseline) ;;
    deep)  args+=(--profile deep --root "$HOME" --max-duration 10m) ;;
    project)
      local path="${1:-$PWD}"
      args+=(--profile deep --root "$path" --max-duration 5m)
      echo "Target: $path" ;;
    *) echo "Unknown mode: $mode" >&2; exit 1 ;;
  esac

  echo "Running: bumblebee ${args[*]}"
  bumblebee "${args[@]}" > "$tmp" 2>/dev/null || true
  report "$tmp"
}

cmd="${1:-quick}"
case "$cmd" in
  quick|deep) do_scan "$cmd" ;;
  project)    shift; do_scan project "${1:-$PWD}" ;;
  refresh)    refresh ;;
  catalogs)
    if c="$(resolve_catalogs)"; then echo "Using: $c"; validate_catalogs "$c"; else
      echo "No catalogs found. Run: scan.sh refresh"; exit 1; fi ;;
  -h|--help|help)
    sed -n '2,16p' "$0" ;;
  *) echo "Unknown command: $cmd (try: quick | deep | project <path> | refresh | catalogs)" >&2; exit 1 ;;
esac
