---
name: deploy
description: Deploy the Cash Flow website (shilmancashflow.com) end to end - checks, commit, push to GitHub, Cloudflare Worker deploy, cache purge and live verification. Use whenever the user asks to deploy, publish, ship or put the site live, in English or Hebrew.
---

# Deploy Cash Flow

A request to deploy is the user's standing approval to run this whole flow without
asking: commit, push to `origin/main`, deploy the Worker, purge the cache. Stop only on
the conditions below.

- Repo root: `shilman-cash-flow/`, branch `main`, remote `origin`
  (github.com/arielelya/shilman-cash-flow). Run every command from here, never from the
  parent `cash_flow/` folder.
- Worker: `shilman-cash-flow` (Workers with Assets, serves `dist/`, config `wrangler.jsonc`).
- workers.dev: https://shilman-cash-flow.shilman-cash-flow.workers.dev
- Production: https://shilmancashflow.com, served from Cloudflare's edge cache, so every
  deploy needs a purge.

## Stop conditions

Stop, report what happened, and do not continue when:

- `typecheck`, `test` or `build` fails.
- Anything staged looks like a secret: `.env*` (except `.env.local.example`), `*.pem`,
  `*.key`, or content containing `sb_secret_`, `sbp_`, `service_role` or a private key.
- The branch is not `main`, or a rebase onto `origin/main` conflicts (run
  `git rebase --abort` first).
- The changes touch `supabase/migrations/` or `supabase/functions/`. The frontend must
  not go live before the DB change. Ask whether it was applied (see `db-change`).
- `git push` is rejected after syncing, or wrangler is not authenticated
  (ask the user to run `npx wrangler login`).

Never force push, use `--no-verify`, `reset --hard`, or amend pushed commits.

## 1. Sync

```bash
git status -sb
git fetch origin
git pull --rebase --autostash origin main
```

Check for DB changes (committed, uncommitted and untracked):

```bash
git diff --name-only origin/main -- supabase/migrations supabase/functions
git status --porcelain -- supabase/migrations supabase/functions
```

## 2. Checks

```bash
npm run typecheck
npm run test
npm run build
```

Do not run `npm run test:db`. It hits the live Supabase project.

## 3. Commit

Skip when the working tree is clean.

```bash
git add -A
git diff --cached --stat
```

Review the staged list against the stop conditions. Unstage files that are clearly not
part of the work (screenshots, scratch files) and mention them in the report.

Match the repo's commit style: an imperative subject under 70 characters describing the
change, a blank line, and a body explaining why. No em or en dashes. Pass the message
through a HEREDOC and end it with the `Co-Authored-By` trailer.

## 4. Push

```bash
git push origin main
```

## 5. Deploy

```bash
npx wrangler deploy
```

Keep the `Current Version ID` from the output for the report.

## 6. Verify workers.dev

```bash
grep -o 'assets/index-[^"]*\.js' dist/index.html
curl -s https://shilman-cash-flow.shilman-cash-flow.workers.dev/ | grep -o 'assets/index-[^"]*\.js'
```

The two hashes must match. If they don't, investigate instead of redeploying blindly.

## 7. Purge the production cache

The purge uses a Cloudflare API token stored in the macOS Keychain as
`cloudflare-cache-purge-token` (permissions: Zone > Cache Purge and Zone > Zone > Read,
for shilmancashflow.com). Run it as a single command, because shell variables do not
persist between calls, and never print the token:

```bash
CF_TOKEN=$(security find-generic-password -s cloudflare-cache-purge-token -w 2>/dev/null) || { echo "NO_PURGE_TOKEN"; exit 0; }
ZONE_ID=$(curl -s -H "Authorization: Bearer $CF_TOKEN" "https://api.cloudflare.com/client/v4/zones?name=shilmancashflow.com" \
  | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).result?.[0]?.id ?? ""))')
[ -n "$ZONE_ID" ] || { echo "ZONE_NOT_FOUND"; exit 0; }
curl -s -X POST -H "Authorization: Bearer $CF_TOKEN" -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log("purge success="+j.success, JSON.stringify(j.errors))})'
```

On `NO_PURGE_TOKEN` or `ZONE_NOT_FOUND`, the deploy is still done. Tell the user to purge
manually (Cloudflare dashboard -> shilmancashflow.com -> Caching -> Configuration ->
Purge Everything) and point them to the one-time setup at the end of this file.

## 8. Verify production

```bash
curl -s https://shilmancashflow.com/ | grep -o 'assets/index-[^"]*\.js'
```

The hash must match `dist/index.html`. A purge can take up to about 30 seconds. If the old
hash is still served, wait with Monitor and an until-loop (not a foreground sleep), for
up to 2 minutes.

## 9. Report

Short, in Hebrew:
- Commit hash and subject, or "no new changes".
- Push done.
- Worker Version ID.
- workers.dev verified; production verified, or purge pending.
- Anything unstaged, skipped or unusual.

## One-time setup: purge token

In the Cloudflare account that owns shilmancashflow.com: My Profile -> API Tokens ->
Create Token -> Custom: Zone / Cache Purge / Purge and Zone / Zone / Read, restricted to
shilmancashflow.com. Then store it (the command prompts for the value, so it never
lands in shell history):

```bash
security add-generic-password -a shilman-cash-flow -s cloudflare-cache-purge-token -w
```
