# Launch Chrome Debug

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Starts Google Chrome with remote debugging on port 9222 and a separate profile on macOS, Linux or Windows, so the Chrome DevTools MCP server can connect to it through `--browser-url`. Use when Chrome DevTools MCP tools fail because no debug target is available.

## Install

Copy this complete folder to `~/.claude/skills/launch-chrome-debug/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/launch-chrome-debug/` for personal Codex use. For repository-only use, copy to `.claude/skills/launch-chrome-debug/` or `.agents/skills/launch-chrome-debug/` respectively. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

## Credit

The Chrome launch commands and the `--browser-url` setup in `SKILL.md` are adapted from the documentation of [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) (`docs/advanced-usage.md`), © Google LLC, licensed under the [Apache License 2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/LICENSE). The macOS, Linux and Command Prompt commands are reproduced unchanged; the PowerShell variant and the rest of this skill are original and MIT-licensed.
