---
name: incident-response
description: Production incident runbook for a small team - severity call, fixed triage order, rollback-first decision, user comms, and a one-page blameless postmortem. Use when a service is down, erroring, or degraded in production, e.g. "site is down", "we're getting 500s", "uptime alert fired", "users report errors", "was it the last deploy?", "roll back", or "write the postmortem".
---

# Incident Response

## Overview

Lightweight on purpose: no incident-commander rotation, no war-room tooling. One person must be able to run it alone, half-awake. Three rules: follow the triage order, roll back before hunting root cause, and write the postmortem even when it is tempting to move on.

Tool names below (Better Stack, Render, Sentry) are examples. Substitute the uptime monitor, host, and error tracker the project actually uses.

## Severity levels

| Level | Definition | Response time |
|-------|-----------|----------------|
| **S1** | Full outage, data loss risk, or payment/auth broken | Immediate, drop everything |
| **S2** | Major feature broken, subset of users affected, no data risk | Within the hour |
| **S3** | Minor bug, cosmetic, workaround exists | Next business day |

Unsure between S1 and S2? Treat it as S1. Over-reacting to a false alarm costs less than under-reacting to a real one.

## Workflow

1. **Acknowledge** the alert so it stops re-firing. Do not resolve it yet. Write down the alert timestamp.

2. **Triage in this order.** Do every step even if an earlier one looks conclusive:
   1. **Uptime monitor** - real outage or monitor false positive (flaky health endpoint, one region failing)? Check the service's uptime graph, not just the alert text.
   2. **Host logs** - last 30 minutes. Look for a 5xx spike, out-of-memory kills, or crash-loop restarts.
   3. **Error tracker** - a new error signature, or a known one spiking? A brand-new error type points at the last deploy.
   4. **Recent deploys** - did a deploy land in the 30-60 minutes before the alert? Compare its timestamp with the alert timestamp.

3. **Decide: roll back or fix forward.**
   - A deploy correlates with the start and root cause is not obvious within 5 minutes: **roll back first, diagnose after.**
   - Rollback options:
     - **Host rollback** (fastest): redeploy the last known-good deploy from the host's deploy history. On Render, a Dashboard rollback reuses the old build artifact and **disables auto-deploy** for the service; re-enable it after the fix lands, or the next push will not deploy. Rollbacks do not revert disks, instance type, or custom domains, and only recent build artifacts are kept.
     - **Git revert**: `git revert <bad-commit>` and push so the branch matches what is running. Never `git reset --hard` on a shared branch.
   - No deploy correlates (infrastructure issue, third-party outage, database connection exhaustion): diagnose in place. Check database connection and pool metrics, and the status pages of upstream providers (payments, LLM APIs, analytics).

4. **Confirm resolution.**
   - Pass: uptime monitor green **and** error rate back at its pre-incident baseline for at least 10 consecutive minutes.
   - Fail: any relapse inside that window. Return to step 2; do not declare resolved on the first clean data point.

5. **User comms (S1/S2 only)** - short, honest, no jargon:
   > We're aware of an issue affecting [feature] and are actively working on it. [If true: your data is safe.] We'll update this within [timeframe].

   Post where users look (status page, in-app banner, or direct email for a small paying base). Post again on resolution. Silence after the first message erodes trust faster than the incident.

6. **Blameless postmortem** within 24 hours, for every severity. One page:
   ```markdown
   # Incident: <short title> - <date>

   **Severity:** S1/S2/S3
   **Duration:** <start> - <end> (X minutes)
   **User impact:** who/what was affected, how many users if knowable

   ## What happened
   Chronological narrative. Describe systems, not people ("the deploy introduced X").

   ## Root cause
   The mechanism - not "bad deploy" but why the deploy caused it.

   ## Detection
   Alert, user report, or manual check? A user report means a monitoring gap - add a follow-up.

   ## Resolution
   What fixed it (rollback / hotfix / config change), with the exact command or action.

   ## Follow-ups
   - [ ] <concrete action> - #<issue number>
   ```

7. **File every follow-up as a real issue** linked from the postmortem, with the severity noted. Unlinked follow-up text is where action items die.

## Done criteria

- [ ] Alert timestamp, the log or error evidence that identified the cause, and the exact rollback or fix action are recorded
- [ ] Recovery held for 10+ minutes (monitor graph or error-rate screenshot attached)
- [ ] Auto-deploy state checked after any host rollback
- [ ] Postmortem written; every follow-up has an issue number

The postmortem and its linked issues are the deliverable, not a verbal summary.

## Common mistakes

- Debugging root cause for 30 minutes while users stay down, when a rollback was available.
- Rolling back in the host dashboard, then forgetting auto-deploy is now off - the fix merges but never ships.
- Rolling back on the host without reverting the branch, so the next unrelated deploy reintroduces the bug.
- Declaring resolved on one green check.
- Skipping the postmortem for S2/S3 incidents, which are the cheapest to learn from.

## Stop conditions

- Root cause involves a database migration or data mutation: stop all further database changes and confirm a recent restorable backup exists ([[backup-verify]]) before touching anything.
- The rollback fails, or the last known-good deploy is unclear: stop and escalate to the designated incident lead rather than guessing.
- Suspected security incident (auth bypass, data exposure): handle it as a security incident, preserve logs, and do not publish details until the scope is known.
