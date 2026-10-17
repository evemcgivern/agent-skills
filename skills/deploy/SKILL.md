---
name: deploy
description: Merge dev to main for production deployment. Repo-agnostic — detects the repo's conventions and defers to any repo-local runbook. Use once daily or when ready to push to production.
allowed-tools: Bash(git:*), Bash(gh:*), Bash(npm:*), Bash(npx:*), Bash(cargo:*), Bash(go:*), Bash(python3:*), Bash(python:*), Bash(jq:*), Bash(grep:*), Bash(sed:*), Bash(awk:*), Bash(comm:*), Bash(tr:*), Bash(sort:*), Bash(head:*), Bash(echo:*)
---

# Deploy to Production (generic)

## Overview

Promote `dev` → `main` (the repo's integration branch → its release branch) for a production deploy. This skill is **repo-agnostic**: it detects each project's conventions and runs the right steps, rather than assuming a specific host, versioning tool, or database. Steps marked **(CONDITIONAL)** only run when the repo actually has that machinery.

**Announce at start:** "Running production deploy."

## Step 0: Detect repo conventions — and defer to any repo-local runbook

**Do this first. Never assume.** A wrong assumption here (squash vs merge, release-please vs none, which remote) corrupts every later step.

```bash
SLUG=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
REMOTE=$(git remote | grep -qx upstream && echo upstream || echo origin)   # primary remote
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
echo "repo=$SLUG remote=$REMOTE default=$DEFAULT_BRANCH"
git branch -a | grep -qE '(^|/)(dev)$' && echo "has dev branch" || echo "NO dev branch"
```

1. **Branch model.** This skill assumes a `dev` → `main` (default) flow. If the repo has **no `dev`** branch (deploys straight from the default branch, or uses `release/*`), STOP and ask the user how they deploy — don't force a dev→main flow.

2. **Defer to a repo-local deploy runbook if one exists.** Check, in order: the project `CLAUDE.md`/`AGENTS.md` for a "Releasing"/"Deploy" section, a project-level `.claude/skills/deploy/`, `CONTRIBUTING.md`, `docs/DEPLOY*`/`RELEASING*`. **If the repo documents its own deploy process, follow THAT** — use this skill only for scaffolding it leaves unspecified. Some repos explicitly forbid generic deploy automation (e.g. a self-contained version-bump flow); honor that.

3. **Detect post-deploy machinery** so you know which conditional steps apply:
   - **Versioning:** release-please (`release-please-config.json` / `.release-please-manifest.json`) · a version-bump GH workflow (`.github/workflows/*version*`, often committing `VERSION`/manifests with `[skip ci]`) · manual `VERSION` · none.
   - **Merge strategy:** release-please and other title-driven changelogs **require `--squash`** (the PR title becomes the changelog commit). Repos that keep `main`/`dev` aligned via merge commits use `--merge`. Match the repo's existing history (`git log $REMOTE/main --merges --oneline | head`); if unknown, default to `--squash`.
   - **DB migrations (CONDITIONAL):** `supabase/migrations/`, `prisma/migrations/`, `migrations/`, etc.
   - **Publish targets (CONDITIONAL):** npm (`package.json` + a publish workflow), a VS Code extension (`vscode/package.json`), Docker, GitHub Release, etc.
   - **Host:** Render/Vercel/Fly/etc. auto-deploy on `main` push, or a manual deploy. Usually inferable from config; not required to proceed.

Record what you found — later steps reference it. Throughout this skill, substitute the real `$REMOTE`/`$SLUG`/`$DEFAULT_BRANCH` you detected (examples below use `origin`/`main`).

## Step 1: Switch to dev and sync remote refs

```bash
git checkout dev && git pull
# Fast-forward local main to match the remote, so every later `main..dev` ref
# compares against fresh upstream state (stale local main produces false-positive
# phantom-drift and wrong PREV_DEPLOY_BASE values).
git fetch "$REMOTE" main:main
```

## Step 1.5: Back-sync async post-deploy artifacts (CONDITIONAL)

**Applies only if the repo's versioning lands commits on `main` only** (a release-please release commit, a `[skip ci]` version/manifest bump, a changelog transform). These are async/manual and drift behind `dev` until the next deploy; if not synced, the next deploy hits a merge conflict on those files.

```bash
git fetch "$REMOTE" main
git log "dev..$REMOTE/main" --oneline --format="%s"
```

Classify what came back:

- **Only the repo's known version/changelog artifacts** (e.g. `chore(version):`/`chore(main): release`/changelog files) → back-merge them, taking main's side on the generated files:
  ```bash
  git merge "$REMOTE/main" --no-edit
  # On conflict, the ONLY expected paths are the generated version/changelog files; take theirs.
  git push "$REMOTE" dev
  ```
- **Any other commit on main** (a hotfix pushed direct to main, an unexpected file) → **STOP and ask the user.** Do not auto-resolve. Recommended framing: if it's docs-only and `git merge --no-commit --no-ff "$REMOTE/main"` is conflict-clean, the safest path is usually to back-merge it before continuing (otherwise every future deploy re-flags it); offer "skip" and "pause deploy" as secondary options.

**Repos with no main-only automation** (the version stamp is part of the squash, or there's no versioning) can skip this step.

## Step 2: Check what's being deployed (phantom-diff aware)

**File diff is necessary but NOT sufficient — also identify what's genuinely new.**

```bash
# All files differing between main and dev (may include phantom diff).
git diff main..dev --stat

# Dev-side commits genuinely NEW since the previous deploy's base.
# Filter out the repo's version/changelog automation commits (adjust the regex to
# the repo's convention), then take the most recent remaining first-parent commit
# on main — that's the previous deploy.
PREV_DEPLOY_BASE=$(git log "$REMOTE/main" --first-parent --format="%H %s" \
  | grep -vE 'chore\(version\)|chore\(main\): release|chore\(changelog\)' \
  | head -1 | awk '{print $1}')
echo "PREV_DEPLOY_BASE: $PREV_DEPLOY_BASE  (confirm this is your last deploy commit)"
git log "$PREV_DEPLOY_BASE..dev" --oneline --no-merges --first-parent
```

**Sanity-check the anchor.** If the first-parent list shows commits older than ~24h since the last deploy, main HEAD is probably a non-deploy commit (a direct-push docs PR, a hotfix the filter missed). Override with the previous deploy PR's merge SHA:
```bash
PREV_DEPLOY_BASE=$(gh pr view <prev-deploy-pr> --repo "$SLUG" --json mergeCommit --jq '.mergeCommit.oid')
```

**PHANTOM DIFF WARNING.** A `--squash` deploy replaces N dev commits with one new-SHA main commit, so the old commits' *content* is on main but their *SHAs* aren't in main's ancestry. The next `git diff main..dev` re-surfaces that content as if new (a one-bugfix deploy can show a 12,000-line diff). **Classify deploy size by the dev-side first-parent commit list, not the file diff.** Cross-reference:
- file diff tiny + commit list huge → phantom; trust the file diff.
- file diff huge + commit list tiny → trust the commit list; the PR title must describe only those commits (re-listing already-shipped features pollutes the changelog).
- both large → genuinely large; both small/zero → minimal/abort if zero.

(Merge-commit deploys, `--merge`, don't create this phantom — but the back-merge in Step 10 keeps `main`/`dev` aligned regardless.)

If `git diff --stat` is empty, abort: "Nothing to deploy."

## Step 3: Build / test gate

Run the repo's gate — whatever its CI requires before merge:
```bash
npm run build        # or: cargo build · go build · python -m unittest discover · npm test · etc.
```
If it fails, abort. Do not deploy a broken build.

### Step 3.5: Pre-Deploy Verification — Version Gates & Realistic-Scale Perf

A green build and passing unit tests do not catch every production regression. Check version compatibility and realistic-scale performance before merging.

**(a) Version/compatibility gates must never point ahead of what THIS deploy ships.** Any "requires version ≥ X" constant — a client gating the API, a mobile companion gating the backend, a feature-flag minimum, an extension gating a CLI — must be **≤ the version this deploy actually stamps**. A gate set to a guessed/future version rejects the very artifact it ships beside, so every updated user hits a false "incompatible / please update" error that updating cannot fix.

```bash
# Surface min-version / compatibility constants touched since the last deploy.
git diff "$PREV_DEPLOY_BASE..dev" \
  -G'(MIN_|_MIN|minVersion|min_version|requires.{0,12}version|COMPAT)' \
  -- '*.ts' '*.tsx' '*.js' '*.py' '*.json' '*.go' '*.rs'
```

For each gate found, confirm it is `≤` the version going out now. If a gate is documented as "set at deploy time," **set it now** — do not ship the placeholder. Where practical, back it with a guard test (`gate ≤ repo version`) so the mistake fails CI, not users.



**(b) Perf-smoke against realistic-scale data, not a toy dataset.** O(n) regressions — N+1 queries, unbounded scans, per-item subprocess/RPC fan-out — are invisible on seed data and brutal in production. Before deploying anything that touches a hot path (a list/query/render that runs on load), time it against **production-scale volume**:

- Run a `performance-test` skill if the repo has one, or time the touched endpoint/query/command against a prod-sized fixture (not the dev seed).
- Specifically hunt for work that is O(rows × something): a per-row query, a per-record external call, a loop that re-scans, the same expensive read repeated per item instead of memoized once.


## Step 4: Determine commit type + PR title

The squash commit's title is what a title-driven changelog (release-please, a version-bump workflow) reads, and it's what users see as the release note. Make it real.

1. Scan dev-side commits since the last deploy for prefixes — bound by **time**, not the `main..dev` range (which walks dev's whole feature line):
   ```bash
   git log dev --first-parent --no-merges \
     --since="$(git log -1 --format=%cI "$PREV_DEPLOY_BASE")" --oneline
   ```
2. Pick the highest-priority conventional type present: `feat` > `fix` > `perf` > `refactor` > `chore`.
3. Collect scopes from commits that touch files actually in the diff.

**The title must describe what shipped** — `chore: deploy to production` produces an empty changelog. Good: `feat(graph,detail): blocked-by surfacing + dep chips`.

## Step 5: Create the deploy PR (dev → main)

```bash
gh pr create --base main --head dev \
  --title "<type>(<scopes>): <2-3 key changes>" \
  --body "<summary + the genuinely-new commit list from Step 2>"
```
If the repo's versioning derives the changelog from the PR body (e.g. a version-bump workflow), write the body **as the changelog entry**.

## Step 6: Wait for CI checks

```bash
gh pr checks <pr-number> --watch --repo "$SLUG"
```
If checks fail: stop, report, do not merge.

## Step 7: Merge

Use the repo's convention (from Step 0):
```bash
gh pr merge <pr-number> --squash --admin   # title-driven changelog / release-please
# OR
gh pr merge <pr-number> --merge  --admin   # repos that keep main/dev aligned via merge commits
```
`--admin` bypasses approval for a solo/CI-gated workflow (checks already passed). Prefer not to use `--admin` if the repo requires review by policy — ask.

## Step 8: Verify merged

```bash
gh pr view <pr-number> --json state --jq '.state'   # expect MERGED
```

If the repo stamps version async (release-please PR, or a `version-bump` workflow firing on merge), wait for that commit to land on main before publishing:
```bash
# Poll until the version/changelog commit appears, e.g.:
gh api "repos/$SLUG/commits/main" --jq '.commit.message' | head -1
```

## Step 8.5: Post-deploy actions (CONDITIONAL — only what the repo has)

Run only the ones that apply (from Step 0):

- **DB migrations** — if the host auto-deploys code but not schema, apply pending migrations immediately after merge, **gated on explicit user confirmation; never auto-apply** (they can't be rolled back by a PR revert):
  ```bash
  npx supabase db push        # or: npx prisma migrate deploy · etc.
  ```
  Report the migration status in the final summary either way (silence here has caused schema-cache outages).
- **Package/artifact publishes** — npm, VS Code extension, Docker, GitHub Release — via the repo's workflows (e.g. `gh workflow run npm-publish.yml --ref main -f dry_run=false`). Mind same-day version collisions (date-derived versions may need a suffix; hand-set extension versions must be bumped per publish).
- **Back-merge the async version stamp** into dev (see Step 10) so the next deploy doesn't drift.

## Step 9: Close referenced issues (CONDITIONAL)

Squash merges don't honor `Closes #X` from the PR body, and merges to a non-default branch don't auto-close. If the repo relies on manual closing, extract issue numbers from **dev-side work since the last deploy, bounded by TIME** (not a SHA range — dev's first-parent line diverges from main and over-reports):

```bash
T_PREV=$(git log -1 --format=%cI "$PREV_DEPLOY_BASE")
gh pr list --repo "$SLUG" --base dev --state merged --limit 200 \
  --json number,title,body,mergedAt --jq "[.[] | select(.mergedAt > \"$T_PREV\")]" > /tmp/deploy-prs.json
```

Two-pass extraction — **only auto-close on an explicit closure directive at line start**; log the rest for review (bare contextual `#N` mentions have silently closed in-flight issues before):

```bash
CORPUS=$(jq -r '.[] | .title + "\n" + (.body // "")' /tmp/deploy-prs.json)
CLOSURE_NUMS=$(echo "$CORPUS" \
  | grep -oE '^[-*[:space:]]*(Close|Closes|Closed|Fix|Fixes|Fixed|Resolve|Resolves|Resolved)( by)?:?[[:space:]]+#[0-9]+' \
  | grep -oE '#[0-9]+' | tr -d '#' | sort -n -u)
# Everything else: log for manual review, do NOT close.
ALL_NUMS=$(echo "$CORPUS" | grep -oE '#[0-9]+' | tr -d '#' | sort -n -u)
comm -23 <(echo "$ALL_NUMS") <(echo "$CLOSURE_NUMS") | sed 's/^/  review: #/'
```

Close only the ones that are genuinely OPEN issues (the state check skips PR numbers):
```bash
for num in $CLOSURE_NUMS; do
  [ "$(gh issue view "$num" --repo "$SLUG" --json state --jq .state 2>/dev/null)" = OPEN ] \
    && gh issue close "$num" --repo "$SLUG" --comment "Shipped in #<deploy-pr>." --reason completed
done
```

## Step 10: Back-merge main → dev (align after the deploy)

A `--squash` deploy (or an async version stamp) leaves main with commits dev lacks. Back-merge so future `git diff main..dev` is clean and the next deploy's anchors stay correct:
```bash
git checkout dev
git fetch "$REMOTE" main
git merge --no-ff "$REMOTE/main" -m "chore(deploy): back-merge main after #<deploy-pr>"
git push "$REMOTE" dev
git diff main..dev --stat   # should be empty / near-empty; if real content, STOP and investigate
```

## Step 11: Return to dev

```bash
git checkout dev && git pull
```

## Step 12: Report

```
Deploy complete:
- Repo / PR: <slug> #<num> (<url>)
- Files changed: <count> (+<ins>/-<del>)
- Version: <stamped version, or "n/a">
- Publishes: <npm@x / extension vY / none>
- Migrations: <none / applied <list> / PENDING — user declined>
- Host: <auto-deploys from main / manual>
```

Always state the migration and publish status explicitly — even "none."

## Flags

- `--dry-run` — show what would deploy without merging.
- `--force` — skip the build gate (emergency hotfix only).

## Error Handling

| Error | Action |
|-------|--------|
| No `dev` branch / unfamiliar branch model | STOP at Step 0; ask the user how they deploy. |
| Repo has its own deploy runbook | Follow it; use this skill only for gaps. |
| Build/test fails | Stop. Fix on dev, retry. |
| Nothing to deploy | Abort. |
| Unexpected commit on main (Step 1.5) | STOP and ask; don't auto-resolve. |
| Version gate ahead of deploy (Step 3.5a) | Fix the gate before merging; don't ship the placeholder. |
| Scale-perf regression (Step 3.5b) | Fix (batch/memoize/index) before merging; a hot path that's slow at scale is a production incident. |
| Pending migrations (Step 8.5) | Surface; wait for explicit confirmation; never auto-apply. |
| Publish version collision | Bump/suffix per the registry's rule; don't silently no-op. |
