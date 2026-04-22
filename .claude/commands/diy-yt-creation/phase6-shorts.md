---
description: "Phase 6 Shorts: Create YouTube Shorts from existing long-form videos"
argument-hint: <CompositionName (e.g., ClaudeCodeV2120)>
---

<objective>
Create derivative YouTube Shorts (9:16 vertical, 15-60s) from an existing long-form video composition.

**Goal**: Analyze scripts to identify hook-worthy moments, then create vertical Short compositions.
**Input**:
  - Existing composition at `src/$ARGUMENTS/`
  - Scene scripts at `src/$ARGUMENTS/scripts/scene-*.txt`
  - Audio at `public/audio/<name>/sceneNN.mp3`
  - Sync files at `src/$ARGUMENTS/scripts/sceneNN-sync.json`
**Output**:
  - Shorts analysis with recommendations
  - New vertical composition(s) at `src/$ARGUMENTSShorts/<ShortTitle>/`

**Key Requirements**:
  - Use `--shorts` flag when generating audio (uses faster ELEVENLABS_SPEED_SHORTS setting)
  - Scripts must be punchy, single-line (no empty lines = no pauses)
  - NO overlapping elements - use phase-based rendering exclusively
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 5 (Render) is `done`.
  - If not: STOP and report "Phase 5 (Render) has not been completed. Run `/diy-yt-creation:phase5-render $ARGUMENTS` first."
- **Re-run check**: If Phase 6-Shorts is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

### MANDATORY: Invoke youtube-shorts-hooks Skill

Before analyzing scripts, ALWAYS invoke the `youtube-shorts-hooks` skill:
```
/youtube-shorts-hooks <topic summary>
```
This provides the hook psychology framework (7 formulas, 1.5s cliff, loop design, vertical safe zones) that must inform every Short's script and visual design. Use its 7-gate validation checklist before finalizing each Short.

## Phase 6a: Analyze Scripts for Shorts Candidates

### Step 1: Gather Source Material

Read all scene scripts from `src/$ARGUMENTS/scripts/scene-*.txt` and the timing.ts file.

For each script, analyze for hook-worthy content using the Kallaway Formula criteria AND the youtube-shorts-hooks skill's 5-criteria scoring (scroll-stop, standalone, specificity, curiosity, emotion — min 18/25):

**Hook Strength (scored 1-5):**
1. Does it grab attention in first 3 seconds?
2. Is there a contrarian or surprising element?
3. Would it make someone stop scrolling?

**Standalone Value:**
1. Does this segment make sense without prior context?
2. Does it deliver value in 15-60 seconds?
3. Is there a clear payoff?

**Visual Interest:**
1. Does the scene have dynamic visuals?
2. Terminal demos, stats animations, before/after?

### Step 2: Score and Rank Segments

For each potential Short, provide:

```markdown
## Recommended Shorts for $ARGUMENTS

### Short 1: "[Title]" (Score: X/5)
- **Scenes:** [which scenes from source]
- **Duration:** ~XX seconds
- **Hook:** "[First line that grabs attention]"
- **Why:** [Reasoning - contrarian hook? visual demo? pain point?]

### Short 2: "[Title]" (Score: X/5)
...
```

