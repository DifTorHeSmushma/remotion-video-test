// Injected on every page during `replay`.
// Runs at document-start (via context.addInitScript), so DOM setup is deferred
// until DOMContentLoaded. The window.__cursor API is exposed immediately and
// queues calls until the cursor element is mounted.

(() => {
  if (window.__cursorInstalled) return;
  window.__cursorInstalled = true;

  const ID = '__ab_cursor';
  const RIPPLE_ID = '__ab_ripple_layer';
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  let resolveReady;
  const ready = new Promise((r) => { resolveReady = r; });

  let realApi = null;
  const callWhenReady = (name, args) => ready.then(() => realApi[name].apply(realApi, args));
  window.__cursor = {
    show:          (...a) => callWhenReady('show', a),
    move:          (...a) => callWhenReady('move', a),
    ripple:        (...a) => callWhenReady('ripple', a),
    pulse:         (...a) => callWhenReady('pulse', a),
    scrollTo:      (...a) => callWhenReady('scrollTo', a),
    scrollBy:      (...a) => callWhenReady('scrollBy', a),
    scrollElement: (...a) => callWhenReady('scrollElement', a),
    fadeIn:        (...a) => callWhenReady('fadeIn', a),
    fadeOut:       (...a) => callWhenReady('fadeOut', a),
    getPosition: () => realApi ? realApi.getPosition() : { x: -100, y: -100 },
    isReady:  () => !!realApi,
  };

  function install() {
    const css = document.createElement('style');
    css.textContent = `
      #${ID} {
        position: fixed; top: 0; left: 0; width: 40px; height: 40px;
        pointer-events: none; z-index: 2147483647;
        transform: translate3d(-200px, -200px, 0);
        opacity: 0;
        transition: transform 800ms cubic-bezier(.4, 0, .2, 1), opacity 300ms ease;
        filter: drop-shadow(0 6px 14px rgba(0,0,0,.55)) drop-shadow(0 2px 4px rgba(0,0,0,.45));
        will-change: transform, opacity;
      }
      #${ID} .__ab_cursor_glow {
        position: absolute; top: 0; left: 0; width: 40px; height: 40px;
        border-radius: 50%; background: radial-gradient(circle, rgba(99,102,241,.55) 0%, rgba(99,102,241,0) 65%);
        transform: scale(1); transform-origin: 30% 30%;
        transition: transform 200ms cubic-bezier(.2,.7,.3,1);
        pointer-events: none;
      }
      #${ID}.__ab_cursor_pulse .__ab_cursor_glow { transform: scale(1.7); }
      #${RIPPLE_ID} {
        position: fixed; top: 0; left: 0; pointer-events: none;
        z-index: 2147483646; width: 100%; height: 100%; overflow: hidden;
      }
      .__ab_ripple {
        position: absolute; width: 28px; height: 28px; margin: -14px 0 0 -14px;
        border-radius: 50%; border: 3px solid rgba(255,255,255,.95);
        box-shadow: 0 0 0 3px rgba(99,102,241,.7), 0 0 22px 8px rgba(99,102,241,.45);
        animation: __ab_ripple_anim 700ms cubic-bezier(.2,.7,.3,1) forwards;
      }
      @keyframes __ab_ripple_anim {
        0%   { transform: scale(.4); opacity: 1; }
        60%  { opacity: .8; }
        100% { transform: scale(4); opacity: 0; }
      }
    `;
    (document.head || document.documentElement).appendChild(css);

    const cursor = document.createElement('div');
    cursor.id = ID;
    cursor.innerHTML =
      '<div class="__ab_cursor_glow"></div>' +
      '<svg width="40" height="40" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" style="position:relative;display:block;">' +
        '<path d="M5 3 L5 24 L11 19 L14 26 L17.5 24.5 L14.5 17.5 L22 17 Z" ' +
              'fill="white" stroke="black" stroke-width="1.6" stroke-linejoin="round"/>' +
      '</svg>';
    document.documentElement.appendChild(cursor);

    const ripples = document.createElement('div');
    ripples.id = RIPPLE_ID;
    document.documentElement.appendChild(ripples);

    let curX = -200, curY = -200;
    let visible = false;

    realApi = {
      show(x, y) {
        curX = x; curY = y;
        cursor.style.transition = 'none';
        cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        // force reflow so subsequent transitions apply
        // eslint-disable-next-line no-unused-expressions
        cursor.offsetHeight;
        cursor.style.transition = 'transform 800ms cubic-bezier(.4, 0, .2, 1), opacity 300ms ease';
        return Promise.resolve();
      },
      async fadeIn() {
        cursor.style.opacity = '1';
        visible = true;
        await sleep(310);
      },
      async fadeOut() {
        cursor.style.opacity = '0';
        visible = false;
        await sleep(310);
      },
      async move(x, y, duration = 800) {
        if (!visible) {
          cursor.style.opacity = '1';
          visible = true;
        }
        cursor.style.transition = `transform ${duration}ms cubic-bezier(.4, 0, .2, 1), opacity 300ms ease`;
        cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        curX = x; curY = y;
        await sleep(duration + 30);
      },
      async pulse() {
        cursor.classList.add('__ab_cursor_pulse');
        await sleep(120);
        cursor.classList.remove('__ab_cursor_pulse');
        await sleep(100);
      },
      async ripple(x, y) {
        const r = document.createElement('div');
        r.className = '__ab_ripple';
        r.style.left = x + 'px';
        r.style.top = y + 'px';
        ripples.appendChild(r);
        setTimeout(() => r.remove(), 750);
      },
      async scrollTo(targetY, duration = 1200) {
        const startY = window.scrollY;
        const distance = targetY - startY;
        const startTime = performance.now();
        return new Promise((resolve) => {
          const ease = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
          const step = (now) => {
            const elapsed = now - startTime;
            const t = Math.min(elapsed / duration, 1);
            window.scrollTo(0, startY + distance * ease(t));
            if (t < 1) requestAnimationFrame(step);
            else resolve();
          };
          requestAnimationFrame(step);
        });
      },
      async scrollBy(deltaY, duration = 1200) {
        return this.scrollTo(window.scrollY + deltaY, duration);
      },
      async scrollElement(selector, targetY, duration = 1200) {
        const el = document.querySelector(selector);
        if (!el) {
          console.warn('[__cursor.scrollElement] selector not found:', selector);
          return this.scrollTo(targetY, duration);
        }
        const startY = el.scrollTop;
        const distance = targetY - startY;
        const startTime = performance.now();
        return new Promise((resolve) => {
          const ease = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
          const step = (now) => {
            const elapsed = now - startTime;
            const t = Math.min(elapsed / duration, 1);
            el.scrollTop = startY + distance * ease(t);
            if (t < 1) requestAnimationFrame(step);
            else resolve();
          };
          requestAnimationFrame(step);
        });
      },
      getPosition() { return { x: curX, y: curY }; },
    };

    resolveReady();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', install, { once: true });
  } else {
    install();
  }
})();
