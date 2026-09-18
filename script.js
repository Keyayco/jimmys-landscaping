/* =========================================================
   Jimmy's Landscaping (Pty) LTD — script.js
   Plain JavaScript, no libraries.
   ========================================================= */

/* ---------------------------------------------------------
   CONFIG — the only part you normally need to edit.
   --------------------------------------------------------- */
var CONFIG = {
  // Business phone in international format, digits only (no +, no spaces).
  phone: '27670033499',

  // Where the enquiry form posts to. Leave as '' until a backend exists.
  // With '' the form opens WhatsApp with the enquiry filled in, so no lead is lost.
  // Examples: 'https://formspree.io/f/xxxxxxx'  or  '/api/enquiry'
  formEndpoint: ''
};

document.documentElement.classList.add('js');

/* ---------------------------------------------------------
   Mobile menu
   --------------------------------------------------------- */
(function () {
  var toggle = document.getElementById('menuToggle');
  var nav = document.getElementById('mobileNav');
  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  // close after tapping a link
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') setOpen(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setOpen(false);
  });
})();

/* ---------------------------------------------------------
   Header shadow once the page scrolls
   --------------------------------------------------------- */
(function () {
  var header = document.getElementById('header');
  if (!header) return;
  var ticking = false;

  function update() {
    header.classList.toggle('is-stuck', window.scrollY > 10);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
  }, { passive: true });
  update();
})();

/* ---------------------------------------------------------
   Section reveals on scroll
   --------------------------------------------------------- */
(function () {
  var items = document.querySelectorAll('.reveal');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry, i) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      // small stagger so groups of cards do not all pop at once
      el.style.transitionDelay = Math.min(i * 70, 210) + 'ms';
      el.classList.add('is-visible');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  items.forEach(function (el) { io.observe(el); });
})();

/* ---------------------------------------------------------
   Current section highlight in the desktop nav
   --------------------------------------------------------- */
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-desktop a'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);
  if (!sections.length || !('IntersectionObserver' in window)) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      links.forEach(function (a) {
        a.classList.toggle('is-current', a.getAttribute('href') === '#' + entry.target.id);
      });
    });
  }, { rootMargin: '-45% 0px -50% 0px' });

  sections.forEach(function (s) { io.observe(s); });
})();

/* ---------------------------------------------------------
   Gallery filters
   --------------------------------------------------------- */
(function () {
  var buttons = document.querySelectorAll('.filter');
  var tiles = document.querySelectorAll('#gallery .tile');
  if (!buttons.length) return;

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cat = btn.getAttribute('data-filter');

      buttons.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', String(on));
      });

      tiles.forEach(function (tile) {
        var show = cat === 'all' || tile.getAttribute('data-cat') === cat;
        tile.classList.toggle('is-hidden', !show);
      });
    });
  });
})();

/* ---------------------------------------------------------
   Enquiry form
   Validates, then either posts to CONFIG.formEndpoint or,
   if none is set, hands the enquiry to WhatsApp.
   --------------------------------------------------------- */
(function () {
  var form = document.getElementById('enquiryForm');
  var status = document.getElementById('formStatus');
  if (!form) return;

  function fieldOf(input) { return input.closest('.field'); }

  function showError(input, msg) {
    var field = fieldOf(input);
    field.classList.add('has-error');
    var slot = field.querySelector('.error');
    if (slot) slot.textContent = msg;
  }

  function clearError(input) {
    var field = fieldOf(input);
    field.classList.remove('has-error');
    var slot = field.querySelector('.error');
    if (slot) slot.textContent = '';
  }

  function validate() {
    var ok = true;
    var name = form.elements['name'];
    var phone = form.elements['phone'];
    var service = form.elements['service'];

    [name, phone, service].forEach(clearError);

    if (!name.value.trim()) { showError(name, 'Please enter your name.'); ok = false; }

    var digits = phone.value.replace(/\D/g, '');
    if (digits.length < 9) { showError(phone, 'Please enter a contact number we can reach you on.'); ok = false; }

    if (!service.value) { showError(service, 'Please choose a service.'); ok = false; }

    return ok;
  }

  // clear the error as soon as the person fixes the field
  form.addEventListener('input', function (e) {
    if (e.target.closest('.field')) clearError(e.target);
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status';
    status.textContent = '';

    if (!validate()) {
      status.className = 'form-status is-bad';
      status.textContent = 'Please check the highlighted fields.';
      var bad = form.querySelector('.has-error input, .has-error select');
      if (bad) bad.focus();
      return;
    }

    var data = {
      name: form.elements['name'].value.trim(),
      phone: form.elements['phone'].value.trim(),
      service: form.elements['service'].value,
      message: form.elements['message'].value.trim()
    };

    // No backend yet: send it through WhatsApp instead of losing the enquiry.
    if (!CONFIG.formEndpoint) {
      var text =
        'Landscaping enquiry\n' +
        'Name: ' + data.name + '\n' +
        'Phone: ' + data.phone + '\n' +
        'Service: ' + data.service +
        (data.message ? '\nDetails: ' + data.message : '');

      window.open('https://wa.me/' + CONFIG.phone + '?text=' + encodeURIComponent(text), '_blank');

      status.className = 'form-status is-ok';
      status.textContent = 'Opening WhatsApp with your enquiry. If nothing opens, phone 067 003 3499.';
      form.reset();
      return;
    }

    // Backend connected.
    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    status.textContent = 'Sending your enquiry…';

    fetch(CONFIG.formEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed');
        status.className = 'form-status is-ok';
        status.textContent = 'Thank you. Your enquiry has been sent and we will be in touch.';
        form.reset();
      })
      .catch(function () {
        status.className = 'form-status is-bad';
        status.textContent = 'That did not send. Please phone 067 003 3499 or use the WhatsApp button.';
      })
      .then(function () { button.disabled = false; });
  });
})();

/* ---------------------------------------------------------
   Footer year
   --------------------------------------------------------- */
(function () {
  var el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();
