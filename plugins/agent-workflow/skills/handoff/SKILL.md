---
name: handoff
description: "Writes a copy-pasteable handoff prompt that lets a fresh session of your agent (Claude Code, Codex, Gemini CLI and others) resume the current work cold. Use when ending a session and the next one has to pick up without re-investigating. Triggers on /handoff and on phrases like 'hand this off', 'write up where we are for a new session', 'I'm going to /clear, catch the next session up', 'park this for tomorrow'."
---

# Handoff

Produce a **detailed, copy-pasteable handoff prompt** the user can paste into a fresh session of their agent (Claude Code, Codex, Gemini CLI or another) to resume work cold.

The receiving session should have enough context to **start executing immediately** — not enough to investigate. That distinction is the whole design: a handoff that says "look into the auth problem" has moved the investigation, not the work.

## Step 1: probe the state

Run these first. They are cheap, and every concrete detail they yield saves the fresh session a grep.

```sh
git branch --show-current       # current branch
git status -sb                  # tracking + ahead/behind
git status --short              # uncommitted files
git log --oneline -5            # recent commits
pwd                             # basename is the fallback project name
head -5 CLAUDE.md AGENTS.md GEMINI.md 2>/dev/null  # project name from the first heading of whichever exists
gh pr status                    # PRs on the current branch
```

**If a probe errors, treat that signal as absent and omit the corresponding
section** — a handoff carrying `fatal: not a git repository` teaches the next
session nothing. Not every directory is a repo and not every repo has a PR.

## Step 2: read the conversation

The probes are secondary. **The conversation is the primary source** — it holds
the decisions, the intent, the open threads and the style signals that git state
cannot capture. A handoff assembled only from `git log` reproduces what happened
and loses why, which is the half the next session actually needs.

## Step 3: write the block

Follow the structure below exactly. Do not rename sections, add sections, or
reorder them — a fixed shape is what lets someone scan a handoff they have read
fifty times before.

### Sizing

Aim for **600–1500 words**. Long enough to paste and execute without
re-grepping; short enough to fit one terminal window. Over 1500, compress the
conversational-context section first — it is the most compressible and the
least load-bearing.

### Format

````
# RESUME {project-name-from-instructions-file-heading-or-basename} — handoff

## Why we're here (strategic frame)
{2-3 sentences on WHY this work is happening — the thesis, the positioning, the
motivating problem. Not "what we're doing" but "what makes this worth doing."}

## Shipped this session
- {concrete outcome with #issue or PR number if applicable}
- {concrete outcome}

5-10 bullets. Every bullet names a specific artifact: PR number, issue number,
file path, commit SHA, or named decision. No "worked on" vagueness.

## Locked-in decisions (do NOT re-litigate)
- {decision with one-line rationale}

Choices already made that the fresh session might reopen. Include the rationale,
not just the conclusion — the logic is what stops it being re-argued.

## In-flight state
- **Branch**: {branch-name}
- **Uncommitted**: {file list or "clean"}
- **Unpushed**: {commit list or "up to date"}
- **Last commit**: {subject verbatim}
- **Open PRs on this branch**: {gh output or "none"}
- **Other open loops**: {e.g. "dev server on port 3000", "stashed WIP on feat/X"}

## Open questions (not yet decided)
- {question the session was about to answer but didn't}

Omit this section entirely if there are none.

## Next concrete action
{ONE paragraph, 2-4 sentences. The specific task, which branch to be on, which
files to touch, which commands to run. State any critical precondition ("run X
before Y"). Write it as a direct instruction to the next session.}

## Relevant files (paths + one-line descriptions)
- `path/to/file.ts` — what it contains or why it matters to the next action

5-10 paths max. Prefer files the next action will actually touch over every file
mentioned. Include paths outside the repo when they matter — notes directories,
memory files.

## Critical constraints
- {a style, positioning, or architectural rule that must be followed}

Standing orders. 3-6 items — these are the rails, not a full style guide.

## Recent conversation (last 2-3 exchanges)
{Tight paraphrase or direct quote of the last 2-3 exchanges. Preserves tone,
direction, and half-formed ideas that had not yet become decisions. This is what
lets the fresh session hear where the conversation was going.}

## Free-text note
{the user's /handoff argument, verbatim; omit the section entirely if none}
````

After the block, add exactly one line:

> Copy the block above into a fresh session of your agent (for example after `/new` or `/clear`).

Nothing else. No explanation, no commentary, no offer to follow up — the output
is a thing to paste, and anything after it is noise the user has to scroll past.

## Arguments

Free text passed to `/handoff` (e.g. `/handoff parking this for tomorrow`) goes
**verbatim** into the final section. It is the user's own note to their future
self; do not paraphrase or tidy it.

## Style

- Scan-friendly. Bullets and short sentences.
- Name specifics — issue numbers, file paths, SHAs, commands.
- Don't editorialise. "Worked on a lot of import stuff" is worthless;
  "Filed #212-#218, design doc at docs/design/csv-import.md, benchmark
  picked the smaller model" is useful.
- **Match the voice already in the conversation.** Formal session, formal
  handoff; casual session, casual handoff. The next session inherits the tone.
- Do not wrap the handoff in triple backticks — the format above uses a
  four-backtick fence so nested code fences inside sections still render.
