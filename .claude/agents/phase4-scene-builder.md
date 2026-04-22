---
name: phase4-scene-builder
description: Builds complete Remotion composition from scratch — all scene TSX files, shared components, constants (timing/colors/fonts/springs), and final Composition.tsx with TransitionSeries. Runs validate-scene per scene. Self-contained — reads ALL inputs from disk, never relies on main context state. Writes all files to src/<AnimationName>/. Returns scene inventory + validation summary.
argument-hint: <AnimationName>
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
model: sonnet
---

# Phase 4: Scene Builder Agent

Build the complete Remotion composition for `$ARGUMENTS` with animations precisely synced to the word-level timestamps from Phase 3.

**Goal**: Create React components where every visual element appears/animates exactly when the corresponding word is spoken.

**Self-Contained Inputs** (read from disk — do NOT assume main context state):
1. `.agents/plans/$ARGUMENTS.plan.md` — visual design from Phase 1 (if not found, fall back to glob `.agents/plans/*.plan.md` matching `$ARGUMENTS` split on PascalCase boundaries)
2. `src/$ARGUMENTS/scripts/sceneNN-sync.json` — word timestamps from Phase 3 (read all)
3. `src/$ARGUMENTS/constants/timing.ts` — scene durations from Phase 3
4. `src/$ARGUMENTS/scripts/full-script.md` — for scene names and narration context
5. **`src/$ARGUMENTS/retention-strategy.md`** — per-scene component prescriptions from Phase 3.5 (READ THIS FIRST before building any scene — it specifies exactly which retention components to use with exact props and triggerFrames)

**Output**: Complete `src/$ARGUMENTS/` with all components, scenes, and composition

---

## ⚠️ RETENTION STRATEGY — Read Before Building ANY Scene

**If `src/$ARGUMENTS/retention-strategy.md` exists:**

Read it immediately after loading timing.ts. It is the authoritative source for:
- Which retention components each scene uses (KineticCaption, ColorShift, SpotlightFocus, etc.)
- Exact `combineMs`, `interval`, `triggerFrame`, and `accentColor` prop values
- SpotlightFocus element timing (which words activate which diagram elements)
- Dead zone fixes (which scenes need additional interrupts and at which frames)
- Global Composition.tsx elements (SlimProgressBar, ProgressDots, MidVideoReHook)

**Apply the strategy prescriptions exactly** — do not fall back to generic rules for scenes that have a strategy entry.

**If `retention-strategy.md` does NOT exist:**

Fall back to the general rules in `scene-design.md` (KineticCaption for narration-primary scenes, ColorShift on every scene, FitHeadline for standalone headlines).

---

## ⚠️ CRITICAL RULES — Read Before Writing ANY Code

These rules are violated in nearly every session. Read them first, apply them throughout.

### RULE 1: FONTS Constant Keys
Use `FONTS.primary` and `FONTS.mono` ONLY. NEVER `FONTS.inter`, `FONTS.jetbrainsMono`, or any other key. The constants only have `primary` and `mono` keys.

### RULE 2: TransitionSeries durationInFrames — NO `+ T`
```tsx
// WRONG — 15-frame drift per scene
<TransitionSeries.Sequence durationInFrames={SCENES.hook.duration + TRANSITION_DURATION}>

// CORRECT — duration already includes transition overlap
<TransitionSeries.Sequence durationInFrames={SCENES.hook.duration}>
```
Scene durations already include `TRANSITION_DURATION`. Adding `+ T` accumulates a 15-frame error per scene.

### RULE 3: Never Hardcode `delay:` Arrays
```tsx
// WRONG — hardcoded delays cause cumulative drift
const items = [
  { text: 'First', delay: 0 },
  { text: 'Second', delay: 80 },
];

// CORRECT — each item synced to its spoken word
const items = [
  { text: 'First', triggerFrame: wordToFrame(1.2, AUDIO_OFFSET) },
  { text: 'Second', triggerFrame: wordToFrame(3.8, AUDIO_OFFSET) },
];
```

### RULE 4: Never Put `<Audio>` Inside Scene Components
Audio is managed **exclusively in Composition.tsx**. Scene components must NEVER include `<Audio>` tags — it causes every narration to play twice simultaneously.

