# Bows for Battle Website Plan — v2

Date: 2026-08-28
Supersedes: `BowsForBattle_Website_Plan.md` (v1, 2026-06-22)

---

## 1. What Changed From v1

v1 was a structure and tone plan. It got the tone right and the structure mostly right, and the current build follows it faithfully.

v2 exists because of two things v1 did not account for:

1. **Research into ~20 comparable veteran outdoor-therapy nonprofits** revealed a standard credibility checklist that every serious organization in this space has and the current build has none of: EIN in the footer, a board page, a transparency page, a persistent donate button, third-party trust seals, and a split between giving time and giving money.
2. **Bows for Battle is newly established.** There is no program history, no impact data, and no participant stories. v1 assumed those would be filled in. They cannot be yet, and inventing them is not an option.

The key strategic finding: **there is no professionalized archery-focused veteran nonprofit online.** The comparable archery orgs either have no trust signals at all or have let their domains lapse. Bows for Battle does not need to out-design Wounded Warrior Project. Hitting the standard checklist makes it the most credible archery-veteran organization on the internet.

### Governing principle for v2

> Where we lack a track record, we substitute transparency. We never substitute invention.

---

## 2. Current State Audit

### 2.1 What exists

| File | Status |
|---|---|
| `index.html` | Home. Good bones. Contains fabricated data — see 2.2. |
| `mission.html` | Mission and vision. Copy is accurate (matches bowsforbattle.org). Keep. |
| `programs.html` | Program pillars and photo gallery. Accurate but thin. Expand. |
| `support.html` | Sponsorship tier table plus a non-functional form. Rework substantially. |
| `contact.html` | Contact form, non-functional. Wire up. |
| `styles.css` | 18KB, single stylesheet. Solid foundation, keep and extend. |
| `Pictures/` | 20 images including `Logo.png`. Sufficient for now. |
| `Reference/sponsorship_packages.csv` | Source of truth for business sponsorship tiers. |

### 2.2 Fabricated content that must be removed before anyone sees this

These were auto-generated to establish visual feel. They read as factual claims and must not survive to launch.

- `index.html:116-119` — the entire stat block: `125+ Veterans Served`, `90+ Bows Provided`, `24 Event Days`, `800+ Mentorship Hours`. **All four are invented.** For a brand-new organization these are not placeholders, they are fabricated impact claims, and a donor discovering that is an unrecoverable credibility loss.
- `index.html:112` — the quote *"Every arrow is a moment of control..."* is presented in quotation marks with no attribution. Either attribute it to a real person who said it, or restyle it as an unquoted statement of principle.
- `index.html:99-102` — the four "From X to Y" focus panels are generic but not factually false. Acceptable to keep as statements of intent.

### 2.3 Functional and technical gaps

- **Both forms are non-functional.** `support.html` and `contact.html` have `<form>` elements with no `action` — submissions go nowhere. This is worse than having no form, because a veteran or donor who reaches out gets silence.
- **No donation capability at all.** The "support form" collects a package selection and an amount but cannot take a payment.
- **Header and footer are duplicated across all 5 pages.** At 15+ pages this becomes unmaintainable. See section 8.
- **Footer contains no legal information** — no EIN, no address, no phone, no 501(c)(3) statement.
- **No 988 crisis line anywhere on the site.**
- **`index.html` is missing the `<span>Bows for Battle</span>` brand text** that all four other pages have — inconsistent header.
- **Accessibility:** an automated contrast pass found 6 failures, all the same root cause — **text placed directly over background photographs with no darkening scrim.** Affected: the primary nav links over the header image (measured ~1.74:1 against the underlying layer, needs 4.5:1) and the footer text. Everything else passes. Fix is a semi-opaque overlay behind text that sits on imagery, not a palette change.
- **No `robots.txt`, no `sitemap.xml`, no favicon, no Open Graph tags** — links shared to Facebook or a text message will render as a bare URL with no image or description.

---

## 3. The Example-Content Convention

