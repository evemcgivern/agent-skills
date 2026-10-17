# Deploy

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Merge dev to main for production deployment. Repo-agnostic — detects the repo's conventions and defers to any repo-local runbook. Use once daily or when ready to push to production.

## Install

Copy this complete folder to `~/.claude/skills/deploy/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/deploy/` for personal Codex use. For repository-only use, copy to `.claude/skills/deploy/` or `.agents/skills/deploy/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
