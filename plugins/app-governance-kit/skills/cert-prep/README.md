# Cert Prep

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Coach a learner preparing for CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation, or the IAM Certificate with scenario drills on the Halden demo estate, then log gaps and plan the next drills. Use for weekly study sessions or a readiness check. Not exam content and not a pass guarantee.

## When and how to use it

**Use it when**
- You prepare for CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation or the IAM Certificate.
- You want a weekly study session with short scenario drills.
- You want a readiness check and a list of weak areas.

**Try it**
```text
Coach me for CSAM. I have five hours a week and an exam in eight weeks.
Run a drill on tiering an AI use case, then rate my answer.
```
You get scenario drills on the Halden demo estate, a rating of strong, partial or gap for each answer, a ranked gap list and a next-drill plan.

**Skip it when**
- You want real exam questions or a pass prediction. This skill gives neither. Use the certification body's own outline and training.

## What it looks like

One drill from a study session. The learner's answers are invented; the device data comes from the kit's fictional demo estate.

````text
Learner: CHAMP. Two years in IT support, 3 hours a week, no exam date.
Coach:   Drill 1: retire hardware with data-wipe evidence. Attach devices.csv.
         Ten devices are marked retired and finance wants the disposal
         closed this week. What do you check first?
Learner: That every retired device has a retirement date.
Coach:   Partial. All ten have dates, but DEV-011 and DEV-042 have no
         confirmed wipe, so the disposal cannot close yet. Wipe or
         destruction evidence comes first (XW-010, retirement and
         decommissioning). Logged as a gap; next drill: practicum 07.
...      (two to four more drills on different tasks)
Coach:   Gaps, most important first: disposal evidence, ...
         This is practice, not a prediction of your exam result.
         Decision needed: which gap to work first, and whether to book.

```findings
[{"type": "knowledge_gap", "id": "disposal-evidence"}]
```
````

The [field guide](https://evemcgivern.github.io/app-governance-kit/field-guide.html#cert-heading) compares the six certifications, and the [practicum](https://evemcgivern.github.io/app-governance-kit/practicum.html) holds the matching exercises.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:cert-prep`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh cert-prep   # into ~/.claude/skills/cert-prep
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/cert-prep/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex cert-prep   # into ~/.agents/skills/cert-prep
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/cert-prep/` instead. Or copy this folder by hand to `~/.agents/skills/cert-prep/`, or `.agents/skills/cert-prep/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/cert-prep/` for personal use (`scripts/install.sh --target codex cert-prep` does this), or `<repo>/.agents/skills/cert-prep/` for one repository.
- Windsurf: `<repo>/.agents/skills/cert-prep/`.
- Cline: `<repo>/.cline/skills/cert-prep/`, `<repo>/.claude/skills/cert-prep/` or `~/.cline/skills/cert-prep/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r cert-prep.zip cert-prep
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `cert-prep.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/app-governance-kit/skills && zip -r cert-prep.zip cert-prep
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

Drills use the kit's fictional Halden demo estate. A single-skill install or upload does not include it: download the files from [`demo-estate/`](https://github.com/evemcgivern/agent-skills/tree/main/plugins/app-governance-kit/demo-estate) and attach them to the session.

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
