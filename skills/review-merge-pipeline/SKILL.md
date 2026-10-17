---
name: review-merge-pipeline
description: Automated pipeline that code-reviews uncommitted changes, fixes issues found, commits, pushes, creates a PR, and merges with --admin. Accepts an optional worktree path argument and flags --no-review / --no-merge / --rebase / --cross-model. Use when work is done and you want to ship it without manual steps.
---

# Review-Merge Pipeline

## Overview

One-shot pipeline: **code review → fix → commit → push → PR → merge**. No manual steps, no questions — just ship it.

**Announce at start:** "Running the review-merge pipeline."

## Prerequisites

Before running this pipeline, verify:
1. You're on a feature branch (not `main`/`master`/`dev`) — if on main or dev, abort with: "Cannot run pipeline on main/dev. Create a feature branch first."
2. There are staged or unstaged changes, or unpushed commits — if nothing to ship, abort with: "Nothing to ship."

**Merge target:** All PRs target `dev` (not `main`). Production deploys happen via `/deploy` (dev → main merge, once daily).

## The Pipeline

### Step 0: Handle Worktree Argument (Optional)

The skill accepts an optional worktree path as its first argument:

```
/review-merge-pipeline .worktrees/my-feature
/review-merge-pipeline /absolute/path/to/worktree
```

**If a path argument is provided:**

1. Resolve to an absolute path and verify it exists:
   ```bash
   WT_PATH="$(cd "$ARG" 2>/dev/null && pwd)" || { echo "Path does not exist: $ARG"; exit 1; }
   ```
2. Verify it's a registered git worktree:
   ```bash
   git worktree list --porcelain | grep -q "^worktree $WT_PATH$" || { echo "Not a registered git worktree: $WT_PATH. Run 'git worktree list' to see registered worktrees."; exit 1; }
   ```
3. Remember the caller's directory so the final cleanup step can return there:
   ```bash
   ORIGINAL_PWD="$(pwd)"
   cd "$WT_PATH"
   ```
4. All subsequent pipeline steps (build check, review, commit, push, PR, merge) run **inside the worktree**.

**If no argument is provided:** The pipeline runs in the current working directory (original behavior — no change).

**Why this matters:** Worktrees let you ship a completed branch without disturbing another feature branch you're working on in the primary checkout. The post-merge step (Return to Dev) is worktree-aware — see Step 8.

### Step 1: Build Check

Run the project's build command to catch type errors before review:

```bash
npm run build  # or cargo build, go build, etc.
```

**If build fails:** Fix the errors, re-run build. Do NOT proceed to review with a broken build.

### Step 2: Code Review

Launch the `pr-review-toolkit:code-reviewer` agent to review all uncommitted changes (or all commits on the branch if already committed).

Pass the agent a clear description of what changed and why, plus `git diff` output.

Focus the review on:
- Bugs and logic errors
- Security vulnerabilities
- Accessibility issues
- Project convention violations (check CLAUDE.md)

**If `--cross-model` flag is set:** ALSO dispatch a parallel review via Codex's native `review` subcommand. Codex catches a different class of issues than the layered Claude reviewer (different model = different blind spots). Run in the SAME message as the layered review, not after, so both run in parallel:

```bash
codex review --uncommitted "<context paragraph: what changed and why, including specific things to weigh>"
```

For post-commit pipelines (most common), use `--base` instead:

```bash
codex review --base dev "<context paragraph>"
```

The `[PROMPT]` argument carries the same context paragraph you give the layered reviewer — model-specific instruction tuning ("things I want you to find that our primary reviewer might miss") is optional but improves cross-model differentiation. Codex returns its findings to stdout. Capture and consolidate with the layered findings in Step 3.

**Do not use** the `codex:codex-rescue` subagent for this — `codex review` is the native, direct path. The rescue subagent is for substantial coding handoffs, not pre-merge review.

### Step 3: Fix Issues

Consolidate findings from the layered reviewer AND (if `--cross-model`) the codex review. Deduplicate convergent catches; preserve unique catches from either reviewer.

For each issue found:

| Confidence | Action |
|------------|--------|
| 90-100 (Critical) | **Must fix** before proceeding |
| 80-89 (Important) | **Fix** unless it's a pre-existing pattern or out of scope |
| < 80 (Minor) | **Skip** — note in PR description if relevant |

