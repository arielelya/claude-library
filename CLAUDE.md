# claude-library

Personal library of reusable Claude skills and project context.

- `global/skills/` — general skills, relevant in any project.
- `projects/<name>/` — context (`CLAUDE.md` / `context.md`) and skills for one project only. Read only the folder of the project being worked on.

Keep this file short: it is loaded in every session. Put long material under `projects/` or `reference/`.
