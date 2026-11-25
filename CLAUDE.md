# claude-library

Personal library of reusable Claude skills and project context.

- `global/skills/` — general skills, relevant in any project.
- `projects/<name>/` — context (`CLAUDE.md` / `context.md`), scripts and skills for one project only. Read only the folder of the project being worked on.

## When a skill is needed

1. Look for it on the user's computer first: the project's `.claude/skills/`, then `~/.cursor/skills/` and `~/.agents/skills/`.
2. If the user is not on the computer (it is not reachable), take it from this repo: `projects/<name>/skills/` or `global/skills/`. Read only; do not push from there.

## Where skills live

Skills exist in two places: the user's computer and this repo. The computer is the source of truth; the repo is a read-only copy for when the computer is not available.

- Computer reachable: read and edit the files on the computer, then push the same change to this repo (commit to `main`). Only changes made on the computer go into the repo.
- Computer not reachable (the user is on another machine): read skills and project context from this repo, read-only. Do not commit or push anything to the repo. If a change is needed, show it in the reply so the user can apply it from the computer.
- Before pushing from the computer, compare with the repo. If the repo differs in a way the computer's version does not explain, ask the user instead of overwriting.
- Typical computer locations: `~/Developer/cash_flow/shilman-cash-flow/.claude/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`, `~/Desktop/VELE/Website/`.
- Never copy secrets, `.env*` files or local settings into the repo.

## Projects

| Project | What it is | Folder on the computer | Folder in this repo |
|---|---|---|---|
| Cash Flow | The Shilman Finance website and app | `~/Developer/cash_flow/shilman-cash-flow` (an older copy is under `~/Desktop/shilman finance/Website/cash_flow`) | `projects/shilman-cash-flow/` |
| VELE | The VELE Shopify store (velewellness.com), plus brand files and a dashboard | `~/Desktop/VELE/Website` (brand files and `Dashboard` are in `~/Desktop/VELE`) | `projects/vele/` |
| Shilman content | Skills for Shilman Finance posts and Instagram content, kept in the claude.ai account | none (account skills) | `projects/shilman/skills/` |

## Adding a new skill

1. Install it on the computer first: the project's `.claude/skills/` for a project skill, or `~/.agents/skills/` for a general one.
2. Copy it to this repo: `projects/<name>/skills/<skill>/` or `global/skills/<skill>/`. Copy the whole folder, but not secrets or local settings.
3. Add a row for it in `README.md`.
4. Commit and push to `main`.

Which account belongs to which service (e.g. Composio): `reference/accounts.md`.

Keep this file short: it is loaded in every session. Put long material under `projects/` or `reference/`.
