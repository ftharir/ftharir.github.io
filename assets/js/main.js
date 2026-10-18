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
})();