### RULE 5: Code Blocks MUST Have `whiteSpace: 'pre'`
```tsx
// WRONG — indentation collapses
<div style={{ fontFamily: FONTS.mono, fontSize: 24 }}>

// CORRECT — indentation preserved
<div style={{ fontFamily: FONTS.mono, fontSize: 24, whiteSpace: 'pre' }}>
```
Also: terminal dot rows inside `whiteSpace: 'pre'` containers need `whiteSpace: 'normal'`.

### RULE 6: Never Import `@remotion/transitions/wipe`
The `wipe` subpath is not installed and silently kills compositions. Use `slide` from `@remotion/transitions/slide` instead.

### RULE 7: Icon/Emoji Divs MUST Have Explicit `color`
```tsx
// WRONG — renders black on dark background
<div style={{ fontSize: 28 }}>{item.icon}</div>

// CORRECT
<div style={{ fontSize: 28, color: item.color }}>{item.icon}</div>
```

### RULE 8: All Stacked Text Divs Need `display: 'block'`
```tsx
// WRONG — sibling divs collapse to one line in headless Chromium
<div style={{ fontSize: 24 }}>Line 1</div>
<div style={{ fontSize: 24 }}>Line 2</div>

// CORRECT
<div style={{ fontSize: 24, display: 'block' }}>Line 1</div>
<div style={{ fontSize: 24, display: 'block' }}>Line 2</div>
```
Parent `flexDirection: 'column'` is NOT sufficient. Each div needs its own `display: 'block'`.

### RULE 9: Always Clamp Interpolations
```tsx
// CORRECT — always include both clamp options
interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
})
```

### RULE 10: Phase Boundaries Must Cover Full Narration
`PHASE_END` fade-out must NOT start until the LAST word of that section finishes. Calculate: `PHASE_END = wordToFrame(lastWordEnd, OFFSET) + 30` (1s buffer).

### RULE 11: Minimum Font Size is 20px
YouTube requires all text to be readable. `fontSize: 14`, `fontSize: 16`, `fontSize: 18` — all too small. Minimum is 20px.

### RULE 12: `import React from 'react'` Required
Every TSX file that uses JSX must have `import React from 'react'` at the top.

---

## Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 3 (Audio) is `done`.
  - If not: STOP and report "Phase 3 (Audio) has not been completed."
- **Re-run check**: If Phase 4 is already `done`, note it but proceed (subagent mode always continues).

## Step 0: Read All Inputs From Disk

Before writing any code, read:

1. Find the plan file using this priority:
   - First, check for `.agents/plans/$ARGUMENTS.plan.md` (direct match by AnimationName)
   - If not found, glob `.agents/plans/*.plan.md` and find the file whose kebab-case name
     best matches `$ARGUMENTS` split on PascalCase boundaries
     (e.g., `ClaudeCodeDesktop` -> look for a file containing `claude-code-desktop`)
   - If still not found, STOP and report the error. Do NOT proceed without a plan.
   Store the resolved path as `PLAN_FILE` for all subsequent references.

2. Read timing constants:
   ```
   src/$ARGUMENTS/constants/timing.ts
   ```

3. Read all sync JSON files:
   ```bash
   ls src/$ARGUMENTS/scripts/*-sync.json
   ```
   Read each one to extract word timestamps.

4. Read the full script for scene context:
   ```
   src/$ARGUMENTS/scripts/full-script.md
   ```

5. **Read retention strategy (if present)**:
   ```
   src/$ARGUMENTS/retention-strategy.md
   ```
   If this file exists, load it as `RETENTION_STRATEGY`. You will look up each scene's
   prescription before writing that scene's TSX. If not present, continue with generic rules.

6. **Read Remotion best-practices skill (MANDATORY)**:
   Read the skill index first, then read EVERY rule file it lists:
   ```
   .claude/commands/remotion-best-practices/SKILL.md
   ```
   Then read ALL rule files under `.claude/commands/remotion-best-practices/rules/` — use glob to discover them:
   ```bash
   ls .claude/commands/remotion-best-practices/rules/*.md
   ```
   Read each `.md` file. These are the official Remotion best practices and MUST be applied to all generated code.
   Key rules to internalize before writing any scene:
   - `animations.md` — spring patterns, interpolation
   - `audio.md` — volume, trimming, speed
   - `compositions.md` — composition registration
   - `sequencing.md` — Sequence timing
   - `timing.md` — interpolation curves, springs
   - `transitions.md` — TransitionSeries patterns
   - `text-animations.md` — typography animation
   - `fonts.md` — font loading
   - `sfx.md` — sound effects
   - `voiceover.md` — TTS integration

   **Do NOT skip this step.** These rules are updated independently and may contain patterns not covered by the baked-in rules above.

