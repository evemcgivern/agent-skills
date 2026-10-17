# Scrub AI Tells

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> Whether ChatGPT skills can run the bundled Python script is not verified.

Reports and removes the characters that mark prose as machine-written: invisible characters (zero-width space, word joiner, byte-order mark, soft hyphen) and non-standard spaces always, and visible tells (em dashes, en dashes, curly quotes, the ellipsis glyph) only when asked. It is not watermark removal. Use before publishing a blog post, doc, or README written with AI help, or when someone asks to "strip invisible Unicode" or says text "looks like AI wrote it". The bundled script is stdlib-only Python and exits 1 when tells are found, so report mode also works as a CI check.

## What it looks like

A real run on a two-line draft that holds a zero-width space, a no-break space, a narrow no-break space, two em dashes, three curly quotes and an ellipsis glyph. Report mode counts each kind and exits 1, so it also works as a CI check:

```text
$ python3 scrub_ai_tells.py draft.md
draft.md:
  invisible     1
  exotic_space  2
  em_dash       2
  curly_quote   3
  ellipsis      1

9 tell(s) total
$ echo $?
1
```

Applying it with the default em dash replacement keeps a `draft.md.bak` copy and changes only what the flags allow:

```text
$ python3 scrub_ai_tells.py draft.md --write --em-dash " - "
scrubbed draft.md (9 tells found)
```

| Tell | Found | After `--write --em-dash " - "` |
|---|---|---|
| Invisible (zero-width space) | 1 | Removed |
| Exotic space (no-break, narrow no-break) | 2 | Plain space |
| Em dash | 2 | Spaced hyphen ` - ` |
| Curly quote | 3 | Kept; needs `--straighten-quotes` |
| Ellipsis glyph | 1 | Kept; needs `--ellipsis` |

## Install

Copy this complete folder to `~/.claude/skills/scrub-ai-tells/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/scrub-ai-tells/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/scrub-ai-tells/` or `.agents/skills/scrub-ai-tells/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/scrub-ai-tells/` or `.claude/skills/scrub-ai-tells/`. Supporting files in this folder may be required. See the [install section of the collection README](../../../../README.md#install) for plugin installs and current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scrub_ai_tells.py` — stdlib-only Python script that reports or rewrites tells in files, directories, or stdin.
- `tests/` — unittest checks for the script (`python3 -m unittest discover` inside `tests/`).
- `VERSION` and `CHANGELOG.md` — package version history.
