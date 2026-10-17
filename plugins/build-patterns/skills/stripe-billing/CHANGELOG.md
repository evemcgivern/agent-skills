# Changelog: stripe-billing

## 0.2.0 — 2026-10-17

- Rewrite the description with trigger phrases.
- Read `current_period_end` from subscription items on API `2025-03-31.basil`+.
- Use `subscription_data.metadata` and `subscription_data.trial_period_days`.
- Record the event id in the same transaction as the write.
- Handle `invoice.paid` and out-of-order events; list all subscription statuses.
- Add a failure-then-resend test, pass/fail criteria, and Common mistakes.

## 0.1.0 — 2026-10-17

- Include the reviewed public version of `stripe-billing`.
- Generalize personal and project-specific references.
