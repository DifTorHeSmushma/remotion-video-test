---
description: "Standalone Shorts full-auto: Create a complete YouTube Short (1-3 min) from topic to render-ready"
argument-hint: <topic, product URL, or concept description>
---

<objective>
Execute the ENTIRE Standalone YouTube Shorts Creation Workflow from concept to render-ready vertical composition.

**This is NOT for deriving Shorts from long-form videos** — use `/diy-yt-creation:phase6-shorts` for that.
This creates **original standalone Shorts** (1-3 minutes, 1080x1920 vertical) with cinematic hooks, beat-aligned music, and phase-based rendering.

**Goal**: Go from concept to render-ready vertical composition autonomously, then STOP for user approval before rendering.
**Output**: `out/<AnimationName>Short/final.mp4` + all intermediate artifacts

IMPORTANT: Do NOT ask questions during execution EXCEPT before rendering. Gather all parameters upfront, then run autonomously through Phases 0-4b. Phase 5 MUST stop and wait for explicit user approval before starting any render.

**CRITICAL**: NEVER start `remotion render` without explicit user confirmation. This is a hard gate, not a suggestion.
</objective>

<initial-setup>

## Step 1: Parse Input and Detect Parameters

Parse "$ARGUMENTS" to extract parameters:

**If structured brief** (contains "**Topic**:", "**Duration**:", etc.):
- Extract all fields directly from the brief
- Store as `PARAMS` object for passing to phases

**If freeform text**:
- Look for duration patterns: "60s", "90s", "2min", "3min"
- Extract topic/URL from the text

## Step 2: Set Parameters (Use Defaults for Missing Values)

```yaml
PARAMS:
  topic: "<extracted from $ARGUMENTS>"
  duration: "<detected or default: 90s>"
  tone: "<from brief or default: tech-influencer-edgy>"
  resolution: "1080x1920"           # ALWAYS vertical — non-negotiable
  target_audience: "<from brief or infer from topic>"
  key_angle: "<from brief or determine in Phase 0>"
  links: "<URLs from brief or empty>"
  must_mention: "<from brief or empty>"
  technical_terms: "<from brief or empty>"
```

### Duration-to-Structure Quick Reference (Shorts)

| Duration | Scenes | Words | Phases per Scene | Structure |
|----------|--------|-------|------------------|-----------|
| 60s | 1 | ~170 | 4-5 | Thumbnail + Hook + 2-3 Body + CTA + EndThumbnail |
| 90s | 1-2 | ~255 | 5-6 | Thumbnail + Hook + 3-4 Body + CTA + EndThumbnail |
| 2min | 2-3 | ~340 | 4-5 each | Thumbnail + Hook + 4-6 Body + CTA + EndThumbnail |
| 3min | 3-4 | ~510 | 4-5 each | Thumbnail + Hook + 6-8 Body + CTA + EndThumbnail |

**Word count**: Shorts use `--shorts` TTS flag (1.15x speed), so ~2.85 words/second instead of 2.5.

## Step 3: Derive AnimationName

Convert topic to PascalCase + "Short" suffix:
- "gemma 4 on-device" -> "Gemma4Short"
- "claude code hooks" -> "ClaudeCodeHooksShort"
- "archon docker branches" -> "ArchonDockerBranchesShort"

Store as `ANIMATION_NAME` for all phases.

**Audio directory name**: Convert to kebab-case WITHOUT "Short" suffix:
- "Gemma4Short" -> `public/audio/gemma4/`
- "ClaudeCodeHooksShort" -> `public/audio/claude-code-hooks/`

## Step 4: Initialize Directory Structure

```
src/{ANIMATION_NAME}/
  constants/
  scenes/
  scripts/
  research/
  images/          (optional, for screenshots)
```

## Step 5: Initialize Phase Status File

Create `src/{ANIMATION_NAME}/phase-status.md`:

```markdown
# Phase Status: {ANIMATION_NAME} (Standalone Short)

| Phase | Status | Completed |
|-------|--------|-----------|
| 0 - Research | pending | |
| 1 - Plan | pending | |
| 2 - Script | pending | |
| 2a - TTS Script | pending | |
| 3 - Audio | pending | |
| 3.2 - BG Music | pending | |
| 4 - Build | pending | |
| 4b - Visual QA | pending | |
| 5 - Render | pending | |
```

</initial-setup>

<orchestration>

