# VELE — Shopify Website

Working instructions for Claude on the VELE store (velewellness.com). Read fully at the start of every session.
Anything written as a plain statement is approved and decided. Only items that are not yet decided carry a label: **[Proposal]** = under consideration, **[Open]** = needs Ariel's decision. Do not act on labeled items without asking.

## 0. Start of every session
1. Read this file. Reference docs are in `docs/` next to it (see section 11).
2. Check which theme is live before touching anything: list the themes through the Shopify API and look at `role` (`MAIN` = live). Never trust theme names (section 7).
3. Work only on an unpublished draft theme. Verify with screenshots and checks, then tell Ariel what changed. Ariel publishes herself.
4. Anything that affects the live site immediately (menus, collections, products, policies, pages are store data, not theme code) needs a clear heads-up to Ariel, ideally before, and always in your report.
5. If you are not sure what Ariel wants, ask (section 1 says how).

## 1. How to work with Ariel
- Ariel is the founder of VELE. Communicate in Hebrew, feminine forms, concise, clear, practical. Code, comments, and commit messages in English.
- Do not agree automatically. Challenge assumptions, flag problems and risks, and propose a better alternative when there is one. The goal is the best result, not approval.
- Explain design and development decisions in terms of what they do for the brand and the shopping experience, not technical detail for its own sake.
- Plain language: Ariel is not a developer. Explain any technical term in one simple sentence the first time (for example SEO, meta description, variant, collection). If she says she did not understand, explain again more simply with an example, do not repeat the same wording.
- Questions: when you need a decision, ask with multiple-choice options she can click (the question tool), each option with one line on what it leads to. She can always answer in her own words.
- Small decisions: move forward independently. Ask when missing information materially changes the result, or when you are not sure. Never guess on brand, legal, pricing, or product facts.
- Always separate approved decisions from proposals in what you report.
- Never publish a theme, delete anything, or change money-related or legal content without her explicit yes in the current conversation.
- After finishing: report what changed, what was verified (and where), what is not done and why. Short, no step-by-step recap.

## 2. Brand
- **VELE** — "sails" in Italian: wind, movement, direction, progress.
- Tagline: "Trust Your Wind." Use this exact wording everywhere on the site (never "Trust the Wind"). It appears once on the homepage, in the hero. "JOIN THE WIND" in the signup area is a different phrase and stays.
- Positioning: premium-accessible luxury wellness. Starts with women's activewear, expands later to wider wellness and menswear. Clothing that works for the workout and for everyday life: quality, comfort, aesthetics.
- Values: movement, health, discipline, personal growth, quality.
- Market: Israel first (US later, not now).
- Audience: women 25–45, active, care about aesthetics and wellness. Looking for flattering, high-quality activewear that works beyond the studio. The site should feel ambitious and stylish, yet welcoming.
- Anti-positioning: not loud, not cluttered, not childish, not discount-driven.

## 3. Design direction
- Reference: Alo Yoga (plus the "Apple precision / Dior quiet luxury" feel from the brand foundation). Build an independent VELE identity, do not copy.
- Look: premium, clean, feminine, minimalist, urban. Generous spacing, clear hierarchy, precise typography.
- Photography: product shots plus lifestyle. Soft natural warm light, editorial, nothing that looks like stock or dropshipping.
- Avoid: clutter, oversized logos, heavy effects, aggressive sales messaging, aggressive popups.
- Rule of thumb: when in doubt, do less.

### Palette
Brand palette vs. where it lives in the theme:

| Brand color | HEX | Theme palette slot (`settings.color_palette`) |
|---|---|---|
| Cream | #F8F6F1 | `background` |
| Charcoal | #242421 | `foreground` (text / headings, never pure black) |
| Stone | #DCD6CC | `color1` (swatch borders, light text over photos) |
| Brown | #54463A | `color2` (primary button border/text, selected variant, hero overlay) |
| Navy | #323B61 | `color3` (currently almost unused) |
| Olive | #5E6656 | `color4` (sale badge) |

- The brand palette is a **guideline**, not a rule that every color must appear. Use only the colors a design actually needs. The theme palette was aligned to it on Nov 17, 2026.
- Brand colors are not necessarily product colors in a drop.
- Default: do not add colors outside this palette. Use tints of existing ones: hairlines `rgb(36 36 33 / 0.10)`, secondary text `rgb(36 36 33 / 0.68)`.
- If a design really needs a new color: do not add it on your own. Show Ariel the color (HEX plus a visual swatch or preview), explain where it would be used and why the existing palette is not enough, and wait for her approval.
- Palette values live in `config/settings_data.json`, but some hex codes are also hard-coded in `templates/index.json` (hero overlay and text) and in the custom wishlist CSS. Update all places when the palette changes.

### Typography
- Brand identity: logo in Cormorant Garamond, tagline in Cardo. These define the identity; they are not the fonts for all site text.
- Theme fonts: headings Cardo (400), body Inter (400), Hebrew headings Bellefair. No other typefaces.
- Labels, eyebrows, nav: uppercase with letter-spacing (about 0.06–0.1em) instead of bold weight.
- Use the theme variables (`var(--font-heading--family)`, `var(--font-body--family)`), never hard-coded fonts.

