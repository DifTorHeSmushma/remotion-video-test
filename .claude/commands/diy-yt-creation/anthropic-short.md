---
description: "Anthropic/Claude launch Short — scaffold a 90-120s vertical Short using the ClaudeDesignShort design system"
argument-hint: "<topic or URL, e.g. 'Claude Design' or 'https://anthropic.com/news/xyz'>"
---

# /diy-yt-creation:anthropic-short — Anthropic/Claude Launch Short

<objective>
Create a standalone 90-120s YouTube Short (1080x1920, 30fps) for an **Anthropic or Claude product/feature launch**, using the visual system proven in `ClaudeDesignShort` and the reusable components in `src/shared/templates/anthropic-short/`.

This command is SPECIFIC to Anthropic/Claude topics. For a generic launch Short use `/diy-yt-creation:shorts-full-auto`.

**Goal**: Go from topic to render-ready composition autonomously, STOP before render, then on user approval render at 1.0x + post-process to 1.05x.
</objective>

<when-to-use>
Use this command when the user asks for a Short about:
- A Claude product launch (Design, Code, Skills, Sonnet/Opus/Haiku release, MCP server, etc.)
- An Anthropic feature or API update
- A Claude Code version bump (see `/diy-yt-creation:claude-code-version` for release-notes-only variant)

Do NOT use this for:
- Generic AI/coding topics (use `/diy-yt-creation:shorts-full-auto`)
- Videos about non-Anthropic tools (the top banner is a Claude wordmark)
- Long-form videos (use `/diy-yt-creation:full-auto`)
</when-to-use>

<initial-setup>

## Step 1: Parse topic + gather assets

Parse `$ARGUMENTS` to extract the topic. Immediately **ASK the user** for:
1. **Hero word** — the single word for the Phase 1 slam-in (e.g. `DESIGN`, `OPUS 4.7`, `SKILLS`)
2. **Product screenshot** (hero) — the main visual for the hook
3. **Feature assets** — per feature they want to spotlight, one screenshot OR short video (.mp4 or .webm)
4. **Full-video thumbnail** — the thumbnail of the long-form video this Short promotes
5. **Target URL** — where viewers should go (e.g. `claude.ai/design`)
6. **Accent colors** — confirm defaults (orange primary, purple/blue/green secondaries) OR override per slide

Derive composition name: PascalCase + `Short` suffix.
- "Claude Design" → `ClaudeDesignShort`
- "Opus 4.7 launch" → `Opus47LaunchShort`
- "MCP servers" → `MCPServersShort`

Derive audio folder: kebab-case WITHOUT `Short`.
- `ClaudeDesignShort` → `public/audio/claude-design-short/`

## Step 2: Invoke youtube-shorts-hooks skill for hook design

**CRITICAL**: Before writing ANY script copy, run the hook-design skill to get proven scroll-stop patterns tuned for this channel's faceless-tech audience.

```
Use the `youtube-shorts-hooks` skill to design the opening 3-5 seconds of this Anthropic/Claude launch Short. Topic: <extracted topic>. Hero word: <user's input>. The hook must fit the "Just Launched [BRAND WORD]" + product-screenshot pattern established in ClaudeDesignShort.
```

The skill will return a hook formula + opening line. Use it verbatim as the first sentence of Scene 01.

## Step 3: Research topic (Phase 0)

Run `/diy-yt-creation:phase0-research` with the topic to gather:
- Official launch facts (stats, quotes, partner names)
- Access details (which plans, pricing, URL)
- Real quotes from the launch blog
- Technical capabilities worth showing

Store at `src/<Name>/research/content-brief.md`.

</initial-setup>

<script-generation>

## Step 4: Write the TTS script

Create `src/<Name>/scripts/full-script.md` with TWO scenes:

**Scene 01 — Hook + Explainer + Proof (~45-55s at Shorts 1.13x)**
Structure (use research findings verbatim):
- Hook (3-5s): "Claude just launched <Hero>." + 1-sentence value prop
- Explainer (12-18s): what it does in plain English, 2-3 concrete behaviors
- Outputs (5-8s): what users get — list 2-3 artifacts
- Proof (15-20s): partner validation with named companies + a stat

**Scene 02 — Features + Access + CTA (~45-55s)**
Structure:
- Features (20-25s): 3 feature sub-phases (one per screenshot/video provided)
- Combined Team/Misc (8-10s): 2-card combo of lighter features
- Access (8-10s): plan tiers + "Powered by <current model>"
- Full-video tease: "Full breakdown on the channel"
- URL reveal (3-4s): "Find it at <URL>"
- CTA (3-4s): "Full video on the channel"

