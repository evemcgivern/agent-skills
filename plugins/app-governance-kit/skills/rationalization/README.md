# Rationalization

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk. Use for portfolio reviews, budget cycles, or post-merger cleanup.

## What it looks like

Example output on the kit's fictional demo estate (60 apps, licenses checked 2026-09-01). The per-app TIME table and data disposition are left out here:

````text
Duplicates (same category)               Keep     Why
APP-008 + APP-041  Contract management   APP-041  more users, lower cost
APP-014 + APP-052  E-signature           APP-014  more users, lower cost
APP-022 + APP-037  Endpoint management   open     022 has 345 more users;
                                                  037 costs 61,200 USD less
APP-029 + APP-058  Transport management  APP-058  more users, lower cost
APP-033 + APP-046  Customs brokerage     APP-046  more users, lower cost
Decision needed: final keep or retire calls.

Licenses
LIC-044  APP-044  expired 2025-12-31  97 entitlements for 748 users
LIC-017  APP-017  expired 2026-03-31  246 entitlements for 649 users
Far above users: 7 licenses, for example LIC-025 (350 for 45 users)

Potential savings: 294,200 to 355,400 USD a year from retiring one app
in each pair, depending on the endpoint call. A range, not a promise.

```findings
[{"type": "duplicate_app", "id": "APP-008+APP-041"},
 {"type": "duplicate_app", "id": "APP-014+APP-052"},
 {"type": "duplicate_app", "id": "APP-022+APP-037"},
 {"type": "duplicate_app", "id": "APP-029+APP-058"},
 {"type": "duplicate_app", "id": "APP-033+APP-046"},
 {"type": "expired_license", "id": "LIC-044"},
 {"type": "expired_license", "id": "LIC-017"}]
```
````

Run the same portfolio review yourself in [practicum exercise 4](https://evemcgivern.github.io/app-governance-kit/practicum.html#rationalization).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `program-setup`. Run it as `/app-governance-kit:rationalization`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh rationalization   # into ~/.claude/skills/rationalization
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/rationalization/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex rationalization   # into ~/.agents/skills/rationalization
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/rationalization/` instead. Or copy this folder by hand to `~/.agents/skills/rationalization/`, or `.agents/skills/rationalization/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/rationalization/` for personal use (`scripts/install.sh --target codex rationalization` does this), or `<repo>/.agents/skills/rationalization/` for one repository.
- Windsurf: `<repo>/.agents/skills/rationalization/`.
- Cline: `<repo>/.cline/skills/rationalization/`, `<repo>/.claude/skills/rationalization/` or `~/.cline/skills/rationalization/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r rationalization.zip rationalization
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `rationalization.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r rationalization.zip rationalization
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
- `template.csv`
- `themes.md`
- `agents/openai.yaml` for ChatGPT/Codex skill-card metadata.
- `VERSION` and `CHANGELOG.md` for this package snapshot.

Source: [https://github.com/evemcgivern/app-governance-kit](https://github.com/evemcgivern/app-governance-kit).
