---
description: "Phase 4: Build Remotion scenes with animation keyframes synced to word timestamps"
argument-hint: <AnimationName (folder name under src/)>
---

> **Context Tip**: In full-auto-v2 workflows, Phase 4 runs as the `phase4-scene-builder`
> subagent (Task tool) to isolate its ~9,000-line output from the main context.
> This command (`phase4-sync.md`) is for **standalone/debug use only** — run it directly
> when you need to build or rebuild scenes interactively with inline output visible.

<objective>
Execute Phase 4 of the DIY YouTube Video Creation Workflow.
Build the complete Remotion composition for "$ARGUMENTS" with animations precisely synced to the word-level timestamps from Phase 3.

**Goal**: Create React components where every visual element appears/animates exactly when the corresponding word is spoken.
**Input**:
  - Plan file from Phase 1 (see Plan File Discovery in Step 1)
  - `src/$ARGUMENTS/scripts/sceneNN-sync.json` (word timestamps from Phase 3)
  - `src/$ARGUMENTS/constants/timing.ts` (scene durations from Phase 3)
**Output**: Complete `src/$ARGUMENTS/` with all components, scenes, and composition
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 4)
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 3 (Audio) is `done`.
  - If not: STOP and report "Phase 3 (Audio) has not been completed. Run `/diy-yt-creation:phase3-audio $ARGUMENTS` first."
- **Re-run check**: If Phase 4 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Read Plan and Sync Data

### Plan File Discovery

Locate the plan file using this priority:
1. `.agents/plans/$ARGUMENTS.plan.md` (direct match by AnimationName)
2. If not found, glob `.agents/plans/*.plan.md` and find the file whose kebab-case name
   best matches $ARGUMENTS split on PascalCase boundaries
   (e.g., `ClaudeCodeDesktop` -> look for a file containing `claude-code-desktop`)
3. If still not found, STOP and ask the user for the plan file path. Do NOT proceed without a plan.

Store the resolved path as `PLAN_FILE` for all subsequent references.

1. Read `PLAN_FILE` for visual design specs
2. Read all `sceneNN-sync.json` files for word timestamps
3. Read `constants/timing.ts` for scene durations and starts
4. **Read Remotion best-practices skill (MANDATORY)**: Read `.claude/commands/remotion-best-practices/SKILL.md`, then glob and read ALL `.md` files under `.claude/commands/remotion-best-practices/rules/`. These are the official Remotion patterns — apply them to all generated code. Project-specific rules in this command take precedence on conflicts.

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

### Use in Scenes

```tsx
import { Img, staticFile } from 'remotion';

<Img
  src={staticFile('images/<animationname>/scene01-hero.png')}
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>
```

If no images are specified in the plan, skip this step.

## Step 1c: Capture Screenshots (If Specified in Plan)

If the plan includes a `screenshots:` section, create the manifest and capture real website screenshots before building scenes.

### Create Screenshot Manifest

Create `src/$ARGUMENTS/images/screenshots.json` from plan specifications:

```json
{
  "composition": "$ARGUMENTS",
  "defaults": {
    "viewport": [1920, 1080],
    "color_scheme": "dark",
    "wait_strategy": "networkidle",
    "delay_after_load_ms": 1500
  },
  "screenshots": [
    {
      "name": "<from plan>",
      "url": "<from plan>",
      "scene": "<from plan>",
      "usage": "<from plan>",
      "color_scheme": "<from plan, default dark>"
    }
  ]
}
```

Optional fields per entry: `full_page`, `scroll_to_selector`, `dismiss_selectors`, `eval_before`, `wait_for_selector`.

### Capture Screenshots

```bash
python capture-screenshots.py $ARGUMENTS
```

Output will be in `public/images/<animationname>/`.

### Verify Captures

Check script output summary:
- Each file should be >10KB (not blank)
- Default dimensions are 1920x1080 (matches video canvas)
- No cookie banners or popups visible in captures

### Handle Failures

If any screenshots fail to capture (auth wall, anti-bot, CAPTCHA):
1. Note the failure in the build log
2. Continue building scenes — use a styled placeholder card for missing screenshots
3. The user can manually capture later via `/capture-screenshot <url> --composition $ARGUMENTS`

### Use in Scenes

Same as AI images:
```tsx
import { Img, staticFile } from 'remotion';

<Img
  src={staticFile('images/<animationname>/github-repo-hero.png')}
  style={{
    width: '85%',
    borderRadius: 12,
    border: '2px solid rgba(255,255,255,0.1)',
    boxShadow: '0 20px 60px rgba(0,0,0,0.5), 0 0 60px rgba(99,102,241,0.15)',
    objectFit: 'contain',
  }}
/>
```

If no screenshots are specified in the plan, skip this step.

## Step 2: Create Constants Using Theme System

Read the theme selection from the plan and create constants using the shared theme system.

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

// Create theme with custom colors from plan
const theme = createTheme({
  name: 'my-video',
  colors: {
    primary: '#B604D4',    // From plan
    secondary: '#D94FE8',  // From plan
    accent: '#10B981',     // From plan
  },
});

// Add composition-specific colors if needed
export const COLORS = extendColors(theme.colors, {
  brandOrange: '#FF9900',
  partnerBlue: '#0078D4',
});

// constants/fonts.ts and springs.ts similar pattern
```

### Option C: Full Custom (Legacy Pattern)

If the plan specifies completely custom values not fitting any theme, create constants manually:
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

// IMPORTANT: durationRestThreshold is a spring() call parameter, not a SpringConfig property.
// Always pass it to eliminate the visible ~0.5% animation gap at spring end:
//   spring({ frame, fps, config: SPRINGS.entrance, durationRestThreshold: 0.001 })
// The default (0.005) leaves a perceptible gap. 0.001 ensures full completion.
export const SPRING_REST_THRESHOLD = 0.001;
```

**Preference**: Use Option A or B when possible for consistency and reduced duplication.

### Step 2d: Create bits-theme.ts (If Plan Uses remotion-bits Components)

If the plan specifies `remotion_bits_components_used`, create a theme bridge file:

```typescript
// constants/bits-theme.ts
import { createBitsThemeVars } from '../../shared/themes/bits-bridge';
import { COLORS } from './colors';

export const BITS_THEME_VARS = createBitsThemeVars(COLORS);
```

Then apply in Composition.tsx on the root `<AbsoluteFill>`:
```tsx
import { BITS_THEME_VARS } from './constants/bits-theme';

<AbsoluteFill style={{ ...BITS_THEME_VARS, backgroundColor: COLORS.background }}>
```

## Step 2b: Build Scene00Preview Component (MANDATORY)

Every video MUST have a Scene00Preview component built BEFORE other scenes. This "In this video..." preview hook increases watch time by 32%.