**Do NOT proceed to Step 1 until all sources are read.**

---

## Step 1: Read Plan and Sync Data

From the plan, extract:
- Scene list (names, durations, visual descriptions)
- Color palette (primary, secondary, accent, background)
- Font choices
- Spring configurations
- Component requirements
- remotion_bits_components_used (if any)
- Transition selections

From timing.ts, extract:
- `SCENES` object (all scenes with start/duration)
- `TOTAL_FRAMES`, `FPS`, `TRANSITION_DURATION`
- `AUDIO_OFFSET_FIRST`, `AUDIO_OFFSET_REST`

From sync JSONs, extract:
- Word timestamps for each scene (for animation trigger frames)

---

## Step 1b: Generate AI Images (If Specified in Plan)

If the plan includes an `images:` section, create the manifest and generate images before building scenes.

### Create Image Manifest

Create `src/$ARGUMENTS/images/manifest.json` from plan specifications:

```json
{
  "composition": "$ARGUMENTS",
  "images": [
    {
      "name": "scene01-hero",
      "prompt": "<from plan>",
      "aspect_ratio": "16:9"
    }
  ]
}
```

### Generate Images

```bash
python generate-scene-images.py $ARGUMENTS
```

Output will be in `public/images/<animationname>/`.

If no images are specified in the plan, skip this step.

---

## Step 1c: Prepare Brand Logos & Person Photos

Scan ALL scene scripts for brand/company names and person names. For each:

### Brand Logos (MANDATORY for every company mention)

1. Check `src/shared/constants/brandLogos.ts` — use `BRAND_LOGOS.<key>` if available
2. If missing, download and add:
   ```bash
   curl -sL "https://github.com/<org>.png?size=128" -o "public/images/shared/logos/<brand>-logo.png"
   ```
3. Add entry to `src/shared/constants/brandLogos.ts`

### Person Photos (when a specific person is introduced by name)

```bash
curl -sL "https://github.com/<username>.png?size=256" -o "public/images/<comp>/<person>-photo.png"
```

In scenes, use:
```tsx
import { BRAND_LOGOS } from '../../shared/constants/brandLogos';
<Img src={staticFile(BRAND_LOGOS.openai)} style={{ width: 44, height: 44, objectFit: 'contain' }} />
```

**Rule**: Text-only company cards without logos look amateurish. Every brand mention in a scene card MUST have its real logo image.

---

## Step 2: Create Constants Using Theme System

Read the theme selection from the plan and create constants.

### Option A: Use a Preset Theme Directly

```typescript
// constants/colors.ts
import { vibrantTheme } from '../../shared/themes';
export const COLORS = vibrantTheme.colors;

// constants/fonts.ts
import { vibrantTheme } from '../../shared/themes';
export const FONTS = vibrantTheme.fonts;
export const FONT_WEIGHTS = vibrantTheme.fontWeights;

// constants/springs.ts
import { vibrantTheme } from '../../shared/themes';
export const SPRINGS = vibrantTheme.springs;
```

### Option B: Create Custom Theme with Overrides

```typescript
// constants/colors.ts
import { createTheme, extendColors } from '../../shared/themes';

const theme = createTheme({
  name: 'my-video',
  colors: {
    primary: '#B604D4',
    secondary: '#D94FE8',
    accent: '#10B981',
  },
});

export const COLORS = extendColors(theme.colors, {
  brandOrange: '#FF9900',
});
```

### Option C: Full Custom (Legacy Pattern)

```typescript
// constants/springs.ts
export const SPRINGS = {
  entrance: { damping: 12, stiffness: 100, mass: 0.5 },
  smoothSlide: { damping: 15, stiffness: 80, mass: 0.8 },
  bouncy: { damping: 8, stiffness: 120, mass: 0.4 },
  gentle: { damping: 20, stiffness: 60, mass: 1.0 },
  snappy: { damping: 14, stiffness: 200, mass: 0.3 },
  exit: { damping: 18, stiffness: 90, mass: 0.6 },
};
```