## Phase 0: Research (Lightweight)

Shorts research is lighter than long-form — focus on the ONE key angle, not exhaustive coverage.

### Step 0.1: Topic Research

If `PARAMS.links` contains URLs:
- Fetch and analyze the linked content (README, docs, blog posts)
- Extract the single most compelling angle for a Short

If freeform topic:
- Use WebSearch to find: current stats, recent announcements, community sentiment
- Identify the "scroll-stop" fact or insight

### Step 0.2: Write Content Brief

Write `src/{ANIMATION_NAME}/research/content-brief.md`:

```markdown
# Content Brief: {topic}

## Format
- **Type**: Standalone YouTube Short
- **Duration**: {PARAMS.duration}
- **Resolution**: 1080x1920 (vertical)

## Core Angle
{One sentence — the single insight this Short delivers}

## Scroll-Stop Hook
{The opening line that makes viewers stop scrolling — must work in 1.5 seconds}

## Key Facts (3-5 max)
- {Fact 1 with source}
- {Fact 2 with source}
- {Fact 3 with source}

## Visual Concept
{What the viewer SEES — not just what they hear. Shorts are visual-first.}

## Target Audience
{Who watches this and why they care}

## Hook Psychology
{Which youtube-shorts-hooks formula fits best and why}
```

**Proceed immediately** to Phase 1.

---

## Phase 1: Plan (Vertical Layout + Cinematic Hook Blueprint)

### Step 1.1: Invoke youtube-shorts-hooks Skill

**MANDATORY**: Before writing the plan, invoke the youtube-shorts-hooks skill:
```
/youtube-shorts-hooks {PARAMS.topic}
```
This provides the 7 hook formulas, 1.5-second cliff rule, loop design patterns, and vertical safe zones. Use its framework to select the hook formula.

### Step 1.2: Select Hook Formula

Score the top 3 hook formulas from youtube-shorts-hooks against the content brief using its 5-criteria scoring (scroll-stop, standalone, specificity, curiosity, emotion — minimum 18/25 to proceed).

### Step 1.3: Write Plan

Write `.agents/plans/{ANIMATION_NAME}.plan.md`:

```markdown
# Plan: {ANIMATION_NAME}

## Format
- Type: Standalone YouTube Short
- Duration: {duration}
- Resolution: 1080x1920
- FPS: 30
- TRANSITION_DURATION: 0 (Shorts use direct cuts, no TransitionSeries)

## Hook Design
- **Formula**: {selected youtube-shorts-hooks formula}
- **Opening line**: "{scroll-stop line}" (must land in < 1.5 seconds)
- **Score**: {X}/25 (scroll-stop + standalone + specificity + curiosity + emotion)

## Cinematic Hook Blueprint

```yaml
cinematic_hook_blueprint:
  pattern: {FilmTrailer | ContrastPivot | StatCascade | RackFocusReveal | TerminalHacker}

  visual_beats:
    - beat: scrollStop
      timing: "0-1.5s (frames 0-45)"
      spring: slam
      sfx: smashCut
      visual: "{what appears — big number, bold claim, brand logo}"
    - beat: context
      timing: "1.5-4s"
      spring: heavy
      sfx: transition
      visual: "{supporting context}"
    - beat: pivot
      timing: "4-6s"
      spring: snappy
      sfx: pivot (triple)
      retention: [ScreenShake, GlitchInterrupt]
      visual: "{the twist or contrast}"
    - beat: payoff
      timing: "6-10s"
      spring: reveal
      sfx: brandReveal
      visual: "{the reveal or answer}"

  pivot_word: "{exact word from script where pivot hits}"
  brand_reveal_word: "{exact word for brand/product reveal}"

  music_profile:
    hook_mood: "{mood from HOOK_PATTERNS}"
    hook_bpm: "{bpm range, e.g., 95-105}"
    body_bpm: "{75-90}"
    cta_bpm: "{110-120}"
