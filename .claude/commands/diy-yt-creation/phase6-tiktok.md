---
description: "Phase 6 TikTok: Create TikTok videos from existing long-form or Shorts compositions"
argument-hint: <CompositionName (e.g., ClaudeCodeV2120 or ClaudeOpus46Shorts/AdaptiveThinking)>
---

<objective>
Create TikTok-optimized vertical videos (9:16, 15-90s) from existing long-form or Shorts compositions.

**Goal**: Adapt existing content for TikTok's algorithm, UI safe zones, and audience behavior.
**Input**:
  - Existing composition at `src/$ARGUMENTS/`
  - Scene scripts, audio, and sync files from source
**Output**:
  - TikTok composition(s) at `src/<Name>TikTok/<Title>/`
  - TikTok-specific metadata (hashtags, description, cover frame)

**Key Differences from YouTube Shorts**:
  - TikTok UI safe zones differ (top 15% + bottom 20% obscured)
  - No "Full video below" CTA (TikTok doesn't link to YouTube) — use engagement CTAs instead
  - Loop engineering: outro should flow visually back to intro for replay boost
  - Captions are MANDATORY (TikTok-native karaoke style)
  - Hashtag strategy: 3-5 max (not YouTube's long list)
  - Description: engagement hook, not SEO keywords
  - Cover frame selection (TikTok lets creators pick cover, not always frame 0)

**Source Types**:
  - From long-form: analyze scripts, extract segments (like Shorts workflow)
  - From existing Shorts: adapt safe zones, CTA, metadata, and caption style
</objective>

<process>

## Phase 6t-a: Analyze Source & Select Content

### Step 1: Determine Source Type

Check if `$ARGUMENTS` points to:
- **Long-form composition** (e.g., `ClaudeCodeV2120`) → Run full analysis like Shorts Phase 6a
- **Existing Shorts composition** (e.g., `ClaudeOpus46Shorts/AdaptiveThinking`) → Skip to Phase 6t-b (adapt existing Short)

### Step 2: For Long-Form Sources — Analyze Scripts

Read all scene scripts from `src/$ARGUMENTS/scripts/scene-*.txt`.

Score each segment using TikTok-optimized criteria:

**Hook Strength (scored 1-5):**
1. Does it grab attention in first 1.5 seconds? (TikTok is faster than Shorts)
2. Is there a pattern interrupt — something unexpected?
3. Would it make someone stop mid-scroll on a phone?

**Completion Potential (TikTok's #1 signal):**
1. Does the segment deliver a payoff that rewards watching to the end?
2. Is the pacing tight enough to maintain 70%+ watch-through?
3. Can the ending loop back to the beginning?

**Engagement Triggers:**
1. Does it provoke a comment? (opinion, question, debate)
2. Is it save-worthy? (useful tip, reference, tutorial)
3. Is it share-worthy? (surprising stat, relatable pain point)

### Step 3: Score and Rank

```markdown
## TikTok Candidates for $ARGUMENTS

### TikTok 1: "[Title]" (Score: X/5)
- **Scenes:** [source scenes]
- **Duration:** ~XXs (target 45-75s for educational)
- **Hook:** "[First 1.5 seconds]"
- **Loop Point:** [How the ending connects back to the start]
- **Engagement Trigger:** [What will make people comment/save/share?]
```

**Duration targets by content type:**
| Type | Duration | Notes |
|------|----------|-------|
| Pure hook / trend | 15-20s | Highest completion rate |
| Quick tip | 21-34s | Strong organic reach |
| Educational explainer | 45-75s | Best for AI/tech niche |
| Deep-dive tutorial | 60-90s | High save rate, moderate completion |

### Step 4: User Selection

Present analysis and ask which TikToks to create.

**AskUserQuestion**:
- Question: "Which TikToks should I create?"
- Options: Top 3-4 candidates + "All recommended" + "Custom selection"

---

## Phase 6t-b: Create TikTok Compositions

### Step 5: Create Directory Structure

For each selected TikTok, create:

```
src/<Name>TikTok/<Title>/
├── Composition.tsx
├── metadata.md           # TikTok-specific metadata
├── constants/
│   ├── timing.ts         # WIDTH=1080, HEIGHT=1920
│   └── colors.ts
├── scenes/
│   └── Scene01*.tsx       # TikTok-optimized scene
└── scripts/
    ├── scene-01-<name>.txt
    └── scene01-sync.json
```

### Step 6: Create timing.ts

```typescript
/**
 * Timing constants for TikTok: <Title>
 * Derived from $ARGUMENTS
 */

export const FPS = 30;
export const WIDTH = 1080;   // Vertical TikTok
export const HEIGHT = 1920;  // 9:16 aspect ratio

export const AUDIO_OFFSET_FIRST = 15;
export const AUDIO_OFFSET_REST = 10;
export const BUFFER_FRAMES = 15;
export const TRANSITION_DURATION = 15;

// TikTok-specific: cover frame (user can select in TikTok app)
export const COVER_FRAME = 45; // Frame with best visual for cover selection

// TikTok-specific: NO Full Video CTA — use engagement CTA instead
export const ENGAGEMENT_CTA_START = /* TOTAL_FRAMES - 75 */; // Last 2.5s

export const SCENES = {
  // ... derived from source
} as const;

export const TOTAL_FRAMES = /* calculated */;

export const AUDIO_OFFSET = AUDIO_OFFSET_FIRST;
export const AUDIO_FILES = {
  scene01: 'audio/<source>-tiktok/<title>/scene01.mp3',
};
```

### Step 7: Generate TikTok Audio

**Audio approach depends on source type:**

**From long-form:** Write a new punchy script and generate fresh audio:
1. Write script to `src/<Name>TikTok/<Title>/scripts/scene-01-<name>.txt`
   - Single continuous line (NO empty lines)
   - Even punchier than Shorts — every word must earn its place
   - ~3 words per second target (slightly faster than Shorts)
2. Generate audio with `--shorts` flag (same faster pacing):
   ```bash
   python text-to-speech.py \
     -i src/<Name>TikTok/<Title>/scripts/scene-01-<name>.txt \
     -o public/audio/<source>-tiktok/<title>/ \
     -s src/<Name>TikTok/<Title>/scripts/ \
     -n scene01 \
     --shorts
   ```

**From existing Short:** Reuse audio directly:
1. Copy sync JSON: `cp src/<Short>/scripts/scene01-sync.json src/<Name>TikTok/<Title>/scripts/`
2. Reference same audio file in timing.ts (no re-generation needed)

### Step 8: Create TikTok Scene Components

TikTok scenes follow the same vertical rules as Shorts BUT with these critical differences:

#### TikTok Safe Zones (DIFFERENT from Shorts!)

```
┌────────────────────┐ y=0
│  ╔═══ UNSAFE ═══╗  │ y=0-290:  Username, follow button,
│  ║  TikTok UI   ║  │           search icon (TOP 15%)
│  ╚══════════════╝  │
├────────────────────┤ y=290
│                    │
│   SAFE CONTENT     │ y=290-1000: Primary content zone
│   ZONE             │
│                    │
├────────────────────┤ y=1000
│   CAPTION ZONE     │ y=1000-1400: Captions + secondary content
│                    │
├────────────────────┤ y=1400
│  ╔═══ UNSAFE ═══╗  │ y=1400-1920: Like/comment/share buttons,
│  ║  TikTok UI   ║  │             description text, sound pill
│  ║  Buttons     ║  │             (BOTTOM 27%)
│  ╚══════════════╝  │
└────────────────────┘ y=1920
```

**Key layout differences from Shorts:**
- Title/hook content starts at y=300 (not y=60)
- Content cards: y=440 to y=1000 (narrower window)
- Captions: bottomOffset=500 (not 420) to avoid TikTok UI
- Right margin needs 120px clear for like/comment/share/bookmark buttons

```tsx
// TikTok-specific layout constants
const TIKTOK_SAFE = {
  topStart: 300,      // Below username/follow button
  contentStart: 440,  // Below title zone
  contentEnd: 1000,   // Above caption zone
  captionY: 1100,     // Caption placement
  rightMargin: 120,   // Clear for action buttons
  bottomUnsafe: 1400, // TikTok UI starts here
};
```

#### No "Full Video Below" CTA — Use Engagement CTA

TikTok videos should NOT reference YouTube. Replace the mandatory Shorts CTA with:

```tsx
// WRONG for TikTok — references YouTube
{isFullVideoCTA && (
  <div>Want the full breakdown? Full video below 👇</div>
)}

// CORRECT for TikTok — drives engagement
const ENGAGEMENT_CTA_START = TOTAL_FRAMES - 75; // Last 2.5s
const isEngagementCTA = frame >= ENGAGEMENT_CTA_START;

{isEngagementCTA && (
  <div style={{
    position: 'absolute',
    top: 600,
    left: 40,
    right: 160, // Clear right side for TikTok buttons
    textAlign: 'center',
    opacity: interpolate(frame, [ENGAGEMENT_CTA_START, ENGAGEMENT_CTA_START + 15], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }),
  }}>
    <div style={{
      backgroundColor: COLORS.surface,
      border: `3px solid ${COLORS.primary}`,
      borderRadius: 24,
      padding: '32px 40px',
    }}>
      <div style={{ fontSize: 44, fontWeight: 700, color: COLORS.text, display: 'block' }}>
        Which one surprised you?
      </div>
      <div style={{ fontSize: 48, fontWeight: 800, color: COLORS.primary, marginTop: 16, display: 'block' }}>
        Comment below 💬
      </div>
    </div>
  </div>
)}
```

**Engagement CTA templates:**
- Opinion: "Which one surprised you? Comment below 💬"
- Save: "Save this for later 🔖"
- Follow: "Follow for more AI tips ➕"
- Share: "Send this to a dev friend 📤"
- Question: "What would you add? 👇"

#### Loop Engineering

TikTok rewards replays. Design the ending to visually flow back to the start:

```tsx
// Last 15 frames: fade content to match the opening visual state
const loopFade = frame >= TOTAL_FRAMES - 15
  ? interpolate(frame, [TOTAL_FRAMES - 15, TOTAL_FRAMES], [1, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  : 1;

// Apply to scene wrapper
<div style={{ opacity: loopFade }}>
  {/* scene content */}
</div>
```

#### Mandatory Captions

TikTok videos MUST include captions. Use the `ShortsCaptions` component with TikTok-optimized settings:

```tsx
import { ShortsCaptions } from '../../shared/components';
import syncData from './scripts/scene01-sync.json';

// In Composition.tsx — captions are MANDATORY for TikTok
<ShortsCaptions
  syncData={syncData}
  audioOffset={AUDIO_OFFSET}
  style="tiktok"           // Word-by-word karaoke (TikTok-native)
  activeColor="#FFD700"     // Yellow highlight (highest engagement on TikTok)
  bottomOffset={500}        // Higher than Shorts (500 vs 420) to avoid TikTok UI
  totalFrames={TOTAL_FRAMES}
/>
```

### Step 9: Create Composition.tsx

```typescript
import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { ShortsCaptions } from '../../shared/components';
import { BrandWatermark } from '../../shared/components/BrandWatermark';
import { AUDIO_FILES, AUDIO_OFFSET, TOTAL_FRAMES } from './constants/timing';
import { Scene01Main } from './scenes/Scene01Main';
import syncData from './scripts/scene01-sync.json';

export const <Title>Composition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0D1117' }}>
      {/* Main scene */}
      <Sequence durationInFrames={TOTAL_FRAMES}>
        <Scene01Main />
      </Sequence>

      {/* Audio */}
      <Sequence from={AUDIO_OFFSET} durationInFrames={TOTAL_FRAMES - AUDIO_OFFSET}>
        <Audio src={staticFile(AUDIO_FILES.scene01)} />
      </Sequence>

      {/* Captions — MANDATORY for TikTok */}
      <ShortsCaptions
        syncData={syncData}
        audioOffset={AUDIO_OFFSET}
        style="tiktok"
        activeColor="#FFD700"
        bottomOffset={500}
        totalFrames={TOTAL_FRAMES}
      />

      {/* Brand watermark — smaller, avoid TikTok buttons */}
      <BrandWatermark size={160} opacity={0.10} />
    </AbsoluteFill>
  );
};
```

### Step 10: Register in Root.tsx

```typescript
// Import
import { <Title>Composition } from './<Name>TikTok/<Title>/Composition';
import {
  TOTAL_FRAMES as <TITLE>_TOTAL_FRAMES,
  WIDTH as <TITLE>_WIDTH,
  HEIGHT as <TITLE>_HEIGHT,
} from './<Name>TikTok/<Title>/constants/timing';

// Register — prefix with source name + "TikTok"
<Composition
  id="$ARGUMENTS-TikTok-<Title>"
  component={<Title>Composition}
  durationInFrames={<TITLE>_TOTAL_FRAMES}
  fps={30}
  width={<TITLE>_WIDTH}
  height={<TITLE>_HEIGHT}
/>
```

### Step 11: Generate TikTok Metadata

Create `src/<Name>TikTok/<Title>/metadata.md`:

```markdown
# TikTok Metadata for <Title>

## Caption (Description)
[Engagement hook — first 80 chars are visible before truncation]
[1-2 lines of value or context]
[Engagement question to drive comments]

#Tag1 #Tag2 #Tag3 #Tag4 #Tag5

## Hashtags (3-5 max)
- 1 broad trend: #AITools or #TechTok or #LearnOnTikTok
- 2 niche topic: #ClaudeAI #AICoding
- 1 community: #DevTok or #CodeTok
- 1 branded (optional): #DIYSmartCode

## Cover Frame
Frame [N] — [description of what's visible]
(Use COVER_FRAME from timing.ts)

## Sound Strategy
- Primary: Original TTS voiceover
- Optional: Add trending TikTok sound at 15-20% volume via FFmpeg post-render

## Engagement CTA Style
[Which engagement CTA template was used: opinion/save/follow/share/question]
```

**TikTok Caption (Description) Rules:**
- First 80 characters are the hook (all that's visible before "...more")
- Max 2,200 characters total
- 3-5 hashtags (more dilutes reach)
- NO links (not clickable under 1K followers)
- NO YouTube references
- Write for engagement, not SEO
- Include a question or opinion prompt to drive comments

**Example:**

```markdown
## Caption (Description)
Your AI now decides how hard to think — and it's a game changer ⚡

4 effort levels. Zero config. The model picks the right one automatically.

Which level would you use most? 👇

#AICoding #ClaudeAI #DevTok #TechTok #LearnOnTikTok
```

### Step 12: Optional — Background Music Post-Processing

TikTok videos with background music get ~98% more views. Add a subtle music layer after rendering:

```bash
# After rendering the TikTok video, optionally add background music:
powershell.exe -Command "
& 'C:\Program Files\FFmpeg\bin\ffmpeg.exe' `
  -i 'out/<name>/tiktok.mp4' `
  -i 'public/audio/music/<track>.mp3' `
  -filter_complex '[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=shortest[out]' `
  -map '0:v' -map '[out]' `
  -c:v copy -c:a aac -y `
  'out/<name>/tiktok-with-music.mp4' 2>&1
Write-Host 'EXIT:' `$LASTEXITCODE
"
```

This step is OPTIONAL. Ask the user if they want background music added.

</process>

<tiktok-vs-shorts-checklist>

## Quick Checklist: TikTok Adaptations from Shorts

| Feature | YouTube Shorts | TikTok |
|---------|---------------|--------|
| Safe zone top | y=60 | y=300 (username/follow) |
| Safe zone bottom | y=1280 | y=1400 (action buttons) |
| Right margin | Normal | 120px clear (like/comment/share) |
| End CTA | "Full video below 👇" | Engagement CTA (comment/save/follow) |
| Captions | Optional (recommended) | MANDATORY (karaoke style) |
| Caption bottomOffset | 420px | 500px |
| Caption activeColor | Green (#39E508) | Yellow (#FFD700) |
| Hashtags | 10-15+ | 3-5 max |
| Description | SEO-optimized, links | Engagement hook, no links |
| Thumbnail | Frame 0 (mandatory) | Cover frame (selectable) |
| Loop design | Not required | Recommended (fade back to start) |
| Background music | Not common | Highly recommended (15-20% vol) |
| BrandWatermark size | 180 | 160 (avoid button overlap) |
| Duration sweet spot | 15-60s | 45-75s (educational) |
| First impression | 3 seconds | 1.5 seconds |
| Directory suffix | `<Name>Shorts/` | `<Name>TikTok/` |
| Composition ID prefix | `<Name>-<Title>` | `<Name>-TikTok-<Title>` |

</tiktok-vs-shorts-checklist>

<adapting-existing-short>

## Fast Path: Adapting an Existing Short to TikTok

If `$ARGUMENTS` points to an existing Shorts composition (e.g., `ClaudeOpus46Shorts/AdaptiveThinking`):

1. **Copy the Short's directory** to `<Name>TikTok/<Title>/`
2. **Adjust safe zones** in scene components:
   - Move title from y=60 to y=300
   - Ensure right margin clears 120px
   - Move content cards into y=440-1000 range
3. **Replace the end CTA**:
   - Remove "Full video below 👇"
   - Add engagement CTA ("Comment below 💬", "Save for later 🔖", etc.)
4. **Add/update captions**:
   - Ensure `ShortsCaptions` is included
   - Change `bottomOffset` from 420 to 500
   - Change `activeColor` to `#FFD700` (yellow)
5. **Add loop fade** to last 15 frames
6. **Reduce BrandWatermark** from `size={180}` to `size={160}`
7. **Create TikTok metadata.md** (NOT YouTube metadata)
8. **Reuse audio** — no re-generation needed
9. **Register in Root.tsx** with `TikTok` prefix in composition ID

</adapting-existing-short>

<output>
**Files created**:
```
src/<Name>TikTok/<Title>/
├── Composition.tsx
├── metadata.md           # TikTok caption, hashtags, cover frame
├── constants/
│   ├── timing.ts
│   └── colors.ts
├── scenes/
│   └── Scene01*.tsx
└── scripts/
    ├── scene-01-<name>.txt  (if new audio generated)
    └── scene01-sync.json

public/audio/<source>-tiktok/<title>/
└── scene01.mp3              (if new audio generated)
```

**Root.tsx updated**: New composition registered with `TikTok` in ID

**Report to user**:
1. TikTok title and composition ID
2. Duration (frames and seconds)
3. Source (long-form scenes or adapted Short)
4. Engagement CTA style used
5. Caption style and color
6. TikTok metadata summary (caption hook + hashtags)
7. Preview command: `pnpm dev` then select composition
8. Render command: `pnpm exec remotion render $ARGUMENTS-TikTok-<Title> out/<name>/tiktok.mp4 --codec h264 --crf 15 --color-space bt709 --x264-preset slow`
9. Optional: background music command

**Next steps**:
- Preview in Remotion Studio
- Render and verify safe zones visually
- Optional: add background music via FFmpeg
- Copy metadata from `metadata.md` when uploading to TikTok
- Select cover frame in TikTok app (reference COVER_FRAME in timing.ts)
</output>
