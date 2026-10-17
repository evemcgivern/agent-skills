# Review Older Issues

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Revalidates a bounded batch of open GitHub issues against current code, pull requests and related closed issues. Each issue gets one verdict: still valid, shipped, superseded or duplicate, needs rescoping, unwarranted, or unverified. The skill closes or rewrites issues only when the evidence supports it. It detects the repository's own labels, issue templates and branch conventions instead of assuming them, and needs the GitHub CLI (`gh`). Use on `/review-older-issues` or when asked to "review issues 1-100" or "clean up stale issues".

## What it looks like

Example output, invented data. Each issue that was open when the batch started gets exactly one verdict, the evidence behind it, and the action taken:

```text
Selection: issues #1-#40, filtered to open at snapshot 2026-03-02 10:14 UTC
Checked revision: 4e1c9a2 (main). Skipped (already closed at snapshot): #3, #17

| Issue | Verdict      | Evidence                                   | Action                  | Result                  |
|-------|--------------|--------------------------------------------|-------------------------|-------------------------|
| #4    | SHIPPED      | PR #88 merged to main; src/auth/reset.ts:42 | Closed as completed     | Closed, comment read back |
| #9    | SUPERSEDED / DUPLICATE | Same gap as #61, which holds the decision  | Closed as not planned   | Closed, links #61       |
| #12   | RESCOPE      | Export shipped (PR #70); CSV import still missing | Body rewritten to the import work | Body read back |
| #21   | VALID        | Rate limit still absent in src/api/upload.ts | None                  | Unchanged               |
| #33   | UNWARRANTED  | Feature removed in PR #102; no remaining work | Closed as not planned | Closed, comment read back |
| #38   | UNVERIFIED   | Fix merged to integration branch; deploy unknown | None              | Unchanged               |

Counts: 1 SHIPPED · 1 SUPERSEDED / DUPLICATE · 1 RESCOPE · 1 VALID · 1 UNWARRANTED · 1 UNVERIFIED
Resume from: #41
```

A merged pull request is not proof the change shipped. When it cannot be confirmed, as with #38, the issue is left alone and marked `UNVERIFIED`.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `review-older-issues/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
