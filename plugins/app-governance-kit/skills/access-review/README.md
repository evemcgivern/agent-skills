# Access Review

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05. Use for quarterly or annual access reviews.

## When and how to use it

**Use it when**
- Your quarterly access review is due and you have an account export and an HR list.
- A person left in May and you need to know if their accounts still exist.
- An auditor asks for a memo on who can reach the finance apps.

**Try it**
```text
Review this account export against the HR list. Flag orphaned, dormant and privileged accounts.
Write the auditor memo for the Q3 access review of the finance apps.
```
You get an exceptions table, an evidence summary and a one-page auditor memo. Dormant means no login in 90 days. Each removal is marked **Decision needed** for the application owner.

**Skip it when**
- You want accounts removed. This skill lists exceptions. The application owner decides each removal.

## What it looks like

Example output on the kit's fictional demo estate (120 accounts, 80 HR records, export checked 2026-09-01). Accounts on confidential applications come first:

````text
Exceptions
Account  Person   App      Issue                                  Action
ACC-063  EMP-072  APP-003  Left 2026-07-02, logged in 2026-08-08  Remove
ACC-104  EMP-099  APP-044  No matching person in the HR list      Investigate
ACC-019  EMP-071  APP-019  Left 2026-05-15, logged in 2026-08-20  Remove
7 admin accounts: ACC-017, 034, 051, 068, 085, 102, 119           Re-approve
Dormant (no login in 90 days): none
Segregation of duties: not checked, no role rules supplied

Decision needed: each removal, by the application owner.
Clauses: XW-016 periodic review, XW-017 leaver removal,
XW-018 privileged access.

```findings
[{"type": "orphaned_account", "id": "ACC-063"},
 {"type": "orphaned_account", "id": "ACC-104"},
 {"type": "orphaned_account", "id": "ACC-019"}]
```
````

A full run also writes the evidence summary and a one-page auditor memo. Try the same review yourself in [practicum exercise 5](https://evemcgivern.github.io/app-governance-kit/practicum.html#access-review).

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:access-review`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh access-review   # into ~/.claude/skills/access-review
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/access-review/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex access-review   # into ~/.agents/skills/access-review
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/access-review/` instead. Or copy this folder by hand to `~/.agents/skills/access-review/`, or `.agents/skills/access-review/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/access-review/` for personal use (`scripts/install.sh --target codex access-review` does this), or `<repo>/.agents/skills/access-review/` for one repository.
- Windsurf: `<repo>/.agents/skills/access-review/`.
- Cline: `<repo>/.cline/skills/access-review/`, `<repo>/.claude/skills/access-review/` or `~/.cline/skills/access-review/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r access-review.zip access-review
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `access-review.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r access-review.zip access-review
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
