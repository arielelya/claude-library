# CLAUDE.md

This file gives Claude Code the product and technical context needed to work effectively on the Shilman Finance Cash Flow application.

---

# Project Context

## What is Shilman Finance?

**Shilman Finance** is a personal-finance brand focused on making money management clear, practical, and approachable.

The broader mission is to help people understand their financial situation, manage their money better, and make more confident financial decisions without requiring accounting or finance expertise.

The main software product in this repository is:

# Cash Flow

Cash Flow is a **Hebrew, RTL, mobile-first personal finance and budgeting application**.

The product is designed for individuals and households who want a simple way to understand:

- how much money comes in,
- where money goes,
- whether they are staying within budget,
- how their month is progressing,
- whether they are moving toward savings goals,
- and how their overall financial position changes over time.

The product should make financial information easier to understand, not more intimidating.

---

# Product Philosophy

Cash Flow should feel:

- trustworthy,
- clear,
- calm,
- practical,
- modern,
- professional,
- financially credible,
- easy to understand.

The product is not intended to feel like:

- accounting software,
- an enterprise finance dashboard,
- a spreadsheet replacement for professionals,
- a trading platform,
- or an overly technical fintech product.

The user should be able to understand the state of their finances quickly.

Clarity is more important than showing every possible metric.

---

# Target User

The product is intended for regular people managing personal or household finances.

One account currently represents one household budget.

The typical user wants to:

- understand monthly income and expenses,
- plan spending,
- track actual spending,
- reduce financial uncertainty,
- create savings goals,
- monitor investments,
- and build better financial habits.

The user should not need financial expertise to use the application successfully.

---

# Current Product

The application currently runs at:

`shilmancashflow.com`

Current version shown in Settings:

```text
2.2.0
```

The app is entirely in **Hebrew** and uses **RTL** layout globally.

The application is organized around six primary areas:

| Route | Hebrew label | Purpose |
|---|---|---|
| `/dashboard` | דאשבורד | Monthly overview of income, expenses, net cash flow, recent activity, goals, investments and market indexes |
| `/budget` | תזרים | Monthly budget / expense management, planned vs actual, carryover, categories and transactions. Labelled תזרים because it carries income as well as expenses, and has to read true in tracking mode where nothing is planned |
| `/goals` | מטרות | Savings goals, milestones, progress and due-date awareness |
| `/investments` | השקעות | Investment portfolios and value history |
| `/annual-summary` | סיכום שנתי | Annual financial summary, monthly trends, categories and year-over-year comparison |
| `/settings` | הגדרות | User profile, operating mode, theme, password and account management |

Additional flows include:

- `/login`
- `/onboarding`
- `/reset-password`

---

# Two Operating Modes

Cash Flow supports two different ways of using the product.

## Budget Mode

Budget mode is for users who actively plan spending.

Each category has a monthly plan in `budgets.planned_amount`. `NULL` means no plan, `0` is a valid plan, and the plan never includes carryover.

For expense categories, leftover and overspend both roll over:

```text
carryover_amount = previous month's balance (when both months have a plan)
balance          = planned_amount + carryover_amount - actual_amount
```

A month without a plan, or a missing month, breaks the chain. Any change in a month recalculates every later month.

A plan edit goes through the `set_category_plan` RPC. It applies to the selected month and onward, stops at a past month without a plan, and always updates the months after the current month.

This mode is intended for active budgeting.

## Tracking Mode

Tracking mode is for users who mainly want visibility.

The planning layer is reduced and the product focuses on:

- actual income,
- actual expenses,
- totals,
- and financial tracking.

The current mode is stored in:

```text
profiles.budget_mode
```

and exposed through `AuthContext` as:

```text
budgetMode
```

Several screens change their labels and content depending on this value.

In tracking mode new months are created without a plan, so nothing carries in the background, and no screen shows budget information.

Switching modes goes through the `set_budget_mode` RPC. It is idempotent, never touches
transactions, and re-derives the months after the current month: no plan in tracking mode,
the current month's plan in budget mode.

Switching **off** leaves the current month exactly as it is, so switching straight back on
loses nothing.

Switching **on** fills the current month where it has *no* plan, from the last month that
had one, else `categories.planned_amount`. A plan the user already set is never
overwritten. Without this a user coming back from a tracking period landed in budget mode
with nothing planned and no way to fix it, because `set_category_plan` refuses a past month
that has no plan (fixed in `20260918110350_budget_mode_restore_plans.sql`).

`create_budgets_with_carryover` seeds a new month from the last month **that has a plan**,
not simply the last month. Seeding from the last month whatever it held meant one tracking
period made every later month inherit `NULL` forever.

Carryover is unaffected by either: `recalculate_budget_chain` still breaks the chain at a
month without a plan, so the first restored month starts at carry 0 rather than inheriting
a stale balance from before the tracking period.

---

# Main Product Areas

## Dashboard

The dashboard is the user's financial overview for the selected month.

It includes:

- total income,
- total expenses,
- net result,
- recent financial activity,
- goal summaries,
- investment summaries,
- live market indexes.

The dashboard should answer:

> What is happening with my money right now?

---

## Budget / Expenses

This is the core monthly money-management experience.

It includes:

- expense categories,
- income categories,
- planned amounts,
- actual spending,
- carryover,
- transaction management,
- category drill-down,
- search.

CSV export and category management are reached from Settings, not from here.

This area should make it easy to understand:

> What did I plan, what actually happened, and where am I over or under?

---

## Goals

Savings goals include:

- target amount,
- target date,
- current amount,
- milestones,
- progress,
- achieved / active states.

There is no way to add money to a goal directly. `contributeToGoal` was the only thing
that wrote `goals.current_amount` by hand, no screen ever called it, and the value would
not have survived the next milestone edit anyway; it was deleted on 2026-09-19. Progress
moves through the milestones and nowhere else.

A milestone carries **two** figures: `amount`, its target, and `saved_amount`, the money
already put toward it (added 2026-10-02). `saved_amount` has no date of its own - the
point is that the money exists, not when it arrived - and the goals screen shows the pair
as `6,000/25,000` on any milestone that is not yet complete, smaller figure first.

**The column name is narrower than the meaning.** A goal is not always a savings pot: it
is often something being paid off in instalments, an apartment or a car, so the user-facing
label is **"עד כה"** and not "נחסך". Do not reintroduce saving-specific copy for this
field, here or in `EditGoalModal`. The column keeps its name because renaming it would
cost a migration for no behaviour.

The pair is rendered inside a `dir="ltr"` span, not by DOM order. The figures are LTR runs
on an RTL line, so without an explicit direction the smaller one lands to the right of the
slash, which is not how a fraction reads.

`goals.current_amount` is derived: the `update_goal_progress_on_milestone_change` trigger
recalculates it on every milestone insert, update or delete, as the sum of **completed
milestones at their full `amount` plus `LEAST(saved_amount, amount)` for the ones still
open**. Before 2026-10-02 it counted completed milestones only, so a user six months into
a 50,000 milestone saw no progress at all while real money accumulated. The `LEAST` caps
each milestone's contribution at its own target, so a partial figure larger than the
milestone cannot inflate the goal; the column itself is only constrained to be
non-negative, because lowering a milestone's `amount` below money already saved must not
fail with a constraint error. The client caps it too, in `saveEditMilestone`, and says so
rather than clamping silently.

