#!/usr/bin/env node
// browser-screencast: replay mode
// Launches a fresh Chrome with a dedicated persistent profile, replays a flow.json
// with smooth visible cursor + click ripples + smooth scroll, records native WebM,
// emits a Remotion-ready manifest.json with frame-accurate timestamps.

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');
const { chromium } = require('playwright');

const CURSOR_JS = fs.readFileSync(path.join(__dirname, 'lib', 'cursor-inject.js'), 'utf8');
const FFMPEG = process.env.FFMPEG_PATH || 'C:/Program Files/FFmpeg/bin/ffmpeg.exe';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--first-run' || a === '--annotate') args[a.slice(2)] = true;
    else if (a.startsWith('--')) args[a.slice(2)] = argv[++i];
    else args._.push(a);
  }
  return args;
}

function ts() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function isLoginUrl(url) {
  return /\/(login|sign[-_]?in|signin|auth|account\/login)(\b|\/)/i.test(url);
}

async function resolveTarget(page, action) {
  // Returns { locator, x, y } or null
  for (const selector of (action.selectors || [])) {
    try {
      const locator = page.locator(selector).first();
      await locator.scrollIntoViewIfNeeded({ timeout: 1500 }).catch(() => {});
      const box = await locator.boundingBox({ timeout: 2500 });
      if (!box) continue;
      const x = Math.round(box.x + box.width / 2);
      const y = Math.round(box.y + box.height / 2);
      return { locator, x, y, via: selector };
    } catch (err) { /* try next */ }
  }
  return null;
}

async function moveCursor(page, x, y, duration) {
  await page.evaluate(([x, y, d]) => window.__cursor.move(x, y, d), [x, y, duration]);
  await page.mouse.move(x, y, { steps: 12 });
}

async function tryClick(page, action, opts, lastCursor) {
  const target = await resolveTarget(page, action);
  if (target) {
    // Animate cursor from previous position to new target
    await moveCursor(page, target.x, target.y, opts.cursorSpeed);
    await sleep(80);
    // Pulse + ripple + click
    await page.evaluate(([x, y]) => {
      window.__cursor.pulse();
      window.__cursor.ripple(x, y);
    }, [target.x, target.y]);
    await sleep(80);
    await page.mouse.click(target.x, target.y);
    return { ok: true, x: target.x, y: target.y, via: target.via };
  }
  if (action.fallbackUrl) {
    console.log(`  selectors failed; nav fallback to ${action.fallbackUrl}`);
    await page.goto(action.fallbackUrl, { waitUntil: 'networkidle', timeout: 30000 });
    return { ok: true, via: 'fallbackUrl', x: lastCursor.x, y: lastCursor.y };
  }
  throw new Error('No selector matched and no fallbackUrl');
}

async function tryHover(page, action, opts) {
  const target = await resolveTarget(page, action);
  if (!target) throw new Error('Hover selector not found');
  await moveCursor(page, target.x, target.y, opts.cursorSpeed);
  if (action.holdMs) await sleep(action.holdMs);
  return { ok: true, x: target.x, y: target.y };
}

async function tryType(page, action, opts) {
  const target = await resolveTarget(page, action);
  if (!target) throw new Error('Type selector not found');
  await moveCursor(page, target.x, target.y, opts.cursorSpeed);
  await sleep(80);
  await page.evaluate(([x, y]) => {
    window.__cursor.pulse();
    window.__cursor.ripple(x, y);
  }, [target.x, target.y]);
  await target.locator.click();
  await page.keyboard.type(action.value || '', { delay: action.delayPerChar || 80 });
  return { ok: true, x: target.x, y: target.y };
}

async function tryFocus(page, action) {
  const target = await resolveTarget(page, action);
  if (!target) throw new Error('Focus selector not found');
  await target.locator.focus();
  return { ok: true, x: target.x, y: target.y };
}

async function doScroll(page, action, opts) {
  const dur = action.durationMs || opts.scrollSpeed;
  const target = action.to;
  if (action.container) {
    await page.evaluate(
      ([sel, y, d]) => window.__cursor.scrollElement(sel, y, d),
      [action.container, target, dur],
    );
  } else {
    await page.evaluate(([y, d]) => window.__cursor.scrollTo(y, d), [target, dur]);
  }
  await sleep(dur + 50);
  return { ok: true };
}

async function doWait(page, action) {
  if (action.forSelector) {
    await page.waitForSelector(action.forSelector, { timeout: action.timeout || 15000 });
  } else if (action.forUrl) {
    await page.waitForURL(action.forUrl, { timeout: action.timeout || 15000 });
  } else {
    await sleep(action.ms || 500);
  }
  return { ok: true };
}

