---
description: "Create a Claude Code version update video from release notes"
argument-hint: <Version tag or changelog URL, e.g., v2.1.20 or https://github.com/marckrenn/claude-code-changelog/releases/tag/v2.1.20>
---

<objective>
Create a Claude Code version update video using the standardized template.
This command produces consistent, branded videos for each Claude Code release.

**Input**: Version tag or changelog URL. Primary source is now the community changelog at `https://github.com/marckrenn/claude-code-changelog/tags` — it mirrors every Claude Code release AND includes curated **Highlights** sections we use directly. Accept either a bare version (`v2.1.20`) or a full tag URL (`https://github.com/marckrenn/claude-code-changelog/releases/tag/v2.1.20`).
**Output**: `out/ClaudeCodeVXYZ/claude_code_version_XYZ.mp4` (e.g., `claude_code_version_2120.mp4`)

**Template**: Use `src/ClaudeCodeV2121-25/` as the reference template.

**Duration and scene count are DYNAMIC based on release content:**

| Total Changes | Approx Duration | Word Count | Scene Count |
|---------------|-----------------|------------|-------------|
| ≤10 changes | ~75s | ~190 words | 5-6 |
| 11-20 changes | ~120s | ~300 words | 7-8 |
| 21-30 changes | ~180s | ~450 words | 9-10 |
| 30+ changes | ~300s | ~750 words | 11-12 |

**Categories are derived from actual release content** - NOT a fixed list. Group related changes together. Examples of possible categories (use only what applies):
- Security/Auth, Proxy/Network, Cloud Providers
- CI/CD, Automation, Flags
- VS Code, IDE Integration, Editor Features
- Developer Experience, UX, Progress Indicators
- Task Management, Session Handling
- Performance, Memory, Speed
- Bug Fixes (grouped by area)
- Quality of Life, Polish, Small Fixes

**Video Structure (fixed elements):**
- Scene 01: First content category — opens with stats only (e.g., "Five new features, thirty fixes, seven improvements"), then immediately dives into the first category's content. NO separate overview/stats-only scene. Do NOT mention the version number in speech — the audience already knows it from the thumbnail and title. The version badge is shown visually on screen.
- Scenes 02-N: **Remaining categories derived from release content** (varies per release)
- Final Scene: CTA - Update command and subscribe
- Outro: Brand outro video (8s)

**IMPORTANT: NO overview-only scene, NO silent intro, and NO spoken version number in the opener.** The first scene must contain real content (the first category). Start with stats counts (~3s) then transition directly into the category. The version is conveyed visually via the version badge — saying it aloud wastes time and is redundant with the thumbnail/title.

**MANDATORY COMPONENTS:**
- BrandWatermark - Logo watermark with corner cycling
- OutroSequence - Brand outro video as final scene
- VersionBranding - Anthropic + Claude Code logos (top-right) + GitHub releases URL (bottom-right). Copy from template `components/VersionBranding.tsx`. Uses `images/anthropic/Anthropic logo - Ivory.svg` and `images/anthropic/Claude Code logo - Ivory.svg`. **CRITICAL**: The bottom-right version string MUST import `VERSION` from `../constants/timing` — do NOT hardcode the version string. Pattern: `` {`github.com/anthropics/claude-code/releases  |  ${VERSION}`} ``. Hardcoded version strings have been a recurring bug on every new video (the template gets copied and the hardcoded version leaks through).
- DynamousBanner - ONE appearance at ~50% of video (270 frames), position `bottom-center`
- DynamousCourse - ONE appearance, staggered 60 frames after DynamousBanner (300 frames, 1s longer than banner), position `bottom-right`
- WatchNextMidroll - **MANDATORY once per video at ~30% mark.** 5-second full-screen recommendation card promoting another video. Uses gap-insert pattern in TransitionSeries (blank 150-frame Sequence) + absolute Sequence overlay. **ALWAYS ask the user** for: (1) video title, (2) thumbnail image path or description, (3) accent color. Import from `../shared/components/WatchNextMidroll`. SFX: `cinematic-whoosh.mp3` at gap start. See `src/ClaudeCodeV2173-74/Composition.tsx` for reference implementation with custom `WatchNextWorkshop` variant.
</objective>

<process>

## Step 0: Check if Video Already Exists

