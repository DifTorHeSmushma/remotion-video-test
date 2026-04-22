# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automated video creation platform using Remotion (React-based video framework) + ElevenLabs TTS with word-level audio synchronization. The system produces explainer videos from concept to rendered MP4 through a 6-phase workflow.

**Stack**: Remotion 4.0 / React 19 / TypeScript 5.9 / TailwindCSS 4 / Python 3.10+ (TTS pipeline) / pnpm

## Commands

**IMPORTANT: Always use pnpm, never npm**

```bash
pnpm dev             # Launch Remotion Studio (preview compositions in browser)

# Multi-worktree studio management (one studio per worktree, ports 3001-3009)
python scripts/studio-manager.py start <worktree-path> [--name <video-name>]  # Start studio, register Caddy subdomain
python scripts/studio-manager.py list                                          # List running studios
python scripts/studio-manager.py stop <name-or-path>                          # Stop studio, remove route
python scripts/studio-manager.py stop-all                                      # Stop all studios
# Requires: pip install requests  |  Optional: STUDIO_DOMAIN=yourdomain.com
# See docs/studio-caddy-setup.md for Caddy infrastructure setup
# Slash command: /start-studio <worktree-path> [--name <video-name>]

pnpm build           # Bundle video compositions
pnpm lint            # ESLint + TypeScript type checking (eslint src && tsc)

# Render a specific composition to MP4 (high quality — standard settings)
pnpm exec remotion render <CompositionId> out/<animation-name>/final.mp4 --codec h264 --image-format png --pixel-format yuv444p10le --color-space bt709 --crf 5 --x264-preset slow --hardware-acceleration disable

# Generate TTS audio for all scenes in a composition (chunked mode = default for new videos)
python generate-all-audio.py <AnimationName> --chunk sentence --parallel 5  # sentence-chunked, 5 concurrent
python generate-all-audio.py <AnimationName>                                # single-call mode (legacy, no delta regen)

# Generate TTS for a single scene
python text-to-speech.py -i src/<Name>/scripts/scene-01-name.txt -o public/audio/<name>/ -s src/<Name>/scripts/ -n scene01 --chunk sentence

# Generate TTS for Shorts (faster speed)
python text-to-speech.py -i <script.txt> -o <audio-dir> -s <sync-dir> -n scene01 --shorts --chunk sentence

# Delta regen: re-generate ONLY the chunks whose text changed (requires prior --chunk sentence run)
python regen-changed.py <AnimationName>              # match chunks by checksum, bill only what changed
python regen-changed.py <AnimationName> --dry-run    # preview plan, no API calls
python regen-changed.py <AnimationName> --scene 02   # single scene
python regen-changed.py <AnimationName> --force      # regen everything at current voice/model params

# Generate AI image for a scene
python generate-image.py -p "prompt" -o public/images/<name>/ -n image-name --aspect-ratio 16:9

# Batch generate images from manifest
python generate-scene-images.py <AnimationName>

# Capture website screenshots for a composition (requires agent-browser)
python capture-screenshots.py <AnimationName>                    # all from manifest
python capture-screenshots.py <AnimationName> --name github-repo # single screenshot
python capture-screenshots.py <AnimationName> --dry-run          # preview commands
python capture-screenshots.py <AnimationName> --force            # re-capture existing

# Generate AI B-roll clips for a composition (requires FAL_KEY)
python scripts/generate-broll.py <AnimationName>
python scripts/generate-broll.py <AnimationName> --dry-run  # Preview prompts, no API calls

# Generate custom background music for a composition (requires ELEVENLABS_API_KEY)
python generate-bg-music.py <AnimationName>
python generate-bg-music.py <AnimationName> --prompt "lo-fi ambient, soft piano"
python generate-bg-music.py <AnimationName> --dry-run  # Preview, no API call

# Detect cross-video callback phrases in scripts
python scripts/detect-callbacks.py <AnimationName>

# Extract a 5-second recap clip from a rendered composition
python scripts/extract-recap-clip.py <SourceComposition> <SceneId> <OutputPath>

# Fact-check script claims via Perplexity API (optional, requires PERPLEXITY_API_KEY)
python scripts/perplexity-verify.py <AnimationName>              # verify all Tier 1+2 claims
python scripts/perplexity-verify.py <AnimationName> --dry-run    # extract claims without API calls
python scripts/perplexity-verify.py <AnimationName> --tier 1     # only critical claims

# premix-word-sfx.py — DEPRECATED, do not use (per-word pops create continuous noise)

# Validate audio-visual sync precision (cross-references sync JSON ↔ scene keyframes ↔ timing chain)
npx tsx scripts/validate-sync.ts <AnimationName>              # full composition audit
npx tsx scripts/validate-sync.ts <AnimationName> --scene Scene01  # single scene
npx tsx scripts/validate-sync.ts <AnimationName> --verbose    # detailed output
# Slash command: /validate-sync <AnimationName> [SceneNN]
```

