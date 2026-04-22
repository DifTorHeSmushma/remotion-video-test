---
name: browser-screencast
description: Capture a manual browser flow and replay it as a smooth automated screencast with visible cursor, click ripples, and smooth scrolling. Use when the user wants to record a browser walkthrough for a video tutorial, demo a logged-in product flow, generate b-roll for Remotion, or produce frame-accurate timestamps for TTS narration sync. Two modes — "record" attaches to the user's existing Chrome (preserves real logins) to capture click/scroll/nav events, "replay" launches a dedicated persistent Chrome profile that re-executes the flow with a smoothly animated cursor and produces a WebM video plus Remotion-ready manifest. Triggers on "record this browser flow", "screencast a demo", "replay my browser actions", "make a tutorial video of this", "automate this walkthrough", "capture web app demo".
allowed-tools: Bash, Read, Write, Edit
---

# browser-screencast — Capture & Replay Browser Demos

## For Claude: Interactive Orchestration (DO THIS)

When the user asks anything like "screencast the [X] flow", "record my browser", "replay that flow", or "make a browser demo video", **DO NOT dump CLI commands for the user to run**. Instead, orchestrate the whole thing yourself by running the scripts via the Bash tool. The user should never need to paste commands manually.

**Interactive pattern:**

1. **If user wants to record**: Check which Chrome is on CDP 9222 (`curl http://localhost:9222/json/version` or just try `record.js start`). Run `node .claude/skills/browser-screencast/bin/record.js start` for them. Tell them you've started recording; they perform their demo in their own Chrome. When they say "stop"/"done"/"dump", run `record.js dump --out flows/<name>.json --name "..."`. Offer to clear the recording.

2. **If user wants to replay a flow**: Look in `flows/` for existing flow files. If there are multiple, ask which one. Check whether the dedicated profile (`~/.claude-screencast-profile/`) is likely logged in for that site — on first run for any new site, auto-run `--first-run` first (opens browser, user logs in, closes window). Then run the actual replay with `--annotate` unless user says otherwise. Show them the output paths when done.

3. **If user wants to capture + replay in one go**: Chain both — start recording, wait for "stop", dump to flow, replay with annotate.

4. **Always run commands via the Bash tool yourself** using this form (works in any shell, since Bash tool uses git-bash, not PowerShell):
   ```
   "C:/nvm4w/nodejs/node.exe" .claude/skills/browser-screencast/bin/replay.js <flow.json> [flags]
   ```
   OR use `pnpm screencast <flow.json> [flags]` if the project has the pnpm script (this repo does).

5. **For blocking operations like `--first-run`** (waits for user to close browser window), use `run_in_background: true` on the Bash tool call, then tell the user "the window is open — log in then close it, I'll continue once you do." You'll get a notification when the process exits.

6. **Known: the user's shell is PowerShell on Windows**. If they ever ask for a manual command, give them a PowerShell-friendly form: `pnpm screencast flows\xyz.json --annotate` — no explicit node path needed.

---

## Mode overview

A two-mode skill for producing high-quality automated browser screencasts that can be ingested by Remotion compositions.

| Mode | Tool | Purpose |
|---|---|---|
| **record** | Attaches to user's running Chrome via CDP | Capture clicks, scrolls, and navigations from a real logged-in session |
| **replay** | Launches dedicated Playwright Chrome with persistent profile | Re-run captured flow with visible cursor, click ripples, smooth scroll, native WebM recording |

## When to use

- User wants a polished tutorial/demo video of a web app
- Recording behind logins (Stripe, Linear, GitHub, Circle, Notion, etc.)
- Generating b-roll clips for a Remotion composition (TTS-synced)
- Producing a frame-accurate manifest for narration alignment

## Prerequisites

- Chrome must be running with `--remote-debugging-port=9222` for record mode
  - Start with: `chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/path/to/your/profile"` OR shortcut with that flag added
- Playwright installed: `pnpm add -D playwright` (one-time)
- `ffmpeg` on PATH for the optional annotated review MP4

## Mode 1 — record

Captures the user's actions in their existing Chrome. Uses their real session, no profile copying.

```bash
# 1. Start the recorder (injects into currently-open page)
node .claude/skills/browser-screencast/bin/record.js start

# 2. User performs the demo manually in Chrome
#    Recorder logs clicks, inputs, scrolls, and pushState navigations to localStorage
#    Survives SPA navigation; survives full reload too (re-run "start" after a reload)

# 3. Dump the recording into a clean flow.json
node .claude/skills/browser-screencast/bin/record.js dump --out flows/dynamous-events.json

# 4. (Optional) Clear the in-page recording for a fresh capture
node .claude/skills/browser-screencast/bin/record.js clear
```

Options:
- `--cdp-port 9222` — alternate CDP port (default 9222)
- `--out path` — output path for `dump` (default `flow.json`)
- `--name "Friendly name"` — embedded in the manifest

The cleaned `flow.json` looks like:

```json
{
  "name": "Dynamous events demo",
  "site": "https://community.dynamous.ai",
  "viewport": { "width": 1920, "height": 1080 },
  "actions": [
    { "type": "navigate", "url": "https://community.dynamous.ai/feed", "label": "Start on Feed" },
    { "type": "click", "selectors": ["a[href='/courses']", "text=Courses"], "fallbackUrl": "/courses", "label": "Open Courses tab" },
    { "type": "scroll", "to": 600, "smooth": true, "label": "Scroll down to lessons" }
  ]
}
```

