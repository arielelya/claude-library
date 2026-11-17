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
- what recurring expenses are coming,
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
| `/budget` | הוצאות | Monthly budget / expense management, planned vs actual, carryover, categories, transactions and recurring transactions |
| `/goals` | מטרות | Savings goals, milestones, progress and due-date awareness |
| `/investments` | השקעות | Investment portfolios and value history |
| `/annual-summary` | סיכום שנתי | Annual financial summary, monthly trends, categories and year-over-year comparison |
| `/settings` | הגדרות | User profile, currency, operating mode, theme, password and account management |

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

Switching modes goes through the `set_budget_mode` RPC. It is idempotent, never touches transactions or the current month's plans, and re-derives the months after the current month: no plan in tracking mode, the current month's plan in budget mode. Returning to budget mode after a tracking period starts clean, because the tracking months have no plan.

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
- recurring transactions,
- category drill-down,
- search,
- CSV export.

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

Contributions are capped at the goal target.

Milestones can update overall goal progress through database triggers.

The goal experience should feel motivating but financially grounded.

---

## Investments

Users can create named investment portfolios.

Each portfolio contains a time series of value entries.

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

The annual summary provides a higher-level view using:

```text
yearly_summaries
```

It includes:

- monthly income,
- monthly expenses,
- expenses by category,
- year-over-year comparisons,
- Hebrew observations.

The observations are currently rule-based, not generated by AI.

---

# Financial Insights

The application contains rule-based financial insights through:

```text
useFinancialInsights
```

These compare current and previous periods and produce Hebrew messages.

Insight types include:

- positive,
- warning,
- suggestion,
- achievement.

They are prioritized for display.

There is currently no AI involved in this feature.

---

# Recurring Transactions

Recurring transactions are generated lazily.

Creating a recurring transaction only materializes the current month.

Future months are generated when the user opens them through:

```text
generate_recurring_transactions_for_month
```

Generated transaction rows contain:

```text
recurring_id
```

and database rules prevent direct editing of generated rows.

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

# Currency

Supported display currencies:

- ILS - ₪
- USD - $
- EUR - €

ILS is the default.

Currency is stored in:

```text
profiles.currency
```

This is **display-only multi-currency**.

There is no FX conversion.

Amounts remain the values entered by the user.

Changing currency changes formatting and symbols, not historical financial values.

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

# Repository Location

All commands run from the repository root:

```text
shilman-cash-flow/
```

which currently sits inside a parent:

```text
cash_flow/
```

---

# Commands

```bash
npm run dev
# Vite development server on http://localhost:8080

npm run build
# Production build -> dist/

npm run typecheck
# tsc --noEmit

npm run lint
# eslint .

npm run test
# vitest run

npm run test:watch
# vitest watch mode

npm run test:db
# node test-runner.mjs - integration tests against the live Supabase project

npm run test:all
# vitest run && node test-runner.mjs
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
RecurringTransactions
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
4. expose a `refreshX()` function.

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
generate_recurring_transactions_for_month
recalculate_budget_chain
recalculate_forward
recalculate_balance
recalculate_yearly_summary
set_category_plan
set_budget_mode
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

`BudgetsContext` listens for this event and re-fetches after a 600ms debounce so database-triggered calculations are reflected in the UI.

## Recurring transaction changes

`RecurringTransactionsContext` dispatches:

```text
recurring-transactions-changed
```

and `TransactionsContext` listens for it.

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
transaction Zod schema
validate_transaction_date, validate_budget_edit (database)
```

Search in `BudgetSearchPanel` still looks back 12 months, because it only views data.

Transactions beyond the end of the current month are also blocked.

---

# Categories

Categories are soft-deleted rather than physically removed.

Deletion sets:

```text
is_active = false
deleted_at = ...
```

This preserves historical transaction relationships.

Normal category reads filter:

```text
is_active = true
```

Categories are ordered by:

```text
position
```

and drag-and-drop ordering uses:

```text
dnd-kit
```

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

The project contains approximately 160 timestamped migrations under:

```text
supabase/migrations/
```

These define:

- schema,
- triggers,
- RPCs,
- RLS policies,
- financial behavior.

Edge Functions live under:

```text
supabase/functions/
```

Current functions include:

```text
delete-account
market-data
copy-user-data
cleanup-unconfirmed-users
generate-month
recalculate-yearly-summary
```

JWT verification configuration is defined in:

```text
supabase/config.toml
```

---

# RLS and User Isolation

Every domain table is scoped through:

```text
user_id
```

and protected using Supabase Row Level Security.

Client queries also explicitly filter with:

```ts
.eq('user_id', user.id)
```

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

Fields include:
- display_name
- avatar_url
- currency
- budget_mode
- is_onboarded

## Categories

```text
categories
```

Includes:
- income / expense type,
- planned amount,
- icon,
- position,
- soft-delete fields.

## Transactions

```text
transactions
```

Includes:
- amount,
- transaction_date,
- notes,
- recurring_id.

## Recurring Transactions

```text
recurring_transactions
```

Includes:
- amount,
- day_of_month,
- start_date,
- end_date,
- is_active.

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

```text
yearly_summaries
```

Contains cached JSON rollups including:

```text
monthly_data
expenses_by_category
expenses_by_category_by_month
```

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

The following components currently exist but are not rendered in live pages:

```text
SavingsPlannerCard
CategoryChart
```

Treat them as dormant code, not current product behavior.

`HeroStrip` is the shared page header for most major sections except the dashboard.

---

# TypeScript

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
