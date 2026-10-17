# Stay Within Limits

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

Keeps long-running or parallel agent work inside 5-hour and weekly usage limits by running work in bounded waves, checking usage between waves, pausing at 95%, and resuming only after the window resets. Use for multi-wave subagent runs, overnight or unattended jobs, or when asked to "don't blow my usage", "watch my limits", "pause before the cap", or "resume when the window resets".

## Install

Copy this complete folder to `~/.claude/skills/stay-within-limits/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/stay-within-limits/` for personal Codex use. For repository-only use, copy to `.claude/skills/stay-within-limits/` or `.agents/skills/stay-within-limits/` respectively. Supporting files in this folder may be required. See the [collection README](../../../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
