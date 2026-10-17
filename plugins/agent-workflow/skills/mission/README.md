# Mission

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they have no git worktree and keep no state between sessions.

Keeps a small mission record outside the repository so work can resume cleanly in a later agent session. The record holds the outcome, constraints, milestones, decisions, next action, and hashed evidence files, and is bound to one Git worktree. The bundled script never runs stored actions, starts background processes, or changes Git state, and it uses revision checks and file locks so stale writers fail instead of overwriting state. Use it when asked to start, checkpoint, resume, or complete a mission across sessions.

## When and how to use it

**Use it when**
- A job runs for several days and has clear milestones.
- You want to record decisions and proof files so the next session does not guess.
- You return to a task after a break and need the next unfinished step.

**Try it**

```text
Start a mission called release-notes. Outcome: publish accurate release notes. Milestone: draft, done when the notes name every user-facing change. Next action: draft the notes.
Resume the release-notes mission.
```

A saved record outside your repo. On resume, you get the next unfinished milestone and the recorded next action. Each finished milestone needs an evidence file, and the record stores that file's hash. The skill never runs the next action for you. It needs a Git worktree and a POSIX system.

**Skip it when**
- The task fits one session, or you want the agent to carry out the work. Mission only records progress.

## What it looks like

Real output, from a throwaway Git repository and state folder. The mission has two milestones, `draft` and `review`. One checkpoint marked `draft` complete with an evidence file. A later session asks where things stand (JSON trimmed to the keys that matter):

```text
$ python3 scripts/mission.py resume release-notes
{
  "inspect_first": "Inspect current effects before acting: effects may be in progress or uncertain",
  "next_action": "Review the draft",
  "next_unfinished": {
    "acceptance": "A second reader signs off",
    "description": "Review draft",
    "id": "review",
    "status": "pending"
  },
  "replay_action": false
}
```

`replay_action` is always `false`: the record says what to do next, and the agent decides whether to do it. Unsafe writes fail with a nonzero exit and leave the record unchanged:

```text
$ python3 scripts/mission.py checkpoint release-notes --expected-revision 1 ...
mission: stale revision: expected 1, current 2

$ python3 scripts/mission.py complete release-notes --expected-revision 2
mission: all milestones must be complete before completing the mission
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

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:mission`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh mission   # into ~/.claude/skills/mission
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/mission/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex mission   # into ~/.agents/skills/mission
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/mission/` instead. Or copy this folder by hand to `~/.agents/skills/mission/`, or `.agents/skills/mission/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/mission/` for personal use (`scripts/install.sh --target codex mission` does this), or `<repo>/.agents/skills/mission/` for one repository.
- Windsurf: `<repo>/.agents/skills/mission/`.
- Cline: `<repo>/.cline/skills/mission/`, `<repo>/.claude/skills/mission/` or `~/.cline/skills/mission/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app has no git worktree and keeps no state between sessions.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT has no git worktree and keeps no state between sessions.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/mission.py` — the mission CLI (Python 3 standard library, POSIX).
- `tests/test_mission.py` — unittest suite for the CLI; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
