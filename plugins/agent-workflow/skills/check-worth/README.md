# Check Worth

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it reads the source but cannot check it against your repo or GitHub issues.

Reviews an external PDF, image, screenshot, article, or URL against a repository's open and closed issues and its code, and sorts each idea into already tracked, shipped, superseded, a candidate new issue, or not actionable, with `file:line` evidence and `UNABLE TO VERIFY` where the source falls short. Read-only unless you authorize issue creation or code changes. Use on "/check-worth" or when asking whether an external idea is worth pulling into a repository.

## What it looks like

Example output, invented data. The reply leads with the conclusion, then one row per idea from the source:

```text
One idea is worth a new issue. Two are already covered, and one could not be checked.

| Source takeaway             | Repository status       | Evidence                         | Recommendation       |
|-----------------------------|-------------------------|----------------------------------|----------------------|
| Cache prompt prefixes       | Shipped                 | src/llm/client.ts:88             | None                 |
| Retry with backoff on 429   | Already tracked         | #57 (open), src/llm/retry.ts:12  | Comment on #57       |
| Log token cost per request  | Candidate new issue     | No match in issues or code       | Draft below          |
| "Cuts latency by 40%"       | UNABLE TO VERIFY        | Source gives no benchmark setup  | Do not act on it     |

Source limitations: PDF pages 1-12 read; page 13 is an image with no legible text.
```

After the table come the existing issue and code matches, the draft for the new issue (title, scope, non-goals, acceptance criteria), and deferred follow-ups. Nothing is filed or changed until you say so.

## Install

Copy this complete folder to `~/.claude/skills/check-worth/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/check-worth/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/check-worth/` or `.agents/skills/check-worth/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/check-worth/` or `.claude/skills/check-worth/`. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
