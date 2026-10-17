---
name: review-older-issues
description: "Revalidate a bounded batch of open GitHub issues against current code, pull requests, and related closed issues; close issues already shipped or no longer warranted, and rescope issues whose remaining work differs from the body. Works in any repo and detects its labels, templates, and branch conventions. Use on /review-older-issues and on phrases like 'review issues 1-100', 'clean up stale issues', 'audit the old backlog', 'are these old issues still valid'."
---

# Review Older Issues

Revalidate only the requested issues that are **open at the start of the batch**. For each, determine whether the issue is still accurate and actionable by checking its complete history, current code, relevant pull requests, and related closed issues. When evidence shows the old issue is no longer valid, close it with a reason and explanatory comment, or update the existing issue body so it describes the real remaining work.

This workflow can update GitHub issues because the user invokes it to review and clean up the backlog. Do not create replacement issues unless the user separately asks. Preserve issue history; do not erase useful decisions or silently discard unique unfinished work.

## Inputs and boundaries

- Accept an explicit issue-number range/list, or a count of open issues to process.
- Interpret `1-100` as issue numbers #1 through #100 inclusive, **then filter to issues currently open**. It does not mean the first 100 open issues.
- Interpret “the first 100 open issues” as the lowest-numbered 100 issues that are open when the batch starts. State the ordering and snapshot the target list before editing anything.
- For an explicit list/range, capture the open-state snapshot before processing. Never add issues that become open later to that batch. Skip any target already closed at snapshot time and report it as skipped.
- Closed issues may be researched as evidence or canonical duplicates, but must never become cleanup targets in this workflow.
- Work in bounded batches. If no range/count is supplied, ask for one rather than selecting the entire backlog.
- Assume nothing about the repository's conventions: label names, issue templates, issue types, milestones, project boards, default or integration branches, and close-reason habits differ between repos. Detect them (step 1) or ask.
- If an API/rate limit prevents reliable enumeration or complete evidence retrieval, stop at the last verified issue and report the remainder as `UNVERIFIED`.

## 1. Establish the repository and batch snapshot

1. Confirm the current repository with `git rev-parse --show-toplevel`, remote metadata, and `gh repo view`. Do not infer a repository from a prior session.
2. Read the repository's agent and contributor guidance if present (for example `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`), then any issue-specific or domain guidance relevant to the issues. Follow repo-specific conventions and safety rules.
3. Record branch and worktree status. Local code evidence is tied to the checked-out revision; record its commit SHA. Do not switch branches or modify code for this audit.
4. Confirm GitHub CLI authentication and repository identity.
5. Detect the repository's issue conventions instead of assuming them:
   - Default branch and any integration branch: `gh repo view --json defaultBranchRef`, plus recent PR base branches (`gh pr list --state merged --limit 30 --json baseRefName`).
   - Labels in use: `gh label list --limit 200`. Use only labels that already exist; never create labels.
   - Issue templates and forms: `.github/ISSUE_TEMPLATE/` and any `.github/issue_template.md`. A rescoped body should follow the template's sections when one exists.
   - Whether the repo uses issue types, milestones, or project boards, from the issues themselves. Leave those fields as they are unless the repo's guidance says how to update them.
   If a convention matters for an action and cannot be detected, ask the user rather than guessing.
6. Enumerate open issues and freeze the target numbers before any issue mutation:

```bash
gh issue list --state open --limit 1000 --json number,title,body,labels,assignees,createdAt,updatedAt,url
```

Apply the requested range/count to the returned open issue set. If more results may exist than the command returned, paginate or query additional pages until the target selection is reliable. Record the snapshot time, selection rule, and target list.

## 2. Gather evidence per target

Read the complete issue body and all comments, not just the title:

```bash
gh issue view <N> --comments
```

Capture the current state, state reason, title, labels, milestone, assignees, body, comments, and linked references. Extract the issue's claimed problem, scope, acceptance criteria, dependencies, and decisions already made.

Then investigate both implementation and history:

