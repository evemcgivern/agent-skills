# Goal Checklist

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT the progress strip works, but --sync cannot check git.

Tracks a multi-issue goal as a one-line progress strip that the agent re-prints whenever an item changes state. Symbols separate not started, in progress, merged to the integration branch, shipped, and verified, plus unproven and blocked markers. The strip round-trips, so pasting it back restores the list, and `--sync` checks recorded merge SHAs against git to move merged items to shipped.

## What it looks like

The legend, left to right through the pipeline:

| Symbol | Meaning |
|---|---|
| ⬜ | Not started |
| 🔄 | In progress |
| 🟦 | Merged to the integration branch (needs its merge SHA) |
| 🚀 | Merged to production and deployed (needs its merge SHA) |
| ✅ | Confirmed working in production, from a run someone watched |
| 🔍 | Believed fixed, unproven |
| ⏸️ | Blocked, and always names the blocker |

**A short goal** prints as one line. Items sort by state, then by issue number, and the tally underneath is the key:

```text
⬜ #37, ⬜ #112, 🔄 #94 (PR #137), 🟦 #106 (5f6e7d8c9)
· 2⬜ not started · 1🔄 in progress · 1🟦 on dev · 4 total
```

**A bigger goal** switches to one row per state once the line would wrap. When one decision holds up several items, a single line above the strip says so, and the blocked items share one row:

```text
Settling #130's schema unblocks five items.
⬜ #37, #112, #127, #134, #136
🔄 #130 1/5 (steps 2-5 designed)
🟦 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
🔍 #107 (needs deploy)
⏸️ on #130: #104, #105, #117, #119, #129
· 5⬜ not started · 1🔄 in progress · 2🟦 on dev · 1🔍 unproven · 5⏸️ blocked · 14 total
```

**After a deploy**, `--sync` checks each recorded merge SHA against git. The two merged items are now live, so they move up a stage and nothing else changes:

```text
⬜ #37, #112, #127, #134, #136
🔄 #130 1/5 (steps 2-5 designed)
🚀 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
🔍 #107 (needs deploy)
⏸️ on #130: #104, #105, #117, #119, #129
· 5⬜ not started · 1🔄 in progress · 2🚀 shipped · 1🔍 unproven · 5⏸️ blocked · 14 total
```

You never ask for the strip. Once a goal is active, the agent ends any reply where an item changed state with the updated strip. To resume in a new session, paste the last strip back in and it restores the list exactly, fractions and notes included.

## Install

Copy this complete folder to `~/.claude/skills/goal-checklist/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/goal-checklist/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/goal-checklist/` or `.agents/skills/goal-checklist/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/goal-checklist/` or `.claude/skills/goal-checklist/`. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
