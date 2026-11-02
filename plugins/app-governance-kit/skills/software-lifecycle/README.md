# Software Lifecycle

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> Not for the Claude app or ChatGPT: running it there would mean uploading your inventory to a remote sandbox. The tool runs on your own machine, next to the inventory.

Find installed software past or near end of life, with a CISA KEV needs-review flag, by running the offline [software-lifecycle](https://github.com/evemcgivern/software-lifecycle) tool on a software inventory export on your own machine. Reports summary counts only, never names or item IDs. Use for a quarterly software lifecycle review or before an upgrade budget request.

The skill holds instructions only. The check itself is done by the software-lifecycle tool, pinned to release v0.7.0, commit `1ebc996e52b728507a4113aee6c67ea0e208a9e7`. Runs locally with no network by default; not independently assessed.

## When and how to use it

**Use it when**
- You run a quarterly review of what software is past or near end of life.
- You prepare an upgrade budget request and need counts by state.
- You want the KEV needs-review items first, without showing an agent your software names.

**Try it**
```text
Check our software inventory export for end of life as of 2026-10-24. Counts only.
Which item IDs need review because their vendor and product appear in CISA KEV?
```
The agent asks for your header row, gets the tool at the pinned commit, runs `preflight` and then the check with `--counts-only` into a folder you name, and reports summary counts. It does not name item IDs, and it does not open the inventory or the full report.

**Skip it when**
- You need to review software licenses or duplicate apps. Use the rationalization skill.
- You need to check device refresh dates. Use the hardware-lifecycle skill.

## What it looks like

Example of what the agent reports on the tool's synthetic demo (`examples/` at the pinned commit, 60 rows, checked 2026-10-24 against the synthetic test data). The counts come from an earlier release of the tool and were not re-run on v0.7.0: Unverified.

````text
Checked on 2026-10-24. KEV data current: yes (synthetic demo data).

50 items from 60 rows.
Past end of life 8 · Ends within 12 months 5 · Mainstream support ended 1
Supported 25 · Unmatched 11
Names to review: 1 (unmatched on purpose, not a finding).
Classification: governable 40, component 0, bundle member 3, unknown 7.

Item IDs are not relayed. Read each list in report.md yourself.
The vendor and product appear in CISA KEV. This does not mean your version is affected.

Decision needed: for each past-end-of-life or ends-soon item, the asset owner
chooses replace, upgrade, retire, or request risk acceptance.
Decision needed: a person checks each review-urgently version against KEV.

```findings
[]
```
````

## Install

<!-- install:begin -->
Pick your platform. Steps expand below. The [Install section of the collection README](../../../../README.md#install) has the full guide.

<details>
<summary><b>Claude Code (terminal CLI)</b> — recommended</summary>

```bash
claude plugin marketplace add evemcgivern/agent-skills
claude plugin install app-governance-kit@evemcgivern-skills
```

This installs the whole `app-governance-kit` plugin, so you also get its other skills: `access-review`, `ai-intake`, `app-governance`, `cert-prep`, `crosswalk`, `hardware-lifecycle`, `itam-maturity`, `program-setup`, `rationalization`. Run it as `/app-governance-kit:software-lifecycle`. Inside a session, the same thing is `/plugin marketplace add evemcgivern/agent-skills`, then `/plugin install app-governance-kit@evemcgivern-skills`.

Update later with `claude plugin marketplace update evemcgivern-skills`, then `claude plugin update app-governance-kit@evemcgivern-skills`.

To install only this skill, copy it from a clone of the repo:

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh software-lifecycle   # into ~/.claude/skills/software-lifecycle
```

Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.

</details>

<details>
<summary><b>Claude Code desktop app</b></summary>

In a local Code session choose **+ → Plugins → Add plugin**, enter `evemcgivern/agent-skills` as the marketplace, then install **app-governance-kit** (it brings the plugin's other skills too).

Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/software-lifecycle/` instead.

</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

```bash
git clone https://github.com/evemcgivern/agent-skills.git && cd agent-skills
scripts/install.sh --target codex software-lifecycle   # into ~/.agents/skills/software-lifecycle
```

Add `--project <repo-path>` to install into that repository's `.agents/skills/software-lifecycle/` instead. Or copy this folder by hand to `~/.agents/skills/software-lifecycle/`, or `.agents/skills/software-lifecycle/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

</details>

<details>
<summary><b>Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline</b></summary>

These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:

- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/software-lifecycle/` for personal use (`scripts/install.sh --target codex software-lifecycle` does this), or `<repo>/.agents/skills/software-lifecycle/` for one repository.
- Windsurf: `<repo>/.agents/skills/software-lifecycle/`.
- Cline: `<repo>/.cline/skills/software-lifecycle/`, `<repo>/.claude/skills/software-lifecycle/` or `~/.cline/skills/software-lifecycle/`.

</details>

<details>
<summary><b>Claude app: not supported</b></summary>

Running it in the Claude app would mean uploading your confidential inventory to a remote sandbox; run it on your own machine instead.

Use Claude Code or Codex on your computer instead.

</details>

<details>
<summary><b>ChatGPT: not supported</b></summary>

Running it in ChatGPT would mean uploading your confidential inventory to a remote sandbox; run it on your own machine instead.

Use Claude Code or Codex on your computer instead.

</details>

The skill needs the [software-lifecycle](https://github.com/evemcgivern/software-lifecycle) tool, Python 3.9 or newer and git on your own machine. Its steps fetch the tool at release v0.7.0, commit `1ebc996e52b728507a4113aee6c67ea0e208a9e7`, and check `git rev-parse HEAD`.

The kit's full site, with visuals and an interactive practicum: https://evemcgivern.github.io/app-governance-kit/

<!-- install:end -->

The tool also ships an optional counts-only server for desktop chat apps and a one-click Claude Desktop package, which is unsigned. The tool's docs say each was tested once on one Mac; everything beyond that is Unverified. See the tool's [docs/mcp-setup.md](https://github.com/evemcgivern/software-lifecycle/blob/main/docs/mcp-setup.md). This skill does not use them.

## Included

- `SKILL.md`
- `crosswalk.csv`
- `agents/openai.yaml` for ChatGPT/Codex skill-card metadata.
- `VERSION` and `CHANGELOG.md` for this package snapshot.

The procedure, checklist, templates and demo live in the tool's repository at the pinned commit, so they are not copied here.
