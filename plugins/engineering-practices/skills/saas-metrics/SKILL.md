---
name: saas-metrics
description: Compute and report MRR, churn, activation, and retention for a small SaaS product from Stripe and PostHog data, with metric definitions a small team can maintain, starter Stripe and HogQL snippets, a monthly business-review template, and warnings about common miscounts (trials, refunds, currency, proration). Use when asked for "a business review", "our MRR", "churn numbers", "activation rate", "retention cohort", or to set up recurring metrics reporting.
---

# SaaS Metrics

## Overview

The goal is metrics a small team can compute correctly and re-derive monthly without a dedicated analyst — which means favoring simple, auditable definitions over textbook-perfect ones, and being explicit about the edge cases (trials, refunds, currency, proration) that silently distort MRR if ignored. Stripe is the source of truth for revenue figures; PostHog is the source of truth for product usage/activation/retention.

## Metric definitions

- **MRR (Monthly Recurring Revenue)**: sum of the monthly-normalized recurring amount across all *active* (or `past_due`, still counted until formally churned) subscriptions. Annual plans divide by 12. Explicitly **exclude**: one-time charges, setup fees, trialing subscriptions (they have no committed revenue yet), and canceled subscriptions past their period end.
- **Churn (revenue)**: MRR lost from downgrades + cancellations in the period, as a percentage of starting MRR. Report **gross churn** (ignores expansion) and optionally **net churn** (gross churn minus expansion/upgrade revenue) — state which one is being reported, they tell different stories and get confused constantly.
- **Churn (logo/customer)**: count of paying customers who canceled ÷ paying customers at period start. Distinct from revenue churn — a small customer canceling moves logo churn a lot more than revenue churn.
- **Activation**: user completes a defined "aha" action within N days of signup (product-specific — e.g., `project_created` within 7 days for a project-management tool). Pick one event, document why, don't redefine it every quarter.
- **Retention**: percentage of a signup cohort still active (performing the activation-adjacent event, or still subscribed) at 30/60/90 days.

## Stripe MRR calculation

Pull active and past-due subscriptions and normalize to monthly:

```ts
// compute-mrr.ts — a starting point; assumes one currency and flat per-unit prices
const MONTHS_PER_UNIT = { day: 12 / 365, week: 12 / 52, month: 1, year: 12 };
let mrr = 0;
// Auto-pagination: iterates every page, not just the first 100
for await (const sub of stripe.subscriptions.list({ status: 'all', limit: 100 })) {
  if (sub.status !== 'active' && sub.status !== 'past_due') continue;
  for (const item of sub.items.data) {
    const recurring = item.price.recurring;
    if (!recurring || item.price.unit_amount == null) continue; // tiered/metered prices need their own logic
    const amount = item.price.unit_amount * (item.quantity ?? 1);
    const months = MONTHS_PER_UNIT[recurring.interval] * recurring.interval_count;
    mrr += amount / months;
  }
}
console.log(`MRR: ${(mrr / 100).toFixed(2)}`); // amounts are in the currency's minor unit (cents for USD)
```

Don't silently under-count by only reading the first page — use the SDK's auto-pagination (as above) or `starting_after`. The snippet ignores discounts and coupons; subtract them if they are material, and say so in the report.

## PostHog HogQL: activation & retention

```sql
-- Activation: % of people who signed up 7-30 days ago (so each has had the full
-- 7 days) who fired the activation event within 7 days of signing up
SELECT
  countIf(activated) * 100.0 / count() AS activation_rate
FROM (
  SELECT
    person_id,
    minIf(timestamp, event = 'user_signed_up') AS signup_at,
    minIf(timestamp, event = 'project_created') AS activation_at,  -- your activation event
    (countIf(event = 'project_created') > 0 AND activation_at <= signup_at + INTERVAL 7 DAY) AS activated
  FROM events
  WHERE timestamp > now() - INTERVAL 30 DAY
  GROUP BY person_id
  HAVING countIf(event = 'user_signed_up') > 0  -- minIf returns 1970-01-01, not NULL, when nothing matches
    AND signup_at <= now() - INTERVAL 7 DAY      -- skip signups younger than the 7-day window
)
```

