# Personal CLAUDE.md for Claude Code

The text that goes in `~/.claude/CLAUDE.md` on the computer, so it loads in every Claude Code session. On a new computer, paste it there (or run the installer script from the Desktop).

```
# Personal rules (apply in every project)

## Language
- Reply in Hebrew, feminine address, simple words.
- Do not mix English words into Hebrew sentences. If a technical term is unavoidable, explain it in Hebrew.

## Skills
- When a skill is needed, look on this computer first: the project's `.claude/skills/`, then `~/.cursor/skills/` and `~/.agents/skills/`.
- If it is not there, or the user is on another machine, read it from GitHub `arielelya/claude-library` (`projects/<name>/skills/` or `global/skills/`), read-only.
- This computer is the source of truth. After changing a skill or a CLAUDE.md here, copy the same change to that repo if it is cloned here; otherwise tell the user it still needs to be copied.
- Which account belongs to which service: `reference/accounts.md` in that repo.

## Safety
- Never delete files or folders unless the user asked, and delete only what was asked.
- Run steps that depend on each other one after another, not in parallel.
- Never put secrets, `.env` files or local settings into the repo.
```
