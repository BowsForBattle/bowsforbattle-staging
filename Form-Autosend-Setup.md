# Form Autosend Setup

The website forms now submit to a serverless endpoint at `/api/form-submit`.

## What Is Implemented

- Frontend handler in `forms.js` sends form data with `fetch`.
- Netlify function in `netlify/functions/form-submit.js` validates and emails submissions.
- Redirect in `netlify.toml` maps `/api/form-submit` to the Netlify function.

## Required Environment Variables (Netlify)

Set these in Netlify Site Settings -> Environment Variables:

- `RESEND_API_KEY` (required)
- `FORM_FROM` (recommended)
- `FORM_TO` (optional, defaults to both org emails)
- `FORM_REPLY_TO` (optional)
- `ALLOWED_ORIGINS` (recommended)

### Suggested values

- `FORM_FROM`: `Bows for Battle Forms <forms@bowsforbattle.org>`
- `FORM_TO`: `jessehall@bowsforbattle.org,dustinlangsdorf@bowsforbattle.org`
- `FORM_REPLY_TO`: `jessehall@bowsforbattle.org`
- `ALLOWED_ORIGINS`: `https://bowsforbattle.org,https://www.bowsforbattle.org`

## Resend Setup

1. Create Resend account.
2. Verify your sending domain (`bowsforbattle.org`).
3. Add DNS records requested by Resend (SPF/DKIM).
4. Generate API key and set `RESEND_API_KEY` in Netlify.

## Built-in Safeguards

Server-side protections in `form-submit.js`:

- Allow-list of valid form titles only
- Payload size limits and strict JSON parsing
- Field count and field length limits
- Suspicious-content checks (`<script`, `javascript:` patterns)
- Link-count throttling in message content
- Honeypot trap field
- Minimum form-fill elapsed time requirement
- In-memory per-IP rate limiting per function instance
- Optional origin allow-list via `ALLOWED_ORIGINS`

Client-side protections in `forms.js`:

- Submit cooldown in local storage
- Honeypot field insertion
- Minimum time before submit
- Disabled submit button while sending

## Notes

- Local `file://` testing will not submit to Netlify functions. Test on deployed preview/production URL.
- No anti-spam system can guarantee zero spam, but this setup significantly reduces bot and abuse traffic for a static site.
