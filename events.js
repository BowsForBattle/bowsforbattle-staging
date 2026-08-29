/* ============================================================
   Bows for Battle - events page rendering
   ------------------------------------------------------------
   Reads EVENTS and ORG from data.js and renders the schedule
   table, the filter chips, the per-event calendar links and the
   whole-season .ics download.

   Nothing here needs editing to change an event. Edit data.js.
   ============================================================ */
(function () {
  'use strict';

  if (typeof EVENTS === 'undefined') { return; }

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  /* ---------------- dates ---------------- */

  function parse(isoDate) {
    var p = isoDate.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function pad(n) { return String(n).padStart(2, '0'); }
  function iso(d) {
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }
  function todayIso() {
    var n = new Date();
    return iso(new Date(n.getFullYear(), n.getMonth(), n.getDate()));
  }
  function fmtLong(isoDate) {
    var d = parse(isoDate);
    return DAYS[d.getDay()] + ', ' + MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();
  }
  function fmtSpan(e) {
    if (!e.end) { return fmtLong(e.date); }
    var a = parse(e.date), b = parse(e.end);
    if (a.getMonth() === b.getMonth()) {
      return MONTHS[a.getMonth()] + ' ' + a.getDate() + '-' + b.getDate() + ', ' + b.getFullYear();
    }
    return MONTHS[a.getMonth()] + ' ' + a.getDate() + ' - ' +
           MONTHS[b.getMonth()] + ' ' + b.getDate() + ', ' + b.getFullYear();
  }
  function daysOut(isoDate) {
    return Math.round((parse(isoDate) - parse(todayIso())) / 86400000);
  }
  function countdown(isoDate) {
    var n = daysOut(isoDate);
    if (n < 0) { return ''; }
    if (n === 0) { return 'Today'; }
    if (n === 1) { return 'Tomorrow'; }
    if (n < 31) { return 'In ' + n + ' days'; }
    var m = Math.round(n / 30.4);
    return 'In about ' + m + (m === 1 ? ' month' : ' months');
  }

  /* ---------------- calendar entries ----------------
     Turns "9:00 am - 1:00 pm" into start and end hours. Returns null
     when hours have not been posted, which makes an all-day calendar
     entry rather than inventing a time. */

  function parseTime(s) {
    if (!s) { return null; }
    var m = s.match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*(?:-|to|–|—)\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)/i);
    if (!m) { return null; }
    function to24(h, ap) {
      h = +h;
      ap = (ap || '').toLowerCase();
      if (ap === 'pm' && h !== 12) { h += 12; }
      if (ap === 'am' && h === 12) { h = 0; }
      return h;
    }
    var endAp = m[6];
    var startAp = m[3] || endAp;
    return {
      sh: to24(m[1], startAp), sm: +(m[2] || 0),
      eh: to24(m[4], endAp), em: +(m[5] || 0)
    };
  }
  function stamp(isoDate, h, mi) {
    return isoDate.replace(/-/g, '') + 'T' + pad(h) + pad(mi) + '00';
  }
  /* Calendar end dates are exclusive, so an all-day event needs +1 day. */
  function exclusiveEnd(e) {
    var d = parse(e.end || e.date);
    d.setDate(d.getDate() + 1);
    return iso(d).replace(/-/g, '');
  }
  function tz() {
    if (typeof ORG !== 'undefined' && ORG.timezone) { return ORG.timezone; }
    try {
      return Intl.DateTimeFormat().resolvedOptions().timeZone;
    } catch (err) {
      return 'America/Chicago';
    }
  }

  function gcalUrl(e) {
    var t = parseTime(e.time);
    var dates = t
      ? stamp(e.date, t.sh, t.sm) + '/' + stamp(e.date, t.eh, t.em)
      : e.date.replace(/-/g, '') + '/' + exclusiveEnd(e);
    var parts = [];
    if (e.time) { parts.push(e.time); }
    if (e.cost) { parts.push('Cost: ' + e.cost); }
    if (e.detail) { parts.push(e.detail); }
    parts.push('bowsforbattle.org');
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE' +
      '&text=' + encodeURIComponent(e.name + ' - Bows for Battle') +
      '&dates=' + dates +
      (t ? '&ctz=' + encodeURIComponent(tz()) : '') +
      '&details=' + encodeURIComponent(parts.join('\n')) +
      '&location=' + encodeURIComponent(e.location || '');
  }

  function icsEscape(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/\\/g, '\\\\')
      .replace(/;/g, '\\;')
      .replace(/,/g, '\\,')
      .replace(/\r?\n/g, '\\n');
  }

  function vevent(e, stampNow) {
    var t = parseTime(e.time);
    var uid = 'bfb-' + e.date + '-' +
      e.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') +
      '@bowsforbattle.org';
    var lines = ['BEGIN:VEVENT', 'UID:' + uid, 'DTSTAMP:' + stampNow];
    if (t) {
      lines.push('DTSTART;TZID=' + tz() + ':' + stamp(e.date, t.sh, t.sm));
      lines.push('DTEND;TZID=' + tz() + ':' + stamp(e.date, t.eh, t.em));
    } else {
      lines.push('DTSTART;VALUE=DATE:' + e.date.replace(/-/g, ''));
      lines.push('DTEND;VALUE=DATE:' + exclusiveEnd(e));
    }
    var desc = [];
    if (e.time) { desc.push(e.time); }
    if (e.cost) { desc.push('Cost: ' + e.cost); }
    if (e.detail) { desc.push(e.detail); }
    if (e.contact) { desc.push('Contact: ' + e.contact); }
    desc.push('bowsforbattle.org');
    lines.push('SUMMARY:' + icsEscape(e.name + ' - Bows for Battle'));
    lines.push('DESCRIPTION:' + icsEscape(desc.join('\n')));
    if (e.location) { lines.push('LOCATION:' + icsEscape(e.location)); }
    lines.push('END:VEVENT');
    return lines.join('\r\n');
  }

  function buildIcs(list) {
    var now = new Date();
    var stampNow = now.getUTCFullYear() + pad(now.getUTCMonth() + 1) + pad(now.getUTCDate()) +
      'T' + pad(now.getUTCHours()) + pad(now.getUTCMinutes()) + pad(now.getUTCSeconds()) + 'Z';
    return ['BEGIN:VCALENDAR', 'VERSION:2.0',
            'PRODID:-//Bows for Battle//Events//EN', 'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH', 'X-WR-CALNAME:Bows for Battle']
      .concat(list.map(function (e) { return vevent(e, stampNow); }))
      .concat(['END:VCALENDAR'])
      .join('\r\n');
  }

  /* ---------------- markup helpers ---------------- */

  var WHO_LABEL = {
    veterans: 'Veterans',
    public: 'Open to all',
    volunteers: 'Volunteers'
  };

  function esc(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function badges(e) {
    var out = '';
    if (e.cat) { out += '<span class="ev-badge ev-cat">' + esc(e.cat) + '</span>'; }
    if (e.who && WHO_LABEL[e.who]) {
      out += '<span class="ev-badge ev-who ev-who-' + esc(e.who) + '">' + WHO_LABEL[e.who] + '</span>';
    }
    return out;
  }
  function flags(e) {
    var out = '';
    if (e.example) { out += '<span class="example ev-flag">example event</span>'; }
    if (e.tag) { out += '<span class="example ev-flag">' + esc(e.tag) + '</span>'; }
    return out;
  }

  /* ---------------- state ---------------- */

  var filter = 'all';
  var showPast = false;

  function matches(e) {
    if (filter === 'all') { return true; }
    if (filter === 'veterans' || filter === 'public' || filter === 'volunteers') {
      return e.who === filter;
    }
    return e.cat === filter;
  }

  function visible() {
    var t = todayIso();
    return EVENTS
      .filter(function (e) {
        var over = (e.end || e.date) < t;
        return showPast ? over : !over;
      })
      .filter(matches)
      .sort(function (a, b) {
        return showPast ? (a.date < b.date ? 1 : -1) : (a.date < b.date ? -1 : 1);
      });
  }

  /* ---------------- render ---------------- */

  function row(e, i) {
    var id = 'ev-detail-' + i;
    var cd = showPast ? '' : countdown(e.date);
    return '' +
      '<tr class="ev-row' + (e.example ? ' ev-row-example' : '') + '">' +
        '<td class="ev-date">' +
          '<span class="ev-date-main">' + esc(fmtSpan(e)) + '</span>' +
          (cd ? '<span class="ev-countdown">' + esc(cd) + '</span>' : '') +
        '</td>' +
        '<td class="ev-main">' +
          '<span class="ev-name">' + esc(e.name) + '</span>' +
          '<span class="ev-badges">' + badges(e) + flags(e) + '</span>' +
          (e.location ? '<span class="ev-loc">' + esc(e.location) + '</span>' : '') +
          '<button class="ev-toggle" type="button" aria-expanded="false" aria-controls="' + id + '">Details</button>' +
          '<div class="ev-detail" id="' + id + '" hidden>' +
            (e.detail ? '<p>' + esc(e.detail) + '</p>' : '') +
            (e.contact ? '<p class="ev-contact"><strong>Contact:</strong> ' + esc(e.contact) + '</p>' : '') +
            '<a class="link-button btn-sm" href="' + esc(gcalUrl(e)) + '" target="_blank" rel="noopener noreferrer">Add to Google Calendar</a>' +
          '</div>' +
        '</td>' +
        '<td class="ev-time">' + (e.time ? esc(e.time) : '<span class="example">hours to be posted</span>') + '</td>' +
        '<td class="ev-cost">' + (e.cost ? esc(e.cost) : '<span class="example">cost to be posted</span>') + '</td>' +
      '</tr>';
  }

  function render() {
    var body = document.getElementById('ev-body');
    if (!body) { return; }

    var list = visible();
    body.innerHTML = list.map(row).join('');

    var empty = document.getElementById('ev-empty');
    if (empty) {
      empty.hidden = list.length > 0;
      if (!list.length) {
        empty.innerHTML = showPast
          ? '<strong>No past events.</strong> Bows for Battle has not held an event yet. ' +
            'Once the first one happens it stays listed here.'
          : '<strong>Nothing matches that filter.</strong> Choose "Everything" to see the full schedule.';
      }
    }

    var count = document.getElementById('ev-count');
    if (count) {
      count.textContent = list.length + (list.length === 1 ? ' event' : ' events');
    }

    var note = document.getElementById('ev-example-note');
    if (note) {
      note.hidden = list.filter(function (e) { return e.example; }).length === 0;
    }
  }

  /* ---------------- wire up ---------------- */

  document.addEventListener('DOMContentLoaded', function () {
    var chips = document.querySelectorAll('#ev-filters .chip');
    Array.prototype.forEach.call(chips, function (c) {
      c.addEventListener('click', function () {
        Array.prototype.forEach.call(chips, function (o) {
          o.classList.remove('on');
          o.setAttribute('aria-pressed', 'false');
        });
        c.classList.add('on');
        c.setAttribute('aria-pressed', 'true');
        filter = c.getAttribute('data-f');
        render();
      });
    });

    var pastBtn = document.getElementById('ev-past');
    if (pastBtn) {
      pastBtn.addEventListener('click', function () {
        showPast = !showPast;
        pastBtn.setAttribute('aria-pressed', showPast ? 'true' : 'false');
        pastBtn.textContent = showPast ? 'Show upcoming events' : 'Show past events';
        var h = document.getElementById('ev-heading');
        if (h) { h.textContent = showPast ? 'Past Events' : 'Upcoming Events'; }
        render();
      });
    }

    /* Expand or collapse one event's details. */
    var body = document.getElementById('ev-body');
    if (body) {
      body.addEventListener('click', function (evt) {
        var btn = evt.target.closest ? evt.target.closest('.ev-toggle') : null;
        if (!btn) { return; }
        var panel = document.getElementById(btn.getAttribute('aria-controls'));
        if (!panel) { return; }
        var open = !panel.hidden;
        panel.hidden = open;
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        btn.textContent = open ? 'Details' : 'Hide details';
      });
    }

    var dl = document.getElementById('ev-ics');
    if (dl) {
      dl.addEventListener('click', function (evt) {
        evt.preventDefault();
        var t = todayIso();
        var future = EVENTS.filter(function (e) { return (e.end || e.date) >= t; });
        if (!future.length) { return; }
        var blob = new Blob([buildIcs(future)], { type: 'text/calendar;charset=utf-8' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'bows-for-battle-events.ics';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      });
    }

    /* Org facts injected from data.js so they are typed in exactly one place. */
    if (typeof ORG !== 'undefined') {
      Array.prototype.forEach.call(document.querySelectorAll('[data-org]'), function (el) {
        var k = el.getAttribute('data-org');
        if (ORG[k]) { el.textContent = ORG[k]; }
      });
    }

    render();
  });
})();
