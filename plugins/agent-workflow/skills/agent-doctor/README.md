# Agent Doctor

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Inspects a project's discovered agent instructions (`AGENTS.md`, `CLAUDE.md`) and skill folders under `.agents`, `.codex`, and `.claude` for static wiring problems. The bundled scanner is read-only and bounded: it never loads, changes, or enables anything, rejects symlink escapes, and reports findings as Markdown or JSON. An optional `--model <name>` option reports, as an advisory, skills whose prose claims a different model identity. The `--usage` mode reads local Claude Code and Codex session logs (read-only, skill names and counts only) and lists skills that are rarely or never called, with offline freshness notes. The agent then asks the owner, skill by skill, whether to update, keep, or archive; `scripts/skill_archive.py` archives only after an explicit yes, never deletes, and can restore.

## Install

Copy this complete folder to `~/.claude/skills/agent-doctor/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/agent-doctor/` for personal Codex use. For repository-only use, copy to `.claude/skills/agent-doctor/` or `.agents/skills/agent-doctor/` respectively. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/agent_doctor.py` — the read-only scanner and `--usage` report (Python 3, standard library only).
- `scripts/skill_archive.py` — moves skills into a dated archive folder and back, after an explicit `--yes`; never deletes.
- `references/usage.md` — usage report options, counting rules, verdicts, privacy, the required ask-first workflow, and archive exit codes.
- `tests/` — unit tests with temporary fixtures and synthetic logs; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