### Step 2d: Create bits-theme.ts (If Plan Uses remotion-bits Components)

```typescript
// constants/bits-theme.ts
import { createBitsThemeVars } from '../../shared/themes/bits-bridge';
import { COLORS } from './colors';

export const BITS_THEME_VARS = createBitsThemeVars(COLORS);
```

Apply in Composition.tsx root:
```tsx
<AbsoluteFill style={{ ...BITS_THEME_VARS, backgroundColor: COLORS.background }}>
```

---

## Step 2b: Build Scene00Preview Component (MANDATORY)

Every video MUST have a Scene00Preview built FIRST. This "In this video..." preview hook increases watch time by 32%.

### Scene00Preview Pattern

```typescript
/**
 * Scene00Preview - "In this video..." teaser
 * Duration: 10-15 seconds (300-450 frames)
 * Synced to scene00-sync.json word-level timestamps.
 * Audio starts at frame AUDIO_OFFSET_PREVIEW.
 */

import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { COLORS } from '../constants/colors';
import { SPRINGS } from '../constants/springs';
import { AUDIO_OFFSET_PREVIEW } from '../constants/timing';

export const Scene00Preview: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const audioFrame = frame - AUDIO_OFFSET_PREVIEW;

  // Phases based on audio sync timestamps
  const PHASE1_END = 75;
  const PHASE2_END = 155;
  const PHASE3_END = 215;
  const PHASE4_END = 295;

  const phase1Opacity = interpolate(audioFrame, [0, 5, 60, 75], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  // ... similar for phases 2-5

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {/* Phase 1: Attention grab */}
      {phase1Opacity > 0 && <Phase1Content opacity={phase1Opacity} frame={audioFrame} fps={fps} />}
      {/* Phase 2-5: Teasers + CTA */}
    </AbsoluteFill>
  );
};
```

### Preview Animation Principles

1. **Rapid Visual Changes**: Every 10-15 frames (0.3-0.5s) for maximum energy
2. **Overlapping Transitions**: Phases fade out while next phase fades in (no black gaps)
3. **Scale Pops**: Elements scale 0 → 1.1 → 1.0 on entrance (high stiffness spring)
4. **Large Typography**: 280px for stats, 72px for text
5. **"Upcoming" Badge**: Top-left corner with pulsing indicator

---

## Step 2c: Create Scaffold Composition (For Per-Scene Validation)

Create a minimal scaffold so that `remotion still` works for per-scene validation:

```typescript
// src/$ARGUMENTS/Composition.tsx (SCAFFOLD — upgraded in Step 5)
import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { COLORS } from './constants/colors';
import { $ARGUMENTS as $ARGUMENTSComposition } from './$ARGUMENTS/Composition';

export const $ARGUMENTS: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {/* Scenes added incrementally during Step 4 */}
    </AbsoluteFill>
  );
};
```

### Register in Root.tsx

```typescript
import { $ARGUMENTS } from './$ARGUMENTS/Composition';
import { TOTAL_FRAMES } from './$ARGUMENTS/constants/timing';

<Composition
  id="$ARGUMENTS"
  component={$ARGUMENTS}
  durationInFrames={TOTAL_FRAMES}
  fps={30}
  width={1920}
  height={1080}
/>
```

### Verify Scaffold Renders

```bash
pnpm exec remotion still $ARGUMENTS out/$ARGUMENTS/validate/scaffold.png --frame=0
```

---

## Step 3: Build Reusable Components

Create components defined in the plan under `components/`:
- `SceneBackground.tsx` — consistent scene wrapper with gradient
- Visual components as specified (terminals, diagrams, icons, etc.)

Follow Remotion best practices:
- Components receive `startFrame` props for animation triggers
- Use `useCurrentFrame()` + `interpolate()` / `spring()` internally
- Always clamp interpolations (RULE 9 above)
- Pass `fps` explicitly to `spring()`: `spring({ frame, fps: 30, config })`

---

## Step 4: Build Scene Components (With Per-Scene Validation)

**Loop**: For each scene in the plan:

0. **Lookup retention strategy** — If `RETENTION_STRATEGY` was loaded, find the section for this scene (e.g., `### SceneNN`). Read the Components table and SpotlightFocus timing block. These override generic rules for this scene.
1. **Create** `scenes/SceneNN<Name>.tsx` — apply retention prescriptions from step 0
2. **Import into scaffold** — Add to `Composition.tsx` inside `<Sequence>`:
   ```typescript
   <Sequence from={SCENES.<sceneName>.start} durationInFrames={SCENES.<sceneName>.duration}>
     <SceneNN<Name> />
   </Sequence>
   ```
3. **Validate** — Run `/validate-scene $ARGUMENTS SceneNN`
4. **Fix if needed** — Fix and re-validate before next scene
5. **Next scene** — Move on only after validation passes

After all scenes are built, apply global Composition.tsx elements from the strategy's **Global Elements** section (SlimProgressBar, ProgressDots, MidVideoReHook). These are added as AbsoluteFill overlays OUTSIDE TransitionSeries.

### The Sync Formula

```typescript
// For each word in the sync JSON:
// scene_frame = word.start_seconds * 30 + audio_offset
// audio_offset = 30 for scene 1 (AUDIO_OFFSET_FIRST), 20 for scenes 2+ (AUDIO_OFFSET_REST)
```

### Animation Pattern

Comment the sync source at the top of each scene:

```typescript
/**
 * Synced to sceneNN-sync.json word-level timestamps.
 * Audio starts at scene frame <offset>. Formula: seconds * 30 + <offset> = frame.
 *
 *   "keyword1"    X.XXXs → frame NN
 *   "keyword2"    X.XXXs → frame NN
 */
```

For each visual beat:

```typescript
const frame = useCurrentFrame();
const fps = 30;

// "Docker" at 1.2s → frame 56 (with offset 20)
const dockerOpacity = interpolate(frame, [54, 70], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
const dockerScale = spring({ frame: frame - 54, fps, config: SPRINGS.entrance });
```

### Using remotion-bits Wrappers

If the plan includes `remotion_bits_components_used`, import from the WRAPPER, not directly:

```typescript
// CORRECT — audio-synced wrapper
import { SyncedAnimatedText, SyncedCodeBlock, SyncedStaggeredMotion } from '../../shared/components/bits';
import { wordToFrame } from '../../shared/utils/cleanSyncData';

// WRONG — bypasses audio sync
import { AnimatedText } from 'remotion-bits';
```

**Exception**: `TypeWriter`, `AnimatedCounter`, `GradientTransition`, `MatrixRain` — direct import from `remotion-bits` is fine (no sync needed).

### CRITICAL: Avoid Overlapping Elements

**Phase-Based Rendering** (preferred for complex scenes):
```typescript
const PHASE1_END = 120;
const PHASE2_END = 240;

const isPhase1 = frame < PHASE1_END;
const isPhase2 = frame >= PHASE1_END && frame < PHASE2_END;
const isPhase3 = frame >= PHASE2_END;

{isPhase1 && <ContentA />}
{isPhase2 && <ContentB />}
{isPhase3 && <ContentC />}
```

**Architecture Diagrams**: Render arrows BEFORE boxes in component tree (z-index order):
```tsx
<AbsoluteFill>
  {/* Layer 1: Arrows (z-index lower) */}
  <svg style={{ position: 'absolute', width: '100%', height: '100%', zIndex: 0 }}>
    {connections.map(conn => <Arrow key={conn.id} from={conn.from} to={conn.to} />)}
  </svg>
  {/* Layer 2: Boxes (z-index higher) */}
  {boxes.map(box => <DiagramBox key={box.id} {...box} style={{ zIndex: 1 }} />)}
</AbsoluteFill>
```

---

## Step 5: Upgrade Scaffold to Final Composition.tsx

The scaffold from Step 2c already imports all scenes in `<Sequence>` wrappers. Now upgrade to `TransitionSeries`, audio layers, SFX, BrandWatermark, and OutroSequence.

### Read Transition Selection from Plan

```yaml
transitions:
  primary:
    id: slide-left
  accent:
    id: fade
```

### Complete Composition Template

