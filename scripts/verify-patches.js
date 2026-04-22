#!/usr/bin/env node
/**
 * Postinstall script — verifies pnpm patches applied correctly.
 * Checks that @remotion/studio PlaybackRateSelector.js contains our custom speeds.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CUSTOM_SPEEDS = [1.05, 1.1, 1.12, 1.15, 1.25];

function findPlaybackRateSelector() {
  const pnpmDir = path.join(__dirname, '..', 'node_modules', '.pnpm');
  if (!fs.existsSync(pnpmDir)) return null;

  const entries = fs.readdirSync(pnpmDir);
  // Prefer patched dirs (_pa_) over unpatched ones
  const studioDirs = entries
    .filter((e) => e.startsWith('@remotion+studio@') && !e.includes('server') && !e.includes('shared'))
    .sort((a, b) => {
      const aPatched = a.includes('_pa_') ? 0 : 1;
      const bPatched = b.includes('_pa_') ? 0 : 1;
      return aPatched - bPatched;
    });
  if (studioDirs.length === 0) return null;

  for (const studioDir of studioDirs) {
    const filePath = path.join(
      pnpmDir,
      studioDir,
      'node_modules',
      '@remotion',
      'studio',
      'dist',
      'components',
      'PlaybackRateSelector.js',
    );
    if (fs.existsSync(filePath)) return filePath;
  }
  return null;
}

function main() {
  const filePath = findPlaybackRateSelector();

  if (!filePath) {
    console.warn(
      '\x1b[33m⚠ [verify-patches] Could not find @remotion/studio PlaybackRateSelector.js.\n' +
        '  The Remotion version may have changed. Run /patch-remotion-speeds to regenerate the patch.\x1b[0m',
    );
    return;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const missing = CUSTOM_SPEEDS.filter(
    (speed) => !content.includes(String(speed)),
  );

  if (missing.length > 0) {
    console.warn(
      `\x1b[33m⚠ [verify-patches] Custom playback speeds missing from Studio: ${missing.join(', ')}\n` +
        `  The patch may not have applied. Run: pnpm install\n` +
        `  If the Remotion version changed, run /patch-remotion-speeds to regenerate.\x1b[0m`,
    );
  } else {
    console.log(
      '\x1b[32m✓ [verify-patches] Custom playback speeds (1.05x–1.25x) applied to Remotion Studio.\x1b[0m',
    );
  }
}

main();