Rather than generating plausible-sounding filler, unknown content is filled with a **realistic example of the kind of information that belongs there**, wrapped in a marker that makes the formatting itself the "replace me" signal.

The example teaches the board what is wanted. The highlight says it is not real.

### 3.1 Markup

Inline:

```html
<span class="example">March 2026</span>
```

For a whole block:

```html
<div class="example-block">
  <p>A realistic sample founder story, written the way a real one would read.</p>
</div>
```

Where the example alone does not convey the ask, it is followed by a `.status-note` explaining what is needed and who owns it.

### 3.2 Styling

Amber fill with a dashed underline, defined in `styles-v2.css` section 1, with brighter variants for the dark surfaces. Deliberately conspicuous. Every page also carries a `.example-legend` strip beneath the header explaining the convention to anyone reviewing the draft.

### 3.3 Launch gate

A page is not publishable while it contains the class.

```bash
grep -o 'class="[^"]*example[^"]*"' *.html | cut -d: -f1 | uniq -c
```

**Zero results is the launch condition for any given page.** Current counts are in section 13.

### 3.4 Why this over lorem ipsum, blank fields, or invented content

Invented content risks shipping by accident. Lorem ipsum tells the board nothing. A blank field says something is missing but not what. A realistic example answers "what do you want from me?" in the exact place the answer goes, which turns the website itself into the content-collection worksheet.

---

## 4. Target Information Architecture

### 4.1 Primary navigation

Seven items plus a persistent Donate button. Each nav item is a short **hub** page that routes to
focused child pages.

```
[Logo]   Home   About   Programs   Events   Get Involved   Give   Contact   [ DONATE ]
```

| Hub | Children | What the section owns |
|---|---|---|
| **About** | mission, story, board, transparency | Who we are, and every money fact - budget, goals, governing documents |
| **Programs** | what-happens, eligibility, safety | What we do and what it is like to turn up |
| **Events** | - | When things are |
| **Get Involved** | equip, host, volunteer | Help that is not money |
| **Give** | donate, sponsorship | Money |

Plus `index`, `contact` and `legal`. **20 pages.**

**Get Involved contains no money at all.** An earlier draft gave it a "Fund" lane whose only job was
to send you to Give, which made the two sections overlap and read as disorganised. The split is now
absolute: Give is money, Get Involved is everything else.

### 4.2 One fact, one home

Every piece of content belongs to exactly one page; other pages link to it. This is the rule that
matters most, because breaking it is what made the previous version confusing. An audit of that
version found the budget table on two pages, "what it costs" on two pages, the session walkthrough on
two pages, Anchor Point on two pages, and sponsorship on three.

Current state, verified:

| Content | Sole home |
|---|---|
| First-year budget | `transparency.html` |
| First-year goals | `transparency.html` (homepage carries a two-item teaser that links to it) |
| Governing documents, verification | `transparency.html` |
| Session walkthrough, what to bring, what it costs | `what-happens.html` |
| Eligibility criteria and the interest form | `eligibility.html` |
| Range safety and insurance | `safety.html` |
| Impact-denominated amounts, Anchor Point | `donate.html` |
| Sponsorship tiers | `sponsorship.html` |
| Founder story | `story.html` |

### 4.3 Footer (every page)

Three bands:

1. **Crisis band** - highest visual priority:
   > **In crisis? Dial 988 then Press 1.**
   > Text 838255 - Chat at VeteransCrisisLine.net
   > Free, confidential, 24/7. You do not need to be enrolled in VA benefits or health care.

   The phrasing **"Dial 988 then Press 1"** is VA's specified wording - based on veteran preference,
   and it ensures callers route to the Veterans Crisis Line rather than the general 988 Lifeline. Use
   exactly this. `988` is a `tel:` link.

2. **Legal band** - legal name, EIN, mailing address, phone, 501(c)(3) statement.

3. **Utility band** - grouped by audience (For Veterans / Support Us / The Organization / Legal).

### 4.4 Deferred pages

