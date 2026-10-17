---
name: service-debugging
description: "Turn a live production symptom into a ranked, falsifiable cause: check the failure catalog, correlate recent changes, pull evidence for the top hypothesis, and record the result. Use when a deployed service misbehaves — 500s, timeouts, a blank page, a 404 on a page that exists, a silent no-op, a stuck queue, wrong data, or an error cluster spiking — when the same failure keeps recurring, or when asked to 'debug prod', 'find the root cause', or diagnose an incident rather than triage it."
---

# Service Debugging

## Overview

Production systems fail the same handful of ways over and over. The expensive part of debugging is not reading logs — it is knowing which of the five things this particular system does wrong is happening right now. That knowledge lives in a **failure catalog**, and consulting it is the first move, not the last.

**Core principle: a debugging pass ends with a ranked cause and the evidence that would falsify it.** Raw log excerpts and a list of things worth checking are the *input* to that, never the deliverable.

## When to use

- A live production symptom needs a cause (not just mitigation — for mitigation-first triage use an incident-response skill, if installed)
- An error-tracking cluster needs triage
- A failure has recurred and "we fixed that" apparently didn't
- A feature is deployed and green but demonstrably not working

**When NOT to use:**
- Site is down right now and nobody has rolled back yet → incident response (an incident-response skill, if installed) first, diagnose after
- A deploy you just shipped looks broken → roll back with a deploy or rollback skill, if installed (for example `deploy` from the [stylusnexus marketplace](https://github.com/stylusnexus/agent-plugins)); don't diagnose a live outage
- A bug reproducible on your machine → a local systematic-debugging skill, if installed
- You can't get a reliable signal at all → build a fast pass/fail feedback loop first (for example `debug-feedback-loop` from the [stylusnexus marketplace](https://github.com/stylusnexus/agent-plugins))

## The output contract

Every run produces exactly these four parts, in this order:

1. **Symptom** — one sentence. Observable, with a timestamp and blast radius ("all users" / "one tenant" / "1 in ~40 requests").
2. **Ranked causes** — one to three, most likely first. Each carries:
   - the *mechanism* (what specifically happens, not a category)
   - the evidence supporting it
   - the single check that would **rule it out**
3. **Verification links** — deep links to the exact log query, trace, dashboard panel, deploy, or `file:line` a human can open. Not "check the logs."
4. **Verdict** — `CONFIRMED` (evidence is dispositive) or `UNCONFIRMED` (best hypothesis), plus the next action.

A cause with no falsifying check is a guess wearing a lab coat. Write the check.

## Procedure

**1. Consult the failure catalog first.** Before reading a single log line, check whether this system has a catalog of named failure modes it has already exhibited — a mistake catalog in the instructions file, a postmortem directory, past incident issues. Match the symptom against it. If the catalog names this failure, you are done in two minutes instead of forty.

If no catalog exists, note that gap — step 6 starts one.

**2. Establish the change.** Almost every incident correlates with a change. In order: recent deploys, config/env/flag changes, migrations applied, upstream provider status, traffic shape. A symptom that starts at a timestamp with no correlating change is itself strong evidence (points at load, data growth, expiry, or a scheduled job).

**3. Classify the symptom** against the first-look table below.

**4. Pull evidence for the top candidate only.** Fanning out across every observability surface produces volume, not answers. Take the leading hypothesis, find the one query that confirms or kills it, run that.

**5. Rank and falsify.** Order surviving causes by evidence, not by how interesting they are. For each, state what would disprove it. If the top two are indistinguishable on current evidence, say so and name the discriminating check.

**6. Feed the catalog back.** A confirmed cause becomes a named entry — symptom, mechanism, fix, and the check that identifies it next time. This is the step that makes the next incident cheap, and it is the one that always gets skipped. A catalog nobody adds to decays into folklore.

## Symptom → first look

| Symptom | Look here first |
|---|---|
| Blanket 5xx starting at a timestamp | The deploy or config change at that timestamp |
| 404 on a page that exists in the repo | Routing rewrites — middleware, locale prefixes, host redirects |
| Works locally, dead in prod | Env var missing/different, build-time vs runtime config, flag default ≠ prod value |
| Silent no-op — no error, nothing happens | Swallowed exception, an early return before the write, a guard failing closed, an unseeded parent in a nested update |
| Deployed, green, but the feature does nothing | Nothing ever exercised the real write path; or the component exists but no route renders it |
| Intermittent, or only some users | Caching layer, per-tenant row, row-level permission scoping, stale client bundle |
| Slow, then timeouts under load | N+1 query, unbounded scan, missing index, connection-pool exhaustion |
| Queue stuck or jobs retried forever | At-least-once delivery meeting a non-idempotent handler, or a fail-closed gate |
| Wrong data, no error at all | Partially-applied migration, a default overwriting a real value, a write race |
| Upstream API errors in bursts | Rate limit or quota, not an outage — check response headers before blaming the vendor |

## Common mistakes

| Mistake | Why it costs you |
|---|---|
| Reading logs before checking recent deploys | The deploy timestamp answers in 30 seconds what log-reading answers in 30 minutes |
| Reporting raw log excerpts as the finding | Volume isn't diagnosis. Excerpts are evidence *for* a stated cause |
| Fixing the first plausible cause | Plausible ≠ confirmed. Run the falsifying check before touching code |
| Treating a monitor alert as ground truth | Confirm the symptom independently; flaky health checks page for nothing |
| Skipping step 6 | Every skipped catalog entry is a full re-diagnosis next time |
| Debugging a live outage instead of mitigating | Roll back, *then* diagnose. Use an incident-response skill, if installed |

## Stop conditions

- **Cause implicates data loss or a destructive migration** — stop before any further mutation; confirm a backup exists and restores (for example `backup-verify` from the [stylusnexus marketplace](https://github.com/stylusnexus/agent-plugins)) first.
- **Cause looks like a security issue** (auth bypass, data exposure, leaked credential) — stop, preserve logs, escalate. Do not "just fix it" quietly.
- **Two fixes for the same symptom have already failed** — the model of the system is wrong. Stop patching and re-derive from step 1.
- **Evidence contradicts the documented behavior** — surface the contradiction; do not silently reconcile it.
