# Scrub AI Tells

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> Whether ChatGPT skills can run the bundled Python script is not verified.

Reports and removes the characters that mark prose as machine-written: invisible characters (zero-width space, word joiner, byte-order mark, soft hyphen) and non-standard spaces always, and visible tells (em dashes, en dashes, curly quotes, the ellipsis glyph) only when asked. It is not watermark removal. Use before publishing a blog post, doc, or README written with AI help, or when someone asks to "strip invisible Unicode" or says text "looks like AI wrote it". The bundled script is stdlib-only Python and exits 1 when tells are found, so report mode also works as a CI check.

## When and how to use it

**Use it when**
- You will publish a blog post that you drafted with AI help.
- Pasted text has invisible characters that break search or diffs.
- You want a check on a docs folder that fails when such characters appear.

**Try it**

```text
/scrub-ai-tells draft.md
Remove the invisible characters in draft.md and show me the diff.
```

A report with counts per character type, such as zero-width spaces, em dashes and curly quotes. Invisible characters are removed with --write, and the original is saved as draft.md.bak. Punctuation changes happen only after you agree. Other agents can ask in words.

**Skip it when**
- You want text that sounds less like AI, or you want to remove a watermark. This skill changes characters only.

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

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install writing@evemcgivern-skills
```

This installs the whole `writing` plugin, so you also get its other skills: `clearly`, `table`. Run it as `/writing:scrub-ai-tells`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install writing@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update writing@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh scrub-ai-tells   # into ~/.claude/skills/scrub-ai-tells
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **writing** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/scrub-ai-tells/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex scrub-ai-tells   # into ~/.agents/skills/scrub-ai-tells
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/scrub-ai-tells/` instead. Or copy this folder by hand to `~/.agents/skills/scrub-ai-tells/`, or `.agents/skills/scrub-ai-tells/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/scrub-ai-tells/` for personal use (`scripts/install.sh --target codex scrub-ai-tells` does this), or `<repo>/.agents/skills/scrub-ai-tells/` for one repository.
- Windsurf: `<repo>/.agents/skills/scrub-ai-tells/`.
- Cline: `<repo>/.cline/skills/scrub-ai-tells/`, `<repo>/.claude/skills/scrub-ai-tells/` or `~/.cline/skills/scrub-ai-tells/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r scrub-ai-tells.zip scrub-ai-tells
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `scrub-ai-tells.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r scrub-ai-tells.zip scrub-ai-tells
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** Whether ChatGPT skills can run the bundled Python script is not verified, so ChatGPT may apply the rules by hand.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scrub_ai_tells.py` — stdlib-only Python script that reports or rewrites tells in files, directories, or stdin.
- `tests/` — unittest checks for the script (`python3 -m unittest discover` inside `tests/`).
- `VERSION` and `CHANGELOG.md` — package version history.