### Scene00Preview Component Pattern

Preview hooks use rapid phase-based rendering with visual changes every 10-15 frames:

```typescript
/**
 * Scene00Preview - "In this video..." teaser
 * Duration: 10-15 seconds (300-450 frames)
 * Visual changes every 10-15 frames for maximum energy
 *
 * Synced to scene00-sync.json word-level timestamps.
 * Audio starts at frame AUDIO_OFFSET_PREVIEW.
 */

import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { COLORS } from '../constants/colors';
import { SPRINGS } from '../constants/springs';
import { AUDIO_OFFSET_PREVIEW } from '../constants/timing';
import { SceneBackground } from '../components/SceneBackground';
import { StarburstBackground } from '../../shared/components';

export const Scene00Preview: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Audio-synced frame (minimal offset for preview energy)
  const audioFrame = frame - AUDIO_OFFSET_PREVIEW;

  // Define phases based on audio sync timestamps
  // Phases should overlap slightly for smooth transitions
  const PHASE1_END = 75;   // Attention grab (~2.5s)
  const PHASE2_END = 155;  // Teaser 1 (~5s)
  const PHASE3_END = 215;  // Teaser 2 (~7s)
  const PHASE4_END = 295;  // Teaser 3 (~9.5s)
  // Phase 5 is CTA to end

  // Each phase has fade in, hold, fade out
  const phase1Opacity = interpolate(audioFrame, [0, 5, 60, 75], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const phase2Opacity = interpolate(audioFrame, [60, 70, 140, 155], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  // ... similar for phases 3-5

  return (
    <AbsoluteFill>
      <SceneBackground variant="primary" showGlow glowIntensity={0.4} />

      {/* MANDATORY: StarburstBackground for Scene00Preview energy */}
      <StarburstBackground
        rays={12}
        colors={[COLORS.primary, COLORS.secondary]}
        rotationSpeed={0.3}
        opacity={0.12}
        smoothness={0.8}
      />

      {/* "UPCOMING" badge - visible during phases 1-4, fades before CTA */}
      <UpcomingBadge opacity={upcomingOpacity} />

      {/* Phase 1: MASSIVE STAT - Pattern Interrupt */}
      <Phase1Content opacity={phase1Opacity} frame={audioFrame} fps={fps} />

      {/* Phase 2: Teaser 1 */}
      {audioFrame >= 60 && <Phase2Content opacity={phase2Opacity} frame={audioFrame - 60} fps={fps} />}

      {/* ... Phases 3-4 ... */}

      {/* Phase 5: CTA "Let's dive in" */}
      <CTAContent opacity={ctaOpacity} frame={audioFrame - 288} fps={fps} />
    </AbsoluteFill>
  );
};
```

### Preview Animation Principles

1. **Rapid Visual Changes:** Every 10-15 frames (0.3-0.5s) for maximum energy
2. **Overlapping Transitions:** Phases fade out while next phase fades in (no black gaps)
3. **Scale Pops:** Elements scale 0 → 1.1 → 1.0 on entrance using spring with high stiffness
4. **Pulsing Glow:** Use `Math.sin(frame * 0.15)` for breathing glow effects on stats
5. **Large Typography:** 280px for stats, 72px for text — this is the attention grab
6. **"Upcoming" Badge:** Top-left corner with pulsing indicator, fades out before CTA

### Preview Spring Config

```typescript
// High energy springs for preview
const PREVIEW_SPRINGS = {
  slamIn: { damping: 10, stiffness: 200, mass: 0.8 },  // Fast, punchy entrance
  pop: { damping: 12, stiffness: 100, mass: 0.5 },     // Scale pop
  bouncy: { damping: 8, stiffness: 120, mass: 0.4 },   // CTA bounce
};
```

### Reference Implementation

See `src/AIDevProductivity/scenes/Scene00Preview.tsx` for the complete reference implementation with all animation patterns.

## Step 2b.5: Build Cinematic Hook Scene (Scene01Hook) — MANDATORY

Every video MUST have a cinematic hook that goes beyond basic text-on-screen. Read the **cinematic hook blueprint** from the plan file (`.agents/plans/$ARGUMENTS.plan.md` → `cinematic_hook_blueprint:` section).

### Hook Blueprint Inputs

1. **Pattern** — `FilmTrailer`, `ContrastPivot`, `StatCascade`, `RackFocusReveal`, `TerminalHacker`, or `SplitScreenDuel`
2. **Visual beats** — ordered list of animation phases with spring types and SFX
3. **Pivot word** — the exact word in sync JSON that triggers the pivot moment
4. **Brand reveal word** — the word where the product/brand name appears
5. **Assets needed** — portraits, logos, screenshots, videos
6. **Music profile** — BPM range for beat alignment (from `public/audio/<name>/bg-music-metadata.json`)

If no blueprint exists in the plan, default to **ContrastPivot** pattern.

### Spring Presets

Import from `src/shared/constants/hookSprings.ts`:

```typescript
import { HOOK_SPRINGS, HOOK_SFX } from '../../shared/constants/hookSprings';
import { SPRING_REST_THRESHOLD } from '../../shared/components/retention';

// Use preset by name from blueprint:
spring({ frame: frame - triggerFrame, fps, config: HOOK_SPRINGS.heavy, durationRestThreshold: SPRING_REST_THRESHOLD })
spring({ frame: frame - pivotFrame, fps, config: HOOK_SPRINGS.slam, durationRestThreshold: SPRING_REST_THRESHOLD })
```

### Beat Alignment (Optional — When bg-music-metadata.json Exists)

If `public/audio/<name>/bg-music-metadata.json` exists, read the hook BPM and snap impact frames:

```typescript
import { alignToDownbeat } from '../../shared/utils/beatAlignment';

// Read BPM from metadata (Phase 3.2 output)
const HOOK_BPM = 100; // from bg-music-metadata.json hook.bpm

// Snap pivot and reveal to nearest downbeat
const PIVOT_FRAME = alignToDownbeat(wordToFrame(pivotTimestamp, AUDIO_OFFSET), HOOK_BPM as any);
const REVEAL_FRAME = alignToDownbeat(wordToFrame(revealTimestamp, AUDIO_OFFSET), HOOK_BPM as any);
```

This is OPTIONAL polish — if metadata doesn't exist, use raw `wordToFrame()` values.

### Pattern Templates

Each pattern follows a specific visual structure. The hook scene file (`scenes/Scene01Hook.tsx`) implements the selected pattern.

#### FilmTrailer Pattern

