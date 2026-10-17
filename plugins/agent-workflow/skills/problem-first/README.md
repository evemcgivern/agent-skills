# Problem First

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Rewrites a draft prompt for an agent so it hands over the problem instead of your solution: problem, evidence, your fix ideas labelled as optional, an autonomy line, and what done means. It moves and labels your words without changing them, and says so when a prompt is already specific enough to send as is. Use on "/problem-first", "rewrite this prompt problem-first", or "am I prescribing a fix".

## Install

Copy this complete folder to `~/.claude/skills/problem-first/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/problem-first/` for personal Codex use. For repository-only use, copy to `.claude/skills/problem-first/` or `.agents/skills/problem-first/` respectively. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

## Credit

Based on the idea in [this video](https://youtu.be/D8PikZ1KhUo).
