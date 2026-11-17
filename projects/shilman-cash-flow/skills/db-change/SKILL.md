---
name: db-change
description: Use before changing anything in Cash Flow's Supabase layer or financial calculations - migrations, tables, columns, RLS policies, triggers, RPCs, Edge Functions, or the mirrored logic in src/lib/finance.ts.
---

# Supabase and financial logic changes

There is one Supabase project (`fzwxcaidvaweczxwvljk`) and it is production.
There is no staging database. Every applied migration touches real user money data.

## 1. Propose before touching anything

Before writing or applying SQL, explain to the user:

- What changes: tables, columns, policies, triggers, RPCs.
- What happens to existing rows (defaults, backfill, nullability).
- Which derived values move: `budgets.actual_amount`, `balance`, `carryover_amount`,
  `yearly_summaries`, goal progress.
- Whether RLS or user isolation is affected.
- The rollback SQL.

Wait for explicit approval. Changes to RLS, dropped columns or tables, and changes to
core financial rules always need approval, even when the request sounds like it covers them.

## 2. Write the migration

- File: `supabase/migrations/YYYYMMDDHHMMSS_short_snake_description.sql`.
- Start with a comment explaining why the change exists, not only what it does.
- Prefer idempotent, additive SQL (`ADD COLUMN IF NOT EXISTS`, defaults that preserve
  existing rows). Document column semantics with `COMMENT ON`.
- New domain table: `user_id` column, `ENABLE ROW LEVEL SECURITY`, and policies that
  scope select/insert/update/delete to `auth.uid() = user_id`. Client queries still add
  `.eq('user_id', user.id)`.
- Categories are soft-deleted (`is_active`, `deleted_at`). Never hard-delete rows that
  transactions reference.

## 3. Keep financial logic in one place

Derived values are owned by Postgres (triggers and RPCs such as `recalculate_forward`,
`recalculate_balance`, `recalculate_yearly_summary`). `src/lib/finance.ts` mirrors some of
them for display, for example `computeBudgetChain` and `getPlanEditMonths` document
`recalculate_budget_chain` and `set_category_plan`.

If a rule changes, update the DB implementation and the mirror together. Tests for
`finance.ts` live in `src/__tests__/finance.test.ts`. `calculateInvestmentStats` is not
covered there because it no longer matches `Investments.tsx`. A change to mirrored logic
updates or adds tests with concrete numbers, including edge cases (zero, negative, month
boundaries, read-only months outside the 3-month edit window).

Budget model (`20260912120000_budget_plans_v2.sql`): `planned_amount` is only the plan
(NULL = no plan), `carryover_amount` is the previous month's balance when both months have a
plan, and the chain never recalculates months before `budget_window_start()`. Plans and
modes change only through `set_category_plan` and `set_budget_mode`.

A new write path that triggers DB-side recalculation must dispatch the matching refresh
event (`transactions-changed`, `recurring-transactions-changed`) so the UI refetches.

## 4. Apply (only after approval)

The Supabase CLI is not installed. SQL runs through the Management API. The token is in
the macOS Keychain (`supabase-management-token`). Read it inline so it is never printed:

```bash
curl -s -X POST https://api.supabase.com/v1/projects/fzwxcaidvaweczxwvljk/database/query \
  -H "Authorization: Bearer $(security find-generic-password -s supabase-management-token -w)" \
  -H "Content-Type: application/json" \
  --data @/path/to/query.json
```

Never echo the token or write it into a file, a commit or a migration. If the Keychain
item is missing, ask the user.

Apply exactly the SQL in the committed migration file, not an edited variant.

## 5. After applying

- Check the result with a read query (column exists, policy listed, sample values correct).
- Regenerate `src/integrations/supabase/types.ts` if the schema changed:
  `GET https://api.supabase.com/v1/projects/fzwxcaidvaweczxwvljk/types/typescript`.
- Run `npm run typecheck` and `npm run test`.
- `npm run test:db` exercises RPCs and RLS against production with test accounts.
  Suggest it after schema or RLS changes, and run it only when the user agrees.

## Edge Functions

Code lives in `supabase/functions/<name>/`, JWT settings in `supabase/config.toml`.
Changing `verify_jwt` is a security change and needs approval. Deploying a function needs
the Supabase CLI (`npx supabase functions deploy <name>`), which is also a production
change: confirm with the user first.

## Frontend deploy order

If the frontend depends on the new schema: apply the migration first, then deploy the
frontend with the `deploy` skill. The reverse order breaks production for live users.
