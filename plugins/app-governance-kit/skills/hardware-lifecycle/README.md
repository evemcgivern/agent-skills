# Hardware Lifecycle

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Check a device fleet for hardware overdue for refresh and retired devices missing a confirmed data wipe, estimate replacement cost, and produce a disposal-readiness summary. Use for a refresh cycle review, before a hardware budget request, or before closing out a disposal.

## What it looks like

Example output on the kit's fictional demo estate (60 devices, checked 2026-09-01):

````text
Devices needing action
Device   Type     Status   Issue                                 Recommendation
DEV-008  server   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-027  mobile   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-045  laptop   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-011  mobile   retired  Retired 2023-02-19, wipe not confirmed  Wipe or certified destruction
DEV-042  desktop  retired  Retired 2025-01-09, wipe not confirmed  Wipe or certified destruction

Refresh cost: 3 devices, from 10,240 USD at original purchase cost.
Unverified: current replacement prices, which set the top of the range.
Decision needed: the asset owner picks replace, upgrade or extend.

Blocking disposal: DEV-011, DEV-042. Neither can be marked disposed
until wipe evidence is attached.
Decision needed: confirmation from whoever is accountable for disposal.

```findings
[{"type": "overdue_refresh", "id": "DEV-008"},
 {"type": "overdue_refresh", "id": "DEV-027"},
 {"type": "overdue_refresh", "id": "DEV-045"},
 {"type": "unwiped_retired_device", "id": "DEV-011"},
 {"type": "unwiped_retired_device", "id": "DEV-042"}]
```
````

Work the same fleet yourself in [practicum exercise 7](https://evemcgivern.github.io/app-governance-kit/practicum.html#hardware-lifecycle).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:hardware-lifecycle`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh hardware-lifecycle   # into ~/.claude/skills/hardware-lifecycle
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/hardware-lifecycle/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex hardware-lifecycle   # into ~/.agents/skills/hardware-lifecycle
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/hardware-lifecycle/` instead. Or copy this folder by hand to `~/.agents/skills/hardware-lifecycle/`, or `.agents/skills/hardware-lifecycle/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/hardware-lifecycle/` for personal use (`scripts/install.sh --target codex hardware-lifecycle` does this), or `<repo>/.agents/skills/hardware-lifecycle/` for one repository.
- Windsurf: `<repo>/.agents/skills/hardware-lifecycle/`.
- Cline: `<repo>/.cline/skills/hardware-lifecycle/`, `<repo>/.claude/skills/hardware-lifecycle/` or `~/.cline/skills/hardware-lifecycle/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r hardware-lifecycle.zip hardware-lifecycle
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `hardware-lifecycle.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r hardware-lifecycle.zip hardware-lifecycle
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
