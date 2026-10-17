# Service Debugging

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it ranks causes only from evidence you paste in.

Turns a live production symptom into a ranked, falsifiable cause. It starts from the system's catalog of known failures and the most recent change, pulls evidence for the leading hypothesis only, and ends with a symptom statement, one to three ranked causes each with the check that would rule it out, links a person can open, and a confirmed or unconfirmed verdict. Use when a deployed service returns 500s, times out, shows a blank page, silently does nothing, or keeps failing the same way, or when asked to "debug prod" or "find the root cause".

## When and how to use it

**Use it when**
- Users report 500 errors that began after a deploy.
- A page returns 404 in production but exists in the repo.
- The same failure came back after "we fixed that".

**Try it**
```text
Checkout returns 500 for about 1 in 40 requests since 14:05 UTC. Find the most likely cause.
Our nightly sync shows green but writes nothing. Rank the causes and tell me how to rule each one out.
```
You get four parts: the symptom, one to three ranked causes with a check that would rule each out, links to the evidence, and a verdict of CONFIRMED or UNCONFIRMED.

**Skip it when**
- The site is down right now. Roll back or run incident response first, then diagnose.

## What it looks like

Example output, invented data. Every run returns the same four parts, in this order:

```text
SYMPTOM
  Since 14:05 UTC, POST /api/checkout returns 500 for about 1 in 3 requests, all tenants.

RANKED CAUSES
  1. Connection-pool exhaustion after the 14:02 deploy raised worker count from 4 to 12
     Evidence: pool-timeout errors start at 14:05; 12 workers x 10 connections > database limit of 100
     Rules it out: errors continue after rolling back to 4 workers
  2. Slow query from a missing index on orders.customer_id
     Evidence: p95 query time up 6x in the same window
     Rules it out: EXPLAIN shows an index scan on the live database

VERIFICATION LINKS
  <log query: pool timeouts, 13:50-14:30>   <deploy 14:02>   src/db/pool.ts:18

VERDICT
  UNCONFIRMED. Next: roll back the worker count, then rerun cause 1's check.
```

Where to look first, from the skill's symptom table:

| Symptom | Look here first |
|---|---|
| Blanket 5xx starting at a timestamp | The deploy or config change at that timestamp |
| Works locally, dead in prod | Missing or different env var, build-time versus runtime config |
| Silent no-op | A swallowed exception, an early return, a guard failing closed |
| Wrong data, no error | Partially applied migration, a default overwriting a real value |

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `review-older-issues`, `saas-metrics`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:service-debugging`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh service-debugging   # into ~/.claude/skills/service-debugging
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/service-debugging/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex service-debugging   # into ~/.agents/skills/service-debugging
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/service-debugging/` instead. Or copy this folder by hand to `~/.agents/skills/service-debugging/`, or `.agents/skills/service-debugging/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/service-debugging/` for personal use (`scripts/install.sh --target codex service-debugging` does this), or `<repo>/.agents/skills/service-debugging/` for one repository.
- Windsurf: `<repo>/.agents/skills/service-debugging/`.
- Cline: `<repo>/.cline/skills/service-debugging/`, `<repo>/.claude/skills/service-debugging/` or `~/.cline/skills/service-debugging/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r service-debugging.zip service-debugging
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `service-debugging.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** The Claude app ranks causes only from evidence you paste in.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r service-debugging.zip service-debugging
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** ChatGPT ranks causes only from evidence you paste in.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