## Video Creation Workflow (diy-yt-creation)

The primary workflow lives in `.claude/commands/diy-yt-creation/`. It can be run as individual phases or end-to-end via `full-auto`:

| Phase | Command | Input | Output |
|-------|---------|-------|--------|
| 0 | phase0-research | Topic/URL | `src/<Name>/research/content-brief.md` (includes hook architecture) |
| 1 | phase1-plan | Research brief | `.agents/plans/<topic>.plan.md` (visual hook design) |
| 2 | phase2-script | Plan | `src/<Name>/scripts/full-script.md` (raw script for review) |
| 2a | phase2a-script | Reviewed script | `src/<Name>/scripts/scene-NN-<name>.txt` (TTS-optimized) |
| 2b | phase2b-factcheck | Scene scripts + brief | `src/<Name>/scripts/fact-check-report.md` (verified claims) |
| 3 | phase3-audio | Script files | `public/audio/<name>/sceneNN.mp3` + `scripts/sceneNN-sync.json` |
| 4 | phase4-sync | Audio + sync JSON | Complete `src/<Name>/` with scenes, components, constants |
| 5 | phase5-render | Composition code | `out/<Name>/final.mp4` + `src/<Name>/youtube-description.txt` |
| 6 | phase6-shorts | Long-form video | Vertical Shorts in `src/<Name>Shorts/<Title>/` |

**Review checkpoint**: Phase 2 creates a raw script and STOPS for user review. User edits `full-script.md` directly, then runs Phase 2a to apply TTS optimization and split into scene files.

## Key Constraints

### CRITICAL: Always Research with the Current Year

**When looking up statistics, quotes, data, or external sources, always use the current year — never rely on training data alone.**

- Use `WebSearch` or the `web-researcher` agent with explicit year filters (e.g. "Stack Overflow survey 2025", "Jensen Huang quote 2026")
- Training data cutoff means statistics and tech leader statements may be 1–2 years out of date — always verify with a live search before including in scripts or descriptions
- When updating a YouTube description's Resources section, verify each link is live and points to the most current primary source available
- Prefer primary sources (official survey sites, earnings call transcripts, direct interview links) over secondary reporting

### CRITICAL: Never Auto-Render Full Videos

**NEVER start a full video render (`remotion render`) unless the user explicitly asks you to.** Rendering is expensive (takes several minutes, produces large files) and should only happen when the user is satisfied with the current state. Rendering QA stills (`remotion still --frame=N`) for debugging is fine and expected.

### CRITICAL: Check Shared Components First

