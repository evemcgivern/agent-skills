# Goal Checklist

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT the progress strip works, but --sync cannot check git.

Tracks a multi-issue goal as a one-line progress strip that the agent re-prints whenever an item changes state. Symbols separate not started, in progress, merged to the integration branch, shipped, and verified, plus unproven and blocked markers. The strip round-trips, so pasting it back restores the list, and `--sync` checks recorded merge SHAs against git to move merged items to shipped.

## What it looks like

The legend, left to right through the pipeline:

| Symbol | Meaning |
|---|---|
| ⬜ | Not started |
| 🔄 | In progress |
| 🟦 | Merged to the integration branch (needs its merge SHA) |
| 🚀 | Merged to production and deployed (needs its merge SHA) |
| ✅ | Confirmed working in production, from a run someone watched |
| 🔍 | Believed fixed, unproven |
| ⏸️ | Blocked, and always names the blocker |

**A short goal** prints as one line. Items sort by state, then by issue number, and the tally underneath is the key:

```text
⬜ #37, ⬜ #112, 🔄 #94 (PR #137), 🟦 #106 (5f6e7d8c9)
· 2⬜ not started · 1🔄 in progress · 1🟦 on dev · 4 total
```

**A bigger goal** switches to one row per state once the line would wrap. When one decision holds up several items, a single line above the strip says so, and the blocked items share one row:

```text
Settling #130's schema unblocks five items.
⬜ #37, #112, #127, #134, #136
🔄 #130 1/5 (steps 2-5 designed)
🟦 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
🔍 #107 (needs deploy)
⏸️ on #130: #104, #105, #117, #119, #129
· 5⬜ not started · 1🔄 in progress · 2🟦 on dev · 1🔍 unproven · 5⏸️ blocked · 14 total
```

**After a deploy**, `--sync` checks each recorded merge SHA against git. The two merged items are now live, so they move up a stage and nothing else changes:

```text
⬜ #37, #112, #127, #134, #136
🔄 #130 1/5 (steps 2-5 designed)
🚀 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
🔍 #107 (needs deploy)
⏸️ on #130: #104, #105, #117, #119, #129
· 5⬜ not started · 1🔄 in progress · 2🚀 shipped · 1🔍 unproven · 5⏸️ blocked · 14 total
```

You never ask for the strip. Once a goal is active, the agent ends any reply where an item changed state with the updated strip. To resume in a new session, paste the last strip back in and it restores the list exactly, fractions and notes included.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:goal-checklist`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh goal-checklist   # into ~/.claude/skills/goal-checklist
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/goal-checklist/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex goal-checklist   # into ~/.agents/skills/goal-checklist
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/goal-checklist/` instead. Or copy this folder by hand to `~/.agents/skills/goal-checklist/`, or `.agents/skills/goal-checklist/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/goal-checklist/` for personal use (`scripts/install.sh --target codex goal-checklist` does this), or `<repo>/.agents/skills/goal-checklist/` for one repository.
- Windsurf: `<repo>/.agents/skills/goal-checklist/`.
- Cline: `<repo>/.cline/skills/goal-checklist/`, `<repo>/.claude/skills/goal-checklist/` or `~/.cline/skills/goal-checklist/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r goal-checklist.zip goal-checklist
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `goal-checklist.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** In the Claude app the progress strip works, but --sync cannot check git.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r goal-checklist.zip goal-checklist
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** In ChatGPT the progress strip works, but --sync cannot check git.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