Everything that reads `current_amount` moved with it: the progress bar, the dashboard goal
summary, and the monthly "יש לחסוך" figure, which gets smaller because the gap is smaller.

`goals.done` is **only ever set by the user**, through `markGoalAsDone`. The trigger used
to flip it to true once the milestone sum reached the target, and only ever in that
direction, so the client reset it to false after every milestone edit. That guard did more
harm than good: it ran on any milestone change including a rename, so editing a milestone
on a goal the user had marked finished silently un-finished it, while `deleteMilestone` had
no such reset and could leave a goal auto-marked. Both the auto-set and the guard were
removed on 2026-09-18 (`20260918111100_goals_no_autocomplete.sql`). Reaching the target
amount is not the same as deciding the goal is finished.

The goal experience should feel motivating but financially grounded.

---

## Investments

Users can create named investment portfolios. A name is unique per user, and a portfolio
holds at most one value reading per day, so a chart never has to pick between two readings
for the same date. `InvestmentsContext.investmentErrorMessage` turns either violation into
a Hebrew message.

Each portfolio contains a time series of value entries. `amount` is the portfolio's value
at that date; `flow` is external money moved in or out (negative is a withdrawal), which is
what separates a deposit from a gain.

The app derives:

- initial value,
- current value,
- absolute change,
- percentage change,
- allocation,
- historical views.

Investment values may be positive, zero, or negative.

---

## Annual Summary

The annual summary provides a higher-level view. It is computed on request by:

```text
get_yearly_summary(p_year)
get_transaction_years()
```

Both aggregate out of `transactions` and run as the caller, so RLS decides what they
return. Nothing about a year is stored (see Data Model).

The screen opens on the most recent year `get_transaction_years` reports, not on the current
calendar year, and only on the first load that returns one, so it never overrides a year the
user picked. It opened on the current year regardless, which landed an account last used in
2024 on "אין נתונים לשנת 2026" with no hint of where its own data was.

The screen carries four cards, in this order:

1. **תוצאה נטו** - the net result, the comparison to the same months of the previous year,
   and a strip of six figures: income, expenses, savings rate, leading category, and the
   peak income and expense months. Under the headline sits the period every figure covers.
2. **מגמות חודשיות** - income and expenses across the counted months. The expense line is
   dashed as well as orange, because green and orange is the pair protanopes struggle with.
   The y axis runs from zero, like every other money axis in the app. Fitting it to the data
   instead drew a steady year's two lines pinned to opposite edges of the plot, which made a
   22% gap read as the whole chart; a transaction is `CHECK (amount > 0)`, so a zero floor
   can never clip a month.
3. **תובנות שנתיות** - rule-based Hebrew observations, plus a full-year projection for a
   year still in progress. Every threshold scales with the length of the period.
4. **לאן הכסף הלך** - the five largest categories as ranked bars, each with its year total,
   its share, **what it cost in an average month**, and a sparkline of its counted months.
   The rest collapse into one "כל השאר" row that expands. Tapping a category opens its
   month-by-month breakdown.

A year whose every transaction sits in the month still running has no counted month yet, and
says when it will: the month after the one those transactions are in. That is February only
when the year's first transaction is in January, and the screen named February regardless,
which told every account opened mid-year to come back months later than it had to.

This replaced a category donut on 2026-09-24. In RTL, on a phone, with a real household's
category list, a circle turns the long tail into unlabelled slivers and needs a legend,
while a bar carries its own label and sorts itself. The monthly average and the sparkline
are the two things a year view can say that a month view cannot: what a category really
costs, and whether it grew all year or had one expensive month.

The Hebrew observations are rule-based, not generated by AI. An AI version was costed and
deferred on 2026-09-24: the design that would work computes every number in code and lets
the model only select and phrase, because a wrong figure in this product costs more than a
dull one.

---

# Financial Insights

**`useFinancialInsights` no longer exists.** It was deleted on 2026-09-18 with the other
dormant components, and this section still described it as present, which contradicted the
Dormant Components section further down. Its source is in git history.

The only rule-based insights in the product are the ones the annual summary generates for
itself. No AI is involved in any of them. The one place a model is involved is the assistant
chat, below, and it is kept apart from these on purpose.

---

# Recurring Transactions

**Removed on 2026-09-18.** The feature was dormant for months: the UI was hidden, production
never held a template, and signed-in users could not execute the generator. The
`recurring_transactions` table, `transactions.recurring_id` and all related triggers, functions
and client code were deleted (`20260918100000_drop_recurring_transactions.sql`).

Do not reintroduce a `recurring_id` reference without also restoring the generator's privileges
and the rule that blocked editing generated rows.

---

# Market Data

Market indexes are retrieved through the Supabase Edge Function:

```text
market-data
```

and consumed through:

```text
useRealTimeMarketData
```

This is currently the application's only external market-data source.

---

# AI Assistant

A floating button on every signed-in screen (`AiChatLauncher` in `components/AiChat.tsx`,
rendered by `Layout`) opens a chat where the user asks free-form questions about their own
figures. Added 2026-11-18.

```text
AiChat.tsx -> lib/ai-chat.ts (supabase.functions.invoke) -> Edge Function ai-chat -> Gemini API
```

It is the design the annual summary section said an AI version would need: **every figure is
computed in code and the model only selects and phrases.** The function gives Gemini seven
read-only tools (`get_summary`, `get_category_totals`, `get_monthly_totals`,
`search_transactions`, `get_budget_status`, `get_goals`, `get_investments`). Each one reads
rows and computes in `supabase/functions/ai-chat/aggregate.ts`, a pure module with no Deno or
network code so vitest runs it directly. The prompt tells the model never to do arithmetic
and to quote only what a tool returned. A wrong figure in this product costs more than a
dull one.

Rules that must survive later edits:

- **Reads run as the caller.** The function builds its client from the request's own
  `Authorization` header, so RLS decides what a tool can see, and every query also filters on
  `user_id`. There is no service-role client in `ai-chat` on purpose: a prompt that talks the
  model into a different query still cannot reach another account. Do not add one.
- **Read-only.** There are no write tools. Adding one means deciding what the user sees and
  confirms first, because the model would be choosing the write.
- **`investmentStats` mirrors `computeInvestmentStats`** (`lib/investments.ts`), and
  `ai-chat-aggregate.test.ts` checks the two against each other. The assistant quoting a
  different profit from the investments screen is the failure this exists to prevent. If the
  screen's arithmetic changes, change both. `get_budget_status` reports the database's own
  `balance` and does not recompute it, for the same reason.
- **The key is a secret, never an environment variable the browser can see.** `GEMINI_API_KEY`
  is an Edge Function secret:
  `npx supabase secrets set GEMINI_API_KEY=... --project-ref fzwxcaidvaweczxwvljk`.
  Never put it in `.env`, in a `VITE_` variable (those are bundled into the site) or in the
  repo. `GEMINI_MODEL` is an optional secret that switches the model with no code change;
  the default is `gemini-3.5-flash-lite`. Google retires models, so if the function starts
  answering 502, read the log for the upstream status before anything else, and check
  ai.google.dev/gemini-api/docs/models.