**Before creating ANY new component**, always check `src/shared/components/` for existing reusable components. Common components include:
- `SubscribeBanner` - **MANDATORY: 1× per video (≤ 8 min) or 2× per video (> 8 min / > 14,400 frames).** Animated subscribe CTA with profile pic, red SUBSCRIBE button, bell shake, and mouse-click animation. Place at ~75% of video (1×) or ~50% + ~80% (2×). SFX: `spring-pop.mp3` on fly-in + `bell-notification.mp3` at +150 frames. See `composition-structure.md` for full integration guide.
- `DynamousMidroll` - **MANDATORY once per long-form video (5+ minutes).** Full-screen ~35s immersive promotion break (Cole Medin intro, community showcase, course preview, CTA with 10% OFF). Place at ~50-65% of video at a natural content break. Does NOT apply to Shorts or videos under 5 minutes. See `composition-structure.md` for full integration guide.
- `WatchNextMidroll` - Optional 5-second full-screen midroll recommending another video. Shows thumbnail image + video title + creator profile pic with spring animations. Place at ~30% of video using gap-insert pattern (same as DynamousMidroll). Export: `WATCH_NEXT_MIDROLL_DURATION` (150 frames). Props: `thumbnailSrc`, `videoTitle`, `accentColor`. SFX: place `cinematic-whoosh.mp3` at gap start in Composition.tsx. Integration: add `WATCH_NEXT_GAP = WATCH_NEXT_MIDROLL_DURATION` to timing.ts, blank `TransitionSeries.Sequence` + absolute `<Sequence>` overlay in Composition.tsx.
- `DynamousBanner` - Animated Dynamous.ai promotion banner (always paired with DynamousCourse)
- `DynamousCourse` - Scrolling AI Agent Mastery Course curriculum panel (always paired with DynamousBanner)
- `BrandWatermark` - Logo watermark with corner cycling
- `OutroSequence` - Brand outro video sequence
- `ChromaKeyVideo` - Green screen video compositing
- `LightLeakOverlay` - Cinematic WebGL light leak effect (`@remotion/light-leaks`). Primary use: inside `<TransitionSeries.Overlay>` at scene cut points (zero-frame cost). Also works standalone in `<Sequence>`. Props: `seed`, `hueShift` (0-360), `opacity`, `durationInFrames`. Phase 4 now auto-generates this as `TransitionSeries.Overlay` at every scene cut point.
- `StarburstBackground` - Animated WebGL starburst ray background (`@remotion/starburst`). Subtle rotating rays behind hero stats, title cards, CTAs, or Scene00Preview. Keep `opacity` low (0.10-0.20). Props: `rays`, `colors`, `rotationSpeed`, `smoothness`, `vignette`, `originOffsetX/Y`, `opacity`, `blendMode`. Phase 4 now auto-generates this in Scene00Preview.
- `BRollLayer` - `<OffthreadVideo>` wrapper for AI-generated B-roll overlays (35% opacity, screen blend, fade in/out)
- `StrokeText` - Outlined text using `webkitTextStroke`. Props: `text`, `strokeColor`, `strokeWidth`, `fillColor`, `fontSize`, `fontFamily`, `fontWeight`, `style`. Use for titles over busy backgrounds, hero stats with high contrast. Min fontSize 24px.
- `RemotionSfx` (`SFX` constant) - Remote-hosted WAV URLs from `@remotion/sfx` for built-in sounds: `ding`, `vineBoom`, `bruh`, `windowsXpError`, `whip`, `whoosh`, `pageTurn`, `uiSwitch`, `mouseClick`, `shutterModern`, `shutterOld`. Use with `<Audio src={SFX.ding} volume={0.3} />`. Requires internet during render. Volume cap 0.5.
- `CallbackClip` - PIP overlay for cross-video recap clips (spring entrance, fade exit, configurable position)
- `src/shared/components/metaphors/` - 7 Kurzgesagt-inspired spatial metaphor components:
  - `TokenRoulette` - Token prediction as probability-weighted roulette wheel
  - `EmbeddingMap` - 2D scatter-plot showing word clusters by semantic similarity
  - `AttentionSpotlights` - Spotlight beams showing attention weights between words
  - `ContextWindow` - Shrinking spotlight visualizing context window fill
  - `RAGLibrary` - Library card catalogue search animation for RAG
  - `AgentTools` - Swiss army knife unfolding tool blades
  - `BackpropFlow` - Water flowing through network layers (forward/backward pass)
- `src/shared/templates/sixty-seconds/` - 60-second explainer video templates:
  - `SixtySecondsHook` - 300-frame (10s) hook with large headline spring-in
  - `SixtySecondsExplain` - 1050-frame (35s) phase-based explanation with progress dots
  - `SixtySecondsCTA` - 450-frame (15s) CTA with gradient background and bouncing arrow
