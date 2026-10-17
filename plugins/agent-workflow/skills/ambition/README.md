# Ambition

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Reconsiders a project or shelved idea against what tools and models can do now. It proposes three different, grounded outcomes, separates observed facts from assumptions, recommends one, and designs the smallest experiment that would settle its hardest uncertainty. It is advisory: it never starts work, spends money, or expands an assignment on its own. It can hand a chosen outcome to the mission skill, if installed.

## When and how to use it

**Use it when**
- You shelved an idea a year ago and wonder if it is easier now.
- A project feels small and you want options for something bigger.
- You must choose where to spend the next month and want a test before you commit.

**Try it**

```text
Revisit the offline sync idea we shelved for the notes app. Is it worth trying now?
Think bigger about my recipe app. What outcomes are worth a test?
```

A short context note, a table of three options, one recommendation, and a small experiment with a pass or fail rule and a cost ceiling. The agent does not run the experiment until you say go.

**Skip it when**
- The work is already approved and you want it built. Ask for the build directly.

## What it looks like

Example output, invented data, shortened. The reply is a short context, an options table, the experiment for the recommended option, and the decision left to you.

Context: offline editing was shelved because merging edits needed a server rewrite (observed: `docs/roadmap.md`).

| # | Outcome, who benefits | Constraint challenged | Hardest uncertainty | Effort, downside |
|---|---|---|---|---|
| 1 | Offline editing for field staff | Merging needed a server rewrite (observed) | Whether a client-side merge handles the note format (untested capability) | Weeks (estimate); risk of lost edits |
| 2 | Read-only offline cache | None; feasible today | Whether users need to edit offline (assumed) | Days (estimate); small upside |
| 3 | Leave the scope alone | - | - | None |

Recommended: 1. Option 2 is cheaper but skips what field staff asked for.

```text
1. Hypothesis: a client-side merge keeps every edit in recorded conflicts.
2. Smallest artifact: a script that merges 50 recorded edit pairs.
3. Procedure: the script does not exist yet, so writing it is the work.
   Baseline: the current server merge on the same 50 pairs.
4. Pass/fail: zero lost edits passes; any silent loss fails.
5. Resources: proposed ceiling of one day, no spend; needs the edit samples.
6. Next decision: pass, plan option 1; fail, offer option 2;
   inconclusive, widen the sample.

Decision needed: run the experiment, yes or no?
```

Nothing starts until you answer: the skill only advises.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
```

This installs the whole `agent-workflow` plugin, so you also get its other skills: `agent-doctor`, `check-worth`, `efficient-frontier-routing`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `quick-recap`, `sonnet-prompt-improver`, `stay-within-limits`, `up-to-speed`. Run it as `/agent-workflow:ambition`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install agent-workflow@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update agent-workflow@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh ambition   # into ~/.claude/skills/ambition
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **agent-workflow** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/ambition/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex ambition   # into ~/.agents/skills/ambition
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/ambition/` instead. Or copy this folder by hand to `~/.agents/skills/ambition/`, or `.agents/skills/ambition/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/ambition/` for personal use (`scripts/install.sh --target codex ambition` does this), or `<repo>/.agents/skills/ambition/` for one repository.
- Windsurf: `<repo>/.agents/skills/ambition/`.
- Cline: `<repo>/.cline/skills/ambition/`, `<repo>/.claude/skills/ambition/` or `~/.cline/skills/ambition/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b></summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r ambition.zip ambition
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `ambition.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

</details>

<details>
<summary><b>ChatGPT</b></summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/agent-workflow/skills && zip -r ambition.zip ambition
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
