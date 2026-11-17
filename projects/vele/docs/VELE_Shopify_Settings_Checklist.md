# VELE — Shopify Admin Settings Checklist
### Pre-launch readiness review of store configuration (as opposed to the page-content audit)

Live-checked directly in the Shopify admin. Organized by urgency.

**Current stage (as of Nov 8, 2026): samples, not photography/launch yet.** Payment-provider setup is intentionally deferred until the photography stage begins. Everything else can be picked off whenever there is a spare few minutes.

---

## Resolved — Aug 23, 2026

Terms of Service, Refund/Returns & Exchanges, Shipping, and Privacy policies are all live and correct. Final wording is Ariel's own: competitive commercial return terms (14 days, first exchange free, ₪20 return / ₪25 additional exchange fee, free cancellation before dispatch) layered on top of, not overriding, statutory Israeli consumer-protection rights, including Amendment 13 to the Privacy Protection Law for the Privacy Policy. Published to Shopify's policy pages:
- https://velewellness.com/policies/terms-of-service
- https://velewellness.com/policies/refund-policy
- https://velewellness.com/policies/shipping-policy
- https://velewellness.com/policies/privacy-policy

(These pages are the source of truth for returns, shipping and fees. Other older documents may disagree.)

## Resolved — Nov 8, 2026

- **Business registration (עוסק מורשה) is in, and the legally-required Contact Information policy is fully filled in:** https://velewellness.com/policies/contact-information (trade name, phone, email, street address, VAT number, trade number). It is automatically surfaced in the Checkout footer.
- **Google sign-in is live and verified in production** (Shopify New Customer Accounts, Social sign-in, Google OAuth client, publishing status In production).
- **Facebook/Meta sign-in deliberately deferred.** Meta Business Verification needs a company registration or a sole-proprietor certificate. Launching Google-only for now.
- **Accessibility Statement page published:** https://velewellness.com/pages/accessibility (IS 5568 / WCAG 2.0 AA commitment, known limitations, feedback contact). A full technical accessibility audit is not urgent yet.
- **Phone number:** not a legal requirement for the distance-sale disclosure (name, business number and address are). Using the personal number publicly is a choice. Customer-service decision: publish the number now, convert it to WhatsApp Business later; email (hello@velewellness.com) stays the official written channel.
- **Order-notification sender email** switched to hello@velewellness.com.

## Resolved — Nov 17, 2026
- Footer Help block now links to Terms, Refund Policy, Shipping Policy, Contact Information and Accessibility Statement.

---

## Launch blockers

**1. No payment provider is active.** Settings → Payments shows no provider, and PayPal is "Setup incomplete". Shopify Payments/Stripe are not available in Israel; PayPlus via iCount is the realistic path. **Intentionally deferred** until photography/launch prep begins.

## Important before real customers arrive

**2. Store owner account has no two-factor authentication.** Settings → Users → Security. Two-minute setup.

**3. Confirm the phone number is also set in Settings → General → Store contact details** (consistency, not compliance).

**4. International shipping rates exist but are not usable yet.** An "International" zone with a ₪57 rate exists, but those countries are not in any Market. Not urgent (Israel first).

## On the radar for later

**5. Only the Israel market is active.** Shopify suggests US and EU markets for when expansion starts.

**6. Full technical accessibility audit** (contrast, keyboard navigation, screen reader) once there is meaningful traffic.

**7. Customer-service phone setup, deferred to the website-launch stage:** convert the number to WhatsApp Business (business name/logo, hours, in-brand greeting and away messages), keep email as the official channel, and later get a dedicated business number.

**8. Instagram gallery on the site (@vele.wellness), deferred until the profile has at least 9 clean, coherent posts.**

---

## Already in good shape
- Business entity and store address (Israel, Giv'at Shmuel).
- ILS currency, Israel VAT 18%, tax service active.
- Domestic shipping rates configured: ₪35 standard (free over ₪250), 3–5 business days.
- Checkout configuration, one active fulfillment location, billing active.
- Legal policies, Contact Information and Accessibility Statement live.
- Google sign-in live. Sender email on hello@velewellness.com.
