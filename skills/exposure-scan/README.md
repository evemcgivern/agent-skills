# Exposure Scan

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Scan installed packages against bumblebee threat-intelligence exposure catalogs to detect known-compromised dependency releases (supply-chain campaigns like shai-hulud, node-ipc, gemstuffer). Use when checking for compromised packages, running a supply-chain or dependency security scan, auditing the machine after a reported npm/PyPI/Go/gem/extension compromise, or refreshing threat-intel catalogs.

## Install

Copy this complete folder to `~/.claude/skills/exposure-scan/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/exposure-scan/` for personal Codex use. For repository-only use, copy to `.claude/skills/exposure-scan/` or `.agents/skills/exposure-scan/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
