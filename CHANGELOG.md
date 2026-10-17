# Changelog

Each skill keeps its own `VERSION` and `CHANGELOG.md`; release-please maintains them. This file records changes to the repository as a whole.

## Unreleased

All of this landed on 2026-10-17, after the first commit. Per-skill versions and changes are in each skill's own `CHANGELOG.md` and on the GitHub releases page.

### Marketplace

- Converted the repository into a Claude Code plugin marketplace, `evemcgivern-skills`, with 5 plugins and 36 skills: `agent-workflow` (13), `engineering-practices` (10), `app-governance-kit` (9), `writing` (3) and `role-ready-application` (1).
- Imported `app-governance-kit` and `role-ready-application` from the author's earlier packages.
- Added release-please (one version and changelog per skill), a validation workflow that also runs every skill's tests, `scripts/install.sh` for copying single skills, a root `.gitignore`, `SECURITY.md`, `CODEOWNERS` and pinned workflow actions.

### Skills

- Moved 17 skills to [stylusnexus/agent-plugins](https://github.com/stylusnexus/agent-plugins), where they live now: `deploy`, `pr-wait`, `review-merge-pipeline`, `spec-review`, `auth-hardening`, `rate-limit-audit`, `webhook-reliability`, `exposure-scan`, `db-migration-safety`, `backup-verify`, `dependency-upgrade`, `stripe-billing`, `api-design`, `analytics-instrumentation`, `incident-response`, `observability-setup` and `cdf`.
- Dropped `repo-activity-summary`, because stylusnexus's `work-plan` already ships it.
- Of the 20 skills in 0.1.0, three remain here: `quick-recap`, `stay-within-limits` and the skill now named `efficient-frontier-routing`.
- Renamed `efficient-frontier` to `efficient-frontier-routing` and replaced its short text with the fuller routing policy, a configuration reference and a worked example.
- Added `clearly`, `table` and `scrub-ai-tells` (`writing`).
- Added `agent-doctor`, `ambition`, `check-worth`, `fable-chief-agent`, `goal-checklist`, `handoff`, `mission`, `problem-first`, `sonnet-prompt-improver` and `up-to-speed` (`agent-workflow`).
- Added `audit-background-processes`, `background-jobs`, `launch-chrome-debug`, `llm-engineer`, `review-older-issues`, `saas-metrics`, `service-debugging`, `spec-workflow`, `spec-workflow-drift` and `transactional-email` (`engineering-practices`).
- Added a usage and freshness report to `agent-doctor` (`--usage`), with a separate `skill_archive.py` that moves a skill to a dated backup folder only after an explicit `--yes` and can restore it.
- Listed the `tutor` plugin from its own repository, then removed the listing the same day when that repository was made private.

### Docs

- Per-platform install steps in the root README, in `role-ready-application` and in `app-governance-kit`, with the Claude app and ChatGPT steps corrected to match the vendors' help pages.
- The full app governance site (practicum, crosswalk explorer, impact map, lifecycle, field guide, SAM toolkit) is linked from the `app-governance-kit` plugin.
- A "What it looks like" section in every skill README: real output where a script exists, diagrams where the sequence matters, and examples elsewhere.
- Compatibility badges (Claude, Codex / ChatGPT, other agents) on every skill README, backed by `compatibility.json` and a validator check, with a Compatibility section in the root README.

## 0.1.0 — 2026-10-17

- Publish 20 reviewed skills in a clean repository with no private source history.
- Generalize personal and project-specific references while retaining skill workflows.
- Add per-skill README, VERSION, and CHANGELOG metadata.
