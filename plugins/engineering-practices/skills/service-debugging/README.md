# Service Debugging

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it ranks causes only from evidence you paste in.

Turns a live production symptom into a ranked, falsifiable cause. It starts from the system's catalog of known failures and the most recent change, pulls evidence for the leading hypothesis only, and ends with a symptom statement, one to three ranked causes each with the check that would rule it out, links a person can open, and a confirmed or unconfirmed verdict. Use when a deployed service returns 500s, times out, shows a blank page, silently does nothing, or keeps failing the same way, or when asked to "debug prod" or "find the root cause".

## What it looks like

Example output, invented data. Every run returns the same four parts, in this order:

```text
SYMPTOM
  Since 14:05 UTC, POST /api/checkout returns 500 for about 1 in 3 requests, all tenants.

RANKED CAUSES
  1. Connection-pool exhaustion after the 14:02 deploy raised worker count from 4 to 12
     Evidence: pool-timeout errors start at 14:05; 12 workers x 10 connections > database limit of 100
     Rules it out: errors continue after rolling back to 4 workers
  2. Slow query from a missing index on orders.customer_id
     Evidence: p95 query time up 6x in the same window
     Rules it out: EXPLAIN shows an index scan on the live database

VERIFICATION LINKS
  <log query: pool timeouts, 13:50-14:30>   <deploy 14:02>   src/db/pool.ts:18

VERDICT
  UNCONFIRMED. Next: roll back the worker count, then rerun cause 1's check.
```

Where to look first, from the skill's symptom table:

| Symptom | Look here first |
|---|---|
| Blanket 5xx starting at a timestamp | The deploy or config change at that timestamp |
| Works locally, dead in prod | Missing or different env var, build-time versus runtime config |
| Silent no-op | A swallowed exception, an early return, a guard failing closed |
| Wrong data, no error | Partially applied migration, a default overwriting a real value |

## Install

Copy this complete folder to `~/.claude/skills/service-debugging/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/service-debugging/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/service-debugging/` or `.agents/skills/service-debugging/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/service-debugging/` or `.claude/skills/service-debugging/`. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
