# Handoff

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex partial, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%97%90%20%C2%B7%20ChatGPT%20%E2%97%90-yellow)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT get no git or GitHub state. Outside Claude Code, the prompt still targets a fresh Claude Code session and reads CLAUDE.md, so adapt it by hand.

Writes a copy-pasteable handoff prompt that lets a fresh Claude Code session resume the current work cold: why the work matters, what shipped, decisions not to reopen, branch and PR state, the next concrete action, relevant files, standing constraints, and the last few exchanges. Use when ending a session with "hand this off", "park this for tomorrow", or before `/clear`.

## What it looks like

Example output, invented data, shortened (a real handoff runs 600-1500 words). The sections always appear in this order. Open questions and the free-text note are left out here because there were none:

```text
# RESUME csv-importer — handoff

## Why we're here (strategic frame)
Large CSV exports time out on import. Streaming removes the file-size ceiling.

## Shipped this session
- PR #41 merged: streaming parser behind the `stream_import` flag
- #42 filed: quoted newlines split rows
- #43 filed: BOM breaks the header match
- `docs/import.md` updated with the flag and its default
- Benchmark recorded: 2 GB file imports in 40 s, was a timeout

## Locked-in decisions (do NOT re-litigate)
- Old parser stays until #43 closes: rollback must remain one flag flip

## In-flight state
- **Branch**: feat/import-progress
- **Uncommitted**: src/import/progress.ts
- **Unpushed**: up to date
- **Last commit**: feat(import): emit row counts
- **Open PRs on this branch**: none
- **Other open loops**: dev server on port 3000

## Next concrete action
On feat/import-progress, finish the row counter in src/import/progress.ts,
then run `npm test -- import` before opening the PR.

## Relevant files (paths + one-line descriptions)
- `src/import/progress.ts` — half-written progress emitter
- `src/import/stream.ts` — the parser that calls it

## Critical constraints
- No new parsing dependencies
- Keep the old parser path working
- Commit subjects use `type(scope): summary`

## Recent conversation (last 2-3 exchanges)
Agreed the bar shows rows, not percent: the total is unknown while streaming.
```

Below the block, the reply has exactly one more line: "Copy the block above into a fresh Claude Code session after `/new` or `/clear`."

## Install

Copy this complete folder to `~/.claude/skills/handoff/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/handoff/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/handoff/` or `.agents/skills/handoff/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/handoff/` or `.claude/skills/handoff/`. The git and GitHub checks work in any local agent, but the prompt it writes is addressed to a fresh Claude Code session and takes the project name from `CLAUDE.md`, so in other agents adjust the closing line and project name by hand. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

