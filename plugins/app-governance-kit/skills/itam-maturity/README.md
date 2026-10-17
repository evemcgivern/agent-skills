# Itam Maturity

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09. Use for a baseline assessment or a yearly re-check.

## What it looks like

Example output on the stated scores in the kit's fictional demo estate (1 ad hoc, 5 improving):

````text
Area                                  Score
Governance and policy                   3
Inventory and discovery                 3
Entitlement and license management      1   gap
Lifecycle, request to retirement        2   gap
Vendor and contract management          4
Data quality and reconciliation         1   gap
Risk and security integration           3
Cost and financial management           4
Reporting and improvement               3
Unverified: scores are as stated; no evidence was supplied to support them.

Gaps: entitlement (XW-006, XW-007, XW-008), data quality (XW-026),
lifecycle (XW-009, XW-010). Entitlement and data quality tie at 1;
entitlement goes first because license gaps carry audit exposure.

90-day plan, entitlement
Owner role: software asset manager
Actions: match purchase records to installs for the top ten products;
record an expiry date for every license; review renewals monthly.
Evidence: an entitlement position report for those ten products.
Decision needed: owners and budget.

```findings
[{"type": "maturity_gap", "id": "entitlement"},
 {"type": "maturity_gap", "id": "data-quality"},
 {"type": "maturity_gap", "id": "lifecycle"}]
```
````

Score the same answers yourself in [practicum exercise 2](https://evemcgivern.github.io/app-governance-kit/practicum.html#itam-maturity).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:itam-maturity`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh itam-maturity   # into ~/.claude/skills/itam-maturity
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/itam-maturity/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex itam-maturity   # into ~/.agents/skills/itam-maturity
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/itam-maturity/` instead. Or copy this folder by hand to `~/.agents/skills/itam-maturity/`, or `.agents/skills/itam-maturity/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/itam-maturity/` for personal use (`scripts/install.sh --target codex itam-maturity` does this), or `<repo>/.agents/skills/itam-maturity/` for one repository.
- Windsurf: `<repo>/.agents/skills/itam-maturity/`.
- Cline: `<repo>/.cline/skills/itam-maturity/`, `<repo>/.claude/skills/itam-maturity/` or `~/.cline/skills/itam-maturity/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r itam-maturity.zip itam-maturity
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `itam-maturity.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r itam-maturity.zip itam-maturity
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
