# Clearly

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT the writing rules work; the --explain video needs a local install, so it uses a diagram or page. On a computer, it asks before installing `manim` and `ffmpeg`.

Plain, short, scannable writing for tired readers, with comma-delimited lists and an optional `--explain` mode that picks a diagram, page, or short video.

## Credits

Adapted from ASD-STE100 (controlled technical English), Strunk's *The Elements of Style*, and the [i-have-adhd](https://github.com/ayghri/i-have-adhd) plugin (MIT, Ayoub Ghriss). See [THIRD-PARTY.md](../../../../THIRD-PARTY.md).

## When and how to use it

**Use it when**
- You write a status update, error message or commit message and want it short.
- A doc is hard to read and needs plain sentences.
- You want a topic explained as a diagram, page or short video.

**Try it**

```text
Rewrite this status update clearly: [paste]
Explain how our retry queue works --explain
```

Text that leads with the answer, with short sentences and one action per step. With --explain, the agent picks a diagram, page, video or text only, and tells you which in one line. Video needs manim, ffmpeg and macOS say. The agent asks before it installs anything.

**Skip it when**
- You write fiction, marketing copy, or text that must keep your own voice.

## What it looks like

The same status update before and after the skill. Example output, invented data.

**Before**

```text
Just wanted to give a quick update: basically, the deployment that was being
worked on yesterday has been delayed in order to allow the team to look into
some issues that were identified with the database migration (#6411, #279),
and it should hopefully be ready in a bit, assuming everything goes well.
```

**After**

```text
The deployment is delayed. The database migration failed two checks: 6411, 279.

1. Fix the migration script.
2. Run the two checks again.
3. Deploy when both checks pass. Expected: Thursday.

Next: open 6411 and read the failed check (2 minutes).
```

The answer comes first, each sentence holds one idea, filler is gone, issue numbers sit on one comma line without `#`, "in a bit" becomes a day, and the update ends with one short next action.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install writing@evemcgivern-skills
```

This installs the whole `writing` plugin, so you also get its other skills: `scrub-ai-tells`, `table`. Run it as `/writing:clearly`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install writing@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update writing@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh clearly   # into ~/.claude/skills/clearly
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **writing** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/clearly/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex clearly   # into ~/.agents/skills/clearly
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/clearly/` instead. Or copy this folder by hand to `~/.agents/skills/clearly/`, or `.agents/skills/clearly/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/clearly/` for personal use (`scripts/install.sh --target codex clearly` does this), or `<repo>/.agents/skills/clearly/` for one repository.
- Windsurf: `<repo>/.agents/skills/clearly/`.
- Cline: `<repo>/.cline/skills/clearly/`, `<repo>/.claude/skills/clearly/` or `~/.cline/skills/clearly/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r clearly.zip clearly
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `clearly.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** In the Claude app the writing rules work; the --explain video needs a local install, so it uses a diagram or page.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r clearly.zip clearly
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** In ChatGPT the writing rules work; the --explain video needs a local install, so it uses a diagram or page.

</details>

The `--explain` video needs a local install: on a computer, the skill asks before installing `manim` and `ffmpeg`. In the Claude app and ChatGPT the writing rules work, and `--explain` uses a diagram or page instead.

<!-- install:end -->