```typescript
import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { BrandWatermark, OutroSequence } from '../shared/components';
import { SCENES, TRANSITION_DURATION, OUTRO_DURATION } from './constants/timing';
// ... scene imports

const t = TRANSITION_DURATION;

const TRANSITIONS = {
  primary: slide({ direction: 'from-left' }),
  accent: fade(),
  primarySfx: 'sfx/final/scene/wipe-left.mp3',
  accentSfx: 'sfx/final/intro-outro/glitch-in.mp3',
};

const AUDIO_FILES = [
  { src: 'audio/<name>/scene00.mp3', from: SCENES.preview.start + AUDIO_OFFSET_PREVIEW },
  { src: 'audio/<name>/scene01.mp3', from: SCENES.hook.start + AUDIO_OFFSET_FIRST },
  { src: 'audio/<name>/scene02.mp3', from: SCENES.<second>.start + AUDIO_OFFSET_REST },
  // ... continue for all scenes (offset AUDIO_OFFSET_REST for scenes 2+)
];

const TRANSITION_SFX = [
  { src: TRANSITIONS.accentSfx, from: SCENES.preview.start + SCENES.preview.duration - 5 },
  { src: TRANSITIONS.primarySfx, from: SCENES.hook.start + SCENES.hook.duration - 5 },
  // ... continue for all scenes
];

export const <AnimationName>: React.FC = () => {
  return (
    <AbsoluteFill>
      <TransitionSeries>
        {/* NO + t in durationInFrames — RULE 2 */}
        <TransitionSeries.Sequence durationInFrames={SCENES.preview.duration}>
          <Scene00Preview />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={TRANSITIONS.accent}
          timing={linearTiming({ durationInFrames: t })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENES.hook.duration}>
          <Scene01Hook />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={TRANSITIONS.primary}
          timing={linearTiming({ durationInFrames: t })}
        />

        {/* ... continue for all scenes ... */}

        {/* MANDATORY: Outro — always uses fade */}
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />
        <TransitionSeries.Sequence durationInFrames={OUTRO_DURATION}>
          <OutroSequence />
        </TransitionSeries.Sequence>
      </TransitionSeries>

      {/* MANDATORY: Background music — use per-video track if exists, else shared fallback */}
      {/* Check: public/audio/<animationname>/bg-music.mp3 exists? Use it. Otherwise: audio/shared/bg-music.wav */}
      <Audio src={staticFile('audio/<name>/bg-music.mp3')} volume={0.08} />

      {/* Audio narration */}
      {AUDIO_FILES.map(({ src, from }) => (
        <Sequence key={src} from={from}>
          <Audio src={staticFile(src)} />
        </Sequence>
      ))}

      {/* Transition SFX */}
      {TRANSITION_SFX.map(({ src, from }, idx) => (
        <Sequence key={`sfx-${idx}`} from={from} durationInFrames={30}>
          <Audio src={staticFile(src)} volume={0.7} />
        </Sequence>
      ))}

      {/* MANDATORY: Brand watermark */}
      <BrandWatermark />
    </AbsoluteFill>
  );
};
```

### Transition Assignment Rules

1. **Hook entrance** (Scene 0 → 1): Always use **accent** transition
2. **Middle scenes** (Scene 1 → N-1): Always use **primary** transition
3. **CTA entrance** (Scene N-1 → CTA): Always use **accent** transition
4. **Outro** (CTA → Outro): Always use **fade**

### Mandatory Elements Checklist

Every composition MUST include:
1. **OutroSequence** — The branded outro (8s / 240 frames) as the final sequence
2. **Background music** — Check if `public/audio/<animationname>/bg-music.mp3` exists (generated via `generate-bg-music.py`). If yes, use `audio/<animationname>/bg-music.mp3`. Otherwise fall back to `audio/shared/bg-music.wav`. Volume 0.08.
3. **BrandWatermark** — Logo with corner cycling
4. **Transition SFX** — Audio synced to each scene transition (volume 0.7)

---

## Step 6: Verify Root.tsx Registration

Verify the composition is registered in `src/Root.tsx`. The scaffold step should have added it, but verify:
- Import is present
- `<Composition>` entry exists with correct `id`, `durationInFrames`, `fps`, `width`, `height`

---

## Step 7: Apply Remotion Best Practices (from skill loaded in Step 0.6)

You loaded the full `remotion-best-practices` skill rules in Step 0.6. Now apply them as a final review pass on ALL generated code. Key checks:

