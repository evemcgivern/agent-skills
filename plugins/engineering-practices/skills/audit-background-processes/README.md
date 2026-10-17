# Audit Background Processes

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they cannot see your computer's processes.

Inventories stray background processes that long agent sessions leave behind, such as watch loops, `tail -f` on finished logs, orphaned `sleep` calls, and detached runs, and cleans them up without killing anyone else's live work. The rule is to confirm ownership first and kill by PID, never by a broad `pkill -f` pattern. The bundled script reports suspected orphans with PID, parent, age and command, and kills nothing unless you pass `--kill` with specific PIDs that are still on its suspect list. Use it before any pattern-based kill, when a machine feels loaded, or when a run died for no clear reason.

## When and how to use it

**Use it when**
- A machine is slow after a long agent session and you suspect leftover watch loops.
- A test run died with no error and you fear a broad `pkill` hit it.
- You want to clean up stray `tail -f` and `sleep` jobs without harming other sessions.

**Try it**
```text
List the stray background processes on this machine. Do not kill anything yet.
The report shows PIDs 4120 and 4133 as old sleep loops that I started. Kill only those two.
```
You get a report of your own shells, live test runs and suspected orphans, each with PID, parent, age and command. Other users' processes are left out of the report. Kills go by PID only, and only for PIDs still on the list.

**Skip it when**
- You started one job and know its PID. Run `kill <pid>` yourself. The Claude app and ChatGPT cannot see your processes.

## What it looks like

Real output from a report run on a test machine, after starting three throwaway processes and closing the shell that launched them. The other suspects on that machine were login helpers and app agents, which is why you read every line before passing a PID to `--kill`:

```text
=== your interactive shells (never kill) ===
  959   958 02-00:17:06 -zsh
81810 81809    03:47:12 -zsh

=== your live test and benchmark runs (killing one loses its in-flight work) ===
  none

=== suspected orphans: PID PPID AGE COMMAND ===
3383 1 00:03 sleep 3600
3385 1 00:03 bash -c while true; do sleep 30; done
3387 1 00:03 tail -f /dev/null
... (18 more lines, trimmed: login helpers and app agents)

Read each line before acting. To kill some of them: ~/.claude/skills/audit-background-processes/audit.sh --kill PID [PID...]
```

How to read a row:

| Signal | Safe to kill? |
|---|---|
| `ppid = 1` and it is a watch or `sleep` you started | Yes, by PID |
| `-zsh`, `-bash`, or `zsh -i` | Never, it is someone's terminal |
| A test or benchmark run, even with `ppid = 1` | Ask its owner first |
| You cannot tell whose it is | Ask first |

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `review-older-issues`, `saas-metrics`, `service-debugging`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:audit-background-processes`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh audit-background-processes   # into ~/.claude/skills/audit-background-processes
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/audit-background-processes/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex audit-background-processes   # into ~/.agents/skills/audit-background-processes
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/audit-background-processes/` instead. Or copy this folder by hand to `~/.agents/skills/audit-background-processes/`, or `.agents/skills/audit-background-processes/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/audit-background-processes/` for personal use (`scripts/install.sh --target codex audit-background-processes` does this), or `<repo>/.agents/skills/audit-background-processes/` for one repository.
- Windsurf: `<repo>/.agents/skills/audit-background-processes/`.
- Cline: `<repo>/.cline/skills/audit-background-processes/`, `<repo>/.claude/skills/audit-background-processes/` or `~/.cline/skills/audit-background-processes/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app cannot see your computer's processes.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT cannot see your computer's processes.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `audit.sh` — process inventory that only reports by default; `--kill PID...` sends SIGTERM to named PIDs that are still suspected orphans.
- `VERSION` and `CHANGELOG.md` — package version history.
