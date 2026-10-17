# Crosswalk

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing. Use when writing or auditing a control, or explaining how frameworks overlap.

## What it looks like

Example output for the three sample controls in the kit's fictional demo estate. Clause numbers come from `crosswalk.csv`:

| Control | XW row | ISO/IEC 19770-1 | COBIT 2019 | ISO/IEC 27001 | ISO/IEC 42001 |
|---|---|---|---|---|---|
| C1 Keep an accurate inventory with owners | XW-001 | 8.3 | BAI09.01 | A.5.9 | no direct equivalent |
| C2 Review access on a schedule, remove what is not needed | XW-016 | no direct equivalent | DSS05.04 | A.5.18 | no direct equivalent |
| C3 Assess each AI system for risk before deployment | XW-021 | no direct equivalent | APO12 | no direct equivalent | 6.1.4, A.5 |

````text
Gaps
C2: ISO/IEC 19770-1 and 42001 have no access-review clause; their auditors
    would look for the ISO/IEC 27001 control instead.
C3: ISO/IEC 27001 has no AI-specific clause; its auditor would look for the
    AI system inside the general risk assessment.

```findings
[{"type": "crosswalk_match", "id": "C1:XW-001"},
 {"type": "crosswalk_match", "id": "C2:XW-016"},
 {"type": "crosswalk_match", "id": "C3:XW-021"}]
```
````

Browse all 29 themes across the four frameworks in the [crosswalk explorer](https://evemcgivern.github.io/app-governance-kit/crosswalk.html), or map the controls yourself in [practicum exercise 3](https://evemcgivern.github.io/app-governance-kit/practicum.html#crosswalk).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `hardware-lifecycle`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:crosswalk`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh crosswalk   # into ~/.claude/skills/crosswalk
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/crosswalk/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex crosswalk   # into ~/.agents/skills/crosswalk
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/crosswalk/` instead. Or copy this folder by hand to `~/.agents/skills/crosswalk/`, or `.agents/skills/crosswalk/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/crosswalk/` for personal use (`scripts/install.sh --target codex crosswalk` does this), or `<repo>/.agents/skills/crosswalk/` for one repository.
- Windsurf: `<repo>/.agents/skills/crosswalk/`.
- Cline: `<repo>/.cline/skills/crosswalk/`, `<repo>/.claude/skills/crosswalk/` or `~/.cline/skills/crosswalk/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r crosswalk.zip crosswalk
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `crosswalk.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r crosswalk.zip crosswalk
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