```
Phase 1 — Cold Open → Context (0 → PIVOT_FRAME):
├── [0 → AUDIO_OFFSET] Pure black silence (tension)
├── [AUDIO_OFFSET → CARD1_END] Title card: HOOK_SPRINGS.heavy, fade in/hold/fade out
├── [CARD1_END → PIVOT-6] Context bg: gradient + screenshot/visual at low opacity
│   ├── Sequential text springs synced to word timestamps (HOOK_SPRINGS.snappy)
│   ├── Vignette tightens: radial-gradient transparent% interpolates 55→40
│   └── Final context line: HOOK_SPRINGS.slam (scale 1.3→1.0)
└── [PIVOT-6 → PIVOT] White flash smash cut: 6-frame interpolation [0→1→0]

Phase 2 — PIVOT → Reveal (PIVOT_FRAME → FEATURE_START):
├── [PIVOT] Triple SFX: HOOK_SFX.pivot (impact-slam + screen-shake + glitch-zap)
├── [PIVOT → PIVOT+8] Pivot word in 200-240px accent color, holds 6-8 frames
│   ├── GlitchInterrupt(triggerFrame=PIVOT, duration=4)
│   └── ScreenShake(triggerFrame=PIVOT, intensity=5, duration=5)
├── [PIVOT+10 → REVEAL] Portrait/logo reveal:
│   ├── Main visual fills 40-50% of screen (spring fade-in 20 frames)
│   ├── Supporting elements stagger in (HOOK_SPRINGS.stagger, +8 frame intervals)
│   └── Text reveals synced to narration timestamps
└── [REVEAL] Brand name: HOOK_SPRINGS.reveal (scale 0.7→1.0)
    ├── Accent color with textShadow glow
    ├── ScreenShake(triggerFrame=REVEAL, intensity=8, duration=10)
    └── SFX: HOOK_SFX.brandReveal

Phase 3 — Rapid-Fire → CTA (FEATURE_START → SCENE_END):
├── [BG] Screenshot/visual at 15% opacity as subtle backdrop
├── Feature cards: Each cycles every ~80-120 frames
│   ├── Scale: HOOK_SPRINGS.slam (1.4→1.0)
│   ├── Opacity: fade in over 8 frames
│   └── Only active card visible (find latest triggered)
├── [LAUNCH] Announcement badges: green/purple bg, spring-in
└── [CTA] Final line: 64px white, centered, fade to black
    └── 4-keyframe fade-out: [start, start+14, SCENE_DUR-24, SCENE_DUR] → [0,1,1,0]
```

#### ContrastPivot Pattern

```
Phase 1 — Context Build (0 → PIVOT_FRAME):
├── [0 → AUDIO_OFFSET] Pure black or gradient bg
├── Sequential evidence elements: stats, quotes, examples
│   └── Each springs in with HOOK_SPRINGS.snappy
└── Tension builds with vignette/darkening

Phase 2 — PIVOT + Contrarian Reveal (PIVOT_FRAME → EVIDENCE_START):
├── [PIVOT] Smash cut: white flash + GlitchInterrupt + ScreenShake
├── [PIVOT → PIVOT+8] "BUT." in accent color, holds then fades
└── [PIVOT+15 → REVEAL] Contrarian claim springs in (HOOK_SPRINGS.reveal)

Phase 3 — Evidence + CTA (EVIDENCE_START → SCENE_END):
├── Supporting points: staggered list items synced to narration
└── CTA: action statement with 4-keyframe fade-out
```

#### StatCascade Pattern

```
Phase 1 — Stat Slams (0 → CONTEXT_START):
├── Stat 1: Hero number (160px+), HOOK_SPRINGS.slam (scale 1.4→1.0)
│   └── ScreenShake on impact
├── Stat 2: Second number, same slam pattern
└── Stat 3: Third number, biggest shake

Phase 2 — Context (CONTEXT_START → CTA_START):
├── "What does this mean?" — HOOK_SPRINGS.gentle
└── Explanation text synced to narration

Phase 3 — CTA (CTA_START → SCENE_END):
└── Promise statement with 4-keyframe fade-out
```

### Cinematic Techniques Checklist

Every hook scene MUST include these techniques:

- [ ] **Spring physics variation** — At least 3 different HOOK_SPRINGS presets used (not all the same spring)
- [ ] **Smash cut at pivot** — White flash overlay (6-frame interpolation [0→1→0]) at the pivot word
- [ ] **Triple SFX at pivot** — GlitchInterrupt + ScreenShake + impact-slam all fire simultaneously
- [ ] **ScreenShake at brand reveal** — Second shake at the key reveal moment (higher intensity than pivot)
- [ ] **Vignette dynamics** — Radial gradient that tightens during tension phases
- [ ] **4-keyframe fade-out on last phase** — Prevents text overlap with next scene during transition
- [ ] **Phase-based rendering** — All content gated by `{isPhaseN && ...}` conditionals
- [ ] **Minimum 75 frames reading time** — Last content trigger has 75+ frames before scene ends
- [ ] **All text has explicit `color`** — No browser-default black text on dark backgrounds

### SFX Integration

The hook's SFX entries go in Composition.tsx, NOT in the scene component. Map blueprint SFX presets to Composition audio:

```typescript
// In Composition.tsx — Hook SFX section
// Smash cut at context entrance
<Sequence from={SCENES.hook.start + SMASH_CUT_FRAME} durationInFrames={30}>
  <Audio src={staticFile(HOOK_SFX.smashCut.src)} volume={HOOK_SFX.smashCut.vol} />
</Sequence>

// Triple SFX at pivot
{HOOK_SFX.pivot.map((sfx, i) => (
  <Sequence key={i} from={SCENES.hook.start + PIVOT_FRAME} durationInFrames={30}>
    <Audio src={staticFile(sfx.src)} volume={sfx.vol} />
  </Sequence>
))}

// Brand reveal slam
<Sequence from={SCENES.hook.start + REVEAL_FRAME} durationInFrames={30}>
  <Audio src={staticFile(HOOK_SFX.brandReveal.src)} volume={HOOK_SFX.brandReveal.vol} />
</Sequence>
```

### Background Music Integration

If multi-segment music exists (`public/audio/<name>/bg-music-hook.mp3`), use dynamic volume curves:

```typescript
{/* Hook music — energetic, fades in/out */}
<Sequence from={0} durationInFrames={SCENES.hook.duration}>
  <Audio
    src={staticFile(`audio/${name}/bg-music-hook.mp3`)}
    volume={(f) => interpolate(
      f, [0, 15, SCENES.hook.duration - 45, SCENES.hook.duration],
      [0, 0.12, 0.12, 0],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    )}
  />
</Sequence>
```

If only single-track music exists (`bg-music.mp3`), limit it to hook + first scene:

```typescript
<Sequence from={0} durationInFrames={SCENES.scene02.start}>
  <Audio src={staticFile(`audio/${name}/bg-music.mp3`)} volume={0.10} />
</Sequence>
```

