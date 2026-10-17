---
name: background-jobs
description: Design cron jobs and background workers on Render — cron job versus long-running worker, idempotency, Postgres job claiming with advisory or row locks, retries with backoff, timeout budgets, catch-up after downtime, and heartbeat monitoring so silent failures surface. Use when asked to "set up a cron job", "build a background worker", "why did the nightly job silently fail", "make this job idempotent", or when designing any scheduled or async task.
---

# Background Jobs (Render)

## Overview
Render offers two shapes for non-request-driven work: **Cron Jobs** (scheduled, run-to-completion, billed per second of run time with a small monthly minimum per cron job) and **Background Workers** (long-running services, always-on, poll a queue or run a loop). Picking the wrong shape is the first mistake this skill prevents; silent failure is the second — a cron job that fails at 3am and nobody notices until a customer complains is worse than no job at all.

## Choosing Cron Job vs. Worker

- **Render Cron Job**: task runs on a schedule, finishes, exits. Use for: nightly data rollups, digest emails, cleanup sweeps, periodic external API syncs. Billed only for execution time — cheaper for infrequent tasks. Render runs at most one instance of a cron job at a time (a late run delays the next one) and stops any run after 12 hours.
- **Render Background Worker**: a service that stays running, typically polling a queue (e.g., a Postgres table used as a job queue, or a message broker) or holding a persistent connection (webhook listener, websocket relay). Use for: anything that needs sub-minute latency, or genuinely continuous processing (not just "runs often") — 24/7 billing applies regardless of how busy it is.
- Rule of thumb: if the task can tolerate the schedule's granularity (hourly/daily) and finishes in minutes, it's a cron job. If it needs to react within seconds of an event, it's a worker (or better, a webhook-driven route handler, if it fits inside a request timeout).

## Workflow

1. **Design for idempotency first.** Every job must be safe to run twice with the same inputs — your own retry logic re-runs work, a crash mid-run leaves partial effects, and manual re-triggers happen. Concretely: use `INSERT ... ON CONFLICT DO NOTHING/UPDATE` instead of bare `INSERT`, check-then-act patterns replaced with atomic upserts, and any "send an email" step made safe to repeat. A database transaction cannot undo an email that already left, so checking and setting `sent_at` in the same transaction as the send still double-sends if the job crashes after the send and before the commit. Instead, pass the provider an idempotency key derived from the job (for example `welcome-email/<user_id>`) where the provider supports one, and/or write an outbox row before sending and send from that row, marking it sent afterwards. Queues and cron retries deliver at least once, so every handler must tolerate running again on the same input.

2. **Job claiming for workers pulling from a shared queue table:** use Postgres advisory locks (`pg_try_advisory_lock`) or row-level locking (`SELECT ... FOR UPDATE SKIP LOCKED`) to claim a row — `SKIP LOCKED` is the right default for a multi-worker queue since it lets concurrent workers grab different rows without blocking each other. Never claim by reading a row then updating its status in a separate query — that's a race condition between the read and the claim; do it as one statement that picks exactly one row:

   ```sql
   UPDATE jobs SET status = 'running', claimed_at = now()
   WHERE id = (
     SELECT id FROM jobs
     WHERE status = 'pending'
     ORDER BY created_at
     LIMIT 1
     FOR UPDATE SKIP LOCKED
   )
   RETURNING *;
   ```

   A bare `UPDATE jobs ... WHERE status = 'pending' RETURNING *` claims every pending row at once.

3. **Retries with backoff.** Check the platform's docs for what happens to a failed cron run, and don't rely on platform retries: make retries the job's own responsibility. Transient failures (network blip, rate limit from a third-party API) get retried; permanent failures (malformed data, a 4xx from a well-formed request) don't — retrying those just wastes the retry budget and delays the alert. Exponential backoff (e.g., 1min → 5min → 15min, capped, max 3–5 attempts) rather than fixed-interval retry; track attempt count on the job row so retries don't loop forever on a truly broken input — after max attempts, mark as `failed` and alert, don't silently drop it.

4. **Timeout budgets.** Every job needs an explicit max-duration expectation, checked against Render's limits for the service (cron runs are stopped after 12 hours). A job that occasionally runs long (e.g., an AI-generation batch job with variable model latency) needs either a hard timeout with partial-progress checkpointing (resume from where it stopped) or a job-size cap (batch size limited so worst-case duration stays bounded) — don't let an unbounded job silently eat the next scheduled run's window.

5. **Catch-up after downtime.** If Render itself has downtime or a deploy causes a missed cron run, decide up front: does the next run need to "catch up" on the missed window (process everything since the last successful run, using a `last_run_at` watermark) or is a missed run acceptable to skip (e.g., a "daily digest" that's fine to just skip once)? Watermark-based catch-up (store `last_processed_at`, process `WHERE updated_at > last_processed_at` on every run) handles both missed-run and normal-run cases with the same code path — prefer it over special-casing "did we miss a run."

6. **Heartbeat monitoring** — the core defense against silent failure:
   - Every job emits a heartbeat event at start and completion (success or failure) — to Better Stack (via a heartbeat/dead-man's-switch check) and/or a PostHog event (`job_completed` with `status`, `duration_ms`, `rows_processed` properties).
   - Set up a Better Stack heartbeat monitor per scheduled job with an expected-interval alert — if the job doesn't check in within its expected window (schedule interval + reasonable buffer), that's the alert, not waiting for a customer to notice missing data.
   - On failure, the job should emit the heartbeat with `status: failed` and the error reason before exiting — a job that crashes without emitting anything is indistinguishable from a job that never ran, which is exactly the silent-failure case this exists to prevent.

## Checklist
- [ ] Cron Job vs. Worker choice justified by latency/duration needs, not habit
- [ ] Idempotency verified — safe to run twice with same inputs (upserts, gated sends, no read-then-act races)
- [ ] Job claiming uses `FOR UPDATE SKIP LOCKED` or advisory locks for any multi-worker queue
- [ ] Retry logic distinguishes transient vs. permanent failures, with capped exponential backoff
- [ ] Timeout budget explicit; long-running jobs checkpoint or cap batch size
- [ ] Catch-up strategy decided (watermark-based resume vs. acceptable-to-skip) and implemented
- [ ] Heartbeat emitted on start/success/failure to Better Stack and/or PostHog, with an alert configured for missed check-ins

## Output
The job implementation plus a one-paragraph runbook note: schedule, expected duration, what the heartbeat alert means if it fires, and manual re-trigger instructions.

## Stop Conditions
- The job writes to a production database and there's no idempotency guarantee → do not ship it; a retried non-idempotent job (duplicate charges, duplicate emails) is a customer-facing incident waiting to happen.
- No heartbeat/alerting exists for a job handling money, billing, or customer-facing data → treat this as a blocker, not a nice-to-have, before calling the job done.
- The job needs to run a migration or bulk `UPDATE`/`DELETE` against production data → confirm a recent backup exists first, and the change has been reviewed for safety.