### Components (as implemented in the Horizon theme)
- Sharp corners on product images and cards (radius 0). Soft rounding only on inputs (8px) and popovers (4px).
- Primary button: transparent with Brown (#54463A) border and text. A solid charcoal Add-to-cart as the main action is a **[Proposal]**.
- Cart is a drawer. Thin-stroke icons. Subtle motion only: product-card hover zoom, second image on hover, checkmark on add-to-cart.
- Logo: wordmark only (`VELE_logo_black.png`), small and quiet in the header. No symbol yet.

## 4. Content and catalog rules
- Copy: concise, confident, refined, natural voice. Same voice across homepage, product pages, cart, and emails.
- **Never invent** reviews, product features, certifications, prices, availability, or shipping and return terms. Product pages carry only **verified** information on fit, fabric, sizing, care and shipping, taken from what Ariel confirmed. Where info is missing, leave a clear placeholder and tell her.
- Do not present planned products as available for purchase.
- The initial assortment is small. Build richness through photography, styling, and product and color combinations, not filler.
- Mobile first: simple navigation, easy size and color selection, a prominent add-to-cart, tap targets of at least 44px.
- Drop 01 core styles in development: Full-Length Leggings (high waist, no front seam), Biker Shorts (high-waisted), Essential Bra (removable pads), Built-In Cup Bra (fixed cups). English product names are working names until approved as customer-facing names.
- Store state (Nov 17, 2026): the store holds 7 sample products (Essential Bra, Cross Back Bra, Breeze Studio Tank, Daily Soft Tee, High-Waist Sculpt Legging 25", High-Waist Sculpt Biker Short 5", Grip Socks). They do not match the four core styles above. Treat prices and names as samples, and do not assume the catalog is final. Only Essential Bra has size variants (12 variants), the rest have one.
- Navigation: SHOP ALL, TOPS, LEGGINGS, ACCESSORIES, NEW. All upper-body items, including bras, stay under TOPS. No separate BRAS item. (A "Bras" collection exists but is not linked.)

## 5. Language and RTL
- The site is bilingual: **Hebrew is the default**, with a language switcher to English.
- Hebrew and English layouts should look identical. Only the text changes, with correct RTL alignment. Prefer CSS logical properties (`margin-inline-start`, `text-align: start`) over left/right.
- Hebrew copy: feminine address to the customer, natural, elegant, premium. Never a literal translation from English.
- Menu items, product names, and key English taglines stay in English. Everything else is natural Hebrew.
- Price format: ₪120 (no decimals) unless a real price requires them.
- Check in both languages: mixed Hebrew/English lines, numbers and prices inside RTL text, icons and arrows that need mirroring, the language switcher, cart and checkout.

## 6. Store facts
- Shopify store, theme **Horizon**, domain velewellness.com (admin store handle: bjvyip-wk.myshopify.com). Currency ILS, VAT 18%, only the Israel market is active.
- Contact: hello@velewellness.com (also the order-email sender). Instagram: @vele.wellness (the footer also links a Facebook page). There is no TikTok or YouTube account.
- Customer accounts: Shopify New Customer Accounts with Google sign-in (live). Facebook sign-in deliberately deferred.
- Legal pages live under `/policies/` (terms-of-service, refund-policy, shipping-policy, privacy-policy, contact-information) plus `/pages/accessibility`. **They are the source of truth for returns, shipping, and fees. Never copy numbers from other documents or from memory.** Older documents disagree with each other (for example return window and shipping time).
- Help pages that exist: about ("The VELE Way"), faq, shipping-returns, track-my-order, size-guide, contact, accessibility.
- Welcome popup offers 10% off the first order (code `WELCOME10`).

## 7. Technical map and gotchas
Tools: the Shopify connector gives theme tools (`theme_bash` to read and edit theme files in a draft, `theme_commit` to save, `theme_screenshot` to preview, `theme_publish`) and the Admin GraphQL API.
- **Theme names are misleading.** On Nov 17 the published theme was called "VELE - draft (16 Nov)" while "VELE - live" was unpublished. Check `role` (`MAIN` = live). As of Nov 17, 2026 the live theme is "VELE - draft (17 Nov)" and "VELE - live" is an unpublished backup.
- `theme_publish` refuses themes the agent did not create. Ariel publishes from Online Store > Themes.
- `theme_bash` cannot read the live theme and is rate limited ("busy, try in 60 seconds"). Batch related reads and edits into one script.
- `theme_screenshot` renders without full styling fidelity (for example grids can look broken). Use it to check content, not pixel-level design. Final visual checks need a real browser.
- Config files (`config/settings_data.json`, `sections/*-group.json`) start with a comment header and are single-line JSON. Use `jq --jsonc` or skip the first 9 lines, and keep the header when rewriting.
- Where things live: palette in `config/settings_data.json` (`color_palette`); social URLs in the same file; footer links are hard-coded button blocks in `sections/footer-group.json` (the "footer" menu is unused); homepage content in `templates/index.json`; welcome popup in `snippets/welcome-popup.liquid` plus its trigger in `assets/vele-custom.js`; custom styles in `assets/vele-custom.css`.
- Apps in the theme: PageFly and Swishlist (wishlist, with its own custom CSS in `settings_data.json` and `vele-custom.css`), plus an Instafeed section. Files named `*.gem-*` and `*gp-template-bk*` are old page-builder backups. Do not edit them unless asked.
- Menus, collections, products, pages and policies are **store data**, not theme code. Changing them is live immediately and applies to every theme. Never fake a data change in theme code.
- Admin API (version 2026-10): `collectionByHandle` and `Collection.ruleSet` are deprecated. Use `collectionByIdentifier` and `Collection.sources`, and edit with `collectionUpdate(collection: CollectionUpdateInput)` using `sourcesToUpdate`. The TOPS collection is a tag condition (`top`). `menuUpdate` replaces the whole item list, so pass the existing item ids.

## 8. Implementation workflow
- Make changes in a draft copy, verify, then Ariel publishes. Never edit the live theme directly.
- Prefer native Shopify and Horizon capabilities (theme settings, sections, blocks, metafields) over custom code.
- Custom code: organized and maintainable, one clearly named file or section per feature. Do not stack CSS patches that fight each other. Before adding CSS, check whether an earlier patch already covers the area, and consolidate instead.
- Keep performance (image sizes, no heavy scripts or apps), accessibility (contrast, focus, alt text, IS 5568 / WCAG AA direction), and the purchase flow working.
- Test on mobile and desktop, in Hebrew and English, including add-to-cart, cart drawer, and wishlist.

## 9. Deferred on purpose (do not raise as urgent)
Current stage: samples, not photography or launch.
- **Payment provider:** until the photography/launch stage. Shopify Payments is not available in Israel, so the realistic path is an Israeli provider (PayPlus via iCount was researched). Until then, consider hiding empty express-checkout pills.
- **Product descriptions** (fabric, fit, care): until specs are final. **Product galleries (4–6 images):** until photography. **Reviews:** after the first real orders. Choosing the app is fine, installing is not.
- **Instagram gallery on the site:** only once @vele.wellness has at least 9 clean, coherent posts.
- **WhatsApp Business and a dedicated business number:** at the website-launch stage.
- **Facebook sign-in, full technical accessibility audit, US/EU markets:** later.

## 10. Current backlog and open decisions (updated Nov 17, 2026)
Done on Nov 17: theme colors aligned to the brand palette; tagline set to "Trust Your Wind."; footer Help block links to terms, refund, shipping, contact information and accessibility; footer social icons fixed; "Shop All" title; the welcome popup is exit-intent on desktop and delayed on mobile.

Backlog, in rough priority order:
1. SEO: homepage title is just "VELE", no meta description, og/twitter data empty. Needs approved copy (Hebrew and English) before changing.
2. Button hierarchy on product pages: re-check whether the wishlist button is heavier than add-to-cart.
3. Three email-capture points (popup, homepage block, footer). Decide whether to consolidate.
4. Mobile: header icons about 16px, menu close button tiny. Raise to 44px tap targets (verify in a real narrow browser first).
5. Unfinished-looking blocks: video strip with native player controls, "Made For Movement" banner with baked-in text, "Shop the Look" hotspots.
6. Mobile scan not yet completed (needs a real narrow viewport).

Ideas from competitor research (Alo, Lululemon, Vuori, Skims, Sporty & Rich) are **proposals**, not decisions. See `docs/VELE_Shopify_Improvement_Ideas.md`.

Open decisions for Ariel:
- Final customer-facing product names, and which products are really in Drop 01.
- Return and shipping terms to show on product pages (check against the policy pages first).
- Logo: wordmark only for now, or a symbol too.

## 11. Reference documents
In `docs/` next to this file:
- `VELE_Shopify_Settings_Checklist.md`: store configuration and legal status.
- `VELE_Shopify_Improvement_Ideas.md`: Nov 8 review and competitor ideas (condensed).
Only in the claude.ai Project "wellness brand" (not on this computer): `VELE_Visual_Identity.md`, `VELE_Site_Audit.md` (Aug 2026, partly outdated), `VELE_About_Page_Draft.md`, and the PDFs `VELE Brand Foundation`, `VELE Drop 01`, `VELE 1`.
When documents conflict, the live store and the policy pages win, then Ariel's latest instruction.

## 12. Skills and where they live
- Project skills go in `.claude/skills/` in this folder (none yet). Useful skills from the library `arielelya/claude-library`: `frontend-design` (in `global/skills/`), `web-design-guidelines` and `webapp-testing` (in `projects/shilman-cash-flow/skills/`).
- Any machine, or when this computer is not reachable: read-only copy of this file and its docs in GitHub `arielelya/claude-library` under `projects/vele/`. Accounts per service: `reference/accounts.md` there.
- This computer is the source of truth. After changing a skill or this file here, push the same change to the repo.
