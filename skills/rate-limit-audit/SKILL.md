---
name: rate-limit-audit
description: Pre-launch gate that inventories every endpoint calling a paid API (LLM, email, SMS) and every auth endpoint, verifies a rate limiter exists, and actually tests it with scripted burst requests to confirm 429s fire. Use before launching a new product/feature, after adding an LLM-calling or auth route, or when asked to check rate limiting.
---

# Rate Limit Audit

## Overview

A rate limiter that's configured but never tested is a rate limiter that might not actually work — wrong key extraction, wrong window, or a middleware ordering bug can all silently no-op it. This skill's job is proving the limit fires, not just confirming code that looks like a limiter exists. Required pre-launch on any endpoint that calls a paid API (Anthropic/Vercel AI SDK, email, SMS) and on all auth endpoints (login, password reset, OTP, signup) — per the house security rules.

## Workflow

1. **Inventory every endpoint in scope** — grep the App Router for candidates:
   ```bash
   # Paid-API-calling routes
   grep -rl "anthropic\|generateText\|streamText\|@ai-sdk" app/api
   grep -rl "sendEmail\|resend\|sendgrid\|nodemailer" app/api
   grep -rl "twilio\|sendSms" app/api

   # Auth-adjacent routes
   grep -rl "signIn\|signUp\|reset-password\|verify-otp\|magic-link" app/api
   ```
   Build a table: route path, category (LLM / email / SMS / auth), current limiter (none / found), limiter library used.

2. **Recommend defaults per endpoint class** (starting points — tune to actual cost/abuse profile):

   | Class | Suggested limit | Key |
   |---|---|---|
   | LLM chat/completion endpoint | 20 req / 10 min per user | user id (fallback IP if anonymous) |
   | LLM endpoint, anonymous/free tier | 5 req / 10 min | IP |
   | Email send (transactional) | 10 / hour per recipient | recipient email + IP |
   | Email send (bulk/invite) | 5 / hour per sender | user id |
   | SMS/OTP send | 3 / 10 min, 10 / day | phone number |
   | Login attempt | 5 / 15 min | IP + email combo (lock the pair, not just the IP) |
   | Password reset request | 3 / hour | email (return same response regardless of match) |
   | Signup | 10 / hour | IP |

3. **Verify implementation** — for Next.js on Render (no built-in edge rate-limit infra like Vercel's), the common pattern is a Postgres- or Redis-backed limiter:
   ```ts
   // lib/rate-limit.ts — sliding window over Postgres, no extra infra needed
   export async function checkRateLimit(key: string, limit: number, windowSeconds: number) {
     const windowStart = new Date(Date.now() - windowSeconds * 1000);
     const count = await prisma.rateLimitHit.count({
       where: { key, createdAt: { gte: windowStart } },
     });
     if (count >= limit) return { allowed: false, retryAfter: windowSeconds };
     await prisma.rateLimitHit.create({ data: { key } });
     return { allowed: true };
   }
   ```
   In the route handler:
   ```ts
   const { allowed, retryAfter } = await checkRateLimit(`llm:${userId}`, 20, 600);
   if (!allowed) {
     return new Response('Too many requests', { status: 429, headers: { 'Retry-After': String(retryAfter) } });
   }
   ```
   If Redis (Upstash) is already in the stack for a given project, prefer it over the Postgres table for lower latency — but don't add a new Redis dependency solely for rate limiting on a low-traffic route.

4. **Actually test it with burst requests** — this is the non-negotiable step:
   ```bash
   # Fire 25 requests in quick succession against a limit of 20/10min
   for i in $(seq 1 25); do
     curl -s -o /dev/null -w "%{http_code}\n" -X POST https://staging.example.com/api/chat \
       -H "Authorization: Bearer $TEST_TOKEN" -H "Content-Type: application/json" \
       -d '{"message":"test"}'
   done | sort | uniq -c
   ```
   Expected output: ~20 lines of `200`, ~5 lines of `429`. If all 25 return `200`, the limiter is not working — investigate before shipping, don't assume the code is correct because it compiles.

5. **Test the auth-lockout case specifically** — brute-force a login endpoint with a wrong password 6+ times, confirm the 6th+ attempt returns 429 (or an account-lock message) rather than a normal "wrong password" 401 indistinguishable from the first attempt.

6. **Document the limits** in a short reference (README section or `docs/rate-limits.md`) so future endpoints get added consistently rather than each developer picking arbitrary numbers.

## Checklist

- [ ] Every LLM-calling route inventoried and has a limiter
- [ ] Every email/SMS-sending route inventoried and has a limiter
- [ ] Every auth route (login, signup, reset, OTP) inventoried and has a limiter
- [ ] Each limiter's key includes the right dimension (user/IP/email/phone — not just IP alone for account-specific abuse)
- [ ] Burst test run against at least the highest-risk endpoint (LLM chat, login) with captured 429 evidence
- [ ] `Retry-After` header present on 429 responses
- [ ] Limits documented somewhere durable, not just in code comments

## Output / Evidence

Show the user the inventory table (route / class / limiter present / tested), and the raw burst-test output (`uniq -c` counts of status codes) for at least the two highest-risk routes. A limiter claimed without a burst-test result attached should be treated as unverified.

## Stop Conditions

- Any paid-API or auth endpoint has zero rate limiting and the task is a pre-launch gate — stop, this blocks launch, don't just note it as a finding and move on.
- Burst test shows the limiter not firing (all requests succeed past the stated limit) — stop and fix before marking the audit passed.
- Rate limit keyed only on IP for an authenticated endpoint where multiple legitimate users share an IP (office NAT, mobile carrier) — flag as likely to cause false-positive lockouts, recommend combining with user id.
