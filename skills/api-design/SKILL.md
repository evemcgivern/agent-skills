---
name: api-design
description: REST conventions for Next.js App Router route handlers — resource naming, versioning, pagination, a standard error envelope, Zod request/response validation, status-code discipline, OpenAPI generation, and API-response scrubbing (no PII/internal IDs/tokens). Use when asked to "design an API route," "add a new endpoint," "review this route handler," or "generate API docs."
---

# API Design (Next.js Route Handlers)

## Overview
Covers REST design for `app/api/**/route.ts` handlers in a web application. Adapt the examples to one repository’s conventions and keep error shapes, validation, and status-code handling consistent. Folds in prior general REST guidance (resource naming, HTTP verbs, pagination) but is scoped specifically to the Next.js App Router + Zod + Prisma/Supabase stack actually in use, not GraphQL or framework-agnostic design.

## Workflow

1. **Resource naming.** Plural nouns, nested for ownership: `/api/campaigns/[campaignId]/npcs`, `/api/users/[userId]/courses`. No verbs in paths (`/api/campaigns/create` is wrong — that's what `POST /api/campaigns` is for). Query params for filtering/sorting, never for identifying a specific resource (`/api/campaigns?id=123` should be `/api/campaigns/123`).

2. **Versioning strategy.** Default to no version prefix until a breaking change is actually needed (YAGNI) — when one is needed, prefix the path (`/api/v2/campaigns`) rather than a header, since it's more visible in logs, Render request metrics, and Better Stack traces. Keep `v1` (unprefixed or `/api/v1/`) alive alongside `v2` for a defined deprecation window; never silently break `v1` consumers, especially where third-party integrations may exist.

3. **Pagination.** Cursor-based by default for anything that can grow unbounded (campaign lists, course content, activity feeds) — `?cursor=<opaque>&limit=20`, response includes `nextCursor: string | null`. Offset-based (`?page=1&limit=20`) is acceptable only for small, bounded, rarely-changing collections where "jump to page 5" is a real user need (e.g., an admin table). Cap `limit` server-side (e.g., max 100) regardless of what the client requests — an unbounded limit is a denial-of-service surface against your own database.

4. **Standard error envelope.** Every error response uses the same shape so client code has one parsing path:
   ```json
   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "campaignId must be a valid UUID",
       "details": { "field": "campaignId" }
     }
   }
   ```
   `code` is a stable machine-readable string (`VALIDATION_ERROR`, `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `RATE_LIMITED`, `INTERNAL_ERROR`) — client code branches on `code`, never on `message` (message is for humans/logs and can change wording without breaking clients). Never include stack traces, raw Prisma/Postgres errors, or internal file paths in `details` — that's exactly the leak `privacy-audit` greps for.

5. **Zod validation on both sides.** Request body/query/params validated with a Zod schema at the top of the handler before any DB call — reject early with `VALIDATION_ERROR` and Zod's `.flatten()` field errors mapped into `details`. Response shape also defined as a Zod schema (even if not runtime-validated on every response in production for performance, it should exist as the documented contract and can be asserted in tests) — this schema doubles as the OpenAPI source (step 7) and as the single place that defines what leaves the server, which is what step 8's scrubbing check is verified against.

6. **Status-code discipline:**
   - `200` OK (successful GET/PUT/PATCH), `201` Created (successful POST creating a resource, include `Location` header or the created resource), `204` No Content (successful DELETE, no body).
   - `400` Bad Request (validation failure — malformed input), `401` Unauthorized (no/invalid session — NextAuth v5 session check failed), `403` Forbidden (valid session, insufficient permission — role check failed), `404` Not Found (resource doesn't exist *or* the caller isn't allowed to know it exists — don't leak existence via a 403 vs. 404 distinction for resources scoped to other users' data), `409` Conflict (e.g., duplicate resource, optimistic-lock version mismatch), `422` Unprocessable Entity (well-formed but semantically invalid, if you want to distinguish from 400 — optional, `400` is fine if the codebase doesn't already use 422), `429` Too Many Requests (rate limit — required on auth endpoints and any paid-API-calling endpoint per house security rules), `500` Internal Server Error (never expose the underlying cause in the body).
   - Role check (`403`) happens on **every** protected endpoint, not just the ones that "look sensitive" — this is a house OWASP-basics requirement, not optional.

7. **OpenAPI generation.** Derive the OpenAPI spec from the Zod schemas (e.g., `zod-to-openapi` or equivalent) rather than hand-writing YAML that drifts from the actual validation — the Zod schema is the source of truth, the spec is generated output. Regenerate as part of the route-handler PR, not as a separate later task, so it never falls out of sync. Check whether the repository already has an API documentation generator before adding a duplicate.

8. **API-response scrubbing.** Before returning any Prisma/Supabase query result, check it against the response Zod schema from step 5 — anything not in that schema should be excluded via `select`/`omit` at the query level, not filtered after the fact (filtering after fetch means the sensitive field still passed through application memory and log-adjacent tooling unnecessarily). Specifically scrub: password hashes, BYOK API keys, internal Stripe customer IDs unless the client legitimately needs them, other users' data in list endpoints, raw error objects. This is the same check `privacy-audit` runs independently — treat this step as the design-time version of that audit-time check.

## Checklist
- [ ] Resource paths are plural nouns, nested for ownership, no verbs
- [ ] Versioning approach stated (unprefixed until a breaking change forces `/v2/`)
- [ ] Pagination is cursor-based for unbounded collections, with a server-enforced `limit` cap
- [ ] Errors use the standard envelope with a stable `code`, no internal detail leakage
- [ ] Zod schemas validate request input and define the response contract
- [ ] Status codes follow the discipline above; role check present on every protected route
- [ ] OpenAPI spec generated from Zod schemas, not hand-maintained separately
- [ ] Response payload scrubbed via `select`/`omit` at the query level, checked against the response schema

## Output
The route handler code, its Zod schemas, and (if requested) the generated OpenAPI fragment. For a review task, a findings list keyed to file:line against this checklist.

## Stop Conditions
- A route returns a full Prisma model without `select`/`omit` and the model contains a sensitive field (password hash, API key, other users' data) → flag as a blocking finding, not a style note.
- An endpoint lacks a role/permission check that a sibling endpoint in the same resource has → treat as a likely authorization gap, not an inconsistency to shrug off.
- A paid-API-calling or auth endpoint has no rate limiting → flag per the house pre-launch requirement; don't ship without it.
