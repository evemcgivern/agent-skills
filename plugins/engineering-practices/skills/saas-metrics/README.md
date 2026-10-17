# SaaS Metrics

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: full](https://img.shields.io/badge/Claude-full-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-full-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)

Computes and reports MRR, revenue and logo churn, activation, and retention for a small SaaS product from Stripe and PostHog data. It gives simple metric definitions a small team can re-derive every month, a starter Stripe MRR script and HogQL queries, a monthly business-review template, and a list of common miscounts such as trials, refunds, currency mixing, proration, and annual plans. Use it when asked for a business review, MRR or churn numbers, an activation rate, a retention cohort, or recurring metrics reporting.

## What it looks like

Example output, invented data. The monthly review follows the skill's template, with the month's distortions called out so the trend is not misread later:

```markdown
# Business Review — March 2026

## Revenue
- MRR: $18,420 (prior month: $17,150, change: 7.4%)
- Gross churn: 4.4% | Net churn: 2.2%
- New MRR added: $1,640 | Expansion MRR: $390 | Churned MRR: $760

## Product
- New signups: 312
- Activation rate (7-day): 41%
- 30-day retention: 27%

## Notable
- One annual plan renewed ($2,400), counted as $200 of MRR, not $2,400
- Two trials converted; they enter MRR this month, not before
- One refund ($49) backed out of March revenue

## Actions
- [ ] Reconcile Stripe and PostHog paying-customer counts (off by 3)
```

The common miscounts the skill checks for each month:

| Miscount | Correct handling |
|---|---|
| Trials counted as MRR | Leave out until the subscription is `active` |
| Annual plan at face value | Divide by 12 |
| Proration charge added to MRR | One-time revenue, not recurring |
| Cancel-at-period-end dropped early | Keep in MRR; flag as next month's committed churn |

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
