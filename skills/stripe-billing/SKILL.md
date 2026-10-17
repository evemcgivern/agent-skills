---
name: stripe-billing
description: Implement or review Stripe subscription billing for a Next.js App Router product (Checkout, customer portal, webhook handler, plan changes, trials, dunning). Use when adding subscriptions or paywalls to a product or service, when reviewing existing billing code for correctness, or when a webhook/proration/trial bug is reported.
---

# Stripe Billing

## Overview

Stripe is the billing system of record for pricing decisions (what plan, what price, what trial), but the **local Prisma tables are the source of truth for authorization** inside the app — populated and kept in sync exclusively via webhooks, never written to directly from a Checkout redirect or client callback. This split is the most common source of billing bugs: a user pays, gets redirected back, sees "still on free plan" because the app trusted the redirect instead of waiting for the `checkout.session.completed` webhook.

Applies to products with paid tiers. Payment forms, Elements embeds, and one-off charges are out of scope unless the product also has a subscription track.

## Workflow

1. **Confirm the data model** exists before writing routes. Minimum Prisma shape:
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
   Store Stripe's `status` string as-is (`trialing`, `active`, `past_due`, `canceled`, `unpaid`) — don't invent a parallel enum that can drift out of sync with Stripe's.

2. **Checkout Session route** (`app/api/billing/checkout/route.ts`): create with `mode: 'subscription'`, pass `client_reference_id` = internal user id, and `metadata` on the subscription (not just the session) so webhooks can resolve the user without a second lookup.

3. **Customer portal route** (`app/api/billing/portal/route.ts`): look up `stripeCustomerId` from Prisma, never accept it from the client. Configure the portal's allowed actions (plan switch, cancel, update payment method) in the Stripe Dashboard, not in code.

4. **Webhook handler** (`app/api/webhooks/stripe/route.ts`) — this is the part that must be correct:
   - Verify signature with the raw body (Next.js route handlers need `req.text()`, not `req.json()`, before verification):
     ```ts
     const sig = req.headers.get('stripe-signature')!;
     const rawBody = await req.text();
     const event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET!);
     ```
   - Idempotency: record processed `event.id` in a small `WebhookEvent` table (unique constraint) and skip if already seen — Stripe retries on non-2xx and can also double-send.
   - Handle at minimum: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`, `invoice.payment_succeeded`.
   - Every handler writes to Prisma inside a transaction; return `200` only after the write commits. Return non-2xx on any failure so Stripe retries.

5. **Plan changes & proration**: use `stripe.subscriptions.update` with `proration_behavior: 'create_prorations'` (default) for upgrades, `'none'` for same-price seat changes. Let Stripe compute proration — do not hand-roll partial-period math.

6. **Trials**: set `trial_period_days` on the Checkout Session or `trial_end` on the subscription directly. Handle `customer.subscription.trial_will_end` (fires 3 days out) to trigger an in-app or email nudge — this is the dunning surface most teams forget.

7. **Dunning**: rely on Stripe's Smart Retries (Dashboard setting) for `invoice.payment_failed`; the app's job is to reflect `past_due` status (soft-lock features, show a banner) and reflect `canceled` after Stripe exhausts retries — don't build a custom retry scheduler.

## Testing checklist (Stripe CLI + test clocks)

- [ ] `stripe listen --forward-to localhost:3000/api/webhooks/stripe` running during dev
- [ ] `stripe trigger checkout.session.completed` — subscription row created in Prisma
- [ ] `stripe trigger customer.subscription.updated` — status/priceId updated
- [ ] `stripe trigger invoice.payment_failed` — app shows past_due state
- [ ] Replay the same event twice (`stripe events resend <id>`) — no duplicate writes, confirms idempotency
- [ ] Test clock: create a customer on a test clock, advance past trial end, confirm `trial_will_end` then `active`/`payment_failed` fire in order
- [ ] Portal cancel-at-period-end: confirm `cancelAtPeriodEnd` flips true, access persists until `currentPeriodEnd`

## Output / Evidence

Report to the user: which webhook events are handled (and which are deliberately not), the idempotency mechanism used, and the CLI trigger output showing each handled event landing in Prisma (row before/after). If reviewing existing code, flag any place that trusts client-supplied Stripe IDs or writes subscription state outside the webhook handler.

## Stop Conditions

- No `STRIPE_WEBHOOK_SECRET` configured for the environment being tested — stop, don't fake signature verification.
- Any code path that grants access before a webhook confirms payment — flag as a security/business-logic bug, don't silently patch without telling the user (it may be intentional optimistic UI that needs a corresponding revoke path).
- Live-mode keys detected in a test run — stop immediately, this is a real-money risk.
