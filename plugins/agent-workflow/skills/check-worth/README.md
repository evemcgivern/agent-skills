# Check Worth

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it reads the source but cannot check it against your repo or GitHub issues.

Reviews an external PDF, image, screenshot, article, or URL against a repository's open and closed issues and its code, and sorts each idea into already tracked, shipped, superseded, a candidate new issue, or not actionable, with `file:line` evidence and `UNABLE TO VERIFY` where the source falls short. Read-only unless you authorize issue creation or code changes. Use on "/check-worth" or when asking whether an external idea is worth pulling into a repository.

## When and how to use it

**Use it when**
- A colleague sends a PDF of ideas and you want to know what your repo already covers.
- You see an article about retry budgets and wonder if it is worth an issue.
- A screenshot shows a feature in another product and you want to know if your code has it.

**Try it**

```text
/check-worth ./vendor-report.pdf
Is the idea in https://example.com/blog/retry-budgets worth an issue in this repo?
```

A table with each takeaway, its status in your repo (new, tracked, shipped, contradicted or unverifiable), the evidence and a recommendation. The review is read-only. It files an issue only if you say so. Other agents can ask in words.

**Skip it when**
- You already know you want the change. Write the issue or the code directly.

## What it looks like

Example output, invented data. The reply leads with the conclusion, then one row per idea from the source:

```text
One idea is worth a new issue. Two are already covered, and one could not be checked.

| Source takeaway             | Repository status       | Evidence                         | Recommendation       |
|-----------------------------|-------------------------|----------------------------------|----------------------|
| Cache prompt prefixes       | Shipped                 | src/llm/client.ts:88             | None                 |
| Retry with backoff on 429   | Already tracked         | #57 (open), src/llm/retry.ts:12  | Comment on #57       |
| Log token cost per request  | Candidate new issue     | No match in issues or code       | Draft below          |
| "Cuts latency by 40%"       | UNABLE TO VERIFY        | Source gives no benchmark setup  | Do not act on it     |

Source limitations: PDF pages 1-12 read; page 13 is an image with no legible text.
```

After the table come the existing issue and code matches, the draft for the new issue (title, scope, non-goals, acceptance criteria), and deferred follow-ups. Nothing is filed or changed until you say so.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `ambition`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:check-worth`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh check-worth   # into ~/.claude/skills/check-worth
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/check-worth/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex check-worth   # into ~/.agents/skills/check-worth
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/check-worth/` instead. Or copy this folder by hand to `~/.agents/skills/check-worth/`, or `.agents/skills/check-worth/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/check-worth/` for personal use (`scripts/install.sh --target codex check-worth` does this), or `<repo>/.agents/skills/check-worth/` for one repository.
- Windsurf: `<repo>/.agents/skills/check-worth/`.
- Cline: `<repo>/.cline/skills/check-worth/`, `<repo>/.claude/skills/check-worth/` or `~/.cline/skills/check-worth/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r check-worth.zip check-worth
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `check-worth.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** The Claude app can read the source but cannot check it against your repo or GitHub issues.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r check-worth.zip check-worth
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** ChatGPT can read the source but cannot check it against your repo or GitHub issues.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