- `src/shared/components/retention/` - Retention-focused animation primitives (pattern interrupt toolkit):
  - ~~`KineticCaption`~~ - **DO NOT USE.** Windowed TikTok-style captions — clutters the frame in both long-form and Shorts. Never add to any video.
  - ~~`CameraZoom`~~ - **DO NOT USE.** Ken Burns zoom causes visible text drift. All scenes contain text, so this is never appropriate.
  - `ScreenShake` - Reusable screen shake for emphasis moments. Props: `triggerFrame`, `intensity` (default 6px), `duration` (default 8 frames)
  - `GlitchInterrupt` - Brief chromatic aberration + RGB split + flicker. Props: `triggerFrame`, `duration` (default 12 frames)
  - `ColorShift` - Periodic subtle hue-rotate pulse every N seconds to break visual monotony. Props: `interval` (default 450 frames)
  - `FitHeadline` - Auto-sizing headline using `@remotion/layout-utils` `fitText()`. Props: `text`, `maxWidth`, `maxFontSize`, `minFontSize`
  - `RETENTION_SPRINGS` - Spring configs tuned for retention effects (`wordPop`, `wordScale`, `cameraZoom`, `shake`, `glitch`)
  - `BlurReveal` - Curiosity gap: shows content blurred, unblurs at triggerFrame. Props: `children`, `triggerFrame`, `durationFrames` (90), `blurStart` (20px)
  - `SpotlightFocus` - Dims inactive elements, highlights active element. Props: `children`, `active` (boolean), `dimOpacity` (0.25)
  - `ProgressDots` - N-dot progress indicator (Zeigarnik Effect). Props: `totalDots`, `activeDotIndex`, `dotColor`, `position`
  - `SlimProgressBar` - 4px top-bar completion signal. Props: `totalFrames`, `color`, `startFrame`. Skip on Scene00Preview.
  - `SegmentTitleCard` - 60-frame full-screen chapter interstitial ("3 of 5: [Topic]"). Props: `segmentNumber`, `totalSegments`, `title`. Use as TransitionSeries.Sequence.
  - `FloatingCallout` - Slide-in pill for definitions/protips/warnings. Props: `text`, `triggerFrame`, `durationFrames` (150), `variant`, `position`
  - `TeaserOverlay` - 60-frame blurred preview of future content (open loop teasers). Props: `children`, `captionText`, `blurAmount` (8px)
  - `GhostPreview` - Visual foreshadowing: renders dim ghost outline of upcoming content before it fully appears at triggerFrame (primes viewer attention, based on Li et al. 2020 research). Props: `children`, `triggerFrame`, `previewDuration` (60), `ghostOpacity` (0.15), `ghostScale` (0.95)
- `src/shared/constants/hookSprings.ts` - Cinematic hook spring presets (`HOOK_SPRINGS`: heavy/gentle/snappy/slam/reveal/stagger), SFX presets (`HOOK_SFX`: smashCut/pivot/brandReveal/featureCard/announcement with pre-capped volumes), and pattern definitions (`HOOK_PATTERNS`: FilmTrailer/ContrastPivot/StatCascade/RackFocusReveal/TerminalHacker/SplitScreenDuel). Used by Phase 4 hook builder via cinematic hook blueprint from Phase 1.
- `src/shared/components/HubAndSpoke.tsx` - Hub-and-spoke architecture diagram with gradient fills, glowing connections, and brand logo support. Props: `hub` (label/iconSrc/color), `spokes` (label/iconSrc/color/triggerFrame), `hubWidth`, `spokeWidth`. Nodes have multi-layer shadows, gradient fills, and animated draw-on connections.
- `src/shared/components/FlowDiagram.tsx` - Sequential pipeline/flow diagram with gradient nodes and glowing arrows. Props: `nodes` (label/iconSrc/color/triggerFrame/sublabel), `direction`, `nodeWidth`, `nodeHeight`.
- `src/shared/components/LayeredArchitecture.tsx` - Stacked horizontal layers (UI>API>DB) with gradient fills and glowing arrows between layers. Props: `layers` (label/items/color/triggerFrame), `width`, `layerHeight`.
- `src/shared/components/ComparisonDiagram.tsx` - Side-by-side Before/After or VS comparison with gradient panels and pulsing divider. Props: `left`/`right` (title/items/color/triggerFrame), `mode` ('before-after'|'versus').
- `src/shared/components/GitBranching.tsx` - Git commit/merge diagrams with SVG branch lanes.
- `DIAGRAM_STYLES` constant (from `src/shared/components/constants/`) - Shared visual styles for all diagram nodes: `nodeGradient()`, `nodeShadow()`, `nodeBorder()`, `nodeAccentTop()`, connection glow settings. Use for custom diagrams that don't fit the shared components.
- `src/shared/components/diagrams/` - Enterprise-grade diagram system with Lucide icons:
  - `InfographicFlow` - **PREFERRED for multi-stage processes.** Row-based pastel-banded stages with Lucide icons, pill nodes, flow arrows. Supports `mode="light"` (enterprise infographic) and `mode="dark"`. Props: `title`, `subtitle`, `stages[]` (label/icon/nodes/connector/description), `mode`.
  - `DiagramIcon` - Professional icon wrapper. Renders Lucide icons in colored circle/rounded backgrounds with shadow. Props: `icon` (LucideIcon), `imageSrc`, `letter`, `color`, `bg`, `size`, `variant`.
  - `DiagramIconGroup` - Row of small labeled icons (e.g., "Plugins | API | Community" bubbles).
  - Palettes: `LIGHT_PALETTE`, `DARK_PALETTE`, `getDiagramPalette(mode)`, `getStagePalette(palette, index)` - 8 pastel stage colors per mode.