### Reference Implementation

See `src/ArchonOverview/hooks/HookVariant7.tsx` for the complete FilmTrailer pattern reference (651 lines, 3 phases, 6 SFX triggers, spring physics variation, smash cuts, vignette dynamics).

### Validate Hook Scene

After building the hook scene, run:
```bash
/validate-scene $ARGUMENTS Scene01
```

## Step 2c: Create Scaffold Composition (For Per-Scene Validation)

Create a minimal scaffold `Composition.tsx` so that `remotion still` works for per-scene validation during Step 4. This scaffold uses simple `<Sequence>` wrappers — it gets upgraded to `TransitionSeries` in Step 5.

### Create Scaffold Composition

```typescript
// src/$ARGUMENTS/Composition.tsx (SCAFFOLD — upgraded in Step 5)
import { AbsoluteFill, Sequence } from 'remotion';
import { COLORS } from './constants/colors';

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

This triggers the initial webpack bundle (~10s). All subsequent `remotion still` calls reuse the bundle and are fast (~3-5s).

## Step 3: Build Reusable Components

Create components defined in the plan under `components/`:
- `SceneBackground.tsx` — consistent scene wrapper with gradient
- Visual components as specified (terminals, diagrams, icons, etc.)

Follow Remotion best practices:
- Components receive `startFrame` props for animation triggers
- Use `useCurrentFrame()` + `interpolate()` / `spring()` internally
- Always clamp interpolations: `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'`
- Pass `fps` explicitly to `spring()`: `spring({ frame, fps: 30, config })`

## Step 4: Build Scene Components (With Per-Scene Validation)

For each scene, follow this loop:

1. **Create** `scenes/SceneNN<Name>.tsx`
2. **Import into scaffold** — Add the scene to `Composition.tsx` inside a `<Sequence>` wrapper:
   ```typescript
   <Sequence from={SCENES.<sceneName>.start} durationInFrames={SCENES.<sceneName>.duration}>
     <SceneNN<Name> />
   </Sequence>
   ```
3. **Validate** — Run `/validate-scene $ARGUMENTS SceneNN` to catch layout bugs immediately
4. **Fix if needed** — If validation fails, fix issues and re-validate before proceeding
5. **Next scene** — Move to the next scene only after current scene passes

This catches bugs in each scene before they propagate to subsequent scenes.

For each scene, create `scenes/SceneNN<Name>.tsx`:

### The Sync Formula

```typescript
// For each word in the sync JSON:
// scene_frame = word.start_seconds * 30 + audio_offset
//
// audio_offset = 30 for scene 1, 20 for scenes 2+
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
 *   ...
 */
```

For each visual beat, create an animation triggered by its word's frame:

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

### Using remotion-bits Wrappers (When Plan Specifies)

If the plan includes `remotion_bits_components_used`, use the synced wrappers instead of manual interpolate for supported patterns:

```typescript
import { SyncedAnimatedText, SyncedCodeBlock, SyncedStaggeredMotion } from '../../shared/components/bits';
import { wordToFrame } from '../../shared/utils/cleanSyncData';

// Text entrance synced to "Docker" at 1.2s
<SyncedAnimatedText triggerFrame={wordToFrame(1.2, AUDIO_OFFSET)} split="word">
  Docker containers simplified
</SyncedAnimatedText>

// Code block synced to "example" at 5.8s
<SyncedCodeBlock
  code={codeString}
  triggerFrame={wordToFrame(5.8, AUDIO_OFFSET)}
  lineStagger={5}
  showLineNumbers
/>

// Feature list synced to "features" at 8.3s
<SyncedStaggeredMotion triggerFrame={wordToFrame(8.3, AUDIO_OFFSET)} stagger={10}>
  <div style={{ display: 'block' }}>Fast builds</div>
  <div style={{ display: 'block' }}>Easy scaling</div>
  <div style={{ display: 'block' }}>Portable</div>
</SyncedStaggeredMotion>
```

**IMPORTANT**: Phase-based rendering still applies — wrap bits components in `{isPhase && ...}` conditionals.

### Retention Toolkit (Pattern Interrupt Components)

Use these shared components from `src/shared/components/retention/` to boost viewer retention:

```typescript
import { ScreenShake, GlitchInterrupt, ColorShift, FitHeadline } from '../../shared/components/retention';

// Shake on emphasis words ("But", "However", big reveals)
<ScreenShake triggerFrame={wordToFrame(5.2, AUDIO_OFFSET)} intensity={4}>
  {/* content to shake */}
</ScreenShake>

// Brief chromatic aberration glitch for visual interrupts
<GlitchInterrupt triggerFrame={wordToFrame(8.5, AUDIO_OFFSET)}>
  {/* content to glitch */}
</GlitchInterrupt>

// Auto-sizing headline that never overflows
<FitHeadline text="Dynamic Headline" maxWidth={1600} />
```

### Visual Enhancement Components (Optional)

```typescript
import { StarburstBackground, LightLeakOverlay } from '../../shared/components';

// Animated starburst rays behind hero stats or title cards (keep opacity LOW)
<StarburstBackground
  rays={12}
  colors={[COLORS.primary, COLORS.secondary]}
  opacity={0.12}
  rotationSpeed={0.2}
/>

// Light leak for emphasis moments (standalone — not TransitionSeries.Overlay)
// Place at Composition level inside a <Sequence>
<Sequence from={emphasisFrame} durationInFrames={40}>
  <LightLeakOverlay seed={5} hueShift={0} opacity={0.5} durationInFrames={40} />
</Sequence>
```

**StarburstBackground** — best for: HeroStat backgrounds, SegmentTitleCard, CTA energy, Scene00Preview.
**LightLeakOverlay** — best for: TransitionSeries.Overlay at cut points (see composition-structure.md), hook/CTA emphasis.

### Advanced Visual Enhancement Components (Optional)

```typescript
import {
  MotionBlurTrail, ProceduralNoise, AnimatedShape, RoundedTextBox
} from '../../shared/components';

// Motion blur on fast-moving spring animations (hero reveals, fly-ins)
<MotionBlurTrail layers={8} lagInFrames={0.5}>
  <div style={{ transform: `translateY(${springValue}px)` }}>
    Big Stat Reveal
  </div>
</MotionBlurTrail>

// Organic Perlin noise background (replaces static particles)
<ProceduralNoise
  seed="scene03"
  color={COLORS.primary}
  count={15}
  opacity={0.12}
  speed={0.006}
/>

// SVG shapes with draw-on animation (diagrams, accents)
<AnimatedShape
  shape="circle"
  width={120}
  stroke={COLORS.primary}
  triggerFrame={wordToFrame(5.2, AUDIO_OFFSET)}
/>

// TikTok-style rounded text boxes (especially good for Shorts)
<RoundedTextBox
  text="This changes everything"
  fontFamily={FONTS.primary}
  fontSize={48}
  boxColor="rgba(139,92,246,0.85)"
  triggerFrame={wordToFrame(3.2, AUDIO_OFFSET)}
/>
```

