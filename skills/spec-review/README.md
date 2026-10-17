# Spec Review

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Use when a design spec, plan, or requirements doc is drafted/ratified/about-to-be-implemented and you want a rigorous second-model review that verifies the spec's claims against the real codebase — catching wrong data-model assumptions (scalar-vs-M2M), unverified schema/API claims, missing acceptance criteria, ambiguity, and internal contradictions before code is written. The spec-world analog of /codex:review for PRs.

## Install

Copy this complete folder to `~/.claude/skills/spec-review/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/spec-review/` for personal Codex use. For repository-only use, copy to `.claude/skills/spec-review/` or `.agents/skills/spec-review/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