- `lucide-react` - 1000+ professional SVG icons. Import directly: `import { Search, Brain, Cpu } from 'lucide-react'`. Browse: https://lucide.dev/icons. Use in diagram components via `icon` prop.
- `src/shared/components/charts/` - **24-component data visualization library** with gradient fills, glow effects, glass panels, spring animations. **Always use these instead of raw SVG charts.** Import: `import { ComponentName } from '../../shared/components/charts'`
  - **Data Charts:**
    - `RadialProgressRing` - Apple Watch-style circular progress gauge. Props: `frame`, `targetPct`, `label`, `color`, `size`. Best for: percentage comparisons, ratios.
    - `GrowthBarChart` - Horizontal bar chart with gradient fills, staggered entrance, glass panel. Props: `frame`, `title`, `bars[]`, `maxValue`. Best for: growth timelines, benchmarks.
    - `DonutChart` - Multi-segment donut with animated draw-on and legend. Props: `frame`, `segments[]`, `centerValue`, `centerLabel`. Best for: market share, distribution breakdowns.
    - `RadarChart` - Spider/radar chart for multi-dimension comparison (1-3 datasets). Props: `frame`, `axes[]`, `datasets[]`. Best for: capability comparison, tool evaluation.
    - `WaterfallChart` - Incremental positive/negative waterfall with running baseline. Props: `frame`, `bars[]`, `positiveColor`, `negativeColor`. Best for: revenue breakdown, change analysis.
    - `ModernFunnel` - Layered narrowing bands with particle flow and pulsing gate. Props: `frame`, `layers[]`, `passRate`. Best for: conversion funnels, filtering.
    - `CapacityGauge` - Horizontal gauge with green-to-red transition and overflow. Props: `frame`, `targetPct`, `label`. Best for: utilization, thresholds.
    - `GaugeCluster` - Row of semi-circular dashboard gauges with needles. Props: `frame`, `gauges[]`. Best for: multi-metric dashboards.
    - `HeatmapGrid` - Color intensity grid with diagonal wave animation. Props: `frame`, `data[][]`, `rowLabels`, `colLabels`, `colorRange`. Best for: correlation matrices, feature mapping.
    - `SankeyFlow` - Flow distribution bands from sources to targets with animated draw-on. Props: `frame`, `sourceNodes[]`, `targetNodes[]`, `links[]`. Best for: resource allocation, data flow.
  - **Architecture & Diagrams:**
    - `ZonedArchitecture` - Multi-zone GCP-style architecture diagram with flow arrows. Props: `frame`, `zones[]`, `connections[]`. Best for: system architecture, cloud infrastructure.
    - `EcosystemMap` - Radial hub-spoke with category orbs and product cards. Props: `frame`, `hubLabel`, `categories[]`. Best for: product ecosystems, technology landscapes.
    - `PipelineFlow` - Horizontal pipeline with status badges (complete/active/pending). Props: `frame`, `stages[]`. Best for: CI/CD, data pipelines, workflows.
    - `TreeDiagram` - Top-down org chart / decision tree with right-angle connectors. Props: `frame`, `root` (recursive TreeNode). Best for: hierarchies, decision trees.
    - `NetworkMesh` - Connected graph with animated data flow particles. Props: `frame`, `nodes[]`, `edges[]`. Best for: network topologies, service meshes.
    - `ProcessSteps` - Numbered circular process with curved connectors. Props: `frame`, `steps[]`. Best for: onboarding flows, how-it-works sequences.
    - `VennDiagram` - 2-3 circle Venn with intersection labels. Props: `frame`, `circles[]`, `intersections[]`. Best for: concept overlap, positioning.
  - **Comparison & Layout:**
    - `ComparisonTable` - Apple-style feature comparison with checkmarks. Props: `frame`, `columns[]`, `rows[]`. Best for: product comparison, feature matrices.
    - `MatrixQuadrant` - 2x2 strategy matrix with positioned items. Props: `frame`, `items[]`, `xAxisLabel`, `yAxisLabel`, `quadrantLabels`. Best for: strategy frameworks, prioritization.
    - `FeatureGrid` - Icon + title + description cards in grid. Props: `frame`, `features[]`, `columns`. Best for: feature showcases, capability lists.
    - `TimelineRoadmap` - Horizontal timeline with alternating milestone cards. Props: `frame`, `milestones[]`. Best for: product roadmaps, history.
  - **Dashboard & Metrics:**
    - `MetricDashboard` - KPI stat cards with sparklines and trend indicators. Props: `frame`, `cards[]`, `columns`. Best for: metrics overview, performance dashboards.
    - `StatCardRow` - Large hero stat cards with counters and trend badges. Props: `frame`, `stats[]`. Best for: key stats, growth metrics.
    - `AnnotatedScreenshot` - Screenshot with animated callout annotations. Props: `frame`, `children`, `annotations[]`. Best for: product walkthroughs, UI reviews.
  - Demo: `VizDemo` composition in Root.tsx showcases the original 4 chart components.
