# Eve McGivern’s Agent Skills

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-20-blue.svg)](#skills) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Reusable, portable `SKILL.md` workflows for Claude Code and Codex. They use the open Agent Skills folder format; some workflows also call local CLIs or reference sibling skills, as noted in their documentation.

## Install

Choose one or more skill directories from `skills/` and copy each complete directory to the target platform’s skill location. Keep supporting files beside `SKILL.md`.

### Claude Code CLI and Claude Code desktop (local sessions)

Copy each selected folder to `~/.claude/skills/<skill-name>/`. For repository-only use, copy it to `<repo>/.claude/skills/<skill-name>/`. Claude Code desktop local sessions use Claude Code’s skill locations. Claude.ai Cowork and cloud sessions use skills enabled in the account settings or project skills committed to the repository; local `~/.claude/skills/` files alone do not sync there. See [Claude Code skills docs](https://code.claude.com/docs/en/skills).

### Codex CLI, IDE extension, and desktop app

Copy each selected folder to `~/.agents/skills/<skill-name>/` for personal use, or `<repo>/.agents/skills/<skill-name>/` for one repository. Start a new session or reload skills if needed. See [Codex skills docs](https://developers.openai.com/codex/skills-and-plugins).

### ChatGPT web / account-level skills

A `SKILL.md` folder by itself is not an account-level ChatGPT upload/install. Use Codex skill folders in Codex-compatible surfaces, or paste the skill instructions into the relevant ChatGPT configuration where supported. Do not assume local files sync to ChatGPT web.

## Skills

- [`analytics-instrumentation`](skills/analytics-instrumentation/README.md) — PostHog event taxonomy and instrumentation review for products — naming convention, property schemas, identify/group calls, PII exclusion, a starter dashboard set (activation, retention, funnel), and a per-feature instrumentation checklist. Use when instrumenting a new feature, reviewing existing PostHog events, or setting up analytics for a new product.
- [`api-design`](skills/api-design/README.md) — REST conventions for Next.js App Router route handlers — resource naming, versioning, pagination, a standard error envelope, Zod request/response validation, status-code discipline, OpenAPI generation, and API-response scrubbing (no PII/internal IDs/tokens). Use when asked to "design an API route," "add a new endpoint," "review this route handler," or "generate API docs.
- [`auth-hardening`](skills/auth-hardening/README.md) — NextAuth v5 security audit and hardening checklist — session/cookie config, CSRF, OAuth scopes, per-route role checks, password-reset/OTP rate limits, secret rotation, session invalidation on privilege change. Use when adding auth to a new product, auditing an existing NextAuth v5 app, or reviewing any PR that touches session/role/permission code.
- [`backup-verify`](skills/backup-verify/README.md) — Confirm database backups exist AND actually restore, by enumerating Neon branch snapshots / Supabase scheduled backups / pg_dump artifacts, restoring into a scratch branch, running smoke queries, and recording timestamped evidence. Use before any risky migration or production mutation, and on a monthly cadence regardless.
- [`db-migration-safety`](skills/db-migration-safety/README.md) — Write or review Prisma and Supabase database migrations safely using the expand-contract pattern, idempotent SQL, and batched backfills. Use when adding/changing columns or tables, writing a migration PR, or reviewing one before merge — especially against Neon Postgres or Supabase in production.
- [`dependency-upgrade`](skills/dependency-upgrade/README.md) — Safe batch dependency upgrades across projects — inventory outdated packages (npm outdated / uv lock --upgrade), group by risk (patch/minor/major), upgrade in waves with tsc/test/Playwright gates, read changelogs for majors, run /exposure-scan for supply-chain checks, and land one PR per wave. Use when asked to "upgrade dependencies," "bump packages," "clear npm outdated," or on a periodic maintenance pass.
- [`deploy`](skills/deploy/README.md) — Merge dev to main for production deployment. Repo-agnostic — detects the repo's conventions and defers to any repo-local runbook. Use once daily or when ready to push to production.
- [`efficient-frontier`](skills/efficient-frontier/README.md) — Route model effort efficiently across research, coding, and review, including for users with limited quotas. Use when deciding whether to delegate routine work, reserve stronger models for judgment, or control model usage.
- [`exposure-scan`](skills/exposure-scan/README.md) — Scan installed packages against bumblebee threat-intelligence exposure catalogs to detect known-compromised dependency releases (supply-chain campaigns like shai-hulud, node-ipc, gemstuffer). Use when checking for compromised packages, running a supply-chain or dependency security scan, auditing the machine after a reported npm/PyPI/Go/gem/extension compromise, or refreshing threat-intel catalogs.
- [`incident-response`](skills/incident-response/README.md) — Production incident runbook sized for a small team. Use when a service is down, erroring, or degraded in production — Render alert fires, Better Stack paging, users reporting errors, or a bad deploy is suspected. Covers triage order, rollback, comms, and lightweight postmortem.
- [`observability-setup`](skills/observability-setup/README.md) — Wire a service for observability sized for a small team — Better Stack uptime checks and log drains from Render, error tracking, PostHog product analytics, Render health-check endpoints, and alert thresholds tuned so two humans aren't paged into the ground. Use when launching a new service, adding monitoring to an existing one, or when alert fatigue is a complaint.
- [`pr-wait`](skills/pr-wait/README.md) — Wait for GitHub PR CI checks to complete, then optionally merge
- [`quick-recap`](skills/quick-recap/README.md) — Use when adding or following the red/yellow/green final status block convention for agent responses, especially by installing managed AGENTS.md or CLAUDE.md instructions.
- [`rate-limit-audit`](skills/rate-limit-audit/README.md) — Pre-launch gate that inventories every endpoint calling a paid API (LLM, email, SMS) and every auth endpoint, verifies a rate limiter exists, and actually tests it with scripted burst requests to confirm 429s fire. Use before launching a new product/feature, after adding an LLM-calling or auth route, or when asked to check rate limiting.
- [`repo-activity-summary`](skills/repo-activity-summary/README.md) — Use when the user asks to summarize repo activity, check project status, gauge progress, list open issues and PRs, or see CI health. Triggers on "activity summary", "what's open", "project status", "progress check", "CI status".
- [`review-merge-pipeline`](skills/review-merge-pipeline/README.md) — Automated pipeline that code-reviews uncommitted changes, fixes issues found, commits, pushes, creates a PR, and merges with --admin. Accepts an optional worktree path argument and flags --no-review / --no-merge / --rebase / --cross-model. Use when work is done and you want to ship it without manual steps.
- [`spec-review`](skills/spec-review/README.md) — Use when a design spec, plan, or requirements doc is drafted/ratified/about-to-be-implemented and you want a rigorous second-model review that verifies the spec's claims against the real codebase — catching wrong data-model assumptions (scalar-vs-M2M), unverified schema/API claims, missing acceptance criteria, ambiguity, and internal contradictions before code is written. The spec-world analog of /codex:review for PRs.
- [`stay-within-limits`](skills/stay-within-limits/README.md) — Use when long-running or parallel agent work must respect 5-hour and weekly usage limits by checking usage between waves, pausing near the cap, and resuming only when the window is clear.
- [`stripe-billing`](skills/stripe-billing/README.md) — Implement or review Stripe subscription billing for a Next.js App Router product (Checkout, customer portal, webhook handler, plan changes, trials, dunning). Use when adding subscriptions or paywalls to a product or service, when reviewing existing billing code for correctness, or when a webhook/proration/trial bug is reported.
- [`webhook-reliability`](skills/webhook-reliability/README.md) — Design or review inbound and outbound webhooks for signature verification, idempotency, retry/backoff, dead-letter recording, replay tooling, and timeout budgets. Use when building a new webhook handler or emitter, reviewing an existing one (Stripe, GitHub, or a custom outbound webhook), or investigating a "webhook silently didn't fire" report.
## Notes

- Review each skill and its required tools before use. A skill is instruction text; tool availability, permissions, and platform behavior depend on the host.
- Skills do not replace repository-specific documentation, approval rules, or tests.
- This package does not promise that a task can be completed without the needed model, tools, data, or quota.
- See [PROVENANCE.md](PROVENANCE.md) for the clean-copy and license history.
