# Check Worth

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

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

Copy this complete folder to `~/.claude/skills/check-worth/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/check-worth/` for personal Codex use. For repository-only use, copy to `.claude/skills/check-worth/` or `.agents/skills/check-worth/` respectively. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