```

## Scene Structure

### Scene 01: {name} ({duration}s, {frames} frames)
- **Phases**: {phase count}
- **Phase 1 (Hook)**: {what appears, 0-Xs}
- **Phase 2 (Body)**: {what appears, X-Ys}
- **Phase 3 (Body)**: {what appears, Y-Zs}
- **Phase N (CTA)**: {call to action}
- **Visual style**: {layout description for vertical}
- **Retention**: {ScreenShake at X, GlitchInterrupt at Y, FloatingCallout at Z}

### Scene 02: {name} (if duration > 90s)
...

## Thumbnail Frame (Frame 0)
- **Hero element**: {big number, emoji, or bold text}
- **Color**: {high-contrast accent}
- **Text**: {3-4 words max}

## End Thumbnail Frame (Last Frame)
YouTube lets creators pick a custom thumbnail for Shorts, and the last frame is what viewers see when the video ends/loops. This frame MUST be a standalone high-CTR thumbnail — NOT the CTA or a faded-out state.

- **Design**: Same visual weight as frame 0 thumbnail but can differ in content
- **Hero element**: Key takeaway stat, bold claim, or curiosity hook for replay
- **Color**: High-contrast, matches brand accent
- **Text**: 3-5 words max, large and legible at phone size
- **No animation**: Static frame, no springs or fades
- **No progress bar**: SlimProgressBar hidden on this frame
- **No watermark clutter**: Keep clean for maximum thumbnail impact

## Mandatory Components
- [x] BrandWatermark (size=180)
- [x] NoiseOverlay (opacity=0.07)
- [x] Cinematic hook with SFX
- [x] Thumbnail-optimized frame 0
- [x] End thumbnail frame (last frame — high-CTR static thumbnail for YouTube picker)
- [ ] Product logo banner (if about a specific product)
- [ ] ShortsPartBadge (only if part of a series)
```

**Proceed immediately** to Phase 2.

---

## Phase 2: Script

### Step 2.1: Write Script

Write `src/{ANIMATION_NAME}/scripts/full-script.md`:

**Shorts script rules**:
- NO empty lines between sentences (empty lines = pauses in TTS)
- Punchy, single-line sentences
- First line must hook in < 1.5 seconds (5-8 words max)
- Last 3-5 seconds must be a clear CTA
- Word count must match duration (see Duration-to-Structure table)
- Never hyphenate common acronyms: AI, UI, XSS, SDK, API, GPT, PDF, HTML, RFC
- Never say exact numbers — always say "around" (per user preference)
- No AI slop phrases: "nobody is talking about", manufactured intrigue
- No hype — be honest and community-focused, no superlatives
- Use plain ASCII: no em dashes, no smart quotes (TTS artifacts)

```markdown
# {ANIMATION_NAME} Script

## Scene 01: {name}

{Script text — no empty lines, punchy sentences, hook first}
```

### Step 2.2: Quality Check

Verify:
- [ ] Word count matches target for duration
- [ ] First line is < 8 words and hooks immediately
- [ ] No empty lines in scene scripts
- [ ] No banned phrases (hype, AI slop, exact numbers)
- [ ] CTA in final 3-5 seconds
- [ ] youtube-shorts-hooks 7-gate validation passes

**Proceed immediately** to Phase 2a.

---

## Phase 2a: TTS Script Files

Split `full-script.md` into per-scene TTS files:

- `src/{ANIMATION_NAME}/scripts/scene-01-{name}.txt`
- `src/{ANIMATION_NAME}/scripts/scene-02-{name}.txt` (if multi-scene)

**TTS file rules**:
- One script per scene
- No empty lines (they create unwanted pauses)
- No markdown formatting
- Plain ASCII only (no em dashes, smart quotes, etc.)

**Proceed immediately** to Phase 3.

---

## Phase 3: Audio Generation

### Step 3.1: Generate TTS Audio

For each scene script:
```bash
python text-to-speech.py \
  -i src/{ANIMATION_NAME}/scripts/scene-01-{name}.txt \
  -o public/audio/{audio-dir}/ \
  -s src/{ANIMATION_NAME}/scripts/ \
  -n scene01 \
  --shorts
```

The `--shorts` flag uses `ELEVENLABS_SPEED_SHORTS` (default 1.15x) for faster pacing.

### Step 3.2: Create timing.ts

After all audio is generated, create `src/{ANIMATION_NAME}/constants/timing.ts`:

