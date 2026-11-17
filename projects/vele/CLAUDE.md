# VELE — Shopify Website

Working instructions for Claude on the VELE store (velewellness.com). Read fully at the start of every session.
Anything written as a plain statement is approved and decided. Only items that are not yet decided carry a label: **[Proposal]** = under consideration, **[Open]** = needs Ariel's decision. Do not act on labeled items without asking.

## 1. How to work with Ariel
- Ariel is the founder of VELE. Communicate in Hebrew, feminine forms, concise, clear, practical. Code, comments, and commit messages in English.
- Do not agree automatically. Challenge assumptions, flag problems and risks, and propose a better alternative when there is one. The goal is the best result, not approval.
- Explain design and development decisions in terms of what they do for the brand and the shopping experience (not technical detail for its own sake).
- Small decisions: move forward independently. Ask only when missing information materially changes the result, or when you are not sure what to do. Never guess on brand, legal, pricing, or product facts.
- Always separate approved decisions from proposals in what you report.

## 2. Brand
- **VELE** — "sails" in Italian: wind, movement, direction, progress.
- Tagline: "Trust Your Wind." Use this exact wording everywhere on the site (never "Trust the Wind").
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
Brand palette (identity) vs. what is actually implemented in the theme today:

| Brand color | HEX | Theme palette slot (`settings.color_palette`) |
|---|---|---|
| Cream | #F8F6F1 | `background` |
| Charcoal | #242421 | `foreground` (text / headings, never pure black) |
| Stone | #DCD6CC | `color1` (swatch borders, light text over photos) |
| Brown | #54463A | `color2` (primary button border/text, selected variant, hero overlay) |
| Navy | #323B61 | `color3` (currently almost unused) |
| Olive | #5E6656 | `color4` (sale badge) |

- The brand palette is a **guideline**, not a rule that every color must appear. Use only the colors a design actually needs. The theme palette was aligned to the brand palette on Nov 17, 2026 (draft theme "VELE - draft (17 Nov)").
- Brand colors are not necessarily product colors in a drop.
- Default: do not add colors outside this palette. Use tints of existing ones: hairlines `rgb(36 36 33 / 0.10)`, secondary text `rgb(36 36 33 / 0.68)`.
- If a design really needs a new color: do not add it on your own. Show Ariel the color (HEX plus a visual swatch or preview), explain where it would be used and why the existing palette is not enough, and wait for her approval.
- Palette values live in `config/settings_data.json`, but some hex codes are also hard-coded in `templates/index.json` (hero overlay and text) and in the custom wishlist CSS. Update both places when the palette changes.

### Typography
- Brand identity: logo in Cormorant Garamond, tagline in Cardo. These define the identity; they are not the fonts for all site text.
- Theme fonts: headings Cardo (400), body Inter (400), Hebrew headings Bellefair. No other typefaces.
- Labels, eyebrows, nav: uppercase with letter-spacing (about 0.06–0.1em) instead of bold weight.
- Use the theme variables (`var(--font-heading--family)`, `var(--font-body--family)`), never hard-coded fonts.