- Search current code, tests, configuration, migrations, and docs for the behavior or gap. Search alternate terms and trace relevant callers/consumers. Cite exact file and line locations and the checked-out SHA.
- Inspect relevant pull requests, including merged, closed-unmerged, and open PRs. Search by issue number, linked closing references, title terms, branch names, and affected files. Read PR descriptions and review/merge outcome where available.
- Inspect related closed issues for duplicate/canonical ownership, prior decisions, and closure rationale. Closed state alone is not proof of shipment. Distinguish `COMPLETED` from `NOT_PLANNED`; inspect the closing comment and linked PR/code. A merged PR is not proof its changes exist on the checked-out branch or production.
- Use the branch conventions detected in step 1 before interpreting closing keywords. Closing keywords only auto-close issues when the PR merges into the default branch, so a merge may have landed on an integration branch without closing the issue, or may be merged but unreleased.
- Treat stale premises as unverified. Re-check each factual claim against current code and recent history; do not assume an old issue is invalid merely because it is old.

Use targeted `gh` commands, for example:

```bash
gh issue view <N> --json number,state,stateReason,title,body,labels,assignees,milestone,closedAt,url
gh pr list --state all --search "<N>" --json number,title,state,baseRefName,headRefName,mergedAt,url --limit 100
gh issue list --state all --search "<distinctive terms>" --json number,title,state,stateReason,url --limit 100
```

Fetch full bodies/comments for likely related issues and PRs. Search results and issue titles are leads, not final evidence.

## 3. Classify and choose an action

Assign exactly one verdict to each target:

- **VALID** — the described gap and scope still match current evidence; leave unchanged.
- **SHIPPED** — the claimed work is demonstrably present in the relevant code/release path; close as completed and explain the evidence.
- **SUPERSEDED / DUPLICATE** — a newer issue or decision is the canonical owner and the old issue adds no distinct unfinished requirement; close as not planned, link the canonical owner, and explain why.
- **RESCOPE** — part of the issue remains valid, but the body, scope, or acceptance criteria no longer match reality; update the existing body to preserve the real remaining work and remove only disproven/completed portions.
- **UNWARRANTED** — evidence shows no remaining actionable work and there is no useful canonical issue; close as not planned with a specific rationale.
- **UNVERIFIED** — evidence is incomplete, conflicting, inaccessible, or ambiguous; do not change the issue.

A PR being open, a TODO existing, a test passing in isolation, a release note, or an issue being closed does not alone prove behavior shipped. Require direct code/history evidence appropriate to the claim. When deployment state matters but cannot be verified, say so and avoid the **SHIPPED** verdict.

## 4. Apply justified issue updates

This invocation authorizes routine updates to the selected open issues. Apply only the action supported by evidence:

- **SHIPPED:** close with the completed reason. Add a concise comment citing merged PR(s), code locations/SHA, and any deployment limitation. If only part shipped, rescope instead of closing.
- **SUPERSEDED / DUPLICATE:** close with not-planned reason and comment linking the canonical issue and identifying any distinct work that would prevent closure.
- **UNWARRANTED:** close with not-planned reason and an evidence-based comment. Do not use “stale” as the sole rationale.
- **RESCOPE:** edit the existing issue body while preserving relevant history/comments. Retain the original context that still matters, state what is already done, define the remaining scope and non-goals, and add testable acceptance criteria. Do not close it.
- **VALID / UNVERIFIED:** leave unchanged.

Before each mutation, re-fetch the issue and confirm it remains open and materially unchanged since the snapshot. If its state/body changed, investigate the new information before deciding. Use the issue format and labels detected in step 1; do not invent labels, priority, or acceptance claims unsupported by evidence. Never change code, merge PRs, delete issues, or create replacements as part of this skill.

After each update, read it back and verify the new state/body/comment:

```bash
gh issue view <N> --comments
```

If a mutation fails or readback differs, stop mutating that issue, preserve the error, and report it accurately.

## 5. Batch report and resume point

Return a concise table with one row per target:

| Issue | Verdict | Evidence | Action | Result |
|---|---|---|---|---|

For each verdict, cite issue/PR numbers, exact code locations, and the revision checked. State the target-selection rule, snapshot time, skipped-closed targets, and any unverified evidence. For mutations, report the verified post-update issue state or body result. Finish with counts by verdict and the next issue number/range for resuming.

Do not claim the full batch is complete if any selected issue was not reviewed or any required update failed. Mark such items `UNVERIFIED` and identify the blocker.
