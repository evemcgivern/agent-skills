# LLM Engineer

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it designs the experiment but cannot inspect your local runtime.

Diagnoses language-model behavior across the model, its serving runtime, the prompt and context, and the application driving it. It separates task, harness, runtime, agent-policy and model-output failures, then turns the observed failure into one bounded, falsifiable experiment with controls and an explicit budget. Use when asked to "evaluate a local language model", "debug tool calling", "diagnose an agent that keeps exploring", "compare LLM runtimes", or "design an LLM experiment".

## What it looks like

The first thing the skill does with a failure is place it in one of five layers, because the fix for each is different. More than one layer can contribute, and the report keeps the proven cause apart from the plausible ones:

| Layer | What failed | Examples |
|---|---|---|
| Task or evidence | The job itself | Missing requirements, an invalid test oracle, stale source, a task that cannot be done offline |
| Harness | The measurement | Incomplete capture, wrong deadlines, grading errors, unequal comparison conditions |
| Runtime or protocol | The serving path | Model loading, chat-template mismatch, streaming framing, tool-call parsing, failed cancellation |
| Agent policy | The application's choices | Repeated exploration, assuming an unavailable tool, discarding evidence, finishing too early |
| Model output | The model | A wrong or thin answer when the harness, configuration and evidence are all sound |

Malformed JSON from a quantized model is not blamed on quantization until the template, parser, runtime and sampling settings have been ruled out.

The answer then comes back in the skill's own wording, which says exactly how far the evidence goes:

> "Offline regression passed" means the policy mechanics work with scripted responses. "Candidate had no patch at cutoff" means the run was interrupted. "Verified task completed" is used only when the task's independent criteria passed.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `review-older-issues`, `saas-metrics`, `service-debugging`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:llm-engineer`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh llm-engineer   # into ~/.claude/skills/llm-engineer
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/llm-engineer/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex llm-engineer   # into ~/.agents/skills/llm-engineer
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/llm-engineer/` instead. Or copy this folder by hand to `~/.agents/skills/llm-engineer/`, or `.agents/skills/llm-engineer/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/llm-engineer/` for personal use (`scripts/install.sh --target codex llm-engineer` does this), or `<repo>/.agents/skills/llm-engineer/` for one repository.
- Windsurf: `<repo>/.agents/skills/llm-engineer/`.
- Cline: `<repo>/.cline/skills/llm-engineer/`, `<repo>/.claude/skills/llm-engineer/` or `~/.cline/skills/llm-engineer/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r llm-engineer.zip llm-engineer
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `llm-engineer.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** The Claude app can design the experiment but cannot inspect your local runtime.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r llm-engineer.zip llm-engineer
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** ChatGPT can design the experiment but cannot inspect your local runtime.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `references/runtime-diagnosis.md` — diagnosing loading, protocol, latency, memory and stopping failures.
- `references/evaluation-design.md` — freezing a claim, qualifying the harness, and grading results.
- `examples/experiment-packet.md` — an experiment template with a synthetic worked example.
- `VERSION` and `CHANGELOG.md` — package version history.
