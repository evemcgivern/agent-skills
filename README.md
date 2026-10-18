# Eve McGivern's Agent Skills

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-37-blue.svg)](#skills)

Skills for Claude Code, Codex and other agents that read `SKILL.md` folders (Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and more), packaged as a Claude Code plugin marketplace. Each skill is a folder with a `SKILL.md`. [Compatibility](#compatibility) shows where each skill works; under [Install](#install), pick your tool and one click opens the steps.

## Compatibility

Every skill README shows three badges, one per group of hosts. The first two split into the agent that runs on your computer and the chat app:

| Host | What it is |
|---|---|
| Claude Code | Claude Code (CLI, desktop and IDE extensions), running on your computer |
| Claude app | The Claude app (claude.ai) with an uploaded skill |
| Codex | Codex (CLI, IDE extension and app), running on your computer |
| ChatGPT | Skills uploaded to ChatGPT |
| Other agents | Local agents that read `SKILL.md` folders: Gemini CLI and Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline and others |

**app** means a chat app: the Claude app and ChatGPT run skills in a remote sandbox with no access to your local files, repo or local shell (ChatGPT network access depends on the workspace settings and is not guaranteed). A skill that needs a local shell, repo, git or the GitHub CLI, session logs, local processes or a local MCP server does not work there.

**✔ full** works as written. **◐ partial** works with a limit, stated in one line under the badges. **✖ no** does not work on that host. A badge's colour follows the local agent (Claude Code or Codex): green for full, yellow for partial, grey for no.

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode and Windsurf; Claude Code reads `.claude/skills` instead, and Cline reads `.cline/skills` or `.claude/skills`. Antigravity CLI replaced Gemini CLI for unpaid and Google One users on 2026-06-18.

<details>
<summary><b>All 37 skills</b> (✔ full, ◐ partial, ✖ no)</summary>

| Skill | Plugin | Claude Code | Claude app | Codex | ChatGPT | Other agents |
|---|---|:-:|:-:|:-:|:-:|:-:|
| [`agent-doctor`](plugins/agent-workflow/skills/agent-doctor/README.md) | agent-workflow | ✔ | ✖ | ✔ | ✖ | ◐ |
| [`ambition`](plugins/agent-workflow/skills/ambition/README.md) | agent-workflow | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`check-worth`](plugins/agent-workflow/skills/check-worth/README.md) | agent-workflow | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`efficient-frontier-routing`](plugins/agent-workflow/skills/efficient-frontier-routing/README.md) | agent-workflow | ✔ | ✖ | ✔ | ✖ | ◐ |
| [`fable-chief-agent`](plugins/agent-workflow/skills/fable-chief-agent/README.md) | agent-workflow | ✔ | ✖ | ✔ | ✖ | ◐ |
| [`goal-checklist`](plugins/agent-workflow/skills/goal-checklist/README.md) | agent-workflow | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`handoff`](plugins/agent-workflow/skills/handoff/README.md) | agent-workflow | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`mission`](plugins/agent-workflow/skills/mission/README.md) | agent-workflow | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`orchestrator`](plugins/agent-workflow/skills/orchestrator/README.md) | agent-workflow | ✔ | ✖ | ◐ | ✖ | ◐ |
| [`problem-first`](plugins/agent-workflow/skills/problem-first/README.md) | agent-workflow | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`quick-recap`](plugins/agent-workflow/skills/quick-recap/README.md) | agent-workflow | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`sonnet-prompt-improver`](plugins/agent-workflow/skills/sonnet-prompt-improver/README.md) | agent-workflow | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`stay-within-limits`](plugins/agent-workflow/skills/stay-within-limits/README.md) | agent-workflow | ✔ | ✖ | ◐ | ✖ | ◐ |
| [`up-to-speed`](plugins/agent-workflow/skills/up-to-speed/README.md) | agent-workflow | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`access-review`](plugins/app-governance-kit/skills/access-review/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`ai-intake`](plugins/app-governance-kit/skills/ai-intake/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`app-governance`](plugins/app-governance-kit/skills/app-governance/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ◐ | ✔ |
| [`cert-prep`](plugins/app-governance-kit/skills/cert-prep/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`crosswalk`](plugins/app-governance-kit/skills/crosswalk/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`hardware-lifecycle`](plugins/app-governance-kit/skills/hardware-lifecycle/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`itam-maturity`](plugins/app-governance-kit/skills/itam-maturity/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`program-setup`](plugins/app-governance-kit/skills/program-setup/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`rationalization`](plugins/app-governance-kit/skills/rationalization/README.md) | app-governance-kit | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`audit-background-processes`](plugins/engineering-practices/skills/audit-background-processes/README.md) | engineering-practices | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`background-jobs`](plugins/engineering-practices/skills/background-jobs/README.md) | engineering-practices | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`launch-chrome-debug`](plugins/engineering-practices/skills/launch-chrome-debug/README.md) | engineering-practices | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`llm-engineer`](plugins/engineering-practices/skills/llm-engineer/README.md) | engineering-practices | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`review-older-issues`](plugins/engineering-practices/skills/review-older-issues/README.md) | engineering-practices | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`saas-metrics`](plugins/engineering-practices/skills/saas-metrics/README.md) | engineering-practices | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`service-debugging`](plugins/engineering-practices/skills/service-debugging/README.md) | engineering-practices | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`spec-workflow`](plugins/engineering-practices/skills/spec-workflow/README.md) | engineering-practices | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`spec-workflow-drift`](plugins/engineering-practices/skills/spec-workflow-drift/README.md) | engineering-practices | ✔ | ✖ | ✔ | ✖ | ✔ |
| [`transactional-email`](plugins/engineering-practices/skills/transactional-email/README.md) | engineering-practices | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`role-ready-application`](plugins/role-ready-application/skills/role-ready-application/README.md) | role-ready-application | ✔ | ✔ | ✔ | ✔ | ✔ |
| [`clearly`](plugins/writing/skills/clearly/README.md) | writing | ✔ | ◐ | ✔ | ◐ | ✔ |
| [`scrub-ai-tells`](plugins/writing/skills/scrub-ai-tells/README.md) | writing | ✔ | ✔ | ✔ | ◐ | ✔ |
| [`table`](plugins/writing/skills/table/README.md) | writing | ✔ | ✔ | ✔ | ✔ | ✔ |
</details>

