---
description: "Google ecosystem Short — scaffold a 90-120s vertical Short using the GoogleShortShell design system (Search / Chrome / Gemini / Android / Pixel / Workspace)"
argument-hint: "<topic or URL, e.g. 'AI Mode in Chrome' or 'https://blog.google/products/search/ai-mode-chrome/'>"
---

# /diy-yt-creation:google-short — Google Ecosystem Short

<objective>
Create a standalone 90-120s YouTube Short (1080x1920, 30fps) for **any Google product** — Search, Chrome, Gemini, Android, Pixel, Workspace, YouTube, Maps, Cloud, etc. — using the reusable components in `src/shared/templates/google-short/`.

This command is SPECIFIC to Google-ecosystem topics. For Anthropic/Claude use `/diy-yt-creation:anthropic-short`. For a generic Short use `/diy-yt-creation:shorts-full-auto`.

**Goal**: Go from topic to render-ready composition autonomously, STOP before render, then on user approval render at 1.0x + post-process to 1.05x.
</objective>

<when-to-use>
Use this command when the user asks for a Short about:
- A Google Search feature (AI Mode, SGE, Shopping, etc.)
- A Chrome update (new tabs, privacy controls, extensions API)
- A Gemini release or new capability
- An Android / Pixel launch or feature
- A Google Workspace update (Docs, Sheets, Meet, Calendar AI)
- A Google Cloud / Vertex AI announcement
- A YouTube product change

Do NOT use this for:
- Anthropic/Claude topics (use `/diy-yt-creation:anthropic-short`)
- Generic AI/coding topics (use `/diy-yt-creation:shorts-full-auto`)
- Long-form videos (use `/diy-yt-creation:full-auto`)
</when-to-use>

<initial-setup>

## Step 1: Parse topic + pick the top-banner logo + gather assets

Parse `$ARGUMENTS` to extract the topic. If the user gave a URL, fetch it to understand what's being launched/updated. Immediately **ASK the user** for:
1. **Top-banner logo** — which product wordmark goes on top? Options (any `BRAND_LOGOS` key):
   - `google` — general / Search / Workspace (default, 520px wordmark)
   - `gemini` — Gemini topics (520px wordmark)
   - `chrome` — Chrome topics (use `topLogoWidth: 200` — square icon)
   - `android` — Android topics (200px square icon)
   - `googleG` — multi-surface / Google-broad (180px square)
2. **Hero word** — the single word/phrase for the Phase 1 slam-in (e.g. `AI MODE`, `GEMINI 2`, `PIXEL 10`, `SEARCH`). `GoogleHeroSlide` auto-fits via `FitHeadline` so long un-wrappable tokens (e.g. `DESIGN.MD`, `ANTIGRAVITY`) shrink instead of overflowing — but prefer words ≤ 7 chars OR add a natural break (space, dash) to preserve the 220px max impact. See `agent-pitfalls.md` "Hero Word Slam-In Overflows".
3. **Overline phrase** — the line above the hero word. **NOT hardcoded to "Just Launched"** — pick what fits:
   - Launch: "Just Launched", "Rolling out now", "New today"
   - Update: "New in Chrome", "Gemini update", "Android 15"
   - Explainer: "Explained in 90s", "How Search works", "Under the hood"
   - Curiosity: "The Pixel stack", "Actually useful", "The quiet update"
4. **Product screenshot** (hero) — the main visual for the hook
5. **Feature assets** — per feature they want to spotlight, one screenshot OR short video (.mp4 or .webm)
6. **Full-video thumbnail** — the thumbnail of the long-form video this Short promotes (if any)
7. **Target URL** — where viewers should go (e.g. `google.com/search`, `chrome.com/ai-mode`)
8. **Accent rotation** — confirm defaults (blue primary, red/yellow/green secondaries rotating) OR override per slide

Derive composition name: PascalCase + `Short` suffix.
- "AI Mode in Chrome" → `AIModeChromeShort`
- "Gemini 2 launch" → `Gemini2LaunchShort`
- "Pixel 10 launch" → `Pixel10LaunchShort`
- "Google Workspace AI" → `WorkspaceAIShort`

## Step 1.5: Detect + offer embedded videos from the source (conditional)

**If — and only if — the source is a URL AND the page contains embedded demo videos**, list them and ASK the user via `AskUserQuestion` which to embed in the Short. Skip this step silently if the source has no videos.