After fixing, re-run the build to verify fixes don't break anything.

**If the review found 0 critical/important issues:** Skip to Step 4.

**In the PR description**, when `--cross-model` was used, note which findings came from each reviewer (especially unique catches from Codex — they demonstrate the cross-model value).

### Step 4: Commit

If there are uncommitted changes, commit them:

```bash
git add <specific files>
git commit -m "<conventional commit message>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Follow the project's commit conventions (check CLAUDE.md). Use conventional commits by default. The Co-Authored-By trailer should match the current model identity — check the conversation's environment block for the model name and ID.

### Step 5: Push

```bash
git push -u origin <branch-name>
```

### Step 6: Create PR

```bash
gh pr create --base dev --title "<conventional commit title>" --body "$(cat <<'EOF'
## Summary
<2-4 bullet points describing what changed>

## Code Review
<Brief summary of review findings and fixes applied>

## Test plan
- [ ] <verification steps>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**If the project uses milestones:** Add `--milestone "<milestone name>"` if you can determine the right one from context (check CLAUDE.md, issue references, or memory).

**If the PR closes an issue:** Include `Closes #<number>` in the body.

### Step 7: Merge

```bash
gh pr merge <pr-number> --squash --admin
```

Use `--squash` by default (single clean commit on main). Use `--admin` to bypass branch protection (as requested).

**Verify merge succeeded:**
```bash
gh pr view <pr-number> --json state --jq '.state'
```

Expected: `MERGED`

### Step 8: Return to Base Branch

**If the pipeline was run inside a worktree** (Step 0 resolved a path argument):

1. `cd "$ORIGINAL_PWD"` — return to the caller's original working directory.
2. Do NOT run `git checkout dev` inside the worktree. `dev` is likely checked out in the primary working directory; `git checkout` in a worktree would fail with "already checked out" or leave the worktree on a now-deleted branch.
3. Recommend the `finishing-a-development-branch` skill for worktree cleanup, or clean up manually:
   ```bash
   git worktree remove <worktree-path>
   git branch -D <merged-branch-name>
   ```

**Otherwise** (pipeline ran in the current working directory):

```bash
git checkout dev && git pull
```

### Step 9: Report

Print a concise summary:

```
Pipeline complete:
- PR: <url>
- Status: Merged to main
- Review: <N> issues found, <M> fixed
```

## Error Handling

| Error | Action |
|-------|--------|
| Build fails after fixes | Stop. Report failures. Don't push broken code. |
| Push rejected | Pull and rebase, then retry once. If still fails, report. |
| PR creation fails | Check if PR already exists for this branch. If so, update it. |
| Merge fails | Report the failure. Don't force-merge. |
| Not on a feature branch | Abort with clear message. |
| On dev or main | Abort — create a feature branch first. |
| Worktree path argument does not exist | Abort with: "Path does not exist: <arg>" |
| Worktree path argument is not a registered worktree | Abort with: "Not a registered git worktree: <arg>. Run 'git worktree list' to see registered worktrees." |
| Post-merge `git checkout` fails inside a worktree | Expected — do not retry. Skip to `finishing-a-development-branch` recommendation. |

## Flags and Options

The user may pass flags after the skill invocation:

- `--no-review` — Skip code review (Steps 2-3). Use when review was already done.
- `--no-merge` — Stop after PR creation (skip Steps 7-8). Use when you want CI to run first.
- `--rebase` — Use `--rebase` instead of `--squash` for merge.
- `--cross-model` — During Step 2, ALSO run Codex's native `codex review` in parallel for a different-model second opinion. Consolidate findings in Step 3. Worth the ~30-60s extra latency when the change touches anything load-bearing (schema, AI prompts, security gates, retry/error paths). Different models catch different classes of bugs.

## Common Mistakes

**Merging with failing build**
- Always build-check before AND after fixing review issues.

**Committing unrelated files**
- Stage specific files, not `git add -A`. Never commit `.env`, credentials, or large binaries.

**Generic PR titles**
- Use conventional commit format: `type(scope): description`. Match the project's conventions.

**Skipping the return to base**
- In the primary working directory: always checkout the base branch (`dev`) and pull after merge. Stale branches cause confusion.
- In a worktree: do NOT `git checkout` inside the worktree — return to the caller's original directory and recommend cleanup via `finishing-a-development-branch`.
