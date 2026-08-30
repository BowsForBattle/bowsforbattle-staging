/* ============================================================
   Bows for Battle - SITE DATA
   ------------------------------------------------------------
   THIS IS THE ONLY FILE THAT NEEDS EDITING TO CHANGE AN EVENT.

   The events page, the filters and the calendar downloads are
   all generated from what is below, so a date typed here cannot
   disappear from one place and linger on another.

   FLAGS that render on the page so nothing is silently invented:
     example: true    the whole entry is a placeholder, not a
                      real event. It renders highlighted.
     tag: "..."       an amber note - something still to confirm
                      on an otherwise real entry.
   Delete the flag when the real value goes in.
   ============================================================ */

const ORG = {
  name: "Bows for Battle, Inc.",
  address: "N64W14960 Mill Rd, Menomonee Falls, WI 53051",
  email: "jessehall@bowsforbattle.org",
  timezone: "America/Chicago"
};

/* ------------------------------------------------------------
   EVENTS

   date     ISO date, "YYYY-MM-DD"
   end      optional ISO date for multi-day events
   name     what it is called
   cat      Range Day | Intro | Fundraiser | Meeting | Work Day
   who      veterans | public | volunteers
   time     posted hours, or "" if not set yet
   cost     what it costs to attend
   location where it is
   detail   a sentence or two shown when the row is opened
   contact  who to ask
   ------------------------------------------------------------ */

const EVENTS = [
   {
      date: "2026-09-20",
      name: "Bows for Battle Meat Raffle",
      cat: "Fundraiser", who: "public",
      time: "1:00 pm - 3:00 pm",
      cost: "Raffle entry at event",
      location: "American Legion Post 294, 231 Goodwin Avenue, Hartland, WI 53029",
      detail: "Hosted by American Legion Auxiliary Post 294. All proceeds support Bows for Battle.",
      contact: "Bows for Battle"
   },
   {
      date: "2027-01-16",
      end: "2027-01-17",
      name: "Winter Warrior 3D Shoot - First Bow Presentation",
      cat: "Fundraiser", who: "public",
      time: "",
      cost: "",
      location: "Sherwood Forest Bowmen, Sussex, WI",
      detail: "Bows for Battle will present its first five bows to veterans during the Winter Warrior 3D Shoot.",
      contact: "Bows for Battle"
   }
];
