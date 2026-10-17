# Review Older Issues

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they have no access to your repo, git or GitHub CLI.

Revalidates a bounded batch of open GitHub issues against current code, pull requests and related closed issues. Each issue gets one verdict: still valid, shipped, superseded or duplicate, needs rescoping, unwarranted, or unverified. The skill closes or rewrites issues only when the evidence supports it. It detects the repository's own labels, issue templates and branch conventions instead of assuming them, and needs the GitHub CLI (`gh`). Use on `/review-older-issues` or when asked to "review issues 1-100" or "clean up stale issues".

## When and how to use it

**Use it when**
- Your backlog has issues #1 to #100 and many may be shipped already.
- You plan a sprint and need to know which old issues still hold.
- A big merge landed on an integration branch and its issues stayed open.

**Try it**
```text
/review-older-issues 1-50
Review issues 12, 18 and 31 against the code and the pull requests.
```
You get one verdict per open issue (VALID, SHIPPED, SUPERSEDED, RESCOPE, UNWARRANTED or UNVERIFIED) with evidence. When called, the skill closes or rescopes issues on GitHub with a comment, even if you only asked a question, so start with a small batch. Other agents can ask in words.

**Skip it when**
- You want new issues written or code changed. This skill does neither.

## What it looks like

Example output, invented data. Each issue that was open when the batch started gets exactly one verdict, the evidence behind it, and the action taken:

```text
Selection: issues #1-#40, filtered to open at snapshot 2026-03-02 10:14 UTC
Checked revision: 4e1c9a2 (main). Skipped (already closed at snapshot): #3, #17

| Issue | Verdict      | Evidence                                   | Action                  | Result                  |
|-------|--------------|--------------------------------------------|-------------------------|-------------------------|
| #4    | SHIPPED      | PR #88 merged to main; src/auth/reset.ts:42 | Closed as completed     | Closed, comment read back |
| #9    | SUPERSEDED / DUPLICATE | Same gap as #61, which holds the decision  | Closed as not planned   | Closed, links #61       |
| #12   | RESCOPE      | Export shipped (PR #70); CSV import still missing | Body rewritten to the import work | Body read back |
| #21   | VALID        | Rate limit still absent in src/api/upload.ts | None                  | Unchanged               |
| #33   | UNWARRANTED  | Feature removed in PR #102; no remaining work | Closed as not planned | Closed, comment read back |
| #38   | UNVERIFIED   | Fix merged to integration branch; deploy unknown | None              | Unchanged               |

Counts: 1 SHIPPED · 1 SUPERSEDED / DUPLICATE · 1 RESCOPE · 1 VALID · 1 UNWARRANTED · 1 UNVERIFIED
Resume from: #41
```

A merged pull request is not proof the change shipped. When it cannot be confirmed, as with #38, the issue is left alone and marked `UNVERIFIED`.

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `saas-metrics`, `service-debugging`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:review-older-issues`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh review-older-issues   # into ~/.claude/skills/review-older-issues
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/review-older-issues/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex review-older-issues   # into ~/.agents/skills/review-older-issues
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/review-older-issues/` instead. Or copy this folder by hand to `~/.agents/skills/review-older-issues/`, or `.agents/skills/review-older-issues/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/review-older-issues/` for personal use (`scripts/install.sh --target codex review-older-issues` does this), or `<repo>/.agents/skills/review-older-issues/` for one repository.
- Windsurf: `<repo>/.agents/skills/review-older-issues/`.
- Cline: `<repo>/.cline/skills/review-older-issues/`, `<repo>/.claude/skills/review-older-issues/` or `~/.cline/skills/review-older-issues/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

The Claude app runs in a remote sandbox with no access to your repo, git or GitHub CLI.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

ChatGPT runs in a remote sandbox with no access to your repo, git or GitHub CLI.

Use Claude Code or Codex on your computer instead.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
