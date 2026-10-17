# Security

These skills are instructions plus a few shell and Python scripts that agents run on your machine. Read a skill before you install it, and run its scripts only on code you trust.

## Supported versions

Only the latest `main` is supported. Fixes land there and ship in the next release; older releases do not get backported fixes.

## Scope

In scope:

- The shipped shell and Python scripts under `plugins/` and `scripts/`.
- Skill instructions (`SKILL.md` and the files they point to), including anything that could lead an agent to run a harmful command, leak data, or follow instructions planted in content it reads.
- The install guidance in the READMEs and `scripts/install.sh`.

Out of scope: third-party tools a skill tells you to install or run (report those to their maintainers), and the agents themselves.

## Security posture

Last checked against the repository settings on 2026-10-17.

### What the scripts do

No shipped script imports a network library or calls `curl` or `wget`. Nothing sends data off your machine. The network use you may see comes from the agent, the `gh` CLI or the tools a skill tells the agent to run.

| Script | Reads or writes | Network | Needs confirmation |
| --- | --- | --- | --- |
| `scripts/install.sh` | Reads this repo, copies skill folders into a skills folder | No | Skips existing skills. Replaces one only with `--force`. Rejects names outside `A-Za-z0-9._-` |
| `scripts/gen-skill-install.py` | Rewrites the Install section of skill READMEs (maintainers only) | No | `--check` only reports |
| `agent-doctor` `agent_doctor.py` | Reads instruction files, skill folders and, with `--usage`, local Claude Code and Codex session logs. Writes nothing | No | Not needed, read only |
| `agent-doctor` `skill_archive.py` | Moves skills to a dated archive folder, writes a record file. Never deletes | No | `archive` refuses without `--yes`. `plan` changes nothing |
| `mission` `mission.py` | Writes JSON under `~/.local/state/agent-missions` (or `--state-dir`). Runs read-only `git` commands | No | No. It never runs recorded actions |
| `audit-background-processes` `audit.sh` | Reports your own processes only | No | `--kill` takes numeric PIDs only, sends SIGTERM only to a PID in a fresh suspect list, and refuses the rest |
| `scrub-ai-tells` `scrub_ai_tells.py` | Reads the files you name. Rewrites them only with `--write` and saves `FILE.bak` first | No | `--write` is opt in |

Session logs: `--usage` reads them to count skill calls. It keeps skill names, timestamps and counts, and prints no conversation text.

Also in the repo: `tests/` runs `validate.py` and unit tests, and `plugins/app-governance-kit/demo-estate/generate.py` writes sample files. Neither uses the network.

### Threat model for skills

- Prompt injection. A fetched page, PDF, image or issue can carry planted instructions. `check-worth` treats them as untrusted data and does not let them trigger commands, file reads outside the task, or sending data anywhere. Other skills that read outside content have no such rule. Treat their input with care.
- Pinned installs. `stay-within-limits` runs `ccusage` at a pinned version (`ccusage@20.0.26`), never `@latest` and never with `-y`. The agent asks you before the first run in a session.
- Skills that run commands: `agent-doctor` (Python, read only except archive), `mission` (Python, git), `handoff` (git status and log), `goal-checklist` (git), `check-worth` (`gh issue` reads), `review-older-issues` (`gh`, can edit issues), `audit-background-processes` (`ps`, `kill`), `launch-chrome-debug` (starts Chrome with a debug port), `scrub-ai-tells` (can rewrite files), `spec-workflow-drift` (can stage and commit cleanup files), `stay-within-limits` (`npx`).
- Where they confirm: `skill_archive.py` needs `--yes`, `audit.sh --kill` needs explicit PIDs and the skill tells the agent to ask when ownership is unclear, `stay-within-limits` asks before `npx`, and `review-older-issues` works on a batch you name and re-checks each issue before changing it.

### Supply chain controls

Checked with read-only `gh api` calls and the files under `.github/`.

- GitHub Actions are pinned to commit SHAs. Dependabot updates them weekly.
- Allowed actions: GitHub-owned actions, `googleapis/release-please-action` and `amannn/action-semantic-pull-request`. SHA pinning is required.
- The default workflow token is read only. Actions cannot approve pull requests.
- Only the `release-please` job holds write permissions (`contents` and `pull-requests`). It uses the `RELEASE_PLEASE_TOKEN` secret, a personal access token the owner keeps for this repository (its scope is not visible from the repo), and falls back to the default token if it is unset.
- CodeQL code scanning runs weekly on Actions and Python.
- Secret scanning and push protection are on. Dependabot alerts and security updates are on.
- A repository ruleset ("Protect release tags") blocks deleting, moving or updating tags that match `*-v*`. It has no bypass actors.
- `main` requires a pull request and the `skills` and `pr-title` checks. Admins are included. History must be linear. Force pushes and deletion are blocked. Required approving reviews: 0.

### Before you run a skill

1. Read `SKILL.md` and any script it names.
2. Prefer pinned installs. Never switch a pinned version to `@latest`.
3. Run skills in a project you trust.
4. The Claude app and ChatGPT run skills in a sandbox with no access to your local files or shell. Local-shell skills do not run there.

### Known limits

- Skills are instructions that an agent interprets. The agent can still misread them or be steered by content it reads.
- No third party has audited this repository.
- Some commits carry a `Claude-Session` trailer with a public link. Opening it needs a Claude login.

## Reporting a problem

Report a vulnerability or a harmful instruction through GitHub's private vulnerability reporting: **Security → Report a vulnerability** on this repository. Please do not open a public issue for it.

Include the skill name, the file and line, and what an agent could be tricked into doing. Expect a reply within a week.