```typescript
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

export const AUDIO_OFFSET = 15; // frames before narration starts (thumbnail display time)

// Scene durations from audio files
const SCENE01_AUDIO_FRAMES = {frames}; // {seconds}s * 30fps
const BUFFER_FRAMES = 75; // 2.5s reading time buffer at end
const END_THUMBNAIL_FRAMES = 1; // 1 static frame at the very end for YouTube thumbnail picker

// MANDATORY: reserve last 10-20s (300-600 frames, target 450) for YouTube end-screen video cards.
// Critical narration / punchline must end BEFORE END_SCREEN_ZONE_START.
export const END_SCREEN_ZONE_FRAMES = 450; // 15s — range 300-600

export const SCENES = {
  scene01: {
    start: 0,
    duration: AUDIO_OFFSET + SCENE01_AUDIO_FRAMES + BUFFER_FRAMES,
  },
  // scene02: { ... } if multi-scene
} as const;

export const TRANSITION_DURATION = 0; // Shorts use direct cuts

const SCENE_FRAMES = Object.values(SCENES).reduce((sum, s) => sum + s.duration, 0);
export const TOTAL_FRAMES = SCENE_FRAMES + END_SCREEN_ZONE_FRAMES;
export const END_SCREEN_ZONE_START = TOTAL_FRAMES - END_SCREEN_ZONE_FRAMES;

// Audio-to-frame sync helper
export const wordToFrame = (time: number, offset: number): number =>
  Math.round(time * FPS) + offset;
```

### Step 3.3: Validate Duration

**Hard limits**:
- Minimum: 1800 frames (60 seconds)
- Maximum: 5400 frames (180 seconds / 3 minutes)

If TOTAL_FRAMES < 1800: STOP — script is too short, needs more content.
If TOTAL_FRAMES > 5400: STOP — script is too long, needs trimming.

**Proceed immediately** to Phase 3.2.

---

## Phase 3.2: Background Music Generation (AUTO)

Generate multi-segment background music matching the hook's cinematic pattern.

**Read** the cinematic hook blueprint from `.agents/plans/{ANIMATION_NAME}.plan.md` to extract:
- `music_profile.hook_mood` -> `--hook-mood` flag
- `music_profile.hook_bpm` -> `--hook-bpm` flag
- `music_profile.body_bpm` -> `--body-bpm` flag
- `music_profile.cta_bpm` -> `--cta-bpm` flag

**Run**:
```bash
python generate-bg-music.py {ANIMATION_NAME} --multi-segment \
  --hook-mood {hook_mood} \
  --hook-bpm {hook_bpm} \
  --body-bpm {body_bpm} \
  --cta-bpm {cta_bpm}
```

**Expected output**:
- `public/audio/{audio-dir}/bg-music-hook.mp3`
- `public/audio/{audio-dir}/bg-music-body.mp3`
- `public/audio/{audio-dir}/bg-music-cta.mp3`
- `public/audio/{audio-dir}/bg-music-metadata.json`

**For Shorts under 90s**: The body segment may be very short or unused. That's fine — the hook and CTA segments are what matter most for cinematic impact.

**Proceed immediately** to Phase 4.

---

## Phase 4: Build Vertical Scenes

### Step 4.0: Read All Inputs

Gather from disk:
- `.agents/plans/{ANIMATION_NAME}.plan.md` (visual design + cinematic hook blueprint)
- `src/{ANIMATION_NAME}/scripts/sceneNN-sync.json` (word timestamps)
- `src/{ANIMATION_NAME}/constants/timing.ts` (scene durations)
- `public/audio/{audio-dir}/bg-music-metadata.json` (BPM for beat alignment)

### Step 4.1: Create Constants

**colors.ts**:
```typescript
export const COLORS = {
  background: '#0B1120',
  cardBackground: '#1A2235',
  text: '#F1F5F9',
  textSecondary: '#94A3B8',
  primary: '#3B82F6',      // Adapt to topic/brand
  secondary: '#8B5CF6',
  accent: '#22C55E',
  danger: '#EF4444',
  glow: '#3B82F633',
} as const;
```

**fonts.ts** (import shared):
```typescript
export { FONTS } from '../../shared/constants/fonts';
```

**springs.ts**:
```typescript
import { HOOK_SPRINGS } from '../../shared/constants/hookSprings';

export const SPRINGS = {
  ...HOOK_SPRINGS,
  entrance: { damping: 12, stiffness: 100, mass: 0.5 },
  pop: { damping: 10, stiffness: 130, mass: 0.5 },
} as const;
```

### Step 4.2: Build Scene Components (Cinematic Hook + Phases)

