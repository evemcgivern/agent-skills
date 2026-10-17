---
name: stripe-billing
description: Implement or review Stripe subscription billing in a Next.js App Router app — Checkout Sessions, customer portal, signed and idempotent webhook handler, plan changes and proration, trials, and dunning. Use when asked to "add subscriptions", "add a paywall", "review our billing code", or when a user "paid but is still on free", or a webhook, proration, or trial bug is reported.
---

# Stripe Billing

## Overview

Stripe is the system of record for prices, plans, and trials. The app's own database is the source of truth for **access**, and only the webhook handler writes to it. Never grant access from the Checkout success redirect: the classic bug is "I paid but I'm still on free" because the app trusted the redirect instead of waiting for the webhook.

Covers subscriptions. One-off payments and Elements forms are out of scope unless the product also sells subscriptions.

## Workflow

1. **Data model first.** Minimum Prisma shape:
   ```prisma
   model Customer {
     id               String   @id @default(cuid())
     userId           String   @unique
     stripeCustomerId String   @unique
     user             User     @relation(fields: [userId], references: [id])
   }

   model Subscription {
     id                   String   @id @default(cuid())
     customerId           String
     stripeSubscriptionId String   @unique
     status               String   // mirrors Stripe's status enum verbatim
     priceId              String
     currentPeriodEnd     DateTime
     cancelAtPeriodEnd    Boolean  @default(false)
     updatedAt            DateTime @updatedAt
     customer             Customer @relation(fields: [customerId], references: [id])
   }
   ```
   Store Stripe's `status` string as-is: `incomplete`, `incomplete_expired`, `trialing`, `active`, `past_due`, `canceled`, `unpaid`, `paused`. Do not invent a parallel enum.
   On API version `2025-03-31.basil` or later, `current_period_end` is no longer on the Subscription; read it from `subscription.items.data[i].current_period_end`. Pin the API version in the Stripe client so a dashboard upgrade cannot silently turn it into `undefined`.

2. **Checkout Session route** (`app/api/billing/checkout/route.ts`): `mode: 'subscription'`, `client_reference_id` = internal user id, and `subscription_data.metadata.userId` so subscription events can find the user without a second lookup. Reuse the stored `stripeCustomerId` as `customer` when one exists, so each user has one Stripe customer.

3. **Customer portal route** (`app/api/billing/portal/route.ts`): read `stripeCustomerId` from the database for the signed-in user; never accept it from the client. Configure allowed actions (switch plan, cancel, update card) in the Dashboard portal settings.

4. **Webhook handler** (`app/api/webhooks/stripe/route.ts`), in this order:
   1. Verify the signature against the raw body. Use `req.text()`, not `req.json()`:
      ```ts
      const sig = req.headers.get('stripe-signature')!;
      const rawBody = await req.text();
      const event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET!);
      ```
      On the Edge runtime use `await stripe.webhooks.constructEventAsync(...)`. Return `400` if verification throws.
   2. In **one database transaction**: insert `event.id` into a `WebhookEvent` table with a unique constraint, then apply the state change. If the insert hits the unique constraint, return `200` and stop. Recording the id outside the transaction loses events: a failed write marks the event as seen, and Stripe's retry is skipped.
   3. Return `200` only after commit; return `5xx` on any failure so Stripe retries.
   - Handle at minimum: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`.
   - Stripe does not guarantee event order. For subscription events, re-fetch the subscription with `stripe.subscriptions.retrieve(id)` and write its current state, rather than applying each event's payload as a delta.

5. **Plan changes and proration.** Call `stripe.subscriptions.update` on the existing subscription item with the new price. `proration_behavior: 'create_prorations'` (the default) adds prorations to the next invoice; `'always_invoice'` bills them now; `'none'` skips them. Let Stripe compute proration.

6. **Trials.** Set `subscription_data.trial_period_days` on the Checkout Session, or `trial_end` on the subscription. Handle `customer.subscription.trial_will_end` (sent three days before the trial ends) to trigger a reminder.

7. **Dunning.** Turn on Smart Retries in the Dashboard. The app shows `past_due` (banner, soft-lock) and then whatever final state the Dashboard setting chooses after retries fail (`canceled`, `unpaid`, or still `past_due`). Do not build a custom retry scheduler.

## Testing checklist (Stripe CLI + test clocks)

- [ ] `stripe listen --forward-to localhost:3000/api/webhooks/stripe` running; its `whsec_` secret set as `STRIPE_WEBHOOK_SECRET`
- [ ] `stripe trigger checkout.session.completed` creates the subscription row
- [ ] `stripe trigger customer.subscription.updated` updates status and price
- [ ] `stripe trigger invoice.payment_failed` shows the past-due state
- [ ] `stripe events resend <id>` on an already-processed event writes nothing new
- [ ] A handler forced to throw returns 5xx, and the resend then succeeds (proves the id is not recorded on failure)
- [ ] Test clock: advance past trial end; `trial_will_end` then `invoice.paid` or `invoice.payment_failed` arrive and the row matches Stripe
- [ ] Portal cancel: `cancelAtPeriodEnd` becomes true and access lasts until `currentPeriodEnd`

## Pass / fail

- **Pass:** every box above checked with before/after rows captured; access is granted only by webhook-written rows.
- **Fail:** access granted from the redirect or client; any client-supplied Stripe ID trusted; a duplicate or retried event changes data twice or is lost.

## Common mistakes

- Parsing JSON before verifying the signature, so the raw bytes no longer match.
- Reading `subscription.current_period_end` on a `basil`-or-later API version.
- Applying out-of-order events as deltas, so an old `updated` overwrites a newer state.
- Only putting `metadata` on the Checkout Session, where subscription events cannot see it.
- Using the Dashboard endpoint secret locally instead of the one `stripe listen` prints.

## Output / Evidence

Which events are handled (and which are deliberately not), the idempotency mechanism, and the CLI output showing each handled event landing in the database (row before/after). For a review, flag every place that trusts client-supplied Stripe IDs or writes subscription state outside the webhook handler.

## Stop Conditions

- No `STRIPE_WEBHOOK_SECRET` for the environment under test: stop; do not fake signature verification.
- Access granted before a webhook confirms payment: flag as a business-logic bug and tell the user before patching; it may be intentional optimistic UI that needs a revoke path.
- Live-mode keys (`sk_live_`) in a test run: stop immediately; real money is at risk.
