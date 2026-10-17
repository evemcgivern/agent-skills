---
name: repo-activity-summary
description: Summarize current GitHub repo activity - open issues, open PRs with check status, recent CI runs, and local branch state - in one report with planning takeaways, via the gh CLI. Use on "activity summary", "what's open", "project status", "progress check", "CI status", or a request to list open issues and PRs.
allowed-tools: Bash(gh issue list:*), Bash(gh pr list:*), Bash(gh run list:*), Bash(git branch:*), Bash(git status:*)
---

# Repo Activity Summary

Report open issues, pull requests, and CI status for the current repo. Read-only: never comment, label, close, or re-run. If `gh` is not authenticated or this is not a GitHub clone, stop and say so.

## Data gathering

Run these in parallel:

```bash
gh issue list --state open --limit 15 \
  --json number,title,labels,milestone,updatedAt \
  --jq '.[] | "\(.number)\t\(.title)\t\(.labels | map(.name) | join(","))\t\(.milestone.title // "none")\t\(.updatedAt[:10])"'

gh pr list --state open --limit 10 \
  --json number,title,headRefName,createdAt,isDraft,statusCheckRollup \
  --jq '.[] | "\(.number)\t\(.title)\t\(.headRefName)\t\(.createdAt[:10])\t\(.isDraft)\t\(.statusCheckRollup | map((.conclusion | select(. != "")) // .state // .status) | unique | join(","))"'

gh run list --limit 8 \
  --json name,status,conclusion,headBranch,createdAt,event \
  --jq '.[] | "\((.conclusion | select(. != "")) // .status)\t\(.name)\t\(.headBranch)\t\(.createdAt[:10])\t\(.event)"'

git branch --show-current
git status --porcelain   # count the lines = uncommitted files
```

## Output format

```
## Open Issues (showing N)
| # | Title | Milestone | Labels |
[newest first; if 15 came back, say more may exist]
Breakdown by milestone. Highlight P0/P1 items.

## Open Pull Requests (N)
| # | Title | Branch | Draft? | CI |

## CI Status (recent runs)
| Status | Workflow | Branch |

## Current Branch Context
[branch + uncommitted file count]

## Planning Takeaways
[2-4 bullets: blockers, active work, items needing attention]
```

## Pass criteria

- Every section present; an empty one says so ("No open pull requests").
- Every failing PR check or CI run (FAILURE, CANCELLED, ACTION_REQUIRED) appears in the takeaways.
- Truncation at a `--limit` is stated, never hidden.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `checks` field on `gh pr list` | Not a valid JSON field; use `statusCheckRollup` |
| `.conclusion // .status` | Running checks have `conclusion: ""`, which `//` does not skip; commit statuses use `state`. Use the expressions above |
| "15 open issues" when the limit was 15 | Say "showing 15" |
| Omitting branch context | Always include branch and uncommitted count |
