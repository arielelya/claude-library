# claude-library

Personal library of reusable Claude skills and project context.

- `global/skills/` — general skills, relevant in any project.
- `projects/<name>/` — context (`CLAUDE.md` / `context.md`), scripts and skills for one project only. Read only the folder of the project being worked on.

## Where skills live

Skills exist in two places: this repo and the user's computer. The repo is the source of truth.

- Read skill content and project context from this repo.
- When a skill or CLAUDE.md needs updating, update the repo first (commit and push to `main`).
- If the same file also exists on the computer (and the computer is reachable), update that copy too so both stay identical. Typical computer locations: `~/Developer/cash_flow/shilman-cash-flow/.claude/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`.
- If the computer is not reachable, update only the repo and say so.
- Never copy secrets, `.env*` files or local settings into the repo.

Keep this file short: it is loaded in every session. Put long material under `projects/` or `reference/`.
