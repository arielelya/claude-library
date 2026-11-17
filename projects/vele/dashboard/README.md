# VELE — Operations Dashboard

An internal CRM/ops platform for the VELE wellness brand: pricing, inventory,
orders, shipments and customers, all driven by editable backoffice settings,
with an API for your website to feed data in automatically.

Runs locally against a SQLite file. No cloud account, no subscription, and your
business data never leaves the machine.

---

## Getting started

```bash
npm install
npm run db:reset   # creates data/vele.db and seeds 120 days of sample trading
npm run dev        # http://localhost:4000
```

When you're ready to replace the sample data with real data, delete the products,
customers and orders from the UI — or wipe and start clean:

```bash
rm data/vele.db && npm run dev   # empty database, schema created automatically
```

Then set your real values in **Backoffice** and add products under
**Products & Pricing → Add product**.

---

## What each screen does

| Screen | Purpose |
| --- | --- |
| **Overview** | 30-day revenue, gross profit, VAT collected, AOV. Order pipeline counts, restocking list, shipments past ETA. |
| **Orders** | Filter by status, payment and source. Open an order to move it through the pipeline, edit lines, adjust charges, dispatch it and read its full history. |
| **Shipments** | Every dispatch with carrier, tracking, ETA and delivery status. Flags anything past its ETA. Tracking numbers become clickable carrier links. |
| **Inventory** | On hand vs reserved vs available, stock value at cost and retail, and an append-only movement ledger explaining every change. |
| **Products & Pricing** | Cost, price ex/inc VAT and margin per product, editable inline and saved in bulk. Every price change is logged. |
| **Customers** | Lifetime value, order counts and history, contact details and tags. |
| **Expenses** | Every payment behind the business: spend by month, category and vendor, FX and payment fees, invoice coverage and a review queue. Fills itself from invoices dropped in `../Expenses/Invoices`. |
| **Backoffice** | VAT rates, currency, order numbering, low-stock threshold, working days, carriers, and shipping methods with handling + transit times. |
| **Integrations** | Shopify connection, API keys, and the sync activity log. |

---

## How the money works

Getting this wrong is expensive, so the rules are strict and enforced in one place:

- **All money is stored as integers in agorot** (`price_minor`, `total_minor`, …).
  Floating-point money drifts; integers don't. `src/lib/money.ts` is the only
  place conversion and rounding happen.
- **All tax rates are basis points.** `1800` = 18.00%.
- **Catalog prices are stored excluding VAT.** Whether the storefront *displays*
  inclusive prices is a backoffice toggle, not a change to stored data.
- **Order lines snapshot price, cost and tax rate at the time of sale**, so
  repricing your catalog never rewrites history.
- **Order-level discounts are allocated across lines in proportion to value**,
  so each line is taxed at its own rate on the correctly discounted amount. The
  rounding remainder lands on the largest line.
- **Revenue figures exclude cancelled and refunded orders** everywhere.

## How stock works

`products.stock_on_hand` is a running balance; `inventory_movements` is the
append-only ledger that explains it. `src/lib/inventory.ts` is the only module
allowed to change the balance.

```
available = stock_on_hand − stock_reserved
```

Stock follows order status automatically:

| Order status | Effect on stock |
| --- | --- |
| pending / confirmed / processing / packed | Reserved (still on the shelf, not promisable to anyone else) |
| shipped / delivered | Reservation released, units deducted, `sale` movement logged |
| cancelled / refunded | Reservation released; if already dispatched, units are returned to stock |

Transitions are modelled as "undo the old state, then apply the new one", so
correcting a mistake (e.g. shipped → processing) stays accurate instead of
silently drifting.

---

## Connecting your website

### Shopify

1. Shopify admin → **Settings → Apps → Develop apps** → create an app with
   `read_orders`, `read_products`, `read_customers`.
2. Put the credentials in `.env.local` (see `.env.example`):
   ```
   SHOPIFY_ADMIN_TOKEN=shpat_...
   SHOPIFY_WEBHOOK_SECRET=...
   ```
3. Add webhooks for `orders/create` and `orders/updated` pointing at
   `https://your-host/api/shopify/webhook`.
4. Restart the server.

Webhook signatures are verified with HMAC-SHA256 against the raw request body;
unsigned or tampered requests are rejected with a 401. Re-delivery of the same
order is detected and ignored rather than duplicated.

### Any other platform

Generate a key under **Integrations**, then POST orders:

```bash
curl -X POST http://localhost:4000/api/ingest/orders \
  -H "Authorization: Bearer vele_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "web-1042",
    "payment_status": "paid",
    "customer": { "name": "Noa Levi", "email": "noa@example.com", "city": "Tel Aviv" },
    "items": [{ "sku": "VL-MAG-60", "qty": 2 }]
  }'
```

