# Launch Chrome Debug

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: partial](https://img.shields.io/badge/Claude-partial-yellow)](../../../../README.md#compatibility) [![Codex / ChatGPT: partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-partial-yellow)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)
> Claude: Works in Claude Code with Chrome DevTools MCP set up; the Claude app cannot start Chrome on your computer. Codex / ChatGPT: Works in Codex with Chrome DevTools MCP set up (starting Chrome may need approval); ChatGPT cannot reach your Chrome.

Starts Google Chrome with remote debugging on port 9222 and a separate profile on macOS, Linux or Windows, so the Chrome DevTools MCP server can connect to it through `--browser-url`. Use when Chrome DevTools MCP tools fail because no debug target is available.

## What it looks like

A representative exchange on macOS (example output, invented data):

```text
> The DevTools MCP can't find a browser. Start Chrome for debugging.

Starting Chrome with a debug port and a separate profile:
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable &

Checking the port:
  curl -s http://127.0.0.1:9222/json/version
  {
    "Browser": "Chrome/<version>",
    "Protocol-Version": "1.3",
    "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/<id>"
  }

Port 9222 is answering. The MCP server connects only if its config passes
--browser-url=http://127.0.0.1:9222. Any app on this machine can control this
window while the port is open, so avoid sensitive sites and close it when done.
```

## Install

Copy this complete folder to `~/.claude/skills/launch-chrome-debug/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/launch-chrome-debug/` for Codex, Gemini CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/launch-chrome-debug/` or `.agents/skills/launch-chrome-debug/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/launch-chrome-debug/` or `.claude/skills/launch-chrome-debug/`. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

## Credit

The Chrome launch commands and the `--browser-url` setup in `SKILL.md` are adapted from the documentation of [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) (`docs/advanced-usage.md`), © Google LLC, licensed under the [Apache License 2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/LICENSE). The macOS, Linux and Command Prompt commands are reproduced unchanged; the PowerShell variant and the rest of this skill are original and MIT-licensed.