### From the skill rules — verify every file against:
- **`animations.md`**: Springs have explicit `fps`, config is flat object, `durationRestThreshold: 0.001`
- **`timing.md`**: All `interpolate()` calls have `extrapolateLeft/Right: 'clamp'`
- **`compositions.md`**: `<Composition>` has correct `id`, `fps`, `width`, `height`, `durationInFrames`
- **`audio.md`**: No `<Audio>` inside scenes, volume uses callback form `volume={() => 0.3}`
- **`sequencing.md`**: `<Sequence>` timing is correct, no overlapping ranges
- **`transitions.md`**: TransitionSeries patterns match current API
- **`fonts.md`**: Fonts loaded correctly, no CSS shorthand in `fontFamily`
- **`sfx.md`**: SFX volume hard cap 0.25 (typical 0.10-0.15, ~12-18 dB below narration), proper placement
- **`text-animations.md`**: Typography patterns applied correctly

### Additional project-specific checks:
- Replace `Math.random()` with `import { random } from 'remotion'` + seed string
- No `Date.now()` or `new Date()` in render functions
- Use `staticFile()` for all assets — no inline `require()` or dynamic imports
- remotion-bits: use wrappers from `../../shared/components/bits` (NEVER direct import)
- Apply `BITS_THEME_VARS` on root `<AbsoluteFill>` if bits components are used

If any rule from the skill conflicts with the project-specific rules in this agent (Rules 1-12 above), the **project-specific rule wins** — it's tuned for this codebase.

---

## Step 8: Generate QA Frames (MANDATORY)

Generate `src/$ARGUMENTS/qa-frames.json` with intelligent frame selections.

```json
{
  "compositionId": "$ARGUMENTS",
  "generatedAt": "<ISO timestamp>",
  "frames": [
    {
      "frame": 0,
      "scene": "preview",
      "reason": "scene-start",
      "description": "Preview scene entry — validate background renders"
    },
    {
      "frame": 144,
      "scene": "preview",
      "reason": "peak-content",
      "description": "Preview hook — all teasers visible"
    },
    {
      "frame": <SCENES.hook.start + 30>,
      "scene": "hook",
      "reason": "animation-cluster",
      "description": "Hook scene — after audio offset, first animations triggered"
    }
    // ... continue for each scene, 3-4 frames per scene
  ]
}
```

**Frame selection strategy** (3-4 per scene):
1. `scene.start` — Entry frame (validate transition clean-up)
2. `scene.start + AUDIO_OFFSET` — After audio starts (first animation should be visible)
3. `scene.start + scene.duration / 2` — Mid-scene peak content
4. `scene.start + scene.duration - TRANSITION_DURATION - 5` — Before exit (all content visible)

---

## Step 9: Final Verification

Run these checks:

```bash
# TypeScript check
pnpm run lint
```

Also verify manually:
- [ ] `qa-frames.json` exists with intelligent frame selections
- [ ] `Composition.tsx` contains `<OutroSequence`
- [ ] `Composition.tsx` contains `<BrandWatermark`
- [ ] `timing.ts` includes `outro` scene with 240 frames duration
- [ ] No `+ TRANSITION_DURATION` in any `durationInFrames` in `Composition.tsx`
- [ ] No `<Audio>` in any scene component files
- [ ] All scene files have `import React from 'react'`

---

## Output Contract

After completing all steps, return to main context:

```
Phase 4 Complete: <AnimationName>

## Scene Inventory
| Scene | File | Lines | Validate |
|-------|------|-------|----------|
| Scene00Preview | scenes/Scene00Preview.tsx | ~400 | ✅ PASS |
| Scene01Hook | scenes/Scene01Hook.tsx | ~350 | ✅ PASS |
| Scene02Solution | scenes/Scene02Solution.tsx | ~420 | ✅ PASS |
| ... | ... | ... | ... |
| Composition | Composition.tsx | ~180 | N/A |

## Components Created
- SceneBackground.tsx
- [Other components from plan]

## Constants Created
- timing.ts ✅
- colors.ts ✅
- fonts.ts ✅
- springs.ts ✅

## QA Frames
- qa-frames.json: N frames across M scenes

## Validation Summary
X/Y scenes passed validate-scene. Validate reports: out/<AnimationName>/validate-*.md

[If any FAIL:]
❌ BLOCKED: Scene03 failed validation — 1 critical issue
  • Font size 14px at line 87 — fix before render
  Full report: out/<AnimationName>/validate-Scene03.md
```

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `4 - Sync` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template in individual phase commands).

Do NOT return TSX code in the summary. File paths and status only.