Each scene file follows this structure:

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, spring } from 'remotion';
import { COLORS } from '../constants/colors';
import { FONTS } from '../constants/fonts';
import { SPRINGS } from '../constants/springs';
import { AUDIO_OFFSET, FPS, TOTAL_FRAMES, wordToFrame } from '../constants/timing';
// Retention components as needed:
import { ScreenShake } from '../../shared/components/retention/ScreenShake';
import { GlitchInterrupt } from '../../shared/components/retention/GlitchInterrupt';
import { FloatingCallout } from '../../shared/components/retention/FloatingCallout';
import { SlimProgressBar } from '../../shared/components/retention/SlimProgressBar';

const O = AUDIO_OFFSET;

// ── Phase boundaries (from sync JSON) ──
const P1_END = wordToFrame({timestamp}, O);
const P2_END = wordToFrame({timestamp}, O);
// ...

// ── End thumbnail (very last frame) ──
const END_THUMBNAIL_FRAME = TOTAL_FRAMES - 1;

// ── Keyframes (precise word timings from sync JSON) ──
const KF_WORD1 = wordToFrame({timestamp}, O);
const KF_WORD2 = wordToFrame({timestamp}, O);
// ... EVERY visual trigger must come from sync JSON

// ── Animation helpers ──
const fadeIn = (f: number, start: number, dur = 12) =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

const phaseOp = (f: number, start: number, end: number, inD = 12, outD = 8) =>
  interpolate(f, [start, start + inD, end - outD, end], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

const ss = (f: number, start: number, config = SPRINGS.pop) =>
  spring({ frame: f - start, fps: FPS, config, durationRestThreshold: 0.001 });

export const Scene01{Name}: React.FC = () => {
  const frame = useCurrentFrame();

  const isThumbnail = frame === 0;
  const isEndThumbnail = frame >= END_THUMBNAIL_FRAME;
  const isPhase1 = !isThumbnail && !isEndThumbnail && frame < P1_END;
  const isPhase2 = !isEndThumbnail && frame >= P1_END && frame < P2_END;
  // ...

  return (
    <AbsoluteFill style={{
      backgroundColor: COLORS.background,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '180px 64px 220px',  // Top: logo banner space, Bottom: above YT UI
    }}>
      {/* Retention: SlimProgressBar (skip on thumbnail frames) */}
      {!isThumbnail && !isEndThumbnail && <SlimProgressBar totalFrames={TOTAL_FRAMES} color={COLORS.primary} startFrame={O} />}

      {/* ═══ THUMBNAIL (frame 0) ═══ */}
      {isThumbnail && (
        <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ display: 'block', fontSize: 280, fontWeight: 900, color: COLORS.primary }}>{heroStat}</div>
          <div style={{ display: 'block', fontSize: 72, fontWeight: 900, color: COLORS.text }}>{titleText}</div>
        </AbsoluteFill>
      )}

      {/* ═══ END THUMBNAIL (last frame — YouTube thumbnail picker) ═══ */}
      {/* Static, high-CTR frame. Can differ from frame 0 — use key takeaway or curiosity hook.
          Best practices: 3-5 words max, hero stat or bold claim, high-contrast colors,
          no animation, no progress bar, no watermark clutter. */}
      {isEndThumbnail && (
        <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ display: 'block', fontSize: 240, fontWeight: 900, color: COLORS.accent }}>{takeawayStat}</div>
          <div style={{ display: 'block', fontSize: 64, fontWeight: 900, color: COLORS.text, textAlign: 'center' }}>{takeawayText}</div>
        </AbsoluteFill>
      )}

      {/* ═══ PHASE 1: CINEMATIC HOOK ═══ */}
      {/* Apply cinematic_hook_blueprint beats here:
          - Use HOOK_SPRINGS for spring configs
          - Use HOOK_SFX presets (SFX placed in Composition.tsx)
          - Beat-align impacts to bg-music-metadata BPM via alignToDownbeat()
          - Include ScreenShake + GlitchInterrupt at pivot moment
          - Smash cut: white flash overlay at emotional pivot */}
      {isPhase1 && (
        <div style={{ opacity: phaseOp(frame, {hookStart}, P1_END), /* ... */ }}>
          {/* Scroll-stop element — must appear in first 45 frames */}
          {/* Context — supporting visual */}
          {/* Pivot — ScreenShake + smash cut */}
          {/* Payoff — reveal */}
        </div>
      )}

      {/* ═══ BODY PHASES ═══ */}
      {/* Each phase: fade in, content synced to wordToFrame(), fade out before next */}

      {/* ═══ CTA PHASE (last 3-5 seconds) ═══ */}
      {/* Clear call to action — like, follow, comment, full video */}
    </AbsoluteFill>
  );
};
```

### Vertical Layout Rules (CRITICAL)

| Rule | Enforcement |
|------|-------------|
| **Font floor: 28px** | Nothing below 28px. Hero numbers: 200-280px. Titles: 64-96px. Body: 40-48px. |
| **Content above y=1280** | YouTube UI overlaps bottom ~640px. Keep all important content in top 2/3. |
| **Padding**: `180px top, 220px bottom` | Accounts for logo banner (top) and YT UI (bottom). |
| **Phase-based ONLY** | `{isPhaseN && (...)}` — elements REPLACE, never overlap. |
| **All text needs explicit `color`** | Dark background (#0B1120) makes default black text invisible. |
| **All divs need `display: 'block'`** | Headless Chromium div collapse prevention. |
| **`whiteSpace: 'pre'`** on code blocks | Preserves indentation in FONTS.mono containers. |
| **No emoji as icons** | Use Unicode text symbols (headless Chromium renders emoji as black). |
| **Last phase MUST fade out** | 4-keyframe interpolation: `[start, start+N, end-M, end]` -> `[0, 1, 1, 0]`. |
| **Hero word auto-fit** | Any slam-in hero word > 7 chars with no space/dash/slash MUST use `FitHeadline` (maxWidth ~900, minFont 150) so it shrinks instead of overflowing. See `agent-pitfalls.md` "Hero Word Slam-In Overflows" rule. |

### Cinematic Hook Techniques Checklist

For the hook phase (Phase 1), verify ALL of these:

- [ ] **Spring physics variation**: Different spring configs for different animations (slam for impacts, gentle for text, snappy for cards)
- [ ] **Smash cut**: White flash overlay (`[0->1->0]` over 6 frames) at emotional pivot
- [ ] **Triple SFX**: impact-slam + screen-shake + glitch-zap at pivot (placed in Composition.tsx)
- [ ] **ScreenShake**: `triggerFrame` at pivot word
- [ ] **GlitchInterrupt**: `triggerFrame` at pivot or reveal
- [ ] **Beat alignment**: If bg-music-metadata.json exists, snap impact frames to downbeats via `alignToDownbeat()`
- [ ] **Scale pops**: `spring()` scale from 0 to 1 on key reveals
- [ ] **Scroll-stop in first 45 frames**: The hook visual MUST appear before frame 45 (1.5 seconds)

### Step 4.3: Build Composition.tsx

```tsx
import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { AUDIO_OFFSET, FPS, TOTAL_FRAMES } from './constants/timing';
import { COLORS } from './constants/colors';
import { Scene01{Name} } from './scenes/Scene01{Name}';
import { BrandWatermark } from '../shared/components/BrandWatermark';
import { NoiseOverlay } from '../shared/components/NoiseOverlay';
// Import HOOK_SFX for cinematic hook SFX presets
import { HOOK_SFX } from '../shared/constants/hookSprings';

