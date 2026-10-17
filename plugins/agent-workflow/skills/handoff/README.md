# Handoff

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Writes a copy-pasteable handoff prompt that lets a fresh Claude Code session resume the current work cold: why the work matters, what shipped, decisions not to reopen, branch and PR state, the next concrete action, relevant files, standing constraints, and the last few exchanges. Use when ending a session with "hand this off", "park this for tomorrow", or before `/clear`.

## Install

Copy this complete folder to `~/.claude/skills/handoff/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/handoff/` for personal Codex use. For repository-only use, copy to `.claude/skills/handoff/` or `.agents/skills/handoff/` respectively. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

