# Auth Hardening

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

NextAuth v5 security audit and hardening checklist — session/cookie config, CSRF, OAuth scopes, per-route role checks, password-reset/OTP rate limits, secret rotation, session invalidation on privilege change. Use when adding auth to a new product, auditing an existing NextAuth v5 app, or reviewing any PR that touches session/role/permission code.

## Install

Copy this complete folder to `~/.claude/skills/auth-hardening/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/auth-hardening/` for personal Codex use. For repository-only use, copy to `.claude/skills/auth-hardening/` or `.agents/skills/auth-hardening/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