1. Parse the URL from "$ARGUMENTS" to extract the version number (e.g., `v2.1.20`)
2. Derive folder name: `ClaudeCodeV` + version without dots (e.g., `v2.1.20` → `ClaudeCodeV2120`)
3. Check if `src/<FolderName>/` directory already exists
4. **If exists**:
   - Report to user: "A video for Claude Code <version> already exists at src/<FolderName>/"
   - List existing files
   - **STOP execution** - do not proceed with any further steps
5. **If not exists**: Continue to Step 1

## Step 1: Extract Release Info

**Two sources — use BOTH**:
1. **marckrenn's changelog** (`https://github.com/marckrenn/claude-code-changelog`) — curated **Highlights** section per tag. Does NOT list every change, but tells us what matters most. Each tag page also contains a `Source:` link pointing to the exact anchor in the official CHANGELOG.md (e.g., `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2198`).
2. **Official CHANGELOG.md** — the complete list of every fix/feature/improvement for that version. This is where we get the full change inventory.

Process:

1. Normalize the input:
   - Bare version `v2.1.20` → `https://github.com/marckrenn/claude-code-changelog/releases/tag/v2.1.20`
   - Full tag URL → use directly
2. WebFetch the marckrenn tag page. Extract:
   - **Highlights section** (verbatim — the curated "what matters most" list)
   - The `Source:` link to the official CHANGELOG.md anchor
3. WebFetch the official CHANGELOG.md using the Source link (or fall back to `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md` and scroll to the version anchor). Extract:
   - Version number(s)
   - Complete list of bug fixes, new features, improvements
   - Breaking changes (if any)
4. Merge: highlights drive the Scene02 highlights scene; the full official list drives the category scenes and stats counts.
5. Determine release size category and corresponding scene count.

## Step 1.5: Ask User for WatchNext Video Promotion

**MANDATORY — STOP and ask the user before proceeding:**

Use AskUserQuestion to ask all three questions at once:

> "For the WatchNext midroll (5-second video recommendation at ~30% mark), I need:
> 1. **Video title** — What video should we promote? (e.g., "Claude Code Workshop")
> 2. **Thumbnail** — Path to thumbnail image, or describe it and I'll generate one
> 3. **Accent color** — Color for the border/label (default: `#58A6FF` cyan)
>
> This appears as a full-screen recommendation card with your profile pic, the thumbnail, and the title."

Store the answers for use in Step 8 (Composition). If the user provides a thumbnail description instead of a path, generate the thumbnail image using `generate-image.py` before Step 8.

## Step 1.6: Confirm Highlights (Pre-extracted from marckrenn's Changelog)

The marckrenn changelog already contains a curated **Highlights** section — use it directly instead of asking the user to invent items.

1. Present the extracted highlights to the user via AskUserQuestion:

> "The marckrenn changelog lists these highlights for vX.Y.Z:
> 1. <highlight 1>
> 2. <highlight 2>
> 3. <highlight 3>
> ...
>
> Use these as the **Highlights scene**? (yes / edit / skip)"

2. Branches:
   - **yes** → use verbatim for Step 4/7/8
   - **edit** → let user add/remove/rename items
   - **skip** → no highlights scene
   - If the changelog has NO Highlights section (rare/old versions), fall back to asking the user to provide them manually

**If the user provides highlights:**
- Store them for Step 4 (script), Step 7 (scene), and Step 8 (composition)
- Add a dedicated `Scene02Highlights.tsx` immediately after Scene 01 (stats opener + first category)
- The highlights scene uses FeatureCard components with spring-staggered entrances, ~15-20s, ~40-50 words
- Narration format: "Before we dive in, here's what matters most in this release." Then read each highlight with a brief one-line context.
- Shift all subsequent scene indices by +1

**If the user declines or provides nothing:**
- Skip the highlights scene entirely — do NOT create `Scene02Highlights.tsx`
- Do NOT mention highlights in the script
- Proceed with the normal scene flow

## Step 2: Copy Template Structure

1. Create folder `src/<FolderName>/` with subdirectories:
   - `research/`
   - `constants/`
   - `components/`
   - `scenes/`
   - `scripts/`

