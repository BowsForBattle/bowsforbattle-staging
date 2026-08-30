#!/usr/bin/env python3
"""Bows for Battle - static site generator.

Run:  python build.py

Writes plain .html files next to this script. No dependencies, no Node.
The output is ordinary static HTML - double-click index.html and it works.

WHY THIS EXISTS
  The header, footer, navigation and the draft banner live here exactly
  once. Editing them by hand across twenty files guarantees the pages
  drift apart, which is what happened before this file existed.

WHERE THINGS LIVE
    Events are NOT in this file. They live in data.js and render through
    events.js, so a date is typed in one place only.

ONE FACT, ONE HOME
    Every piece of content belongs to exactly one page. Other pages link
    to it rather than repeating it. If you find yourself pasting a budget
    table or a "what it costs" line onto a second page, link instead.
"""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Bump on every deploy so cached HTML, CSS and JS refresh together.
REV = "2026.08.29.3"

SITE = "Bows for Battle"


# ---------------------------------------------------------------------------
# NAVIGATION
#
# NAV is the top bar. SECTIONS maps a hub page to its child pages; a child
# page shows its siblings in a subnav and lights up its parent in the top bar.
# ---------------------------------------------------------------------------

NAV = [
    ("index.html",        "Home"),
    ("about.html",        "About"),
    ("programs.html",     "Programs"),
    ("events.html",       "Events"),
    ("get-involved.html", "Get Involved"),
    ("give.html",         "Give"),
    ("contact.html",      "Contact"),
]

SECTIONS = {
    "about.html": [
        ("mission.html",      "Mission &amp; Vision"),
        ("story.html",        "Our Story"),
    ("board.html",        "Board &amp; Leadership"),
    ],
    "programs.html": [
        ("eligibility.html",  "Eligibility &amp; Apply"),
        ("safety.html",       "Safety"),
    ],
    "get-involved.html": [
        ("equip.html",     "Donate Gear"),
        ("host.html",      "Become a Host"),
        ("volunteer.html", "Volunteer"),
    ],
    "give.html": [
        ("donate.html",      "Donate"),
        ("sponsorship.html", "Business Sponsorship"),
    ],
}

# child page -> hub page
PARENT = {}
for _hub, _kids in SECTIONS.items():
    for _href, _label in _kids:
        PARENT[_href] = _hub


DRAFT_BANNER = ''


def head(title, desc, page, extra_css=()):
    css = ['styles.css', 'styles-v2.css'] + list(extra_css)
    links = '\n'.join(
        '  <link rel="stylesheet" href="%s?v=%s">' % (c, REV) for c in css
    )
    return (
        '<!doctype html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <meta name="description" content="%s">\n'
        '  <title>%s | %s</title>\n'
        '  <link rel="icon" href="Pictures/Logo.png">\n'
        '  <meta property="og:title" content="%s | %s">\n'
        '  <meta property="og:description" content="%s">\n'
        '  <meta property="og:image" content="Pictures/Logo.png">\n'
        '  <meta property="og:type" content="website">\n'
        '%s\n'
        '</head>\n'
    ) % (desc, SITE, title, SITE, title, desc, links)


def header(page):
    """Top bar. A child page lights up its parent hub."""
    active = PARENT.get(page, page)
    items = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ''
        items.append('        <a%s href="%s">%s</a>' % (cls, href, label))
    return (
        '<body class="%s">\n'
        '  <a class="skip-link" href="#main">Skip to main content</a>\n\n'
        '  <header class="site-header">\n'
        '    <div class="container topbar">\n'
        '      <a class="brand" href="index.html" aria-label="Bows for Battle Home">\n'
        '        <img src="Pictures/Logo.png" alt="Bows for Battle logo">\n'
        '%s'
        '      </a>\n'
        '      <nav class="site-nav" aria-label="Primary navigation">\n'
        '%s\n'
        '        <a class="nav-donate" href="donate.html">Donate</a>\n'
        '      </nav>\n'
        '    </div>\n'
        '  </header>\n\n'
        '%s'
    ) % (
        'home-page' if page == 'index.html' else 'internal-page',
        '' if page == 'index.html' else '        <span>Bows for Battle</span>\n',
        '\n'.join(items),
        DRAFT_BANNER,
    )


def subnav(page):
    """Sibling links for a page inside a section. Hubs show their children."""
    hub = PARENT.get(page)
    kids = SECTIONS.get(page) or (SECTIONS.get(hub) if hub else None)
    if not kids:
        return ''
    hub_href = hub or page
    hub_label = dict(NAV).get(hub_href, 'Overview')
    links = ['        <a href="%s"%s>%s</a>' % (
        hub_href, ' class="on"' if page == hub_href else '', hub_label + ' Overview')]
    for href, label in kids:
        cls = ' class="on"' if href == page else ''
        links.append('        <a href="%s"%s>%s</a>' % (href, cls, label))
    return (
        '  <nav class="subnav" aria-label="Section navigation">\n'
        '    <div class="container">\n'
        '%s\n'
        '    </div>\n'
        '  </nav>\n\n'
    ) % '\n'.join(links)


FOOTER = """  <footer class="site-footer">
    <div class="crisis-band">
      <div class="container">
        <p class="crisis-lead">In crisis? <a href="tel:988">Dial 988 then Press 1</a>.</p>
        <p class="crisis-detail">
          Text 838255 &middot; Chat at <a href="https://www.veteranscrisisline.net/get-help-now/chat/" target="_blank" rel="noopener noreferrer">VeteransCrisisLine.net</a><br>
          Free, confidential, 24/7. You do not need to be enrolled in VA benefits or health care.
        </p>
      </div>
    </div>

    <div class="legal-band">
      <div class="container legal-grid">
        <div>
          <p class="legal-name">Bows for Battle, Inc.</p>
          <p>
            <span data-org="address">N64W14960 Mill Rd, Menomonee Falls, WI 53051</span><br>
            <a href="mailto:jessehall@bowsforbattle.org">jessehall@bowsforbattle.org</a>
          </p>
        </div>
        <div>
          <p><span>EIN: 42-2771314</span></p>
          <p>
            Bows for Battle is a registered 501(c)(3) nonprofit organization.
            Contributions are tax-deductible to the extent permitted by law.
          </p>
        </div>
      </div>
    </div>

    <div class="utility-band">
      <div class="container">
        <div class="utility-grid">
          <div>
            <h2>For Veterans</h2>
            <ul class="utility-links">
              <li><a href="eligibility.html">Eligibility &amp; Apply</a></li>
              <li><a href="events.html">Events</a></li>
              <li><a href="safety.html">Safety</a></li>
            </ul>
          </div>
          <div>
            <h2>Support Us</h2>
            <ul class="utility-links">
              <li><a href="donate.html">Donate</a></li>
              <li><a href="sponsorship.html">Sponsorship</a></li>
              <li><a href="equip.html">Donate Gear</a></li>
              <li><a href="host.html">Become a Host</a></li>
              <li><a href="volunteer.html">Volunteer</a></li>
            </ul>
          </div>
          <div>
            <h2>The Organization</h2>
            <ul class="utility-links">
              <li><a href="mission.html">Mission &amp; Vision</a></li>
              <li><a href="story.html">Our Story</a></li>
              <li><a href="board.html">Board &amp; Leadership</a></li>
              <li><a href="contact.html">Contact</a></li>
            </ul>
          </div>
          <div>
            <h2>Legal</h2>
            <ul class="utility-links">
              <li><a href="legal.html#privacy">Privacy Policy</a></li>
              <li><a href="legal.html#donor-privacy">Donor Privacy</a></li>
              <li><a href="legal.html#accessibility">Accessibility</a></li>
              <li><a href="legal.html#disclosures">Disclosures</a></li>
            </ul>
            <h2 style="margin-top:1rem">Follow</h2>
            <ul class="utility-links">
              <li><a href="https://www.facebook.com/profile.php?id=61590572042307" target="_blank" rel="noopener noreferrer">Facebook</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom container" style="width:100%">
          <p>&copy; 2026 <span>Bows for Battle, Inc.</span> All rights reserved.</p>
        </div>
      </div>
    </div>
  </footer>
"""


def phead(eyebrow, h1, lead):
    return (
        '    <section class="page-intro">\n'
        '      <div class="container narrow content">\n'
        '        <p class="eyebrow">%s</p>\n'
        '        <h1>%s</h1>\n'
        '        <p>%s</p>\n'
        '      </div>\n'
        '    </section>\n\n'
    ) % (eyebrow, h1, lead)


