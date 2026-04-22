---
description: "Create an OpenClaw version update video from release notes"
argument-hint: <GitHub release URL, e.g., https://github.com/openclaw/openclaw/releases/tag/v0.3.0>
---

<objective>
Create an OpenClaw version update video using the OpenClaw brand style.
This command produces consistent, branded videos for each OpenClaw release.

**Input**: GitHub release notes URL (e.g., `https://github.com/openclaw/openclaw/releases/tag/v0.3.0`)
**Output**: `out/OpenClawVXYZ/openclaw_version_XYZ.mp4`

**Template**: Use latest `src/ClaudeCodeV2184-85/` as structural reference, but with OpenClaw branding throughout.

**Brand Style — OpenClaw**:
OpenClaw is an open-source AI agent framework. The visual identity should feel:
- **Bold open-source energy** — community-driven, transparent, hacker-friendly
- **Color palette**: Deep navy/black background with warm amber/orange accents (claw motif)
  - Background: `#0B0F1A` (deep space)
  - Primary accent: `#F59E0B` (amber/gold — "claw" warmth)
  - Secondary accent: `#EF4444` (red — energy, breaking changes)
  - Tertiary: `#10B981` (emerald green — new features)
  - Info/links: `#38BDF8` (sky blue)
  - Text: `#F1F5F9` (slate-50)
  - Card bg: `#1E293B` (slate-800)
- **Big OpenClaw logo top-right** (logo image only, no text — 240px, prominent)
- **GitHub releases URL bottom-right** (as source attribution)
- NO Anthropic/Claude branding — this is OpenClaw's video

**Duration and scene count are DYNAMIC based on release content:**

| Highlights Extracted | Approx Duration | Word Count | Scene Count |
|---------------------|-----------------|------------|-------------|
| ≤5 highlights | ~75s | ~190 words | 5-6 |
| 6-12 highlights | ~120s | ~300 words | 7-8 |
| 13-20 highlights | ~180s | ~450 words | 9-10 |
| 20+ highlights | ~300s | ~750 words | 11-12 |

**CRITICAL: Release notes are often very long.** OpenClaw releases contain hundreds of commits, deep technical fixes, dependency bumps, and internal refactors. The video must NOT cover every detail. Step 1.5 (Extract Highlights) distills the release into viewer-worthy content.

**Video Structure (fixed elements):**
- Scene 01: Opens with stats ("X new features, Y breaking changes, Z improvements"), then immediately dives into the first content category. NO separate overview scene. Do NOT say the version number aloud — shown visually via badge.
- Scenes 02-N: **Categories derived from extracted highlights** (varies per release)
- Final Scene: CTA - pip install/upgrade command and subscribe
- Outro: Brand outro video (8s)

**IMPORTANT: NO overview-only scene, NO silent intro, NO spoken version number.**

**MANDATORY COMPONENTS:**
- BrandWatermark - Logo watermark with corner cycling
- OutroSequence - Brand outro video as final scene
- OpenClawBranding - **NEW COMPONENT**: Big OpenClaw logo (top-right, ~400px) + GitHub releases URL (bottom-right). Created per-composition from template.
- DynamousBanner - ONE appearance at ~50% of video (270 frames), position `bottom-center`
- DynamousCourse - ONE appearance, staggered 60 frames after DynamousBanner (300 frames), position `bottom-right`
- WatchNextMidroll - **MANDATORY once at ~30% mark.** Ask user for video title, thumbnail, accent color.
</objective>

<process>

## Step 0: Check if Video Already Exists

1. Parse the URL from "$ARGUMENTS" to extract the version number (e.g., `v0.3.0`)
2. Derive folder name: `OpenClawV` + version without dots (e.g., `v0.3.0` -> `OpenClawV030`)
3. Check if `src/<FolderName>/` directory already exists
4. **If exists**: Report and **STOP**
5. **If not exists**: Continue

## Step 1: Fetch Release Notes

1. Fetch the release notes page using WebFetch from the provided URL
2. Save the raw release notes text to `src/<FolderName>/research/raw-release-notes.md`
3. Note total size — OpenClaw releases can be massive (100+ commits)

## Step 1.5: Extract Highlights (CRITICAL — Content Curation)

**This is the key differentiator from claude-code-version.** OpenClaw releases are often very large with deep technical content. The video cannot cover everything — extract only what matters to viewers.

### Extraction Rules

**INCLUDE (highlight-worthy):**
- New user-facing features (new commands, new capabilities, new integrations)
- Breaking changes that affect user workflows
- Major performance improvements with measurable impact
- New provider/model support
- Security fixes that users should know about
- Notable UX/DX improvements
- New configuration options that unlock new workflows