| Page | Trigger to build it |
|---|---|
| `shop.html` | When merch exists - likely an external storefront link |
| `press.html` | Press kit. **No organization in the competitive survey has one.** Cheap differentiator. |
| `impact.html` | **Only once there is real data.** Not before. |

---

## 5. Ways to Contribute

People can give money, gear, land access, or time. Making the non-cash routes as visible as the cash
one is a genuine differentiator - Wounded Warriors in Action is the only comparable organization that
formalizes non-cash contribution as a first-class pathway, and it was the single highest-leverage idea
from the research.

For an archery organization this matters more than most: **bows, targets and range time are exactly
what a manufacturer, pro shop or landowner can give when they cannot write a cheque.**

| Route | What it is | Page |
|---|---|---|
| **Money** | One-time, monthly, business sponsorship | `donate.html`, `sponsorship.html` |
| **Equip** | Bows, arrows, releases, targets, safety gear; range lane time from pro shops | `equip.html` |
| **Host** | Private land, range or club access, hunting property, a donated guided day | `host.html` |
| **Volunteer** | Event help, coaching, peer mentorship, referrals, or simply turning up | `volunteer.html` |

Each has its own purpose-built intake form. A landowner offering 80 acres and a manufacturer offering
a case of arrows have nothing in common and should not share a textarea.

**Money is deliberately not one of the Get Involved lanes.** It lives under Give. An earlier draft put
a "Fund" lane on Get Involved whose only content was a link to Give, which made the two sections
overlap. Keeping the boundary absolute is what makes the nav self-explanatory.