const O = AUDIO_OFFSET;
const w2f = (t: number) => Math.round(t * FPS) + O;

export const {ANIMATION_NAME}Composition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>

      {/* ── Scene(s) ── */}
      <Scene01{Name} />

      {/* ── Narration Audio ── */}
      <Sequence from={O}>
        <Audio src={staticFile('audio/{audio-dir}/scene01.mp3')} />
      </Sequence>

      {/* ── Sonic Logo (frame 0) ── */}
      <Sequence from={0} durationInFrames={45}>
        <Audio src={staticFile('audio/shared/sonic-logo.mp3')} volume={0.6} />
      </Sequence>

      {/* ── Background Music (multi-segment) ── */}
      {/* Hook music — energetic, matches cinematic hook */}
      <Sequence from={0} durationInFrames={HOOK_END}>
        <Audio
          src={staticFile('audio/{audio-dir}/bg-music-hook.mp3')}
          volume={(f) => {
            const { interpolate: interp } = require('remotion');
            return interp(f, [0, 15, HOOK_END - 30, HOOK_END], [0, 0.12, 0.12, 0], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            });
          }}
        />
      </Sequence>

      {/* Body music — ambient, low volume under narration */}
      <Sequence from={HOOK_END} durationInFrames={CTA_START - HOOK_END}>
        <Audio src={staticFile('audio/{audio-dir}/bg-music-body.mp3')} volume={0.07} />
      </Sequence>

      {/* CTA music — upbeat, fades in and out */}
      <Sequence from={CTA_START} durationInFrames={TOTAL_FRAMES - CTA_START}>
        <Audio
          src={staticFile('audio/{audio-dir}/bg-music-cta.mp3')}
          volume={(f) => {
            const { interpolate: interp } = require('remotion');
            return interp(f, [0, 20, (TOTAL_FRAMES - CTA_START) - 30, TOTAL_FRAMES - CTA_START], [0, 0.12, 0.12, 0], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            });
          }}
        />
      </Sequence>

      {/* ── Cinematic Hook SFX ── */}
      {/* Scroll-stop impact */}
      <Sequence from={w2f({scrollStopTimestamp})} durationInFrames={30}>
        <Audio src={staticFile(HOOK_SFX.smashCut.src)} volume={HOOK_SFX.smashCut.vol} />
      </Sequence>

      {/* Pivot — triple SFX layering */}
      <Sequence from={w2f({pivotTimestamp})} durationInFrames={30}>
        <Audio src={staticFile(HOOK_SFX.pivot[0].src)} volume={HOOK_SFX.pivot[0].vol} />
      </Sequence>
      <Sequence from={w2f({pivotTimestamp})} durationInFrames={25}>
        <Audio src={staticFile(HOOK_SFX.pivot[1].src)} volume={HOOK_SFX.pivot[1].vol} />
      </Sequence>
      <Sequence from={w2f({pivotTimestamp}) + 3} durationInFrames={20}>
        <Audio src={staticFile(HOOK_SFX.pivot[2].src)} volume={HOOK_SFX.pivot[2].vol} />
      </Sequence>

      {/* Brand/product reveal */}
      <Sequence from={w2f({revealTimestamp})} durationInFrames={30}>
        <Audio src={staticFile(HOOK_SFX.brandReveal.src)} volume={HOOK_SFX.brandReveal.vol} />
      </Sequence>

      {/* ── Body SFX (phase transitions, emphasis) ── */}
      {/* Add spring-pop, glitch-zap, screen-shake at phase transitions */}
      {/* All SFX volumes MUST be <= 0.5 */}

      {/* ── Mandatory Overlays ── */}
      <BrandWatermark size={180} />
      <NoiseOverlay opacity={0.07} />

      {/* ── Product Logo Banner (if applicable) ── */}
      {/* <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 10 }}>
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 140, ... }}>
          <Img src={staticFile('images/{brand}/logo.svg')} style={{ height: 36 }} />
        </div>
      </AbsoluteFill> */}

    </AbsoluteFill>
  );
};
```

**Shorts Composition Rules** (differs from long-form):
- **NO TransitionSeries** — use simple `<AbsoluteFill>` with phase conditionals
- **NO OutroSequence** — Shorts end with CTA, not brand outro
- **NO DynamousMidroll** — too short for promo breaks
- **NO SubscribeBanner** — too intrusive for Shorts format
- **NO ShortsFullVideoFooter** — that's for derived Shorts only
- **BrandWatermark size={180}** — smaller for vertical
- **NoiseOverlay opacity={0.07}** — mandatory
- **Sonic logo at frame 0** — mandatory
- **Multi-segment BG music** — hook/body/cta with dynamic volume curves

### Step 4.4: Register in Root.tsx

Add to `src/Root.tsx`:

```tsx
import { {ANIMATION_NAME}Composition } from "./{ANIMATION_NAME}/Composition";
import { TOTAL_FRAMES as {UPPER}_TOTAL } from "./{ANIMATION_NAME}/constants/timing";