```sql
-- 30-day retention: people who signed up 35-42 days ago (so days 25-35 after
-- signup are over for all of them); retained = fired ANY core event in days 25-35
SELECT
  countIf(core_hits > 0) * 100.0 / count() AS retention_30d
FROM (
  SELECT
    c.person_id,
    countIf(e.timestamp >= c.signup_at + INTERVAL 25 DAY
        AND e.timestamp <  c.signup_at + INTERVAL 35 DAY) AS core_hits
  FROM (
    SELECT person_id, min(timestamp) AS signup_at
    FROM events
    WHERE event = 'user_signed_up'
    GROUP BY person_id
    HAVING signup_at BETWEEN now() - INTERVAL 42 DAY AND now() - INTERVAL 35 DAY
  ) AS c
  LEFT JOIN (
    SELECT person_id, timestamp
    FROM events
    WHERE event IN ('project_created', 'project_viewed', 'task_completed')  -- your core events
      AND timestamp > now() - INTERVAL 42 DAY
  ) AS e ON e.person_id = c.person_id
  GROUP BY c.person_id
)
```
Prefer PostHog's built-in Retention insight in the UI for anything beyond a quick check — hand-rolled HogQL cohort logic is easy to get subtly wrong (off-by-one on interval boundaries); use these snippets as a starting point to verify the UI insight, not as the sole source.

## Common miscounts to guard against

- **Trials counted as MRR** — a `trialing` subscription has committed to nothing yet; including it inflates MRR and creates a nasty "MRR drop" the month trials convert or lapse. Exclude until `active`.
- **Refunds not backed out** — a refund on this month's payment should reduce the reported revenue for the period it was refunded in (or the original period, pick one convention and state it) — Stripe's `charge.refunded` events need to feed into whatever revenue-reporting path is used, not just MRR-from-subscriptions.
- **Currency mixing** — if any customers are billed in a currency other than the primary reporting currency, normalize using a consistent (e.g., month-start) FX rate before summing — don't sum raw amounts across currencies as if they were the same unit.
- **Proration double-counting** — a mid-cycle upgrade creates a one-time proration invoice item *and* changes the ongoing subscription amount; MRR calculated from `subscriptions.list` already reflects the new steady-state amount — don't additionally add the one-time proration charge into MRR, that's a one-time revenue event, not recurring.
- **Annual plans reported at face value** — always divide by 12 for MRR; reporting the full annual charge in the month it lands makes that month look like a huge (fake) growth spike.
- **Canceled-but-not-yet-ended subscriptions** — `cancel_at_period_end: true` subscriptions are still `active` and still paying until the period ends; don't drop them from MRR early, but do flag them separately as "committed churn" for the next period's forecast.

## Monthly business-review template

```markdown
# Business Review — <Month Year>

## Revenue
- MRR: $X (prior month: $Y, change: Z%)
- Gross churn: X% | Net churn: X%
- New MRR added: $X | Expansion MRR: $X | Churned MRR: $X

## Product
- New signups: X
- Activation rate (7-day): X%
- 30-day retention: X%

## Notable
- <Any one-off distortions this month: big annual renewal, a refund, a pricing change — call these out explicitly so the trend line doesn't look misleading later>

## Actions
- [ ] <follow-up items>
```

## Output / Evidence

Show the user the raw numbers with their source (Stripe API response / PostHog query result), not just final percentages — enough to spot-check by hand. Flag any of the "common miscounts" that applied this period (a refund, a trial conversion, an annual renewal) so the reported trend isn't misread.

## Stop Conditions

- Stripe and PostHog paying-customer counts disagree by a wide margin — stop and reconcile (likely a gap in the Stripe webhook sync to the app database or PostHog) before reporting numbers that might be wrong.
- A metric definition is being changed from a prior report (e.g., activation event redefined) — flag this explicitly rather than silently producing a number that isn't comparable to last month's.