- **A mode the user is not in is not offered.** In tracking mode `get_budget_status` answers
  that there is no budget, the prompt says so, and the suggested questions leave the budget
  one out.
- **The conversation is not stored.** It is React state in the launcher: it survives closing
  the panel and is gone on reload. Nothing is written to the database or to localStorage, and
  the function logs token counts only, never the conversation.
- **Whole shekels, Israel time.** The prompt asks for whole shekels with the symbol, and
  `todayInIsrael()` gives the function its date, because an edge runtime sits in UTC and the
  date is wrong for the first hours of every Israeli day.

Limits, stated plainly. **Weekly quota: 20 questions per account, per week starting Sunday
00:00 Israel time.** It lives in `public.ai_chat_usage` and is taken by the RPC
`consume_ai_chat_question()`, which runs as the caller (`auth.uid()`), holds the number 20
itself, and checks and counts in one upsert. Changing the limit is a `CREATE OR REPLACE` of
that RPC, not a code change. A failed answer still costs a question, on purpose: any refund
RPC the caller can reach would reset the quota. If the RPC fails the function answers 503
rather than answering uncounted, so the SQL must be live before the function is deployed.
The burst limit (20 questions in 10 minutes) stays in front of it, in the memory of one
function instance: it stops a client loop from burning the week's quota in a minute. Google also uses free-tier content to improve its products and does not use
paid-tier content, so a key that serves real accounts should have billing enabled.

Deploy with the function deploy in the `deploy` skill, step 5a, naming `ai-chat`. The site
can ship before the function: the button then answers that the assistant is not available
yet, which is the 503 the function returns when the secret is missing.

---

# Currency

Cash Flow is **shekels only**.

`profiles.currency` was removed on 2026-09-18. It let a user pick USD or EUR, but no FX
conversion ever ran: the symbol changed and the amounts stayed shekels, so a user on USD
was shown wrong figures.

Formatting goes through `CurrencyContext`, which now holds ILS as a constant. It is kept
as a context, rather than inlined, so real multi-currency support has one place to land.

---

# Export

Financial exports are currently CSV only.

CSV generation uses:

```text
papaparse
```

and includes a UTF-8 BOM so Hebrew opens correctly in Excel.

The export UI lives in:

```text
ExportModal
```

---

# Visual Identity

Shilman Finance uses a premium financial visual language centered around:

- deep navy,
- orange,
- silver,
- neutral light backgrounds,
- semantic green / red financial states.

The intended feeling is:

- trustworthy,
- confident,
- premium,
- modern,
- clean.

It should not feel like a traditional bank or an overly corporate financial platform.

---

# Color Palette

Brand colors are defined centrally as HSL variables in:

```text
src/index.css
```

and exposed through Tailwind tokens.

Do not treat raw HEX values as the design source of truth.

Reference palette:

| Token | HSL | Approx. HEX | Role |
|---|---|---|---|
| `--navy-primary` | `210 67% 11%` | `#0D1B2A` | Main brand color |
| `--orange-primary` | `20 93% 46%` | `#E85D04` | Primary accent / CTA |
| `--silver-primary` | `0 0% 69%` | `#B0B0B0` | Borders / secondary surfaces |
| `--green-income` | `142 50% 42%` | semantic | Income / positive money |
| `--green-success` | `142 76% 36%` | semantic | Completion / success |
| `--red-danger` | `0 55% 45%` | semantic | Over-budget / destructive |
| `--light-blue` | `208 100% 97%` | very light blue | Light-mode card ground |
| `--dashboard-bg` | `216 22% 96%` | `#F5F7FA` | Dashboard page background |

Orange is the primary accent.

Navy provides the main brand identity.

Green and red should remain semantic financial colors rather than decorative accents.

---

# Dark Mode

Dark mode uses the `.dark` class through:

```text
next-themes
```

with class-based theme switching.

In dark mode:

- navy becomes the primary background,
- lighter navy surfaces become cards,
- silver becomes more prominent in borders,
- orange remains the accent.

The design system includes shared gradients and shadows such as:

```text
--gradient-luxury
--gradient-accent
--gradient-silver

--shadow-luxury
--shadow-card
--shadow-orange
```

---

# Typography

Fonts are loaded from Google Fonts in:

```text
index.html
```

## Hebrew

```text
Heebo
```

Primary Hebrew / application font.

Exposed as:

```text
--font-hebrew
```

and used globally on `html` / `body`.

## Latin

```text
Inter
```

Used for Latin text and the `font-luxury` utility.

## Display

```text
Playfair Display
```

Used for premium / display-style headings through:

```text
font-display
```

The global document direction is:

```text
rtl
```

---

# Accounts

The services this project runs on are **not all under the same login**, which has cost time
more than once. Both of the ones that matter are owned by **arielelya1@gmail.com**:

| Service | Account | What lives there |
|---|---|---|
| Cloudflare | `arielelya1@gmail.com` | the `shilmancashflow.com` zone: DNS, and the cache that every deploy has to purge |
| Supabase | `arielelya1@gmail.com` | project `fzwxcaidvaweczxwvljk`: database, auth, email templates |

Signing in as any other address shows **"No domains found in this account"** in Cloudflare,
which reads as the domain being gone rather than as the wrong login. The Cloudflare account
id is `f559365f9c8e6e20320f8bf2eff9d5d8`, so the zone's DNS is at:

```text
https://dash.cloudflare.com/f559365f9c8e6e20320f8bf2eff9d5d8/shilmancashflow.com/dns/records
```

The Worker that serves production lives in **this same account**, and holds the Custom Domains
for `shilmancashflow.com` and `www`. The apex is an `AAAA` record to `100::` with `proxied=true`,
the dummy-origin pattern that hands the request to that Worker. There are no Workers Routes on
the zone and no Pages projects in the account; the Custom Domain is the whole mechanism.

A second Cloudflare account, `shilman.finance@gmail.com`, held a **duplicate Worker of the same
name** bound to nothing. On 2026-11-05 wrangler was logged in as that account and four deploys
went into it while production sat frozen on the previous day's build. None of them failed: a
deploy to the wrong account uploads the assets, prints a Version ID, and reports the version
live at 100%, into a Worker no domain points at. Every symptom read as a stale edge cache, and
the cache was never involved. `wrangler.jsonc` now pins `account_id`, so that deploy is refused
instead of silently succeeding. **When production looks stale, run `npx wrangler whoami` before
touching the cache.** That account is queued for deletion as of 2026-11-05.

The purge still needs its own API token (`cloudflare-cache-purge-token` in the macOS Keychain):
wrangler's OAuth scopes include `zone:read` but no cache purge, whatever account it is on. And a
third-party "connect your Cloudflare" button, like Resend's auto-configure, lands in whichever
account the browser is signed into, so it can still miss this zone.

Auth mail is a third account again: **Resend**, since 2026-10-20, sending as
`no-reply@shilmancashflow.com` from the Ireland region, with DKIM and the sending CNAMEs on
the shilmancashflow.com zone. Before that it went out through Gmail SMTP as
`shilman.finance@gmail.com`, so a password reset arrived from a gmail.com address and linked
to shilmancashflow.com - the shape users are taught to distrust.