def hub_cards(page):
    """The routing grid on a hub page."""
    kids = SECTIONS.get(page, [])
    blurbs = {
        'mission.html':      'What we are here to do, and the principles the program is built on.',
        'story.html':        'Why this organization exists, and exactly where it stands today.',
        'board.html':        'The people accountable for how this organization spends money.',
        'eligibility.html':  'Who we serve, what we are not, and how to sign up.',
        'safety.html':       'Range standards, supervision, and insurance.',
        'equip.html':        'Bows, arrows, targets and range time.',
        'host.html':         'Land, range access, hunting property, or a guided day.',
        'volunteer.html':    'Help at events, mentor, or simply show up.',
        'donate.html':       'One-time gifts and monthly giving.',
        'sponsorship.html':  'Business sponsorship tiers and what each one funds.',
    }
    out = ['    <section class="anchor-section">\n      <div class="container content">\n',
           '        <div class="cards auto-fit">\n']
    for href, label in kids:
        out.append(
            '          <article class="card">\n'
            '            <h2>%s</h2>\n'
            '            <p>%s</p>\n'
            '            <a class="link-button" href="%s">Read More</a>\n'
            '          </article>\n' % (label, blurbs.get(href, ''), href)
        )
    out.append('        </div>\n      </div>\n    </section>\n\n')
    return ''.join(out)


PAGES = []


def page(name, title, desc, body, extra_css=(), scripts=()):
    PAGES.append((name, title, desc, body, extra_css, scripts))


def write_all():
  for name, title, desc, body, extra_css, scripts in PAGES:
    main_cls = 'home-main' if name == 'index.html' else 'internal-main'
    js_files = ['forms.js'] + list(scripts)
    js = ''.join('  <script src="%s?v=%s"></script>\n' % (s, REV) for s in js_files)
    html = (
      head(title, desc, name, extra_css)
      + header(name)
      + subnav(name)
      + '  <main class="%s" id="main">\n' % main_cls
      + body
      + '  </main>\n\n'
      + FOOTER
      + js
      + '</body>\n</html>\n'
    )
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
      f.write(html)
  print('Wrote %d pages (rev %s)' % (len(PAGES), REV))


# ===========================================================================
# HOME
# ===========================================================================

page('index.html', 'Home',
     'Bows for Battle supports veterans through the discipline, focus, and healing power of archery.',
     """    <section class="page-intro home-hero">
      <div class="container home-hero-grid">
        <article>
          <p class="eyebrow">Anchor | Aim | Overcome</p>
          <h1>Mission first. Veterans always.</h1>
          <p>
            Bows for Battle is a 501(c)(3) nonprofit dedicated to supporting veterans through the
            discipline, focus, and healing power of archery. Our mission is to put bows in the hands
            of veterans and create opportunities for them to reconnect with themselves, with fellow
            veterans, and with the outdoors.
          </p>
        </article>
        <aside class="home-callout">
          <h2>Veteran-Centered Support</h2>
          <p>
            Archery creates a repeatable process where breath, posture, patience, and precision help
            veterans reset.
          </p>
          <div class="badge-row">
            <span class="badge">Focus</span>
            <span class="badge">Outdoors</span>
            <span class="badge">Camaraderie</span>
            <span class="badge">Purpose</span>
          </div>
        </aside>
      </div>
    </section>

    <!-- The two reasons anybody comes to this site. Two doors, nothing else
         competing with them. -->
    <section class="home-section">
      <div class="container">
        <div class="door-grid">
          <article class="door">
            <p class="door-kicker">If you served</p>
            <h2>I am a veteran.</h2>
            <p>
              No experience needed. We provide the bow, the arrows and the coaching. Nobody will ask
              you to talk about your service.
            </p>
            <div class="home-actions">
              <a class="link-button" href="eligibility.html">See Eligibility &amp; Apply</a>
              <a class="link-button alt" href="eligibility.html">Am I Eligible?</a>
            </div>
          </article>
          <article class="door">
            <p class="door-kicker">If you want to help</p>
            <h2>I want to support this.</h2>
            <p>
              Money is one of four ways. Gear, land access, and simply showing up matter just as much
              to a veteran walking in for the first time.
            </p>
            <div class="home-actions">
              <a class="link-button" href="donate.html">Donate</a>
              <a class="link-button alt" href="get-involved.html">Other Ways to Help</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="home-section">
      <div class="container home-panel-grid">
        <article class="home-panel">
          <p class="section-head">Where We Are Right Now</p>
          <h2>We are just getting started.</h2>
          <p>
            Bows for Battle was founded on <span>May 3, 2026</span> and received 501(c)(3)
            status in <span>2026</span>. We are building our first programs now.
            That means we do not yet have years of numbers to point to &mdash; what we have is a clear
            plan and a real board.
          </p>
          <p>
            If you support us this year, you are one of the people who makes the first season
            possible.
          </p>
          <div class="home-actions">
            <a class="link-button alt" href="story.html">Read Our Story</a>
          </div>
        </article>
        <aside class="home-panel">
          <p class="section-head">Community Partners</p>
          <h2>Local support is already showing up.</h2>
          <p>
            Sherwood Forest Bowmen and BK3 Archery have been incredible early partners for
            Bows for Battle. Their support is helping us launch strong and serve veterans well.
          </p>
          <div class="home-actions">
            <a class="link-button alt" href="sponsorship.html">Business Sponsorship</a>
          </div>
        </aside>
      </div>
    </section>

    <section class="home-section">
      <div class="container home-panel-grid">
        <article class="home-panel">
          <p class="section-head">Service Standard</p>
          <h2>How Veterans Move Through the Program</h2>
          <p>
            The program moves from safe entry to outdoor connection and long-term support. The
            structure stays simple, steady, and veteran-first.
          </p>
          <div class="home-actions">
            <a class="link-button alt" href="programs.html">See the Programs</a>
          </div>
        </article>
        <aside class="home-panel process-list">
          <article class="process-step"><span>1</span><div><h3>Stabilize</h3><p>Veterans begin with equipment access, safe instruction, and clear fundamentals.</p></div></article>
          <article class="process-step"><span>2</span><div><h3>Reconnect</h3><p>Outdoor events and peer support rebuild trust and reduce isolation.</p></div></article>
          <article class="process-step"><span>3</span><div><h3>Strengthen</h3><p>Mentorship and routine help veterans carry progress into daily life.</p></div></article>
        </aside>
      </div>
    </section>

    <section class="home-section">
      <div class="container">
        <p class="section-head">Outdoor Brotherhood</p>
        <h2>What Archery Offers</h2>
        <div class="focus-grid">
          <article class="home-panel"><h3>From Noise to Focus</h3><p>Archery creates a repeatable process where breath, posture, and patience help veterans reset.</p></article>
          <article class="home-panel"><h3>From Isolation to Team</h3><p>Shared practice in the outdoors builds trust with people who understand military culture.</p></article>
          <article class="home-panel"><h3>From Routine to Purpose</h3><p>Consistency over time turns each event into long-term confidence and growth.</p></article>
          <article class="home-panel"><h3>From Support to Impact</h3><p>Community backing funds equipment, events, and mentorship pathways for veterans.</p></article>
        </div>
      </div>
    </section>
""")


# ===========================================================================
# ABOUT
# ===========================================================================

page('about.html', 'About',
     'Who Bows for Battle is, why it exists, who runs it, and where the money goes.',
     phead('About', 'Who we are and how we operate.',
           'Bows for Battle is a new organization. These pages tell you what we intend to do, who is '
           'accountable for doing it, and where the money goes &mdash; without asking you to take any '
           'of it on faith.')
     + hub_cards('about.html'))