**In-kind receipting note:** for donated gear the acknowledgment must *describe* the item ("one
compound bow, model X") but must **never state a dollar value** - valuation is the donor's
responsibility under IRS rules. Build this into the receipt template.

---

## 6. Naming Decisions

### 6.1 Monthly giving program

Research finding: every mature organization brands its recurring giving program — Heroes on the Water has "Honor Circle," Team Rubicon has "Support Squad." Unnamed monthly giving reads as an afterthought and underperforms.

**Recommendation: "Anchor Point."**

An anchor point in archery is the fixed spot where the string hand meets the face at full draw — the reference that makes every shot repeatable. It means consistency and stability, it is authentic archery vocabulary rather than marketing language, and it ties directly to the existing tagline **Anchor | Aim | Overcome**.

Suggested entry level $15/month, matching the category norm.

Alternates if the board prefers: *The Quiver*, *Full Draw Club*, *Point of Aim*.

### 6.2 Impact-denominated giving amounts

Project Healing Waters' donation form is the model worth copying: instead of "$50 / $100 / $250" it says "materials for 50 flies," "a new reel," "a guided day for five veterans."

This works even with zero program history, because it describes **a mechanism, not a claimed outcome.** The archery version writes itself — a starter bow setup, a set of arrows and a release, a range day for one veteran, equipment for a full clinic.

Actual dollar figures need the board's real cost numbers, so these ship as `[NEEDS INPUT]` until the treasurer provides them.

---

## 7. Legal, Compliance, and Trust

Now that 501(c)(3) status is confirmed, all of the following are unblocked. Not legal advice — the state registration and receipt language items are worth a short review by a nonprofit attorney or a compliance service before launch.

### 7.1 Required on the site

- **Footer, every page:** full legal name as filed, `EIN: XX-XXXXXXX`, mailing address, phone. Several state charitable-solicitation statutes require name/address/phone wherever a donation can be made. EIN-in-footer is also the single strongest convention in this category.
- **Donation page:** legal name, address, phone, tax-deductibility statement, description of charitable purpose, and any state-mandated disclosure text.
- **Public disclosure (IRC 6104):** the Form 1023, the determination letter, and the last 3 years of Form 990 must be available on request. Posting them on `transparency.html` satisfies this cleanly and is standard practice. With no 990 filed yet, post the determination letter now.
- **Privacy policy:** effectively mandatory. CCPA/CPRA excludes nonprofits, but **CalOPPA does not** — any site collecting PII from California residents must conspicuously post one. Colorado's privacy law has no nonprofit exemption at all, so write to Colorado-adequate standards and you are covered everywhere.
- **Donor privacy statement:** state plainly *"We never sell, rent, or trade donor information."* Disproportionate trust return for one sentence.
- **CAN-SPAM:** applies to nonprofits. Every newsletter needs accurate headers, a valid physical postal address, and a working unsubscribe honored within 10 business days.

### 7.2 State charitable solicitation registration

A donate button legally constitutes solicitation. Verify Wisconsin registration status with the **WI Department of Financial Institutions** (dfi.wi.gov, 608-261-9555).

**Wisconsin exemption:** organizations receiving **≤ $25,000/year** with no paid employees and all work done by unpaid volunteers are exempt from registration. Once you cross $25,000 you must register **within 30 days**.

**Year-one recommendation:** register in Wisconsin or document the exemption. Do not attempt multi-state registration — full coverage runs $3,000–5,000/yr in fees and is not a rational first-year spend. Add to the donation page: *"Bows for Battle is registered to solicit contributions in Wisconsin."* Track inbound gifts by state and register elsewhere when volume justifies it.

### 7.3 Receipting

- **$250+ single gift** requires a contemporaneous written acknowledgment with: org name, amount, description (not value) of any non-cash gift, and a statement of whether goods or services were provided in return.
- **Quid pro quo over $75** — a $100 shoot ticket that includes a $30 meal — requires the *organization* to disclose that the deductible amount is limited to the excess over fair market value, with a good-faith estimate. **This is the rule most likely to bite an archery nonprofit,** because tournaments, banquets, raffles, and swag are exactly this pattern. Penalties apply for failure to disclose.
- **Raffle tickets are not deductible at all**, and Wisconsin regulates raffles separately (license via the Department of Administration). Do not let a donation platform auto-receipt raffle tickets as gifts.

### 7.4 Trust signals to acquire

| Signal | Availability | Action |
|---|---|---|
| **Candid/GuideStar Seal of Transparency** | **Bronze and Silver are free and achievable immediately** by completing the profile | Claim before launch, embed badge in footer |
| **Charity Navigator** | Requires operating history and filed 990s | Year 2+ |
| **Google Workspace for Nonprofits** | Free for eligible 501(c)(3)s | Apply now — gives real `@bowsforbattle.org` email |
| **PayPal Giving Fund** | Requires 501(c)(3) + Candid listing | Secondary channel post-launch |
| **Liability + D&O insurance** | — | Required before running events; reference it on program pages |

### 7.5 Accessibility

Nonprofits are generally ADA Title III public accommodations and courts benchmark against WCAG. If BFB ever pursues VA or federal grant money, **Section 508 applies and points at WCAG 2.1 AA.**

Beyond compliance, this is mission alignment: **many veterans have service-connected vision, motor, or TBI-related impairments.** A site that is inaccessible to the people it claims to serve is a substantive failure, not a technical one.

Targets — all free, all easy when done from the start:

- Semantic HTML, one `<h1>` per page, logical heading order
- Meaningful `alt` on content images, `alt=""` on decorative
- Contrast ≥ 4.5:1 body / 3:1 large text — **the known issue is text over photos; add a scrim, not a palette change**
- Visible keyboard focus, full keyboard operability
- `<label for>` on every input; errors in text, not color alone
- Skip-to-content link, `lang="en"`, descriptive per-page `<title>`
- Respect `prefers-reduced-motion`
- Publish `accessibility.html` naming WCAG 2.1 AA as the goal with a contact for problems

Test with axe DevTools, WAVE, and Lighthouse. **Do not install an accessibility overlay widget** (accessiBe and similar) — they are widely criticized, have been the subject of an FTC action, and do not substitute for correct markup.

### 7.6 Content and imagery guardrails

Imagery is deferred, but these rules should be written down now so they apply when photos arrive.

Avoid both failure modes that veteran audiences consistently reject:

1. **The broken veteran** — pitiable, trauma-defined framing. Veterans specifically report this harms their employment prospects.
2. **The uncritical hero** — flags, eagles, and reverence. Reads as exploitative.

Aim between them: **strength-based and agency-forward.** Archery is an advantage here — it is a skill-mastery activity, so the natural imagery is *competence*, not rescue. A veteran shooting well, coaching someone else, laughing at the range.

- **No stock military imagery.** Veterans detect it instantly.
- Real people, real names, **written photo/story releases**, honored if withdrawn.
- Language: "veteran" not "vet" in formal copy; "living with PTSD" not "suffering from"; avoid "wounded warrior" (it is another organization's mark).
- **Do not use VA seals or imply VA affiliation** — this is both a legal issue and a common unforced error by new veteran nonprofits. Use the plain text treatment "Dial 988 then Press 1" in our own typography, which requires no approval, rather than the branded VCL logo lockup.
- **Safe messaging on suicide:** never lead with "22 a day"-style statistics as a headline, never describe method, use "died by suicide." Always pair any mention of crisis with the crisis line in the same visual block. Several comparable organizations use the suicide statistic as a fundraising hook while providing no crisis resource — that is the worst pattern observed in the research and we will not repeat it.

---

## 8. Technical Architecture — Decisions Required

### 8.1 Templating - resolved: build.py

At seven pages, hand-copying the header and footer was tolerable. At twenty it is not, and the pages
had already begun to drift.

`build.py` is a small Python static site generator, modelled on the one used for the Tri-County
Archers site. Nav, header, footer, the draft banner and every page body live in that one file; running
`python build.py` writes all twenty `.html` files. Python only, no Node, no dependencies, and the
output is ordinary static HTML that still opens by double-clicking.

The `.html` files are build output. **Editing them directly is a mistake - the next build overwrites
it.** The README says so prominently.

`REV` in `build.py` cache-busts CSS and JS on every deploy.

### 8.2 Hosting

**Recommendation: Cloudflare Pages.** Free with unlimited bandwidth, free SSL, and it consolidates DNS, hosting, CDN, and a WAF in one place — the WAF matters for a site taking donations. Netlify is the alternative if bundled form handling is preferred. Both are $0 versus Squarespace's ~$16–49/month.

### 8.3 Forms

Static sites cannot process forms natively. Options: **Web3Forms** (250 submissions/month free, host-agnostic), **Netlify Forms** (unlimited on current plans, but ties you to Netlify), or **Formspree** (50/month free).

Add a honeypot plus Turnstile or hCaptcha — a veteran nonprofit contact form will get spammed. **Never build a custom form that collects payment data**; always hand payment to the donation platform's hosted embed so the site stays out of PCI scope.

### 8.4 Donation platform

**Recommendation: Zeffy.** 0% platform fee and 0% processing (funded by an optional donor tip at checkout), it auto-issues IRS-compliant receipts including for in-kind and offline gifts, it embeds into static HTML, and it handles year-end donor summaries.

The receipt automation is the decisive factor, not the fee. **Stripe-direct and raw PayPal do not generate EIN-bearing deductibility receipts** — you would be hand-writing acknowledgments for every gift, which is unsustainable for a volunteer organization and a live compliance risk given the $250 and $75 quid-pro-quo rules.

Alternative: **Givebutter** — better peer-to-peer and event ticketing tooling, which matters if BFB runs tournament fundraisers, and it includes a real CRM. 0% if donor tips stay enabled.

Skip **Classy** (~$3,000+/yr license, absurd at this size). Add **PayPal Giving Fund** later as a *supplementary* channel only — it makes PayPal the charity of record and **you may never receive the donor's contact information**, which makes stewardship impossible.

Regardless of platform: **keep an independent donor record from day one**, even a spreadsheet. Platform lock-in of donor data is a real long-term cost.

### 8.5 Squarespace migration — critical sequencing

- **Squarespace serves images from its own CDN and those URLs die the moment the subscription is cancelled.** Download the entire media library before touching anything.
- Squarespace exports blog posts (XML) and products (CSV) only. **Page content, layouts, design, custom CSS, navigation, forms, and all existing form submissions do not export.** Manually copy any content worth keeping — the mission text is already captured and confirmed accurate.
- **Copy the existing MX, SPF, DKIM, DMARC, and TXT records exactly before any DNS change.** Losing MX records silently kills email — this is the classic migration disaster.
- Crawl the current site first to inventory URLs, then set 301 redirects for anything that changes.
- Lower DNS TTL to 300s a day before cutover.
- **Do not cancel Squarespace until the new site has run clean for two weeks.**

---

## 9. Build Plan and Current Status

### Phase 1 - Structure (complete)

1. **All fabricated statistics removed.** The `125+ / 90+ / 24 / 800+` block is gone, replaced by an
   honest "Where We Are Right Now" section and dated first-year goals.
2. `build.py` generates all 20 pages from one definition of nav, header and footer.
3. Hub-and-children information architecture (4.1), with a subnav of siblings on every child page.
4. **Duplication eliminated** (4.2) - every fact verified to have exactly one home.
5. Get Involved and Give no longer overlap.
6. Home page routes the two real audiences through two equal doors.
7. Three-band footer on every page: 988 crisis line, EIN and legal identity, audience-grouped links.
8. Example-content system applied throughout (section 3).
9. Events page driven by `data.js` with filters, per-event Google Calendar links and a whole-schedule
   `.ics` export.
10. Accessibility: skip links, one `<h1>` per page, labelled inputs, alt text, reduced-motion support,
    and **zero colour-contrast failures across all 20 pages**.

Forms are intentionally inert - each carries a visible "not yet active" notice.

### Phase 2 - Content (board, blocking)

Replace the example content with real information. Section 10 is the list. This is the critical path.

### Phase 3 - Make it work

11. Wire the forms to a real backend with spam protection.
12. Stand up the donation platform and the Anchor Point recurring option.
13. Claim the Candid profile, earn the Bronze then Silver seal, embed the badge.
14. Attorney review of `legal.html`.
15. Confirm Wisconsin registration or document the exemption.

### Phase 4 - Launch

16. Full example-content sweep - must return zero.
17. Rescue all images off the Squarespace CDN **before** cancelling anything.
18. Record existing DNS records, especially MX.
19. Deploy, verify, cut DNS over, confirm SSL and email.
20. Two-week soak, then cancel Squarespace.

### Phase 5 - Post-launch

21. Merch store, press kit, PayPal Giving Fund, Google Workspace for Nonprofits.
22. `impact.html` - only once there is real data.

---

## 10. Inputs Needed From the Board

Everything below becomes a `[NEEDS INPUT]` marker in the build until answered.

### Legal and financial
- [ ] Exact legal name as filed
- [ ] EIN
- [ ] Public mailing address and phone
- [ ] Determination letter PDF
- [ ] Articles of incorporation, bylaws, conflict-of-interest policy (PDF)
- [ ] First-year operating budget
- [ ] Wisconsin DFI registration status, or confirmation of the under-$25k exemption
- [ ] Liability and D&O insurance status

### People
- [ ] Board roster — names, roles, photos, short bios
- [ ] Founder story — 300–500 words, first person
- [ ] Instructor certifications held (USA Archery, NFAA levels)
- [ ] Any veterans on the board or staff to sign off on tone and imagery

### Program
- [ ] Eligibility criteria — service era, discharge status, geography, any disqualifiers
- [ ] Is the program free to the veteran?
- [ ] How a veteran applies or signs up
- [ ] What a typical session or clinic actually consists of
- [ ] First-year goals — specific, dated, numeric
- [ ] Which metrics we commit to tracking and publishing

### Money
- [ ] Real cost figures for impact-denominated tiers — what does a starter setup actually cost?
- [ ] Approve or replace **"Anchor Point"** as the monthly program name
- [ ] Approve **Zeffy** (or choose Givebutter)
- [ ] Confirm the sponsorship tiers in `Reference/sponsorship_packages.csv` are current

### Decisions for you
- [ ] Does anyone besides the developer need to edit content? (determines whether to add a CMS)
- [ ] Hosting — recommend Cloudflare Pages
- [ ] Merch: external storefront (Bonfire, Printful) or self-hosted?

---

## 11. Explicitly Out of Scope for Now

- **Photography.** Deferred by direction. Guardrails in 7.6 apply when it resumes.
- **Participant stories and testimonials.** None exist. Will not be fabricated or composited — that is fraud exposure, not just poor taste.
- **Impact metrics.** Not until real data exists.
- **Multi-state charitable registration.** Not a rational first-year spend.
- **Chapter/locator map.** Single-location organization.
- **Podcast, speaker requests, planned giving, DAF/stock/crypto channels.** All standard for mature organizations in this space; all premature here.

---

## 12. Estimated Year-One Cost

| Item | Cost |
|---|---|
| Domain | ~$12/yr |
| Hosting (Cloudflare Pages) | $0 |
| Forms (Web3Forms) | $0 |
| Donation platform (Zeffy) | $0 |
| Email (Google Workspace for Nonprofits) | $0 |
| WI charitable registration | $0–75 |
| Liability + D&O insurance | ~$500–1,500 |
| **Total** | **~$515–1,590** |

Versus Squarespace at roughly $190–590/year for hosting alone. **The migration pays for a meaningful share of the insurance.**

---

## 13. Current Build State

20 pages generated by `build.py`. Plain static HTML - double-click `index.html`.

### Source files

| File | Purpose |
|---|---|
| `build.py` | The site. Nav, header, footer and every page body. **Edit this, not the .html files.** |
| `data.js` | Events and org facts - the only file to edit to change the schedule |
| `events.js` | Renders the events table, filters and calendar exports |
| `styles.css` | Original v1 stylesheet |
| `styles-v2.css` | Structural additions, loads second |
| `styles-v3-events.css` | Events page only |

### Verified

- All internal links and anchor targets resolve across all 20 pages.
- Every fact has exactly one home (see 4.2) - checked by grep, not by eye.
- One `<h1>` per page; every image has `alt`; every form input has a `<label for>`.
- Skip link, crisis band, EIN and 988 present on all 20 pages.
- **Zero colour-contrast failures on all 20 pages**, measured against WCAG AA with alpha compositing
  and gradient handling.
- Events page: filters, past/upcoming toggle, detail expansion and `.ics` generation exercised in
  browser; the calendar file validates as iCalendar.
- No horizontal overflow at 375px.
- Every form is inert and carries a visible "not yet active" notice.

### Known drift risk

The homepage carries a two-item teaser of the first-year goals that also appear in full on
`transparency.html`. That is a deliberate teaser, but it means a goal change touches two places. If
goals start changing often, move them into `data.js` alongside the events and render both from there.

### Example content remaining

| File | Markers |
|---|---|
| `about.html` | 9 |
| `board.html` | 18 |
| `contact.html` | 13 |
| `donate.html` | 34 |
| `eligibility.html` | 20 |
| `equip.html` | 18 |
| `events.html` | 9 |
| `get-involved.html` | 10 |
| `give.html` | 9 |
| `host.html` | 19 |
| `index.html` | 15 |
| `legal.html` | 42 |
| `mission.html` | 9 |
| `programs.html` | 9 |
| `safety.html` | 17 |
| `sponsorship.html` | 15 |
| `story.html` | 15 |
| `transparency.html` | 42 |
| `volunteer.html` | 17 |
| `what-happens.html` | 17 |

**Total: 357.** The launch condition is zero.

```bash
grep -o 'class="[^"]*example[^"]*"' *.html | cut -d: -f1 | uniq -c
```
