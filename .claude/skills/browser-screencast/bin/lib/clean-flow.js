// Convert the raw recorder dump (localStorage __abRecording) into a clean, replayable flow.json.
// - Drops scroll(0,0) and duplicate consecutive events
// - Combines click + immediate pushState into a single click action with a fallback URL
// - Preserves explicit scrolls
// - Preserves form inputs

function cleanFlow(rawEvents, meta = {}) {
  const events = rawEvents.filter(e =>
    // Drop only window-level scrolls at (0,0); keep container scrolls at y=0 and non-zero scrolls
    !(e.type === 'scroll' && !e.container && (e.y || 0) === 0 && (e.x || 0) === 0)
  );

  const actions = [];

  // Establish start URL from the first 'start' event
  const startEvt = events.find(e => e.type === 'start');
  if (startEvt) {
    actions.push({
      type: 'navigate',
      url: startEvt.url,
      label: 'Start state',
    });
  }

  for (let i = 0; i < events.length; i++) {
    const e = events[i];
    if (e.type === 'click') {
      const next = events[i + 1];
      // Capture pushState that happens within 200ms of the click as the click's destination
      let fallbackUrl = e.href || null;
      if (next && next.type === 'navigate' && (next.t - e.t) < 250) {
        fallbackUrl = absUrl(next.to, e.url) || fallbackUrl;
        i++; // skip the navigate event we just absorbed
      }
      const text = (e.text || '').replace(/\s+/g, ' ').trim().slice(0, 60);
      const action = {
        type: 'click',
        selectors: [e.selector].filter(Boolean),
        label: text || 'Click',
      };
      if (text) action.selectors.push(`text=${text.split('\n')[0].slice(0, 40)}`);
      if (e.ariaLabel) action.selectors.push(`[aria-label="${e.ariaLabel}"]`);
      if (fallbackUrl) {
        action.selectors.push(`a[href="${relUrl(fallbackUrl, e.url) || fallbackUrl}"]`);
        action.fallbackUrl = fallbackUrl;
      }
      actions.push(action);
    } else if (e.type === 'input') {
      actions.push({ type: 'input', selectors: [e.selector], value: e.value, label: `Type "${e.value.slice(0, 40)}"` });
    } else if (e.type === 'change') {
      actions.push({ type: 'change', selectors: [e.selector], value: e.value, checked: e.checked, label: 'Change' });
    } else if (e.type === 'scroll') {
      const container = e.container || undefined;
      const label = `Scroll ${container ? 'container' : 'window'} to y=${e.y}`;
      const prev = actions[actions.length - 1];
      // Dedupe: if previous was a scroll on the same container, update its target instead of pushing a new one
      if (prev && prev.type === 'scroll' && prev.container === container) {
        prev.to = e.y;
        prev.label = label;
      } else {
        actions.push({ type: 'scroll', to: e.y, container, smooth: true, label });
      }
    } else if (e.type === 'navigate') {
      // Standalone navigations (not absorbed into a click)
      actions.push({ type: 'navigate', url: absUrl(e.to, e.url), label: 'Navigate' });
    }
    // 'start' / 'resume' already handled or ignored
  }

  return {
    name: meta.name || 'Untitled flow',
    capturedAt: new Date().toISOString(),
    site: meta.site || (startEvt ? new URL(startEvt.url).origin : null),
    viewport: meta.viewport || { width: 1920, height: 1080 },
    actions,
  };
}

function absUrl(maybeRel, base) {
  if (!maybeRel) return null;
  try { return new URL(maybeRel, base).toString(); } catch { return maybeRel; }
}

function relUrl(abs, base) {
  try {
    const u = new URL(abs);
    const b = new URL(base);
    if (u.origin === b.origin) return u.pathname + u.search + u.hash;
    return null;
  } catch { return null; }
}

module.exports = { cleanFlow };
