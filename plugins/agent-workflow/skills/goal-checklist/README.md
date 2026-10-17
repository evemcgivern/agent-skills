# Goal Checklist

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Tracks a multi-issue goal as a one-line progress strip that the agent re-prints whenever an item changes state. Symbols separate not started, in progress, merged to the integration branch, shipped, and verified, plus unproven and blocked markers. The strip round-trips, so pasting it back restores the list, and `--sync` checks recorded merge SHAs against git to move merged items to shipped.

## Install

Copy this complete folder to `~/.claude/skills/goal-checklist/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/goal-checklist/` for personal Codex use. For repository-only use, copy to `.claude/skills/goal-checklist/` or `.agents/skills/goal-checklist/` respectively. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
