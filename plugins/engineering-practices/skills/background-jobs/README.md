# Background Jobs

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Designs scheduled and background work on Render: when to use a cron job and when to use a long-running worker, how to make jobs idempotent, how to claim jobs from a Postgres queue table, retries with backoff, timeout budgets, catch-up after missed runs, and heartbeat monitoring so a failed job raises an alert instead of failing silently. Use it when asked to set up a cron job, build a background worker, or find out why a nightly job failed without anyone noticing.

## What it looks like

The life of one job pulled from a Postgres queue table. A worker claims exactly one row in a single statement, so two workers never take the same job. Only transient errors are retried, with a capped backoff; anything else, or a job that runs out of attempts, is marked `failed` and raises an alert instead of disappearing:

```mermaid
flowchart TD
    A[Job row: pending] --> B["Claim one row<br/>FOR UPDATE SKIP LOCKED"]
    B --> C[running]
    C -->|success| D[done + heartbeat]
    C -->|error| E{Transient?}
    E -->|no: bad data, 4xx| F[failed + alert]
    E -->|yes: network, rate limit| G{Attempts left?}
    G -->|yes| H[Back off: 1m, 5m, 15m] --> A
    G -->|no| F
```

Choosing the shape before writing any code:

| | Cron job | Background worker |
|---|---|---|
| Runs | On a schedule, then exits | All the time, polling a queue or holding a connection |
| Billed | Per second of run time | Around the clock, busy or idle |
| Fits | Nightly rollups, digest emails, cleanup sweeps | Work that must react within seconds |

Every job, either shape, sends a heartbeat when it starts and when it ends, including on failure. A missed check-in is the alert.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