**MotionBlurTrail** — wraps any moving element for cinematic blur. Best for: spring entrances, scale pops, hero stat reveals. Avoid on static content.
**ProceduralNoise** — Perlin noise-driven particle backgrounds. Best for: organic ambient motion, replacing static gradient backgrounds.
**AnimatedShape** — SVG circle/rect/triangle/star/polygon with stroke draw-on. Best for: diagram elements, decorative accents, visual metaphors.
**RoundedTextBox** — pixel-perfect multiline rounded text boxes. Best for: Shorts captions, callout labels, highlighted quotes.

### Additional Packages Available (Direct Import)

```typescript
// Embed Lottie animations from lottiefiles.com
import { Lottie } from '@remotion/lottie';
import animationData from './assets/loading.json';
<Lottie animationData={animationData} style={{ width: 200, height: 200 }} />

// Preload assets to eliminate loading flashes in Studio
import { preloadAudio, preloadImage } from '@remotion/preload';
preloadAudio(staticFile('audio/mycomp/scene01.mp3'));

// Frame-synced GIF playback
import { Gif } from '@remotion/gif';
<Gif src={staticFile('images/mycomp/demo.gif')} width={400} height={300} />
```

### Timing Tips
- Start animation 2 frames before the word for visual anticipation
- Use 15-20 frame fade-ins for text elements
- Use `spring()` for scale/position entrances (more organic)
- Use `interpolate()` for opacity and linear progress
- Add shake/pulse effects for emphasis words (4-8 frame duration)

### CRITICAL: Avoid Overlapping Elements

Elements must NEVER visually overlap or compete for the same screen space. Use these patterns:

**Phase-Based Rendering** (preferred for complex scenes):
```typescript
// Define phases based on content sections
const PHASE1_END = 120;  // First topic ends
const PHASE2_END = 240;  // Second topic ends

const isPhase1 = frame < PHASE1_END;
const isPhase2 = frame >= PHASE1_END && frame < PHASE2_END;
const isPhase3 = frame >= PHASE2_END;

// Render ONLY one phase at a time
{isPhase1 && <ContentA />}
{isPhase2 && <ContentB />}  // Replaces ContentA
{isPhase3 && <ContentC />}  // Replaces ContentB
```

**Sequential Animation** (for elements that share space):
```typescript
// Element B waits for Element A to exit before entering
const elementAOpacity = interpolate(frame, [0, 30, 60, 90], [0, 1, 1, 0], { extrapolateRight: 'clamp' });
const elementBOpacity = interpolate(frame, [90, 120], [0, 1], { extrapolateLeft: 'clamp' });

// Never both visible at same time
{elementAOpacity > 0 && <ElementA opacity={elementAOpacity} />}
{elementBOpacity > 0 && <ElementB opacity={elementBOpacity} />}
```

**Grid Layout** (for multiple elements):
- Use CSS Grid or Flexbox with explicit positioning
- Define clear screen zones (left/right, top/bottom quadrants)
- Never allow elements to "float" without explicit position

### Architecture Diagrams with Connected Elements

**CRITICAL: Load the `visual-diagrams` skill** when building any scene with architecture diagrams,
hub-and-spoke layouts, flowcharts, pipelines, or connected component visualizations. This skill
ensures YouTube-grade visual quality with gradient fills, depth shadows, glowing connections,
and brand logo support.

#### Use Shared Diagram Components (ALWAYS Check First)

Before building custom diagram layouts, check if a shared component fits. All support `mode="light"` and `mode="dark"`.

**Enterprise-grade components** (from `../../shared/components/diagrams`, uses `lucide-react` icons):

| Visual Need | Component | Import |
|---|---|---|
| **Multi-stage process (PREFERRED)** | `InfographicFlow` | `../../shared/components/diagrams` |
| Chronological events, roadmap | `Timeline` | `../../shared/components/diagrams` |
| Big numbers, metrics, KPIs | `StatCardRow` | `../../shared/components/diagrams` |
| Feature lists, capability grids | `FeatureGrid` | `../../shared/components/diagrams` |
| Iterative loops, feedback cycles | `ProcessCycle` | `../../shared/components/diagrams` |
| Tweets, announcements, key quotes | `QuoteCard` | `../../shared/components/diagrams` |

**Classic dark-mode components** (from `../../shared/components`):

| Visual Need | Component | Import |
|---|---|---|
| Central element + surrounding services | `HubAndSpoke` | `../../shared/components` |
| Sequential process/pipeline | `FlowDiagram` | `../../shared/components` |
| Stacked layers (UI > API > DB) | `LayeredArchitecture` | `../../shared/components` |
| Side-by-side comparison | `ComparisonDiagram` | `../../shared/components` |
| Git workflow visualization | `GitBranching` | `../../shared/components` |

**Icon library**: Import Lucide icons directly for use in any diagram component:
```tsx
import { Search, Brain, Cpu, Database, Shield, Send } from 'lucide-react';
// Browse all 1000+ icons: https://lucide.dev/icons
```

All components have professional visual treatment built in (gradient fills, shadows, glowing
connections, brand logo support via `iconSrc` prop).

#### Brand Logos — MANDATORY for All Company/Tool Mentions

**Every brand or company name displayed in a scene MUST include its real logo.** Use the shared library first, download missing logos as needed.

**Step 1 — Check the shared library:**
```tsx
import { BRAND_LOGOS } from '../../shared/constants/brandLogos';
import { Img, staticFile } from 'remotion';

// Use in cards, diagram nodes, comparison panels
<Img src={staticFile(BRAND_LOGOS.openai)} style={{ width: 44, height: 44, objectFit: 'contain' }} />
```

**Step 2 — Download missing logos:**
```bash
# GitHub org avatars (128px) — most reliable source
curl -sL "https://github.com/<org>.png?size=128" -o "public/images/shared/logos/<brand>-logo.png"
```
Then add the entry to `src/shared/constants/brandLogos.ts`.

**Step 3 — Use in diagram components:**
```tsx
<HubAndSpoke
  hub={{ label: 'Docker', iconSrc: staticFile(BRAND_LOGOS.docker), color: '#2496ED' }}
  spokes={[
    { label: 'Redis', iconSrc: staticFile(BRAND_LOGOS.redis), color: '#DC382D', triggerFrame: 30 },
  ]}
/>
```