page('mission.html', 'Mission &amp; Vision',
     'The mission and vision of Bows for Battle, and the principles the program is built on.',
     phead('About', 'Mission &amp; Vision',
           'What we are here to do, stated plainly.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Our Mission</h2>
            <p>
              Bows for Battle is a nonprofit organization dedicated to supporting veterans through the
              discipline, focus, and healing power of archery. Our mission is to put bows in the hands
              of veterans and create opportunities for them to reconnect with themselves, with fellow
              veterans, and with the outdoors.
            </p>
            <p>
              Through the fundamentals of archery &mdash; stance, breath, focus, patience, and
              precision &mdash; veterans are encouraged to center their energy, quiet the noise of
              daily life, and find strength in the moment. Each shot becomes more than an arrow
              released; it becomes an act of control, clarity, and personal growth.
            </p>
            <p>
              Bows for Battle believes that time outdoors, shared purpose, and veteran camaraderie can
              play a powerful role in healing. By providing access to archery equipment, outdoor
              shooting events, mentorship, and a brotherhood of support, we aim to help veterans
              rediscover confidence, peace, and connection after service.
            </p>
          </article>
          <aside class="highlight">
            <h2>Our Vision</h2>
            <p>
              Bows for Battle envisions a future where no veteran feels isolated, forgotten, or
              without purpose.
            </p>
            <p>
              Through archery, outdoor connection, and veteran camaraderie, we strive to reduce
              avoidable veteran loss by creating spaces where veterans can regain focus, build trust,
              find peace, and reconnect with a community that understands them.
            </p>
            <h2 style="margin-top:1.4rem">What We Stand On</h2>
            <ul class="list">
              <li><strong>Stance</strong> &mdash; build stability before action.</li>
              <li><strong>Breath</strong> &mdash; regulate stress and sharpen attention.</li>
              <li><strong>Focus</strong> &mdash; stay present with intentional movement.</li>
              <li><strong>Patience</strong> &mdash; prioritize discipline and repetition.</li>
              <li><strong>Precision</strong> &mdash; reinforce confidence through control.</li>
            </ul>
          </aside>
        </div>
      </div>
    </section>
""")


page('story.html', 'Our Story',
     'Why Bows for Battle exists, told by its founder, and an honest account of where the organization stands today.',
     phead('About', 'Our Story',
           'Why this exists, and exactly where it stands today.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article>
            <h2>From the Founder</h2>
            <div class="example-block">
              <p>
                I served <span>eight years in the U.S. Army as an infantry squad leader, with
                deployments to Afghanistan in 2011 and 2013</span>. Coming home was harder than I
                expected. The structure was gone, the people were gone, and the quiet was worse than
                the noise had been.
              </p>
              <p>
                A friend put a bow in my hands at a range outside <span>Madison</span> in the fall of
                <span>2023</span>. I was terrible at it. But for twenty seconds at a time, at full
                draw, there was nothing else in my head. No spiraling, no replaying. Just the pin, the
                breath, and the release. I went back the next week, and the week after that.
              </p>
              <p>
                What I noticed over the following year was not really about archery. It was that I had
                somewhere to be, people who expected me there, and something I was measurably getting
                better at. Those three things did more for me than anything else I tried.
              </p>
              <p>
                Bows for Battle exists because equipment and range time cost money, and because doing
                this alone is not the same as doing it with people who understand where you have been.
                We want to remove the first barrier and provide the second.
              </p>
              <p><strong>&mdash; <span>Name</span>, Founder</strong></p>
            </div>
            <p class="status-note">
              <strong>Replace this entire block.</strong> 300&ndash;500 words, first person, from the
              founder. Be specific &mdash; service history, the actual moment archery mattered, and the
              concrete reason the organization exists. Research on new nonprofits is consistent that a
              specific, authentic founder narrative outperforms polished institutional copy with early
              donors. If the story touches a personal crisis, pair it with the crisis line and follow
              safe-messaging guidance.
            </p>
          </article>
          <aside class="highlight">
            <h2>Where We Are Right Now</h2>
            <dl class="def-list">
              <dt>Founded</dt>
              <dd>May 3, 2026</dd>
              <dt>501(c)(3) determination received</dt>
              <dd>2026</dd>
              <dt>Programs delivered to date</dt>
              <dd>Events are announced on our Facebook page.</dd>
              <dt>Veterans served to date</dt>
              <dd>To be published as programs begin.</dd>
            </dl>
            <p style="margin-top:1rem">
              We would rather tell you this plainly than imply a history we do not have. When these
              numbers change, they will change here first.
            </p>
          </aside>
        </div>
      </div>
    </section>
""")


page('board.html', 'Board &amp; Leadership',
     'The volunteer board of directors accountable for how Bows for Battle operates and spends money.',
     phead('About', 'Board &amp; Leadership',
           'The people accountable for how this organization spends money and treats the veterans it serves.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="person-grid">
          <article class="person">
            <img class="portrait" src="Pictures/Logo.png" alt="">
            <h2>Jesse Hall</h2>
            <p class="role">President</p>
            <p>
              Bio details coming soon.
            </p>
          </article>
          <article class="person">
            <img class="portrait" src="Pictures/Logo.png" alt="">
            <h2>Dustin Langsdorf</h2>
            <p class="role">Vice President</p>
            <p>
              Bio details coming soon.
            </p>
          </article>
        </div>

        <p class="status-note" style="margin-top:1.2rem">
          Additional board bios and photos will be published as they are finalized.
        </p>
      </div>
    </section>
""")


page('transparency.html', 'Transparency',
     'Bows for Battle budget, governing documents and how to verify our status independently.',
     phead('About', 'Transparency',
           'We are asking people to fund an organization with no track record. The least we can do is '
           'show our work.')
     + """    <section class="anchor-section" id="goals">
      <div class="container content">
        <h2>Program Goals</h2>
        <p>
          This section is intentionally paused for now. Board-approved program goals will be published
          here once finalized.
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section" id="budget">
      <div class="container content">
        <h2>Where the Money Goes</h2>
        <div class="split-2">
          <article class="highlight">
            <h3>First-Year Budget</h3>
            <div class="table-wrap">
              <table>
                <thead><tr><th>Category</th><th>Budgeted</th><th>Share</th></tr></thead>
                <tbody>
                  <tr><td class="example">Equipment for veterans</td><td class="example">$18,000</td><td class="example">60%</td></tr>
                  <tr><td class="example">Event and range costs</td><td class="example">$7,500</td><td class="example">25%</td></tr>
                  <tr><td class="example">Insurance</td><td class="example">$1,500</td><td class="example">5%</td></tr>
                  <tr><td class="example">Administration and filing</td><td class="example">$3,000</td><td class="example">10%</td></tr>
                </tbody>
              </table>
            </div>
            <p style="margin-top:0.8rem;margin-bottom:0" class="example">
              Bows for Battle operates through volunteer support.
            </p>
          </article>
          <aside class="highlight">
            <h3>Governing Documents</h3>
            <ul class="doc-list">
              <li><span class="example">IRS Determination Letter (PDF)</span></li>
              <li><span class="example">Articles of Incorporation (PDF)</span></li>
              <li><span class="example">Bylaws (PDF)</span></li>
              <li><span class="example">Conflict of Interest Policy (PDF)</span></li>
              <li><span class="example">Form 1023 Application (PDF)</span></li>
            </ul>
            <p style="margin-top:0.8rem;font-size:0.9rem">
              Federal law requires a 501(c)(3) to make its exemption application, determination letter,
              and last three years of Form 990 available on request. We post them instead.
            </p>
            <p style="font-size:0.9rem;margin-bottom:0">
              <strong>Form 990:</strong> <span class="example">Not yet filed. Our first fiscal year
              ends December 31, 2026, and the return will be posted here once filed.</span>
            </p>
          </aside>
        </div>
      </div>
    </section>

    <section class="anchor-section" id="verify">
      <div class="container content">
        <h2>Verify Us Yourself</h2>
        <p>Do not take our word for any of this. You can confirm our status and filings independently:</p>
        <ul class="list">
          <li><a href="https://apps.irs.gov/app/eos/" target="_blank" rel="noopener noreferrer">IRS Tax Exempt Organization Search</a> &mdash; search our EIN</li>
          <li><span class="example">Candid / GuideStar profile</span> &mdash; <span class="example">link once the profile is claimed and the Seal of Transparency is earned</span></li>
          <li><span class="example">Wisconsin DFI charitable organization registry</span></li>
        </ul>
        <p class="status-note">
          <strong>Action needed.</strong> Claim the Candid profile before launch &mdash; Bronze and
          Silver Seals of Transparency are free and achievable immediately by a brand-new
          organization, and the seal badge belongs in the footer. Charity Navigator requires filed
          990s and is a year-two target.
        </p>
        <p>
          We never sell, rent, or trade donor information. See our
          <a href="legal.html#donor-privacy">donor privacy policy</a>.
        </p>
      </div>
    </section>
""")


# ===========================================================================
# PROGRAMS
# ===========================================================================

page('programs.html', 'Programs',
     'What Bows for Battle offers veterans: equipment access, outdoor events and mentorship.',
     phead('Programs', 'Built around consistency, safety, and camaraderie.',
           'Reliable spaces where veterans can practice archery, reconnect outdoors, and build trust '
           'with peers. No prior experience is required, and we provide the equipment.')
     + """    <section class="anchor-section">
      <div class="container content">
        <h2>What We Offer</h2>
        <div class="cards three-up">
          <article class="card">
            <h3>Equipment Access</h3>
            <p>Bows, arrows, releases, and safety gear provided at no cost, so a veteran can start without buying anything.</p>
          </article>
          <article class="card">
            <h3>Outdoor Events</h3>
            <p>Range days and field events that combine focus training with healthy community time.</p>
          </article>
          <article class="card">
            <h3>Mentorship</h3>
            <p>Guidance from peers and coaches to help sustain progress beyond a single event.</p>
          </article>
        </div>
      </div>
    </section>

"""
     + hub_cards('programs.html')
     + """    <section class="anchor-section muted-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Program Principles</h2>
            <ul class="list">
              <li><strong>Stance:</strong> build stability before action.</li>
              <li><strong>Breath:</strong> regulate stress and sharpen attention.</li>
              <li><strong>Focus:</strong> stay present with intentional movement.</li>
              <li><strong>Patience:</strong> prioritize discipline and repetition.</li>
              <li><strong>Precision:</strong> reinforce confidence through control.</li>
            </ul>
            <p style="margin-bottom:0">
              <a class="link-button alt" href="mission.html">Read the Full Mission</a>
            </p>
          </article>
          <aside class="highlight programs-photo">
            <img src="Pictures/3d target with arrows in bullseye.jpg" alt="Arrows grouped tightly in a target">
          </aside>
        </div>
      </div>
    </section>

    <section class="programs-media-row">
      <div class="container programs-gallery">
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture.jpg" alt="Archer practicing form and release outdoors"></figure>
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture1.jpg" alt="Archer at full draw during outdoor training"></figure>
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture2.jpg" alt="Archer focusing on precision at the range"></figure>
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture3.jpg" alt="Archer working on stance and alignment"></figure>
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture4.jpg" alt="Archer releasing an arrow during guided practice"></figure>
        <figure class="highlight programs-photo"><img src="Pictures/archer shooting-picture5.jpg" alt="Archers training together at an outdoor range"></figure>
      </div>
    </section>
""")


page('_what-happens.html', 'What Happens',
     'What a Bows for Battle session is actually like, hour by hour, what to bring and what it costs.',
     phead('Programs', 'What Happens at a Session',
           'Most people want to know what they are walking into before they commit. Here is the '
           'honest version.')
     + """    <section class="anchor-section">
      <div class="container content">
        <h2>Hour by Hour</h2>
        <div class="example-block">
          <dl class="def-list">
            <dt><span>First 15 minutes</span></dt>
            <dd><span>Arrive, coffee, introductions. No icebreakers, no sharing circle. You do not have to talk about your service or why you came.</span></dd>
            <dt><span>Next 30 minutes</span></dt>
            <dd><span>Safety briefing and equipment fitting. A coach measures your draw length and sets you up with a bow that fits. Left-handed and adaptive setups available.</span></dd>
            <dt><span>Next 90 minutes</span></dt>
            <dd><span>Shooting at 10 and 20 yards with coaching. Small groups of three to four with one coach each.</span></dd>
            <dt><span>Last 30 minutes</span></dt>
            <dd><span>Pack up, informal time, and a standing invitation to the next session.</span></dd>
            <dt><span>What you leave with</span></dt>
            <dd><span>A shot you can repeat, a date for the next range day, and the phone number of someone who will notice if you do not show up.</span></dd>
          </dl>
        </div>
        <p class="status-note">
          <strong>Replace with the real program design.</strong> Describe an actual session hour by
          hour, who runs it, group sizes, and what a participant walks away with. Most comparable
          organizations never answer this question and prospective participants have to guess.
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section">
      <div class="container content">
        <h2>Before You Come</h2>
        <div class="cards three-up">
          <article class="card">
            <h3>What it costs</h3>
            <p class="example" style="font-size:1.1rem;font-weight:700">Nothing, for veterans.</p>
            <p class="example" style="margin-bottom:0">
              Range days, intro sessions and equipment use are free. Public fundraiser events have a
              posted entry fee, and veterans still get in free.
            </p>
          </article>
          <article class="card">
            <h3>What to bring</h3>
            <p class="example">
              Nothing. We provide bows, arrows, releases and all safety gear. Wear closed-toe shoes and
              dress for the weather &mdash; outdoor sessions run rain or shine unless we call it off.
            </p>
            <p class="example" style="margin-bottom:0">
              If you already own a bow, bring it. Field points only, no broadheads.
            </p>
          </article>
          <article class="card">
            <h3>Who runs it</h3>
            <p class="example" style="margin-bottom:0">
              Sessions are led by USA Archery Level 2 certified instructors. At least one board member
              is present at every event. Coaches are a mix of veterans and civilian volunteers.
            </p>
          </article>
        </div>

        <div class="split-2" style="margin-top:1.2rem">
          <article class="highlight">
            <h3>Bringing someone</h3>
            <p class="example" style="margin-bottom:0">
              Spouses, family and friends are welcome at range days. Tell us when you sign up so we
              bring enough equipment.
            </p>
          </article>
          <aside class="highlight">
            <h3>Accessibility</h3>
            <p class="example" style="margin-bottom:0">
              Adaptive equipment and seated shooting positions are available at every session. Tell us
              what you need when you sign up and it will be set up before you arrive.
            </p>
          </aside>
        </div>
      </div>
    </section>

    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Ready to come out?</h2>
            <p>Check that you are eligible and put your name in. It takes two minutes.</p>
            <p style="margin-bottom:0"><a class="link-button" href="eligibility.html">Eligibility &amp; Sign Up</a></p>
          </article>
          <aside class="highlight">
            <h2>When is the next one?</h2>
            <p>Every scheduled session, with hours and location, is on the events page.</p>
            <p style="margin-bottom:0"><a class="link-button alt" href="events.html">See the Schedule</a></p>
          </aside>
        </div>
      </div>
    </section>
""")


page('eligibility.html', 'Eligibility &amp; Apply',
     'Who Bows for Battle serves, what the program is not, and how a veteran signs up.',
     phead('Programs', 'Eligibility &amp; How to Apply',
           'We would rather be specific and have you know immediately whether this is for you, than '
           'be vague and waste your time.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Who Is Eligible</h2>
            <dl class="def-list">
              <dt>Service</dt>
              <dd class="example">Any veteran of any branch, any era. Combat service is not required.</dd>
              <dt>Discharge status</dt>
              <dd class="example">Any discharge status other than dishonorable.</dd>
              <dt>Geography</dt>
              <dd class="example">Southern Wisconsin. We are a single-location organization and cannot yet support travel.</dd>
              <dt>Experience</dt>
              <dd class="example">None required. Most participants have never shot a bow.</dd>
              <dt>Physical requirements</dt>
              <dd class="example">None. Adaptive equipment and seated shooting positions are available. Tell us what you need.</dd>
              <dt>Cost</dt>
              <dd class="example">Free.</dd>
            </dl>
          </article>

          <aside class="highlight">
            <h2>What We Are Not</h2>
            <p class="example">
              Bows for Battle is not a clinical or therapeutic program. Our coaches are archery
              instructors and peers, not counselors. We are a place to build a skill alongside people
              who understand military culture &mdash; and we will happily point you toward clinical
              resources if that is what you need.
            </p>
            <p class="status-note" style="margin-top:0.8rem">
              <strong>Important.</strong> Being honest about what the program is <em>not</em> protects
              both the veteran and the organization. Have the board and your insurer review this
              language.
            </p>
          </aside>
        </div>
      </div>
    </section>

    <section class="anchor-section muted-section">
      <div class="container content">
        <h2>How to Sign Up</h2>
        <ol class="list">
          <li class="example">Fill out the interest form below, or call us.</li>
          <li class="example">We call you back within a week to answer questions and confirm a date.</li>
          <li class="example">Complete a liability waiver and a short medical and equipment questionnaire before your first session.</li>
          <li class="example">Show up. We handle the rest.</li>
        </ol>

        <article class="highlight" style="margin-top:1rem">
          <h3>Veteran Interest Form</h3>
          <p class="form-inert">
            This form securely sends your details to our team.
          </p>
          <form aria-label="Veteran interest form" class="email-form" data-form-title="Veteran Interest Form">
            <div class="field">
              <label for="vet-name">Full Name</label>
              <input id="vet-name" name="vet-name" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="vet-email">Email</label>
              <input id="vet-email" name="vet-email" type="email" autocomplete="email">
            </div>
            <div class="field">
              <label for="vet-phone">Phone</label>
              <input id="vet-phone" name="vet-phone" type="tel" autocomplete="tel">
            </div>
            <div class="field">
              <label for="vet-branch">Branch and years of service (optional)</label>
              <input id="vet-branch" name="vet-branch" type="text">
            </div>
            <div class="field">
              <label for="vet-needs">Anything we should know? (optional)</label>
              <textarea id="vet-needs" name="vet-needs" rows="4"></textarea>
            </div>
            <button type="submit">Submit Interest</button>
          </form>
        </article>

        <div class="status-note" style="margin-top:1.2rem">
          <strong>If you are in crisis, please do not wait for us to reply.</strong>
          Dial <a href="tel:988">988 then Press 1</a> to reach the Veterans Crisis Line. Free,
          confidential, 24/7, and you do not need to be enrolled in VA benefits or health care.
        </div>
      </div>
    </section>
""")


page('safety.html', 'Safety',
     'Range safety standards, supervision and insurance for Bows for Battle sessions.',
     phead('Programs', 'Range Safety',
           'Every session is supervised. These are the standards we hold ourselves to, and what we '
           'bring to any range or property that hosts us.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Our Standards</h2>
            <ul class="list">
              <li class="example">All sessions are supervised by a certified instructor.</li>
              <li class="example">A safety briefing is mandatory before every session, including for returning participants.</li>
              <li class="example">Whistle commands control the line. Nobody goes downrange until the line is called clear.</li>
              <li class="example">Equipment is inspected before each session.</li>
              <li class="example">No alcohol before or during sessions.</li>
              <li class="example">A signed liability waiver is required before shooting.</li>
              <li class="example">Field points only. No broadheads.</li>
            </ul>
          </article>
          <aside class="highlight">
            <h2>Insurance</h2>
            <p class="example">
              Bows for Battle carries general liability and participant accident coverage, and
              directors and officers coverage for its board. Certificates are available to partner
              ranges and landowners on request.
            </p>
            <p class="status-note" style="margin-top:0.8rem">
              <strong>Required before any event runs.</strong> Landowners and ranges will ask for proof
              of coverage before allowing an event on their property.
            </p>
            <p style="margin-bottom:0">
              <a class="link-button alt" href="host.html">Hosting Us? What We Bring</a>
            </p>
          </aside>
        </div>
      </div>
    </section>
""")


# ===========================================================================
# EVENTS
# ===========================================================================

page('events.html', 'Events',
     'Every Bows for Battle range day, intro session, work day and fundraiser, with hours, cost and who each one is for.',
     phead('Events', 'One page, every date.',
           'Range days, intro sessions, work days and fundraisers. Each one says who it is for, what '
           'it costs, and where it is. Add any of them to your calendar in one click.')
     + """    <section class="anchor-section" id="schedule">
      <div class="container content">

        <div class="status-note" id="ev-example-note">
          <strong>These are not real events yet.</strong> Bows for Battle has not scheduled its first
          session. Everything listed below is an example showing what a real listing will look like.
          Edit <code>data.js</code> to replace them &mdash; that one file feeds this whole page.
        </div>

        <h2 id="ev-heading">Upcoming Events</h2>

        <div class="filters" id="ev-filters" role="group" aria-label="Filter events">
          <span class="filters-lbl">Show</span>
          <button class="chip on" type="button" data-f="all" aria-pressed="true">Everything</button>
          <button class="chip" type="button" data-f="veterans" aria-pressed="false">For veterans</button>
          <button class="chip" type="button" data-f="public" aria-pressed="false">Open to all</button>
          <button class="chip" type="button" data-f="volunteers" aria-pressed="false">Volunteers</button>
          <button class="chip" type="button" data-f="Range Day" aria-pressed="false">Range Days</button>
          <button class="chip" type="button" data-f="Intro" aria-pressed="false">Intro Sessions</button>
          <button class="chip" type="button" data-f="Fundraiser" aria-pressed="false">Fundraisers</button>
          <button class="chip" type="button" data-f="Work Day" aria-pressed="false">Work Days</button>
        </div>

        <p class="ev-count-line"><span id="ev-count"></span> shown</p>

        <div class="table-wrap">
          <table class="ev-table">
            <caption class="sr-only">Bows for Battle events, with dates, hours and cost</caption>
            <thead>
              <tr>
                <th scope="col">Date</th>
                <th scope="col">Event</th>
                <th scope="col">Hours</th>
                <th scope="col">Cost</th>
              </tr>
            </thead>
            <tbody id="ev-body"></tbody>
          </table>
        </div>

        <div class="status-note" id="ev-empty" hidden></div>

        <p style="margin-top:1rem">
          <button class="link-button alt" type="button" id="ev-past" aria-pressed="false">Show past events</button>
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section" id="calendar">
      <div class="container content">
        <h2>Put the Season on Your Phone</h2>
        <div class="split-2">
          <article class="highlight">
            <h3>Add the whole schedule at once</h3>
            <p>
              One file, every upcoming event. Import it into Google Calendar, Apple Calendar or Outlook
              and the dates come with you.
            </p>
            <p><a class="link-button" href="#" id="ev-ics">Download calendar file (.ics)</a></p>
            <p style="font-size:0.9rem;margin-bottom:0">
              Prefer one event at a time? Open <strong>Details</strong> on any row above and use
              <strong>Add to Google Calendar</strong>.
            </p>
          </article>
          <aside class="highlight">
            <h3>Never miss the first one</h3>
            <p>
              We will email when dates are set. Range dates, weather calls, and nothing else &mdash; no
              more than a couple of messages a month.
            </p>
            <p class="form-inert">
              This form securely sends your details to our team.
            </p>
            <form aria-label="Event notification signup" class="email-form" data-form-title="Event Notification Signup">
              <div class="field">
                <label for="ev-notify">Email</label>
                <input id="ev-notify" name="ev-notify" type="email" autocomplete="email">
              </div>
              <button type="submit">Notify Me</button>
            </form>
          </aside>
        </div>
      </div>
    </section>

    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>First time coming out?</h2>
            <p>
              What a session is like hour by hour, what to bring, and what it costs &mdash; all on one
              page.
            </p>
            <p style="margin-bottom:0"><a class="link-button" href="eligibility.html">Eligibility &amp; Apply</a></p>
          </article>
          <aside class="highlight">
            <h2>Not sure you qualify?</h2>
            <p>Our eligibility criteria are short, specific, and say plainly what we are not.</p>
            <p style="margin-bottom:0"><a class="link-button alt" href="eligibility.html">Check Eligibility</a></p>
          </aside>
        </div>
      </div>
    </section>
""",
     extra_css=('styles-v3-events.css',),
     scripts=('data.js', 'events.js'))


# ===========================================================================
# GET INVOLVED  (help that is not money)
# ===========================================================================

page('get-involved.html', 'Get Involved',
     'Support Bows for Battle with gear, land or range access, or your time.',
     phead('Get Involved', 'Three ways to help that are not money.',
           'A case of arrows, a weekend on your land, or simply showing up to a range day are worth '
           'just as much to a veteran walking through the door for the first time.')
     + hub_cards('get-involved.html')
     + """    <section class="anchor-section muted-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Looking to give money?</h2>
            <p>
              One-time gifts, monthly giving and business sponsorship all live on the Give page, so
              there is one place to find them.
            </p>
            <p style="margin-bottom:0"><a class="link-button" href="give.html">Ways to Give</a></p>
          </article>
          <aside class="highlight">
            <h2>Prefer to help in another way?</h2>
            <p style="margin-bottom:0">
              You can donate gear, offer land or range access, or volunteer at events. Every type of
              support helps us serve more veterans.
            </p>
          </aside>
        </div>
      </div>
    </section>
""")


page('equip.html', 'Donate Gear',
     'Donate bows, arrows, targets, safety equipment or range time to Bows for Battle.',
     phead('Get Involved', 'Donate Gear',
           'If you are a manufacturer, pro shop, or an archer with a bow you no longer shoot, gear is '
           'one of the most directly useful things you can give.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="lane">
          <p class="lane-kicker">Equip</p>
          <h2>Every bow donated is a veteran who does not have to wait.</h2>
          <p>
            Equipment is the difference between a veteran shooting this month and a veteran waiting
            while we raise the money to buy a setup.
          </p>

          <div class="split-2" style="margin-top:1rem">
            <div>
              <h3>What we can use</h3>
              <ul class="list">
                <li class="example">Compound and recurve bows in shootable condition, any draw weight</li>
                <li class="example">Arrows, rests, releases, sights, and quivers</li>
                <li class="example">Targets &mdash; bag, block, and 3D</li>
                <li class="example">Armguards, finger tabs, and other safety gear</li>
                <li class="example">Adaptive equipment of any kind</li>
                <li class="example">Range lane time or bay rental from pro shops</li>
              </ul>
            </div>
            <div>
              <h3>What we cannot use</h3>
              <ul class="list">
                <li class="example">Damaged limbs or cracked risers</li>
                <li class="example">Broadheads &mdash; we shoot field points only</li>
              </ul>
              <p class="status-note" style="margin-top:0.8rem;font-size:0.9rem">
                <strong>Tax note:</strong> we will send a receipt describing what you donated, but IRS
                rules prevent us from assigning it a dollar value &mdash; valuation is the donor's
                responsibility.
              </p>
            </div>
          </div>

          <h3 style="margin-top:1.2rem">Offer Equipment</h3>
          <p class="form-inert">
            This form securely sends your details to our team.
          </p>
          <form aria-label="Equipment donation form" class="email-form" data-form-title="Equipment Donation Form">
            <div class="field">
              <label for="eq-name">Name</label>
              <input id="eq-name" name="eq-name" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="eq-email">Email</label>
              <input id="eq-email" name="eq-email" type="email" autocomplete="email">
            </div>
            <div class="field">
              <label for="eq-org">Business or shop name (if applicable)</label>
              <input id="eq-org" name="eq-org" type="text" autocomplete="organization">
            </div>
            <div class="field">
              <label for="eq-items">What are you offering?</label>
              <textarea id="eq-items" name="eq-items" rows="4" placeholder="Example: one compound bow, 60 lb, plus a dozen arrows and a hard case."></textarea>
            </div>
            <button type="submit">Offer Equipment</button>
          </form>
        </div>
      </div>
    </section>
""")


page('host.html', 'Become a Host',
     'Offer land, range access, hunting property or a guided day to Bows for Battle.',
     phead('Get Involved', 'Become a Host',
           'Access to safe places to shoot is our hardest constraint &mdash; harder than money. If you '
           'own land, run a range, or guide professionally, you can create program capacity that '
           'funding alone cannot buy.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="lane">
          <p class="lane-kicker">Host</p>
          <h2>Ways to host</h2>

          <div class="split-2" style="margin-top:1rem">
            <div>
              <dl class="def-list">
                <dt>Private land</dt>
                <dd>Acreage where we can safely set up a range for a day. We bring targets, equipment, and supervision.</dd>
                <dt>Archery range or club</dt>
                <dd>Recurring lane time or a reserved bay, even a few hours a month.</dd>
                <dt>Hunting property</dt>
                <dd>Access for veterans during season, with or without you guiding.</dd>
                <dt>Guiding or outfitting</dt>
                <dd>Donate a guided day. You bring the expertise, we handle the logistics and the veteran.</dd>
              </dl>
            </div>
            <div>
              <h3>What we bring</h3>
              <ul class="list">
                <li>Proof of general liability and participant accident insurance</li>
                <li>Certified instructors and at least one board member on site</li>
                <li>Signed waivers from every participant</li>
                <li>All targets, equipment, and safety gear</li>
                <li>Site left exactly as we found it</li>
              </ul>
              <p class="status-note" style="margin-top:0.8rem;font-size:0.9rem">
                Landowners in Wisconsin should also be aware of the state's recreational use statute,
                which generally limits liability for landowners who allow recreational access without
                charge. Confirm the specific citation and language with counsel before publishing.
              </p>
            </div>
          </div>

          <h3 style="margin-top:1.2rem">Offer a Location</h3>
          <p class="form-inert">
            This form securely sends your details to our team.
          </p>
          <form aria-label="Host offer form" class="email-form" data-form-title="Host Offer Form">
            <div class="field">
              <label for="host-name">Name</label>
              <input id="host-name" name="host-name" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="host-email">Email</label>
              <input id="host-email" name="host-email" type="email" autocomplete="email">
            </div>
            <div class="field">
              <label for="host-type">What are you offering?</label>
              <select id="host-type" name="host-type">
                <option value="">Select one</option>
                <option>Private land</option>
                <option>Archery range or club access</option>
                <option>Hunting property access</option>
                <option>Guiding or outfitting</option>
                <option>Something else</option>
              </select>
            </div>
            <div class="field">
              <label for="host-location">General location</label>
              <input id="host-location" name="host-location" type="text" placeholder="Example: 40 acres near Mount Horeb, WI">
            </div>
            <div class="field">
              <label for="host-detail">Tell us about it</label>
              <textarea id="host-detail" name="host-detail" rows="4"></textarea>
            </div>
            <button type="submit">Offer a Location</button>
          </form>
        </div>

        <p style="margin-top:1rem">
          Want to know what we do on site? See our
          <a href="safety.html">range safety standards</a>.
        </p>
      </div>
    </section>
""")


page('volunteer.html', 'Volunteer',
     'Volunteer at Bows for Battle events, mentor a veteran, or simply show up.',
     phead('Get Involved', 'Stand With Us',
           'You do not need to be a veteran, and you do not need to know anything about archery. A lot '
           'of what makes a range day work is people setting up targets, running the sign-in table, '
           'and making sure nobody stands around alone.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="lane">
          <p class="lane-kicker">Stand With Us</p>
          <h2>Ways to help</h2>

          <div class="split-2" style="margin-top:1rem">
            <div>
              <ul class="list">
                <li>Event setup and teardown</li>
                <li>Sign-in and check-in table</li>
                <li>Coaching, if you hold an instructor certification</li>
                <li>Peer mentorship &mdash; for veterans who want to walk alongside someone newer</li>
                <li>Food, transportation, and logistics</li>
                <li>Photography, once participants have consented</li>
                <li>Simply attending. Turnout is what makes a room feel worth walking into.</li>
              </ul>
            </div>
            <div>
              <h3>Refer a Veteran</h3>
              <p>
                If you know a veteran who might benefit from this, you can tell us about them &mdash;
                but please talk to them first. We will not cold-contact anyone who has not agreed to
                hear from us.
              </p>
            </div>
          </div>

          <h3 style="margin-top:1.2rem">Volunteer</h3>
          <p class="form-inert">
            This form securely sends your details to our team.
          </p>
          <form aria-label="Volunteer form" class="email-form" data-form-title="Volunteer Form">
            <div class="field">
              <label for="vol-name">Name</label>
              <input id="vol-name" name="vol-name" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="vol-email">Email</label>
              <input id="vol-email" name="vol-email" type="email" autocomplete="email">
            </div>
            <div class="field">
              <label for="vol-help">How would you like to help?</label>
              <textarea id="vol-help" name="vol-help" rows="4"></textarea>
            </div>
            <div class="field">
              <label for="vol-cert">Certifications, if any (optional)</label>
              <input id="vol-cert" name="vol-cert" type="text" placeholder="Example: USA Archery Level 1 Instructor">
            </div>
            <button type="submit">Volunteer</button>
          </form>
        </div>

        <p style="margin-top:1rem">
          Volunteer days and work days are listed on the <a href="events.html">events page</a>.
        </p>
      </div>
    </section>
""")


# ===========================================================================
# GIVE  (money)
# ===========================================================================

page('give.html', 'Give',
     'Ways to give money to Bows for Battle: one-time gifts, monthly giving and business sponsorship.',
     phead('Give', 'Put a bow in a veteran\'s hands.',
           'Bows for Battle is a 501(c)(3) nonprofit and contributions are tax-deductible to the '
           'extent permitted by law.')
     + hub_cards('give.html')
     + """    <section class="anchor-section muted-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Where your money goes</h2>
            <p>
              Your gifts directly support veteran programming, equipment, and event delivery as we
              launch and grow.
            </p>
            <p style="margin-bottom:0"><a class="link-button alt" href="contact.html">Questions About Giving</a></p>
          </article>
          <aside class="highlight">
            <h2>Rather give something other than money?</h2>
            <p>
              Gear, land or range access, and volunteer time are just as useful &mdash; sometimes more
              so.
            </p>
            <p style="margin-bottom:0"><a class="link-button alt" href="get-involved.html">Get Involved</a></p>
          </aside>
        </div>
      </div>
    </section>
""")


page('donate.html', 'Donate',
     'Support Bows for Battle through sponsorship levels that fund events, veterans, and equipment packages.',
     phead('Give', 'Donate',
           'Local businesses may sponsor events, veterans, or equipment packages. Your support '
           'directly helps us change lives and build a stronger veteran community.')
     + """    <section class="anchor-section" id="one-time">
      <div class="container content">
        <h2>Sponsorship Levels</h2>
        <figure class="highlight" style="padding:0;overflow:hidden">
          <img src="Pictures/Sponsorship%20packages.png" alt="Bows for Battle sponsorship levels flyer" style="display:block;width:100%;height:auto">
        </figure>

        <div class="cards auto-fit" style="margin-top:1rem">
          <article class="card">
            <h3>Fuel Hope</h3>
            <p style="font-weight:700">$0 - $249.00</p>
            <p>Every gift-big or small-fuels hope and changes lives.</p>
            <p style="margin-bottom:0">You'll be recognized on our website Supporter Wall.</p>
          </article>
          <article class="card">
            <h3>Bronze Sponsor</h3>
            <p style="font-weight:700">$250</p>
            <ul class="list">
              <li>Name listed on website and social media</li>
              <li>Recognition at sponsored events</li>
              <li>Thank you certificate of appreciation</li>
            </ul>
          </article>
          <article class="card">
            <h3>Silver Sponsor</h3>
            <p style="font-weight:700">$500</p>
            <ul class="list">
              <li>All Bronze benefits</li>
              <li>Logo listed on website and social media</li>
              <li>Recognition at events</li>
              <li>Thank you certificate of appreciation</li>
            </ul>
          </article>
          <article class="card">
            <h3>Gold Sponsor</h3>
            <p style="font-weight:700">$1,000</p>
            <ul class="list">
              <li>All Silver benefits</li>
              <li>Logo on event signage and promotional materials</li>
              <li>Verbal recognition at events</li>
              <li>Thank you certificate of appreciation</li>
            </ul>
          </article>
          <article class="card">
            <h3>Mission Sponsor</h3>
            <p style="font-weight:700">$2,500+</p>
            <ul class="list">
              <li>All Gold benefits</li>
              <li>Premier logo placement on all materials</li>
              <li>Featured recognition in press and promotions</li>
              <li>Opportunity for speaking or presenting at events</li>
              <li>Thank you certificate of appreciation</li>
            </ul>
          </article>
        </div>

        <article class="highlight" style="margin-top:1.2rem">
          <h3>Donation Form</h3>
          <p class="form-inert">
            This form securely sends your details to our team.
            No payment is processed on this page.
          </p>
          <form aria-label="Donation form" class="email-form" data-form-title="Donation Form">
            <div class="field">
              <label for="don-amount">Amount (USD)</label>
              <input id="don-amount" name="don-amount" type="number" min="1" step="1">
            </div>
            <div class="field">
              <label for="don-name">Full Name</label>
              <input id="don-name" name="don-name" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="don-email">Email</label>
              <input id="don-email" name="don-email" type="email" autocomplete="email">
            </div>
            <div class="field">
              <label for="don-note">In honor or memory of (optional)</label>
              <input id="don-note" name="don-note" type="text">
            </div>
            <button type="submit">Donate</button>
          </form>
          <p style="margin-top:0.8rem;font-size:0.88rem;margin-bottom:0">
            You can also mail a check to <span data-org="address">N64W14960 Mill Rd,
            Menomonee Falls, WI 53051</span>.
          </p>
        </article>
      </div>
    </section>

    <section class="anchor-section muted-section" id="other">
      <div class="container content">
        <h2>Where Your Support Goes</h2>
        <div class="split-2">
          <article class="highlight">
            <h3>100% Volunteer-Run</h3>
            <p>
              100% of your donation goes directly to support veterans and our programs.
            </p>
            <p style="margin-bottom:0">
              We are a 100% volunteer-run organization. Every dollar makes a difference.
            </p>
          </article>
          <aside class="highlight">
            <h3>Your Support Helps Fund</h3>
            <ul class="list">
              <li>Events and programs</li>
              <li>Veteran support</li>
              <li>Equipment packages</li>
              <li>Healing and community</li>
            </ul>
          </aside>
        </div>

        <p style="margin-top:1rem">
          Questions about sponsorship benefits? See <a href="sponsorship.html">Business Sponsorship</a>
          or email <a href="mailto:jessehall@bowsforbattle.org">jessehall@bowsforbattle.org</a>.
        </p>
      </div>
    </section>
""")


page('sponsorship.html', 'Business Sponsorship',
     'Business sponsorship tiers for Bows for Battle and what each one funds.',
     phead('Give', 'Business Sponsorship',
           'Sponsorship supports veteran programming directly. Recognition matters because visible '
           'partners help other businesses say yes &mdash; but the point of every tier is what it puts '
           'in a veteran\'s hands.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Package</th>
                <th>Amount</th>
                <th>Recognition</th>
                <th>What It Funds</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Fuel Hope</td>
                <td>$0 &ndash; $249</td>
                <td>Name on the website supporter wall</td>
                <td class="example">Arrows and safety gear</td>
              </tr>
              <tr>
                <td>Bronze Sponsor</td>
                <td>$250</td>
                <td>Name on website and social media, event recognition, thank-you certificate</td>
                <td class="example">A starter setup for one veteran</td>
              </tr>
              <tr>
                <td>Silver Sponsor</td>
                <td>$500</td>
                <td>All Bronze benefits plus logo listing</td>
                <td class="example">Equipment and range costs for one range day</td>
              </tr>
              <tr>
                <td>Gold Sponsor</td>
                <td>$1,000</td>
                <td>All Silver benefits plus signage, promotional placement, verbal recognition</td>
                <td class="example">Starter setups for six veterans</td>
              </tr>
              <tr>
                <td>Mission Sponsor</td>
                <td>$2,500+</td>
                <td>All Gold benefits plus premier logo placement, press recognition, speaking opportunity</td>
                <td class="example">A full season of range days at one partner location</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="status-note" style="margin-top:1rem">
          Tiers and recognition come from <code>Reference/sponsorship_packages.csv</code> and are
          unchanged. The <strong>What It Funds</strong> column is new and needs the treasurer's real
          figures &mdash; it keeps the emphasis on veteran outcomes rather than sponsor perks.
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Sponsorship Inquiry</h2>
            <p class="form-inert">
              This form securely sends your details to our team.
            </p>
            <form aria-label="Sponsorship inquiry form" class="email-form" data-form-title="Sponsorship Inquiry Form">
              <div class="field">
                <label for="sp-company">Business Name</label>
                <input id="sp-company" name="sp-company" type="text" autocomplete="organization">
              </div>
              <div class="field">
                <label for="sp-name">Contact Name</label>
                <input id="sp-name" name="sp-name" type="text" autocomplete="name">
              </div>
              <div class="field">
                <label for="sp-email">Email</label>
                <input id="sp-email" name="sp-email" type="email" autocomplete="email">
              </div>
              <div class="field">
                <label for="sp-package">Package of Interest</label>
                <select id="sp-package" name="sp-package">
                  <option value="">Select one</option>
                  <option>Fuel Hope ($0 - $249)</option>
                  <option>Bronze Sponsor ($250)</option>
                  <option>Silver Sponsor ($500)</option>
                  <option>Gold Sponsor ($1,000)</option>
                  <option>Mission Sponsor ($2,500+)</option>
                  <option>In-kind product or services</option>
                  <option>Not sure yet</option>
                </select>
              </div>
              <div class="field">
                <label for="sp-message">Message (optional)</label>
                <textarea id="sp-message" name="sp-message" rows="4"></textarea>
              </div>
              <button type="submit">Send Inquiry</button>
            </form>
          </article>
          <aside class="highlight">
            <h2>Our Partners</h2>
            <p>
              Huge thanks to our earliest major sponsors: <strong>Sherwood Forest Bowmen</strong>
              and <strong>BK3 Archery</strong>. Their support has been amazing to work with and makes
              veteran programming possible.
            </p>
            <h2 style="margin-top:1.4rem">Prefer to give product?</h2>
            <p>
              Bows, arrows, targets and range time are often more useful to us than a cheque, and they
              are fully deductible in-kind gifts.
            </p>
            <p style="margin-bottom:0"><a class="link-button alt" href="equip.html">Donate Gear</a></p>
          </aside>
        </div>
      </div>
    </section>
""")


# ===========================================================================
# CONTACT
# ===========================================================================

page('contact.html', 'Contact',
     'Contact Bows for Battle about veteran participation, volunteering, hosting, partnerships or donations.',
     phead('Contact', 'Get in touch.',
           'Whether you are a veteran interested in participating, a business wanting to help, or '
           'someone with a bow in the garage you no longer shoot &mdash; we would like to hear from '
           'you.')
     + """    <section class="anchor-section">
      <div class="container content">
        <div class="split-2">
          <article class="highlight">
            <h2>Send a Message</h2>
            <p class="form-inert">
              This form securely sends your details to our team.
            </p>
            <form aria-label="Contact form" class="email-form" data-form-title="Contact Form">
              <div class="field">
                <label for="full-name">Full Name</label>
                <input id="full-name" name="full-name" type="text" autocomplete="name">
              </div>
              <div class="field">
                <label for="contact-email">Email</label>
                <input id="contact-email" name="contact-email" type="email" autocomplete="email">
              </div>
              <div class="field">
                <label for="contact-phone">Phone (optional)</label>
                <input id="contact-phone" name="contact-phone" type="tel" autocomplete="tel">
              </div>
              <div class="field">
                <label for="topic">Topic</label>
                <select id="topic" name="topic">
                  <option value="">Select one</option>
                  <option>Veteran program participation</option>
                  <option>Volunteering</option>
                  <option>Donating equipment or gear</option>
                  <option>Offering land or range access</option>
                  <option>Business sponsorship or partnership</option>
                  <option>Donation or receipt question</option>
                  <option>Media inquiry</option>
                  <option>General inquiry</option>
                </select>
              </div>
              <div class="field">
                <label for="message">Message</label>
                <textarea id="message" name="message" rows="6"></textarea>
              </div>
              <button type="submit">Send Message</button>
            </form>
          </article>

          <aside class="highlight">
            <h2>Reach Us Directly</h2>
            <dl class="def-list">
              <dt>Email</dt>
              <dd><a href="mailto:jessehall@bowsforbattle.org">jessehall@bowsforbattle.org</a></dd>
              <dt>Mailing address</dt>
              <dd><span data-org="address">N64W14960 Mill Rd, Menomonee Falls, WI 53051</span></dd>
              <dt>Response time</dt>
              <dd>Please allow up to a week for a reply.</dd>
            </dl>

            <h2 style="margin-top:1.4rem">Faster Routes</h2>
            <ul class="list">
              <li><a href="eligibility.html">Veteran interest form</a></li>
              <li><a href="equip.html">Offer equipment</a></li>
              <li><a href="host.html">Offer land or range access</a></li>
              <li><a href="volunteer.html">Volunteer</a></li>
              <li><a href="sponsorship.html">Sponsorship inquiry</a></li>
            </ul>

            <div class="status-note" style="margin-top:1.4rem">
              <strong>If you are in crisis, please do not wait for us to reply.</strong>
              Dial <a href="tel:988">988 then Press 1</a> to reach the Veterans Crisis Line. It is
              free, confidential, staffed 24/7, and you do not need to be enrolled in VA benefits or
              health care.
            </div>
          </aside>
        </div>
      </div>
    </section>
""",
     scripts=('data.js', 'events.js'))


# ===========================================================================
# LEGAL
# ===========================================================================

page('legal.html', 'Legal &amp; Policies',
     'Privacy policy, donor privacy policy, accessibility statement and required disclosures for Bows for Battle.',
     """    <section class="page-intro">
      <div class="container narrow content">
        <p class="eyebrow">Legal &amp; Policies</p>
        <h1>Our policies, in plain language.</h1>
        <p>Last updated: <span class="example">[date]</span></p>
        <div class="status-note">
          <strong>Attorney review required before launch.</strong> Everything on this page is a working
          draft based on general research, not legal advice. The receipt language, state disclosure
          text, and solicitation registration status should each be confirmed by a nonprofit attorney
          or a compliance service.
        </div>
      </div>
    </section>

    <nav class="subnav" aria-label="On this page">
      <div class="container">
        <a href="#privacy">Privacy Policy</a>
        <a href="#donor-privacy">Donor Privacy</a>
        <a href="#accessibility">Accessibility</a>
        <a href="#disclosures">Disclosures</a>
      </div>
    </nav>

    <section class="anchor-section" id="privacy">
      <div class="container content">
        <h2>Privacy Policy</h2>

        <h3>What we collect</h3>
        <p>When you use this website, we may collect:</p>
        <ul class="list">
          <li class="example">Your name, email address, phone number, and mailing address, if you provide them through a form</li>
          <li class="example">Information you volunteer in a message, such as branch of service</li>
          <li class="example">Donation amounts and dates</li>
          <li class="example">Basic, anonymous traffic information such as pages visited</li>
        </ul>

        <h3>What we never see</h3>
        <p class="example">
          Payment card numbers are handled entirely by our donation processor. They never pass through
          this website and we never see or store them.
        </p>

        <h3>How we use it</h3>
        <ul class="list">
          <li class="example">To respond to you</li>
          <li class="example">To send tax receipts and acknowledgments</li>
          <li class="example">To send program and event updates, if you asked for them</li>
          <li class="example">To keep the records a nonprofit is required to keep</li>
        </ul>

        <h3>Who we share it with</h3>
        <p class="example">
          Only service providers who help us operate &mdash; our donation processor and our email
          service. They may use your information only to perform that service. We also disclose
          information when required by law.
        </p>

        <h3>Email</h3>
        <p class="example">
          Every email we send includes a working unsubscribe link and our physical mailing address, and
          we honor unsubscribe requests promptly.
        </p>

        <h3>Your choices</h3>
        <p class="example">
          You can ask us what information we hold about you, correct it, or ask us to delete it. Email
          jessehall@bowsforbattle.org and we will respond within 30 days.
        </p>

        <h3>Children</h3>
        <p class="example">
          This website is not directed to children under 13 and we do not knowingly collect their
          information.
        </p>

        <p class="status-note">
          <strong>Note on scope.</strong> California's CCPA excludes nonprofits, but CalOPPA still
          requires a posted privacy policy for any site collecting personal information from California
          residents. Colorado's privacy law has no nonprofit exemption at all &mdash; drafting to
          Colorado-adequate standards covers you everywhere.
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section" id="donor-privacy">
      <div class="container content">
        <h2>Donor Privacy Policy</h2>
        <article class="highlight">
          <p style="font-size:1.15rem;font-weight:700">
            Bows for Battle never sells, rents, trades, or shares donor information with any other
            organization for their own use.
          </p>
          <p style="margin-bottom:0">
            This applies to every donor, at every level, whether or not you ask.
          </p>
        </article>

        <h3>Recognition</h3>
        <p class="example">
          We list supporter names on our website and at events only with permission. You can give
          anonymously, and you can change your mind at any time by contacting us.
        </p>

        <h3>Communication</h3>
        <p class="example">
          You can ask us to stop contacting you, or to contact you less often, and we will honor that
          without asking you to justify it.
        </p>

        <h3>Receipts</h3>
        <p class="example">
          Every donation receives a written acknowledgment containing our legal name, EIN, the date,
          the amount, and a statement of whether any goods or services were provided in return.
        </p>
        <p class="example">
          For donated equipment, our receipt will describe the item but will not assign it a dollar
          value. IRS rules place the responsibility for valuing a non-cash gift on the donor.
        </p>
        <p class="example">
          Where a contribution includes something of value in return &mdash; an event ticket that
          includes a meal, for example &mdash; we will tell you the fair market value of what you
          received and the portion of your payment that is deductible.
        </p>
        <p class="status-note">
          <strong>Compliance note.</strong> The $250 written-acknowledgment rule and the $75 quid pro
          quo disclosure rule are both IRS requirements with penalties attached, and the quid pro quo
          rule is the one most likely to apply to an archery nonprofit running tournaments, banquets,
          and raffles. Note also that <strong>raffle ticket purchases are not deductible at all</strong>,
          and Wisconsin regulates raffles separately.
        </p>
      </div>
    </section>

    <section class="anchor-section" id="accessibility">
      <div class="container content">
        <h2>Accessibility Statement</h2>
        <p>
          Many veterans live with service-connected vision, hearing, motor, or cognitive impairments. A
          website that is difficult for them to use is a failure of our mission, not just a technical
          shortcoming.
        </p>

        <h3>Our commitment</h3>
        <p class="example">
          We aim to meet Web Content Accessibility Guidelines (WCAG) 2.1 Level AA across this website.
        </p>

        <h3>What we have done</h3>
        <ul class="list">
          <li class="example">Semantic headings and landmarks so screen readers can navigate the page structure</li>
          <li class="example">A skip-to-content link on every page</li>
          <li class="example">Visible keyboard focus indicators, and full keyboard operability</li>
          <li class="example">Text contrast meeting or exceeding WCAG AA ratios</li>
          <li class="example">Labels on every form field</li>
          <li class="example">Alternative text on images that carry meaning</li>
          <li class="example">Respect for reduced-motion preferences</li>
        </ul>

        <h3>Known limitations</h3>
        <p class="example">
          This site is under active development. Some sections are incomplete, and forms are not yet
          functional.
        </p>

        <h3>Tell us about a problem</h3>
        <p class="example">
          If any part of this site is difficult to use, email jessehall@bowsforbattle.org and
          describe what happened. We will fix it and tell you when it is done. If
          you need information from this site in another format, ask and we will provide it.
        </p>
      </div>
    </section>

    <section class="anchor-section muted-section" id="disclosures">
      <div class="container content">
        <h2>Required Disclosures</h2>

        <h3>Tax-exempt status</h3>
        <p>
          <span>Bows for Battle, Inc.</span> is a nonprofit corporation organized under
          the laws of <span>the State of Wisconsin</span> and recognized by the
          Internal Revenue Service as tax-exempt under Section 501(c)(3) of the Internal Revenue Code.
          <span>EIN: 42-2771314.</span> Contributions are tax-deductible to the extent
          permitted by law.
        </p>

        <h3>Charitable solicitation registration</h3>
        <p class="example">
          Bows for Battle is registered to solicit charitable contributions in the State of Wisconsin.
          We do not currently solicit contributions in states where we are not registered.
        </p>
        <p class="status-note">
          <strong>Confirm before launch.</strong> A donate button legally constitutes solicitation.
          Verify registration with the Wisconsin Department of Financial Institutions (dfi.wi.gov,
          608-261-9555), or document the applicable exemption if you qualify. Once receipts exceed
          the exemption threshold, registration is required within 30 days.
          <br><br>
          Roughly 40 jurisdictions require registration triggered by online solicitation, and several
          require specific disclosure wording to appear verbatim wherever donations are accepted.
          Multi-state registration is not a rational first-year expense &mdash; track incoming gifts by
          state and register elsewhere when volume justifies it. Any state-mandated language belongs in
          this section.
        </p>

        <h3>Public inspection of documents</h3>
        <p>
          Federal law requires us to make our exemption application, determination letter, and three
          most recent annual returns available for public inspection. You can request these directly by
          email at <a href="mailto:jessehall@bowsforbattle.org">jessehall@bowsforbattle.org</a>.
        </p>

        <h3>No government affiliation</h3>
        <p>
          Bows for Battle is an independent nonprofit organization. We are not affiliated with,
          endorsed by, or a partner of the U.S. Department of Veterans Affairs or any branch of the
          United States Armed Forces.
        </p>
      </div>
    </section>
""",
     scripts=('data.js', 'events.js'))


if __name__ == '__main__':
    write_all()
