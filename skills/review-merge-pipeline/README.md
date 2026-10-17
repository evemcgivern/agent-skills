# Review Merge Pipeline

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Automated pipeline that code-reviews uncommitted changes, fixes issues found, commits, pushes, creates a PR, and merges with --admin. Accepts an optional worktree path argument and flags --no-review / --no-merge / --rebase / --cross-model. Use when work is done and you want to ship it without manual steps.

## Install

Copy this complete folder to `~/.claude/skills/review-merge-pipeline/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/review-merge-pipeline/` for personal Codex use. For repository-only use, copy to `.claude/skills/review-merge-pipeline/` or `.agents/skills/review-merge-pipeline/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