Two things about that zone are easy to break. The Resend records live on the `send` and
`rsend` subdomains, so the root SPF and the IONOS MX records that carry the business mail are
untouched and must stay that way. And both CNAMEs are **DNS only**: proxied through Cloudflare,
mail stops leaving. `supabase/templates/README.md` holds the template side.

---

# Repository Location

All commands run from the repository root:

```text
shilman-cash-flow/
```

which currently sits inside a parent:

```text
cash_flow/
```

## Branches

`main` is the product. It is what deploys.

`redesign/stage-1-foundations` is a **rejected** visual redesign, kept locally
and never merged or deployed. Twelve commits from September 2026 that rebuilt
the whole look: a token layer, Assistant in place of Heebo, shared Row/Bar/Stat
primitives, and two attempts at grouping - first removing every card ground so
content sat flat on the page, then "wells", tinted sunken regions on white with
a 248px desktop rail.

Both groupings were rejected after being seen on real data. The first read as
"no division, no differentiation between components", worst at desktop width;
the second was rejected too. **Do not treat that branch as unfinished work to
pick up, and do not re-propose either grouping.** If visual change comes up
again, start by asking what specifically is wrong with the current screens.

Two things on that branch are worth knowing about, because they are defects
rather than styling and they are still live on `main`:

- The bottom bar declares `backdrop-blur` over an opaque ground, so it does
  nothing. Fixing it changes how the bar looks, which is why it was left.
- Nothing in the product sets `unicode-bidi`, so an amount rendered inside
  Hebrew text can have its minus sign and shekel glyph reordered. The fix
  touches all 61 places that draw a figure. Latent, not observed.

The accessibility and mobile fixes from that period were separated out and are
on `main`: the viewport zoom lock is gone, fields are 16px at phone width
(enforced once in `index.css`, because 45 fields override the Input default),
the bar clears the iPhone home indicator, and the FAB has an accessible name.

The dialog close button sits at the physical **top right**, deliberately
(2026-10-01). It was moved to the logical edge during that period because in
RTL the right edge is where a right-aligned title begins, but every
`DialogTitle` in the product is centered, so there is nothing to collide with,
and the right corner is where a Hebrew reader looks for it. It is a bare grey
glyph with no ring or circle, turning orange on hover; the keyboard focus ring
is `focus-visible` only, so tapping it no longer leaves an orange ring behind.
If a right-aligned dialog title is ever added, give that dialog's header
padding rather than moving the button back.

---

# Commands

```bash
npm run dev
# Vite development server on http://localhost:8080

npm run build
# Production build -> dist/

npm run typecheck
# tsc --noEmit on tsconfig.app.json and tsconfig.node.json
# (the root tsconfig.json has "files": [], so a bare tsc --noEmit checks nothing)

npm run lint
# eslint .

npm run test
# vitest run

npm run test:watch
# vitest watch mode

npm run test:db
# node test-runner.mjs - integration tests against the live Supabase project

npm run test:e2e
# playwright test - browser tests, desktop and phone viewports

npm run test:e2e:ui
# playwright test --ui - the same suite in Playwright's interactive runner

npm run test:all
# vitest run && playwright test && node --env-file=.env.local test-runner.mjs
```

Deploying an edge function is separate from deploying the site, and is not an npm script:

```bash
npx supabase functions deploy market-data --project-ref fzwxcaidvaweczxwvljk
# from shilman-cash-flow/, after npx supabase login. See the deploy skill, step 5a.
```

Run a single browser test:

```bash
npx playwright test --project=desktop -g "translates an unconfirmed address"
```

Run a single unit test:

```bash
npx vitest run src/__tests__/auth-page.test.tsx
```

Run a specific test by name:

```bash
npx vitest run -t "shows error popup when fields are empty"
```

`npm install` requires legacy peer dependencies.

This is already configured through:

```text
.npmrc
```

---

# Browser Tests

`e2e/` holds Playwright tests, run against a real Chromium at both desktop and phone
widths. They cover what jsdom cannot: layout at 390px, autofill attributes the browser
actually honours, and whether an error shaped the way GoTrue shapes its own reaches the
screen in Hebrew.

They are hermetic. `e2e/helpers.ts` intercepts every request to `supabase.co`, and the
deny-everything net is registered **first** so that Playwright, which matches handlers
newest-first, lets the specific stubs win. A call the helper does not account for is
aborted rather than allowed through, so a run cannot create an account, send mail or trip a
rate limit against the live project.

Adding a stub means adding it to `stubSupabase`, not relaxing the catch-all.

---

# Important Test Warning

`npm run test:db` is **not hermetic**.

It connects to the real Supabase project.

The integration runner:

```text
test-runner.mjs
```

uses test accounts and exercises:

- database tables,
- RPCs,
- RLS isolation,
- authentication,
- and cleanup.

Run this deliberately, not as a casual local check.

---

# Application Architecture

The application is a static React SPA built with:

- **Vite**
- **React 18**
- **TypeScript**
- **Supabase**
- **Tailwind**
- **shadcn/ui**
- **framer-motion**
- **Vitest**

There is no application server.

The browser communicates directly with Supabase.

Production output is served as an SPA through Cloudflare using:

```text
wrangler.jsonc
```

---

# Provider Architecture

The application's domain data is organized through React Context providers.

`src/main.tsx` nests the providers in this order:

```text
Auth
Currency
Categories
Transactions
Budgets
Goals
Investments
```

Each context under:

```text
src/contexts/*Context.tsx
```

owns one primary area of Supabase-backed state.

Contexts generally:

1. fetch the full user-scoped data set on login,
2. store it in `useState`,
3. expose CRUD helpers,
4. expose a `refreshX()` function,
5. expose `loadError`, true when the last read failed.

`loadError` exists because `loading` cannot answer the question that matters. A failed read
left the previous state in place, which on a first load is an empty list, and the screen
drew zeros - indistinguishable from an account that really has no budget, and in this
product that is a reason not to act on the number. A read has three outcomes, not two:
there is data, there is no data, and nothing is known.

Screens render the failure through `components/LoadError.tsx`, and **only when there is
nothing to draw** (`loadError && data.length === 0`). A background refresh that fails
behind figures already on screen keeps them and leans on the toast: good numbers are worth
more than an error page. The dashboard and the תזרים screen are the exception in shape only
- each totals several sources, so any one of them failing empty makes every figure on it
meaningless, and each picks the failed source by priority.

**A screen waits for every read its figures are derived from, not only the ones it reads
rows out of.** The תזרים screen gated on categories and budgets while summing every
"actual" - the three headline totals, each category's בפועל and יתרה, ניצול תקציב, every
ring - from `transactions`, which it did not wait for. While that read was in flight, and
for good if it failed, the screen drew a complete and confident month in which nothing had
been spent and every category still had its whole plan available. Both screens now gate on
`transactionsLoading` and name `transactionsError` first in their failed-source priority.

`AuthContext` carries the same idea as `profileError`. Anything routing on `isOnboarded`
must consult it: an unreadable profile means unknown, not false, and sending an established
user through onboarding is not a harmless detour, because choosing a mode there runs
`set_budget_mode` and re-derives their plans.

