---
name: check-worth
description: "Review an external PDF, image, screenshot, article, or URL against a repository's current issues and code to sort its ideas into new, already tracked, shipped, contradicted, or unverifiable, read-only by default. Use when the user asks to '/check-worth' or '$check-worth' a source, or asks whether an external idea is worth pulling into a repository as an issue or code change."
---

# Check Worth

Review an external artifact against a repository's current issues and implementation. Determine what is genuinely new, what is already covered, what is contradicted by the code, and what is not verifiable from the supplied artifact.

Default to read-only review. Do not create issues, edit code, or change configuration unless the user explicitly authorizes that follow-up.

This is a global skill. When invoked inside a repository, use the current working directory and its repository metadata as the comparison context. When invoked outside a repository, do not guess which project the source belongs to and do not scan unrelated directories. Ask for the repository path, project name, or a sufficiently specific codebase context before performing the issue/code comparison. It is still acceptable to extract and summarize the source while waiting, but label the repository comparison `UNABLE TO VERIFY`.

## Ground the repository

Identify the artifact type, repository root, branch, dirty-worktree state, remote, and requested output. Read repository-local `AGENTS.md` first.

If an issue number is supplied, fetch it before other issue-specific work:

```text
gh issue view <N> --comments
```

Read the complete body and every comment. Treat comments as scope and decision evidence.

## Extract the source faithfully

### PDF

Use text extraction and visual rendering. Prefer `pdftotext -layout` plus `pdftoppm -png`; inspect title, diagrams, code, tables, and ending pages. Check whether the file contains the actual document or only an inbox/feed view, thumbnail, preview, or partial capture. If the body is absent, report `UNABLE TO VERIFY` instead of inferring recommendations from a title or thumbnail.

### Image or screenshot

Inspect at useful resolution and crop long or narrow images into readable sections. Use OCR only as an aid; verify important claims against the pixels. Record headings, diagrams, code, workflows, caveats, and visible measurements. Do not treat unreadable diagram text as confirmed prose.

### URL

Open the canonical URL with the available browser or web tool. Prefer the primary source. Record access failures, authentication walls, publication date, truncation, and differences from any attached artifact. Do not substitute a search-result snippet for the requested source.

Preserve provenance: local path or URL, extraction method, pages/sections inspected, and limitations.

## Clean up review artifacts

Store temporary extraction and rendering output under a task-scoped temporary directory such as `tmp/pdfs/<slug>/`. Before finishing, remove generated text, page images, crops, OCR output, contact sheets, and other intermediates. Do not delete the user's supplied artifact or any pre-existing repository files. If cleanup cannot be completed, report the exact leftover path.

## Convert the source into proposals

Separate claims, mechanisms, assumptions, and evidence. Discard promotional framing and generic advice. Preserve useful failure modes and negative guidance. Translate each surviving mechanism into one sentence of repository-specific work, such as “add an opt-in benchmark arm” or “capture a missing provenance field.”

## Check existing issues and code

Search all relevant open and closed GitHub issues, including bodies, with `gh issue list --state all --limit 500 --json number,title,body,labels`; fetch full bodies/comments for likely matches. Classify each proposal as already tracked, shipped/partly shipped, superseded/blocked, candidate new issue, or not actionable yet. Prefer a child issue under an existing epic when appropriate.

Search implementation, tests, configuration, documentation, and history. Use fast text search first; trace callers and consumers for API, schema, routing, persistence, security, or safety changes. Cite exact `file:line` locations. Check disabled configuration, narrow tests, prototype-only comments, missing backend capability, residency/approval/protected-path constraints, and docs impact.

Treat a clean build, issue comment, or plausible design as progress evidence, not runtime proof. State what was and was not verified.

## Issue decision and report

Recommend a new issue only when the mechanism is concrete and relevant, not already owned, technically bounded, measurable, and free of silent policy/dependency expansion. Draft title, parent/related issues, context, scope, non-goals, measurement, guardrails, and acceptance criteria. Create only after explicit authorization; verify with `gh issue view <N> --comments`.

Lead with the conclusion. Use a table for multiple proposals:

| Source takeaway | Repository status | Evidence | Recommendation |
|---|---|---|---|

Then include source limitations, existing issue/code matches, new issue candidates, and deferred follow-up. Use `UNABLE TO VERIFY` for inaccessible, partial, unreadable, or unmeasured claims. Never turn a thumbnail, search snippet, model reputation, or issue title into confirmed technical evidence.

Keep the review read-only unless issue creation or implementation is separately requested.
