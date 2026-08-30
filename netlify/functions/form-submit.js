/* ============================================================
   Bows for Battle - Netlify form submission endpoint
   ------------------------------------------------------------
   Validates and sanitizes form submissions, applies anti-spam
   checks, and sends the email through Resend.
   ============================================================ */

const RESEND_ENDPOINT = 'https://api.resend.com/emails';
const DEFAULT_RECIPIENTS = [
  'jessehall@bowsforbattle.org',
  'dustinlangsdorf@bowsforbattle.org'
];
const ALLOWED_FORMS = new Set([
  'Veteran Interest Form',
  'Event Notification Signup',
  'Equipment Donation Form',
  'Host Offer Form',
  'Volunteer Form',
  'Donation Form',
  'Sponsorship Inquiry Form',
  'Contact Form'
]);

const MAX_BODY_BYTES = 30 * 1024;
const MAX_FIELDS = 40;
const MAX_FIELD_VALUE = 2000;
const MAX_FIELD_LABEL = 120;
const MIN_ELAPSED_MS = 2500;
const MAX_LINKS = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_MAX_PER_WINDOW = 6;

const RATE_BUCKET = new Map();

function json(statusCode, payload) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store'
    },
    body: JSON.stringify(payload)
  };
}

function now() {
  return Date.now();
}

function clean(value) {
  return String(value === undefined || value === null ? '' : value)
    .replace(/\0/g, '')
    .trim();
}

function cleanSingleLine(value) {
  return clean(value).replace(/[\r\n]+/g, ' ').slice(0, MAX_FIELD_LABEL);
}

function containsSuspiciousContent(value) {
  if (!value) { return false; }
  const lowered = value.toLowerCase();
  return lowered.includes('<script') || lowered.includes('javascript:') || lowered.includes('onerror=');
}

function urlCount(value) {
  const matches = String(value).match(/https?:\/\//gi);
  return matches ? matches.length : 0;
}

function clientIp(headers) {
  const forwarded = headers['x-nf-client-connection-ip'] || headers['x-forwarded-for'] || '';
  return cleanSingleLine(String(forwarded).split(',')[0] || 'unknown');
}

function rateAllowed(ip) {
  const t = now();
  const existing = RATE_BUCKET.get(ip) || [];
  const fresh = existing.filter((stamp) => (t - stamp) < RATE_WINDOW_MS);

  if (fresh.length >= RATE_MAX_PER_WINDOW) {
    RATE_BUCKET.set(ip, fresh);
    return false;
  }

  fresh.push(t);
  RATE_BUCKET.set(ip, fresh);

  for (const [key, stamps] of RATE_BUCKET.entries()) {
    if (!stamps.length || (t - stamps[stamps.length - 1]) > RATE_WINDOW_MS) {
      RATE_BUCKET.delete(key);
    }
  }

  return true;
}

function parseJson(body) {
  if (!body || Buffer.byteLength(body, 'utf8') > MAX_BODY_BYTES) {
    return null;
  }

  try {
    return JSON.parse(body);
  } catch (err) {
    return null;
  }
}

function normalizeFields(rawFields) {
  if (!Array.isArray(rawFields) || rawFields.length === 0 || rawFields.length > MAX_FIELDS) {
    return null;
  }

  let totalLinks = 0;
  const fields = [];

  for (const item of rawFields) {
    const name = cleanSingleLine(item && item.name);
    const label = cleanSingleLine(item && item.label);
    const value = clean(item && item.value);

    if (!name || !label || !value) {
      continue;
    }

    if (value.length > MAX_FIELD_VALUE || containsSuspiciousContent(value)) {
      return null;
    }

    totalLinks += urlCount(value);
    fields.push({ name, label, value });
  }

  if (!fields.length || totalLinks > MAX_LINKS) {
    return null;
  }

  return fields;
}

function originAllowed(headers) {
  const configured = clean(process.env.ALLOWED_ORIGINS);
  if (!configured) {
    return true;
  }

  const allowSet = new Set(
    configured.split(',').map((s) => clean(s)).filter(Boolean)
  );

  const origin = clean(headers.origin || headers.Origin);
  return !origin || allowSet.has(origin);
}

function emailText(payload, fields, ip) {
  const lines = [];
  lines.push('New website submission');
  lines.push('Form: ' + payload.formTitle);
  lines.push('Page: ' + payload.pageUrl);
  lines.push('IP: ' + ip);
  lines.push('Elapsed: ' + payload.elapsedMs + ' ms');
  lines.push('');
  lines.push('Details:');

  for (const field of fields) {
    lines.push('- ' + field.label + ': ' + field.value);
  }

  return lines.join('\n');
}

async function sendEmail(payload, fields, ip) {
  const apiKey = clean(process.env.RESEND_API_KEY);
  if (!apiKey) {
    throw new Error('Missing RESEND_API_KEY');
  }

  const to = clean(process.env.FORM_TO)
    ? clean(process.env.FORM_TO).split(',').map((s) => clean(s)).filter(Boolean)
    : DEFAULT_RECIPIENTS;

  const from = clean(process.env.FORM_FROM) || 'Bows for Battle Forms <forms@bowsforbattle.org>';
  const replyTo = clean(process.env.FORM_REPLY_TO) || 'jessehall@bowsforbattle.org';
  const subject = 'Bows for Battle - ' + payload.formTitle;

  const response = await fetch(RESEND_ENDPOINT, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from,
      to,
      reply_to: replyTo,
      subject,
      text: emailText(payload, fields, ip)
    })
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error('Resend error: ' + message);
  }
}

exports.handler = async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return json(405, { ok: false, error: 'Method not allowed' });
  }

  const headers = event.headers || {};
  if (!originAllowed(headers)) {
    return json(403, { ok: false, error: 'Origin not allowed' });
  }

  const contentType = clean(headers['content-type'] || headers['Content-Type']).toLowerCase();
  if (!contentType.includes('application/json')) {
    return json(415, { ok: false, error: 'Unsupported content type' });
  }

  const payload = parseJson(event.body);
  if (!payload) {
    return json(400, { ok: false, error: 'Invalid payload' });
  }

  const formTitle = cleanSingleLine(payload.formTitle || 'Website Form');
  const pageUrl = clean(payload.pageUrl || '');
  const elapsedMs = Number(payload.elapsedMs || 0);
  const honeypot = clean(payload.honeypot || '');

  if (!ALLOWED_FORMS.has(formTitle)) {
    return json(400, { ok: false, error: 'Invalid form type' });
  }

  if (!pageUrl || pageUrl.length > 500 || containsSuspiciousContent(pageUrl)) {
    return json(400, { ok: false, error: 'Invalid page URL' });
  }

  if (honeypot) {
    return json(202, { ok: true });
  }

  if (!Number.isFinite(elapsedMs) || elapsedMs < MIN_ELAPSED_MS) {
    return json(429, { ok: false, error: 'Submission too fast' });
  }

  const ip = clientIp(headers);
  if (!rateAllowed(ip)) {
    return json(429, { ok: false, error: 'Rate limit exceeded' });
  }

  const fields = normalizeFields(payload.fields);
  if (!fields) {
    return json(400, { ok: false, error: 'Invalid fields' });
  }

  try {
    await sendEmail({ formTitle, pageUrl, elapsedMs }, fields, ip);
    return json(200, { ok: true });
  } catch (err) {
    return json(500, { ok: false, error: 'Unable to send message' });
  }
};
