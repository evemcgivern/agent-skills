# RoleReady Application

![Version](https://img.shields.io/badge/version-0.2.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

Build truthful role-tailored resumes and cover letters, check whether a job posting is worth applying to, and prepare candidates for interviews, keeping to facts the candidate supplies.

## Install

Pick your platform. Each section opens with one click.

<details>
<summary><b>Claude Code (terminal)</b></summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install role-ready-application@evemcgivern-skills
```

Then start a session and ask, for example, "tailor my resume to this job" and paste the job description, or run `/role-ready-application:role-ready-application`.
</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, add the marketplace `evemcgivern/agent-skills`, then install **role-ready-application**. Desktop and the terminal share user-scope installs. Cloud sessions do not load local plugins.
</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex role-ready-application
```

This copies the skill to `~/.agents/skills/role-ready-application`. Start a new Codex session and ask for it by name. For one repository only, add `--project <repo-path>`.
</details>

<details>
<summary><b>Claude.ai and Claude Cowork</b></summary>

1. Zip the skill folder from a clone of the repo:
   ```bash
   cd plugins/role-ready-application/skills && zip -r role-ready-application.zip role-ready-application
   ```
2. In Claude, turn on code execution under **Settings → Capabilities**, then open **Customize → Skills → + → Create skill → Upload a skill** and upload `role-ready-application.zip`. On Enterprise, an owner must first enable skills under Organization settings.
3. Start a chat and attach your resume and the job description.

Local files in `~/.claude/skills/` do not sync to Claude.ai, so the upload step is needed.
</details>

<details>
<summary><b>ChatGPT</b></summary>

Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading. Zip the folder as above and upload it from the **Plugins → Skills** tab with **+ → Upload from your computer**. ChatGPT scans each upload and can mark it Needs Review or Blocked. The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth.

If you cannot upload skills, open a new chat or project and paste the contents of [`COPY-PASTE.txt`](skills/role-ready-application/COPY-PASTE.txt) as the instructions, then attach your resume and the job description. It is the same workflow as a single plain-text file.
</details>

<details>
<summary><b>Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and other skill-folder agents</b></summary>

Copy `skills/role-ready-application/` to `~/.agents/skills/role-ready-application/` (Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode) or to the folder your agent reads; `scripts/install.sh --target codex role-ready-application` does this. See [Install](../../README.md#install) in the repository README for Windsurf and Cline.
</details>

<details>
<summary><b>Any other assistant</b></summary>

Paste [`COPY-PASTE.txt`](skills/role-ready-application/COPY-PASTE.txt) at the start of a chat, then attach your resume and the job description.
</details>

The skills work only with what you give them in the conversation. They do not need access to email, contacts or connected accounts.


## Skills

| Skill | Use it to |
| --- | --- |
| [`role-ready-application`](skills/role-ready-application/README.md) | Tailor a resume and cover letter to one job, then review the writing |
| [`posting-fit-check`](skills/posting-fit-check/README.md) | Decide whether a posting is worth applying to |
| [`interview-prep`](skills/interview-prep/README.md) | Prepare for an interview |

The candidate pack is a plain text file you own, holding your confirmed facts and stated deal-breakers. A skill uses it only when you name or paste it. Keep it on your own device, never in this repository. See [`shared/candidate-rules.md`](shared/candidate-rules.md) for the layout. The same rules file is copied into each skill, so each works when installed alone.

## Included

The plugin installs three skills: `role-ready-application`, `posting-fit-check` and `interview-prep`, each carrying the shared candidate rules in its references folder.

See the package-specific skill folders for exact file lists, versions, and changelogs.