Edit `flow.json` to add `scroll`, `wait`, or refine labels — replay reads it as the source of truth.

## Mode 2 — replay

Launches a fresh Chrome with a dedicated persistent profile and replays the flow with full visible interactions.

```bash
# First run: empty profile — log in to the sites the flow needs, then close the window. Sessions persist.
node .claude/skills/browser-screencast/bin/replay.js flows/dynamous-events.json

# Subsequent runs: profile reused, no login needed
node .claude/skills/browser-screencast/bin/replay.js flows/dynamous-events.json --out out/screencasts/dynamous
```

Options:
- `--profile <path>` — dedicated profile dir (default `~/.claude-screencast-profile/`)
- `--out <dir>` — output directory (default `out/screencasts/<flow-name>-<timestamp>/`)
- `--viewport 1920x1080` — recording resolution (default 1920×1080)
- `--cursor-speed 800` — ms per cursor move (default 800)
- `--scroll-speed 1200` — ms per smooth scroll (default 1200)
- `--first-run` — open the dedicated profile, wait for the user to log in + close window
- `--annotate` — also generate `replay-annotated.mp4` with burned-in step labels and timestamp

Output:
- `<sha>.webm` — native Playwright recording
- `manifest.json` — frame-accurate timestamps per action (for Remotion + TTS sync)
- `screenshots/step-NN-*.png` — before/after PNG per action (optional Remotion stills)
- `replay-annotated.mp4` (with `--annotate`) — review-friendly MP4 with burned-in labels

## Action types (flow.json)

| Type | Required fields | Optional fields | Behavior |
|---|---|---|---|
| `navigate` | `url` | — | `page.goto(url, networkidle)`. Cursor restored at last known position. |
| `click` | `selectors[]` | `fallbackUrl`, `postWaitMs` | Resolve element → smooth-move cursor → ripple → click. Falls back to nav if no selector matches. |
| `hover` | `selectors[]` | `holdMs` | Smooth-move cursor over element, hold for `holdMs`. |
| `type` | `selectors[]`, `value` | `delayPerChar` (default 80) | Click input, then type char-by-char with realistic delay. |
| `focus` | `selectors[]` | — | Programmatic `focus()` (no cursor animation). |
| `scroll` | `to` (px from top) | `durationMs`, `smooth` | Smooth `scrollTo(y)` with eased animation. |
| `wait` | one of `ms`, `forSelector`, `forUrl` | `timeout` | Pause for time, or until selector/URL appears. |

## Manifest schema (consumed by Remotion compositions)

```json
{
  "fps": 30,
  "totalDurationMs": 21129,
  "totalFrames": 634,
  "video": "replay.webm",
  "viewport": { "width": 1920, "height": 1080 },
  "steps": [
    {
      "id": "courses",
      "label": "Open Courses tab",
      "narrationHint": "First, open the Courses tab.",
      "type": "click",
      "tStartMs": 825,
      "tEndMs": 4370,
      "frameStart": 25,
      "frameEnd": 131,
      "cursorX": 932, "cursorY": 64,
      "screenshotBefore": "screenshots/step-01-before.png",
      "screenshotAfter": "screenshots/step-01-after.png"
    }
  ]
}
```

Pair `frameStart` with TTS audio sequences in Remotion via `<Sequence from={step.frameStart}>` for tight narration sync.

## Common workflows

### "Record a Linear ticket workflow for a tutorial video"
1. Open Linear in your real Chrome (already logged in).
2. `node .claude/skills/browser-screencast/bin/record.js start`
3. Perform the workflow manually.
4. `node .claude/skills/browser-screencast/bin/record.js dump --out flows/linear-ticket.json --name "Create + assign Linear ticket"`
5. (One-time) Open the Playwright profile and log into Linear: `node .claude/skills/browser-screencast/bin/replay.js flows/linear-ticket.json --first-run`
6. `node .claude/skills/browser-screencast/bin/replay.js flows/linear-ticket.json` — produces the WebM + manifest
7. Drop into a Remotion scene with `<OffthreadVideo src={staticFile('screencasts/linear-ticket/replay.webm')} />` and align narration to `manifest.json` frame timings.

### "Add a smooth scroll demo to an existing flow"
Edit `flow.json` and insert:
```json
{ "type": "scroll", "to": 800, "smooth": true, "durationMs": 1200, "label": "Scroll to comments section" },
{ "type": "wait", "ms": 800 },
{ "type": "scroll", "to": 0, "smooth": true, "durationMs": 1200, "label": "Scroll back to top" }
```
Re-run replay.

## Troubleshooting

- **"Cannot connect to Chrome on port 9222"** — start Chrome with `--remote-debugging-port=9222`. Verify with `curl http://localhost:9222/json/version`.
- **First replay run lands on a login page** — log in within the Playwright window, then close it. Re-run replay.
- **Cursor not visible in WebM** — verify cursor inject script ran; check `console` logs in the headed window.
- **Selector not found at replay time** — the page changed since record. Edit `flow.json` and add a `fallbackUrl` or a `text=...` selector.
