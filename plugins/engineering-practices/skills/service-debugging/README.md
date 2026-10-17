# Service Debugging

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Turns a live production symptom into a ranked, falsifiable cause. It starts from the system's catalog of known failures and the most recent change, pulls evidence for the leading hypothesis only, and ends with a symptom statement, one to three ranked causes each with the check that would rule it out, links a person can open, and a confirmed or unconfirmed verdict. Use when a deployed service returns 500s, times out, shows a blank page, silently does nothing, or keeps failing the same way, or when asked to "debug prod" or "find the root cause".

## Install

Copy this complete folder to `~/.claude/skills/service-debugging/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/service-debugging/` for personal Codex use. For repository-only use, copy to `.claude/skills/service-debugging/` or `.agents/skills/service-debugging/` respectively. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