- `src/RacingBarChart/` - Animated benchmark bar chart race composition (accepts JSON data, auto-ranks)
- `src/shared/components/MotionBlurTrail.tsx` - Cinematic motion blur wrapper (`@remotion/motion-blur`). Wraps any component to add blur during fast spring animations. Props: `layers` (default 8), `lagInFrames` (default 0.5). Best for: spring entrances, scale pops, hero stat reveals. Avoid on static text.
- `src/shared/components/ProceduralNoise.tsx` - Organic noise-driven animated background (`@remotion/noise`). Perlin noise particles that drift smoothly. Props: `seed`, `count`, `color`, `size`, `speed`, `opacity`, `blendMode`. Also exports `useNoise(seed, speed)` hook for custom noise values.
- `src/shared/components/AnimatedShape.tsx` - SVG shapes with draw-on animation (`@remotion/shapes`). Supports `circle`, `rect`, `triangle`, `star`, `polygon`. Props: `shape`, `width`, `height`, `fill`, `stroke`, `triggerFrame`, `springConfig`, `points`, `cornerRadius`. Uses `evolvePath()` for stroke draw-on.
- `src/shared/components/RoundedTextBox.tsx` - TikTok-style multiline text box with pixel-perfect rounded corners (`@remotion/rounded-text-box`). Unlike CSS borderRadius, rounds each line individually. Props: `text`, `fontFamily`, `fontSize`, `color`, `boxColor`, `paddingX`, `paddingY`, `borderRadius`, `triggerFrame`. Best for: Shorts captions, callout labels, highlighted quotes.
- `@remotion/media-utils` - Audio/video metadata utilities. Use `getAudioDurationInSeconds(src)` to validate TTS audio durations. Wrapper: `src/shared/utils/mediaUtils.ts` exports `validateAudioDuration()`.
- `@remotion/lottie` - Embed LottieFiles vector animations. Use `<Lottie animationData={data} />` with JSON data from lottiefiles.com. Import directly (no wrapper needed).
- `@remotion/preload` - Preload assets to eliminate loading flashes. Use `preloadAudio(staticFile('audio/...'))` or `preloadVideo()` in component body. Import directly.
- `@remotion/gif` - Frame-synced GIF playback. Use `<Gif src={gifUrl} width={w} height={h} />`. Import directly.
- `@remotion/elevenlabs` - Convert ElevenLabs Speech-to-Text output into Remotion Caption objects. Compatible with `createTikTokStyleCaptions()` from `@remotion/captions`. Useful for auto-generating Shorts captions.
- `src/shared/utils/oklchColors.ts` - oklch() color interpolation utilities. `interpolateOklch()` for perceptually uniform color transitions (no muddy RGB midpoints). Pre-built palettes: `OKLCH_PALETTES.purpleToCyan`, `.pinkToIndigo`, `.warmToCool`, `.darkShift`, `.greenToAmber`.

- `src/shared/constants/brandLogos.ts` (`BRAND_LOGOS`) - Central registry of brand/company logo paths. Use `staticFile(BRAND_LOGOS.openai)` etc. Logos live in `public/images/shared/logos/`. See `brand-logos.md` rule for full usage. Available: anthropic, claude, claudeCode, openai, google, microsoft, nvidia, github, docker, vscode, jetbrains, ollama, cline, n8n, huggingface, cloudflare, yc, openclaw, and more.

Creating duplicate components wastes time and leads to inconsistency. If a similar component exists, extend or reuse it.

### CRITICAL: Verify Asset Paths and Composition IDs Before Renders

