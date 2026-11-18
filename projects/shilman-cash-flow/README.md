# Shilman Finance

A personal finance web app for tracking transactions, budgets, goals, and investments.
Built in Hebrew (RTL) with a navy and orange theme.

## Features

- **Transactions** — add, edit, and delete income/expense entries with category and date
- **Budgets** — monthly planned vs. actual tracking per category, with carryover support
- **Categories** — fully customizable income/expense categories
- **Goals** — savings goals with milestones and progress tracking
- **Investments** — track investment entries over time
- **Annual Summary** — yearly breakdowns with month-over-month and year-over-year comparisons
- **Multi-currency** — currency selection per user
- **Authentication** — email/password sign-in via Supabase Auth

## Tech Stack

- **Frontend**: Vite, React 18, TypeScript
- **UI**: shadcn-ui, Tailwind CSS, Radix primitives
- **Backend**: Supabase (PostgreSQL, Auth, Storage)
- **Routing**: React Router
- **Forms / validation**: React Hook Form, Zod
- **Charts**: Recharts
- **Date handling**: date-fns

## Local Development

Requires Node.js (LTS) and npm.

```sh
# Clone
git clone <YOUR_GIT_URL>
cd shilman-cash-flow

# Install
npm install

# Configure environment
# Create .env with:
#   VITE_SUPABASE_URL=...
#   VITE_SUPABASE_ANON_KEY=...

# Run dev server
npm run dev
```

The dev server runs on `http://localhost:8080` by default.

## Available Scripts

- `npm run dev` — start the development server
- `npm run build` — production build
- `npm run preview` — preview the production build locally
- `npm run lint` — run ESLint

## Project Structure

```
src/
  components/      UI components (modals, dashboard, settings, etc.)
  contexts/        Global state providers (transactions, budgets, goals, etc.)
  hooks/           Reusable React hooks
  integrations/    Supabase client and generated types
  lib/             Utility helpers (finance math, date utils, schemas)
  pages/           Top-level routed pages
```

## Deployment

This project was originally bootstrapped with [Lovable](https://lovable.dev) and can be deployed via Lovable's publish flow, or built and deployed to any static host (Vercel, Netlify, Cloudflare Pages) — the app is a pure static SPA that talks directly to Supabase.
