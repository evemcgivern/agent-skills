# Background Jobs

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Designs scheduled and background work on Render: when to use a cron job and when to use a long-running worker, how to make jobs idempotent, how to claim jobs from a Postgres queue table, retries with backoff, timeout budgets, catch-up after missed runs, and heartbeat monitoring so a failed job raises an alert instead of failing silently. Use it when asked to set up a cron job, build a background worker, or find out why a nightly job failed without anyone noticing.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
