# Cash Flow - open work

Things found and deliberately **not** done, with enough context to pick up cold.

Two rules, learned from `APP_REFERENCE.md` next door - a reference nobody updated became
worse than no reference, because it was read as if it were true:

1. **An item leaves this file when it is done.** It is not marked done, struck through or
   moved to a "completed" section. If it is still written here, it is still open.
2. **Every item says what was actually measured or verified**, and says so when it was
   only reasoned from the code. A backlog of guesses wastes the time of whoever acts on it.

Last reviewed: 2026-11-03.

---

## Performance

### What the split did not cover

Route splitting landed on 2026-11-02 and took the initial JavaScript from **432 KB gzipped
to 241 KB** - 1,516 KB of raw JS down to 797 KB. recharts, papaparse and dnd-kit now arrive
only with the screens that use them. The item that used to sit here is therefore gone, per
the rule at the top of this file.

What is left is the eager graph itself, about 241 KB gzipped, and none of it is obviously
one screen's problem any more: it is React, Supabase, Radix, framer-motion, date-fns and
the dashboard. Two specific weights are still worth a look, both measured from the bundle's
sourcemap on 2026-10-29:

- **`@supabase/realtime-js`, 26.7 KB**, for a feature the app does not use. The realtime
  publication was dropped from every table and cross-context refresh runs on browser events
  instead. It arrives because `@supabase/supabase-js` bundles it. Removing it means
  constructing the client from the sub-packages rather than the umbrella one, so look at
  what `src/integrations/supabase/client.ts` would have to become before promising anything.
- **`zod`, 55.6 KB**, used in exactly one place: the planned-amount schema in
  `CategoryTransactionsModal.tsx`, which checks that a number is between 0 and 1,000,000.
  That is a few lines of hand-written validation. Note the precedent: `src/lib/schemas.ts`
  was deleted in September for being a shared validation layer nobody shared.

**Still unmeasured: what any of this costs in seconds.** The byte counts are facts; load
time depends on the connection and the phone's CPU, and no number should be quoted for it
until someone measures against a real device. A `web-perf` skill exists for this but is not
always offered in a session; Lighthouse against the deployed site does the same job.

---

## Test infrastructure

### Serve the built site to the e2e suite instead of the dev server

`workers: 2` is now pinned in `playwright.config.ts`, which makes the suite trustworthy,
and that was the urgent half. The underlying cause is still there: every browser shares one
Vite dev server, which compiles on demand, so more browsers make each page slower rather
than the run faster.

Building once and serving `dist/` statically would be faster per request and stable under
real parallelism. It also tests what actually ships. The cost is a build step before the
suite and a static server in `webServer`.

### Fixed waits still hiding in the specs

Four tests were converted this session from "wait 2.5 seconds, then assert" to "wait for
this to appear, up to 15 seconds". That shape is what made a screen still legitimately
loading report as broken. Others of the same shape are likely still there and simply have
not been unlucky yet. Worth a sweep for `waitForTimeout` followed by an assertion.

A suite that cries wolf is the real cost here: a run with six unexplained failures during
this session had to be repeated serially just to prove the product was fine, and the next
person may instead dismiss a genuine failure as "just a flake".

---

## Cleanup

- **`budgets.actual_amount` and `budgets.balance` are fetched and never read.** Verified
  across `src/`: both screens sum actuals from the transactions themselves and recompute
  the balance with `calculateBudgetBalance`, so the only derived column that reaches a
  screen is `carryover_amount`. The two are still maintained by database triggers. Before
  dropping them from the `select`, check the places this sweep did not cover -
  `test-runner.mjs`, the Rulebook, anything reading the table outside the app. Keeping them
  is cheap; the point is that nothing depends on them, which is also why trigger drift in
  those two columns cannot show a wrong figure on either screen.
- **Lint baseline: 61 errors, 24 warnings**, almost all `@typescript-eslint/no-explicit-any`.
  Nothing gates on it. Note that `no-unused-vars` is **off**, which is how a `useMemo` over
  the whole transaction list and the two constants it fed survived unread on the תזרים
  screen until they were found by hand.

---

## Decided - do not re-propose

Both of these look like bugs from the code. They are not.

- **Every date rule is on Asia/Jerusalem, and the account-creation floor joined them**
  (2026-11-03). `validate_transaction_date` and `validate_budget_edit` used to trunc
  `profiles.created_at`, a timestamptz, with a bare `date_trunc` - resolving in the session
  timezone, UTC on Supabase - while `budget_current_month` and `budget_window_start` beside
  them said Asia/Jerusalem. Both now say it, and `accountOpenedMonth` in finance.ts matches.
  An audit of the live schema that day found no other function deciding a calendar month on
  another clock: the remaining `now()` callers either say Asia/Jerusalem already or measure
  a duration rather than a month. The floor can only have moved one month later for accounts
  opened within two or three hours of a month boundary, never earlier, because Israel is
  never behind UTC.
- **Neither screen shows a month after the current one** (2026-11-03). It used to reach one
  month ahead, which meant a future month with no budget rows - and the only thing that
  created them was visiting the cash-flow screen on that month, so the same month showed a
  plan or no plan depending on where the user had been first. Planning is unaffected: a
  plan set on the current month already propagates forward through `set_category_plan`.
  `monthHasStarted` in Dashboard.tsx is consequently always true, and the branches on it are
  kept as guards rather than removed.

- **Carryover resets to 0 after a month with no budget rows** (decided 2026-10-20). A
  missed month is not evidence of saving: the user almost certainly did spend and simply
  did not record it, so carrying the old leftover forward invents money, and backfilling
  the missing months invents a great deal more - each one would hand back a full month's
  plan as leftover. The reset is also symmetric, which is what makes it coherent: someone
  who had overspent is not punished for it on return either.
- **The app addresses the reader in the masculine throughout** (changed 2026-10-29, chosen
  as the interim form). It was mixed before - thirteen strings in the feminine while the
  error translator behind them used the masculine, so one failed read could produce the
  same sentence spelled two ways. All of it now matches `src/lib/db-error.ts`. Past-tense
  forms are identical in both genders and were left alone, as were the impersonal
  phrasings. Reversing the choice is thirteen strings across ten files.