If no logo is available, pass a single-character `icon` prop — the component renders a styled
letter badge (colored rounded square with the letter) instead of a raw Unicode symbol.

#### Person Photos

When a scene introduces a specific person by name (developer, CEO, creator), download their photo:
```bash
# GitHub profile photo
curl -sL "https://github.com/<username>.png?size=256" -o "public/images/<comp>/<person>-photo.png"
```
Display as a circular avatar (80-100px) with a colored border next to the person's name card.

#### Custom Diagrams (When No Shared Component Fits)

Use `DIAGRAM_STYLES` from `../../shared/components/constants` for consistent visual treatment:

```typescript
import { DIAGRAM_STYLES } from '../../shared/components/constants';

// Every custom diagram node MUST use these:
background: DIAGRAM_STYLES.nodeGradient(color),     // gradient fill
border: DIAGRAM_STYLES.nodeBorder(color),            // 2px visible border
boxShadow: DIAGRAM_STYLES.nodeShadow(color),         // depth + glow
borderRadius: DIAGRAM_STYLES.borderRadius,            // 14px
// Minimum: width 160, height 100

// Every SVG connection MUST include glow layer:
<line stroke={color} strokeWidth={8} opacity={0.12}
      filter="url(#connectionGlow)" />              // glow
<line stroke={color} strokeWidth={2.5} opacity={0.6}
      strokeDasharray={len} strokeDashoffset={off} /> // main
```

#### Diagram Layout Rules

**Z-Index**: SVG connections (zIndex: 0) BEFORE node divs (zIndex: 2).

**Shortened Lines**: Lines must stop at node edges, not pass through centers:
```typescript
const ux = dx / dist, uy = dy / dist;
const sx = hubX + ux * HUB_MARGIN;  // start at hub edge
const ex = nodeX - ux * NODE_MARGIN; // end at node edge
```

**Background Atmosphere**: Add a radial gradient + ProceduralNoise behind diagrams:
```tsx
<div style={{ position: 'absolute', inset: 0,
  background: `radial-gradient(ellipse at ${CX}px ${CY}px, ${COLORS.primary}08 0%, transparent 60%)` }} />
<ProceduralNoise seed="diagram" color={COLORS.primary} count={12} opacity={0.08} speed={0.004} />
```

## Step 5: Upgrade Scaffold to Final Composition.tsx

The scaffold `Composition.tsx` from Step 2c already imports all scenes inside `<Sequence>` wrappers. Now upgrade it to the final version with `TransitionSeries`, audio layers, SFX, BrandWatermark, and OutroSequence.

### Read Transition Selection from Plan

First, read the transition selection from `PLAN_FILE`:
```yaml
transitions:
  primary:
    id: wipe-left
  accent:
    id: glitch-in
```

### Import Transitions and Configure

```typescript
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { slide } from '@remotion/transitions/slide';
import { BrandWatermark, OutroSequence, LightLeakOverlay } from '../shared/components';

// Import all scenes
// Import SCENES, TRANSITION_DURATION, OUTRO_DURATION from constants/timing

// Transitions from plan (2 per video for consistency)
const TRANSITIONS = {
  primary: slide({ direction: 'from-left' }),  // From plan: wipe-left
  accent: fade(),  // From plan: glitch-in (visual approximation)
  primarySfx: 'sfx/final/scene/wipe-left.mp3',
  accentSfx: 'sfx/final/intro-outro/glitch-in.mp3',
};

const AUDIO_FILES = [
  { src: 'audio/<name>/scene01.mp3', from: SCENES.<first>.start + 30 },
  { src: 'audio/<name>/scene02.mp3', from: SCENES.<second>.start + 20 },
  // ... (offset 20 for all scenes except first which is 30)
];

// MANDATORY: Transition SFX array - one entry per scene transition
// Assignment rules:
// - Hook entrance (Scene 0→1): accent
// - Middle scenes: primary
// - CTA entrance: accent
const TRANSITION_SFX = [
  // Hook entrance - ACCENT
  { src: TRANSITIONS.accentSfx, from: SCENES.<first>.start + SCENES.<first>.duration - 5 },
  // Middle scenes - PRIMARY
  { src: TRANSITIONS.primarySfx, from: SCENES.<second>.start + SCENES.<second>.duration - 5 },
  { src: TRANSITIONS.primarySfx, from: SCENES.<third>.start + SCENES.<third>.duration - 5 },
  // ... continue for all middle scenes
  // CTA entrance - ACCENT
  { src: TRANSITIONS.accentSfx, from: SCENES.<last_before_cta>.start + SCENES.<last_before_cta>.duration - 5 },
];
```

### Complete Composition Template