There is no meaningful React Query cache for domain data.

A `QueryClient` exists but is essentially unused.

Provider order matters because inner providers can depend on outer providers.

---

# Database-Driven Financial Logic

Derived financial values are intentionally owned by Postgres rather than calculated independently in the browser.

Important computed values include:

```text
budgets.actual_amount
budgets.balance
budgets.carryover_amount
```

These are maintained through database triggers and RPCs.

Important RPCs include:

```text
create_default_budgets_for_month
recalculate_budget_chain
recalculate_forward
recalculate_balance
set_category_plan
set_budget_mode
get_yearly_summary
get_transaction_years
```

The client generally:

1. writes source data,
2. lets the database perform derived calculations,
3. re-fetches the updated values.

`src/lib/finance.ts` mirrors some calculations for display and tests.

For example:

```text
computeBudgetChain
getPlanEditMonths
```

document the logic used by:

```text
recalculate_budget_chain
set_category_plan
```

(defined in `supabase/migrations/20260912120000_budget_plans_v2.sql`).

If the financial rule changes, both the database implementation and any mirrored client logic must remain consistent.

---

# Cross-Context Refresh

Contexts communicate some changes through browser events.

## Transaction changes

`TransactionsContext` dispatches:

```text
transactions-changed
```

after writes.

`BudgetsContext` listens for this event and re-fetches once, immediately, with no timer.

There used to be two reads, at 150ms and 1000ms, on the belief that there was no way to know when the database-side recalculation had committed. There is: `after_transaction_change` is an `AFTER ... FOR EACH ROW` trigger, so it runs inside the write's own transaction, PostgREST does not answer until that commits, and the event is dispatched after the write resolved. By the time the handler runs the recalculated rows are already there.

A read that resolves out of order is handled by a sequence number (`fetchSeqRef`) rather than by timing, so only the newest read publishes.

When adding a new write path that causes database-side recalculation, the relevant refresh event may also be required.

---

# Date and Month Rules

## Month Keys

Budgets use the first day of the month as their month key:

```text
YYYY-MM-DD
```

Use:

```text
formatMonthKey
startOfMonth
```

for this behavior.

## Israel Time

Every date rule is enforced twice, in `finance.ts` and in Postgres, and the database side
(`budget_current_month`, `budget_window_start`, `validate_transaction_date`) works in
`Asia/Jerusalem`. The client used the device clock, so near midnight at a month boundary, or
for a user abroad, one side accepted what the other rejected.

Use `israelNow()` from `finance.ts` instead of `new Date()` anywhere a date is compared to
the current month, the edit window, or "the future". It is already the default reference for
`getEditWindowStart`, `isMonthReadOnly` and `isFutureTransaction`.

## Money From User Input

**Whole shekels. The product has no agorot anywhere: not in an input, not in the database,
not on screen.** Decided 2026-11-04.

Every amount in Cash Flow is typed by a person from memory. There is no bank import, no
CSV import and no price feed - `Papa.unparse` is export only, and `market-data` is
read-only and writes no money - so `247.80` is not a truer figure than `248`, it only looks
like one. The planning layer is round by nature, nothing the product decides turns on fifty
agorot, and the carryover chain would otherwise roll a balance of `-0.37` forward through
every later month as permanent noise. The decimal point is also the most dangerous key on a
phone: one slip is a tenfold error, and a tenfold error is hard to catch because the result
still reads as a plausible amount.

If a bank import is ever added, this decision has to be revisited: imported figures come
from outside and are not the user's recollection.

Three layers, the same shape as the date rules:

1. **The keystroke.** Every money field filters with `isMoneyInput()` from `finance.ts` and
   carries `type="text" inputMode="numeric"`. The character never arrives, so the refusal
   is never a surprise at save time.
2. **The parser.** `parseAmount()` takes a run of digits and returns `NaN` for everything
   else - a decimal point, a comma, a minus, exponential notation, empty. It **refuses** a
   decimal point rather than rounding it: accepting `247.80` and storing `248` would save a
   different number from the one on screen, which is how the comma bug did its damage.
   Callers must refuse `NaN` rather than write it; `Number.isFinite` is the check, and
   `GoalsContext` throws on a non-finite amount as the last line of defence.
3. **The database.** A CHECK per user-entered money column. Derived columns
   (`budgets.actual_amount`, `balance`, `carryover_amount`) are deliberately left
   unconstrained: they are recomputed by `recalculate_budget_chain` on every transaction
   write, so a constraint there would make a write fail over a row written years earlier.

Never use `type="number"` for money. It still lets `e`, `-` and `.` through in most
browsers, so the character lands and the rule only bites on save. To check, grep for the
attribute as it would actually be written rather than for the bare string - the plain
search also matches the comments that say not to use it:

```bash
grep -rn 'type="number"' src/ | grep -v '//'
```

Anything that *derives* one money field from another writes whole shekels too -
`deriveWithdrawalPair` and `deriveDepositPair` in `lib/investments.ts` round, because they
set a field programmatically and so bypass its keystroke filter.

Percentages are not money. `toFixed` on a change percentage, an allocation share or a
progress ring is correct and stays.

## Date-only Values

Use:

```text
parseDateOnly
formatDateOnly
```

from:

```text
src/lib/utils.ts
```

for date-only values.

Directly using:

```ts
new Date("2026-03-01")
```

can parse the value as UTC and shift the displayed calendar day in local time.

---

# Historical Edit Limits

The product allows editing the current month and the 3 months before it, in Israel time (`EDIT_WINDOW_MONTHS` in `finance.ts`, `budget_window_start()` in the database).

Older months are read-only: their transactions cannot be added, edited, moved or deleted, and their plans cannot change. Deletes without a signed-in user (the account-deletion cascade) are exempt.

This rule is enforced in multiple places, including:

```text
finance.isMonthReadOnly / useBudgetLimits
BudgetsContext.setCategoryPlan
TransactionsContext guards
TransactionModal and EditTransactionModal
validate_transaction_date, validate_budget_edit (database)
```

Separately from the hard limit, a change inside the window that lands in a **past month**
shows a warning that the later months move with it, because budgets carry forward. Since
2026-09-19 all three screens share one rule: the date is in a month before this one, the
category is an expense, and `budgetMode` is on. `TransactionModal`, `EditTransactionModal`
and the delete confirmation in `CategoryTransactionsModal` each check exactly that, using
`israelNow()`. Keep them together: they drifted once, and the two nearest months, the ones
people actually correct, were the ones that stayed silent.

There is no shared validation module. `src/lib/schemas.ts` held Zod schemas that were meant
to be reused and never were: every screen defined its own rules inline, and after
`AddTransaction` was deleted the file was imported by nothing but its own test. It was
removed on 2026-09-18. Validation lives in the screen and in the database, and those two are
what must agree.

Search in `BudgetSearchPanel` looks back 12 months, because it only views data. Since
2026-09-19 the type and the period are filters rather than preconditions: any one of
keyword, type, category or period returns results, and with no period set the search covers
the full 12 months.

Transactions beyond the end of the current month are also blocked.

---

# Categories

Categories are soft-deleted rather than physically removed.

