# Cash Flow - Application Reference

This file used to hold a 1,161-line reference of the whole app: data model, every feature,
and the functions behind each one. It was written on 14 September 2026 and was never
updated again, so by 19 September it described an app that no longer existed: recurring
transactions, profile photos and the currency picker as live features, six Edge Functions
where two remain, 166 migrations where there are 191, a yearly_summaries table that no
longer exists, and the budget plans v2 change as still pending in production.

A reference nobody updates is worse than no reference: it is read as if it were true.

## Where the answers are now

| Question | Where to look |
|---|---|
| What rule does the app follow, and why | The Cash Flow Rulebook: https://claude.ai/artifact/KqtirYuEdgGr9X4di3AufV |
| What the schema is today | The live database, not `supabase/migrations/`. Read a function or trigger with `pg_get_functiondef`, never from the newest migration file that mentions it |
| What a screen does | The component in `src/`. The contexts in `src/contexts/` own the data, `src/lib/` the shared rules |
| How the budget chain works | `supabase/migrations/20260912120000_budget_plans_v2.sql`, plus the budget section of the Rulebook |
| Whether it still works | `npm run test` for the pure rules, `npm run test:db` for the database |

The old text is in git history: `git show 1a0f767:docs/APP_REFERENCE.md`.