```typescript
export const <AnimationName>: React.FC = () => {
  const t = TRANSITION_DURATION;
  return (
    <AbsoluteFill>
      <TransitionSeries>
        {/* Scene 01 - Hook entrance uses ACCENT transition */}
        <TransitionSeries.Sequence durationInFrames={SCENES.<first>.duration}>
          <Scene01Hook />
        </TransitionSeries.Sequence>

        {/* MANDATORY: Light leak overlay at every scene cut — zero frame cost */}
        {/* seed increments per scene for pattern variety */}
        {/* hueShift: derive from accent color — 0=warm amber, 120=green, 240=blue */}
        <TransitionSeries.Overlay durationInFrames={20}>
          <LightLeakOverlay seed={1} hueShift={0} />
        </TransitionSeries.Overlay>

        <TransitionSeries.Transition
          presentation={TRANSITIONS.accent}
          timing={linearTiming({ durationInFrames: t })}
        />

        {/* Middle scenes use PRIMARY transition */}
        <TransitionSeries.Sequence durationInFrames={SCENES.<second>.duration}>
          <Scene02 />
        </TransitionSeries.Sequence>

        {/* Light leak overlay — increment seed for each cut point */}
        <TransitionSeries.Overlay durationInFrames={20}>
          <LightLeakOverlay seed={2} hueShift={0} />
        </TransitionSeries.Overlay>

        <TransitionSeries.Transition
          presentation={TRANSITIONS.primary}
          timing={linearTiming({ durationInFrames: t })}
        />

        {/* ... continue pattern for all middle scenes:
             1. TransitionSeries.Sequence (scene content)
             2. TransitionSeries.Overlay (light leak — seed={N}, increment per cut)
             3. TransitionSeries.Transition (fade or slide)
             Repeat for each scene. Overlay has ZERO frame cost — it does not
             affect timing or composition duration. */}

        {/* CTA entrance uses ACCENT transition */}
        <TransitionSeries.Overlay durationInFrames={20}>
          <LightLeakOverlay seed={8} hueShift={0} />
        </TransitionSeries.Overlay>

        <TransitionSeries.Transition
          presentation={TRANSITIONS.accent}
          timing={linearTiming({ durationInFrames: t })}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.cta.duration}>
          <SceneCTA />
        </TransitionSeries.Sequence>

        {/* MANDATORY: Outro - always uses fade, NO overlay before outro */}
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />
        <TransitionSeries.Sequence durationInFrames={OUTRO_DURATION}>
          <OutroSequence />
        </TransitionSeries.Sequence>
      </TransitionSeries>

      {/* MANDATORY: Background music — multi-segment preferred */}
      {/* Check if multi-segment exists: public/audio/<name>/bg-music-hook.mp3 */}
      {/* If yes: use 3-segment pattern with dynamic volume. If no: fallback to single track. */}

      {/* Hook music — energetic, fades in/out */}
      <Sequence from={0} durationInFrames={SCENES.hook.duration}>
        <Audio
          src={staticFile(`audio/<name>/bg-music-hook.mp3`)}
          volume={(f) => interpolate(
            f, [0, 15, SCENES.hook.duration - 45, SCENES.hook.duration],
            [0, 0.12, 0.12, 0],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          )}
        />
      </Sequence>
      {/* Body music — ambient, constant volume */}
      <Sequence from={SCENES.hook.duration} durationInFrames={MIDROLL_START - SCENES.hook.duration}>
        <Audio src={staticFile(`audio/<name>/bg-music-body.mp3`)} volume={0.07} />
      </Sequence>
      {/* CTA music — upbeat, fades in/out */}
      <Sequence from={CTA_START} durationInFrames={OUTRO_START - CTA_START}>
        <Audio
          src={staticFile(`audio/<name>/bg-music-cta.mp3`)}
          volume={(f) => interpolate(
            f, [0, 30, (OUTRO_START - CTA_START) - 60, OUTRO_START - CTA_START],
            [0, 0.12, 0.12, 0],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          )}
        />
      </Sequence>
      {/* Fallback if no multi-segment: <Audio src={staticFile('audio/shared/bg-music.wav')} volume={0.08} /> */}

      {/* Audio layer - scene narration */}
      {AUDIO_FILES.map(({ src, from }) => (
        <Sequence key={src} from={from}>
          <Audio src={staticFile(src)} />
        </Sequence>
      ))}

      {/* MANDATORY: Transition SFX - synced to scene changes */}
      {TRANSITION_SFX.map(({ src, from }, idx) => (
        <Sequence key={`sfx-${idx}`} from={from} durationInFrames={30}>
          <Audio src={staticFile(src)} volume={0.3} />
        </Sequence>
      ))}

      {/* MANDATORY: DynamousMidroll narration audio */}
      {/* DynamousMidroll has internal SFX but does NOT play its own narration. */}
      {/* Without this Sequence, the midroll is 35 seconds of near-silence. */}
      <Sequence from={MIDROLL_START + 10}>
        <Audio src={staticFile('audio/shared/dynamous-midroll.mp3')} />
      </Sequence>

      {/* Brand watermark */}
      <BrandWatermark />

      {/* MANDATORY: Persistent topic-brand watermark — top right, opacity 0.35.
          Pick the BRAND_LOGOS key matching the video topic (e.g. .google, .claude, .openclaw).
          Hidden during midroll. See .claude/rules/brand-logos.md */}
      <Sequence from={0} durationInFrames={MIDROLL_START}>
        <Img src={staticFile(BRAND_LOGOS.google)} style={{
          position: 'absolute', top: 10, right: 30, width: 180, height: 180,
          objectFit: 'contain', opacity: 0.35,
        }} />
      </Sequence>
      <Sequence from={MIDROLL_START + DYNAMOUS_MIDROLL_DURATION} durationInFrames={TOTAL_FRAMES - (MIDROLL_START + DYNAMOUS_MIDROLL_DURATION)}>
        <Img src={staticFile(BRAND_LOGOS.google)} style={{
          position: 'absolute', top: 10, right: 30, width: 180, height: 180,
          objectFit: 'contain', opacity: 0.35,
        }} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### Transition Assignment Rules

1. **Hook entrance** (Scene 0 → 1): Always use **accent** transition
2. **Middle scenes** (Scene 1 → N-1): Always use **primary** transition
3. **CTA entrance** (Scene N-1 → CTA): Always use **accent** transition
4. **Outro** (CTA → Outro): Always use **fade** (consistent)

This creates visual rhythm: Accent → Primary → Primary → ... → Accent → Fade

### Mandatory Elements Checklist
Every composition MUST include:
1. **OutroSequence** — The branded outro (8s / 240 frames) as the final sequence
2. **Background music** — Check if `public/audio/<animationname>/bg-music-hook.mp3` exists (multi-segment from Phase 3.2). If yes, use 3-segment pattern (hook/body/cta) with dynamic volume curves. If only `bg-music.mp3` exists, use single track at 0.10 volume. Otherwise fall back to `audio/shared/bg-music.wav` at 0.08.
3. **BrandWatermark** — Logo with corner cycling
4. **Transition SFX** — Audio synced to each scene transition (volume 0.7)
5. **DynamousMidroll narration audio** — `<Sequence from={MIDROLL_START + 10}><Audio src={staticFile('audio/shared/dynamous-midroll.mp3')} /></Sequence>` — the midroll component does NOT play its own narration. Missing this = 35 seconds of near-silence.
6. **LightLeakOverlay at every scene cut** — `<TransitionSeries.Overlay durationInFrames={20}><LightLeakOverlay seed={N} hueShift={0} /></TransitionSeries.Overlay>` between every pair of `TransitionSeries.Sequence` blocks (except before Outro). Zero frame cost — does not affect timing. Increment `seed` per cut point for pattern variety. Adjust `hueShift` to match accent color if desired.

### SFX Timing Rules
- SFX starts **5 frames before** transition begins (`scene.duration - 5`)
- SFX duration: **30 frames** (1 second)
- SFX volume: **0.3** (hard cap 0.5 — see agent-pitfalls.md for per-SFX caps)

### Brand Watermark
Always include `<BrandWatermark />` at the end of the composition (after audio). It displays the logo with subtle transparency and animated position. Props available:
- `size={60}` — smaller logo
- `opacity={0.1}` — more subtle
- `mode="drift"` — smooth floating instead of corner cycling

## Step 6: Verify Root.tsx Registration

The composition was already registered in `Root.tsx` during Step 2c (scaffold). Verify it's still correct after the Step 5 upgrade — the import and `<Composition>` entry should already be in place. Update dimensions if the plan specifies non-standard resolution (e.g., 1280x720).

## Step 7: Apply Remotion Best Practices

When running Phase 4 via this standalone command (not via full-auto-v2), apply these checks manually. The `phase4-scene-builder` agent has all rules baked in — if using full-auto-v2 that agent handles this step.

All rules are documented in `.claude/rules/agent-pitfalls.md`. Key checklist:
- No non-deterministic values in renders (no `Math.random()` without seed — use `import { random } from 'remotion'`)
- All springs pass explicit `fps`: `spring({ frame, fps: 30, config })`
- All interpolations are clamped: `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'`
- `staticFile()` used for all public assets
- No inline `require()` or dynamic imports
- No `+ TRANSITION_DURATION` in `durationInFrames` in TransitionSeries
- `FONTS.primary` / `FONTS.mono` only (not `FONTS.inter`)
- No `<Audio>` inside scene components
- All stacked text divs have `display: 'block'`
- Code blocks have `whiteSpace: 'pre'`

