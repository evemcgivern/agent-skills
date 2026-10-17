# Quick Recap

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

[![Claude: partial](https://img.shields.io/badge/Claude-partial-yellow)](../../../../README.md#compatibility) [![Codex / ChatGPT: partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-partial-yellow)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)
> Claude: Works in Claude Code; in the Claude app the status line works, but paste the install text into project instructions. Codex / ChatGPT: Works in Codex; in ChatGPT the status line works but there is no AGENTS.md to install it into.

Defines a one-line red/yellow/green status line that ends every agent response that completes work, and how to install it as standing instructions in AGENTS.md or CLAUDE.md. Use when asked to "add a status line", "end responses with a recap", "show done/pending/blocked at the end", or when project instructions require the quick-recap convention.

## What it looks like

The last line of a reply that finished some work. The color is chosen from your point of view:

| Line | Use it when |
|---|---|
| `🟢 Updated quick recap docs with output examples` | The requested work is finished. |
| `🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks` | Finished except a non-routine follow-up, which the line names. |
| `🔴 Need the production API key to continue` | Blocked on something only you can supply. |

In place, it closes the reply with nothing after it:

```text
The webhook handler now verifies signatures and rejects replays.
Tests cover both paths.

🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks
```

These fail the convention: `🟢 Done` (says nothing), `🟡 Open a PR next` (a routine step is still 🟢), and any sign-off or `---` after the line.

## Install

Copy this complete folder to `~/.claude/skills/quick-recap/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/quick-recap/` for Codex, Gemini CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/quick-recap/` or `.agents/skills/quick-recap/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/quick-recap/` or `.claude/skills/quick-recap/`. Supporting files in this folder may be required. See the [collection README](../../../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
