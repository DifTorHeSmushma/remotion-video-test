// Injected into the user's page during `record start`.
// Captures clicks, inputs, scrolls, and SPA navigation events into localStorage.
// Survives in-page navigation (pushState). Persists across full reloads via localStorage.
// Returns a status string when called via Playwright's evaluate().

(() => {
  if (window.__abRecorderInstalled) {
    const arr = JSON.parse(localStorage.getItem('__abRecording') || '[]');
    return JSON.stringify({ status: 'already-installed', count: arr.length });
  }
  window.__abRecorderInstalled = true;

  const KEY = '__abRecording';
  const start = Date.now();
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };
  const save = (a) => localStorage.setItem(KEY, JSON.stringify(a));

  if (load().length === 0) {
    save([{ type: 'start', url: location.href, t: 0, ts: new Date().toISOString() }]);
  } else {
    const a = load();
    a.push({ type: 'resume', url: location.href, t: Date.now() - start, ts: new Date().toISOString() });
    save(a);
  }

  const push = (e) => {
    const a = load();
    e.url = location.href;
    e.t = Date.now();
    a.push(e);
    save(a);
  };

  const sel = (el) => {
    if (!el || el.nodeType !== 1) return null;
    if (el.id) return '#' + CSS.escape(el.id);
    if (el.dataset && el.dataset.testid) return '[data-testid="' + el.dataset.testid + '"]';
    if (el.getAttribute && el.getAttribute('aria-label')) {
      return el.tagName.toLowerCase() + '[aria-label="' + el.getAttribute('aria-label').replace(/"/g, '\\"') + '"]';
    }
    const parts = [];
    let cur = el;
    let depth = 0;
    while (cur && cur.nodeType === 1 && cur !== document.body && depth < 5) {
      let part = cur.tagName.toLowerCase();
      if (cur.className && typeof cur.className === 'string') {
        const cls = cur.className.trim().split(/\s+/)
          .filter(c => c && !c.includes(':') && !c.startsWith('css-'))
          .slice(0, 2)
          .map(c => CSS.escape(c)).join('.');
        if (cls) part += '.' + cls;
      }
      const parent = cur.parentElement;
      if (parent) {
        const sibs = Array.from(parent.children).filter(s => s.tagName === cur.tagName);
        if (sibs.length > 1) part += ':nth-of-type(' + (sibs.indexOf(cur) + 1) + ')';
      }
      parts.unshift(part);
      cur = cur.parentElement;
      depth++;
    }
    return parts.join(' > ');
  };

  document.addEventListener('click', (e) => {
    const t = e.target.closest('a,button,[role="button"],input,select,textarea,[onclick],[tabindex]') || e.target;
    push({
      type: 'click',
      selector: sel(t),
      tag: t.tagName.toLowerCase(),
      text: ((t.innerText || t.textContent || '').trim().slice(0, 120)),
      href: t.href || null,
      ariaLabel: t.getAttribute && t.getAttribute('aria-label'),
      x: e.clientX,
      y: e.clientY,
    });
  }, true);

  let inputTimer;
  document.addEventListener('input', (e) => {
    clearTimeout(inputTimer);
    const t = e.target;
    if (!t || (t.tagName !== 'INPUT' && t.tagName !== 'TEXTAREA' && !t.isContentEditable)) return;
    inputTimer = setTimeout(() => {
      const isPwd = t.type === 'password';
      push({
        type: 'input',
        selector: sel(t),
        value: isPwd ? '<<password>>' : (t.value || t.textContent || '').slice(0, 200),
        inputType: t.type || 'contenteditable',
      });
    }, 400);
  }, true);

  document.addEventListener('change', (e) => {
    const t = e.target;
    if (t && (t.tagName === 'SELECT' || t.type === 'checkbox' || t.type === 'radio')) {
      push({ type: 'change', selector: sel(t), value: t.value, checked: t.checked });
    }
  }, true);

  // Capture scrolls on ANY element (SPAs typically scroll an inner container, not window).
  // Capture-phase listener on window catches scroll events before they reach target.
  let scrollTimer;
  let lastScrollKey = '';
  window.addEventListener('scroll', (e) => {
    clearTimeout(scrollTimer);
    const target = e.target;
    scrollTimer = setTimeout(() => {
      let y, container;
      if (!target || target === document || target === document.documentElement || target === document.body) {
        y = window.scrollY || document.documentElement.scrollTop || 0;
        container = null;
      } else if (typeof target.scrollTop === 'number') {
        y = target.scrollTop || 0;
        container = sel(target);
      } else {
        return;
      }
      const key = `${container || 'window'}@${Math.round(y / 10)}`;
      if (key === lastScrollKey) return; // dedupe identical
      lastScrollKey = key;
      push({ type: 'scroll', y: Math.round(y), container });
    }, 200);
  }, true);

  const wrap = (name) => {
    const orig = history[name];
    history[name] = function(...a) {
      const r = orig.apply(this, a);
      push({ type: 'navigate', method: name, to: a[2] || location.href });
      return r;
    };
  };
  wrap('pushState');
  wrap('replaceState');
  window.addEventListener('popstate', () => push({ type: 'navigate', method: 'popstate', to: location.href }));

  return JSON.stringify({ status: 'installed', startUrl: location.href, count: load().length });
})();
