// Small progressive-enhancement script: the site works without it.
(function () {
  // reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }
  // safety net: never leave content hidden
  setTimeout(function () { items.forEach(function (el) { el.classList.add('in'); }); }, 1500);

  // project filter
  var buttons = document.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('[data-areas]');
  function apply(area) {
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.filter === area)); });
    cards.forEach(function (c) {
      var show = area === 'all' || c.dataset.areas.split(' ').indexOf(area) !== -1;
      c.hidden = !show;
    });
    var live = document.getElementById('filter-live');
    if (live) {
      var n = Array.prototype.filter.call(cards, function (c) { return !c.hidden; }).length;
      live.textContent = n + (n === 1 ? ' project' : ' projects');
    }
  }
  if (buttons.length) {
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        apply(b.dataset.filter);
        history.replaceState(null, '', b.dataset.filter === 'all' ? location.pathname : '#' + b.dataset.filter);
      });
    });
    var start = location.hash.replace('#', '');
    apply(start && document.querySelector('[data-filter="' + start + '"]') ? start : 'all');
  }

  // copy e-mail
  document.querySelectorAll('[data-copy]').forEach(function (el) {
    el.addEventListener('click', function () {
      var text = el.dataset.copy;
      var done = function () {
        var old = el.innerHTML;
        el.textContent = 'Copied';
        setTimeout(function () { el.innerHTML = old; }, 1400);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done); } else { done(); }
    });
  });

  // contact form: posts to the form service; without an endpoint it opens the visitor's e-mail app
  var form = document.getElementById('contact-form');
  if (form) {
    var status = document.getElementById('form-status');
    var say = function (text, kind) { status.textContent = text; status.className = 'form-status ' + (kind || ''); };
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements;
      if (f._gotcha.value) { return; }                        // spam trap
      var ok = true;
      ['name', 'email', 'message'].forEach(function (n) {
        var bad = !f[n].value.trim() || (n === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f[n].value.trim()));
        f[n].setAttribute('aria-invalid', String(bad));
        if (bad) { ok = false; }
      });
      if (!ok) { say('Please fill in your name, a valid email and a message.', 'err'); return; }
      var data = { name: f.name.value.trim(), email: f.email.value.trim(), message: f.message.value.trim() };
      var endpoint = form.dataset.endpoint;
      if (!endpoint) {
        var body = data.message + '\n\n— ' + data.name + ' (' + data.email + ')';
        location.href = 'mailto:' + form.dataset.mailto + '?subject=' + encodeURIComponent('Message from ' + data.name) + '&body=' + encodeURIComponent(body);
        say('Your email app should open with the message ready to send.', 'ok');
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; say('Sending…');
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) { throw new Error(r.status); } form.reset(); say('Thank you! Your message was sent.', 'ok'); })
        .catch(function () { say('Sorry, sending failed. Please email me directly.', 'err'); })
        .then(function () { btn.disabled = false; });
    });
  }

  // pointer effects: soft glow that follows the cursor, a spotlight inside cards, a gentle tilt of the portrait.
  // Only for devices with a real pointer, and never when the visitor asks for reduced motion.
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (fine && !calm) {
    var root = document.documentElement, tx = 0, ty = 0, gx = 0, gy = 0, raf = 0;
    var follow = function () {
      gx += (tx - gx) * 0.16; gy += (ty - gy) * 0.16;
      root.style.setProperty('--mx', gx.toFixed(1) + 'px');
      root.style.setProperty('--my', gy.toFixed(1) + 'px');
      raf = (Math.abs(tx - gx) > 0.4 || Math.abs(ty - gy) > 0.4) ? requestAnimationFrame(follow) : 0;
    };
    var arch = document.querySelector('.arch');
    window.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!raf) { raf = requestAnimationFrame(follow); }
      root.classList.add('pointer');
      var host = e.target.closest && e.target.closest('.card, .t-item, .decide, .step, .box, .stat, .fact, .tile');
      if (host) {
        var r = host.getBoundingClientRect();
        host.style.setProperty('--cx', (e.clientX - r.left).toFixed(0) + 'px');
        host.style.setProperty('--cy', (e.clientY - r.top).toFixed(0) + 'px');
      }
      if (arch) {
        var nx = e.clientX / window.innerWidth - 0.5, ny = e.clientY / window.innerHeight - 0.5;
        arch.style.setProperty('--rx', (-ny * 7).toFixed(2) + 'deg');
        arch.style.setProperty('--ry', (nx * 9).toFixed(2) + 'deg');
        arch.style.setProperty('--tx', (nx * 12).toFixed(1) + 'px');
        arch.style.setProperty('--ty', (ny * 10).toFixed(1) + 'px');
      }
    }, { passive: true });
  }
})();
