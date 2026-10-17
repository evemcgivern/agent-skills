#!/usr/bin/env bash
# spec-review.sh — run a Codex second-model review against a spec/plan document.
# Does for specs what `/codex:review` does for PRs: a rigorous, repo-grounded
# review by a different model, returned verbatim. Read-only (never edits).
#
# Usage:
#   spec-review.sh [TARGET] [-- extra focus text ...]
#
#   TARGET (optional):
#     - a spec FILE         e.g. docs/superpowers/specs/2026-05-30-foo-design.md
#     - a spec FOLDER       e.g. .spec-workflow/specs/MVP-plot-lifecycle
#                           (bundles requirements.md + design.md + tasks.md)
#     - a bare NAME         e.g. plot-lifecycle  (searched across known spec dirs)
#     - omitted             → auto-detect the most-recently-modified spec
#
#   Anything after `--` is appended to the review prompt as extra focus.
#
# Env:
#   SPEC_REVIEW_MODEL    override Codex model (default: codex's configured default)
#   SPEC_REVIEW_DIRS     colon-separated extra dirs to search for auto-detect
set -euo pipefail

# ---- locate repo root (so Codex can verify claims against the codebase) ----
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

# ---- parse args: TARGET before `--`, focus text after ----
TARGET=""
FOCUS=""
seen_dd=0
for arg in "$@"; do
  if [[ "$seen_dd" == "1" ]]; then
    FOCUS+="${FOCUS:+ }$arg"
  elif [[ "$arg" == "--" ]]; then
    seen_dd=1
  elif [[ -z "$TARGET" ]]; then
    TARGET="$arg"
  else
    FOCUS+="${FOCUS:+ }$arg"
  fi
done

# ---- candidate spec dirs for auto-detect / bare-name resolution ----
CANDIDATE_DIRS=(
  ".spec-workflow/specs"
  "docs/superpowers/specs"
  "docs/superpowers/plans"
  "docs/specs"
  "docs/plans"
  "specs"
  "plans"
)
if [[ -n "${SPEC_REVIEW_DIRS:-}" ]]; then
  IFS=':' read -r -a EXTRA <<< "$SPEC_REVIEW_DIRS"
  CANDIDATE_DIRS=("${EXTRA[@]}" "${CANDIDATE_DIRS[@]}")
fi

# ---- resolve TARGET → list of files to review ----
declare -a FILES=()
LABEL=""