Deletion sets:

```text
deleted_at = ...
```

This preserves historical transaction relationships.

`is_active` was removed on 2026-09-18. It duplicated `deleted_at`, which holds strictly
more information and which the partial unique index already keys on:

```text
UNIQUE (user_id, name) WHERE deleted_at IS NULL
```

That index is what lets a user re-create the name of a category they deleted. A category
is live when `deleted_at IS NULL`.

`CategoriesContext` exposes `categories` (active only, for pickers and lists) and
`allCategories` (active and deleted). Anything that totals or labels transactions (dashboard,
budget screen, annual summary, CSV export, search) looks categories up in `allCategories`, so a
deleted category's history still counts everywhere it is totalled. The budget screen lists a
deleted category, marked "(נמחקה)" and without a plan, only in months where it has transactions.

Every screen that names a category marks a deleted one "(נמחקה)", and all of them must: the
unique index on the name is partial (`WHERE deleted_at IS NULL`), so a deleted category and a
live one can carry the same name. The annual summary took its names straight from
`get_yearly_summary`, which does not return `deleted_at`, and so showed two rows reading
"סופר" with different totals and nothing to tell them apart. It now looks the id up in
`allCategories` like the rest.

Normal category reads filter:

```text
deleted_at IS NULL
```

Categories are ordered by `position`, which is `NOT NULL`. A new category is placed at the
end of the user's list by the `trg_set_category_position` trigger, so the client never
assigns it.

Drag-and-drop reordering uses `dnd-kit`.

In **budget mode** `CategoryManagementModal` requires a monthly budget for a new **expense**
category and will not stage it without one (2026-09-19). The figure goes to
`categories.planned_amount` through `addCategory`, and then to the current month's row
through `setCategoryPlan`, which is the part that matters:
`create_budgets_with_carryover` reads `NULLIF(c.planned_amount, 0)`, so a deliberate plan
of 0 would come back as no plan at all. Income categories have no plan and tracking mode
has none, so neither is asked. Before this, a new category was born with no plan and set
off the "קיימות קטגוריות ללא תקציב" alert immediately.

---

# Authentication Constraint

Do not await a Supabase request directly inside:

```text
onAuthStateChange
```

Supabase holds an internal lock during this callback and doing so can deadlock the authentication flow.

The existing pattern defers work with:

```ts
setTimeout(..., 0)
```

See the relevant comment in:

```text
AuthContext
```

---

# Supabase

Supabase is the main backend platform.

The project contains 191 timestamped migrations under:

```text
supabase/migrations/
```

## Do not write new migration files

**A schema change is handed to the user as SQL to paste into the SQL Editor, in the reply,
not committed as a file under `supabase/migrations/`.** Ask them to run it, then verify the
result against the live schema with a read-only query and report what came back.

The reason is that a file cannot say whether it ran, and a wrong answer to that question is
expensive in both directions: a file that has been applied but still reads NOT YET APPLIED
invites someone to run it again, and one that was never applied but looks ordinary invites
the assumption that the schema already has it. This directory already carries both kinds of
drift - see the section below - and every new file adds another thing to keep honest.

The live database is the record of what the schema is, which is what the rest of this file
already says. Read a function with `pg_get_functiondef` rather than from the newest file
that mentions it.

Two things follow from this:

- **Take the current definition from the database before rewriting a function.** A
  `CREATE OR REPLACE` built from a migration file can silently undo whatever was changed
  after it, because the files are not in step with the schema.
- **Read-only queries are available without asking; writes are not.**
  `npx supabase db query "<sql>" --remote=fzwxcaidvaweczxwvljk --read-only` runs. Without
  `--read-only` the CLI refuses in an agent session and says so, which is the guardrail
  working, not an obstacle to route around.

## Migration history

`supabase_migrations.schema_migrations` records what has been applied. Two things about it:

**Do not compare it to the filenames by exact version.** Lovable recorded many migrations one
or two seconds off from the filename it wrote itself, so a naive comparison makes 166 of 186
files look unapplied when almost all of them ran. Match within a few seconds.

**It is nearly, not fully, complete.** The 27 hand-applied migrations that could be proved
applied were recorded on 2026-09-18 (`20260918111600`). Fifteen files from 2025 stay
unrecorded: their effects are probably in the schema, but marking one applied that was not
would make a future push skip a change the database needs.

`20260503090000_remove-goal-autocomplete.sql` is deliberately unrecorded because it was
genuinely never applied. **Never push it.** It drops a trigger and never recreates it, so on
its own it stops milestone changes from updating goal progress. `20260918111100` supersedes
it and does the job correctly.

These define:

- schema,
- triggers,
- RPCs,
- RLS policies,
- financial behavior.

## New tables need an explicit grant

From 2026-10-30 Supabase stops granting Data API access automatically to tables created in
`public` on existing projects. The live tables keep the grants they already have, so nothing
in production changes. A table created from that date onwards is unreachable through
supabase-js, PostgREST and GraphQL until it is granted, and the error is `permission denied`,
not an RLS failure: privileges are checked before any policy runs, so a correct
`auth.uid() = user_id` policy will not make an ungranted table readable. Do not debug that as
a policy problem.

No migration in this project grants table privileges - every `GRANT` here is `GRANT EXECUTE`
on an RPC. The migration files therefore no longer rebuild a working database on their own:
replaying them into a fresh project or a preview branch would leave every table invisible to
the client. Nothing does that today (there is no local `supabase db reset`, no preview branch
and no CI that applies migrations), so this is latent rather than broken.

Any migration that creates a table in `public` must grant it in the same file:

```sql
grant select, insert, update, delete on public.<table> to authenticated;
grant select, insert, update, delete on public.<table> to service_role;
```

`anon` is left out on purpose. Every table is user-scoped behind `auth.uid() = user_id` and
nothing here is readable without a session, so granting `anon` would widen the surface for no
feature.

Edge Functions live under:

```text
supabase/functions/
```

Current functions:

```text
ai-chat
delete-account
market-data
```

All three are called by the app and nothing else. `generate-month` and
`recalculate-yearly-summary` were removed on 2026-09-19, from the repo and from the deployed
project: nothing called either of them. `generate-month` was a thin wrapper over
`create_budgets_with_carryover`, which is still there and can be called directly.
`recalculate-yearly-summary` wrapped `recalculate_yearly_summary`, which no longer exists:
there is nothing left to recalculate, because the year is aggregated on request.

`cleanup-unconfirmed-users` and `copy-user-data` were removed on 2026-09-18, both from the
repo and from the deployed project, along with their secrets.

The cleanup job had failed on every run since it was created. The cause was not a missing
secret: `CLEANUP_SECRET` was set as an Edge Function secret all along, while the invoker
read `vault.decrypted_secrets`, a different store, which is empty. **Edge Function secrets
and the database vault are separate places with no connection between them.** That was only the first of three problems: `listUsers()` with no arguments returns the first
50 users, so the job could never have seen account 51 even once the secret was found, and it
left a service-role endpoint guarded by a single shared string.

`copy-user-data` deleted every transaction, budget and category of a target account looked
up by email, then copied another account's in. Nothing in the app ever called it, and its
secret was set, so it was a live and reachable way to destroy an account's data. Its source
is in git history if the seeding behaviour is ever wanted again.

