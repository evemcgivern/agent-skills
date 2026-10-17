# Rate Limit Audit

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Pre-launch gate that inventories every endpoint calling a paid API (LLM, email, SMS) and every auth endpoint, verifies a rate limiter exists, and actually tests it with scripted burst requests to confirm 429s fire. Use before launching a new product/feature, after adding an LLM-calling or auth route, or when asked to check rate limiting.

## Install

Copy this complete folder to `~/.claude/skills/rate-limit-audit/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/rate-limit-audit/` for personal Codex use. For repository-only use, copy to `.claude/skills/rate-limit-audit/` or `.agents/skills/rate-limit-audit/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