**Always verify repo URLs, asset file paths, and composition IDs against existing code before using them.** Do not assume or invent references — grep the codebase first.

- Before any render: confirm the composition ID exists in `Root.tsx`
- Before referencing `staticFile('...')`: confirm the file exists in `public/`
- Before adding repo URLs to scripts/descriptions: verify the URL is correct and live
- Run `/validate-sync <AnimationName>` before rendering to catch all of the above automatically

### Pre-Render Validation Gate

Before rendering (or when asked to render), always run sync validation first:
```bash
npx tsx scripts/validate-sync.ts <AnimationName>
```
If errors are found, fix them before rendering. The script catches: stale timestamps, duration mismatches, missing assets, unregistered compositions, anti-patterns. Webpack cache is auto-cleared by the pre-render hook.

### Context-Only Prompts — Ask for Intent

When the user sends a system/context prompt without an explicit request, **ask what they'd like to do** instead of assuming an action. Never auto-invoke workflows, create PRs, or start rendering without explicit user intent.

## Output Directory

All rendered videos go to `out/` (git-ignored). Use `out/<animation-name>/` subdirectories per composition.

### Render Quality Settings (STANDARD)

```bash
pnpm exec remotion render <CompositionId> out/<name>/final.mp4 --codec h264 --image-format png --pixel-format yuv444p10le --color-space bt709 --crf 5 --x264-preset slow --hardware-acceleration disable
```

| Setting | Value | Purpose |
|---------|-------|---------|
| `--codec` | h264 | Universal compatibility (YouTube, web, mobile) |
| `--image-format` | png | Lossless intermediates (JPEG causes banding on dark gradients) |
| `--pixel-format` | yuv444p10le | 10-bit color, no chroma subsampling — eliminates dark gradient banding |
| `--crf` | 5 | Near-lossless quality (lower = better; 5 near-lossless, 15 good, 23 default) |
| `--color-space` | bt709 | Standard HD color space for web delivery |
| `--x264-preset` | slow | Better compression, higher quality at same file size |
| `--hardware-acceleration` | disable | Ensures CRF works (HW accel ignores CRF) |

For faster renders during development, use `--crf 23 --image-format jpeg --x264-preset fast`.

### AV1 Codec (EXPERIMENTAL — v4.0.440+)

AV1 offers ~30% better compression than H.264 at equal quality. Useful for smaller uploads.

```bash
pnpm exec remotion render <CompositionId> out/<name>/final-av1.mp4 --codec av1 --image-format png --crf 30 --hardware-acceleration disable
```

**Note:** AV1 CRF scale differs from H.264 (AV1 CRF 30 ≈ H.264 CRF 18). No `--x264-preset` for AV1. Significantly slower to encode. Test before using for production renders.

## Analyzing External Repos for Videos

When creating videos about external repositories:

1. **Deep Analysis First**: Use the Explore agent to thoroughly understand:
   - Architecture and component structure
   - Data flow and communication protocols
   - Use cases and value proposition
   - Key technical decisions (ADRs)

2. **Key Documentation Files**: Prioritize reading:
   - `README.md` - Overview
   - `CLAUDE.md` - Internal design principles
   - `docs/architecture*.md` - C4 diagrams, component docs
   - Main entry points and type definitions

3. **Content Brief Structure**: Extract and organize:
   - Core value proposition (1-2 sentences)
   - Pain points the system solves
   - Architecture components (layered)
   - Unique technical decisions
   - Statistics and proof points
   - Cult-hopping opportunities (known brands to anchor concepts)

## Custom Brand Styles

POC brand styles are stored in `public/poc-styles/brands/`. Each brand folder contains HTML templates showing visual design patterns that should be ported to Remotion components.

### Modern Gradient Brand (`public/poc-styles/brands/modern-gradient/`)

A dark, gradient-heavy visual style with glass morphism effects:

**Color Palette:**
- Background: `#0f172a` (midnight) -> `#16213e` (dark space)
- Primary gradients: `#a855f7` (purple) -> `#ec4899` (pink)
- Secondary: `#6366f1` (indigo) -> `#8b5cf6` (violet)
- Accent: `#06b6d4` (cyan)

**Visual Elements:**
- Glass morphism cards: `rgba(255,255,255,0.03)` background + `backdrop-filter: blur(10px)`
- Gradient borders using pseudo-elements
- Animated gradient orbs (blurred, low opacity) for backgrounds
- Text gradients via `-webkit-background-clip: text`

