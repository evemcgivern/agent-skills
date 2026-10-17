# Scrub AI Tells

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Reports and removes the characters that mark prose as machine-written: invisible characters (zero-width space, word joiner, byte-order mark, soft hyphen) and non-standard spaces always, and visible tells (em dashes, en dashes, curly quotes, the ellipsis glyph) only when asked. It is not watermark removal. Use before publishing a blog post, doc, or README written with AI help, or when someone asks to "strip invisible Unicode" or says text "looks like AI wrote it". The bundled script is stdlib-only Python and exits 1 when tells are found, so report mode also works as a CI check.

## Install

Copy this complete folder to `~/.claude/skills/scrub-ai-tells/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/scrub-ai-tells/` for personal Codex use. For repository-only use, copy to `.claude/skills/scrub-ai-tells/` or `.agents/skills/scrub-ai-tells/` respectively. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scrub_ai_tells.py` — stdlib-only Python script that reports or rewrites tells in files, directories, or stdin.
- `tests/` — unittest checks for the script (`python3 -m unittest discover` inside `tests/`).
- `VERSION` and `CHANGELOG.md` — package version history.
