---
name: observability-setup
description: Wire a web service for observability sized for a small team - health-check endpoint, uptime checks, log forwarding, error tracking, product analytics, LLM cost tracking, and page-vs-ticket alert thresholds. Examples use Render, Better Stack, Sentry, and PostHog. Use when launching a new service, auditing monitoring on an existing one, or on "set up monitoring", "add a health check", "forward logs", "we get paged too much", or "alert fatigue".
---

# Observability Setup

## Overview

The goal is not "monitor everything". It is "page on what a human must act on now, ticket everything else". A small team paged for every warning starts ignoring pages. Build that filter in from the start.

Render, Better Stack, Sentry, and PostHog are the example stack. Map each step to the project's equivalent tool if it differs.

## Workflow

1. **Health-check endpoint.** Every service needs one, cheap and dependency-light:
   ```ts
   // app/api/health/route.ts (Next.js App Router; Prisma shown as the example DB client)
   export async function GET() {
     try {
       await prisma.$queryRaw`SELECT 1`; // confirms DB connectivity, not full app health
       return Response.json({ status: 'ok', timestamp: new Date().toISOString() });
     } catch {
       return Response.json({ status: 'error' }, { status: 503 });
     }
   }
   ```
   Set the host's health check path to it (Render: service **Settings > Health Check Path**). A new deploy that cannot reach the database then fails its check and does not receive traffic. Keep the check to the one dependency the service cannot run without; a slow third-party call here turns someone else's outage into yours.

2. **Uptime checks.** One monitor per public-facing service, hitting the health path (or the homepage for a static site) every 1-3 minutes. In Better Stack, set the monitor's **confirmation period** (Configure > Advanced settings) to at least one check interval so a single transient failure does not open an incident, and set a **recovery period** so a flapping service does not auto-resolve. Add maintenance windows around planned work known to cause a blip.

3. **Log forwarding.** Forward host logs to the log tool so they outlive the host's retention and can drive alerts:
   - Render: set a workspace default under **Integrations > Observability > Log Streams**, pointing at the log tool's ingestion endpoint. Override per service under the service's **Settings > Log Stream** if needed (some override options depend on the workspace plan).
   - Emit app logs as JSON (`{ level, message, ...context }`) so alerts match on `level: "error"` instead of fragile strings.
   - Pass: a test log line written by the app appears in the log tool within a few minutes.

4. **Error tracking.** Capture unhandled exceptions, plus a curated set of *handled* errors that signal real problems (webhook signature failures, payment exceptions):
   ```ts
   import * as Sentry from '@sentry/nextjs';
   try {
     await processPayment(input);
   } catch (err) {
     Sentry.captureException(err, { tags: { area: 'billing' } });
     return new Response('Payment processing failed', { status: 500 });
   }
   ```
   Tag by area (`billing`, `auth`, `llm`) so alert rules and triage ([[incident-response]]) can filter quickly.

5. **Product analytics.** Instrument events per [[analytics-instrumentation]]. Session replay helps show *what the user was doing* when something broke; the error tracker stays the source of truth for the exception itself.

6. **LLM cost tracking.** For features that call an LLM API, record model, input/output tokens, cost, and latency per call in the same analytics tool (PostHog's LLM analytics uses `$ai_generation` events for this). A cost spike should show up on a dashboard someone checks, not in a provider console reviewed monthly.

## Alert thresholds (page vs ticket)

| Signal | Action | Rationale |
|---|---|---|
| Uptime check fails past its confirmation period | **Page** | Real, user-facing |
| 5xx rate > 5% over 5 min | **Page** | Broad impact, likely a bad deploy |
| Single low-frequency exception | **Ticket** (daily digest) | Individually low impact |
| Exception rate 10x baseline within 10 min | **Page** | Something just broke |
| Dead-letter webhook row created | **Ticket**; page only above an hourly count | One is a data point, a burst is an incident |
| Disk/memory at 80% | **Ticket**; **page** at 95% | Lead time before an outage |
| Daily LLM cost over budget | **Ticket** | Business signal, not an outage |

These numbers are starting points. Replace them with values based on the service's real traffic and cost baseline, and agree them with whoever gets paged.

## Done criteria

- [ ] `GET /api/health` returns 200 with the DB up and 503 with it unreachable (both tested)
- [ ] Host health check path set; uptime monitor configured with URL, interval, confirmation period, and escalation target recorded
- [ ] Test log line visible in the log tool
- [ ] A deliberate test exception visible in the error tracker with its `area` tag
- [ ] Alert table filled in with this service's numbers and agreed

For an existing service, report each unchecked item as a gap.

## Common mistakes

- Health check that only returns 200 without touching the critical dependency - it stays green during the outage that matters.
- Health check that calls every downstream API - one vendor blip marks the service unhealthy.
- Paging on the first failed check instead of using a confirmation period.
- Plain-text logs, then alerts written as string matches that break on the next wording change.
- Copying the threshold table without replacing the numbers.

## Stop conditions

- Launching a new service with no health-check endpoint: treat it as a blocker, not polish.
- Proposed alerts page on every warning log line or every individual exception: flag the alert-fatigue risk and propose the digest/ticket route before wiring it.
- Logs or error events would capture secrets or PII (for example, full request bodies with auth tokens): stop and scrub before enabling. Secrets never go in logs.