## Step 8: Generate QA Frames (MANDATORY)

**This step is REQUIRED. Do NOT skip it.**

Generate `src/$ARGUMENTS/qa-frames.json` with intelligent frame selections for visual QA. These frames are calculated from the animation keyframes you just created.

### Frame Selection Strategy

Select frames where visual issues are most likely:

```json
{
  "compositionId": "$ARGUMENTS",
  "generatedAt": "<timestamp>",
  "frames": [
    {
      "frame": 0,
      "scene": "intro",
      "reason": "scene-start",
      "description": "Intro scene entry"
    },
    {
      "frame": 144,
      "scene": "preview",
      "reason": "peak-content",
      "description": "Preview hook - all elements visible"
    },
    {
      "frame": 258,
      "scene": "hook",
      "reason": "transition",
      "description": "Transition from preview to hook"
    }
  ]
}
```

### Frame Categories to Include

1. **Scene Transitions** (`reason: "transition"`):
   - `SCENES[scene].start` for each scene (catch transition artifacts)
   - `SCENES[scene].start - 5` (outgoing scene state)

2. **Peak Content** (`reason: "peak-content"`):
   - Mid-scene frames where most elements are visible
   - After final animation keyframe in each scene (everything rendered)

3. **Phase Changes** (`reason: "phase-change"`):
   - For scenes using phase-based rendering, capture frame at each phase boundary
   - Critical for detecting overlap issues

4. **Animation Clusters** (`reason: "animation-cluster"`):
   - Frames where 3+ elements animate within 30 frames
   - High risk of overlap or timing issues

### Calculating Frames from Sync Data

```typescript
// For each scene, identify key frames from sync JSON:
// 1. First word frame (scene start + audio offset)
// 2. Last word frame + 30 (scene fully rendered)
// 3. Midpoint between first and last

const firstWordFrame = syncData[0].start * 30 + AUDIO_OFFSET;
const lastWordFrame = syncData[syncData.length - 1].end * 30 + AUDIO_OFFSET;
const peakContentFrame = Math.floor((firstWordFrame + lastWordFrame) / 2);
```

### Example Output

For a 10-scene video, generate ~25-35 frames:
- 10 scene starts (transitions)
- 10 peak content frames (mid-scene)
- 5-15 phase change / animation cluster frames (scene-dependent)

Save to `src/$ARGUMENTS/qa-frames.json` for use by Phase 5.

## Step 9: VERIFICATION GATE (MANDATORY)

**Before completing Phase 4, verify ALL mandatory elements are present.**

Run these checks against `Composition.tsx`:

```bash
# Check for OutroSequence
grep -q "OutroSequence" src/$ARGUMENTS/Composition.tsx && echo "✅ OutroSequence found" || echo "❌ MISSING: OutroSequence"

# Check for BrandWatermark
grep -q "BrandWatermark" src/$ARGUMENTS/Composition.tsx && echo "✅ BrandWatermark found" || echo "❌ MISSING: BrandWatermark"

# Check for DynamousMidroll narration audio (NOT just the component — the Audio Sequence)
grep -q "dynamous-midroll.mp3" src/$ARGUMENTS/Composition.tsx && echo "✅ Midroll narration audio found" || echo "❌ MISSING: DynamousMidroll narration audio (audio/shared/dynamous-midroll.mp3)"

# Check timing.ts has outro
grep -q "outro:" src/$ARGUMENTS/constants/timing.ts && echo "✅ Outro timing found" || echo "❌ MISSING: outro in timing.ts"
```

**All checks MUST pass:**
- [ ] `Composition.tsx` imports and uses `OutroSequence` from `../shared/components`
- [ ] `Composition.tsx` uses `<OutroSequence />` as the final TransitionSeries scene
- [ ] `Composition.tsx` includes `<BrandWatermark />` after audio layers
- [ ] `Composition.tsx` includes `<Audio src={staticFile('audio/shared/dynamous-midroll.mp3')} />` in a `<Sequence>` overlay
- [ ] `timing.ts` includes `outro: { start: X, duration: 240 }` (8 seconds at 30fps)
- [ ] `qa-frames.json` exists with intelligent frame selections

**If any check fails: STOP and fix before proceeding to Phase 5.**

</process>

<output>
**Files created/updated**:
- `src/$ARGUMENTS/constants/` (colors, fonts, springs — if not existing)
- `src/$ARGUMENTS/components/` (reusable visual elements)
- `src/$ARGUMENTS/scenes/Scene01*.tsx` through `SceneNN*.tsx`
- `src/$ARGUMENTS/Composition.tsx` (includes OutroSequence + BrandWatermark from `src/shared/components/`)
- `src/Root.tsx`
- **`src/$ARGUMENTS/qa-frames.json`** (MANDATORY - for visual QA in Phase 5)

**Report to user**:
1. Component inventory: what was built
2. Scene sync summary: key animation trigger frames per scene
3. Transition types used between scenes
4. **Mandatory elements verified**: OutroSequence ✅, BrandWatermark ✅, outro timing ✅
5. **QA frames generated**: list the frame count and categories
6. Instruction: Run `npm run dev` and preview in Remotion Studio
7. Next step: After sync verification, run `/diy-yt-creation/phase5-render $ARGUMENTS`

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `4 - Sync` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>

## Mandatory Per-Scene Retention Checklist

After building each scene, verify ALL items before moving to the next:

- [ ] Is `ColorShift interval={600}` wrapping the scene's inner content div (not AbsoluteFill)?
- [ ] Is `FitHeadline` used for any standalone headline or large stat display?
- [ ] Is `STAGGER` constant (exported from timing.ts) used for all list item reveals?
- [ ] Is every text element on screen for at least `(word_count / 150) * 30 + 15` frames?
- [ ] Is `SpotlightFocus` used if the scene has 3+ diagram elements with narration addressing each?

Run `/validate-scene <AnimationName> <SceneNN>` immediately after each scene.
