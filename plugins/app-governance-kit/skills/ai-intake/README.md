# Ai Intake

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record. Use whenever a team proposes a new AI tool or changes how one is used.

## When and how to use it

**Use it when**
- A team wants to buy an AI tool that ranks job applicants.
- A chatbot gets a new use that changes who it affects.
- You need an AI inventory record for a tool already in use.

**Try it**
```text
A team wants an AI tool to rank job applicants. Tier it and fill in the inventory record.
We plan a customer support chatbot. What tier is it and which controls apply?
```
You get a restatement of the use case, a risk tier with reasoning under the EU AI Act, controls mapped to NIST AI RMF and ISO/IEC 42001, and an inventory record.

**Skip it when**
- You need a legal opinion. This skill gives a first tier and asks for legal review of any high-risk or prohibited result.

## What it looks like

Example output for one of the six AI systems in the kit's fictional demo estate:

````text
AI-004 (owner: HR)
Restatement: ranks job applicants' CVs and shortlists candidates for
interview. Affects job applicants. Uses CVs, which hold personal data.
Unverified: whether a person reviews each shortlist; where the data came from.

Prohibited practices: none apparent.
Tier: HIGH-RISK. Ranking or filtering job applicants is an employment use.
Obligations are phased in; check the current official timeline.
Legal content last reviewed: 2026-09. Legal review recommended.

Required controls: XW-021 risk assessment before deployment, XW-022 AI
inventory, XW-023 supplier oversight, XW-024 risk register; NIST AI RMF
Govern, Map, Measure, Manage.

Inventory record (template.md): id AI-004, owner HR, personal data yes,
risk tier high, approval pending.
Decision needed: approval to proceed.

```findings
[{"type": "high_risk_ai", "id": "AI-004"}]
```
````

The other five systems each get the same section. The website chat that answers shipment questions, for example, tiers as limited-risk because people must be told they are talking to AI. Practice the tiering in [practicum exercise 6](https://evemcgivern.github.io/app-governance-kit/practicum.html#ai-intake).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:ai-intake`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh ai-intake   # into ~/.claude/skills/ai-intake
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/ai-intake/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex ai-intake   # into ~/.agents/skills/ai-intake
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/ai-intake/` instead. Or copy this folder by hand to `~/.agents/skills/ai-intake/`, or `.agents/skills/ai-intake/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/ai-intake/` for personal use (`scripts/install.sh --target codex ai-intake` does this), or `<repo>/.agents/skills/ai-intake/` for one repository.
- Windsurf: `<repo>/.agents/skills/ai-intake/`.
- Cline: `<repo>/.cline/skills/ai-intake/`, `<repo>/.claude/skills/ai-intake/` or `~/.cline/skills/ai-intake/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r ai-intake.zip ai-intake
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `ai-intake.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r ai-intake.zip ai-intake
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
