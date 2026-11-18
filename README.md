# claude-library

Index of skills and context files. See `CLAUDE.md` for how this repo is used.

## global/skills
Skills useful in any project. Source: [anthropics/skills](https://github.com/anthropics/skills) (Apache 2.0, license files included).

| Skill | Use for |
|---|---|
| skill-creator | Building, editing and evaluating skills |
| docx | Word documents |
| pdf | PDF files |
| pptx | PowerPoint presentations |
| xlsx | Excel spreadsheets |
| frontend-design | Distinctive, non-generic UI design |
| webapp-testing | Browser automation tests and screenshots (Playwright) |

## reference
| File | Contents |
|---|---|
| accounts.md | Which account belongs to which service (identifiers only, no secrets) |

## projects
| Project | Contents |
|---|---|
| shilman-cash-flow | `CLAUDE.md` (latest version from ~/Developer), `README.md`, `docs/` (APP_REFERENCE, BACKLOG), `supabase/templates/README.md` and `scripts/supabase_sql.py`. Skills: `deploy`, `db-change`, `cloudflare`, `wrangler`, `workers-best-practices`, `web-design-guidelines`, `agents-sdk`, `cloudflare-email-service`, `cloudflare-one`, `cloudflare-one-migrations`, `durable-objects`, `nextjs-on-cloudflare`, `sandbox-sdk`, `sandbox-next`, `sandbox-stable`, `sandbox-migrate-to-next`, `turnstile-spin`, `web-perf`, plus the Emil Kowalski design pack (`animate`, `animate-expo`, `animation-performance`, `animation-vocabulary`, `apple-design`, `ask-emil`, `ask-sonner`, `break-ui`, `choreograph`, `emil-design-eng`, `find-animation-opportunities`, `gestures`, `improve-animations`, `learn-taste`, `mobile-native`, `pick-ui-library`, `prototype`, `remove-animations`, `review-animations`, `write-swift`) |
| shilman | Skills exported from the claude.ai account (the account is their source, this is a backup): `shilman-writer` (WhatsApp/Telegram posts for the investors group), `shilman-reels` (Instagram reels, carousels, captions) |
| vele | `CLAUDE.md` for the VELE Shopify website (velewellness.com), copied from the computer. `docs/` (Shopify ideas and settings checklist), `dashboard/README.md`. Computer folder: ~/Desktop/VELE/Website |

Notes:
- `cloudflare`, `wrangler`, `workers-best-practices`, `web-design-guidelines` and the other Cloudflare skills are public skill packs (Cloudflare, vercel-labs/agent-skills), currently used only in Cash Flow.
- The Emil Kowalski pack comes from `emilkowalski/skills`, installed with the skills CLI into the project's `.claude/skills`.
- Not copied: the large `cloudflare/references/` folder (reinstall with `npx skills add cloudflare/skills --skill cloudflare` if needed; the `SKILL.md` links to it), `settings.local.json`, `launch.json`, `.env*` files, and Cursor's own built-in skills (`skills-cursor`).
- `supabase_sql.py` reads its token from the macOS Keychain; no secrets are stored here.