Behaviour worth knowing:

- **Prices come from your catalog**, not the payload, whenever the SKU is known —
  the website cannot post a price the dashboard disagrees with.
- **Unknown SKUs are rejected** (422) rather than silently priced at zero.
- **`external_id` is idempotent**: re-posting returns the existing order instead
  of creating a duplicate.
- Customers are matched on email; stock is reserved on creation.
- Only the SHA-256 hash of each API key is stored. The plaintext is shown once,
  at creation, and is unrecoverable afterwards.

Every inbound request is recorded in the sync log on **Integrations**, including
rejections and why.

---

## Expenses & invoices

Drop an invoice (PDF or a photo of a receipt) into `../Expenses/Invoices` and
it appears under **Expenses** within seconds, categorised. The folder is watched
while the dashboard runs; files added while it was off are picked up on the next
start. **Expenses → Invoices & categories** shows every file and what became of it.

How a file is filed:

1. **Read on this Mac.** `scripts/invoice-text.swift` (compiled on first use into
   `data/.bin/`) reads the PDF text layer, with on-device OCR for scans and photos.
   Nothing is uploaded. Needs the Xcode Command Line Tools (`xcode-select --install`).
   Vision OCR has no Hebrew, so a *scanned* Hebrew receipt needs manual entry; a
   digital Hebrew PDF reads fine.
2. **Parsed.** Alibaba receipts, Shopify bills and PayPal transactions are read
   exactly, including the contract FX rate and processing fee. Anything else goes
   through a generic reader and is always sent to review.
3. **Matched or created.** A file whose amount matches a payment already recorded
   without a document (within 10 days) is attached to it, and any disagreement in
   the ₪ amount is flagged. Otherwise a new expense is created. Identity is the
   file's SHA-256, so renaming or moving a file never duplicates it.
4. **Categorised.** The vendor's history decides; a vendor with several categories
   (Shopify: plan vs domain) is split by the invoice wording; new vendors get a
   keyword suggestion and wait in review. Confirming or correcting a category
   teaches the rule for next time.

Money follows the same rules as the rest of the app, plus FX: each expense stores
the billed amount in its own currency, the rate as integer micro-units
(3.043702 → `3043702`), and the ₪ actually charged. **Fees = charged − billed × rate.**

**Storage.** Expenses live in their own file, `data/expenses.db`, which
`npm run db:reset` does not touch — it holds real bookkeeping, so back it up.
On first start the 2026 Excel report is imported before any invoice is filed, so
the existing invoices attach to its rows. **Export CSV** gives the same columns back
for the accountant.

Overrides (`.env.local`): `VELE_EXPENSES_DB_PATH`, `VELE_INVOICES_DIR`,
`VELE_EXPENSE_WORKBOOK`, and `VELE_WATCH_INVOICES=0` to disable the watcher.

---

## Verifying it still works

```bash
npm run dev              # in one terminal
node scripts/verify.mjs  # in another
```

32 assertions covering API auth, webhook signature verification, VAT
arithmetic, idempotency, stock reservation, dispatch deduction and refund
restocking. It cleans up after itself.

---

## Project layout

```
src/lib/          the engine — all business rules live here
  schema.sql      database schema, heavily commented
  money.ts        money & tax arithmetic (the only place rounding happens)
  inventory.ts    stock ledger (the only place stock_on_hand changes)
  orders.ts       totals, tax allocation, status transitions
  create-order.ts shared order creation for manual entry, API and Shopify
  settings.ts     backoffice settings with defaults
  expenses/       expenses module, with its own schema.sql and database file
    ingest.ts     folder scan, matching and filing of invoice files
    parse.ts      invoice readers (Alibaba, Shopify, PayPal, generic)
    categories.ts categories and learned vendor rules
    watcher.ts    Invoices folder watcher, started from src/instrumentation.ts
  actions/        server actions — every mutation the UI can perform
src/app/          pages and API routes
src/components/   shared UI
scripts/seed.mjs  sample data
scripts/verify.mjs end-to-end checks
```

## Notes and current limits

- **No authentication.** It binds to localhost and is intended for a single
  operator on one machine. Add auth before exposing it to a network.
- **Single warehouse, single currency at a time.** Changing currency in
  Backoffice changes the display symbol; it does not convert historical figures.
- **No product variants yet** — each size/flavour is its own SKU.
- Uses Node's built-in `node:sqlite`, so there are no native dependencies to
  compile. Requires Node 22+.
- The schema is plain SQL and portable to Postgres or Cloudflare D1 when you
  outgrow local-only.
