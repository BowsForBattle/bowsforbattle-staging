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
  address: "1234 Example Road, Barneveld, WI 53507",
  addressExample: true,
  email: "info@bowsforbattle.org",
  phone: "(608) 555-0142",
  phoneExample: true,
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

   Bows for Battle has not held an event yet. Every entry below
   is an example showing the shape of a real one. Replace them
   as actual dates are set - and delete any that are still
   examples before this page goes live.
   ------------------------------------------------------------ */

const EVENTS = [
  {
    date: "2026-10-17",
    name: "Introduction to Archery",
    cat: "Intro", who: "veterans",
    time: "9:00 am - 12:00 pm",
    cost: "Free",
    location: "Example Archery Club, Mount Horeb, WI",
    detail: "A first session for veterans who have never shot a bow. Equipment, coaching and " +
            "safety instruction all provided. No experience needed and nothing to bring.",
    contact: "Program coordinator",
    example: true
  },
  {
    date: "2026-11-14",
    name: "Fall Range Day",
    cat: "Range Day", who: "veterans",
    time: "9:00 am - 1:00 pm",
    cost: "Free",
    location: "Example Archery Club, Mount Horeb, WI",
    detail: "Open range time with coaches on hand. Come for the whole morning or drop in for an " +
            "hour. Returning participants and first-timers shoot together.",
    contact: "Program coordinator",
    example: true
  },
  {
    date: "2027-02-20",
    name: "Winter Indoor Session",
    cat: "Range Day", who: "veterans",
    time: "10:00 am - 2:00 pm",
    cost: "Free",
    location: "Example Indoor Range, Madison, WI",
    detail: "Indoor shooting at 20 yards through the winter months, so the program does not stop " +
            "when the weather turns.",
    contact: "Program coordinator",
    example: true
  },
  {
    date: "2027-04-17",
    name: "Spring Range Day",
    cat: "Range Day", who: "veterans",
    time: "9:00 am - 1:00 pm",
    cost: "Free",
    location: "Example Archery Club, Mount Horeb, WI",
    detail: "First outdoor session of the season. Equipment provided, coaches on the line, and " +
            "time afterward for anyone who wants to stay.",
    contact: "Program coordinator",
    example: true
  },
  {
    date: "2027-05-15",
    name: "Intro to 3D Field Archery",
    cat: "Intro", who: "veterans",
    time: "9:00 am - 2:00 pm",
    cost: "Free",
    location: "Example Conservation Land, Blue Mounds, WI",
    detail: "Walking a 3D course with foam targets at unmarked distances. For veterans who have " +
            "attended at least one range day.",
    contact: "Program coordinator",
    example: true
  },
  {
    date: "2027-06-19",
    name: "Family Day and Fundraiser Shoot",
    cat: "Fundraiser", who: "public",
    time: "10:00 am - 4:00 pm",
    cost: "$20 per shooter, veterans free",
    location: "Example Archery Club, Mount Horeb, WI",
    detail: "Open to everyone. Food, raffle and a shooting course set for all skill levels. This " +
            "is the event that funds the rest of the year.",
    contact: "Event chair",
    example: true
  },
  {
    date: "2027-03-13",
    name: "Course Setup Work Day",
    cat: "Work Day", who: "volunteers",
    time: "8:00 am - 1:00 pm",
    cost: "Free",
    location: "Example Conservation Land, Blue Mounds, WI",
    detail: "Setting targets and clearing lanes before the outdoor season. Bring gloves. Lunch " +
            "provided. No archery experience required.",
    contact: "Volunteer coordinator",
    example: true
  }
];