bundle_dir() {
  local dir="$1"
  local f
  for f in requirements.md design.md tasks.md; do
    [[ -f "$dir/$f" ]] && FILES+=("$dir/$f")
  done
  if [[ ${#FILES[@]} -eq 0 ]]; then
    while IFS= read -r f; do FILES+=("$f"); done < <(find "$dir" -maxdepth 1 -name '*.md' | sort)
  fi
  LABEL="$dir"
}

if [[ -n "$TARGET" && -f "$TARGET" ]]; then
  FILES=("$TARGET"); LABEL="$TARGET"
elif [[ -n "$TARGET" && -d "$TARGET" ]]; then
  bundle_dir "$TARGET"
elif [[ -n "$TARGET" ]]; then
  # bare name: search candidate dirs for a matching file or folder
  hit=""
  for d in "${CANDIDATE_DIRS[@]}"; do
    [[ -d "$d" ]] || continue
    if [[ -d "$d/$TARGET" ]]; then hit="$d/$TARGET"; break; fi
    m="$(find "$d" -maxdepth 1 -iname "*$TARGET*.md" | sort | head -1 || true)"
    if [[ -n "$m" ]]; then hit="$m"; break; fi
  done
  if [[ -z "$hit" ]]; then
    echo "spec-review: no spec matching '$TARGET' found in: ${CANDIDATE_DIRS[*]}" >&2
    exit 2
  fi
  if [[ -d "$hit" ]]; then bundle_dir "$hit"; else FILES=("$hit"); LABEL="$hit"; fi
else
  # auto-detect: newest *.md across candidate dirs (folder specs: newest design.md/requirements.md)
  newest=""
  for d in "${CANDIDATE_DIRS[@]}"; do
    [[ -d "$d" ]] || continue
    while IFS= read -r f; do
      [[ -z "$newest" || "$f" -nt "$newest" ]] && newest="$f"
    done < <(find "$d" -type f -name '*.md' 2>/dev/null)
  done
  if [[ -z "$newest" ]]; then
    echo "spec-review: no specs found. Pass a TARGET path explicitly." >&2
    exit 2
  fi
  # if the newest file lives in a folder-spec, bundle the whole folder
  parent="$(dirname "$newest")"
  if [[ -f "$parent/design.md" || -f "$parent/requirements.md" || -f "$parent/tasks.md" ]]; then
    bundle_dir "$parent"
  else
    FILES=("$newest"); LABEL="$newest"
  fi
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "spec-review: resolved target '$LABEL' but found no .md files to review." >&2
  exit 2
fi

# ---- assemble the spec payload (guarantees content reaches Codex via stdin) ----
PAYLOAD="$(mktemp -t spec-review-payload.XXXXXX)"
trap 'rm -f "$PAYLOAD"' EXIT
for f in "${FILES[@]}"; do
  {
    echo "===== FILE: $f ====="
    cat "$f"
    echo
  } >> "$PAYLOAD"
done

FILE_LIST="$(printf '  - %s\n' "${FILES[@]}")"

# ---- the review prompt: spec-world analog of "find the bugs" ----
read -r -d '' PROMPT <<PROMPT_EOF || true
You are a rigorous, skeptical spec reviewer. Review the SPECIFICATION supplied
in the <stdin> block. This is a design/plan document, NOT a code diff. Your job
is to find what is wrong, missing, ambiguous, or unverified — the spec-world
analog of finding bugs — and to return a verdict VERBATIM with no fixes applied.

The spec lives at these path(s) in the current repo:
$FILE_LIST

CRITICAL — VERIFY CLAIMS AGAINST THE ACTUAL CODEBASE. You have read-only access
to this repository. Do not reason forward from the spec's stated assumptions.
For every claim the spec makes about existing tables, columns, relationships,
functions, routes, types, or component behavior, OPEN the real source and check
it. Grep migrations, schema, and type files. The single most expensive class of
spec defect is a data-model claim that is wrong — especially treating a
many-to-many relationship as if it were a singular scalar (e.g. "the content's
campaign" when content↔campaign is M2M via a junction table). Flag every
relationship the spec assumes is scalar that is actually a set, and vice versa.

Review for these defect classes:
1. UNVERIFIED DATA-MODEL CLAIMS — tables/columns/relationships asserted but not
   matching the real schema; scalar-vs-M2M confusion. Cite the file you checked.
2. UNTESTED ASSUMPTIONS — claims about current behavior, APIs, or libraries not
   grounded in the actual code.
3. MISSING / WEAK ACCEPTANCE CRITERIA — is "done" measurable and testable? What
   would a reviewer run to confirm it works?
4. AMBIGUITY — terms used inconsistently or left undefined; pronouns/references
   with unclear antecedents; two readings that imply different implementations.
5. SCOPE — hidden scope creep; under-specified edges; what is explicitly OUT of
   scope and is that boundary clean?
6. INTERNAL CONTRADICTIONS — section X contradicts section Y or the data model.
7. DEPENDENCIES & ORDERING — depends on unbuilt things; migration idempotency
   and ordering; feature-flag / rollback story.
8. SECURITY & COMPLIANCE — auth, row-level security, input/output trust
   boundaries, and any project-specific compliance rules visible in repo docs
   (e.g. CLAUDE.md). Note violations.
9. TESTABILITY & ROLLOUT — how is this verified, gated, and reverted?

OUTPUT FORMAT (markdown):
- One-line VERDICT: SHIP / SHIP WITH CHANGES / DO NOT SHIP — plus a one-sentence why.
- Findings as a list, each tagged [CRITICAL] / [HIGH] / [MEDIUM] / [LOW], each
  with: the claim or gap, the evidence (cite spec section AND, where you checked
  code, the file:line you verified against), and a concrete recommended change.
- A short "Verified OK" list of important claims you checked that ARE correct.
- If you could not verify a claim because the code was not found, say so
  explicitly rather than assuming.
Be specific and terse. Reward precision over volume. Do not propose to edit any
files — review only.
PROMPT_EOF

if [[ -n "$FOCUS" ]]; then
  PROMPT+=$'\n\nADDITIONAL FOCUS FROM REVIEWER: '"$FOCUS"
fi

# ---- run Codex read-only; capture clean final message via -o ----
OUT="$(mktemp -t spec-review-out.XXXXXX)"
ERR="$(mktemp -t spec-review-err.XXXXXX)"
trap 'rm -f "$PAYLOAD" "$OUT" "$ERR"' EXIT

MODEL_ARGS=()
[[ -n "${SPEC_REVIEW_MODEL:-}" ]] && MODEL_ARGS=(-m "$SPEC_REVIEW_MODEL")

# Disable Codex's bundled automation plugins for this read-only review run so
# they never request macOS Automation/AppleScript control ("X wants to control
# Codex Computer Use.app"). Reading a spec needs neither computer-use nor the
# browser plugin. Scoped to THIS invocation — the user's global
# ~/.codex/config.toml is untouched.
PLUGIN_OVERRIDES=(
  -c 'plugins."computer-use@openai-bundled".enabled=false'
  -c 'plugins."chrome@openai-bundled".enabled=false'
)

echo "spec-review: reviewing → $LABEL" >&2
echo "spec-review: ${#FILES[@]} file(s), repo root $REPO_ROOT" >&2
echo "spec-review: invoking codex exec (read-only)…" >&2

# stdin carries the spec content; Codex appends it as a <stdin> block.
# stderr (MCP/auth noise) is captured to $ERR so a failure can be DIAGNOSED
# (not discarded); the clean verdict is written to $OUT.
set +e
codex exec \
  --sandbox read-only \
  --cd "$REPO_ROOT" \
  "${PLUGIN_OVERRIDES[@]}" \
  ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} \
  -o "$OUT" \
  "$PROMPT" < "$PAYLOAD" 2>"$ERR"
CODEX_RC=$?
set -e

# Codex can exit 0 yet produce NO verdict (e.g. an auth-token refresh failure
# prints a 401 to stderr but still returns 0), so an empty $OUT is also a failure.
if [[ $CODEX_RC -ne 0 || ! -s "$OUT" ]]; then
  echo "spec-review: codex produced no verdict (exit $CODEX_RC)." >&2
  if grep -qiE "invalid_grant|refresh token|token_invalidated|\b401\b|Unauthorized|could not be refreshed|sign ?in again" "$ERR"; then
    echo "  → Codex auth is stale/expired. Fix: 'codex logout && codex login', then confirm with 'echo hi | codex exec'." >&2
  elif grep -qiE "model .*not supported|unsupported.*model|invalid model|not supported when using" "$ERR"; then
    echo "  → The configured Codex model is unsupported for this account. Set SPEC_REVIEW_MODEL to a supported one (e.g. 'gpt-5')." >&2
  else
    echo "  → Codex stderr (noise filtered, last 15 lines):" >&2
    grep -vE "rmcp::transport|codex_api::endpoint|codex_memories|^hook:|SessionStart|UserPromptSubmit" "$ERR" | tail -15 >&2
  fi
  exit 1
fi

echo "=================== CODEX SPEC REVIEW: $LABEL ==================="
cat "$OUT"
