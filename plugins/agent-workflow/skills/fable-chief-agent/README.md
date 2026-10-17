# Fable Chief Agent

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT have no documented subagents, so the delegation loop cannot run. Other agents: needs subagents on a chosen model (Gemini CLI, Antigravity CLI, Cursor, OpenCode); others not verified.

Makes the most capable, most expensive model in a session the senior decision-maker. It keeps that model's reasoning for intent, architecture, decomposition, tradeoffs, final review, and synthesis, and routes discovery, implementation, tests, logs, and verification to cheaper agents by tier. For high-risk work it recommends a review by a model from a different vendor when one is available, and otherwise a fresh same-vendor reviewer, labelled as not cross-vendor.

## When and how to use it

**Use it when**
- Your main session runs on the most expensive model and you want it to decide, not to read files.
- A large refactor needs design choices and also a lot of searching and test runs.
- You want a short final answer with the decisions and the checks, not a long log.

**Try it**

```text
Act as chief agent. Plan the move of the orders service to a new queue and delegate the file reading and test runs.
Delegate the grunt work and keep your own reasoning for the design choices.
```

Cheaper agents gather facts and do scoped edits. The top model decides and reviews their evidence. You get a short answer: what was decided, the check result and the remaining risk.

**Skip it when**
- The task is small, or the main model is not top-tier. Use efficient-frontier-routing instead.

## What it looks like

Who does what. Tier names follow the Claude 5 family; with another provider, map them to its strong, standard, and small models.

| Tier | Owns | Does not |
|---|---|---|
| Fable (the top model in the session) | Real intent, scope, approach, task order, tradeoffs, hidden risks, settling disagreements, final review and answer | Search, read, edit, test, or verify when someone cheaper can |
| Opus | Hardest delegated work: complex implementation, deep debugging, cross-module, security, concurrency, reviewing cheaper agents | Hold final authority |
| Sonnet | Scoped implementation, tests, local refactors, clear failures, following existing patterns | Make product calls or change architecture |
| Haiku | Repo discovery, file and log summaries, checklist checks, edge-case scans | Decide direction: it reports facts |

The boundary in one line:

> If the task is mostly searching, reading, editing, testing, or verifying, it belongs to another agent. If it involves intent, design, tradeoffs, risk, disagreement, or final approval, it belongs to Fable.

For high-risk work (auth, billing, migrations, data loss and the like), Fable decides, Opus handles or reviews the hard parts, and a reviewer from a different vendor is recommended when available. A same-vendor review is labelled as not cross-vendor.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:fable-chief-agent`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh fable-chief-agent   # into ~/.claude/skills/fable-chief-agent
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/fable-chief-agent/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex fable-chief-agent   # into ~/.agents/skills/fable-chief-agent
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/fable-chief-agent/` instead. Or copy this folder by hand to `~/.agents/skills/fable-chief-agent/`, or `.agents/skills/fable-chief-agent/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b> — works with a limit</summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/fable-chief-agent/` for personal use (`scripts/install.sh --target codex fable-chief-agent` does this), or `<repo>/.agents/skills/fable-chief-agent/` for one repository.
- Windsurf: `<repo>/.agents/skills/fable-chief-agent/`.
- Cline: `<repo>/.cline/skills/fable-chief-agent/`, `<repo>/.claude/skills/fable-chief-agent/` or `~/.cline/skills/fable-chief-agent/`.

**Limit:** Needs subagents on a chosen model: Gemini CLI, Antigravity CLI, Cursor and OpenCode document them; GitHub Copilot, Windsurf and Cline are not verified.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app has no documented subagents, so the delegation loop cannot run.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT has no documented subagents, so the delegation loop cannot run.

Use Claude Code or Codex on your computer instead.

</details>

The delegation needs subagents on a chosen model: Claude Code, Codex, Gemini CLI and Antigravity CLI have them; other agents are not verified.

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
