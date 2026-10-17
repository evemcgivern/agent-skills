# RoleReady Application

![Version](https://img.shields.io/badge/version-0.2.0-blue) ![Claude Code CLI](https://img.shields.io/badge/Claude%20Code%20CLI-supported-6B4FBB) ![Claude Code Desktop](https://img.shields.io/badge/Claude%20Code%20Desktop-supported-6B4FBB) ![Codex](https://img.shields.io/badge/Codex-supported-111111) ![ChatGPT](https://img.shields.io/badge/ChatGPT-skill%20upload-74AA9C) ![License](https://img.shields.io/badge/license-MIT-green)

Build truthful role-tailored resumes, offer a cover letter after each resume build, and review writing while preserving the candidate’s own voice.

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

Skills in ChatGPT are available on Business, Enterprise, Healthcare and Edu plans. Zip the folder as above and upload it under **Plugins → Skills → Create → Upload from your computer**; an admin must enable skill uploading, and ChatGPT may mark an upload Needs Review or Blocked.

If you cannot upload skills, open a new chat or project and paste the contents of [`COPY-PASTE.txt`](skills/role-ready-application/COPY-PASTE.txt) as the instructions, then attach your resume and the job description. It is the same workflow as a single plain-text file.
</details>

<details>
<summary><b>Any other assistant</b></summary>

Paste [`COPY-PASTE.txt`](skills/role-ready-application/COPY-PASTE.txt) at the start of a chat, then attach your resume and the job description.
</details>

The skill works only with what you give it in the conversation. It does not need access to email, contacts or connected accounts.


## Included

The plugin installs one skill: `role-ready-application`, with reference guides for writing review, resume formatting, and role-specific filenames.

See the package-specific skill folders for exact file lists, versions, and changelogs.
