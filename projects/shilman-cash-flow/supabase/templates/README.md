# Auth email templates

The three emails Supabase sends on behalf of this app. Until now they existed only in the
dashboard, with no copy in the repo and no way to review a change before users saw it.

| File | Dashboard template | Sent when |
|---|---|---|
| `confirmation.html` | Confirm signup | `signUp`, and the resend offered on the login screen |
| `recovery.html` | Reset password | "שכחתי סיסמה", and "שנה סיסמה" in Settings |
| `email_change.html` | Change email address | changing the address in Settings |

Subjects, which were in English on a Hebrew product until 2026-10-10:

| Template | Subject |
|---|---|
| Confirm signup | אימות כתובת האימייל שלך בשילמן פייננס |
| Reset password | איפוס הסיסמה שלך בשילמן פייננס |
| Change email address | אישור כתובת האימייל החדשה בשילמן פייננס |

The other templates in the dashboard (invite, magic link, reauthentication, and the
notification mails) are Supabase defaults in English. None of them is ever sent: this app
has no invite, magic-link or MFA flow, and every `mailer_notifications_*_enabled` is false.
Leave them alone rather than translating mail nobody receives.

## The logo, and why order matters

The header shows `public/brand/shilman-finance.png`, served at
`https://shilmancashflow.com/brand/shilman-finance.png`. It lives in `public/` because Vite
copies that folder verbatim: the same file under `src/assets/` is content-hashed, so its URL
would change on every build and every mail already sent would lose its logo.

**Deploy the site before pasting a template that references a new image.** The URL does not
exist until `dist/brand/` is live, and the site answers anything it does not have with
index.html, so a mail sent in between shows a broken image rather than a missing one.

Most clients block images by default, so the inline type styles on the `<img>` are doing
real work: they style the alt text, and the header reads correctly with the mark absent.

## Installing a change

`PATCH /v1/projects/{ref}/config/auth` is refused by the agent sandbox, so this is manual:
Authentication -> Emails -> the template -> paste the file -> Save. The subject sits on the
same screen. `_previous/` holds what was live before 2026-10-10 if a change has to go back.

## Two things that will break if you are not careful

**The expiry sentence is not decoration.** Each template says the link is good for one hour,
and that is `mailer_otp_exp` in the dashboard, currently `3600`. They were saying 24 hours
against the same 3600, so the mail was wrong by 23 hours and a user who came back later met
an expired link. If you change `mailer_otp_exp`, change all three sentences with it.

**No flexbox, and no HSL.** The old templates centred an emoji with `display:flex`, which
Gmail and Outlook strip, so it sat in the corner of its circle - the visible symptom that
started this. They also used `hsl()` colours, which Outlook does not parse. Tables, inline
styles and hex only. There are no remote images on purpose, so the mail looks the same
whether or not the client loads them.

## Previewing

```bash
node supabase/templates/preview.mjs
```

Fills in the Supabase variables, writes HTML and PNGs at desktop and phone width to
`.preview/`, and fails loudly on a variable it has no sample value for.
