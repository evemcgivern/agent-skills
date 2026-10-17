# Spec Workflow Drift

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they have no access to your repo.

> **Requires the [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp)** by Pimzino. Install and configure it first. This skill reads the `.spec-workflow/` directory that the server creates; it does not call the server's tools. This skill contains none of the server's code; the server is a separate project under its own license (GPL-3.0 at the time of writing).

Compares the specs in `.spec-workflow/` with the code. It maps which source files each spec covers, lists files no spec documents, flags specs with no recent implementation activity and critical files (auth, AI safety, licensing rules) that lack a spec, and writes a coverage report. Use on `/spec-workflow-drift` or when asked to "check spec drift", "show spec coverage", or "which files aren't in any spec".

## What it looks like

Example output, invented data. A full report starts with the totals, flags any security-relevant file that no spec covers, and ends with prioritized actions:

```markdown
# Spec-Workflow Drift Report

**Generated:** 2026-03-02T09:00:00Z
**Project:** <project>
**Total Specs:** 8 active
**Total Files:** 142
**Coverage:** 89% (126/142 files)
**Drift Files:** 16

🚨 CRITICAL DRIFT DETECTED

The following critical files are not documented in any spec:

- src/lib/rate-limit.ts (SECURITY: rate limiting)

## 🎯 Action Items

1. **Immediate:**
   - Document 1 critical file
2. **This Sprint:**
   - Create a utility spec for 4 infrastructure files
3. **Monitor:**
   - 1 aging spec (no activity in 41 days)
```

How a spec's age is judged, from the date of its last implementation log entry:

| Last logged activity | Status |
|---|---|
| 30 days or less | ACTIVE |
| 31 to 90 days | AGING |
| More than 90 days | STALE |

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `review-older-issues`, `saas-metrics`, `service-debugging`, `spec-workflow`, `transactional-email`. Run it as `/engineering-practices:spec-workflow-drift`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh spec-workflow-drift   # into ~/.claude/skills/spec-workflow-drift
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/spec-workflow-drift/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex spec-workflow-drift   # into ~/.agents/skills/spec-workflow-drift
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/spec-workflow-drift/` instead. Or copy this folder by hand to `~/.agents/skills/spec-workflow-drift/`, or `.agents/skills/spec-workflow-drift/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/spec-workflow-drift/` for personal use (`scripts/install.sh --target codex spec-workflow-drift` does this), or `<repo>/.agents/skills/spec-workflow-drift/` for one repository.
- Windsurf: `<repo>/.agents/skills/spec-workflow-drift/`.
- Cline: `<repo>/.cline/skills/spec-workflow-drift/`, `<repo>/.claude/skills/spec-workflow-drift/` or `~/.cline/skills/spec-workflow-drift/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app has no access to your repo.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT has no access to your repo.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
