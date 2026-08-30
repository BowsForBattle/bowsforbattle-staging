/* ============================================================
   Bows for Battle - secure form submission
   ------------------------------------------------------------
   Sends form data to a serverless endpoint that validates and
   emails submissions to the org inboxes.
   ============================================================ */
(function () {
  'use strict';

  var CFG = window.BFB_FORM_CONFIG || {};
  var MODE = String(CFG.mode || 'mailto').toLowerCase();
  if (MODE !== 'mailto' && MODE !== 'api') {
    MODE = 'mailto';
  }

  var TO = CFG.recipients || [
    'jessehall@bowsforbattle.org',
    'dustinlangsdorf@bowsforbattle.org'
  ];

  var ENDPOINT = CFG.endpoint || '/api/form-submit';
  var MIN_CLIENT_MS = 2500;
  var SUBMIT_COOLDOWN_MS = 20000;

  function clean(value) {
    return String(value === undefined || value === null ? '' : value).trim();
  }

  function now() {
    return Date.now();
  }

  function getFieldValue(field) {
    if (!field) { return ''; }
    if (field.tagName === 'SELECT') {
      var option = field.options[field.selectedIndex];
      return clean(option ? option.text : field.value);
    }
    return clean(field.value);
  }

  function getLabelText(form, field) {
    if (!field.id) { return clean(field.name || 'Field'); }
    var label = form.querySelector('label[for="' + field.id + '"]');
    if (!label) { return clean(field.name || field.id || 'Field'); }
    return clean(label.textContent.replace(/\s+/g, ' '));
  }

  function ensureStatusNode(form) {
    var status = form.querySelector('.form-status');
    if (status) { return status; }
    status = document.createElement('p');
    status.className = 'form-status';
    status.setAttribute('aria-live', 'polite');
    status.style.marginTop = '0.8rem';
    form.appendChild(status);
    return status;
  }

  function setStatus(form, message, ok) {
    var status = ensureStatusNode(form);
    status.textContent = message;
    status.style.color = ok ? '#1f6f43' : '#8e1f1f';
  }

  function toggleSubmit(form, disabled) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) { return; }
    if (!btn.hasAttribute('data-original-text')) {
      btn.setAttribute('data-original-text', btn.textContent || 'Submit');
    }
    btn.disabled = disabled;
    btn.textContent = disabled ? 'Sending...' : btn.getAttribute('data-original-text');
  }

  function ensureHoneypot(form) {
    var trap = form.querySelector('input[name="company_website"]');
    if (trap) { return; }
    trap = document.createElement('input');
    trap.type = 'text';
    trap.name = 'company_website';
    trap.tabIndex = -1;
    trap.autocomplete = 'off';
    trap.setAttribute('aria-hidden', 'true');
    trap.style.position = 'absolute';
    trap.style.left = '-10000px';
    trap.style.opacity = '0';
    form.appendChild(trap);
  }

  function fieldList(form) {
    var out = [];
    var fields = form.querySelectorAll('input, select, textarea');
    Array.prototype.forEach.call(fields, function (field) {
      if (!field.name) { return; }
      if (field.type === 'submit' || field.type === 'button' || field.type === 'hidden') { return; }
      if (field.name === 'company_website') { return; }

      var value = getFieldValue(field);
      if (!value) { return; }

      out.push({
        name: clean(field.name),
        label: getLabelText(form, field),
        value: value
      });
    });
    return out;
  }

  function payload(form) {
    var started = Number(form.getAttribute('data-started-at') || now());
    return {
      formTitle: clean(form.getAttribute('data-form-title') || form.getAttribute('aria-label') || 'Website Form'),
      pageUrl: window.location.href,
      elapsedMs: Math.max(0, now() - started),
      honeypot: clean((form.querySelector('input[name="company_website"]') || {}).value),
      fields: fieldList(form)
    };
  }

  function buildMailBody(data) {
    var lines = [];
    lines.push('New website submission');
    lines.push('Form: ' + data.formTitle);
    lines.push('Page: ' + data.pageUrl);
    lines.push('');
    lines.push('Details:');

    Array.prototype.forEach.call(data.fields || [], function (field) {
      lines.push('- ' + field.label + ': ' + field.value);
    });

    if (!data.fields || !data.fields.length) {
      lines.push('- No fields were completed.');
    }

    return lines.join('\n');
  }

  function mailtoUrl(data) {
    return 'mailto:' + TO.join(',') +
      '?subject=' + encodeURIComponent('Bows for Battle - ' + data.formTitle) +
      '&body=' + encodeURIComponent(buildMailBody(data));
  }

  function cooldownKey(form) {
    return 'bfb-form-last-submit:' + clean(form.getAttribute('data-form-title') || form.getAttribute('aria-label') || 'form');
  }

  function blockedByCooldown(form) {
    try {
      var raw = window.localStorage.getItem(cooldownKey(form));
      var prev = raw ? Number(raw) : 0;
      return prev > 0 && (now() - prev) < SUBMIT_COOLDOWN_MS;
    } catch (err) {
      return false;
    }
  }

  function markSubmitted(form) {
    try {
      window.localStorage.setItem(cooldownKey(form), String(now()));
    } catch (err) {
      /* no-op when storage is unavailable */
    }
  }

  async function submitApi(form, body) {
    try {
      var response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      markSubmitted(form);
      form.reset();
      form.setAttribute('data-started-at', String(now()));
      setStatus(form, 'Message sent successfully. Thank you.', true);
    } catch (err) {
      setStatus(form, 'Unable to send right now. Please email jessehall@bowsforbattle.org directly.', false);
    } finally {
      toggleSubmit(form, false);
    }
  }

  function submitMailto(form, body) {
    try {
      markSubmitted(form);
      form.reset();
      form.setAttribute('data-started-at', String(now()));
      setStatus(form, 'Opening your email app...', true);
      window.location.href = mailtoUrl(body);
    } catch (err) {
      setStatus(form, 'Could not open your email app. Please email jessehall@bowsforbattle.org directly.', false);
    } finally {
      toggleSubmit(form, false);
    }
  }

  async function submit(form) {
    var body = payload(form);

    if (body.honeypot) {
      setStatus(form, 'Message sent successfully. Thank you.', true);
      return;
    }

    if (body.elapsedMs < MIN_CLIENT_MS) {
      setStatus(form, 'Please wait a moment and try again.', false);
      return;
    }

    if (blockedByCooldown(form)) {
      setStatus(form, 'Please wait a few seconds before submitting again.', false);
      return;
    }

    toggleSubmit(form, true);
    if (MODE === 'api') {
      setStatus(form, 'Sending your message...', true);
      await submitApi(form, body);
      return;
    }

    setStatus(form, 'Preparing your email...', true);
    submitMailto(form, body);
  }

  function wire(form) {
    ensureHoneypot(form);
    form.setAttribute('data-started-at', String(now()));
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      submit(form);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var forms = document.querySelectorAll('form.email-form');
    Array.prototype.forEach.call(forms, wire);
  });
})();
