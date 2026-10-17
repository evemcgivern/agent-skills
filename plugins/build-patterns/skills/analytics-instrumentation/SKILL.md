---
name: analytics-instrumentation
description: PostHog event taxonomy and instrumentation review - object_verb naming, flat property schemas, identify/reset/group calls, PII exclusion, LLM usage events, a starter dashboard set (activation, retention, feature funnel), and a per-feature checklist. Use when instrumenting a new feature, auditing existing PostHog events, or setting up analytics for a new product, e.g. "add tracking", "what events should we fire", "review our PostHog events", "is there PII in analytics".
---

# Analytics Instrumentation

## Overview

The usual failure is not "we didn't track it". It is "we tracked it inconsistently": three naming styles mean every dashboard needs a translation layer, and PII slips into event properties because nobody reviewed the payload. Fix the naming up front and make the PII check a standing item.

## Naming convention: `object_verb`

Lowercase snake_case, object first, past-tense verb, so related events sort together:

```
project_created
project_deleted
project_shared
subscription_started
subscription_upgraded
subscription_canceled
llm_query_submitted
llm_query_failed
```

Avoid: verb-first names (`created_project`), intent-free names (`button_clicked` - name the outcome, e.g. `project_export_clicked`), and versioned event names (`project_created_v2` - version a property instead).

## Workflow

1. **Identify the user** as soon as they are known (signup and every login), before feature flag evaluation or conversion events. `identify()` links the earlier anonymous events to the person:
   ```ts
   posthog.identify(user.id, {   // stable internal ID, never the email
     email: user.email,          // person properties: the one place PII may go, if needed at all
     plan: user.plan,
     created_at: user.createdAt,
   });
   ```
   On logout call `posthog.reset()`, or the next user on the same device inherits this person and their groups.

2. **Group calls** for multi-user accounts, so usage and retention can be sliced by account:
   ```ts
   posthog.group('company', company.id, { name: company.name, member_count: company.memberCount });
   ```
   PostHog allows at most 5 group types per project, and an event can belong to only one group of each type. Pick group types deliberately.

3. **Event properties** - flat, consistently typed, minimal:
   ```ts
   posthog.capture('project_created', {
     project_id: project.id,
     template_used: project.templateId ?? null,
     source: 'dashboard_button', // where the action was triggered
   });
   ```
   **No PII in `capture()` properties**: no email, name, phone, address, IP, free-text user input, or raw form values. If PII is needed at all, it goes in person properties via `identify()`. Treat this as a hard rule and audit every new `capture()` call against it.

4. **LLM usage events.** Record cost and performance, not prompt or response content, unless there is an explicit, disclosed reason. PostHog's LLM analytics uses the `$ai_generation` event:
   ```ts
   posthog.capture('$ai_generation', {
     $ai_trace_id: traceId,
     $ai_model: response.model,      // take the model ID from the API response, don't hard-code it
     $ai_provider: 'anthropic',
     $ai_input_tokens: usage.input_tokens,
     $ai_output_tokens: usage.output_tokens,
     $ai_latency: latencySeconds,
     feature: 'project_assistant',   // custom properties are allowed alongside
   });
   ```
   PostHog's provider SDK wrappers send this event automatically; prefer them over hand-written capture where available, and check their privacy-mode setting so content is not stored.

5. **Starter dashboards** - build these first for any new product or major feature:
   - **Activation funnel:** signup -> first key action -> second key action within N days.
   - **Retention:** weekly or monthly cohorts keyed on the one event that best means "got value" (not login - login is a weak proxy).
   - **Feature funnel:** entry point -> intermediate steps -> completion event, to find friction inside one flow.

## Per-feature checklist (before calling a feature shipped)

- [ ] Success event named `object_verb`
- [ ] `_failed` event exists if the action can fail visibly
- [ ] Properties checked for PII: none in `capture()`
- [ ] Fires exactly once per action in a **production** build (React StrictMode double-runs effects in development only, so dev counts mislead)
- [ ] Logged-in user is identified before the event fires (not stuck on an anonymous ID)
- [ ] Event added to a funnel or dashboard

## Auditing existing instrumentation

1. Search all capture calls: `rg -n "posthog\.capture\(|\.capture\(\s*['\"]" --type ts --type js` (ripgrep's `ts` type includes `.tsx`; adjust for server SDKs and other languages).
2. Flag properties that look like PII (`email`, `name`, `phone`, `address`, `ip`) or that pass raw user input.
3. List event names not matching `^[a-z]+(_[a-z]+)+$` or not object-first. Propose renames with a migration note; renames break historical dashboards.
4. Confirm `identify()` runs on signup **and** login, and `reset()` on logout.
5. Pass: zero PII hits (show the search output), every event name conforms or has a rename plan, identify/reset both present.

## Done criteria

Show: the implemented taxonomy (event names and properties), a PostHog query or screenshot of the new events arriving with correct properties, and the PII search output showing it came back clean - not just an assertion.

## Common mistakes

- Using the email as the distinct ID; it changes, and it leaks into every event.
- Forgetting `reset()` on logout on shared devices.
- Hard-coding a model name in LLM events, which goes stale on the next model upgrade.
- Judging double-fires from dev-mode counts.
- Mass-renaming events without telling dashboard owners.

## Stop conditions

- PII already flowing into `capture()` properties in production: stop. It needs a fix plus a possible deletion of historical events; escalate to the project owner instead of only patching forward.
- The naming convention conflicts with many existing events: do not mass-rename unilaterally. Propose a migration plan, since it affects historical dashboards.