The cleanup is now `public.cleanup_unconfirmed_users()`, called straight from pg_cron. An
account is removed when it has never signed in and was created more than 30 days ago
(widened from 7 on 2026-09-19 by `20260919200000_cleanup_window_30_days.sql`; the rule is
otherwise the one the function always used). It refuses to run, deleting nothing, if more than 25
accounts match, so a clock or logic problem surfaces as a failed job rather than as lost
accounts.

**Its name is narrower than its rule, and the rule is the one to trust.** The function tests
`last_sign_in_at IS NULL`, which is "never signed in" and not "never confirmed the address".
In practice confirming establishes a session, so the two almost always agree - but an account
that confirmed and never signed in is inside the rule and would be deleted. Do not widen this
function on the strength of its name: whatever it is called, the condition it deletes on is
the one written in it.

`unlock-new-month` is gone too, both the monthly job and the deployed function. It had
errored on every run since the `unlocked_months` table was dropped, and its source was never
in this repo. One scheduled job now remains in the project, and it works.

JWT verification is configured in:

```text
supabase/config.toml
```

`delete-account` runs with `verify_jwt = true` since 2026-09-19, so the platform rejects a
request with no or a malformed token before the function body runs. The function still
verifies the session itself, because that is what identifies which account to delete;
neither check replaces the other. `ai-chat` is configured the same way and for the same reason. `market-data` stays at `false` on purpose: it returns
public index data and touches no table.

**The file is not the switch.** `config.toml` only reaches production through
`supabase functions deploy <name>` or the dashboard toggle. Changing it alone leaves the
deployed function exactly as it was, with nothing to indicate the drift.

The same is true of the function source: `wrangler deploy` ships the Worker and `dist/`
and nothing under `supabase/`, so a function change can sit committed on `main` and never
reach production. Deploying one from this checkout needs two things that are easy to miss:
`npx supabase login`, which only the user can complete, and an explicit
`--project-ref fzwxcaidvaweczxwvljk`, because `supabase link` has never been run here. Run
it from `shilman-cash-flow/`; from the parent folder the CLI reports the entrypoint as
missing. See the `deploy` skill, step 5a.

---

# RLS and User Isolation

Every domain table is scoped through:

```text
user_id
```

and protected using Supabase Row Level Security. All eight tables carry the same policy,
`auth.uid() = user_id`, for SELECT, INSERT, UPDATE and DELETE: four policies each, except
profiles, which has three because it has no DELETE policy (accounts are removed by the
cascade from `auth.users`). It was nine tables until `yearly_summaries` was dropped on
2026-09-19; the twelve foreign keys between them were fifteen then.

Client queries also explicitly filter with:

```ts
.eq('user_id', user.id)
```

`transactions`, `budgets`, `milestones` and `investment_entries` each store `user_id`
alongside a parent id so RLS can filter without a join. That duplication is enforced by
**composite foreign keys** on `(parent_id, user_id)`, added in
`20260918111300_composite_owner_fks.sql`. Do not replace one with a single-column key: an
INSERT policy only checks `auth.uid() = user_id`, and a foreign key check runs as the table
owner and bypasses RLS, so without the composite key a user could attach their own row to
another account's category, goal or portfolio. `get_yearly_summary` joins transactions to
categories filtering only on `t.user_id`, so a cross-owner `category_id` would put another
account's category name into the attacker's annual summary. The same held for
`recalculate_yearly_summary` before it was dropped: the aggregation moved, the reason for
the composite keys did not.

`transactions.category_id` is `ON DELETE RESTRICT` while profiles cascades to both
categories and transactions. `supabase/verification/20260918111300_account_deletion_verify.sql`
proves the cascade order still deletes an account cleanly; run it after any change to these
keys.

The application should preserve strict user / household data isolation.

---

# Generated Supabase Files

The following files are generated by the Supabase / Lovable toolchain:

```text
src/integrations/supabase/types.ts
src/integrations/supabase/client.ts
```

They should remain synchronized with the database schema.

---

# Data Model

Primary tables include:

## User

```text
profiles
```

`user_id` is the primary key. Fields include:
- display_name
- budget_mode
- is_onboarded
- last_active_at (when the user last opened the app; written by the client on session
  load, at most once an hour)

## Categories

```text
categories
```

Includes:
- income / expense type,
- planned amount,
- icon,
- position,
- deleted_at (soft delete).

## Transactions

```text
transactions
```