**EXCLUDE (skip entirely):**
- Internal refactors with no user-visible impact
- Dependency version bumps (unless they unlock new features)
- CI/CD pipeline changes
- Test additions/fixes
- Code style/linting changes
- Documentation-only changes (unless major new docs)
- Typo fixes
- Minor bug fixes for edge cases most users won't hit

### Categorization

Group extracted highlights into natural categories. Examples (use only what applies):
- **Breaking Changes** (always first if present — red accent, warning tone)
- **New Features** (green accent)
- **Provider/Model Support** (new AI providers, models)
- **Performance** (speed, memory, cost improvements)
- **Developer Experience** (CLI, config, tooling)
- **Security & Auth**
- **Bug Fixes** (only notable ones that many users hit)
- **Quality of Life** (small but appreciated improvements)

### Output

Write `src/<FolderName>/research/highlights.md`:

```markdown
# OpenClaw vX.Y.Z — Extracted Highlights

## Release Stats
- Total commits/changes in release: NNN
- Highlights extracted: NN (XX% of total — rest is internal/minor)
- Breaking changes: N
- New features: N
- Notable improvements: N
- Notable bug fixes: N

## Category: [Name] (N items)
1. **[Feature/Change Name]** — One-line description of what it does and why users care
2. ...

## Category: [Name] (N items)
...

## Excluded (summary)
- N dependency bumps skipped
- N internal refactors skipped
- N test/CI changes skipped
- N minor bug fixes skipped
```

**Present highlights.md to the user for review before proceeding.** Ask:
> "I've extracted N highlights from the N total changes. Here's the breakdown — want me to add or remove anything before scripting?"

## Step 1.7: Ask User for WatchNext Video Promotion

**MANDATORY — STOP and ask the user:**

> "For the WatchNext midroll (5-second video recommendation at ~30% mark), I need:
> 1. **Video title** — What video should we promote?
> 2. **Thumbnail** — Path to thumbnail image, or describe it
> 3. **Accent color** — Color for border/label (default: `#F59E0B` amber)

## Step 2: Create Folder Structure

1. Create folder `src/<FolderName>/` with subdirectories:
   - `research/`
   - `constants/`
   - `components/`
   - `scenes/`
   - `scripts/`

2. **Create OpenClaw-specific components** (do NOT copy from ClaudeCode template):

### `components/OpenClawBranding.tsx`
```tsx
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { FONTS } from '../constants/fonts';
import { COLORS } from '../constants/colors';

export const OpenClawBranding: React.FC = () => {
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', opacity: 0.85 }}>
      {/* OpenClaw logo top-right (wide SVG — 1768x363 aspect ratio) */}
      <Img
        src={staticFile('images/shared/logos/openclaw-logo-text.svg')}
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
          width: 576,
          height: 118,
          objectFit: 'contain',
        }}
      />

      {/* Bottom-right source link */}
      <div
        style={{
          position: 'absolute',
          bottom: 28,
          right: 28,
          display: 'block',
          fontFamily: FONTS.mono,
          fontSize: 17,
          color: COLORS.secondaryText,
        }}
      >
        github.com/openclaw/openclaw/releases
      </div>
    </AbsoluteFill>
  );
};
```

### `constants/colors.ts` — OpenClaw palette
```typescript
export const COLORS = {
  // Backgrounds
  background: '#0B0F1A',
  backgroundGradient: '#111827',
  cardBackground: '#1E293B',

  // Text
  primaryText: '#F1F5F9',
  secondaryText: '#94A3B8',

  // OpenClaw accents
  accentAmber: '#F59E0B',       // Primary — claw warmth
  accentRed: '#EF4444',         // Breaking changes, warnings
  accentGreen: '#10B981',       // New features, success
  accentBlue: '#38BDF8',        // Info, links, secondary
  accentPurple: '#A78BFA',      // Tertiary

  // Semantic
  breaking: '#EF4444',
  feature: '#10B981',
  improvement: '#38BDF8',
  performance: '#F59E0B',

  // Effects
  glow: '#F59E0B33',
  glowStrong: '#F59E0B66',
  glowGreen: '#10B98133',

  // Terminal
  terminalRed: '#FF5F56',
  terminalYellow: '#FFBD2E',
  terminalGreen: '#27C93F',
} as const;
```

3. Create remaining component files adapted for OpenClaw:
   - `SceneBackground.tsx` — use OpenClaw background colors
   - `TerminalWindow.tsx` — copy from template, update colors
   - `VersionBadge.tsx` — amber/gold badge instead of cyan
   - `FeatureCard.tsx` — use OpenClaw card styling
   - `CodeBlock.tsx` — copy from template
   - `CheckmarkIcon.tsx` — copy from template
   - `StatCounter.tsx` — use amber accent

