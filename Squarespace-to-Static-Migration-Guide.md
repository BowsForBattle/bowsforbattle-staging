# Bows for Battle: Squarespace to Static Site Migration Guide

This guide explains how to move bowsforbattle.org from Squarespace hosting to the static website in this repository.

## Goal

- Keep the same domain: bowsforbattle.org
- Replace Squarespace-hosted pages with this static site
- Minimize downtime and preserve email/other DNS services

## Recommended Hosting Options (for static files)

Pick one provider before DNS cutover:

1. Netlify (easy drag-and-drop or Git deploy)
2. Cloudflare Pages (good performance, strong DNS integration)
3. GitHub Pages (works, but less flexible for apex domain workflows)
4. AWS S3 + CloudFront (more control, more setup)

Netlify or Cloudflare Pages is usually fastest for this project.

## Phase 1: Prepare the Site (Before Any DNS Changes)

1. Finalize content
- Remove all yellow example placeholder content.
- Confirm legal, donation, contact, board, and transparency content are real and current.

2. Rebuild generated pages
- Source of truth is build.py.
- Regenerate all HTML files so they match current content.

Command:

```bash
python build.py
```

3. Validate local behavior
- Open index.html and key pages in browser:
  - Home
  - Programs / Events
  - Give / Donate / Sponsorship
  - Contact
  - Legal
- Verify images load from Pictures/.
- Verify internal links are not broken.

4. Confirm external integrations
- Donation button destination (if external payment processor)
- Contact form destination (if using external form endpoint/provider)
- Analytics (if needed)

5. Create a release snapshot
- Commit a clean deployment version in Git so rollback is easy.

## Phase 2: Publish to New Host (Staging URL)

1. Deploy the site to your selected host using its temporary URL.
- Example: your-site.netlify.app or your-site.pages.dev

2. Upload/deploy all required files together:
- All .html files in repo root
- styles.css, styles-v2.css, styles-v3-events.css
- data.js and events.js
- Pictures/ folder

3. Test staging thoroughly
- Mobile and desktop layout
- Navigation and footer links
- Events rendering
- Contact/donate flow behavior

Do not switch DNS yet. First make sure staging is fully correct.

## Phase 3: Domain Cutover from Squarespace

Important: DNS is often managed either in Squarespace or at your domain registrar. Confirm where your DNS zone is hosted before editing records.

1. Inventory existing DNS records
- Export or screenshot all current DNS records.
- Especially preserve:
  - MX (email)
  - TXT (SPF, DKIM, verification)
  - CNAME records for third-party tools

2. Lower TTL 24 hours before cutover (optional but recommended)
- Set relevant records to a low TTL (for example 300 seconds) so propagation is faster.

3. Add domain to new host
- In Netlify/Cloudflare/etc., add:
  - bowsforbattle.org
  - www.bowsforbattle.org
- Follow host instructions for required A/CNAME records.

4. Update DNS records to point web traffic to new host
- Typical pattern:
  - Apex/root (@) -> A/ALIAS/flattened record to host target
  - www -> CNAME to host target

5. Keep non-web records unchanged
- Do not alter MX/TXT/email-related records unless intentionally migrating email.

6. SSL/TLS certificate
- Ensure TLS certificate is issued for both apex and www on the new host.
- Force HTTPS once certificate is active.

## Phase 4: Verification After Cutover

1. Browser checks
- Test both:
  - https://bowsforbattle.org
  - https://www.bowsforbattle.org
- Confirm they resolve to the new static host.

2. Functional checks
- Key page load test
- Form behavior test
- Donation path test
- Image and CSS/JS loading test

3. DNS verification
- Confirm A/CNAME values match host docs.
- Confirm MX/TXT records still match previous configuration.

4. Redirect behavior
- Enforce one canonical domain style (either www or non-www).
- Ensure 301 redirect between the other variant and canonical.

## Phase 5: Decommission Squarespace Hosting

Only do this after at least 48-72 hours of stable production traffic.

1. Keep Squarespace subscription active briefly as fallback.
2. Confirm no traffic/dependency remains on Squarespace-hosted pages.
3. Cancel or downgrade Squarespace plan if no longer needed.
4. Keep domain registration and DNS management in the chosen long-term location.

## Rollback Plan (If Problems Occur)

If major issues appear after cutover:

1. Revert web DNS records to previous Squarespace values.
2. Wait for TTL propagation.
3. Verify site recovery.
4. Fix issues on staging, then attempt cutover again.

Because rollback is DNS-based, preserving original records is critical.

## Recommended Migration Day Checklist

- [ ] Content final, placeholders removed
- [ ] build.py run and output verified
- [ ] Staging tested on desktop/mobile
- [ ] DNS records backed up
- [ ] TTL lowered in advance
- [ ] Apex + www configured on new host
- [ ] SSL active for both domains
- [ ] Post-cutover smoke test complete
- [ ] Rollback records documented

## Notes Specific to This Repo

- HTML is generated from build.py; avoid hand-editing generated HTML when possible.
- Keep REV in build.py updated for each deployment so CSS/JS cache refreshes cleanly.
- Ensure Pictures/ and JS/CSS files deploy alongside HTML files.