The note behind each mark is in [`compatibility.json`](compatibility.json) (checked 2026-10-17).

## Install

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install agent-workflow@evemcgivern-skills
claude plugin install writing@evemcgivern-skills
claude plugin install role-ready-application@evemcgivern-skills
claude plugin install app-governance-kit@evemcgivern-skills
claude plugin install engineering-practices@evemcgivern-skills
```

Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install <plugin>@evemcgivern-skills`. Skills then appear as `/<plugin>:<skill>`, for example `/writing:clearly`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update <plugin>@evemcgivern-skills` for each installed plugin.
</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install the plugins you want. Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit the skill folders to your repository's `.claude/skills/` instead.
</details>

<details>
<summary><b>Claude Code, Codex or other agents — copy single skills</b></summary>

From a clone of this repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --list                          # see skill names
scripts/install.sh clearly table                   # Claude Code, into ~/.claude/skills
scripts/install.sh --target codex --all            # Codex, into ~/.agents/skills
scripts/install.sh --project ~/code/myapp clearly  # one repository only
```

Add `--force` to replace a skill you already have. Or copy a folder by hand from `plugins/<plugin>/skills/<skill>/` to `~/.claude/skills/<skill>/` (Claude Code) or `~/.agents/skills/<skill>/` (Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode). Keep every file in the folder together. `--target codex` writes to `~/.agents/skills`, so it also works for those agents.
</details>

