#!/usr/bin/env node
// browser-screencast: record mode
// Attaches to user's existing Chrome (--remote-debugging-port=9222 by default),
// injects the recorder JS, exposes dump/clear subcommands.
//
// Usage:
//   node record.js start [--cdp-port 9222]
//   node record.js dump  [--cdp-port 9222] [--out flow.json] [--name "..."] [--raw raw.json]
//   node record.js clear [--cdp-port 9222]
//   node record.js status [--cdp-port 9222]

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { cleanFlow } = require('./lib/clean-flow');

const RECORDER_JS = fs.readFileSync(path.join(__dirname, 'lib', 'recorder-inject.js'), 'utf8');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) args[a.slice(2)] = argv[++i];
    else args._.push(a);
  }
  return args;
}

async function getActivePage(cdpPort) {
  const browser = await chromium.connectOverCDP(`http://localhost:${cdpPort}`);
  const ctxs = browser.contexts();
  if (!ctxs.length) throw new Error('No browser context found on CDP');
  // Prefer the most recently active page (last in pages list usually)
  const pages = ctxs.flatMap(c => c.pages()).filter(p => !p.isClosed());
  if (!pages.length) throw new Error('No open pages found');
  const page = pages[pages.length - 1];
  return { browser, page };
}

async function cmdStart(args) {
  const cdpPort = args['cdp-port'] || 9222;
  const { browser, page } = await getActivePage(cdpPort);
  const result = await page.evaluate(RECORDER_JS);
  console.log(JSON.parse(result));
  console.log(`\nRecorder active on: ${page.url()}`);
  console.log('Perform your demo manually in Chrome.');
  console.log(`When done, run:  node "${__filename}" dump --out flow.json --name "<friendly name>"`);
  await browser.close();
}

async function cmdDump(args) {
  const cdpPort = args['cdp-port'] || 9222;
  const outPath = path.resolve(args.out || 'flow.json');
  const rawPath = args.raw ? path.resolve(args.raw) : null;

  const { browser, page } = await getActivePage(cdpPort);
  const raw = await page.evaluate(() => localStorage.getItem('__abRecording'));
  await browser.close();

  if (!raw) {
    console.error('No recording found in localStorage on this page.');
    process.exit(1);
  }
  const events = JSON.parse(raw);
  console.log(`Captured ${events.length} raw events.`);

  if (rawPath) {
    fs.mkdirSync(path.dirname(rawPath), { recursive: true });
    fs.writeFileSync(rawPath, JSON.stringify(events, null, 2));
    console.log(`Raw events: ${rawPath}`);
  }

  const flow = cleanFlow(events, { name: args.name });
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(flow, null, 2));
  console.log(`Clean flow: ${outPath}  (${flow.actions.length} actions)`);
}

async function cmdClear(args) {
  const cdpPort = args['cdp-port'] || 9222;
  const { browser, page } = await getActivePage(cdpPort);
  await page.evaluate(() => localStorage.removeItem('__abRecording'));
  await browser.close();
  console.log('Recording cleared.');
}

async function cmdStatus(args) {
  const cdpPort = args['cdp-port'] || 9222;
  const { browser, page } = await getActivePage(cdpPort);
  const result = await page.evaluate(() => {
    const raw = localStorage.getItem('__abRecording');
    const arr = raw ? JSON.parse(raw) : [];
    return JSON.stringify({
      installed: !!window.__abRecorderInstalled,
      events: arr.length,
      url: location.href,
    });
  });
  await browser.close();
  console.log(JSON.parse(result));
}

(async () => {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  try {
    if (cmd === 'start') await cmdStart(args);
    else if (cmd === 'dump') await cmdDump(args);
    else if (cmd === 'clear') await cmdClear(args);
    else if (cmd === 'status') await cmdStatus(args);
    else {
      console.error('Usage: record.js <start|dump|clear|status> [options]');
      process.exit(1);
    }
  } catch (err) {
    console.error('ERROR:', err.message);
    process.exit(1);
  }
})();