<Composition
  id="{ANIMATION_NAME}"
  component={{ANIMATION_NAME}Composition}
  durationInFrames={{UPPER}_TOTAL}
  fps={30}
  width={1080}
  height={1920}
/>
```

### Step 4.5: Per-Scene Validation

After building each scene, run:
```
/validate-scene {ANIMATION_NAME} SceneNN
```

Fix any issues before proceeding. Do NOT wait until all scenes are built.

### Step 4.6: Full Composition Validation

```bash
npx tsx scripts/validate-sync.ts {ANIMATION_NAME}
```

Fix all errors before proceeding to QA.

### Step 4.7: Write QA Frames Manifest

Write `src/{ANIMATION_NAME}/qa-frames.json`:

```json
{
  "compositionId": "{ANIMATION_NAME}",
  "frames": [
    { "frame": 0, "label": "Thumbnail", "expect": "High-CTR static frame" },
    { "frame": 15, "label": "Hook start", "expect": "Scroll-stop visual" },
    { "frame": {pivotFrame}, "label": "Pivot moment", "expect": "ScreenShake + smash cut" },
    { "frame": {phase2Start}, "label": "Phase 2 start", "expect": "Clean transition, no overlap" },
    { "frame": {ctaStart}, "label": "CTA", "expect": "Clear call to action" },
    { "frame": {lastFrame - 2}, "label": "CTA end", "expect": "CTA visible before end thumbnail" },
    { "frame": {lastFrame}, "label": "End thumbnail", "expect": "Static high-CTR thumbnail — key takeaway, bold text, no animation" }
  ]
}
```

**Proceed to Phase 4b.**

---

## Phase 4b: Visual QA (SKIPPED BY DEFAULT)

**Do NOT run this phase automatically.** Mark the Phase 4b row as `skipped` and proceed directly to Phase 5.

Only spawn `remotion-qa-agent` if the user explicitly requests QA. When requested: Agent tool with `subagent_type: "remotion-qa-agent"` and `prompt: "{ANIMATION_NAME}"`. Apply the standard gate (pass -> proceed, warnings -> note, failures -> stop and fix).

---

## Phase 5: Render Gate

### Step 5.1: Lint Check

```bash
pnpm lint
```

Fix any TypeScript or ESLint errors.

### Step 5.2: Generate YouTube Metadata

Write `src/{ANIMATION_NAME}/metadata.md`:

```markdown
# {ANIMATION_NAME} — YouTube Metadata

