# claude-library

Personal library of reusable Claude skills and project context.

- `global/skills/` — general skills, relevant in any project.
- `projects/<name>/` — context (`CLAUDE.md` / `context.md`), scripts and skills for one project only. Read only the folder of the project being worked on.

## Where skills live

Skills exist in two places: the user's computer and this repo. The computer is the source of truth; the repo is a copy for when the computer is not available.

- Computer reachable: read and edit the files on the computer, then push the same change to this repo (commit to `main`).
- Computer not reachable: read from this repo. If something must change, update the repo and tell the user the change has not reached the computer yet.
- Next time the computer is reachable: compare the repo with the computer and copy pending repo changes to the computer.
- Before overwriting either side, compare both versions. If both changed since the last sync, ask the user instead of overwriting.
- Typical computer locations: `~/Developer/cash_flow/shilman-cash-flow/.claude/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`, `~/Documents/VELE Website/`.
- Never copy secrets, `.env*` files or local settings into the repo.

Keep this file short: it is loaded in every session. Put long material under `projects/` or `reference/`.
