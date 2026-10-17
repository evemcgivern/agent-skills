# Sonnet Prompt Improver

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Rewrites a prompt, system prompt, agent definition or skill so Claude Sonnet 5.5 does what you meant. It frames the request problem-first, adds only the fixes that match a symptom you have seen, and suggests effort and thinking settings. The fixes paraphrase Anthropic's [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) guide (read 2026-10-03, rechecked 2026-10-17). Use on `/sonnet-prompt-improver` or when asked to "improve this prompt for Sonnet".

## When and how to use it

**Use it when**
- Sonnet keeps stopping to ask questions before the work is done.
- You write a system prompt or agent definition for Sonnet 5.5.
- A JSON answer is wrong or does not parse.

**Try it**

```text
/sonnet-prompt-improver Why does Sonnet keep stopping to ask me? Here is my system prompt: [paste]
Improve this agent definition for Sonnet 5.5: [paste]
```

The improved prompt in one code block, with one line per change tied to the symptom you named. For standing prompts and JSON API calls, you also get suggested effort and thinking settings. Other agents can ask in words.

**Skip it when**
- The prompt works, or the model is not Sonnet 5.5. The skill adds fixes only for a symptom you can see.

## What it looks like

Example, invented prompt. What you type, including the symptom you have seen:

```text
/sonnet-prompt-improver Fix the date bug in the CSV export. Last time it also
added tests and docs I didn't ask for.
```

What comes back: the prompt framed problem-first, plus only the fix that matches the symptom, then one line per change.

```text
Problem: Fix the date bug in the CSV export.
Evidence: [ ] (the wrong date and the expected one)
Autonomy: If you have a solution you are happy with, do it. If you are unsure,
give me options or mocks and stop.
Done means: [ ]
When the asked work is done and checked, stop and report; mention extras at
the end instead of doing them.

- treated this as a message you type to an agent
- added an evidence slot and a done slot
- added the autonomy line
- added the stop-and-report line: it adds tests and docs nobody asked for
```

For a system prompt, agent definition, or JSON API call, the reply also suggests effort and thinking settings in one line, such as starting at high effort and sweeping levels against real evals.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:sonnet-prompt-improver`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh sonnet-prompt-improver   # into ~/.claude/skills/sonnet-prompt-improver
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/sonnet-prompt-improver/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex sonnet-prompt-improver   # into ~/.agents/skills/sonnet-prompt-improver
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/sonnet-prompt-improver/` instead. Or copy this folder by hand to `~/.agents/skills/sonnet-prompt-improver/`, or `.agents/skills/sonnet-prompt-improver/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/sonnet-prompt-improver/` for personal use (`scripts/install.sh --target codex sonnet-prompt-improver` does this), or `<repo>/.agents/skills/sonnet-prompt-improver/` for one repository.
- Windsurf: `<repo>/.agents/skills/sonnet-prompt-improver/`.
- Cline: `<repo>/.cline/skills/sonnet-prompt-improver/`, `<repo>/.claude/skills/sonnet-prompt-improver/` or `~/.cline/skills/sonnet-prompt-improver/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r sonnet-prompt-improver.zip sonnet-prompt-improver
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `sonnet-prompt-improver.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r sonnet-prompt-improver.zip sonnet-prompt-improver
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