Includes:
- amount (positive; the category's type decides income or expense),
- transaction_date,
- notes (**required**: NOT NULL plus a not-blank CHECK, mirrored by `transactionSchema`).

`category_id` is deliberately the one foreign key with no `ON DELETE` rule: deleting a
category that has transactions must fail rather than erase financial history. The matching
key on `budgets` cascades, because a budget row is derived, not history.


## Budgets

```text
budgets
```

Includes:
- month,
- planned_amount,
- actual_amount,
- balance,
- carryover_amount.

## Goals

```text
goals
milestones
```

## Investments

```text
investments
investment_entries
```

## Annual Summaries

There is no table. `get_yearly_summary(p_year)` returns one year as JSON, aggregated from
`transactions` each time the screen asks:

```text
monthly_data
expenses_by_category_by_month
```

plus the year's own income and expense totals. `get_transaction_years()` returns the years
the picker can offer. Both are `SECURITY INVOKER`, so RLS scopes them to the caller.

`yearly_summaries` used to store this. It was the only cache in the schema and the only
thing that could drift, and it had: one account's 2025 row held December expenses of
10538.171 against a transaction sum of 10538.17, last rebuilt in March. The table, its four
triggers, its two trigger functions and `recalculate_yearly_summary` were dropped on
2026-09-19, after the bundle that stopped reading them was live.

**Nothing in the schema is a cache now.** Every figure the app shows is derived from the
rows it is derived from, at the moment it is shown, except `budgets.actual_amount`,
`balance` and `carryover_amount`, which are maintained by triggers within the 3-month
window and are the deliberate exception.

---

# UI System

shadcn/ui components live in:

```text
src/components/ui/
```

They are vendored into the repository.

Configuration lives in:

```text
components.json
```

New components can be added through:

```bash
npx shadcn@latest add
```

## Date pickers

There are two, and both give the user a jump and a step (2026-10-01):

- `components/ui/calendar.tsx` wraps react-day-picker and backs every `DatePickerInput`.
  `captionLayout="dropdown-buttons"` puts the month and year dropdowns **and** the
  prev/next arrows in the caption; react-day-picker swaps the arrow directions itself
  under `dir="rtl"`. The caption carries `px-9` so the centered dropdowns stay clear of
  the absolutely positioned arrows.
- `components/MonthPicker.tsx` is the month grid behind the dashboard and budget headers.
  The arrows step a year; the year itself is a dropdown when the range spans more than
  one year, and plain text when it does not.

Both render Hebrew month and weekday names (`locale: he`), like the rest of the product.

The month and year dropdowns are **native `<select>` elements** drawn under a styled
wrapper. The option list the browser opens takes its colors from the select, not from the
wrapper, so the select carries `bg-background text-foreground` explicitly: a hover color
on the wrapper alone once left the open list white on white, unreadable exactly while
being scrolled.

react-day-picker renders each dropdown's visible text **and its caret** inside one element
and gives it the `caption_label` class, so that class must describe an inline row
(`inline-flex items-center`). As a block it pushed the caret onto a second line and every
dropdown grew to 46px inside a 40px caption - which is what made the caption look
inflated next to the 28px arrows.

Style the calendar in `calendar.tsx`. `index.css` used to hold rules keyed on
react-day-picker's default class names (`.rdp-dropdown_month` and friends), which
`calendar.tsx` overrides wholesale, so none of them ever applied; they were removed on
2026-10-01.

The product is Hebrew-first.

User-facing:

- labels,
- validation errors,
- toasts,
- messages

should remain in Hebrew unless there is a specific reason otherwise.

Toasts are shown through `sonner`:

```ts
import { toast } from 'sonner'
```

An older Radix-based toaster also still exists in `src/components/ui/toaster.tsx`.

---

## Touch, motion and theme details (2026-11-18)

Found by running the Web Interface Guidelines and the animation review skills over the app.

- **Transitions name their properties.** No `transition-all` and no `transition: all`:
  it animates things nobody meant to animate, and on the dragged category row it made the
  row chase the finger. Progress bars use `transition-[width]`, tab and toggle buttons
  use `transition-[color,background-color,box-shadow]`.
- **`prefers-reduced-motion`** is handled once, at the end of `index.css`: transitions and
  animations collapse to 1ms. `animate-spin` and `animate-pulse` are exempt, because they
  say "working" rather than decorate. The accordion in `Investments.tsx` reads
  `useReducedMotion()` itself, since framer-motion ignores the CSS rule.
- **`autoFocus` goes through `autoFocusDesktop()`** (`src/lib/autofocus.ts`). It is true
  only where the pointer is precise, so a phone does not raise the keyboard the moment a
  dialog opens.
- **Hover only where the device can hover.** `hoverOnlyWhenSupported` is on in
  `tailwind.config.ts`, so a tap no longer leaves a button stuck in its hover colour.
  Anything that matters on a phone needs a visible rest or `active:` state, not `hover:`.
- **`color-scheme`** follows the theme (`html` light, `html.dark` dark), so native
  scrollbars, `<select>` lists and date inputs match. `theme-color` meta tags are in
  `index.html`. `touch-action: manipulation` is set on everything tappable in `index.css`.
- **The theme toggle** switches on `resolvedTheme`, not `theme`. With the theme left on
  "system" and the device in light mode, the first tap used to set "light" again and
  appear to do nothing. Its accessible name is in Hebrew, and `e2e/settings.spec.ts`
  looks it up by that name.
- **The favicon** lives in `public/` (`favicon.ico`, `favicon.png`, `apple-touch-icon.png`),
  cut from the SF monogram in `public/brand/shilman-finance.png`. It used to be a Lovable
  default plus a link to Lovable's upload bucket.
- **The settings e2e tests** that wait for an error message use `.first()`: the same text
  is shown inline and as a toast, so a bare `getByText` is a strict-mode failure whenever
  the toast has landed.

---

# Shared Presentation Classes

Reusable visual classes in:

```text
src/index.css
```

include:

```text
.luxury-card
.premium-card
.luxe-card
.luxe-press
.btn-luxury
.display-number
.progress-circle
.shimmer-border
.custom-scroll
.animate-fade-in
```

Motion elsewhere uses:

```text
framer-motion
tailwindcss-animate
```

The visual system should remain consistent with Shilman Finance rather than introducing unrelated UI styles.

---

# Dormant Components

None. The seven components and modules nothing rendered were deleted on 2026-09-18:
`AddTransaction`, `TopBar`, `ErrorDialog`, `DetailedChartModal`, `SavingsPlannerCard`,
`CategoryChart` and `useFinancialInsights`. Their source is in git history.

`HeroStrip` is the shared page header for most major sections except the dashboard.

---

# TypeScript

Passwords: the rule this project enforces (8 characters, with a lowercase letter, an
uppercase letter, a digit and a symbol) lives in `src/lib/password.ts` and is used by both
the sign-up and reset screens. `passwordProblem` answers a submit handler with one
sentence; `passwordRequirements` returns the same rule as five labelled booleans, which
both screens render live under the field so the missing part is visible while typing. Sign-up used to promise 6 characters and no character classes,
which is not what the server accepts. If the rule changes in the Supabase dashboard, change
that file too; nothing detects the drift.

The current TypeScript configuration does **not** enable:

```text
strict
strictNullChecks
noImplicitAny
```

and:

```text
@typescript-eslint/no-unused-vars
```

is disabled.

Do not assume the compiler is enforcing null safety.

---

# Product Direction

The product should continue moving toward a financial experience that is:

- simpler,
- clearer,
- more useful,
- more trustworthy,
- and easier for normal users to understand.

Potential future product areas may include:

- stronger financial insights,
- better forecasting,
- richer annual trends,
- improved savings planning,
- clearer budget recommendations,
- more automation,
- better onboarding,
- and deeper financial visibility.

Any future feature should support the core question:

> Does this help the user understand or manage their money better?

---

# Writing Style

The application is Hebrew-first.

**The brand is spelled שילמן פייננס, with two yuds.** It was spelled both ways until
2026-10-20: the login, onboarding and terms screens had פייננס, while the page title, the
in-app header and the auth emails had פיננס - so a user got a mail saying one thing and
landed on a screen saying the other. Note that פיננסי, the ordinary adjective, is unrelated
and keeps its single yud: "ניהול פיננסי חכם" is correct and must not be swept up in a
find-and-replace.

User-facing copy should be:

- clear,
- short,
- practical,
- reassuring without being patronizing,
- financially precise,
- easy to understand.

Avoid:
- financial jargon where plain Hebrew is enough,
- overly formal banking language,
- vague motivational copy,
- technical database terminology.

For this repository, avoid typographic em dashes or en dashes in prose, comments, commit messages, documentation and UI strings.

Use a normal hyphen:

```text
-
```

instead.

---

# Final Product Principle

Cash Flow is not valuable because it stores financial records.

It is valuable when the user can look at the product and quickly understand:

- where they stand,
- what changed,
- what needs attention,
- and what they should do next.

Financial correctness and clarity are the foundation of the product.

---

## Skills and where they live

- Project skills live in `.claude/skills/` in this folder and load automatically. Relevant here: `deploy`, `db-change`, the Cloudflare/Workers skills (`cloudflare`, `wrangler`, `workers-best-practices`, `durable-objects`, `agents-sdk`, `turnstile-spin` and related), and the design skills (`web-design-guidelines`, `apple-design`, `emil-design-eng`, `review-animations` and the rest of the Emil pack). Cloudflare skills that are not in `.claude/skills/` are in `~/.cursor/skills/`.
- Any machine, or when this computer is not reachable: read-only copy in GitHub `arielelya/claude-library` under `projects/shilman-cash-flow/` (general skills under `global/skills/`). Accounts per service: `reference/accounts.md` there.
- This computer is the source of truth. After changing a skill or this file here, push the same change to the repo.