Prioritize segments that:
- Have a strong opening line (contrarian, surprising, pain point)
- Are self-contained (don't require prior context)
- Have visual interest (terminal, stats, comparisons)
- Fit the 15-60 second window

### Step 3: User Selection

Present the analysis to the user and ask which Shorts to create AND for the thumbnail image.

**AskUserQuestion** (two questions):

1. **Which Shorts?**
   - Question: "Which Shorts should I create?"
   - Options: List top 3-4 candidates + "All recommended" + "Custom selection"

2. **Thumbnail for footer (MANDATORY)**
   - Question: "Provide the thumbnail image for the 'Full Video linked below' footer in all Shorts. This should be the long-form video's YouTube thumbnail. Paste the file path or URL."
   - The user provides a path to a thumbnail image (e.g., `c:\Users\...\thumbnail.png`)
   - Copy it to `public/images/<source>/thumbnail.png`
   - Pass as `thumbnailSrc="images/<source>/thumbnail.png"` to `ShortsFullVideoFooter`

---

## Phase 6b: Create Shorts Compositions

After user approves selections, create the Short compositions.

### Step 4: Create Directory Structure

For each selected Short, create:

```
src/$ARGUMENTSShorts/<ShortTitle>/
├── Composition.tsx
├── constants/
│   ├── timing.ts        # WIDTH=1080, HEIGHT=1920
│   └── colors.ts        # Import from source or define
├── scenes/
│   └── Scene01*.tsx     # Vertical scene components
└── scripts/
    └── scene01-sync.json  # Copied from source
```

### Step 5: Create timing.ts

```typescript
/**
 * Timing constants for $ARGUMENTS Short: <ShortTitle>
 * Derived from $ARGUMENTS scenes [X-Y]
 */

export const FPS = 30;
export const WIDTH = 1080;   // Vertical Short
export const HEIGHT = 1920;  // 9:16 aspect ratio

export const AUDIO_OFFSET_FIRST = 15;
export const AUDIO_OFFSET_REST = 10;
export const BUFFER_FRAMES = 15;
export const TRANSITION_DURATION = 15;

// Scene durations from source (recalculated for Short)
export const SCENES = {
  // ... derived from selected source scenes
} as const;

export const TOTAL_FRAMES = /* sum of scene durations with transitions */;
```

### Step 6: Generate Shorts Audio

**IMPORTANT**: Shorts need their own audio files with faster pacing. Do NOT copy audio from long-form videos.

**CRITICAL: Scripts MUST be derived from `full-script.md` ONLY.** Do NOT invent facts, timelines, dates, or claims. Every sentence in a Short script must come directly from the final approved long-form script. The research brief and content brief may contain early/draft information that was corrected during script review — never use them as source material for Shorts scripts. Read `src/<Composition>/scripts/full-script.md` and extract/condense from there.

1. **Write a punchy script** for the Short:
   - **Extract and condense from `full-script.md`** — do NOT write from scratch
   - Single continuous line (NO empty lines - they create pauses)
   - Punchy, engaging text - shorter sentences
   - ~2.5-3 words per second target
   - Save to `src/$ARGUMENTSShorts/<ShortTitle>/scripts/scene-01-<name>.txt`

2. **Generate audio with --shorts flag**:
   ```bash
   python text-to-speech.py \
     -i src/$ARGUMENTSShorts/<ShortTitle>/scripts/scene-01-<name>.txt \
     -o public/audio/<source>-shorts/<short-title>/ \
     -s src/$ARGUMENTSShorts/<ShortTitle>/scripts/ \
     -n scene01 \
     --shorts
   ```

   The `--shorts` flag uses `ELEVENLABS_SPEED_SHORTS` from .env (default 1.15) for faster pacing than long-form videos.

3. **Update timing.ts** with the new audio duration from the generation output

### Step 7: Create Vertical Scene Components

For each scene in the Short, create a vertical adaptation:

1. **Analyze source scene** - What visual elements does it have?
   - Terminal? → Use `VerticalTerminal` template
   - Stats/counters? → Use `VerticalStats` template
   - Text-focused hook? → Use `VerticalHook` template
   - Before/after? → Use `VerticalComparison` template
   - CTA? → Use `VerticalCTA` template

2. **Create vertical scene** - Adapt the layout:
   - Stack elements vertically instead of horizontally
   - Increase font sizes (mobile viewing)
   - Keep text lines shorter (max ~30 chars)
   - Place important content in top 2/3

Import templates from:
```typescript
import { VerticalHook, VerticalStats, VerticalCTA } from '../../shared/templates/shorts';
```

### Step 8: Create Composition.tsx

```typescript
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

import { SCENES, AUDIO_OFFSET_FIRST, TRANSITION_DURATION } from './constants/timing';
import { Scene01Hook } from './scenes/Scene01Hook';
// ... other scenes

import { BrandWatermark, ShortsFullVideoFooter, NoiseOverlay } from '../../shared/components';

export const <ShortTitle>Composition: React.FC = () => {
  const t = TRANSITION_DURATION;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0D1117' }}>
      <TransitionSeries>
        {/* Scenes with transitions */}
      </TransitionSeries>

      {/* Audio layers */}
      <Sequence from={AUDIO_OFFSET_FIRST}>
        <Audio src={staticFile('audio/<path>/scene01.mp3')} />
      </Sequence>

      {/* Brand watermark - MANDATORY */}
      <BrandWatermark size={180} />

      {/* Noise overlay - MANDATORY */}
      <NoiseOverlay opacity={0.07} />

      {/* "Full Video linked below" footer + thumbnail - MANDATORY */}
      <ShortsFullVideoFooter
        color={COLORS.primary}
        thumbnailSrc="images/<source>/thumbnail.png"
      />
    </AbsoluteFill>
  );
};
```

### Step 8b: Add End Thumbnail Frame + End-Screen Reservation Zone

Every Short MUST reserve the **last 10-20 seconds (300-600 frames, target 450)** for YouTube's end-screen video cards. Viewers need time to notice and tap the card, so the tail may only contain teaser visuals, CTA, and the end thumbnail — NO critical narration, stat reveals, or punchlines.

In `timing.ts`:
```typescript
const END_SCREEN_ZONE_FRAMES = 450;   // 15s — range 300-600, non-negotiable floor 300
const END_THUMBNAIL_FRAMES = 1;
const SCENE_FRAMES = /* sum of scene durations with transitions */;
export const TOTAL_FRAMES = SCENE_FRAMES + END_SCREEN_ZONE_FRAMES;
export const END_SCREEN_ZONE_START = TOTAL_FRAMES - END_SCREEN_ZONE_FRAMES;
// Last narration word MUST end before END_SCREEN_ZONE_START.
// If audio overruns, trim the CONTENT block — never shrink the tail.
```

The reservation zone partitions into: teaser phase (~13s, full-video thumbnail) + full-video CTA (~2s) + end thumbnail (1 frame). See `.claude/rules/shorts.md` → "MANDATORY: End-Screen Reservation Zone" for the full pattern.

In the last scene component (or Composition.tsx as an overlay):
```tsx
const END_THUMBNAIL_FRAME = TOTAL_FRAMES - 1;
const isEndThumbnail = frame >= END_THUMBNAIL_FRAME;

// Exclude from all other phases
const isPhase1 = !isThumbnail && !isEndThumbnail && frame < P1_END;

{isEndThumbnail && (
  <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', backgroundColor: COLORS.background }}>
    <div style={{ display: 'block', fontSize: 240, fontWeight: 900, color: COLORS.accent }}>{takeaway}</div>
    <div style={{ display: 'block', fontSize: 64, fontWeight: 900, color: COLORS.text, textAlign: 'center' }}>{headline}</div>
  </AbsoluteFill>
)}
```

End thumbnail content: key takeaway stat or curiosity hook. 3-5 words max, high contrast, no animation, no progress bar.

### Step 9: Register in Root.tsx

Add the new Short composition to `src/Root.tsx`:

```typescript
// Import
import { <ShortTitle>Composition } from './$ARGUMENTSShorts/<ShortTitle>/Composition';
import {
  TOTAL_FRAMES as <SHORT_TITLE>_TOTAL_FRAMES,
  WIDTH as <SHORT_TITLE>_WIDTH,
  HEIGHT as <SHORT_TITLE>_HEIGHT,
} from './$ARGUMENTSShorts/<ShortTitle>/constants/timing';

// Register in RemotionRoot — IMPORTANT: Prefix with main video name
<Composition
  id="$ARGUMENTS-<ShortTitle>"
  component={<ShortTitle>Composition}
  durationInFrames={<SHORT_TITLE>_TOTAL_FRAMES}
  fps={30}
  width={<SHORT_TITLE>_WIDTH}
  height={<SHORT_TITLE>_HEIGHT}
/>
```

### Step 10: Generate YouTube Metadata

For each Short, create a `metadata.md` file with optimized YouTube metadata:

**File**: `src/$ARGUMENTSShorts/<ShortTitle>/metadata.md`

```markdown
# YouTube Metadata for <ShortTitle>

## Title
[Catchy title under 100 chars - use hook + intrigue pattern]

## Description
[Opening hook that restates the value proposition]

[2-3 bullet points or emoji-prefixed lines summarizing key points]

🎯 Full breakdown in the linked video

#aicoding #programming #developer #coding #softwaredevelopment #artificialintelligence #shorts [+ topic-specific tags]

## Tags
[Comma-separated list of 10-15 relevant tags for YouTube search]

## Thumbnail Text (if needed)
[2-3 words for thumbnail overlay]
```

**Metadata Generation Guidelines:**

1. **Title Formula** (max 100 chars):
   - Pattern A: "[Pain Point]... Until You Learn This"
   - Pattern B: "The Secret to [Desired Outcome] ([Framework] Explained)"
   - Pattern C: "[Memorable Phrase]" - [Benefit Statement]
   - Include keywords early for search visibility
   - Use ellipsis (...) or em-dash (—) for intrigue

2. **Description Structure**:
   - Line 1: Hook that mirrors the video's opening line
   - Lines 2-4: Key points with emoji bullets (👤🤖🎯💡✨)
   - Line 5: CTA pointing to full video ("🎯 Full breakdown in the linked video")
   - Line 6+: Hashtags (always include #shorts at the end)

3. **Tags Selection**:
   - Include main topic keywords (ai coding, programming, developer)
   - Include framework/concept names (piv loop, systematic coding)
   - Include tool names if relevant (claude code, cursor, copilot)
   - Include benefit keywords (productivity, workflow, tips)
   - 10-15 tags total, comma-separated

4. **Hashtags in Description**:
   - Always include: #aicoding #programming #developer #coding #shorts
   - Add 3-5 topic-specific hashtags
   - Place at end of description, on single line

**Example metadata.md:**

```markdown
# YouTube Metadata for SlotMachine

## Title
AI Coding Feels Like a Slot Machine... Until You Learn This

## Description
Your AI just wrote 500 lines of code. Tests pass. You ship it. Two hours later — production explodes. 💥

Most developers treat AI coding like gambling. But there's a system that makes it predictable.

Introducing the PIV Loop — the mental model that transforms chaotic AI coding into systematic workflows.

🎯 Full breakdown in the linked video

#aicoding #pivloop #programming #developer #coding #softwaredevelopment #artificialintelligence #claudecode #devtools #productivity #shorts

## Tags
ai coding, piv loop, ai programming, developer productivity, coding tips, software development, claude code, ai tools, systematic coding, programming workflow

## Thumbnail Text
SLOT MACHINE?
```

</process>

<vertical-design-guidelines>

## CRITICAL: Mobile-First Layout Rules

**The upper 2/3 of the screen (y=0 to y=1280) is the ONLY visible area when scrolling.**
Content in the bottom 1/3 may be obscured by UI elements or missed during thumb-scrolling.

### Screen Zones (1080x1920)
```
┌────────────────────┐ y=0
│                    │
│   PRIMARY ZONE     │ y=80-400: Title + main hook
│   (Always visible) │
│                    │
├────────────────────┤ y=400
│                    │
│   CONTENT ZONE     │ y=400-1000: Main content
│   (Full attention) │ Cards, stats, graphics
│                    │
├────────────────────┤ y=1000
│   PAYOFF ZONE      │ y=1000-1280: Final message
│   (Still visible)  │ CTA, tagline
├────────────────────┤ y=1280 ← FOLD LINE
│                    │
│   AVOID THIS ZONE  │ y=1280-1920: May be hidden
│   (UI overlays)    │ by comments, share buttons
│                    │
└────────────────────┘ y=1920
```

## Typography for Mobile (LARGE!)
- **Headlines**: 64-96px (2x larger than horizontal)
- **Body text**: 40-52px minimum
- **Stats/numbers**: 100-140px for impact
- **Line length**: Max ~20 characters per line
- **Font weight**: 700-800 (bold/extra-bold) for visibility

## Layout Rules
- **ALL content above y=1280** (upper 2/3)
- **Full width cards**: Use 40px margins (1000px content width)
- **Large icons**: 60-100px emoji/icons
- **Generous padding**: 28-48px inside cards
- **High contrast**: Solid colors, 3-4px borders
- **Card gap**: 16-20px between stacked cards

## Vertical Spacing Guidelines
| Element | top position | Notes |
|---------|-------------|-------|
| Title section | 60px | Emoji + 2 lines of text |
| Content with title | 420-440px | Leave 60px+ gap below title |
| Content without title | 300px | Phase 2/3 can start higher |
| Card gap | 16-20px | Between stacked cards |

**Example layout:**
```
y=60:   Title (emoji + headline)
y=300:  --- 240px title zone ---
y=420:  Content cards start (when title visible)
y=300:  Content cards start (when title hidden in phase 2/3)
```

- **CRITICAL - NO OVERLAPPING ELEMENTS**: Structure scenes with distinct phases that REPLACE each other
  ```tsx
  // Define phases based on word timing from sync file
  const PHASE2_START = 604;  // Frame when phase 2 content is mentioned
  const CTA_START = TOTAL_FRAMES - 90;  // Last 3 seconds

  // Determine current phase - MUTUALLY EXCLUSIVE
  const isPhase1 = frame < PHASE2_START;
  const isPhase2 = frame >= PHASE2_START && frame < CTA_START;
  const isCTA = frame >= CTA_START;

  // Render only ONE phase at a time - NEVER show multiple phases
  {isPhase1 && (<Phase1Title />)}   {/* Title ONLY during phase 1 */}
  {isPhase1 && (<Phase1Content />)}
  {isPhase2 && (<Phase2Content />)} {/* Completely replaces phase 1 */}
  {isCTA && (<CTAContent />)}       {/* Completely replaces phase 2 */}
  ```

  **PHASE RULES**:
  - Each phase completely REPLACES the previous (no simultaneous rendering)
  - ALL elements including titles must be gated by phase conditions
  - NEVER use "always visible" for any element that could overlap
  - All content areas use the SAME `top` position (elements swap in place)
  - Test by scrubbing through timeline - at NO point should elements overlap

## Sizing Reference
| Element | Horizontal (1920x1080) | Vertical (1080x1920) |
|---------|------------------------|----------------------|
| Headline | 48-64px | 72-96px |
| Body text | 24-32px | 40-52px |
| Stat numbers | 60-80px | 120-160px |
| Icons | 40-60px | 80-120px |
| Card padding | 20-30px | 32-48px |
| Border width | 2px | 3-4px |

## Timing for Vertical
- **Faster pacing**: Shorts viewers have shorter attention spans
- **Front-loaded hook**: First 3 seconds are critical
- **Clear endpoint**: Strong CTA or natural loop point

## MANDATORY: "Full Video linked below" Footer + Thumbnail

Every Short MUST include the `ShortsFullVideoFooter` component in Composition.tsx. This is a **persistent** element visible throughout the entire Short — do NOT add inline CTA elements in scene files.

```tsx
// In Composition.tsx — MANDATORY for every Short
import { ShortsFullVideoFooter } from '../../shared/components';

// Inside the root AbsoluteFill, after NoiseOverlay:
<ShortsFullVideoFooter
  color={COLORS.primary}
  thumbnailSrc="images/<source>/thumbnail.png"  // Long-form video thumbnail
/>
```

**Props:**
- `color` — accent color for the arrow (default: `#D97757`)
- `textColor` — muted text color (default: `#A8A29E`)
- `thumbnailSrc` — path to the long-form video thumbnail (relative to `public/`). **ASK THE USER** for this image during Step 3.
- `thumbnailWidth` — width of thumbnail preview (default: 720px)

**Do NOT:**
- Add inline "Full video below" CTAs in scene components
- Use emoji arrows — the component uses Unicode `\u25BC`
- Skip the thumbnail — always ask the user for it

## Template Selection Guide
| Source Pattern | Vertical Template |
|----------------|-------------------|
| Terminal + side text | `VerticalTerminal` - Terminal above, caption below |
| Stats in a row | `VerticalStats` - Stats stacked vertically |
| Centered text hook | `VerticalHook` - Larger text, top-weighted |
| Side-by-side comparison | `VerticalComparison` - Top/bottom stack |
| CTA with button | `VerticalCTA` - Full-width, larger button |
| Highlighted captions | `RoundedTextBox` - TikTok-style per-line rounded text boxes |

### Shorts-Specific Components

```tsx
// TikTok-style rounded caption boxes (per-line rounded corners)
import { RoundedTextBox } from '../../shared/components';

<RoundedTextBox
  text={"This is the\nbiggest change"}
  fontFamily={FONTS.primary}
  fontSize={52}
  boxColor="rgba(139,92,246,0.85)"
  triggerFrame={wordToFrame(1.5, O)}
/>
```

</vertical-design-guidelines>

<output>
**Files created**:
```
src/$ARGUMENTSShorts/<ShortTitle>/
├── Composition.tsx
├── metadata.md           # YouTube title, description, tags
├── constants/
│   ├── timing.ts
│   └── colors.ts
├── scenes/
│   └── Scene*.tsx
└── scripts/
    └── sceneNN-sync.json

public/audio/<source>-shorts/<short-title>/
└── sceneNN.mp3
```

**Root.tsx updated**: New composition registered with WIDTH/HEIGHT from timing.ts

**Report to user**:
1. Short title and composition ID
2. Duration (frames and seconds)
3. Source scenes used
4. YouTube metadata summary (title + key tags)
5. Preview command: `npm run dev` then select composition
6. Render command: `pnpm exec remotion render $ARGUMENTS-<ShortTitle> out/<name>/short.mp4 --codec h264 --crf 15`

**Next steps**:
- Preview in Remotion Studio (canvas should show 1080x1920)
- Adjust scene timing if needed
- Render with Phase 5 render command
- Copy metadata from `metadata.md` when uploading to YouTube

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `6 - Shorts` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>
