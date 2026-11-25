# Recruiter Screen

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Read a finished resume against one job posting the way a recruiter, and then a hiring manager, would.

## When and how to use it

**Use it when**
- `role-ready-application` has built a resume and you want a second read against the posting.
- You want to know what survives a ten-second skim and what a hiring manager would test.
- You want to catch claims the resume makes that your source resume does not support.

**Try it**

```text
Read this resume against this posting as a recruiter and then a hiring manager. Resume: [paste]. Source resume: [paste]. Job description: [paste].
```

You get two separate verdicts: keep or reject for the recruiter pass, and strong, maybe or weak for the hiring-manager pass. You also get a check for unsupported claims, the interview questions the resume invites, and up to five things to fix first.

**Skip it when**
- You want a hiring prediction, odds or an applicant-tracking score. This is a language model's simulated read and gives none.
- You want the resume rewritten. Use `role-ready-application` for that.
- You want to decide whether to apply at all. Use `posting-fit-check`.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install role-ready-application@evemcgivern-skills
```

This installs the whole `role-ready-application` plugin, so you also get its other skills: `interview-prep`, `posting-fit-check`, `role-ready-application`. Run it as `/role-ready-application:recruiter-screen`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install role-ready-application@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update role-ready-application@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh recruiter-screen   # into ~/.claude/skills/recruiter-screen
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **role-ready-application** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/recruiter-screen/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex recruiter-screen   # into ~/.agents/skills/recruiter-screen
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/recruiter-screen/` instead. Or copy this folder by hand to `~/.agents/skills/recruiter-screen/`, or `.agents/skills/recruiter-screen/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/recruiter-screen/` for personal use (`scripts/install.sh --target codex recruiter-screen` does this), or `<repo>/.agents/skills/recruiter-screen/` for one repository.
- Windsurf: `<repo>/.agents/skills/recruiter-screen/`.
- Cline: `<repo>/.cline/skills/recruiter-screen/`, `<repo>/.claude/skills/recruiter-screen/` or `~/.cline/skills/recruiter-screen/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/role-ready-application/skills && zip -r recruiter-screen.zip recruiter-screen
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `recruiter-screen.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/role-ready-application/skills && zip -r recruiter-screen.zip recruiter-screen
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

<!-- install:end -->

## Included

- `SKILL.md`
- `references/candidate-rules.md`
- `VERSION` and `CHANGELOG.md`