2. Copy component files from `src/ClaudeCodeV2121-25/components/` to the new folder:
   - SceneBackground.tsx
   - TerminalWindow.tsx
   - VersionBranding.tsx
   - VersionBadge.tsx
   - FeatureCard.tsx
   - CodeBlock.tsx
   - CheckmarkIcon.tsx
   - StatCounter.tsx

3. Copy constant files from `src/ClaudeCodeV2121-25/constants/`:
   - colors.ts
   - fonts.ts
   - springs.ts

## Step 3: Research & Content Brief

1. **Analyze the release notes and derive categories from actual content:**
   - Read ALL changes (bug fixes, features, improvements)
   - Group related changes together naturally
   - Create category names that describe the actual grouped content
   - **Do NOT use a fixed list of categories** - let the release content determine the groupings

2. **Determine scene count based on content:**
   - Count total changes (bug fixes + features + improvements)
   - Use the duration/scene table above as a guide
   - Merge small categories, split large ones to balance scenes

3. For each derived category, identify:
   - Key changes to highlight (2-4 per scene)
   - Visual representation (terminal, code block, feature cards, stats)
   - Punchy tagline summarizing the category

4. Write `src/<FolderName>/research/content-brief.md` with:
   - Version summary and stats
   - Derived categories with grouped changes
   - Scene count decision and rationale

## Step 4: Write Scripts

1. **MANDATORY**: Invoke `elevenlabs-tts-optimizer` skill for TTS optimization rules

2. Write `src/<FolderName>/scripts/full-script.md` with all scenes:

   ```markdown
   # Claude Code vX.Y.Z - Full Script

   ## Video Overview
   - **Duration**: ~XXX seconds
   - **Versions Covered**: vX.Y.Z
   - **Word Count Target**: ~XXX words
   - **Scenes**: N + outro

   ---

   ## Scene 01: [First Category Name] (~25-30s, ~63-75 words)
   *Opens with stats counts only (e.g., "Five new features, thirty fixes, seven improvements"), then immediately dives into the first category's content. Do NOT say the version number aloud — it's shown visually via the version badge. NO separate overview scene.*

   [Stats counts + first category content]

   ---

   ## Scene 02: [Second Category Name] (~25s, ~63 words)

   [Category content]

   ---

   [Continue for all scenes...]

   ## Scene N: CTA (~20s, ~50 words)

   [Update command, social proof, subscribe CTA]

   ---

   ## Outro (8s)
   *Logo fade, branding*

   ---

   ## Total Word Count: ~XXX words
   ## Estimated Duration: ~XXX seconds
   ```

3. Apply TTS optimization:
   - Spell out acronyms: API → A P I, CPU → C P U, CLI → C L I, IDE → I D E
   - BUT NOT "AI" — ElevenLabs handles it naturally
   - Technical terms phonetically: nginx → engine-x, venv → v-env
   - Numbers as words: 2.1.20 → two point one point twenty
   - Em-dashes for mid-sentence pauses
   - No ALL CAPS

4. Create individual scene scripts in `src/<FolderName>/scripts/`:
   - `scene-01-overview.txt`
   - `scene-02-<category>.txt`
   - `scene-03-<category>.txt`
   - ... (one per scene)
   - `scene-NN-cta.txt`

## Step 5: Generate Audio

1. Verify `.env` has ELEVENLABS_API_KEY
2. Create audio output directory: `public/audio/<foldername>/` (lowercase)
3. Run batch generation:
   ```bash
   python generate-all-audio.py <FolderName>
   ```
4. Read generated sync JSON files from `src/<FolderName>/scripts/`
5. Note the last_word.end from each sync file for timing calculations

## Step 6: Create Timing Constants

Write `src/<FolderName>/constants/timing.ts`:

**CRITICAL: TransitionSeries Overlap Timing**

TransitionSeries creates overlaps between scenes. Each transition overlaps by `TRANSITION_DURATION` frames.
The `SCENES.start` values must account for this or audio will be out of sync!

```
Formula for scene start (accounting for overlaps):
scene[n].start = scene[n-1].start + scene[n-1].duration - TRANSITION_DURATION
```

**Scene Duration Formula (exact timestamp-based):**
```
scene_duration = AUDIO_OFFSET + ceil(last_word.end * FPS) + TRANSITION_DURATION
```

**IMPORTANT:** Read `last_word.end` directly from the sync JSON file - do not estimate.

