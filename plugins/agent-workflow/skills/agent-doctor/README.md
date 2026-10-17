# Agent Doctor

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they have no access to your project or session logs. Other agents: the scan checks only the .agents, .codex and .claude skill folders, and usage reads only Claude Code and Codex logs.

Inspects a project's discovered agent instructions (`AGENTS.md`, `CLAUDE.md`) and skill folders under `.agents`, `.codex`, and `.claude` for static wiring problems. The bundled scanner is read-only and bounded: it never loads, changes, or enables anything, rejects symlink escapes, and reports findings as Markdown or JSON. An optional `--model <name>` option reports, as an advisory, skills whose prose claims a different model identity. The `--usage` mode reads local Claude Code and Codex session logs (read-only, skill names and counts only) and lists skills that are rarely or never called, with offline freshness notes. The agent then asks the owner, skill by skill, whether to update, keep, or archive; `scripts/skill_archive.py` archives only after an explicit yes, never deletes, and can restore.

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

Copy this complete folder to `~/.claude/skills/agent-doctor/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/agent-doctor/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/agent-doctor/` or `.agents/skills/agent-doctor/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/agent-doctor/` or `.claude/skills/agent-doctor/`. In other agents the scan still runs, but it checks only the `.agents`, `.codex` and `.claude` skill folders and reads only Claude Code and Codex session logs. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/agent_doctor.py` — the read-only scanner and `--usage` report (Python 3, standard library only).
- `scripts/skill_archive.py` — moves skills into a dated archive folder and back, after an explicit `--yes`; never deletes.
- `references/usage.md` — usage report options, counting rules, verdicts, privacy, the required ask-first workflow, and archive exit codes.
- `tests/` — unit tests with temporary fixtures and synthetic logs; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
