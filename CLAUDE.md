# claude-library

Personal library of reusable Claude skills and project context.

- `global/skills/` — general skills, relevant in any project.
- `projects/<name>/` — context (`CLAUDE.md` / `context.md`), scripts and skills for one project only. Read only the folder of the project being worked on.

## Where skills live

Skills exist in two places: the user's computer and this repo. The computer is the source of truth; the repo is a read-only copy for when the computer is not available.

- Computer reachable: read and edit the files on the computer, then push the same change to this repo (commit to `main`). Only changes made on the computer go into the repo.
- Computer not reachable (the user is on another machine): read skills and project context from this repo, read-only. Do not commit or push anything to the repo. If a change is needed, show it in the reply so the user can apply it from the computer.
- Before pushing from the computer, compare with the repo. If the repo differs in a way the computer's version does not explain, ask the user instead of overwriting.
- Typical computer locations: `~/Developer/cash_flow/shilman-cash-flow/.claude/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`, `~/Desktop/VELE/Website/`.
- Never copy secrets, `.env*` files or local settings into the repo.

Which account belongs to which service (e.g. Composio): `reference/accounts.md`.

Keep this file short: it is loaded in every session. Put long material under `projects/` or `reference/`.