## Title
{Short, punchy title — 60 chars max, front-load keywords}

## Description
{2-3 sentence description with keywords}

#Shorts #AI #{relevant hashtags — 5-8 total}

## Tags
{comma-separated tags}
```

### Step 5.3: Present Summary and STOP

```markdown
## Standalone Short Ready for Review

**Composition**: {ANIMATION_NAME}
**Duration**: {seconds}s ({frames} frames at 30fps)
**Resolution**: 1080x1920 (vertical)
**Scenes**: {count}
**Hook**: {hook formula} pattern with cinematic SFX
**BG Music**: Multi-segment ({hook_mood}, {hook_bpm} BPM)

### QA Status
{Pass/warnings from Phase 4b}

### Files Created
- Composition: `src/{ANIMATION_NAME}/Composition.tsx`
- Scene(s): `src/{ANIMATION_NAME}/scenes/`
- Audio: `public/audio/{audio-dir}/`
- Metadata: `src/{ANIMATION_NAME}/metadata.md`

### Preview
Run `pnpm dev` and select "{ANIMATION_NAME}" in Remotion Studio.

**Ready to render?** (waiting for your confirmation)
```

**STOP HERE.** Do NOT render until user explicitly confirms.

### Step 5.4: Render (After User Approval Only)

```bash
pnpm exec remotion render {ANIMATION_NAME} out/{ANIMATION_NAME}/final.mp4 \
  --codec h264 --image-format png --pixel-format yuv444p10le \
  --color-space bt709 --crf 5 --x264-preset slow --hardware-acceleration disable
```

Output: `out/{ANIMATION_NAME}/final.mp4`

</orchestration>

<error-handling>

## If a Phase Fails

1. **Read the error message** carefully
2. **Attempt auto-fix** if possible (lint errors, missing imports, font size violations)
3. **Report to user** with: which phase failed, error details, suggested fix
4. **Do NOT proceed** to next phase until current phase succeeds

## Common Shorts-Specific Issues

| Issue | Fix |
|-------|-----|
| Font size < 28px | Scale up to 28px minimum |
| Content below y=1280 | Move up, increase top padding |
| TOTAL_FRAMES < 1800 | Script too short — add content |
| TOTAL_FRAMES > 5400 | Script too long — trim content |
| Text invisible on dark bg | Add explicit `color` property |
| Phases overlapping | Verify mutually exclusive `isPhaseN` conditions |
| Emoji rendering black | Replace with Unicode text symbols |

</error-handling>
