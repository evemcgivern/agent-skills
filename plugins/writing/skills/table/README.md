# Table

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Turns information into a table a reader can scan in one pass: rows are the things compared, columns are the attributes that change the decision, unknown cells are marked, and the answer is bolded. It also says when content should stay prose or a list. Use on `/table` or when asked to "put that in a table", "tabulate this", or "compare these side by side".

## When and how to use it

**Use it when**
- You compare three vendor quotes side by side.
- You have test failures across several cases with the same fields.
- A paragraph repeats the same fields for each item.

**Try it**

```text
/table Acme: $4,200, 14 days. Birch: $3,900, 21 days. Cedar: $4,500, 10 days.
Put the failing tests from this log in a table, sorted by cause.
```

A Markdown table with one row per item, the answer cells in bold, a source line if the values came from a file or command, and one line for any cell it could not fill. Other agents can ask in words.

**Skip it when**
- Your content is a list of steps or a single idea. The skill gives prose or a list instead.

## What it looks like

A messy comparison turned into a table. Example output, invented data.

**Before**

```text
- option A is $20/mo, deploys from git, has a free tier, no EU region i think
- B: 25 a month, git deploys yes, EU region yes
- option C has a free tier and git deploy, paid plan $7/mo, EU region not sure
we need EU hosting
```

**After**

All three options deploy from git.

| Option | Paid plan (USD/month) | Free tier | EU region | Fits EU need |
|---|---|---|---|---|
| A | 20 | yes | no | no |
| **B** | **25** | n/a | **yes** | **yes** |
| C | 7 | yes | n/a | n/a |

Gaps: B's free tier and C's EU region are not in the list.

Rows keep the reader's order, the shared git-deploy attribute moves to a sentence above the table, unknown cells say `n/a`, the unit sits in the header, the verdict is the last column, and the answer is bold.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install writing@evemcgivern-skills
```

This installs the whole `writing` plugin, so you also get its other skills: `clearly`, `scrub-ai-tells`. Run it as `/writing:table`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install writing@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update writing@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh table   # into ~/.claude/skills/table
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **writing** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/table/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex table   # into ~/.agents/skills/table
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/table/` instead. Or copy this folder by hand to `~/.agents/skills/table/`, or `.agents/skills/table/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/table/` for personal use (`scripts/install.sh --target codex table` does this), or `<repo>/.agents/skills/table/` for one repository.
- Windsurf: `<repo>/.agents/skills/table/`.
- Cline: `<repo>/.cline/skills/table/`, `<repo>/.claude/skills/table/` or `~/.cline/skills/table/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r table.zip table
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `table.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/writing/skills && zip -r table.zip table
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
