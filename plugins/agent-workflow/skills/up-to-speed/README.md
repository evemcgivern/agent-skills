# Up to Speed

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: full](https://img.shields.io/badge/Claude-full-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-full-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)

Gets you up to speed on an unfamiliar field in one sitting (roughly 45-90 minutes, shorter on request), one question at a time: the field's map, the 8-10 terms insiders use, the 3-5 ideas that explain most of it, live debates, and a scored exam with no hints. Use with "get me up to speed on", "crash course", "brief me on", or before a meeting in an industry you don't know.

## What it looks like

One sitting, one question at a time. Every round ends with a check, and every miss is logged and re-tested before the exam:

```mermaid
flowchart TD
    A[Pick a slice that fits one sitting] --> B[Starting level, reason, beliefs]
    B --> C[Map: central question and its parts]
    C --> D[8 to 10 insider terms, checked one by one]
    D --> E[3 to 5 core ideas, tested by prediction]
    E --> F[Misconceptions, live debates, judgment calls]
    F --> G[Re-test every logged miss]
    G --> H[Exam: about 10 questions, no hints]
    H --> I[Score, reteach the weak spot, name the limits]
    I --> J[Final briefing and 3-day recall questions]
```

Each exam answer is marked solid (1), partial (½), or missed (0). The suggested bands are rough defaults, not calibrated thresholds:

| Score | What it means |
|---|---|
| 80% or more | You can hold your own in a conversation with an insider. |
| 50-79% | You can follow along. |
| Under 50% | Not there yet. |

Short on time? The session drops to 5-6 terms, 3 core ideas, a 6-question exam, and no retest, and says what was cut.

## Install

Copy this complete folder to `~/.claude/skills/up-to-speed/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/up-to-speed/` for Codex, Gemini CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/up-to-speed/` or `.agents/skills/up-to-speed/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/up-to-speed/` or `.claude/skills/up-to-speed/`. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

