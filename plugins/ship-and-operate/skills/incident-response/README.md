# Incident Response

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

Production incident runbook for a small team - severity call, fixed triage order, rollback-first decision, user comms, and a one-page blameless postmortem. Use when a service is down, erroring, or degraded in production, e.g. "site is down", "we're getting 500s", "uptime alert fired", "users report errors", "was it the last deploy?", "roll back", or "write the postmortem".

## Install

Copy this complete folder to `~/.claude/skills/incident-response/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/incident-response/` for personal Codex use. For repository-only use, copy to `.claude/skills/incident-response/` or `.agents/skills/incident-response/` respectively. Supporting files in this folder may be required. See the [collection README](../../../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
