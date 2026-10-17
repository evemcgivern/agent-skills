# Webhook Reliability

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Design or review inbound and outbound webhooks for signature verification, idempotency, retry/backoff, dead-letter recording, replay tooling, and timeout budgets. Use when building a new webhook handler or emitter, reviewing an existing one (Stripe, GitHub, or a custom outbound webhook), or investigating a "webhook silently didn't fire" report.

## Install

Copy this complete folder to `~/.claude/skills/webhook-reliability/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/webhook-reliability/` for personal Codex use. For repository-only use, copy to `.claude/skills/webhook-reliability/` or `.agents/skills/webhook-reliability/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