async function annotate(outDir, manifest) {
  const videoPath = path.join(outDir, manifest.video);
  if (!fs.existsSync(videoPath)) {
    console.log('Cannot annotate: video not found');
    return;
  }
  const esc = (s) => s.replace(/\\/g, '\\\\').replace(/:/g, '\\:').replace(/'/g, "\\'").replace(/,/g, '\\,');
  const filters = [
    "drawtext=fontfile='C\\:/Windows/Fonts/consola.ttf':text='%{pts\\:hms}':x=24:y=24:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10",
  ];
  for (const step of manifest.steps) {
    if (step.error) continue;
    const start = (step.tStartMs || 0) / 1000;
    const end = (step.tEndMs || step.tStartMs + 100) / 1000;
    const stepLabel = `${String(step.index + 1).padStart(2, '0')}/${manifest.steps.length}  ${step.label || step.type}`;
    filters.push(
      `drawtext=fontfile='C\\:/Windows/Fonts/seguisb.ttf':` +
      `text='${esc(stepLabel)}':x=24:y=h-72:fontsize=26:fontcolor=white:` +
      `box=1:boxcolor=0x9333ea@0.78:boxborderw=12:` +
      `enable='between(t,${start.toFixed(3)},${end.toFixed(3)})'`
    );
  }
  const outMp4 = path.join(outDir, 'replay-annotated.mp4');
  const result = spawnSync(FFMPEG, [
    '-y', '-i', videoPath,
    '-vf', filters.join(','),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
    outMp4,
  ], { encoding: 'utf8' });
  if (result.status !== 0) {
    console.log('ffmpeg annotate failed:', result.stderr.slice(-500));
  } else {
    console.log(`Annotated: ${outMp4}`);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const flowPath = args._[0];
  if (!flowPath) {
    console.error('Usage: replay.js <flow.json> [--profile dir] [--out dir] [--viewport WxH]');
    console.error('  [--cursor-speed 800] [--scroll-speed 1200] [--first-run] [--annotate]');
    process.exit(1);
  }
  const flow = JSON.parse(fs.readFileSync(flowPath, 'utf8'));

  const profileDir = path.resolve(args.profile || path.join(os.homedir(), '.claude-screencast-profile'));
  fs.mkdirSync(profileDir, { recursive: true });

  const [w, h] = (args.viewport || `${flow.viewport?.width || 1920}x${flow.viewport?.height || 1080}`)
    .split('x').map(Number);

  const flowName = (flow.name || path.basename(flowPath, '.json'))
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const outDir = path.resolve(args.out || path.join('out', 'screencasts', `${flowName}-${ts()}`));
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(path.join(outDir, 'screenshots'), { recursive: true });

  const opts = {
    cursorSpeed: parseInt(args['cursor-speed'] || '800', 10),
    scrollSpeed: parseInt(args['scroll-speed'] || '1200', 10),
    settleMs: parseInt(args['settle-ms'] || '1500', 10),
  };

  console.log(`Profile:  ${profileDir}`);
  console.log(`Viewport: ${w}x${h}`);
  console.log(`Output:   ${outDir}`);
  console.log(`Actions:  ${flow.actions.length}`);

  const context = await chromium.launchPersistentContext(profileDir, {
    channel: 'chrome',
    headless: false,
    viewport: { width: w, height: h },
    deviceScaleFactor: 1,
    recordVideo: { dir: outDir, size: { width: w, height: h } },
    args: [`--window-size=${w + 16},${h + 96}`],
  });

  await context.addInitScript(CURSOR_JS);

  const page = context.pages()[0] || await context.newPage();

  if (args['first-run']) {
    console.log('\n*** FIRST-RUN MODE ***');
    console.log('Log into any sites this flow needs in the opened Chrome window.');
    console.log('When finished, close the Chrome window — sessions persist.\n');
    await context.waitForEvent('close', { timeout: 0 });
    return;
  }

  const startTime = Date.now();
  const steps = [];
  const FPS = 30;

  // Cursor position state — carries over between pages for continuity
  let lastCursor = { x: 80, y: 80 };
  let cursorRevealed = false;

  const waitCursor = () => page.waitForFunction(
    () => typeof window.__cursor === 'object' && window.__cursor.isReady && window.__cursor.isReady(),
    { timeout: 8000 }
  ).catch(() => { console.warn('  warn: cursor not ready in time'); });

  // Restore cursor on every page navigation (including those triggered by clicks)
  page.on('framenavigated', async (frame) => {
    if (frame !== page.mainFrame()) return;
    try {
      await waitCursor();
      // Place cursor immediately at last known position, then optionally fade in
      await page.evaluate(([x, y]) => window.__cursor.show(x, y), [lastCursor.x, lastCursor.y]);
      if (!cursorRevealed) {
        await page.evaluate(() => window.__cursor.fadeIn());
        cursorRevealed = true;
      } else {
        // Force visible immediately on subsequent pages
        await page.evaluate(() => window.__cursor.fadeIn());
      }
    } catch (e) { /* page may have closed */ }
  });

  for (let i = 0; i < flow.actions.length; i++) {
    const action = flow.actions[i];
    const tStart = Date.now() - startTime;

    let cursorPos = null;
    let beforeShot = null, afterShot = null;
    let error = null;

    try {
      if (action.type === 'navigate') {
        if (page.url() !== action.url) {
          // Use `load` not `networkidle` — SPAs with websockets (Circle, Discord, etc.)
          // never hit idle. Fall back to `domcontentloaded` + settle delay if `load` times out.
          try {
            await page.goto(action.url, { waitUntil: 'load', timeout: 15000 });
          } catch {
            await page.goto(action.url, { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
          }
          await sleep(opts.settleMs);
        }
        await waitCursor();
        if (isLoginUrl(page.url()) && !isLoginUrl(action.url)) {
          throw new Error(`Redirected to login (${page.url()}). Run with --first-run to log in.`);
        }
      } else {
        beforeShot = `screenshots/step-${String(i).padStart(2, '0')}-${action.type}-before.png`;
        await page.screenshot({ path: path.join(outDir, beforeShot) }).catch(() => { beforeShot = null; });

        let res;
        if (action.type === 'click')        res = await tryClick(page, action, opts, lastCursor);
        else if (action.type === 'hover')   res = await tryHover(page, action, opts);
        else if (action.type === 'type')    res = await tryType(page, action, opts);
        else if (action.type === 'focus')   res = await tryFocus(page, action);
        else if (action.type === 'scroll')  res = await doScroll(page, action, opts);
        else if (action.type === 'wait')    res = await doWait(page, action);
        else { console.log(`  skip unknown action: ${action.type}`); continue; }

        if (res.x != null && res.y != null) {
          cursorPos = { x: res.x, y: res.y };
          lastCursor = cursorPos;
        }

        // Wait for any navigation triggered by clicks — use `load`, not `networkidle`
        if (action.type === 'click') {
          await page.waitForLoadState('load', { timeout: 8000 }).catch(() => {});
          await sleep(opts.settleMs);
          await waitCursor();
          if (isLoginUrl(page.url())) {
            console.warn(`  warn: landed on a login page (${page.url()}). The flow may need --first-run.`);
          }
        }
        await sleep(action.postWaitMs || 500);
        afterShot = `screenshots/step-${String(i).padStart(2, '0')}-${action.type}-after.png`;
        await page.screenshot({ path: path.join(outDir, afterShot) }).catch(() => { afterShot = null; });
      }
    } catch (err) {
      error = err.message;
      console.error(`  [${i + 1}] FAILED: ${err.message}`);
      // Continue with remaining actions instead of crashing
    }

    const tEnd = Date.now() - startTime;
    steps.push({
      index: i,
      type: action.type,
      label: action.label || action.type,
      narrationHint: action.narrationHint || action.label || action.type,
      url: page.url(),
      tStartMs: tStart,
      tEndMs: tEnd,
      durationMs: tEnd - tStart,
      frameStart: Math.round(tStart / 1000 * FPS),
      frameEnd: Math.round(tEnd / 1000 * FPS),
      cursorX: cursorPos?.x ?? null,
      cursorY: cursorPos?.y ?? null,
      screenshotBefore: beforeShot,
      screenshotAfter: afterShot,
      error,
    });
    const status = error ? 'FAILED' : 'ok';
    console.log(`  [${i + 1}/${flow.actions.length}] ${action.type}: ${action.label || ''}  (${tEnd - tStart}ms) ${status}`);
  }

  // Park cursor offscreen for clean ending
  await page.evaluate(() => window.__cursor.move(-200, -200, 600)).catch(() => {});
  await sleep(800);

  const totalMs = Date.now() - startTime;
  const totalFrames = Math.round(totalMs / 1000 * FPS);

  await context.close();

  const videoFile = fs.readdirSync(outDir).find(f => f.endsWith('.webm'));

  const manifest = {
    name: flow.name,
    capturedAt: new Date().toISOString(),
    site: flow.site,
    fps: FPS,
    viewport: { width: w, height: h },
    totalDurationMs: totalMs,
    totalFrames,
    video: videoFile || null,
    steps,
  };
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
  console.log(`\nDone in ${totalMs}ms (${totalFrames} frames @ ${FPS}fps).`);
  console.log(`Manifest: ${path.join(outDir, 'manifest.json')}`);
  if (videoFile) console.log(`Video:    ${path.join(outDir, videoFile)}`);

  if (args.annotate && videoFile) {
    console.log('\nGenerating annotated MP4...');
    await annotate(outDir, manifest);
  }
}

main().catch(err => {
  console.error('FATAL:', err);
  process.exit(1);
});
