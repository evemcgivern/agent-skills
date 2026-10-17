---
name: analytics-instrumentation
description: PostHog event taxonomy and instrumentation review for products — naming convention, property schemas, identify/group calls, PII exclusion, a starter dashboard set (activation, retention, funnel), and a per-feature instrumentation checklist. Use when instrumenting a new feature, reviewing existing PostHog events, or setting up analytics for a new product.
---

# Analytics Instrumentation

## Overview

The recurring failure mode with product analytics is not "we didn't track it," it's "we tracked it inconsistently" — three different naming conventions across features means every dashboard needs a translation layer, and PII quietly ends up in event properties because no one reviewed the payload. This skill fixes the naming convention up front and makes the PII check a standing item, not an afterthought.

## Naming convention: `object_verb`

Lowercase, snake_case, `object_verb` order (not `verb_object`) so events group alphabetically by the thing they're about:

```
campaign_created
campaign_deleted
campaign_shared
character_leveled_up
subscription_started
subscription_upgraded
subscription_canceled
llm_query_submitted
llm_query_failed
```

Avoid: `created_campaign` (verb-first scatters related events alphabetically), generic names like `button_clicked` (says nothing about intent — name the outcome, e.g. `campaign_export_clicked`), and per-page-variant event names (`campaign_created_v2`) — version the *property*, not the event name.

## Workflow

1. **Identify calls** — call `posthog.identify()` immediately on login/signup, before any other event fires for that session, so pre-login anonymous events get merged into the right person:
   ```ts
   posthog.identify(user.id, {
     email: user.email, // OK: PostHog identify properties can hold PII, it's designed for it and access-controlled
     plan: user.plan,
     created_at: user.createdAt,
   });
   ```

2. **Group calls** — for multi-user accounts/orgs (if a product has team/campaign-sharing features), use `posthog.group()` so retention/usage can be sliced by account, not just by individual user:
   ```ts
   posthog.group('campaign', campaignId, { name: campaign.name, member_count: campaign.members.length });
   ```

3. **Event property schema** — keep properties flat, typed consistently, and minimal:
   ```ts
   posthog.capture('campaign_created', {
     campaign_id: campaign.id,
     template_used: campaign.templateId ?? null,
     source: 'dashboard_button', // where the action was triggered from
   });
   ```
   **No PII in event properties** — no email, name, IP, free-text user input, or anything from a form field, in `capture()` calls. `identify()`/`group()` traits are the only place PII belongs (PostHog treats those with tighter access controls). This is a hard rule, not a style preference — audit every new `capture()` call against it.

4. **LLM-specific event properties** — for applications with AI features, capture cost and performance without capturing the prompt/response content itself unless there's an explicit, disclosed reason to:
   ```ts
   posthog.capture('llm_query_submitted', {
     feature: 'campaign_assistant',
     model: 'claude-sonnet-4-6',
     input_tokens: usage.inputTokens,
     output_tokens: usage.outputTokens,
     estimated_cost_usd: cost,
     latency_ms: latency,
   });
   ```

5. **Starter dashboard set** — build these three first for any new product/feature, they cover the most common business questions:
   - **Activation funnel**: signup → first key action (e.g., `campaign_created`) → second key action within N days. Shows where new users drop off.
   - **Retention**: cohort-based, weekly/monthly, keyed on the single event that best represents "used the product" (not login — login is a weak proxy for value received).
   - **Feature funnel** (per major feature): entry point → intermediate step → completion event, to find friction inside a specific flow (e.g., campaign creation wizard steps).

6. **Per-feature instrumentation checklist** (run this before calling any new feature "shipped"):
   - [ ] Primary success event named per `object_verb` convention
   - [ ] Failure/error variant event exists if the action can fail in a user-visible way (`_failed` suffix)
   - [ ] Properties reviewed for PII — none present in `capture()` calls
   - [ ] Event fires exactly once per logical action (check for double-fire on React re-renders/StrictMode)
   - [ ] `identify()` already called earlier in the session (event isn't stuck on an anonymous id if the user is logged in)
   - [ ] Event added to the relevant funnel/dashboard, not just fired into the void

## Review checklist for existing instrumentation

- [ ] Grep `posthog.capture(` calls for property names that look like PII (`email`, `name`, `phone`, `address`, `ip`, or raw user-input variables passed directly)
- [ ] Confirm event names follow `object_verb`, flag stragglers for a rename (with a migration note — renaming breaks historical dashboards, do it deliberately)
- [ ] Confirm `identify()` fires on both signup and login, not just signup
- [ ] Confirm no event fires from a client component without also checking it isn't double-mounted (common React 18 StrictMode dev bug that inflates counts in dev but not prod — verify by checking prod data, not just dev console)

## Output / Evidence

Show the user: the event taxonomy actually implemented (list of event names + properties), a PostHog screenshot or exported query showing the event flowing in with correct properties, and explicit confirmation no PII appears in `capture()` payloads (grep output showing the search came back clean, not just an assertion).

## Stop Conditions

- Found PII already flowing into `capture()` properties in production — stop, this needs a fix and potentially a PostHog data deletion request for historical events, escalate to the project owner rather than quietly patching going forward only.
- Naming convention conflict with a large number of existing events — don't do a mass rename unilaterally; propose the migration plan to the user since it affects historical dashboard continuity.