How to detect:
1. Use `WebFetch` (or `agent-browser snapshot`) on the source URL.
2. Scan the page for:
   - YouTube embeds: `iframe src="*youtube.com/embed/*"` or `a href="*youtube.com/watch?v=*"`
   - Direct Google MP4s: `storage.googleapis.com/gweb-uniblog-publish-prod/original_videos/*.mp4`
   - `<video>` / `<source>` tags with any MP4 / WebM src
   - Vimeo / Wistia iframe embeds
3. For each hit, note the URL + a 1-line description of what the video appears to show (infer from surrounding heading / caption / alt text).

If no videos found → continue to Step 2 silently.

If videos found → present the list and ask which to embed (multi-select). For each selected video, also ask **clip length** (15 / 20 / 30 / 40 seconds, default 20 for feature demos, 40 for hero demos).

```
AskUserQuestion:
  - "The source article has <N> demo videos. Which should I embed?"
    (multiSelect) options:
      - "Video 1: <1-line description> (<URL>)"
      - "Video 2: <1-line description> (<URL>)"
      - "None — use static screenshots only"
```

**Download pipeline** (one-time, once user confirms selection):

```bash
# YouTube (trim to first N seconds)
yt-dlp "<URL>" --download-sections "*0-<N>" \
  -f "bv*[ext=mp4][height<=720]+ba[ext=m4a]/mp4" --merge-output-format mp4 \
  -o "public/video/<name>/<slug>-raw.%(ext)s"

# Direct MP4 (download entire file, trim later via ffmpeg -t)
curl -fsSL "<URL>" -o "public/video/<name>/<slug>-raw.mp4"

# Re-encode to h264 + mute + (optional) downscale + faststart.
# Trim to <N> seconds if source was a full clip (not pre-trimmed by yt-dlp).
ffmpeg -i public/video/<name>/<slug>-raw.mp4 \
  -t <N> -c:v libx264 -pix_fmt yuv420p -crf 22 -preset medium \
  -vf "scale=1280:-2" -an -movflags +faststart \
  public/video/<name>/<slug>.mp4 -y
rm public/video/<name>/<slug>-raw.mp4
```

Store as `public/video/<name>/<slug>.mp4` (kebab-case slug — e.g. `shopping-demo.mp4`, `hiking-demo.mp4`, `pixel-camera-demo.mp4`).

**Map videos to scenes**: When Scene 01 or Scene 02 narration describes the feature that matches a video, swap the `media.kind` from `'image'` to `'video'` in the scene's `GoogleFeatureSlide` props, OR (for Scene 01's custom Phase 3 flow panel) use `<OffthreadVideo>` wrapped in `<Sequence from={PHASE_START} layout="none">` per the OffthreadVideo phase-gating rule in `agent-pitfalls.md`. Landscape 16:9 videos render natively at width 920 (not `PORTRAIT_SCREENSHOT_MAX_WIDTH`) — 16:9 videos don't overflow the vertical safe zone because their scaled height is small.

Derive audio folder: kebab-case WITHOUT `Short`.
- `AIModeChromeShort` → `public/audio/ai-mode-chrome-short/`

## Step 2: Invoke youtube-shorts-hooks skill for hook design

**CRITICAL**: Before writing ANY script copy, run the hook-design skill to get proven scroll-stop patterns tuned for this channel's faceless-tech audience.

```
Use the `youtube-shorts-hooks` skill to design the opening 3-5 seconds of this Google-ecosystem Short. Topic: <extracted topic>. Hero word: <user's input>. Overline: <user's input>. The hook must fit the "<Overline>" + hero-word + product-screenshot pattern established in GoogleShortShell.
```

The skill will return a hook formula + opening line. Use it verbatim as the first sentence of Scene 01.

## Step 3: Research topic (Phase 0)

Run `/diy-yt-creation:phase0-research` with the topic to gather:
- Official launch/update facts (stats, quotes, partner names, dates)
- Access details (which plans, regions, rollout schedule, URLs)
- Real quotes from the launch blog (blog.google, developers.googleblog.com, etc.)
- Technical capabilities worth showing
- Verified primary-source links (always use WebSearch with current year — see CLAUDE.md)

Store at `src/<Name>/research/content-brief.md`.

</initial-setup>

<script-generation>

## Step 4: Write the TTS script

Create `src/<Name>/scripts/full-script.md` with TWO scenes:

**Scene 01 — Hook + Explainer + Proof (~45-55s at Shorts 1.13x)**
Structure (use research findings verbatim — no invented numbers):
- Hook (3-5s): "<Overline phrase>. <Hero word>." + 1-sentence value prop (e.g. "New in Chrome. AI Mode. One search box, real reasoning.")
- Explainer (12-18s): what it does in plain English, 2-3 concrete behaviors
- Outputs (5-8s): what users get — list 2-3 concrete artifacts/outcomes
- Proof (15-20s): named partners / stat / rollout region ("already rolling out in the US, with India and Brazil next")

**Scene 02 — Features + Access + CTA (~45-55s)**
Structure:
- Features (20-25s): 2-3 feature sub-phases (one per screenshot/video provided)
- Combined combo (8-10s): 2-card combo of lighter features (optional)
- Access (8-10s): plan tiers + rollout + "Powered by <current model / backend>"
- Full-video tease (optional): "Full breakdown on the channel"
- URL reveal (3-4s): "Find it at <URL>"
- CTA (3-4s): debate question ending

Apply TTS rules from `.claude/rules/scriptwriting.md`:
- Soften exact numbers ("around 20+" not "20.3")
- No hyphenated acronyms (AI not A-I)
- No hype words, no "here's the thing", no "under the hood"
- Final line is a debate CTA
- Never read exact version numbers aloud — show on screen only
- No `[PAUSE]` tags

Write the per-scene `.txt` files:
- `src/<Name>/scripts/scene-01-hook.txt`
- `src/<Name>/scripts/scene-02-access.txt`

</script-generation>

<audio-and-assets>

## Step 5: Generate TTS + copy assets

```bash
python text-to-speech.py -i src/<Name>/scripts/scene-01-hook.txt -o public/audio/<name>/ -s src/<Name>/scripts/ -n scene01 --shorts
python text-to-speech.py -i src/<Name>/scripts/scene-02-access.txt -o public/audio/<name>/ -s src/<Name>/scripts/ -n scene02 --shorts
```

Copy user-provided assets:
```bash
mkdir -p public/images/<name>/ public/video/<name>/
cp <user hero screenshot> public/images/<name>/hero.png
cp <feature 1 asset>      public/images/<name>/feature-1.png    # or .mp4 → video/<name>/
cp <feature 2 asset>      public/images/<name>/feature-2.png
cp <feature 3 asset>      public/video/<name>/feature-3.mp4     # example: demo video
cp <full-video thumb>     public/images/<name>/cta-thumb.png
```

</audio-and-assets>

<scaffold>

## Step 6: Scaffold composition from template

Create the following files under `src/<Name>/`.

### `constants/timing.ts`

```ts
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const AUDIO_OFFSET = 15;
export const SCENE02_AUDIO_OFFSET = 10;
export const TRANSITION_DURATION = 0;

const SCENE01_AUDIO_FRAMES = <ceil(scene01 duration * 30)>;
const SCENE02_AUDIO_FRAMES = <ceil(scene02 duration * 30)>;

// Split buffer — short between scenes, long at end of video.
// Prevents 2.5s of dead air between Scene 01's last word and Scene 02.
const SCENE01_BUFFER = 30;   // ~1s after S1 narration ends → S2 cuts in
const SCENE02_BUFFER = 75;   // 2.5s reading time at the end of the video for the CTA

export const SCENES = {
  scene01: { start: 0, duration: AUDIO_OFFSET + SCENE01_AUDIO_FRAMES + SCENE01_BUFFER },
  scene02: {
    start: AUDIO_OFFSET + SCENE01_AUDIO_FRAMES + SCENE01_BUFFER,
    duration: SCENE02_AUDIO_OFFSET + SCENE02_AUDIO_FRAMES + SCENE02_BUFFER,
  },
} as const;

export const TOTAL_FRAMES = SCENES.scene01.duration + SCENES.scene02.duration;

export const wordToFrame = (time: number, offset: number): number =>
  Math.round(time * FPS) + offset;
```

### `constants/colors.ts`, `constants/fonts.ts`, `constants/springs.ts`

Start from the channel baseline (dark navy `#0B1120` background, `FONTS.primary` = Inter, `FONTS.mono` = JetBrains Mono). The Google 4-color accents come from `GOOGLE_ACCENTS` — don't duplicate them into `COLORS`, import directly:

```ts
import { GOOGLE_ACCENTS } from '../../shared/templates/google-short';
// use GOOGLE_ACCENTS.blue / .red / .yellow / .green
```

### `Composition.tsx`

Wrap everything in `<GoogleShortShell>` and place two scene Sequences plus audio + SFX overlays:

```tsx
import { GoogleShortShell } from '../shared/templates/google-short';
import { TOTAL_FRAMES, SCENES, AUDIO_OFFSET, SCENE02_AUDIO_OFFSET } from './constants/timing';
import { COLORS } from './constants/colors';

export const <Name>Composition: React.FC = () => (
  <GoogleShortShell
    totalFrames={TOTAL_FRAMES}
    backgroundColor={COLORS.background}
    topLogoKey="chrome"        // ← pick per Short: google / gemini / chrome / android / googleG
    topLogoWidth={200}         // ← adjust per logo aspect ratio (wordmarks 520, icons 180-200)
    seedPrefix="<kebab-name>"
  >
    <Sequence from={SCENES.scene01.start} durationInFrames={SCENES.scene01.duration}>
      <Scene01Hook />
    </Sequence>
    <Sequence from={SCENES.scene02.start} durationInFrames={SCENES.scene02.duration}>
      <Scene02Access />
    </Sequence>

    {/* Narration audio */}
    <Sequence from={SCENES.scene01.start + AUDIO_OFFSET}>
      <Audio src={staticFile('audio/<name>/scene01.mp3')} volume={() => 1} />
    </Sequence>
    <Sequence from={SCENES.scene02.start + SCENE02_AUDIO_OFFSET}>
      <Audio src={staticFile('audio/<name>/scene02.mp3')} volume={() => 1} />
    </Sequence>

    {/* Sonic logo */}
    <Sequence durationInFrames={45}>
      <Audio src={staticFile('audio/shared/sonic-logo.mp3')} volume={() => 0.5} />
    </Sequence>

    {/* SFX layers — see Step 7 */}
  </GoogleShortShell>
);
```

### `scenes/Scene01Hook.tsx`

Compose using `GoogleHeroSlide` for Phase 1. **Pass the user's chosen `overline`** — do NOT default to "Just Launched" unless they picked it. Grep all keyframes from `scene01-sync.json` (never estimate).

```tsx
<GoogleHeroSlide
  overline="New in Chrome"   // ← use the user's Step 1 answer verbatim
  heroWord="AI MODE"
  accent={GOOGLE_ACCENTS.blue}
  screenshotSrc="images/<name>/hero.png"
  ...
/>
```

### `scenes/Scene02Access.tsx`

Compose using `GoogleFeatureSlide` (one per screenshot/video), **rotating accent colors** across the 4 Google brand colors via `GOOGLE_ACCENT_ROTATION` — no two adjacent slides should share a color. Then `GoogleFeatureCombo` for grouped lighter features, then inline plan-chip row + `GoogleFullVideoTease`, then `GoogleURLReveal`, then `GoogleCTACard`.

Phase boundaries derive from sync JSON — grep for pivot words, plan chip words, model name, URL word, and final word.

### Register in `src/Root.tsx`

Add import + `<Composition>` entry with `width={1080} height={1920} fps={30} durationInFrames={TOTAL_FRAMES}`.

</scaffold>

<sfx>

## Step 7: SFX layer wiring

In `Composition.tsx`, mount the SFX Sequences at absolute composition frames. Respect the 0.25 hard cap and the per-SFX table in `.claude/rules/audio-design.md`.

Minimum SFX set for a Google Short:
- Frame 5 (soft `impact-slam` vol 0.15) — under the overline
- `kfHero` (scale-slam 0.20 + screen-shake 0.15) — hero word slam
- `kfScreenshot` (cinematic-whoosh 0.15 + spring-pop 0.13) — hero image reveal
- Each feature sub-phase boundary (cinematic-whoosh 0.13) — slide transition
- Each feature visual entry (spring-pop 0.15) — screenshot/video pop
- Plan chip reveals (pop 0.12)
- Model/backend badge (scale-slam 0.20)
- Tease card (spring-pop 0.13)
- URL reveal (scale-slam 0.20 + screen-shake 0.15)
- CTA mount (scale-slam 0.20)

</sfx>

<validation-and-render>

## Step 8: Validate

```bash
pnpm lint
pnpm exec tsc --noEmit 2>&1 | grep <Name>    # must be empty
```

Optional: `/rulecheck <Name>` (runs the 3 parallel scanners then the fixer).

## Step 9: Pause for user approval

**STOP HERE.** Show the user:
- TOTAL_FRAMES + predicted duration
- A summary of scene structure (sub-phase list + which accent color each slide uses)
- Which `topLogoKey` is configured
- Any outstanding TODOs