Apply TTS rules from `.claude/rules/scriptwriting.md`:
- Soften exact numbers ("around 20+" not "20.3")
- No hyphenated acronyms (AI not A-I)
- No hype words, no "here's the thing", no "under the hood"
- Final line is a debate CTA

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
cp <opus tease thumb>     public/images/<name>/opus-thumb.png
cp <cta full thumb>       public/images/<name>/cta-thumb.png
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

// CRITICAL: split buffer — short between scenes, long at end of video.
// A single 75-frame buffer on every scene leaves 2.5s of dead air between
// Scene 01's last word and Scene 02 cutting in. Together with SCENE02_AUDIO_OFFSET
// (10), total inter-scene silence is ~1.3s with the values below — natural breath.
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

Copy from `src/ClaudeDesignShort/constants/` as the baseline. Keep the Claude-brand orange + dark-navy palette.

### `Composition.tsx`

Wrap everything in `<AnthropicShortShell>` and place two scene Sequences plus audio + SFX overlays:

```tsx
import { AnthropicShortShell } from '../shared/templates/anthropic-short';
import { TOTAL_FRAMES, SCENES, AUDIO_OFFSET, SCENE02_AUDIO_OFFSET } from './constants/timing';
import { COLORS } from './constants/colors';

export const <Name>Composition: React.FC = () => (
  <AnthropicShortShell
    totalFrames={TOTAL_FRAMES}
    backgroundColor={COLORS.background}
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
  </AnthropicShortShell>
);
```

### `scenes/Scene01Hook.tsx`

Compose using `AnthropicHeroSlide` for Phase 1. Grep all keyframes from `scene01-sync.json` (never estimate). Add a demo-video Phase 2 block manually if the user's hook screenshot has companion video; otherwise reuse the hero screenshot.

### `scenes/Scene02Access.tsx`

Compose using `AnthropicFeatureSlide` (one per screenshot/video), then `AnthropicFeatureCombo` for Team+Misc, then the inline plan-chip row + `AnthropicFullVideoTease`, then `AnthropicURLReveal`, then `AnthropicCTACard`.

Phase boundaries derive from sync JSON — grep for "It" pivot words, plan chip words ("Pro.", "Max."), model name, URL word, and final word.

### Register in `src/Root.tsx`

Add import + `<Composition>` entry with `width={1080} height={1920} fps={30} durationInFrames={TOTAL_FRAMES}`.

</scaffold>

<sfx>

## Step 7: SFX layer wiring

In `Composition.tsx`, mount the SFX Sequences at absolute composition frames. Respect the 0.25 hard cap and the per-SFX table in `.claude/rules/audio-design.md`.

Minimum SFX set for an Anthropic Short:
- Frame 5 (soft `impact-slam` vol 0.15) — under "Claude just launched"
- `kfHero` (scale-slam 0.20 + screen-shake 0.15) — hero word slam
- `kfScreenshot` (cinematic-whoosh 0.15 + spring-pop 0.13) — hero image reveal
- Each feature sub-phase boundary (cinematic-whoosh 0.13) — slide transition
- Each feature visual entry (spring-pop 0.15) — screenshot/video pop
- Each plan chip (pop 0.12)
- Model badge (scale-slam 0.20)
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
- A summary of scene structure (sub-phase list)
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
- First 200 chars keyword-dense (topic + Claude + Anthropic + Opus version)
- Dynamous CTA block (mandatory, between hook and body)
- Feature bullets (keyword-rich)
- Partner social proof
- Resources links (verified live)
- Debate CTA as final line
- 20+ hashtags mixing specific (`#ClaudeDesign`) and broad (`#AITools #ProductDesign`)

</validation-and-render>

<quality-rules>

## Non-negotiable rules for Anthropic Shorts

- **Top Claude banner is always visible** — top:60, 560px wide, colored (no `brightness(0) invert(1)`)
- **Every phase container uses `padding-top: 240px`** — consistent gap below logo
- **NO redundant Claude wordmarks** — the top banner handles branding; never show a Claude logo inside a pill or card
- **Shorts = NO background music** — narration + SFX + sonic logo only
- **Shorts = NO Outro, NO DynamousMidroll, NO SubscribeBanner** (the red Subscribe PILL in the CTA card is fine; the full `SubscribeBanner` component is not)
- **Every visual trigger grepped from sync JSON** — never estimate timestamps
- **Minimum reading time 75 frames (2.5s)** between last content trigger and phase end
- **SFX hard cap volume 0.25** — respect per-SFX table
- **Final render always at 1.05x** — via ffmpeg post-process
- **Filename uses topic-descriptive kebab-case**, never `final.mp4`

</quality-rules>

<references>

## References (load these when scaffolding)

- **Canonical example**: `src/ClaudeDesignShort/` — the gold-standard Anthropic Short
- **Template components**: `src/shared/templates/anthropic-short/` — reusable pieces
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