<details>
<summary><b>Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy the whole skill folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/<skill>/` for personal use (`scripts/install.sh --target codex <skill>`), or `<repo>/.agents/skills/<skill>/` for one repository.
- Windsurf: `<repo>/.agents/skills/<skill>/`.
- Cline: `<repo>/.cline/skills/<skill>/`, `<repo>/.claude/skills/<skill>/` or `~/.cline/skills/<skill>/`.

Five skills have limits in these agents (agent-doctor, efficient-frontier-routing, fable-chief-agent, orchestrator, stay-within-limits); see [Compatibility](#compatibility).
</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

Codex reads skills from `~/.agents/skills/` for personal use or `<repo>/.agents/skills/` for one repository. Use `scripts/install.sh --target codex <skill>` (see above), start a new session, and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).
</details>

<details>
<summary><b>Claude.ai and Claude Cowork</b></summary>

Local `~/.claude/skills/` files do not sync to Claude.ai. Zip one skill folder (the zip must contain the folder itself, with `SKILL.md` inside) and upload it under **Customize → Skills → + → Create skill → Upload a skill** (turn on code execution first under **Settings → Capabilities**; on Enterprise an owner must enable skills under Organization settings), or commit the folder to a project repository's `.claude/skills/`.
</details>

<details>
<summary><b>ChatGPT</b></summary>

Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading. Zip one skill folder and upload it from the **Plugins → Skills** tab with **+ → Upload from your computer**. ChatGPT scans each upload and can mark it Needs Review or Blocked. The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) article is the source of truth.

ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell; check [Compatibility](#compatibility) before uploading. On other plans, use Codex, which reads skill folders directly.
</details>

## Skills

Looking for `deploy`, `pr-wait`, `review-merge-pipeline`, `spec-review`, `auth-hardening`, `rate-limit-audit`, `webhook-reliability`, `exposure-scan`, `db-migration-safety`, `backup-verify`, `dependency-upgrade`, `stripe-billing`, `api-design`, `analytics-instrumentation`, `incident-response`, `observability-setup` or `cdf`? They live in [stylusnexus/agent-plugins](https://github.com/stylusnexus/agent-plugins), a separate marketplace. Five more worth a look there:

- `ship-issues` takes a batch of GitHub issues from intake through merge, and on to deploy when you ask for a release.
- `start-issue` reads an issue in full, checks the work isn't already shipped, and cuts a correctly named branch.
- `prove-it` proves a feature works with real evidence, not just a green CI run.
- `threat-model` writes down who could abuse a new feature or route, and how, before you build it.
- `readiness-review` gives a read-only launch-readiness report on a repo and its live product.

Check out others at [stylusnexus/agent-plugins](https://github.com/stylusnexus/agent-plugins).

### `agent-workflow`

Working habits for coding agents: model routing, background dispatching, status recaps, usage-limit pacing, goal tracking, handoffs, onboarding briefings, prompt tuning, problem framing, and agent-setup checks.

- [`agent-doctor`](plugins/agent-workflow/skills/agent-doctor/README.md) v0.2.0 — Inspects a project's discovered agent instructions (AGENTS.md, CLAUDE.md, GEMINI.md) and skill definitions for static wiring problems, without loading, changing, or enabling them, and reports which installed skills are rarely or never called in local session logs.
- [`ambition`](plugins/agent-workflow/skills/ambition/README.md) v0.2.0 — Reconsiders a project or shelved idea against current capabilities, proposes three ambitious outcomes, and designs an experiment for the hardest uncertainty.
- [`check-worth`](plugins/agent-workflow/skills/check-worth/README.md) v0.2.0 — Review an external PDF, image, screenshot, article, or URL against a repository's current issues and code to sort its ideas into new, already tracked, shipped, contradicted, or unverifiable, read-only by default.
- [`efficient-frontier-routing`](plugins/agent-workflow/skills/efficient-frontier-routing/README.md) v0.2.0 — Routes each task to a suitable model tier in Claude Code, Codex, or another agent host that can start subagents on a chosen model (Gemini CLI, for example), following the user's routing preferences. Keeps small tasks local, delegates discovery, routine coding, and testing to cheaper subagents, and sends difficult decisions and risky reviews to a stronger one.
- [`fable-chief-agent`](plugins/agent-workflow/skills/fable-chief-agent/README.md) v0.2.0 — Makes the most expensive model in a session the senior decision-maker, keeping its reasoning for intent, architecture, decomposition, tradeoffs, final review, and synthesis while cheaper agents handle discovery, implementation, tests, logs, and verification.
- [`goal-checklist`](plugins/agent-workflow/skills/goal-checklist/README.md) v0.2.0 — Tracks a multi-issue goal as a one-line progress strip: seeds a checklist from issue numbers, adds or drops items, marks state, syncs merged vs shipped from git, and re-emits status unprompted as work advances.
- [`handoff`](plugins/agent-workflow/skills/handoff/README.md) v0.2.0 — Writes a copy-pasteable handoff prompt that lets a fresh session of your agent (Claude Code, Codex, Gemini CLI and others) resume the current work cold.
- [`mission`](plugins/agent-workflow/skills/mission/README.md) v0.2.0 — Persist a small, worktree-bound mission record across agent sessions: outcome, constraints, milestones, decisions, next action, and hashed evidence files.
- [`orchestrator`](plugins/agent-workflow/skills/orchestrator/README.md) v0.1.0 — Turns the main session into a dispatcher that stays free where the host allows: it sends each task to a subagent, in the background where the host can, with a self-contained brief, tracks them in a ledger, checks each result, and reports in a few lines.
- [`problem-first`](plugins/agent-workflow/skills/problem-first/README.md) v0.2.0 — Rewrites a draft agent prompt into problem, evidence, ideas, autonomy and done criteria, so you hand over the problem instead of your solution.
- [`quick-recap`](plugins/agent-workflow/skills/quick-recap/README.md) v0.2.0 — Defines a one-line red/yellow/green status line that ends every agent response that completes work, and how to install it as standing instructions in AGENTS.md or CLAUDE.md.
- [`sonnet-prompt-improver`](plugins/agent-workflow/skills/sonnet-prompt-improver/README.md) v0.2.0 — Improves a prompt, system prompt, agent definition or skill for Claude Sonnet 5.5 by applying problem-first framing, adding only the Sonnet 5.5 fixes that match an observed symptom, and suggesting effort and thinking settings.
- [`stay-within-limits`](plugins/agent-workflow/skills/stay-within-limits/README.md) v0.2.0 — Keeps long-running or parallel agent work inside 5-hour and weekly usage limits by running work in bounded waves, checking usage between waves, pausing at 95%, and resuming only after the window resets.
- [`up-to-speed`](plugins/agent-workflow/skills/up-to-speed/README.md) v0.2.0 — Get up to speed on an unfamiliar field in one sitting (roughly 45-90 minutes, shorter on request): the core map, the 8-10 terms insiders use, the 3-5 ideas that explain most of it, live debates, and a scored no-hints exam.

### `writing`

Plain, short, scannable writing: controlled technical English, comma-delimited lists, tables, and a pass that removes AI-writing tells.

- [`clearly`](plugins/writing/skills/clearly/README.md) v0.1.0 — Write plain, short, scannable prose, about 80% of ASD-STE100 (controlled technical English), with habits from Strunk and i-have-adhd.
- [`scrub-ai-tells`](plugins/writing/skills/scrub-ai-tells/README.md) v0.2.0 — Find and remove the characters that mark prose as machine-written — zero-width spaces, narrow no-break spaces, em dashes, curly quotes, ellipsis glyphs.
- [`table`](plugins/writing/skills/table/README.md) v0.2.0 — Presents information as a well-formed table for comparing options, listing items with shared attributes, summarizing findings across cases, or restructuring prose that already carries repeated fields.

### `role-ready-application`

Build truthful, role-tailored resumes and cover letters with candidate-voice review and document preflight.

- [`role-ready-application`](plugins/role-ready-application/skills/role-ready-application/README.md) v0.3.0 — Tailor a truthful resume and cover letter to one job, then review clarity, candidate voice, factual fidelity, and rendered documents.

### `app-governance-kit`

Application portfolio, AI, and access governance methods. Full site with visuals and an interactive practicum: https://evemcgivern.github.io/app-governance-kit/

- [`access-review`](plugins/app-governance-kit/skills/access-review/README.md) v0.1.0 — Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05.
- [`ai-intake`](plugins/app-governance-kit/skills/ai-intake/README.md) v0.1.0 — Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record.
- [`app-governance`](plugins/app-governance-kit/skills/app-governance/README.md) v0.1.0 — Pick the right governance skill for a plain request about a software estate, AI systems, access, or devices, ask for the data, run that skill, and hand every decision back to a person.
- [`cert-prep`](plugins/app-governance-kit/skills/cert-prep/README.md) v0.1.0 — Coach a learner preparing for CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation, or the IAM Certificate with scenario drills on the Halden demo estate, then log gaps and plan the next drills.
- [`crosswalk`](plugins/app-governance-kit/skills/crosswalk/README.md) v0.1.0 — Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing.
- [`hardware-lifecycle`](plugins/app-governance-kit/skills/hardware-lifecycle/README.md) v0.1.0 — Check a device fleet for hardware overdue for refresh and retired devices missing a confirmed data wipe, estimate replacement cost, and produce a disposal-readiness summary.
- [`itam-maturity`](plugins/app-governance-kit/skills/itam-maturity/README.md) v0.1.0 — Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09.
- [`program-setup`](plugins/app-governance-kit/skills/program-setup/README.md) v0.1.0 — Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures.
- [`rationalization`](plugins/app-governance-kit/skills/rationalization/README.md) v0.1.0 — Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk.

### `engineering-practices`

Everyday engineering skills: service debugging, background jobs, transactional email, SaaS metrics, spec-workflow companions, LLM engineering, older-issue triage, and debugging a browser from your agent.

- [`audit-background-processes`](plugins/engineering-practices/skills/audit-background-processes/README.md) v0.2.0 — Inventory and safely clean up stray background processes left by agent sessions — watch loops, tails, orphaned sleeps, detached runs — killing only by PID after confirming ownership.
- [`background-jobs`](plugins/engineering-practices/skills/background-jobs/README.md) v0.2.0 — Design cron jobs and background workers on Render — cron job versus long-running worker, idempotency, Postgres job claiming with advisory or row locks, retries with backoff, timeout budgets, catch-up after downtime, and heartbeat monitoring so silent failures surface.
- [`launch-chrome-debug`](plugins/engineering-practices/skills/launch-chrome-debug/README.md) v0.2.0 — Starts Google Chrome with remote debugging on port 9222 and a separate profile so the Chrome DevTools MCP server can connect, on macOS, Linux or Windows.
- [`llm-engineer`](plugins/engineering-practices/skills/llm-engineer/README.md) v0.2.0 — Evidence-based diagnosis of language-model behavior, serving/runtime configuration, tool-call protocols, and agent evaluation, turning a failure into a bounded, falsifiable experiment.
- [`review-older-issues`](plugins/engineering-practices/skills/review-older-issues/README.md) v0.2.0 — Revalidate a bounded batch of open GitHub issues against current code, pull requests, and related closed issues; close issues already shipped or no longer warranted, and rescope issues whose remaining work differs from the body.
- [`saas-metrics`](plugins/engineering-practices/skills/saas-metrics/README.md) v0.2.0 — Compute and report MRR, churn, activation, and retention for a small SaaS product from Stripe and PostHog data, with metric definitions a small team can maintain, starter Stripe and HogQL snippets, a monthly business-review template, and warnings about common miscounts (trials, refunds, currency, proration).
- [`service-debugging`](plugins/engineering-practices/skills/service-debugging/README.md) v0.2.0 — Turn a live production symptom into a ranked, falsifiable cause: check the failure catalog, correlate recent changes, pull evidence for the top hypothesis, and record the result.
- [`spec-workflow`](plugins/engineering-practices/skills/spec-workflow/README.md) v0.2.0 — Drive spec-driven development through the spec-workflow MCP server: create specs, request approvals, check status, execute tasks from tasks.md and log implementations.
- [`spec-workflow-drift`](plugins/engineering-practices/skills/spec-workflow-drift/README.md) v0.2.0 — Detect drift between spec-workflow specs (.spec-workflow/) and the code: map which source files each spec covers, list files no spec documents, flag stale specs, and write a coverage report.
- [`transactional-email`](plugins/engineering-practices/skills/transactional-email/README.md) v0.2.0 — Set up and audit transactional email for a web app — provider choice (Resend or Postmark), SPF/DKIM/DMARC with verification commands, templates in code, deliverability testing, the transactional-vs-marketing compliance line, and unsubscribe handling.

## Keeping versions current

Each skill has its own `VERSION` and `CHANGELOG.md`. [release-please](https://github.com/googleapis/release-please) maintains them:

1. Merge changes to `main` with [Conventional Commit](https://www.conventionalcommits.org/) titles, for example `fix(clearly): handle empty input`. Squash merges use the PR title, which CI lints.
2. release-please opens one release PR that bumps `VERSION` and `CHANGELOG.md` for each skill that changed (`fix:` is a patch, `feat:` a minor, `feat!:` or a `BREAKING CHANGE:` footer a major).
3. Merging that PR tags each skill (`clearly-v0.2.1`) and creates its GitHub release.

Every pull request runs `python3 -I tests/validate.py` (frontmatter, versions, changelogs, scripts, personal-data scan, marketplace and release config, compatibility badges against `compatibility.json`), `bash tests/install_test.sh`, and `bash tests/run_skill_tests.sh` (every skill's bundled unit tests).

## Provenance

See [PROVENANCE.md](PROVENANCE.md). Licensed under the [MIT License](LICENSE).