### Components (as implemented in the Horizon theme)
- Sharp corners on product images and cards (radius 0). Soft rounding only on inputs (8px) and popovers (4px).
- Primary button: transparent with Brown (#54463A) border and text. The audit recommends a solid charcoal Add-to-cart as the main action **[Proposal]**.
- Cart is a drawer. Thin-stroke icons. Subtle motion only: product-card hover zoom, second image on hover, checkmark on add-to-cart.
- Logo: wordmark only (`VELE_logo_black.png`), small and quiet in the header. No symbol yet.

## 4. Store and technical setup
- Platform Shopify, theme **Horizon**, domain velewellness.com. Existing store: **inspect the current structure and code before proposing or changing anything.**
- Currency ILS, VAT 18%, only the Israel market is active. Sender email: hello@velewellness.com. Instagram: @vele.wellness. There is no TikTok account.
- Customer accounts: New Customer Accounts with Google sign-in (live). Facebook sign-in deliberately deferred.
- Wishlist already exists (custom, built earlier with theme patches). Read the existing implementation before touching it.
- Legal pages are live under `/policies/` (terms, refund, shipping, privacy, contact-information) plus `/pages/accessibility`. **They are the source of truth for returns, shipping, and fees. Never copy numbers from other documents or from memory.** (Older documents in the project disagree with each other, e.g. return window and shipping time.)

## 5. Language and RTL
- The site is bilingual: **Hebrew is the default**, with a language switcher to English.
- Hebrew and English layouts should look identical. Only the text changes, with correct RTL alignment. Prefer CSS logical properties (`margin-inline-start`, `text-align: start`) over left/right.
- Hebrew copy: feminine address to the customer, natural, elegant, premium. Never a literal translation from English.
- Menu items, product names, and key English taglines stay in English. Everything else is natural Hebrew.
- Price format: ₪120 (no decimals) unless a real price requires them.
- Check in both languages: mixed Hebrew/English lines, numbers and prices inside RTL text, icons and arrows that need mirroring, the language switcher, cart and checkout.

## 6. Implementation workflow
- Theme names are misleading (Nov 17: the published theme was named "VELE - draft (16 Nov)", while "VELE - live" was unpublished). Always check the `role` (`MAIN` = live) via the API, never trust the name. As of Nov 17, 2026 the live theme is "VELE - draft (17 Nov)"; "VELE - live" is an unpublished backup. The agent cannot publish themes it did not create, so Ariel publishes from Online Store > Themes.
- Before any change, check whether you are on the **live theme or a draft**. Make changes in a draft copy, verify, then publish. Never edit the live theme directly.
- Prefer native Shopify and Horizon capabilities (theme settings, sections, blocks, metafields) over custom code.
- Custom code: organized and maintainable, one clearly named file or section per feature. Do not stack CSS patches that fight each other. Before adding CSS, check whether an earlier patch already covers the area, and consolidate instead.
- Keep performance (image sizes, no heavy scripts or apps), accessibility (contrast, focus, alt text, IS 5568 / WCAG AA direction), and the purchase flow working.
- Test on mobile and desktop, in Hebrew and English, including add-to-cart, cart drawer, and wishlist.
- Footer and menu changes: automation has failed on these twice. Do them manually in the Theme Editor, or ask Ariel to.
- After finishing: report what changed, what was verified (and where), and what remains. Short, no step-by-step recap.

## 7. Deferred on purpose (do not raise as urgent)
Current stage: samples, not photography or launch.
- **Payment provider:** until the photography/launch stage. Shopify Payments is not available in Israel, so the realistic path is an Israeli provider (PayPlus via iCount was researched). Until then, consider hiding empty express-checkout pills.
- **Product descriptions** (fabric, fit, care): until specs are final. **Product galleries (4–6 images):** until photography. **Reviews:** after the first real orders. Choosing the app is fine, installing is not.
- **Instagram gallery on the site:** only once @vele.wellness has at least 9 clean, coherent posts.
- **WhatsApp Business and a dedicated business number:** at the website-launch stage.
- **Facebook sign-in, full technical accessibility audit, US/EU markets:** later.

## 8. Current backlog (updated Nov 17, 2026, in rough priority order)
Navigation decision: all upper-body items, including bras, stay under TOPS. No separate BRAS item in the main menu.
Done on Nov 17: footer Help block now links to terms, refund, shipping, contact information and accessibility; footer social icons fixed (Instagram and Facebook only); "Shop All" title; the welcome popup is now exit-intent on desktop and delayed on mobile.
1. SEO: homepage title is just "VELE", no meta description, og/twitter data empty. Needs approved copy (Hebrew and English) before changing.
2. Button hierarchy on product pages: re-check whether the wishlist button is heavier than add-to-cart.
3. Three email-capture points (popup, homepage block, footer). Decide whether to consolidate.
4. The tagline repeats on the homepage (hero, video strip, footer). Vary or reduce.
5. Mobile: header icons about 16px, menu close button tiny. Raise to 44px tap targets (verify in a real narrow browser first).
6. Unfinished-looking blocks: video strip with native player controls, "Made For Movement" banner with baked-in text, "Shop the Look" hotspots.
7. Mobile scan not yet completed (needs a real narrow viewport).
8. Size selector: only Essential Bra has size variants so far. Other products get them when real products are set up.

Ideas from competitor research (Alo, Lululemon, Vuori, Skims, Sporty & Rich) are **proposals**, not decisions. See the Improvement Ideas doc.

## 9. Open decisions for Ariel
- Final customer-facing product names, and which products are really in Drop 01.
- Return and shipping terms to be shown on product pages (check against the policy pages, and resolve the conflicting older figures).
- Logo: wordmark only for now, or a symbol too.

## 10. Reference documents (in the Project)
- `VELE_Visual_Identity.md`: implemented colors, type, and components (pulled from the live theme, Nov 8).
- `VELE_Shopify_Improvement_Ideas.md`: latest audit and competitor ideas (Nov 8, Hebrew). Newer than the Site Audit.
- `VELE_Shopify_Settings_Checklist.md`: store configuration and legal status.
- `VELE_Site_Audit.md`: older page-by-page audit (Aug 2026). Partly outdated, for example the footer 404s and the zero prices.
- `VELE_About_Page_Draft.md`, `VELE Brand Foundation.pdf`, `VELE Drop 01.pdf`, `VELE 1.pdf`.
- When these documents conflict, the live store and the policy pages win, then Ariel's latest instruction.
