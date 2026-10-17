# Program Setup

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures. Use when starting a council or when an existing one has become a bottleneck or a rubber stamp.

## What it looks like

Review mode on the draft council charter in the kit's fictional demo estate:

| Step | What's missing | Why it matters | Fix |
|---|---|---|---|
| Sponsor | No executive sponsor named | No sponsor means no enforcement | Name an executive who controls the software budget |
| Decision rights | Purpose says the council oversees software; no decide or advise split, no stated thresholds | Every item can land on the agenda | Fill the decision-rights table, with a cost and risk threshold for each decision |
| Membership | 14 voting members | More than 9 slows decisions | Keep 5 to 9 voting; move the rest to consulted |
| Enforcement | No rule that procurement buys only approved items above threshold | Teams can buy around the council | Add the procurement rule and settle overlaps with other boards in writing |

````text
Decision needed: sponsor sign-off.

```findings
[{"type": "charter_gap", "id": "sponsor"},
 {"type": "charter_gap", "id": "decision-rights"},
 {"type": "charter_gap", "id": "membership-size"}]
```
````

The enforcement gap stays in the table only, because `charter_gap` findings use a fixed list of seven slugs. Review the same charter yourself in [practicum exercise 1](https://evemcgivern.github.io/app-governance-kit/practicum.html#program-setup).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `rationalization`. Run it as `/app-governance-kit:program-setup`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh program-setup   # into ~/.claude/skills/program-setup
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/program-setup/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex program-setup   # into ~/.agents/skills/program-setup
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/program-setup/` instead. Or copy this folder by hand to `~/.agents/skills/program-setup/`, or `.agents/skills/program-setup/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/program-setup/` for personal use (`scripts/install.sh --target codex program-setup` does this), or `<repo>/.agents/skills/program-setup/` for one repository.
- Windsurf: `<repo>/.agents/skills/program-setup/`.
- Cline: `<repo>/.cline/skills/program-setup/`, `<repo>/.claude/skills/program-setup/` or `~/.cline/skills/program-setup/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r program-setup.zip program-setup
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `program-setup.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r program-setup.zip program-setup
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

The kit's full site, with visuals and an interactive practicum: https://evemcgivern.github.io/app-governance-kit/

<!-- install:end -->

## Included

- `SKILL.md` and all workflow reference/template files:
- `SKILL.md`
- `checklist.md`
- `crosswalk.csv`
- `platform-guide.md`
- `sop.md`
- `template.md`
- `themes.md`
- `agents/openai.yaml` for ChatGPT/Codex skill-card metadata.
- `VERSION` and `CHANGELOG.md` for this package snapshot.

Source: [https://github.com/evemcgivern/app-governance-kit](https://github.com/evemcgivern/app-governance-kit).
