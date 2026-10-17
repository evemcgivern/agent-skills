---
name: api-design
description: REST conventions for Next.js App Router route handlers — resource naming, versioning, cursor pagination, one error envelope, Zod request/response validation, status-code rules, OpenAPI generated from Zod, and response scrubbing (no secrets, hashes, or other users' data). Use when asked to "design an API route", "add a new endpoint", "review this route handler", "fix our error responses", or "generate API docs".
---

# API Design (Next.js Route Handlers)

## Overview

REST design for `app/api/**/route.ts` handlers using Zod and Prisma or Supabase. Adapt the examples to the repository's existing conventions; consistency of error shape, validation, and status codes matters more than any single rule here. Not for GraphQL or tRPC.

## Workflow

1. **Resource naming.** Plural nouns, nested for ownership: `/api/projects/[projectId]/tasks`. No verbs in paths: `/api/projects/create` should be `POST /api/projects`. Query params filter and sort; they never identify one resource (`/api/projects?id=123` should be `/api/projects/123`).

2. **Versioning.** No version prefix until a breaking change forces one. Then prefix the path (`/api/v2/projects`) rather than using a header, because paths show up in every log and metrics tool. Keep v1 running for a stated deprecation window; never silently break v1 consumers.

3. **Pagination.** Cursor-based for anything that can grow without bound: `?cursor=<opaque>&limit=20`, response includes `nextCursor: string | null`. Offset (`?page=1&limit=20`) only for small, bounded collections where "jump to page 5" is a real need, such as an admin table. Cap `limit` on the server (for example, max 100) whatever the client sends.

4. **One error envelope.** Every error uses the same shape so clients have one parsing path:
   ```json
   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "projectId must be a valid UUID",
       "details": { "fieldErrors": { "projectId": ["Invalid UUID"] } }
     }
   }
   ```
   `code` is a stable string (`VALIDATION_ERROR`, `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `CONFLICT`, `RATE_LIMITED`, `INTERNAL_ERROR`). Clients branch on `code`, never on `message`. `details` never holds stack traces, raw database errors, or file paths. If the codebase already uses RFC 9457 problem details (`application/problem+json`), keep that instead.

5. **Zod on both sides.** Validate params, query, and body with `safeParse` at the top of the handler, before any database call. On failure return `400` with the field errors in `details`: in Zod 4 use `z.flattenError(result.error)` (the `.flatten()` method is deprecated); in Zod 3 use `result.error.flatten()`. Define the response shape as a Zod schema too. It is the documented contract, the OpenAPI source (step 7), and the list of fields allowed to leave the server (step 8). Assert it in tests even if you skip runtime checks in production.

6. **Status codes.**
   - `200` GET/PUT/PATCH success. `201` POST that creates, with a `Location` header or the created resource. `204` DELETE success, empty body.
   - `400` malformed or invalid input. `401` no valid session. `403` valid session, not allowed. `404` not found, *or* the caller may not know it exists; for resources scoped to other users, return 404 instead of 403 so existence does not leak. `409` duplicate or version conflict. `422` only if the codebase already separates semantic errors from 400. `429` rate limited, with `Retry-After`. `500` with no cause in the body.
   - Every protected endpoint checks permission, not only the ones that look sensitive.

7. **OpenAPI from Zod.** Generate the spec from the Zod schemas rather than hand-writing YAML that drifts. Options: `@asteasolutions/zod-to-openapi`, or Zod 4's built-in `z.toJSONSchema()` for the schema parts. Check whether the repo already has a generator before adding one. Regenerate in the same PR as the route change.

8. **Response scrubbing.** Exclude fields at the query with Prisma `select`/`omit` or an explicit Supabase column list, not by deleting keys after the fetch. Always exclude: password hashes, stored API keys and tokens, payment-provider customer IDs unless the client needs them, other users' rows in list endpoints, raw error objects. Then parse the result against the response schema from step 5.

## Checklist

- [ ] Paths are plural nouns, nested for ownership, no verbs
- [ ] Versioning stated (unprefixed until a breaking change forces `/v2/`)
- [ ] Unbounded collections use cursor pagination; server caps `limit`
- [ ] Every error uses the envelope with a stable `code` and no internal details
- [ ] Zod validates params, query, and body before any database call
- [ ] A Zod response schema exists and tests assert against it
- [ ] Status codes follow step 6; every protected route checks permission
- [ ] OpenAPI generated from Zod, regenerated in this PR
- [ ] Queries use `select`/`omit` matching the response schema

## Pass / fail

- **Pass:** every checklist item holds for every handler in scope.
- **Fail:** any handler returns a full model containing a sensitive field, skips input validation, leaks internals in an error body, or lacks a permission check.

## Common mistakes

- `findMany()` with no `select`, returned straight to the client.
- Unbounded `limit` taken from the query string.
- Returning `403` for another user's resource, which confirms it exists.
- `200` with `{ "error": ... }` in the body.
- Hand-edited OpenAPI YAML that no longer matches validation.

## Output

The handler code, its Zod schemas, and, if requested, the generated OpenAPI fragment. For a review, findings keyed to `file:line` against the checklist.

## Stop Conditions

- A route returns a full model with a sensitive field (password hash, API key, other users' data): blocking finding, not a style note.
- An endpoint lacks a permission check that a sibling endpoint on the same resource has: treat as a likely authorization gap.
- An auth endpoint or one that calls a paid API has no rate limit: blocking before launch (see the `rate-limit-audit` skill).
