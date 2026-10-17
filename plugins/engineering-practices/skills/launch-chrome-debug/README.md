# Launch Chrome Debug

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they cannot start Chrome on your computer or run a local MCP server.

Starts Google Chrome with remote debugging on port 9222 and a separate profile on macOS, Linux or Windows, so the Chrome DevTools MCP server can connect to it through `--browser-url`. Use when Chrome DevTools MCP tools fail because no debug target is available.

## When and how to use it

**Use it when**
- Your Chrome DevTools MCP tools fail with a connection error.
- You want an agent to inspect a live page in a real browser on port 9222.
- You want a separate debug profile so your daily browsing stays out of the session.

**Try it**
```text
Start Chrome for debugging so the DevTools MCP can connect.
The list_pages call failed. Check that port 9222 is responding.
```
You get the launch command for macOS, Linux or Windows, and a `curl` check on `http://127.0.0.1:9222/json/version` that returns JSON when it works.

**Skip it when**
- Your MCP server does not use `--browser-url`. It starts its own Chrome, so you do not need this.

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

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `llm-engineer`, `review-older-issues`, `saas-metrics`, `service-debugging`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:launch-chrome-debug`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh launch-chrome-debug   # into ~/.claude/skills/launch-chrome-debug
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/launch-chrome-debug/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex launch-chrome-debug   # into ~/.agents/skills/launch-chrome-debug
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/launch-chrome-debug/` instead. Or copy this folder by hand to `~/.agents/skills/launch-chrome-debug/`, or `.agents/skills/launch-chrome-debug/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/launch-chrome-debug/` for personal use (`scripts/install.sh --target codex launch-chrome-debug` does this), or `<repo>/.agents/skills/launch-chrome-debug/` for one repository.
- Windsurf: `<repo>/.agents/skills/launch-chrome-debug/`.
- Cline: `<repo>/.cline/skills/launch-chrome-debug/`, `<repo>/.claude/skills/launch-chrome-debug/` or `~/.cline/skills/launch-chrome-debug/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app cannot start Chrome on your computer or run a local MCP server.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT cannot start Chrome on your computer or run a local MCP server.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

## Credit

The Chrome launch commands and the `--browser-url` setup in `SKILL.md` are adapted from the documentation of [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) (`docs/advanced-usage.md`), © Google LLC, licensed under the [Apache License 2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/LICENSE). The macOS, Linux and Command Prompt commands are reproduced unchanged; the PowerShell variant and the rest of this skill are original and MIT-licensed.
