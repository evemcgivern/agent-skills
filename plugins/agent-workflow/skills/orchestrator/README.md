# Orchestrator

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex partial, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%97%90%20%C2%B7%20ChatGPT%20%E2%9C%96-yellow)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it. Codex can hold its reply until its subagents finish, so the main thread may block between batches. Other agents need subagents; Gemini CLI's are experimental. Without background runs, the skill says so.

Turns the main session into a dispatcher that never blocks. It splits the work, sends each task to a background subagent with a self-contained brief, tracks every agent in a ledger file, checks each result before it reports, and answers you in a few lines, so you can keep talking while the work runs. Model choice follows `efficient-frontier-routing` when it is installed. Use with "orchestrate this", "fan this out" or "keep me unblocked".

Rewritten from [olivieropinotti/orchestrator-skill](https://github.com/olivieropinotti/orchestrator-skill) (MIT). See [THIRD-PARTY.md](../../../../THIRD-PARTY.md).

## When and how to use it

**Use it when**
- You have several independent tasks and want them running at once.
- You want to keep talking to the session while long work runs.
- A long session needs a record of which agent is doing what.

**Try it**

```text
/orchestrator
Orchestrate this: audit the auth routes, fix the flaky upload test, and draft the release notes.
status
stop audit-auth
```

Each task goes to its own named agent. The reply says what started and under which name. Results come back one at a time, checked against the brief. `status`, `stop <name>`, `stop all`, `redirect <name> to …` and `stop orchestrating` control it.

**Skip it when**
- The task is one step, a quick question or a conversation.
- The work needs your live input, such as an interactive login.

## What it looks like

Example ledger, invented data. It lives in `.claude/orchestrator.md` (or `.codex/orchestrator.md` in Codex) and is kept out of git:

```text
- [running] audit-auth (strong tier) — find routes that skip the session check — started 14:02
- [done]    fix-upload-test (mid tier) — fixture reset, tests pass — 14:20
- [lost]    release-notes (cheap tier) — agent gone with no report; restarted as release-notes-2 — 14:31
```

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:orchestrator`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh orchestrator   # into ~/.claude/skills/orchestrator
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/orchestrator/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b> — works with a limit</summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex orchestrator   # into ~/.agents/skills/orchestrator
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/orchestrator/` instead. Or copy this folder by hand to `~/.agents/skills/orchestrator/`, or `.agents/skills/orchestrator/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

**Limit:** Codex runs subagents in parallel but can hold its reply until they finish, so the main thread may block between batches.

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b> — works with a limit</summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/orchestrator/` for personal use (`scripts/install.sh --target codex orchestrator` does this), or `<repo>/.agents/skills/orchestrator/` for one repository.
- Windsurf: `<repo>/.agents/skills/orchestrator/`.
- Cline: `<repo>/.cline/skills/orchestrator/`, `<repo>/.claude/skills/orchestrator/` or `~/.cline/skills/orchestrator/`.

**Limit:** Works where the agent can start subagents; where it cannot run them in the background, the skill says so and runs small batches.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app has no background subagents.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT has no documented subagents.

Use Claude Code or Codex on your computer instead.

</details>

The dispatcher needs subagents. Claude Code runs them in the background. Codex runs them in parallel but can hold its reply until they finish. In other agents, where work cannot run in the background, the skill says so and runs small batches.

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
