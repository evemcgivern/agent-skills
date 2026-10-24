# Interview Prep

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Prepare for an interview from the posting and the exact resume and cover letter you sent, using only your own confirmed examples.

## When and how to use it

**Use it when**
- You have an interview coming up and want likely questions tied to the posting and to what you sent.
- You want each answer built from something you really did, with honest answers for the gaps.
- You want to practise out loud, one question at a time, with feedback on each answer.

**Try it**

```text
I have a first-round interview for a Support Operations Analyst role at Example Co. Posting: [paste]. The resume and cover letter I sent: [paste both]. The interviewer is the hiring manager.
Prep me for a phone screen. Posting: [paste]. Resume I sent: [paste]. I did not send a cover letter. Run a mock interview after.
```

The agent asks for anything missing. It then gives up to eight likely questions, your own example for each laid out as situation, action and result, honest bridge answers for gaps, questions to ask the interviewer, company notes with sources (or a list of what to look up), and the facts it used. It then offers a mock interview.

**Skip it when**
- You want a prediction of the interview result. The skill gives no odds or scores.
- You want a thank-you note or follow-up drafted.
- You have not applied yet. Use `posting-fit-check` or `role-ready-application` first.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install role-ready-application@evemcgivern-skills
```

This installs the whole `role-ready-application` plugin, so you also get its other skills: `posting-fit-check`, `role-ready-application`. Run it as `/role-ready-application:interview-prep`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install role-ready-application@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update role-ready-application@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh interview-prep   # into ~/.claude/skills/interview-prep
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **role-ready-application** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/interview-prep/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex interview-prep   # into ~/.agents/skills/interview-prep
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/interview-prep/` instead. Or copy this folder by hand to `~/.agents/skills/interview-prep/`, or `.agents/skills/interview-prep/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/interview-prep/` for personal use (`scripts/install.sh --target codex interview-prep` does this), or `<repo>/.agents/skills/interview-prep/` for one repository.
- Windsurf: `<repo>/.agents/skills/interview-prep/`.
- Cline: `<repo>/.cline/skills/interview-prep/`, `<repo>/.claude/skills/interview-prep/` or `~/.cline/skills/interview-prep/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/role-ready-application/skills && zip -r interview-prep.zip interview-prep
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `interview-prep.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/role-ready-application/skills && zip -r interview-prep.zip interview-prep
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

<!-- install:end -->

## Included

- `SKILL.md`
- `references/candidate-rules.md`
- `VERSION` and `CHANGELOG.md`
