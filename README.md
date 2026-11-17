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

## projects
| Project | Contents |
|---|---|
| shilman-cash-flow | `CLAUDE.md` for the Cash Flow app. Skills: `deploy`, `db-change`, `cloudflare`, `wrangler`, `workers-best-practices`, `web-design-guidelines` |
| vele/dashboard | Dashboard README |

Note: `cloudflare`, `wrangler`, `workers-best-practices` and `web-design-guidelines` are public skill packs (Cloudflare, vercel-labs/agent-skills) currently used only in Cash Flow.

Not copied: the large `cloudflare/references/` folder, `settings.local.json` and `launch.json`.
