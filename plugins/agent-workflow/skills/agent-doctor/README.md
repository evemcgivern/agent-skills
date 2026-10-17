# Agent Doctor

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they have no access to your project or session logs. Other agents: the scan checks only the .agents, .codex and .claude skill folders, and usage reads only Claude Code and Codex logs.

Inspects a project's discovered agent instructions (`AGENTS.md`, `CLAUDE.md`) and skill folders under `.agents`, `.codex`, and `.claude` for static wiring problems. The bundled scanner is read-only and bounded: it never loads, changes, or enables anything, rejects symlink escapes, and reports findings as Markdown or JSON. An optional `--model <name>` option reports, as an advisory, skills whose prose claims a different model identity. The `--usage` mode reads local Claude Code and Codex session logs (read-only, skill names and counts only) and lists skills that are rarely or never called, with offline freshness notes. The agent then asks the owner, skill by skill, whether to update, keep, or archive; `scripts/skill_archive.py` archives only after an explicit yes, never deletes, and can restore.

## When and how to use it

**Use it when**
- A skill you wrote does not load, and you do not know why.
- Two skills share a name, or a link inside a skill points to a missing file.
- Your skill folder is crowded and you want to know which skills you never call.

**Try it**

```text
Why does my release-notes skill not load? Check my agent setup.
Which of my skills have no calls in the last 90 days?
```

A table of problems with severity, file and line, or a usage table with a verdict for each skill. For each rarely used skill, the agent asks if you want to update, keep or archive it. It archives only after your yes. If your logs reach back less than 90 days, skills show as unknown instead of unused.

**Skip it when**
- You need to know if a skill works when it runs. This scan reads files only and does not run anything.

## What it looks like

Real output, from a run on a throwaway project and home folder built for this example (paths shortened to `~` and `<project>`, sources list left out). The wiring scan lists each problem with its file and line:

```text
$ python3 scripts/agent_doctor.py --project <project> --home ~ --model claude-opus-5-5
| Severity | Code                      | File                                            | Line |
| -------- | ------------------------- | ----------------------------------------------- | ---: |
| advisory | model_role_mismatch       | ~/.agents/skills/daily-brief/SKILL.md           |    5 |
| observed | duplicate_skill_name      | ~/.agents/skills/release-notes/SKILL.md         |    1 |
| observed | missing_skill_metadata    | <project>/.claude/skills/lint-fix/SKILL.md      |    1 |
| observed | duplicate_skill_name      | <project>/.claude/skills/release-notes/SKILL.md |    1 |
| observed | broken_markdown_reference | <project>/.claude/skills/release-notes/SKILL.md |    5 |
```

The usage report counts calls in local session logs (here, synthetic logs) and gives each skill a verdict:

```text
$ python3 scripts/agent_doctor.py --usage --project <project> --home ~
Window: last 90 days. RARELY USED means fewer than 3 calls found. Names and counts only.
Logs reach back 200 days and cover the window.

| Skill         | Uses in window | Last used  | Days since SKILL.md changed | Verdict        |
| ------------- | -------------: | ---------- | --------------------------: | -------------- |
| lint-fix      |              0 | -          |                         400 | NO CALLS FOUND |
| old-helper    |              0 | -          |                         400 | NO CALLS FOUND |
| daily-brief   |              1 | 2026-09-07 |                         400 | RARELY USED    |
| release-notes |              7 | 2026-10-16 |                         400 | ACTIVE         |

Totals: 4 skills, 8 calls found in the window; NO CALLS FOUND 2, RARELY USED 1, ACTIVE 1.
```

Both tables are trimmed: the scan also prints a Message column, and the usage report a Source column and freshness notes. After the usage table, the agent asks about each flagged skill in turn: update, keep, or archive. It archives only after an explicit yes, and `scripts/skill_archive.py restore` brings a skill back.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `ambition`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:agent-doctor`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh agent-doctor   # into ~/.claude/skills/agent-doctor
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/agent-doctor/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex agent-doctor   # into ~/.agents/skills/agent-doctor
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/agent-doctor/` instead. Or copy this folder by hand to `~/.agents/skills/agent-doctor/`, or `.agents/skills/agent-doctor/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b> — works with a limit</summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/agent-doctor/` for personal use (`scripts/install.sh --target codex agent-doctor` does this), or `<repo>/.agents/skills/agent-doctor/` for one repository.
- Windsurf: `<repo>/.agents/skills/agent-doctor/`.
- Cline: `<repo>/.cline/skills/agent-doctor/`, `<repo>/.claude/skills/agent-doctor/` or `~/.cline/skills/agent-doctor/`.

**Limit:** The scan checks only the .agents, .codex and .claude skill folders, and the usage report reads only Claude Code and Codex logs.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app has no access to your project or session logs.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT has no access to your project or session logs.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/agent_doctor.py` — the read-only scanner and `--usage` report (Python 3, standard library only).
- `scripts/skill_archive.py` — moves skills into a dated archive folder and back, after an explicit `--yes`; never deletes.
- `references/usage.md` — usage report options, counting rules, verdicts, privacy, the required ask-first workflow, and archive exit codes.
- `tests/` — unit tests with temporary fixtures and synthetic logs; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
