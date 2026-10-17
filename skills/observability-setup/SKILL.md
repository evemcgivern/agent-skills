---
name: observability-setup
description: Wire a service for observability sized for a small team — Better Stack uptime checks and log drains from Render, error tracking, PostHog product analytics, Render health-check endpoints, and alert thresholds tuned so two humans aren't paged into the ground. Use when launching a new service, adding monitoring to an existing one, or when alert fatigue is a complaint.
---

# Observability Setup

## Overview

The design constraint here is not "monitor everything" — it's "page on what a human must act on right now, ticket everything else." A small team that gets paged for every warning-level log line will start ignoring pages, which defeats the entire point. This skill wires the stack (Better Stack, Render, PostHog, error tracking) with that filter built in from the start.

## Workflow

1. **Render health-check endpoint** — every service needs one, cheap and dependency-light:
   ```ts
   // app/api/health/route.ts
   export async function GET() {
     try {
       await prisma.$queryRaw`SELECT 1`; // confirms DB connectivity, not full app health
       return Response.json({ status: 'ok', timestamp: new Date().toISOString() });
     } catch {
       return Response.json({ status: 'error' }, { status: 503 });
     }
   }
   ```
   Point Render's health check config at this path so a bad deploy that can't reach the DB fails the health check and Render won't route traffic to it — this alone prevents a class of incidents.

2. **Better Stack uptime checks** — one check per public-facing service, hitting `/api/health` (or the homepage for a marketing site) at a 1–3 minute interval. Configure:
   - Escalation: page immediately on 3 consecutive failures (avoids paging on a single transient blip), not on the first failure.
   - Maintenance windows around planned deploys if deploys are known to cause a brief blip.

3. **Log drain from Render to Better Stack** — set up Render's log stream to forward to Better Stack so logs survive past Render's own retention window and are searchable/alertable in one place:
   - In Render dashboard: Service → Logs → add a log stream destination pointing at Better Stack's log ingestion endpoint.
   - Structure app logs as JSON where practical (`{ level, message, ...context }`) so Better Stack's log-based alerts can match on `level: "error"` rather than fragile string matching.

4. **Error tracking (Sentry)** — capture unhandled exceptions and, deliberately, a curated set of *handled* errors that indicate real problems (e.g., a webhook signature failure, a payment processing exception) even though the code catches them gracefully:
   ```ts
   import * as Sentry from '@sentry/nextjs';
   try {
     await processPayment(input);
   } catch (err) {
     Sentry.captureException(err, { tags: { area: 'billing' } });
     return new Response('Payment processing failed', { status: 500 });
   }
   ```
   Tag by area (`billing`, `auth`, `llm`) so alert rules and triage ([[incident-response]]) can filter fast.

5. **PostHog product analytics** — wire event capture per [[analytics-instrumentation]]; for observability specifically, PostHog's error tracking / session replay can supplement Sentry for understanding *user-facing* impact (what was the user doing when it broke), while Sentry stays the source of truth for the exception itself.

6. **LLM cost tracking** — for any product calling the Anthropic API (product AI features), tag PostHog events with token counts and estimated cost per call so a cost spike is visible in the same dashboard as everything else, not buried in an Anthropic console only checked monthly.

## Alert threshold design (the "don't page into the ground" part)

| Signal | Action | Rationale |
|---|---|---|
| Health check fails 3x consecutive | **Page** | Real, actionable, user-facing |
| 5xx rate > 5% over 5 min | **Page** | Broad impact, likely a bad deploy |
| Single Sentry exception, low frequency | **Ticket** (daily digest), not page | Individually low-impact; batch review |
| Sentry exception spikes (10x baseline in 10 min) | **Page** | Rate-of-change signals something just broke |
| Dead-letter webhook row created | **Ticket**, page only if count > threshold in an hour | One dead letter is a data point, a burst is an incident |
| Disk/memory approaching limit on Render | **Ticket** with lead time (e.g., at 80%), **page** at 95% | Gives time to act before it's an outage |
| LLM cost per day exceeds budget threshold | **Ticket** (business signal), not page | Not an outage, but needs eyes soon |

Review this table together with the user and response team when setting up a new service — thresholds should reflect actual traffic/cost baselines, not generic defaults copy-pasted without checking.

## Output / Evidence

Show: the `/api/health` endpoint response, the Better Stack check configuration (URL, interval, escalation policy), the Render log drain confirmed flowing (a test log line appearing in Better Stack), and the alert-threshold table reviewed and agreed for this service. For an existing service being audited, report what's missing against this list.

## Stop Conditions

- No health-check endpoint exists and the task is launching a new service — treat as a blocker, not optional polish.
- Proposed alert configuration would page on every warning-level log line or every individual exception — flag this as alert-fatigue risk before wiring it, propose the digest/ticket alternative instead.
- Log drain or error tracking would capture secrets/PII in captured payloads (e.g., full request body logged on error including auth tokens) — stop and scrub before enabling, per the "secrets out of logs" house rule.
