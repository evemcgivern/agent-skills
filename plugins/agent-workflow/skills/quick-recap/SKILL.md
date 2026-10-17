---
name: quick-recap
description: Defines a one-line red/yellow/green status line that ends every agent response that completes work, and how to install it as standing instructions in AGENTS.md or CLAUDE.md. Use when asked to "add a status line", "end responses with a recap", "show done/pending/blocked at the end", or when project instructions require the quick-recap convention.
---

# Quick Recap

Make completion state obvious at the end of every response.

## Status Line

Every response that completes a unit of work ends with one line:

```md
🟢 Actual concise status sentence
```

Rules:

1. Pick the color from the user's point of view:
   - `🟢` the requested work is finished.
   - `🟡` finished except a non-routine follow-up; name the pending item.
   - `🔴` blocked on user input; name what is needed.
2. Write a specific sentence: what happened or what is needed, not "Done".
3. Keep it under 100 characters.
4. Put it last. Nothing after it — no `---`, spacer lines, or sign-off.

## Pass / fail

- **Pass:** the final line starts with exactly one of `🟢` `🟡` `🔴`, is
  under 100 characters, and nothing follows it.
- **Fail:** the line is missing, buried mid-response, followed by other
  content, vague ("All good"), or uses `🔴` for something the agent could
  have done itself.

## Installing

The convention is only automatic when it is in project or user instructions.
When installing this skill, add a short section with the rules above to the
project's `AGENTS.md` and/or `CLAUDE.md` (or the user-level equivalent),
unless the user opts out. Do not duplicate it if a section already exists.

## Examples

```md
🟢 Updated quick recap docs with output examples
```

```md
🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks
```

```md
🔴 Need the production API key to continue
```

## Common mistakes

- Using `🟡` for routine next steps (commit, push, open a PR) — that is `🟢`.
- Adding a prose summary or offer to help after the status line.
- Emitting a status line on a pure question or clarification turn where no
  unit of work completed.
