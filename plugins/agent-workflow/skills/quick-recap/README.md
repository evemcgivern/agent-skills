# Quick Recap

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT the status line works, but the install step cannot write to your instruction files; paste the text in yourself.

Defines a one-line red/yellow/green status line that ends every agent response that completes work, and how to install it as standing instructions in AGENTS.md or CLAUDE.md. Use when asked to "add a status line", "end responses with a recap", "show done/pending/blocked at the end", or when project instructions require the quick-recap convention.

## When and how to use it

**Use it when**
- You run long tasks and want to see in one line if the work is done, pending or blocked.
- You want every reply in a project to end the same way.
- You want to add the status rule to AGENTS.md or CLAUDE.md once.

**Try it**

```text
Add the quick-recap status line to my AGENTS.md.
End each reply with a one-line status: green, yellow or red.
```

A short section added to your instruction file, unless one exists. After that, each reply that completes work ends with one line under 100 characters: green for finished, yellow for finished with a named follow-up, red for blocked on you.

**Skip it when**
- Your message is a plain question. A question needs no status line.

## What it looks like

The last line of a reply that finished some work. The color is chosen from your point of view:

| Line | Use it when |
|---|---|
| `🟢 Updated quick recap docs with output examples` | The requested work is finished. |
| `🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks` | Finished except a non-routine follow-up, which the line names. |
| `🔴 Need the production API key to continue` | Blocked on something only you can supply. |

In place, it closes the reply with nothing after it:

```text
The webhook handler now verifies signatures and rejects replays.
Tests cover both paths.

🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks
```

These fail the convention: `🟢 Done` (says nothing), `🟡 Open a PR next` (a routine step is still 🟢), and any sign-off or `---` after the line.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `orchestrator`, `problem-first`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:quick-recap`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh quick-recap   # into ~/.claude/skills/quick-recap
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/quick-recap/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex quick-recap   # into ~/.agents/skills/quick-recap
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/quick-recap/` instead. Or copy this folder by hand to `~/.agents/skills/quick-recap/`, or `.agents/skills/quick-recap/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/quick-recap/` for personal use (`scripts/install.sh --target codex quick-recap` does this), or `<repo>/.agents/skills/quick-recap/` for one repository.
- Windsurf: `<repo>/.agents/skills/quick-recap/`.
- Cline: `<repo>/.cline/skills/quick-recap/`, `<repo>/.claude/skills/quick-recap/` or `~/.cline/skills/quick-recap/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r quick-recap.zip quick-recap
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `quick-recap.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** In the Claude app the status line works, but paste the install text into project instructions yourself.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r quick-recap.zip quick-recap
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** In ChatGPT the status line works, but there is no AGENTS.md to install it into.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