```typescript
/**
 * Timing constants for ClaudeCodeVXYZ composition
 * Technical release notes showcase - N scenes
 */

export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export const VERSION = 'vX.Y.Z';
export const PRODUCT_NAME = 'Claude Code';

export const AUDIO_OFFSET_FIRST = 15;
export const AUDIO_OFFSET_REST = 10;
export const TRANSITION_DURATION = 15;

// Scene durations from sync JSON (last_word.end):
// scene01: XX.XXs, scene02: XX.XXs, ...
export const SCENES = {
  overview: { start: 0, duration: XXX },          // XX.XXs audio
  [category1]: { start: XXX, duration: XXX },     // XX.XXs audio
  [category2]: { start: XXX, duration: XXX },     // XX.XXs audio
  // ... more scenes
  cta: { start: XXX, duration: XXX },             // XX.XXs audio
} as const;

export const OUTRO_DURATION = 240;
export const TOTAL_FRAMES = XXXX; // ~XXX seconds

export const getAudioOffset = (sceneNumber: number): number => {
  return sceneNumber === 1 ? AUDIO_OFFSET_FIRST : AUDIO_OFFSET_REST;
};

export type SceneName = keyof typeof SCENES;
export const SCENE_NAMES: SceneName[] = [
  'overview',
  // ... all scene names
  'cta',
];
```

## Step 7: Build Scene Components

Create scene files in `src/<FolderName>/scenes/`:

**IMPORTANT: Do NOT create a separate overview/stats-only scene. Scene 01 IS the first content category.** The video opens with stats counts only (~3 seconds of speech, e.g., "Five new features, thirty fixes, seven improvements"), then immediately covers the first category's content. Do NOT say the version number aloud — the version is shown visually via the version badge on screen. Viewers already know the version from the thumbnail and title.

### Scene01[FirstCategory].tsx
First content category scene. Opens with:
- Stats counts spoken aloud (~3s) — NO version number in speech (shown visually via badge)
- Version badge + "Claude Code" title displayed on screen while stats are spoken
- Immediately transitions into the first category's feature cards/content
- The stats act as a brief header, NOT a full separate scene

### Scene02-N: Remaining Category Scenes
Adapt based on content type:

**For lists of fixes/features** - Use FeatureCard components:
```tsx
<FeatureCard icon={<Icon />} title="Feature Name" description="What it does" />
```

**For terminal commands** - Use TerminalWindow component:
```tsx
<TerminalWindow title="Terminal">
  <CodeBlock code="claude update" />
</TerminalWindow>
```

**For before/after** - Use CodeBlock with strikethrough:
```tsx
<CodeBlock code="old code" strikethrough />
<CodeBlock code="new code" highlight />
```

**For stats/numbers** - Use StatCounter component:
```tsx
<StatCounter value={19} label="Bug Fixes" />
```

### SceneNNCTA.tsx
Call-to-action finale:
- Terminal showing `claude update` command
- Social proof: "X developers already starred the repo"
- Subscribe CTA with button visual

### Animation Pattern (use in ALL scenes):
```typescript
// Word timings from sync JSON (frame = seconds * 30 + AUDIO_OFFSET)
const TIMINGS = {
  title: AUDIO_OFFSET,
  [keyword]: Math.round(X.XXX * FPS) + AUDIO_OFFSET,
  // ... more keywords
};

// Animation pattern
const progress = spring({
  frame: frame - TIMINGS.keyword,
  fps,
  config: SPRINGS.snappy,
});

const opacity = interpolate(progress, [0, 1], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

## Step 8: Create Composition

Write `src/<FolderName>/Composition.tsx`:

```typescript
import { AbsoluteFill, Audio, Img, Sequence, staticFile } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

import {
  SCENES,
  AUDIO_OFFSET_FIRST,
  AUDIO_OFFSET_REST,
  TRANSITION_DURATION,
  OUTRO_DURATION,
  VERSION,
  PRODUCT_NAME,
} from './constants/timing';

// Import all scenes
import { Scene01Overview } from './scenes/Scene01Overview';
// ... more scenes
import { SceneNNCTA } from './scenes/SceneNNCTA';

import { BrandWatermark, OutroSequence, DynamousBanner } from '../shared/components';
import { DynamousCourse } from '../shared/components/DynamousCourse';
import { WatchNextMidroll, WATCH_NEXT_MIDROLL_DURATION } from '../shared/components/WatchNextMidroll';
import { VersionBranding } from './components/VersionBranding';