**Template Files Available:**
- `title-*.html`, `stats-*.html`, `code-*.html`, `list-*.html`
- `compare-*.html`, `cta-*.html`, `transition-*.html`

Each HTML file includes **REMOTION PORTING NOTES** comments with specific frame timings, animation sequences, and performance tips.

## Modular Rules

Detailed rules are organized in `.claude/rules/` and load conditionally based on what files you're working with:

| Rule File | Loads When | Content |
|-----------|-----------|---------|
| `agent-pitfalls.md` | Always | FONTS keys, +T bug, delay drift, wipe crash |
| `audio-sync.md` | Editing scenes/compositions | wordToFrame, sync chain, timing constants |
| `composition-structure.md` | Editing Composition.tsx/Root.tsx | Mandatory components, Dynamous, transitions |
| `scene-design.md` | Editing scene files | Phase design, no overlapping, reading time, preview hook |
| `shorts.md` | Editing Shorts files | Vertical layout, thumbnail frame, CTA |
| `visual-qa.md` | Editing any .tsx | QA workflow, pre-render checklist |
| `remotion-rendering.md` | Editing any .tsx | Headless Chromium pitfalls |
| `youtube-metadata.md` | Editing descriptions/scripts | YouTube description format, brand links |
| `python-pipeline.md` | Editing Python files | TTS, image gen, thumbnails |
| `scriptwriting.md` | Editing TTS scripts | Kallaway formula, TTS conventions |
| `brand-logos.md` | Editing scene files, planning | Brand logo library, person photos, `BRAND_LOGOS` constant |

## Session Learning & Knowledge Persistence


<CRITICAL>
**MANDATORY: Learn from every session and persist knowledge.**

At the end of each significant coding session (especially when bugs are fixed or patterns are discovered), update `LEARNING.md` with new insights.

### What to Capture in LEARNING.md

```markdown
## [Date] - [Brief Topic]

### Problem
- What went wrong or was confusing

### Root Cause
- Why it happened (the actual technical reason)

### Solution
- What fixed it (with code examples if applicable)

### Prevention
- How to avoid this in the future
```

### Categories to Track

1. **TypeScript/Remotion Errors**
   - Spring config patterns (`SPRINGS.bouncy` not `SPRINGS.bouncy.config`)
   - Import requirements (`import React from 'react'`)
   - Interpolation clamping requirements

2. **Visual Bugs**
   - Overlapping elements (phase-based rendering)
   - Duplicate CSS properties in style objects
   - Blank frames (missing backgroundColor)

3. **Audio/Sync Issues**
   - Audio offset calculations
   - TransitionSeries timing overlaps
   - Word sync JSON parsing

4. **Build/Lint Errors**
   - Unused variable patterns
   - Module resolution issues
   - Non-deterministic code warnings

5. **Others**
   - Workflow improvements and shortcuts discovered
   - External tool quirks (ElevenLabs, Replicate, ffmpeg)
   - Performance optimizations
   - Documentation gaps or unclear patterns
   - Anything that caused confusion or wasted time

### When to Update LEARNING.md

- After fixing a bug that took more than one attempt
- When discovering a pattern that works well
- After receiving error messages that weren't obvious
- When a workaround is needed for a library limitation

### Example Entry

```markdown
## 2026-02-05 - Spring Config Type Error

### Problem
TypeScript error: `Type '{ readonly fps: 30; readonly config: SpringConfig; }' has no properties in common with type 'Partial<SpringConfig>'`

### Root Cause
The `spring()` function expects a flat SpringConfig object, not a nested object with `fps` and `config` properties. The SPRINGS constant was incorrectly structured.

### Solution
// WRONG
export const SPRINGS = {
  bouncy: {
    fps: FPS,
    config: { damping: 8 },
  },
};
spring({ frame, fps, config: SPRINGS.bouncy.config });

// CORRECT
export const SPRINGS = {
  bouncy: { damping: 8 },
};
spring({ frame, fps, config: SPRINGS.bouncy });

### Prevention
- Always check existing working compositions for patterns
- Reference `src/AgenticProtocols/constants/springs.ts` as canonical example
```

### File Location

`LEARNING.md` lives at the repository root alongside `CLAUDE.md`.
</CRITICAL>


## Browser Automation

Use `agent-browser` for web automation. Run `agent-browser --help` for all commands.

Core workflow:
1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
3. `agent-browser click @e1` / `fill @e2 "text"` - Interact using refs
4. Re-snapshot after page changes