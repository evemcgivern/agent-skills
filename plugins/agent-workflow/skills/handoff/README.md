# Handoff

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT get no git or GitHub state.

Writes a copy-pasteable handoff prompt that lets a fresh session of your agent (Claude Code, Codex, Gemini CLI and others) resume the current work cold: why the work matters, what shipped, decisions not to reopen, branch and PR state, the next concrete action, relevant files, standing constraints, and the last few exchanges. Use when ending a session with "hand this off", "park this for tomorrow", or before `/clear`.

## When and how to use it

**Use it when**
- You stop mid-work and the next session must resume without re-reading everything.
- You are about to clear the session and want to keep the decisions.
- You want to move the work to a different agent.

**Try it**

```text
/handoff parking this for tomorrow
Write up where we are so a new session can resume this work.
```

One block to paste into a fresh session. It has the reason for the work, what shipped, decisions not to reopen, branch and uncommitted files, the next action and the key files. Your note goes in at the end, word for word. Other agents can ask in words.

**Skip it when**
- The work is finished and merged. A commit message or PR note is enough.

## What it looks like

Example output, invented data, shortened (a real handoff runs 600-1500 words). The sections always appear in this order. Open questions and the free-text note are left out here because there were none:

```text
# RESUME csv-importer — handoff

## Why we're here (strategic frame)
Large CSV exports time out on import. Streaming removes the file-size ceiling.

## Shipped this session
- PR #41 merged: streaming parser behind the `stream_import` flag
- #42 filed: quoted newlines split rows
- #43 filed: BOM breaks the header match
- `docs/import.md` updated with the flag and its default
- Benchmark recorded: 2 GB file imports in 40 s, was a timeout

## Locked-in decisions (do NOT re-litigate)
- Old parser stays until #43 closes: rollback must remain one flag flip

## In-flight state
- **Branch**: feat/import-progress
- **Uncommitted**: src/import/progress.ts
- **Unpushed**: up to date
- **Last commit**: feat(import): emit row counts
- **Open PRs on this branch**: none
- **Other open loops**: dev server on port 3000

## Next concrete action
On feat/import-progress, finish the row counter in src/import/progress.ts,
then run `npm test -- import` before opening the PR.

## Relevant files (paths + one-line descriptions)
- `src/import/progress.ts` — half-written progress emitter
- `src/import/stream.ts` — the parser that calls it

## Critical constraints
- No new parsing dependencies
- Keep the old parser path working
- Commit subjects use `type(scope): summary`

## Recent conversation (last 2-3 exchanges)
Agreed the bar shows rows, not percent: the total is unknown while streaming.
```

Below the block, the reply has exactly one more line: "Copy the block above into a fresh session of your agent (for example after `/new` or `/clear`)."

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `mission`, `orchestrator`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:handoff`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh handoff   # into ~/.claude/skills/handoff
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/handoff/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex handoff   # into ~/.agents/skills/handoff
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/handoff/` instead. Or copy this folder by hand to `~/.agents/skills/handoff/`, or `.agents/skills/handoff/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/handoff/` for personal use (`scripts/install.sh --target codex handoff` does this), or `<repo>/.agents/skills/handoff/` for one repository.
- Windsurf: `<repo>/.agents/skills/handoff/`.
- Cline: `<repo>/.cline/skills/handoff/`, `<repo>/.claude/skills/handoff/` or `~/.cline/skills/handoff/`.

The git and GitHub checks work in any local agent, and the project name comes from `CLAUDE.md`, `AGENTS.md` or `GEMINI.md`, whichever exists.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r handoff.zip handoff
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `handoff.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** In the Claude app the conversation sections work, but there is no git or GitHub state.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r handoff.zip handoff
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** In ChatGPT the conversation sections work, but there is no git or GitHub state.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.