4. Create `constants/fonts.ts` and `constants/springs.ts` — same structure as template

## Step 3: Write Content Brief

Using the extracted highlights from Step 1.5:

1. Determine scene count based on highlight count (use table above)
2. Assign highlights to scenes, grouping by category
3. For each scene, identify:
   - Key highlights to cover (2-4 per scene)
   - Visual representation (terminal, code block, feature cards, stats)
   - Accent color (amber for general, red for breaking, green for features)

4. Write `src/<FolderName>/research/content-brief.md`

## Step 4: Write Scripts

1. **MANDATORY**: Invoke `elevenlabs-tts-optimizer` skill for TTS optimization rules

2. Write `src/<FolderName>/scripts/full-script.md`:

   ```markdown
   # OpenClaw vX.Y.Z - Full Script

   ## Video Overview
   - **Duration**: ~XXX seconds
   - **Version**: vX.Y.Z
   - **Highlights covered**: N of M total changes
   - **Word Count Target**: ~XXX words
   - **Scenes**: N + outro

   ---

   ## Scene 01: [First Category] (~25-30s, ~63-75 words)
   *Opens with stats ("X new features, Y breaking changes..."), then covers first category. No spoken version number.*

   [Content]

   ---
   [Continue for all scenes...]

   ## Scene N: CTA (~20s, ~50 words)
   [pip install/upgrade command, star the repo, subscribe]

   ---
   ## Outro (8s)
   ---
   ## Total Word Count: ~XXX words
   ```

3. Apply TTS optimization (same rules as claude-code-version):
   - Spell out: API -> A P I, CLI -> C L I, LLM -> L L M
   - BUT NOT "AI" — ElevenLabs handles it
   - Technical: pip -> pip (already fine), PyPI -> pie-pie
   - Numbers as words
   - Em-dashes for pauses
   - No ALL CAPS

4. Create individual scene scripts in `src/<FolderName>/scripts/`

## Step 5: Generate Audio

1. Verify `.env` has ELEVENLABS_API_KEY
2. Create `public/audio/<foldername>/` (lowercase)
3. Run: `python generate-all-audio.py <FolderName>`
4. Read sync JSON files, note `last_word.end` per scene

## Step 6: Create Timing Constants

Write `src/<FolderName>/constants/timing.ts`:

```typescript
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export const VERSION = 'vX.Y.Z';
export const PRODUCT_NAME = 'OpenClaw';

export const AUDIO_OFFSET_FIRST = 15;
export const AUDIO_OFFSET_REST = 10;
export const TRANSITION_DURATION = 15;

// Scene durations from sync JSON (last_word.end):
export const SCENES = {
  // ... scene entries with start + duration
} as const;

export const OUTRO_DURATION = 240;
export const TOTAL_FRAMES = XXXX;

export const getAudioOffset = (sceneNumber: number): number => {
  return sceneNumber === 1 ? AUDIO_OFFSET_FIRST : AUDIO_OFFSET_REST;
};

export type SceneName = keyof typeof SCENES;
export const SCENE_NAMES: SceneName[] = [/* ... */];
```

**Scene Duration Formula**: `AUDIO_OFFSET + ceil(last_word.end * FPS) + TRANSITION_DURATION`
**Scene Start Formula**: `scene[n].start = scene[n-1].start + scene[n-1].duration - TRANSITION_DURATION`

## Step 7: Build Scene Components

Create scenes in `src/<FolderName>/scenes/`:

**OpenClaw-specific visual patterns:**

- **Breaking changes**: Red-accented cards with warning icon, `border-left: 4px solid #EF4444`
- **New features**: Green-accented cards with sparkle/plus icon
- **Performance**: Amber stat counters with before/after numbers
- **Terminal commands**: `pip install openclaw --upgrade` in TerminalWindow
- **All scenes**: OpenClaw card style with `background: #1E293B`, amber glow on hover states

### Scene01[FirstCategory].tsx
Opens with stats counts + first category content. Version shown visually via VersionBadge (amber).

### Scene02-N: Category Scenes
Adapt visual treatment per category type (see above patterns).

### SceneNNCTA.tsx
- Terminal: `pip install openclaw --upgrade`
- GitHub stars social proof
- Subscribe CTA

### Animation Pattern (same as claude-code-version):
```typescript
const TIMINGS = {
  title: AUDIO_OFFSET,
  [keyword]: Math.round(X.XXX * FPS) + AUDIO_OFFSET,
};

const progress = spring({
  frame: frame - TIMINGS.keyword,
  fps,
  config: SPRINGS.snappy,
  durationRestThreshold: 0.001,
});
```