// Audio configuration — Scene 01 is the first content category (no separate overview)
const AUDIO_FILES = [
  { src: 'audio/<foldername>/scene01.mp3', from: SCENES.[category1].start + AUDIO_OFFSET_FIRST },
  { src: 'audio/<foldername>/scene02.mp3', from: SCENES.[category2].start + AUDIO_OFFSET_REST },
  // ... more audio files
];

// Calculate Dynamous placement — ONE appearance at ~50% of video
const DYNAMOUS_BANNER_DURATION = 270;
const DYNAMOUS_COURSE_DURATION = 300; // 1 second longer than banner
const DYNAMOUS_BANNER_START = Math.round(SCENES.[~50% scene].start + 100);

export const ClaudeCodeVXYZComposition: React.FC = () => {
  const t = TRANSITION_DURATION;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0D1117' }}>
      {/* Scene transitions — NO separate overview scene */}
      <TransitionSeries>
        {/* Scene 01: First Category (opens with quick version mention) */}
        <TransitionSeries.Sequence durationInFrames={SCENES.[category1].duration}>
          <Scene01[Category1] />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />

        {/* Continue with scenes until ~30% mark... */}
        {/* Alternate between fade() and slide({ direction: 'from-right' }) for variety */}

        {/* MANDATORY: WatchNext gap at ~30% — blank placeholder for overlay */}
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />
        <TransitionSeries.Sequence durationInFrames={WATCH_NEXT_GAP}>
          <AbsoluteFill style={{ backgroundColor: '#0D1117' }} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />

        {/* Continue with remaining scenes... */}

        {/* Outro */}
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: t })}
        />
        <TransitionSeries.Sequence durationInFrames={OUTRO_DURATION}>
          <OutroSequence />
        </TransitionSeries.Sequence>
      </TransitionSeries>

      {/* Background music - plays for entire video */}
      <Audio src={staticFile('audio/shared/Binary Horizons.wav')} volume={0.05} />

      {/* Audio layer - each scene's narration */}
      {AUDIO_FILES.map(({ src, from }) => (
        <Sequence key={src} from={from}>
          <Audio src={staticFile(src)} />
        </Sequence>
      ))}

      {/* MANDATORY: Dynamous promotion — ONE appearance at ~50% of video */}
      <Sequence from={DYNAMOUS_BANNER_START} durationInFrames={DYNAMOUS_BANNER_DURATION}>
        <DynamousBanner position="bottom-center" />
        <Audio src={staticFile('sfx/final/emphasis/spring-pop.mp3')} volume={0.6} />
      </Sequence>
      <Sequence from={DYNAMOUS_BANNER_START + 60} durationInFrames={DYNAMOUS_COURSE_DURATION}>
        <DynamousCourse position="bottom-right" />
        <Audio src={staticFile('sfx/final/emphasis/spring-pop.mp3')} volume={0.55} />
      </Sequence>

      {/* MANDATORY: WatchNext midroll — overlay at ~30% of video */}
      {/* WATCH_NEXT_START = the frame where the gap starts in TransitionSeries */}
      <Sequence from={WATCH_NEXT_START} durationInFrames={WATCH_NEXT_GAP}>
        <WatchNextMidroll
          thumbnailSrc={staticFile('images/<foldername>/<thumbnail-filename>')}
          videoTitle="<User-provided video title>"
          accentColor="#58A6FF"
        />
      </Sequence>
      <Sequence from={WATCH_NEXT_START} durationInFrames={20}>
        <Audio src={staticFile('sfx/final/intro-outro/cinematic-whoosh.mp3')} volume={0.4} />
      </Sequence>

      {/* Brand watermark - MANDATORY */}
      <BrandWatermark />

      {/* Version branding (Anthropic + Claude Code logos top-right, GitHub URL bottom-right) */}
      <VersionBranding />
    </AbsoluteFill>
  );
};
```

## Step 9: Register & Validate

1. Update `src/Root.tsx` to register the new composition:
   ```typescript
   import { ClaudeCodeVXYZComposition } from './ClaudeCodeVXYZ/Composition';
   import { TOTAL_FRAMES as VXYZ_TOTAL_FRAMES } from './ClaudeCodeVXYZ/constants/timing';

   <Composition
     id="ClaudeCodeVXYZ"
     component={ClaudeCodeVXYZComposition}
     durationInFrames={VXYZ_TOTAL_FRAMES}
     fps={30}
     width={1920}
     height={1080}
   />
   ```

2. Run lint check:
   ```bash
   pnpm lint
   ```
3. Fix any TypeScript or ESLint errors

4. Preview in Remotion Studio:
   ```bash
   pnpm dev
   ```

## Step 9.5: YouTube Description (SEO-Optimized)

Write `src/<FolderName>/youtube-description.md` following ALL rules from `.claude/rules/youtube-metadata.md`. This is NOT optional — every description must be fully SEO-optimized by default.

**Required structure (in order):**

1. **Hook paragraph (first 200 chars = keywords)**: Must contain "Claude Code", version number, and 2-3 key features/stats. This is what shows in search results before "Show more."
   ```
   Claude Code v2.1.72 ships 14 new features, 30 bug fixes, and 7 improvements — including /plan arguments, a 12x prompt cache cost reduction, 510KB smaller bundle, and native bash parsing. Full breakdown of every change.
   ```

2. **Dynamous CTA** (wrapped in `----` separators)

3. **SEO-optimized chapter titles** (MANDATORY — never use generic labels):
   - Front-load the searchable keyword/concept
   - Include specific numbers, tool names, or API names
   - Each chapter title must work as a standalone search result
   ```
   BAD:  0:11 Developer Experience
   GOOD: 0:11 /plan Arguments, /config Redesign, and Effort Levels (DX)

   BAD:  1:08 Performance
   GOOD: 1:08 12x Prompt Cache Savings and 510KB Bundle Reduction
   ```

4. **Key concepts section**: 3-5 keyword-dense bullet points explaining what the release covers. Each bullet is a search term opportunity.
   ```
   Key Changes in This Release:
   - Bash auto-approval: 6 new commands (lsof, pgrep, tput, ss, fd, fdfind) skip permission prompts
   - Prompt cache fix: SDK query() calls now cache correctly, reducing input token costs up to 12x
   - Plugin stability: Windows OneDrive EEXIST error, marketplace scope blocking, and tilde cache paths all resolved
   ```

5. **Links with keyword-rich context** (not bare URLs):
   ```
   Release Notes (v2.1.72): https://github.com/anthropics/claude-code/releases/tag/v2.1.72
   Claude Code on GitHub (75K+ stars): https://github.com/anthropics/claude-code
   ```

6. **Footer** with update command

7. **Engagement CTA**: A specific, debate-sparking question from the video content — NOT "What do you think?"
   ```
   Which fix were you waiting for the most? Drop it in the comments.
   ```

8. **Hashtags**: 15-25 relevant hashtags mixing specific (#ClaudeCode #PromptCache) with broad (#DevTools #AI)

**Chapter timestamp formula**: `timestamp_seconds = SCENES.<scene>.start / FPS`, format as `M:SS`.

## Step 9.7: Generate Thumbnail Manifest

**MANDATORY** — create `public/images/<foldername>/thumbnail-manifest.json` using this exact template, adapting only the version number, stats, and 3 key items per card:

```json
{
  "composition": "ClaudeCodeVXYZ",
  "title": "Claude Code vX.Y.Z",
  "reference_image": "Use reference face photo — creator bottom center, waist-up, right hand extended palm-up in a casual presenting gesture toward the center card. Wearing red hoodie. Looking at camera with calm, approachable expression. No dramatic lighting — just soft, even lighting matching the dark background.",
  "psychology_hook": "Clean informational thumbnail. Returning viewers recognize the consistent format and click for the update. Stats speak for themselves.",
  "facial_expression": "Calm, natural, approachable. Slight confident smile, direct eye contact. Casual palm-up gesture with right hand. Not performative — just presenting the info.",
  "concept": "EXACT replica of the v2.1.72 thumbnail layout with updated numbers. Background: dark navy (#0D1117) with very subtle circuit board trace pattern in slightly lighter navy on the right side only, barely visible. TOP CENTER: Anthropic asterisk logo (orange/coral) on the left, 'Claude Code' text in large white serif-style font to the right of it — same as the reference image, spanning most of the width. Below that: dark glass pill badge with rounded corners, 'vX.Y.Z' in white text, centered. THREE GLASS CARDS in a row below the version badge, evenly spaced: LEFT CARD — glass morphism with cyan (#58A6FF) left border accent (vertical bar), dark glass background. 'N' in large bold cyan, 'Features' below in white. Then three key items in smaller gray text: '<feature1>', '<feature2>', '<feature3>'. CENTER CARD — glass morphism with green (#3FB950) left border accent, slightly green-tinted glass background. 'N' in large bold green, 'Bug Fixes' below in white. Key items: '<fix1>', '<fix2>', '<fix3>'. RIGHT CARD — glass morphism with purple (#A371F7) left border accent, slightly purple-tinted glass background. 'N' in large bold purple, 'Improved' below in white. Key items: '<improvement1>', '<improvement2>', '<improvement3>'. Creator photo bottom center overlapping the cards from below, same pose as reference. 1920x1080.",
  "logo_references": [
    "public/images/anthropic/Claude Code logo - Ivory.svg",
    "public/images/anthropic/Anthropic logo - Ivory.svg"
  ],
  "width": 1920,
  "height": 1080,
  "style_primary": "split-comparison",
  "text_overlay": {
    "enabled": true,
    "words": ["vX.Y.Z"],
    "position": "top-center",
    "note": "Use Claude Code logo for the title"
  },
  "brand_colors": {
    "primary": "#58A6FF",
    "accent": "#A371F7",
    "secondary": "#fbbf24",
    "success": "#3FB950"
  },
  "face_reference": {
    "enabled": true,
    "reference_dir": "public/reference-faces/creator/",
    "model": "diysmartcode",
    "expression": "calm-confident"
  }
}
```

**Card key items**: Pick the 3 most impactful/recognizable items from each category. Use short labels (2-3 words max). Features = new capabilities, Bug Fixes = most notable fixes, Improved = quality-of-life improvements.

## Step 10: Render

Ask user before rendering, then render with **high quality settings**:
```bash
pnpm exec remotion render <CompositionId> out/<FolderName>/claude_code_version_<version>.mp4 --codec h264 --crf 15 --color-space bt709 --x264-preset slow
```

Example: `out/ClaudeCodeV2120/claude_code_version_2120.mp4`

**Quality Settings Explained:**
- `--crf 15`: High quality (lower = better, 15 is excellent)
- `--color-space bt709`: Standard HD color space for YouTube/web
- `--x264-preset slow`: Better compression efficiency

</process>

<output>
**Files created**:
```
src/<FolderName>/
├── research/content-brief.md
├── constants/
│   ├── colors.ts
│   ├── fonts.ts
│   ├── springs.ts
│   └── timing.ts (with VERSION, SCENES, TOTAL_FRAMES)
├── components/ (copied from template)
│   ├── SceneBackground.tsx
│   ├── TerminalWindow.tsx
│   ├── FeatureCard.tsx
│   ├── CodeBlock.tsx
│   ├── CheckmarkIcon.tsx
│   └── StatCounter.tsx
├── scenes/
│   ├── Scene01[FirstCategory].tsx (opens with stats counts, version shown visually)
│   ├── Scene02[Category].tsx
│   ├── ... (N-2 more category scenes)
│   └── SceneNNCTA.tsx
├── scripts/
│   ├── full-script.md (complete script for review)
│   ├── scene-01-overview.txt through scene-NN-cta.txt
│   └── scene01-sync.json through sceneNN-sync.json
├── Composition.tsx
└── youtube-description.md (SEO-optimized, ready for upload)

public/audio/<foldername>/
├── scene01.mp3 through sceneNN.mp3

public/images/<foldername>/
├── thumbnail-manifest.json (thumbnail generation manifest)

out/<FolderName>/claude_code_version_<version>.mp4
```

**Report to user**:
1. Video: `out/<FolderName>/claude_code_version_<version>.mp4`
2. Version: X.Y.Z
3. Duration: ~XXX seconds (X minutes)
4. Scene count: N scenes + outro (no silent intro)
5. Features covered: [list categories]
6. DynamousBanner (bottom-center) + DynamousCourse (bottom-right): ONE appearance at ~50% of video
7. Run `pnpm dev` to preview
</output>
