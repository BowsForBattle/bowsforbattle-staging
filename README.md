# Bows for Battle Website

This is the redesigned Bows for Battle website. It is a **draft** and is not live — the public site is
still at bowsforbattle.org on Squarespace.

## How to open it

Double-click **`index.html`**. It opens in your browser. Nothing to install.

Keep all the files together in one folder. If the `Pictures` folder is moved or missing, images will
not load.

## The yellow highlighted text

Everywhere you see **yellow highlighted text with a dashed underline**, that is example content. It is
not real. It is there to show what kind of information belongs in that spot, so it is clear what we
need from you.

For instance, the board page currently lists "Jane Doe, Board Chair" with a plausible-looking bio.
That is not a real person — it demonstrates the level of detail a real board entry should have.

Every page also carries a yellow strip near the top reminding reviewers of this.

**Nothing highlighted in yellow should survive to launch.**

Some highlighted sections are followed by a bordered note explaining what specifically is needed and
who needs to provide it. Those notes are for us and also come out before launch.

## How the site is organized

The site answers two questions, because those are the only two reasons anyone visits: *"I served — is
this for me?"* and *"I want to help — how?"* The home page gives each one its own door.

Below that, every top-level menu item is a short **hub** page that routes you to focused pages
underneath it.

| Menu item | Hub page | Pages underneath it |
|---|---|---|
| Home | `index.html` | — |
| About | `about.html` | `mission.html`, `story.html`, `board.html`, `transparency.html` |
| Programs | `programs.html` | `what-happens.html`, `eligibility.html`, `safety.html` |
| Events | `events.html` | — |
| Get Involved | `get-involved.html` | `equip.html`, `host.html`, `volunteer.html` |
| Give | `give.html` | `donate.html`, `sponsorship.html` |
| Contact | `contact.html` | — |

Plus `legal.html` (privacy, donor privacy, accessibility, disclosures), linked from every footer.

**Get Involved is for help that is not money. Give is for money.** They do not overlap, so there is
never a question which one to use.

### One fact, one home

Every piece of information lives on exactly one page. Other pages link to it instead of repeating it.
The budget is only on `transparency.html`. What a session costs is only on `what-happens.html`.
Sponsorship tiers are only on `sponsorship.html`.

If you find yourself pasting the same paragraph onto a second page, link to the first page instead.
Duplicated content is what made an earlier version of this site confusing.

## Changing an event

Events are not edited in HTML. Open **`data.js`** and edit the `EVENTS` list. That single file feeds
the whole events page — the table, the filters and the calendar downloads.

```js
{
  date: "2027-04-17",                     // YYYY-MM-DD
  name: "Spring Range Day",
  cat: "Range Day",                       // Range Day | Intro | Fundraiser | Meeting | Work Day
  who: "veterans",                        // veterans | public | volunteers
  time: "9:00 am - 1:00 pm",              // leave "" if hours are not set
  cost: "Free",
  location: "Example Archery Club, Mount Horeb, WI",
  detail: "Shown when someone opens Details.",
  contact: "Program coordinator",
  example: true                           // DELETE this line once the event is real
}
```

`example: true` marks the entry as a placeholder — it renders highlighted and triggers the warning at
the top of the page. **Delete that line when the event is real.** For an otherwise real event with one
detail unconfirmed, use `tag: "hours to confirm"` instead.

Events move themselves from Upcoming to Past based on the date. Nobody has to tidy up later.

## What does not work yet

**None of the forms do anything.** Contact, volunteer, equipment, host, veteran interest, donation —
all inert. Each shows a blue "not yet active" notice. Filling one out sends nothing to anyone.

The donation form does not take payments and never will in this form — payment will be handled by an
outside service so that no card details ever touch this site.

## What to do with this

Read through it and tell us:

1. Anything highlighted in yellow that you can replace with real information.
2. Anything that is wrong, missing, or worded badly.
3. Anything you disagree with.

The full plan behind this redesign, including the research it is based on and the complete list of
what we need from the board, is in **`BowsForBattle_Website_Plan_v2.md`**.

---

## For whoever edits the files

**Do not edit the .html files directly. They are generated and your changes will be overwritten.**

Everything lives in `build.py`. Edit it, then run:

```bash
python build.py
```

That writes all 20 `.html` files. The header, footer, navigation and draft banner are defined once in
`build.py`, so a nav change is a one-line edit rather than twenty. No Node, no dependencies — the
output is ordinary static HTML you can still double-click.

| File | Purpose |
|---|---|
| `build.py` | The site. Nav, header, footer and every page body. |
| `data.js` | Events and a few org facts. The only file to edit to change the schedule. |
| `events.js` | Renders the events table, filters and calendar exports. |
| `styles.css` | Original stylesheet. |
| `styles-v2.css` | Structural additions, loads second. |
| `styles-v3-events.css` | Events page only. |

Bump `REV` in `build.py` on every deploy so cached CSS and JS refresh together.

To count the example placeholders still outstanding:

```bash
grep -o 'class="[^"]*example[^"]*"' *.html | cut -d: -f1 | uniq -c
```
