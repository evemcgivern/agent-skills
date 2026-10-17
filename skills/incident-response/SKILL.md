---
name: incident-response
description: Production incident runbook sized for a small team. Use when a service is down, erroring, or degraded in production — Render alert fires, Better Stack paging, users reporting errors, or a bad deploy is suspected. Covers triage order, rollback, comms, and lightweight postmortem.
---

# Incident Response

## Overview

This is deliberately lightweight — no incident commander rotation, no status-page automation, no war-room tooling. Two people means the runbook has to be fast to execute solo, at 2am, half-awake. The whole point is: know the triage order cold, roll back before diagnosing root cause, and don't skip the five-minute postmortem even when it's tempting to just move on.

## Severity levels

| Level | Definition | Response time |
|-------|-----------|----------------|
| **S1** | Full outage, data loss risk, or payment/auth broken | Immediate, drop everything |
| **S2** | Major feature broken, subset of users affected, no data risk | Within the hour |
| **S3** | Minor bug, cosmetic, workaround exists | Next business day |

If unsure between S1/S2, treat as S1 — the cost of over-reacting to a false alarm is much lower than the cost of under-reacting to a real one.

## Workflow

1. **Acknowledge** — silence the page/alert so it stops re-firing, but don't close it yet.

2. **Triage in this order** (don't skip steps even if step 1 looks conclusive):
   - **Better Stack** — is this a real outage or a monitor false-positive (e.g., flaky healthcheck endpoint)? Check the uptime graph for the actual service, not just the alert text.
   - **Render logs** — the hosting provider dashboard or CLI, filtered to the last 30 minutes. Look for a spike in 5xx, OOM kills, or crash-loop restarts.
   - **Sentry / error tracking** — new error signature, or existing one spiking in volume? A brand-new error type strongly suggests the last deploy.
   - **Recent deploys** — the hosting provider deployment history — did a deploy land in the last 30–60 minutes? Correlate the timestamp against when the alert fired.

3. **Decide: rollback or forward-fix.**
   - If a deploy correlates with the incident start and root cause isn't obvious in under 5 minutes: **roll back first, diagnose after.** Users don't care that you found the bug if the site is still down while you fix it properly.
   - Rollback mechanism: `git revert <bad-commit>` (never `reset --hard` on a shared branch), push, let Render auto-deploy from the reverted `main`/`dev`. For a faster stopgap, Render's dashboard also supports redeploying a specific prior successful deploy directly — use that if `git revert` would be non-trivial (merge conflicts, multiple commits).
   - If no recent deploy correlates (infra issue, third-party outage, DB connection exhaustion): diagnose in place — check Neon/Supabase connection pool metrics, check upstream API status pages (Stripe, Anthropic, PostHog).

4. **Confirm resolution** — watch Better Stack return green and error rate in Sentry drop to baseline for at least 5–10 minutes before declaring resolved. Don't declare victory on the first clean data point.

5. **User comms** (S1/S2 only) — short, honest, no jargon. Template:
   > We're aware of an issue affecting [feature] and are actively working on it. [If applicable: your data is safe / not affected.] We'll update this within [timeframe].
   Post wherever users would look (status page, in-app banner, or direct email if it's a small paying user base). Update again on resolution — silence after the first message erodes trust faster than the incident itself.

6. **Blameless postmortem** — write this within 24 hours while memory is fresh, even for S2/S3. Template (keep it to one page):
   ```markdown
   # Incident: <short title> — <date>

   **Severity:** S1/S2/S3
   **Duration:** <start> – <end> (X minutes)
   **User impact:** who/what was affected, how many users if knowable

   ## What happened
   Plain narrative, chronological. No blame language ("the deploy introduced X", not "so-and-so broke X").

   ## Root cause
   The actual mechanism — not just "bad deploy" but *why* the deploy caused it.

   ## Detection
   How did we find out? (alert / user report / manual check) — if it was a user report, that's a monitoring gap worth a follow-up.

   ## Resolution
   What fixed it (rollback / hotfix / config change).

   ## Follow-ups
   - [ ] <concrete, assigned, with issue number>
   ```

7. **Create follow-up issues immediately** — a postmortem with unlinked "follow-ups" text is where action items go to die. File each as a real GitHub issue with the severity and postmortem linked.

## Output / Evidence

Show the user: the alert timestamp, the log/error evidence that identified the cause, the rollback command actually run, and the Better Stack graph confirming recovery. The postmortem doc and its follow-up issue links are the deliverable, not a verbal summary.

## Stop Conditions

- Root cause implicates a database migration or data mutation — stop before any further DB changes; confirm a recent backup exists ([[backup-verify]]) before touching anything.
- Rollback itself fails or the "known good" commit is unclear — stop and escalate to the designated incident lead rather than guessing at `main` HEAD.
- Suspected security incident (auth bypass, data exposure) — this is not a normal S1; treat as a security incident, preserve logs, and don't publicly disclose details until scope is understood.
