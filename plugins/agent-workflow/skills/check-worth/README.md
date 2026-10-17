# Check Worth

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Reviews an external PDF, image, screenshot, article, or URL against a repository's open and closed issues and its code, and sorts each idea into already tracked, shipped, superseded, a candidate new issue, or not actionable, with `file:line` evidence and `UNABLE TO VERIFY` where the source falls short. Read-only unless you authorize issue creation or code changes. Use on "/check-worth" or when asking whether an external idea is worth pulling into a repository.

## Install

Copy this complete folder to `~/.claude/skills/check-worth/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/check-worth/` for personal Codex use. For repository-only use, copy to `.claude/skills/check-worth/` or `.agents/skills/check-worth/` respectively. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
