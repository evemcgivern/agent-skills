---
name: db-migration-safety
description: Write or review Prisma and Supabase database migrations safely using the expand-contract pattern, idempotent SQL, and batched backfills. Use when adding/changing columns or tables, writing a migration PR, or reviewing one before merge — especially against Neon Postgres or Supabase in production.
---

# DB Migration Safety

## Overview

The two failure modes this guards against: a migration that locks a large table for the duration of a deploy (site goes down), and a migration that succeeds but corrupts or loses data because it wasn't idempotent or wasn't backed up. Neither is recoverable by "just re-running the migration" — the first needs the expand-contract pattern, the second needs a MANDATORY backup confirmation before anything touches production.

## The expand-contract pattern

Never do add-column + backfill + make-required in one migration against a live table with real traffic. Split into phases, each independently deployable:

1. **Expand** — add the new column/table as *nullable* or with a default, additive only. Old code keeps working unmodified.
2. **Backfill** — populate the new column for existing rows, in batches (see below), running alongside live traffic.
3. **Migrate reads/writes** — deploy application code that writes to (and eventually reads from) the new shape. Both old and new columns may coexist briefly.
4. **Contract** — once all app instances are on the new code path and backfill is confirmed complete, drop the old column / add the `NOT NULL` constraint / drop the old table.

Each phase is its own migration and its own deploy. Collapsing steps 1 and 4 into one migration is the single most common cause of an avoidable outage.

## Workflow

1. **Classify the migration** before writing it:
   - Additive (new nullable column, new table, new index `CONCURRENTLY`) → generally safe, low risk.
   - Constraint-adding (`NOT NULL`, `UNIQUE`, FK) → needs expand-contract, do last, after backfill confirmed.
   - Destructive (`DROP COLUMN`, `DROP TABLE`, type change) → needs expand-contract *and* a deprecation window (keep the old column at least one deploy cycle after the last read of it is removed from code).

2. **Avoid long table locks:**
   - Prisma: `ALTER TABLE ... ADD COLUMN` with a default on Postgres 11+ is fast (no full rewrite) as long as the default isn't a volatile expression — safe by default in most Prisma migrations.
   - Indexes: always `CREATE INDEX CONCURRENTLY` for existing tables with real data — Prisma's default migration won't do this automatically, hand-edit the generated SQL:
     ```sql
     -- CreateIndex
     CREATE INDEX CONCURRENTLY IF NOT EXISTS "idx_subscription_customer_id" ON "Subscription"("customerId");
     ```
     Note: `CONCURRENTLY` cannot run inside a transaction — Prisma migrations run in a transaction by default, so this needs a manually-applied migration marked as such (`prisma migrate resolve --applied` after running the SQL directly, or a `prisma.config` migration marked non-transactional if using the newer driver adapters).

3. **Batch backfills** — never a single `UPDATE` touching the whole table:
   ```sql
   -- Backfill in batches of 1000, sleeping isn't needed on Neon/Supabase managed Postgres
   -- but keep batch size small enough that each statement is sub-second.
   UPDATE "User" SET "normalizedEmail" = LOWER("email")
   WHERE id IN (
     SELECT id FROM "User" WHERE "normalizedEmail" IS NULL LIMIT 1000
   );
   -- repeat until 0 rows affected
   ```
   For large tables, drive this from a script (Node/Prisma or a `uv`-run Python script) with a loop and a small delay between batches, logging progress so it's resumable if interrupted.

4. **Idempotent SQL always** — every migration must be safely re-runnable:
   ```sql
   CREATE TABLE IF NOT EXISTS "WebhookEvent" (...);
   ALTER TABLE "Subscription" ADD COLUMN IF NOT EXISTS "trialEndsAt" TIMESTAMP;
   DROP TABLE IF EXISTS "LegacyBilling";
   CREATE INDEX CONCURRENTLY IF NOT EXISTS ...;
   ```
   Supabase migrations especially — the CLI can partially apply and re-run, so `IF NOT EXISTS` / `IF EXISTS` guards are not optional.

5. **MANDATORY pre-flight backup confirmation** before any migration touches production data (this is a hard gate, not a suggestion):
   - Neon: confirm a recent branch snapshot exists, or create one — `neon branches create --parent main --name pre-migration-<date>`.
   - Supabase: confirm the scheduled backup ran in the last 24h, or trigger a manual one via dashboard/CLI.
   - Neither available: run `pg_dump` manually and confirm the file is non-empty before proceeding.
   - See [[backup-verify]] for the full drill, including an actual restore test — don't just check a backup *exists*, know it *restores*.

6. **Run in staging/branch first** — Neon and Supabase both support branching; apply the migration to a branch, run the app's test suite and a manual smoke check against it, before applying to production.

## Migration PR review checklist

- [ ] Backup confirmed within the last 24h (link to the snapshot/backup evidence)
- [ ] Migration is idempotent (`IF NOT EXISTS`/`IF EXISTS` on every DDL statement)
- [ ] No `NOT NULL`/`UNIQUE`/FK constraint added in the same migration as the column that needs backfilling
- [ ] Any new index on an existing table uses `CONCURRENTLY` (and migration is marked non-transactional if needed)
- [ ] Backfill (if any) is batched, not a single table-wide statement
- [ ] Destructive statements (`DROP COLUMN`/`DROP TABLE`) are in a separate, later migration than the code that stops using that column
- [ ] Tested against a Neon/Supabase branch, not applied straight to prod
- [ ] Rollback plan stated in the PR description (down migration, or "expand-only, no rollback needed")

## Output / Evidence

Show the user: the classification (additive/constraint/destructive), the backup confirmation (snapshot ID + timestamp), the branch test result, and — for backfills — row counts before/after and how long the batched run took.

## Stop Conditions

- No backup confirmed within 24h — stop, do not proceed, surface this before any mutation ([[backup-verify]]).
- A single migration combines add-constraint with the column's initial creation on a table with existing rows — stop and split it.
- Migration touches auth/billing tables (`User`, `Customer`, `Subscription`) — escalate to a second pair of eyes (the user or a second reviewer) regardless of how small the change looks.
