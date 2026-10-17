# SaaS Metrics

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it works from exports you upload; live Stripe and PostHog queries depend on network access that is not guaranteed.

Computes and reports MRR, revenue and logo churn, activation, and retention for a small SaaS product from Stripe and PostHog data. It gives simple metric definitions a small team can re-derive every month, a starter Stripe MRR script and HogQL queries, a monthly business-review template, and a list of common miscounts such as trials, refunds, currency mixing, proration, and annual plans. Use it when asked for a business review, MRR or churn numbers, an activation rate, a retention cohort, or recurring metrics reporting.

## When and how to use it

**Use it when**
- You need MRR and churn for a monthly review and your numbers do not match the Stripe dashboard.
- You want one activation event defined and kept, not redefined each quarter.
- You are setting up a 30-day retention report from PostHog.

**Try it**
```text
Compute our MRR from Stripe and tell me what you excluded.
Set up a monthly business review: MRR, gross churn, 7-day activation and 30-day retention.
```
You get metric definitions, a starter Stripe script, PostHog HogQL queries and a review template, with warnings about trials, refunds, currency and proration.

**Skip it when**
- Your pricing is metered or multi-currency. The starter code assumes one currency and flat prices, so you must extend it.

## What it looks like

Example output, invented data. The monthly review follows the skill's template, with the month's distortions called out so the trend is not misread later:

```markdown
# Business Review — March 2026

## Revenue
- MRR: $18,420 (prior month: $17,150, change: 7.4%)
- Gross churn: 4.4% | Net churn: 2.2%
- New MRR added: $1,640 | Expansion MRR: $390 | Churned MRR: $760

## Product
- New signups: 312
- Activation rate (7-day): 41%
- 30-day retention: 27%

## Notable
- One annual plan renewed ($2,400), counted as $200 of MRR, not $2,400
- Two trials converted; they enter MRR this month, not before
- One refund ($49) backed out of March revenue

## Actions
- [ ] Reconcile Stripe and PostHog paying-customer counts (off by 3)
```

The common miscounts the skill checks for each month:

| Miscount | Correct handling |
|---|---|
| Trials counted as MRR | Leave out until the subscription is `active` |
| Annual plan at face value | Divide by 12 |
| Proration charge added to MRR | One-time revenue, not recurring |
| Cancel-at-period-end dropped early | Keep in MRR; flag as next month's committed churn |

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install engineering-practices@evemcgivern-skills
```

This installs the whole `engineering-practices` plugin, so you also get its other skills: `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `review-older-issues`, `service-debugging`, `spec-workflow`, `spec-workflow-drift`, `transactional-email`. Run it as `/engineering-practices:saas-metrics`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install engineering-practices@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update engineering-practices@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh saas-metrics   # into ~/.claude/skills/saas-metrics
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **engineering-practices** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/saas-metrics/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex saas-metrics   # into ~/.agents/skills/saas-metrics
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/saas-metrics/` instead. Or copy this folder by hand to `~/.agents/skills/saas-metrics/`, or `.agents/skills/saas-metrics/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/saas-metrics/` for personal use (`scripts/install.sh --target codex saas-metrics` does this), or `<repo>/.agents/skills/saas-metrics/` for one repository.
- Windsurf: `<repo>/.agents/skills/saas-metrics/`.
- Cline: `<repo>/.cline/skills/saas-metrics/`, `<repo>/.claude/skills/saas-metrics/` or `~/.cline/skills/saas-metrics/`.

</details>

<details>
<summary><b>Claude app (claude.ai)</b> — works with a limit</summary>

1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r saas-metrics.zip saas-metrics
   ```
2. Turn on code execution under **Settings → Capabilities**.
3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `saas-metrics.zip`.

On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.

**Limit:** The Claude app works from exports you upload; live Stripe and PostHog queries are not guaranteed, because its network is limited to approved package sources and off for Team and Enterprise.

</details>

<details>
<summary><b>ChatGPT</b> — works with a limit</summary>

1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.
2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):
   ```bash
   cd plugins/engineering-practices/skills && zip -r saas-metrics.zip saas-metrics
   ```
3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.

The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.

**Limit:** ChatGPT works from exports you upload; live Stripe and PostHog queries are not guaranteed, because network access depends on the workspace settings.

</details>

<!-- install:end -->

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
