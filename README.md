# Eve McGivern's Agent Skills

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-15-blue.svg)](#skills)

Skills for Claude Code and Codex, packaged as a Claude Code plugin marketplace. Each skill is a folder with a `SKILL.md`. Pick your tool below; one click opens the steps.

## Install

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install ship-and-operate@evemcgivern-skills
claude plugin install agent-workflow@evemcgivern-skills
claude plugin install writing@evemcgivern-skills
claude plugin install role-ready-application@evemcgivern-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install <plugin>@evemcgivern-skills`. Skills then appear as `/<plugin>:<skill>`, for example `/ship-and-operate:deploy`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update <plugin>@evemcgivern-skills` for each installed plugin.
</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install the plugins you want. Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit the skill folders to your repository's `.claude/skills/` instead.
</details>

<details>
<summary><b>Claude Code or Codex — copy single skills</b></summary>

From a clone of this repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --list                          # see skill names
scripts/install.sh deploy pr-wait                  # Claude Code, into ~/.claude/skills
scripts/install.sh --target codex --all            # Codex, into ~/.agents/skills
scripts/install.sh --project ~/code/myapp deploy   # one repository only
```

Add `--force` to replace a skill you already have. Or copy a folder by hand from `plugins/<plugin>/skills/<skill>/` to `~/.claude/skills/<skill>/` (Claude Code) or `~/.agents/skills/<skill>/` (Codex). Keep every file in the folder together.
</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

Codex reads skills from `~/.agents/skills/` for personal use or `<repo>/.agents/skills/` for one repository. Use `scripts/install.sh --target codex <skill>` (see above), start a new session, and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).
</details>

<details>
<summary><b>Claude.ai and Claude Cowork</b></summary>

Local `~/.claude/skills/` files do not sync to Claude.ai. Zip one skill folder (the zip must contain the folder itself, with `SKILL.md` inside) and upload it under **Settings → Capabilities → Skills**, or commit the folder to a project repository's `.claude/skills/`.
</details>

<details>
<summary><b>ChatGPT</b></summary>

A `SKILL.md` folder is not an account-level ChatGPT install. On workspaces that allow uploadable skills, zip one skill folder and upload it under **Plugins → Skills → Create → Upload from your computer**. Availability depends on your plan and workspace admin settings. Otherwise paste the skill's instructions into a custom GPT or project instructions.
</details>

## Skills

Looking for `deploy`, `pr-wait`, `review-merge-pipeline`, `spec-review`, `auth-hardening`, `rate-limit-audit`, `webhook-reliability`, `exposure-scan`, `db-migration-safety`, `backup-verify`, `dependency-upgrade`, `stripe-billing`, `api-design`, `analytics-instrumentation`, `incident-response`, `observability-setup` or `cdf`? They live in [stylusnexus/agent-plugins](https://github.com/stylusnexus/agent-plugins), a separate marketplace. Five more worth a look there:

- `ship-issues` takes a batch of GitHub issues from intake through merge, and on to deploy when you ask for a release.
- `start-issue` reads an issue in full, checks the work isn't already shipped, and cuts a correctly named branch.
- `prove-it` proves a feature works with real evidence, not just a green CI run.
- `threat-model` writes down who could abuse a new feature or route, and how, before you build it.
- `readiness-review` gives a read-only launch-readiness report on a repo and its live product.

Check out others at [stylusnexus/agent-plugins](https://github.com/stylusnexus/agent-plugins).

### `ship-and-operate`

Summarize repo activity: open issues and PRs, CI health, and progress.

- [`repo-activity-summary`](plugins/ship-and-operate/skills/repo-activity-summary/README.md) v0.2.0 — Summarize current GitHub repo activity - open issues, open PRs with check status, recent CI runs, and local branch state - in one report with planning takeaways, via the gh CLI.

### `agent-workflow`

Working habits for coding agents: model routing, final status recaps, and usage-limit pacing.

- [`efficient-frontier`](plugins/agent-workflow/skills/efficient-frontier/README.md) v0.2.0 — Routes model effort across research, coding, testing, and review so strong models handle judgment and cheaper subagents handle volume, including for users with limited quotas.
- [`quick-recap`](plugins/agent-workflow/skills/quick-recap/README.md) v0.2.0 — Defines a one-line red/yellow/green status line that ends every agent response that completes work, and how to install it as standing instructions in AGENTS.md or CLAUDE.md.
- [`stay-within-limits`](plugins/agent-workflow/skills/stay-within-limits/README.md) v0.2.0 — Keeps long-running or parallel agent work inside 5-hour and weekly usage limits by running work in bounded waves, checking usage between waves, pausing at 95%, and resuming only after the window resets.

### `writing`

Plain, short, scannable writing: controlled technical English, comma-delimited lists, and an optional explain mode.

- [`clearly`](plugins/writing/skills/clearly/README.md) v0.1.0 — Write plain, short, scannable prose, about 80% of ASD-STE100 (controlled technical English), with habits from Strunk and i-have-adhd.

### `role-ready-application`

Build truthful, role-tailored resumes and cover letters with candidate-voice review and document preflight.

- [`role-ready-application`](plugins/role-ready-application/skills/role-ready-application/README.md) v0.2.0 — Tailor a truthful resume and cover letter to one job, then review clarity, candidate voice, factual fidelity, and rendered documents.

### `app-governance-kit`

Application portfolio, AI, and access governance methods.

- [`access-review`](plugins/app-governance-kit/skills/access-review/README.md) v0.1.0 — Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05.
- [`ai-intake`](plugins/app-governance-kit/skills/ai-intake/README.md) v0.1.0 — Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record.
- [`app-governance`](plugins/app-governance-kit/skills/app-governance/README.md) v0.1.0 — Pick the right governance skill for a plain request about a software estate, AI systems, access, or devices, ask for the data, run that skill, and hand every decision back to a person.
- [`cert-prep`](plugins/app-governance-kit/skills/cert-prep/README.md) v0.1.0 — Coach a learner preparing for CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation, or the IAM Certificate with scenario drills on the Halden demo estate, then log gaps and plan the next drills.
- [`crosswalk`](plugins/app-governance-kit/skills/crosswalk/README.md) v0.1.0 — Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing.
- [`hardware-lifecycle`](plugins/app-governance-kit/skills/hardware-lifecycle/README.md) v0.1.0 — Check a device fleet for hardware overdue for refresh and retired devices missing a confirmed data wipe, estimate replacement cost, and produce a disposal-readiness summary.
- [`itam-maturity`](plugins/app-governance-kit/skills/itam-maturity/README.md) v0.1.0 — Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09.
- [`program-setup`](plugins/app-governance-kit/skills/program-setup/README.md) v0.1.0 — Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures.
- [`rationalization`](plugins/app-governance-kit/skills/rationalization/README.md) v0.1.0 — Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk.

## Keeping versions current

Each skill has its own `VERSION` and `CHANGELOG.md`. [release-please](https://github.com/googleapis/release-please) maintains them:

1. Merge changes to `main` with [Conventional Commit](https://www.conventionalcommits.org/) titles, for example `fix(deploy): handle empty check list`. Squash merges use the PR title, which CI lints.
2. release-please opens one release PR that bumps `VERSION` and `CHANGELOG.md` for each skill that changed (`fix:` is a patch, `feat:` a minor, `feat!:` or a `BREAKING CHANGE:` footer a major).
3. Merging that PR tags each skill (`deploy-v0.2.1`) and creates its GitHub release.

Every pull request runs `python3 -I tests/validate.py` (frontmatter, versions, changelogs, scripts, personal-data scan, marketplace and release config) and `bash tests/install_test.sh`.

## Provenance

See [PROVENANCE.md](PROVENANCE.md). Licensed under the [MIT License](LICENSE).