## Step 8: Create Composition

Write `src/<FolderName>/Composition.tsx`:

Key differences from claude-code-version:
- Import `OpenClawBranding` instead of `VersionBranding`
- Use OpenClaw color constants
- Background: `#0B0F1A`
- All same mandatory components (BrandWatermark, OutroSequence, DynamousBanner, etc.)

```typescript
import { OpenClawBranding } from './components/OpenClawBranding';

// ... (same TransitionSeries structure as claude-code-version)

export const OpenClawVXYZComposition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0B0F1A' }}>
      <TransitionSeries>
        {/* Scenes with LightLeakOverlay between each */}
      </TransitionSeries>

      {/* Audio layers */}
      {/* DynamousBanner + DynamousCourse at ~50% */}
      {/* WatchNextMidroll at ~30% */}
      {/* BrandWatermark */}

      {/* OpenClaw branding — big logo top-right, GitHub URL bottom-right */}
      <OpenClawBranding />
    </AbsoluteFill>
  );
};
```

## Step 9: Register & Validate

1. Update `src/Root.tsx`:
   ```typescript
   import { OpenClawVXYZComposition } from './OpenClawVXYZ/Composition';
   import { TOTAL_FRAMES as OC_VXYZ_TOTAL } from './OpenClawVXYZ/constants/timing';

   <Composition
     id="OpenClawVXYZ"
     component={OpenClawVXYZComposition}
     durationInFrames={OC_VXYZ_TOTAL}
     fps={30}
     width={1920}
     height={1080}
   />
   ```

2. Run `pnpm lint` and fix errors
3. Preview with `pnpm dev`

## Step 9.5: YouTube Description (SEO-Optimized)

Write `src/<FolderName>/youtube-description.md` following `.claude/rules/youtube-metadata.md`.

**Key differences from Claude Code descriptions:**
- Hook paragraph focuses on OpenClaw, version, headline features
- Link to OpenClaw GitHub repo and releases
- Link to OpenClaw docs if available
- Hashtags: #OpenClaw #AIAgents #OpenSource #Python etc.
- Update command: `pip install openclaw --upgrade`

## Step 9.7: Generate Thumbnail Manifest

Create `public/images/<foldername>/thumbnail-manifest.json`:

**OpenClaw thumbnail style** — warm amber/gold theme instead of Claude's blue:
- Background: deep navy `#0B0F1A` with subtle claw scratch texture
- Top center: Big OpenClaw logo + "OpenClaw" text
- Version badge: amber/gold pill
- Three glass cards: amber (Features), red (Breaking), green (Improvements)
- Creator photo bottom center

## Step 10: Render

Ask user before rendering:
```bash
pnpm exec remotion render <CompositionId> out/<FolderName>/openclaw_version_<version>.mp4 --codec h264 --image-format png --pixel-format yuv444p10le --color-space bt709 --crf 5 --x264-preset slow --hardware-acceleration disable
```

</process>

<output>
**Files created**:
```
src/<FolderName>/
├── research/
│   ├── raw-release-notes.md
│   ├── highlights.md (curated from raw notes)
│   └── content-brief.md
├── constants/
│   ├── colors.ts (OpenClaw amber/gold palette)
│   ├── fonts.ts
│   ├── springs.ts
│   └── timing.ts
├── components/
│   ├── OpenClawBranding.tsx (big logo top-right + GitHub URL)
│   ├── SceneBackground.tsx
│   ├── TerminalWindow.tsx
│   ├── VersionBadge.tsx (amber badge)
│   ├── FeatureCard.tsx
│   ├── CodeBlock.tsx
│   ├── CheckmarkIcon.tsx
│   └── StatCounter.tsx
├── scenes/
│   ├── Scene01[FirstCategory].tsx
│   ├── Scene02-N[Categories].tsx
│   └── SceneNNCTA.tsx
├── scripts/
│   ├── full-script.md
│   ├── scene-01-*.txt through scene-NN-cta.txt
│   └── scene01-sync.json through sceneNN-sync.json
├── Composition.tsx
└── youtube-description.md

public/audio/<foldername>/
├── scene01.mp3 through sceneNN.mp3

public/images/<foldername>/
├── thumbnail-manifest.json

out/<FolderName>/openclaw_version_<version>.mp4
```

**Report to user**:
1. Video: `out/<FolderName>/openclaw_version_<version>.mp4`
2. Version: X.Y.Z
3. Duration: ~XXX seconds
4. Highlights: N extracted from M total changes
5. Scene count: N scenes + outro
6. Categories covered: [list]
7. Run `pnpm dev` to preview
</output>