Ask for explicit approval before rendering. NEVER auto-render.

## Step 10: Render (only on user "yes")

```bash
# Normal-speed master (10-bit 444, near-lossless)
pnpm exec remotion render <Name> out/<Name>/<kebab-topic>.mp4 \
  --codec h264 --image-format png --pixel-format yuv444p10le \
  --color-space bt709 --crf 5 --x264-preset slow --hardware-acceleration disable

# 1.05x YouTube-ready (8-bit, standard compatibility)
powershell.exe -Command "ffmpeg -i 'out/<Name>/<kebab-topic>.mp4' -filter:v 'setpts=PTS/1.05' -filter:a 'atempo=1.05' -c:v libx264 -crf 5 -pix_fmt yuv420p -preset slow -c:a aac -b:a 192k 'out/<Name>/<kebab-topic>-1.05x.mp4' -y"
```

If the first render crashes with `WasmHash`, `rm -rf node_modules/.cache/webpack/` and retry ONCE.

## Step 11: Generate SEO-optimized YouTube description

Create `src/<Name>/youtube-description.md` following `.claude/rules/youtube-metadata.md`:
- First 200 chars keyword-dense (topic + Google + product name + year)
- Dynamous CTA block (mandatory, between hook and body)
- Feature bullets (keyword-rich)
- Partner / availability / rollout proof
- Resources links (verified live — `blog.google`, official docs, etc.)
- Debate CTA as final line
- 20+ hashtags mixing specific (`#AIMode`, `#Chrome`, `#Gemini`) and broad (`#AI`, `#GoogleSearch`, `#Android`)

</validation-and-render>

<quality-rules>

## Non-negotiable rules for Google Shorts

- **Top product logo is always visible** — default `google` wordmark at top:60, swap per Short via `topLogoKey`
- **Every phase container uses `padding-top: 240px`** — consistent gap below logo
- **Hero overline is configurable, not fixed** — use the user's chosen phrase, never force "Just Launched"
- **Accent rotation across slides** — rotate through `GOOGLE_ACCENT_ROTATION` (blue → red → yellow → green), never adjacent slides sharing a color
- **Shorts = NO background music** — narration + SFX + sonic logo only
- **Shorts = NO Outro, NO DynamousMidroll, NO SubscribeBanner** (the red Subscribe PILL in the CTA card is fine; the full `SubscribeBanner` component is not)
- **Every visual trigger grepped from sync JSON** — never estimate timestamps
- **Minimum reading time 75 frames (2.5s)** between last content trigger and phase end
- **SFX hard cap volume 0.25** — respect per-SFX table
- **Final render always at 1.05x** — via ffmpeg post-process
- **Filename uses topic-descriptive kebab-case**, never `final.mp4`
- **Never read exact version numbers aloud** — always show on screen only

</quality-rules>

<references>

## References (load these when scaffolding)

- **Template components**: `src/shared/templates/google-short/` — reusable pieces
- **Template README**: `src/shared/templates/google-short/README.md` — component API + overline inspiration
- **Anthropic reference**: `src/ClaudeDesignShort/` — structurally identical pattern (swap components)
- **Hook design skill**: `youtube-shorts-hooks` — invoked in Step 2
- **Phase commands**: `/diy-yt-creation:phase0-research`, `/diy-yt-creation:phase3-audio`, `/diy-yt-creation:phase4-sync`
- **Rules**:
  - `.claude/rules/agent-pitfalls.md` — FONTS.primary, +T bug, SFX cap, phase fade-out
  - `.claude/rules/scene-design.md` — reading time, phase rendering
  - `.claude/rules/scriptwriting.md` — banned phrases, softened numbers, debate CTA
  - `.claude/rules/audio-design.md` — SFX volume table, Shorts bg-music rule
  - `.claude/rules/youtube-metadata.md` — description SEO, hashtag rules
  - `.claude/rules/brand-logos.md` — top-banner topic-brand watermark

</references>

<output>
- `src/<Name>/` — complete composition (Composition.tsx, scenes/, constants/, scripts/, research/)
- `public/audio/<name>/` — scene01.mp3 + scene02.mp3 + sync JSONs
- `public/images/<name>/` + `public/video/<name>/` — user-provided hero/feature/thumbnail assets
- `src/<Name>/youtube-description.md` — SEO-optimized description
- `out/<Name>/<kebab-topic>.mp4` + `<kebab-topic>-1.05x.mp4` — rendered master + YouTube-ready (only after user approval)
</output>
