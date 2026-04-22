# Rules Guide — Where to Find Project Rules

Reference for the rulecheck agent. Focus on rules that **linters can't enforce** —
architectural patterns and conventions from the full `.claude/rules/` folder.

## Primary Sources — Read ALL of These Each Run

| File | Scope |
|------|-------|
| `.claude/rules/agent-pitfalls.md` | Always-loaded: fonts, +T drift, audio placement, wipe import, CameraZoom |
| `.claude/rules/composition-structure.md` | Composition.tsx: mandatory components, transitions, SFX |
| `.claude/rules/scene-design.md` | Scene files: phase rendering, retention components, typography |
| `.claude/rules/audio-sync.md` | Audio/animation sync: wordToFrame(), AUDIO_OFFSET imports |
| `.claude/rules/remotion-bits.md` | remotion-bits: wrapper imports, banned direct imports |
| `.claude/rules/remotion-rendering.md` | Headless Chromium: div collapse, translate centering, determinism |
| `.claude/rules/scene-validation.md` | Static analysis checklist — all anti-patterns in one place |
| `.claude/rules/midroll-integration.md` | DynamousMidroll: overlay pattern, audio, timing shifts |
| `.claude/rules/audio-design.md` | SFX volume caps per sound type, audio layering rules |
| `.claude/rules/shorts.md` | Vertical layout (1080x1920), Shorts-specific component rules |
| `.claude/rules/post-production.md` | Schema/slider conventions, debug overlays |
| `CLAUDE.md` | Top-level: mandatory shared components, render rules, workflow |
| `.claude/hookify.*.md` | Hookify rules — runtime guards that also encode static violations |

Do NOT check: `.claude/rules/python-pipeline.md`, `scriptwriting.md`, `scriptwriting_old.md`,
`youtube-metadata.md`, `tiktok.md` — those govern Python/content/metadata work, not TSX source.

## Violation Categories

### Tier 1 — Critical (fix first, these cause runtime crashes or double-audio bugs)

| Rule | Source | Grep Pattern | Fix |
|------|--------|-------------|-----|
| Wrong FONTS keys | agent-pitfalls | `FONTS\.inter\|FONTS\.jetbrainsMono` | Replace with `FONTS.primary` / `FONTS.mono` |
| `<Audio>` inside scene | agent-pitfalls | `<Audio` in `src/*/scenes/*.tsx` | Delete — audio belongs in `Composition.tsx` only |
| wipe transition import | agent-pitfalls, composition-structure | `@remotion/transitions/wipe` | Replace with `@remotion/transitions/slide` |
| CameraZoom usage | agent-pitfalls, scene-design | `CameraZoom` (import or JSX) | Delete — causes visible text drift, banned |
| +T duration drift | agent-pitfalls, scene-validation | `durationInFrames.*\+.*TRANSITION` | Remove `+ TRANSITION_DURATION` — already included |
| Math.random() | scene-design, visual-qa, scene-validation | `Math\.random\(\)` (no seed) | Replace with `import { random } from 'remotion'` + seed string |

### Tier 2 — High (cause sync drift or visual bugs in rendered video)

| Rule | Source | Grep Pattern | Fix |
|------|--------|-------------|-----|
| Hardcoded delay arrays | agent-pitfalls, scene-validation | `delay:\s*\d+` in item array literals | Use `triggerFrame: wordToFrame(timestamp, OFFSET)` |
| Raw timestamp math | audio-sync | `Math\.round.*\*\s*30.*\+\s*15` | Use `wordToFrame()` — it includes MP3 latency |
| Hardcoded AUDIO_OFFSET | audio-sync | `AUDIO_OFFSET_FIRST\s*=\s*\d+` in scene files | Import from `../constants/timing` |
| Missing `whiteSpace: 'pre'` | agent-pitfalls, scene-validation | `FONTS\.mono` style block without `whiteSpace` | Add `whiteSpace: 'pre'` to mono containers |
| Icon/emoji missing `color` | agent-pitfalls, scene-validation | emoji/icon divs without explicit `color` style | Add `color: item.color` — default black is invisible on dark bg |
| Unicode escapes in JSX text | agent-pitfalls | `\\u[0-9a-fA-F]{4}` in JSX (not in `{...}`) | Wrap in `{'\uXXXX'}` JS expression |
| Unclamped interpolations | scene-validation | `interpolate\(` without `clamp` in options object | Add `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'` |
| translate(-50%) centering | remotion-rendering, scene-validation | `translate\(-50%` | Replace with flexbox `top/left/right/bottom: 0` pattern |
| Div collapse (no display:block) | remotion-rendering, scene-validation | Stacked `<div style={{` without `display: 'block'` | Add `display: 'block'` to each stacked text div |
| Font size below 20px | scene-design, scene-validation | `fontSize:\s*[1-9]\b\|fontSize:\s*1[0-9]\b` | Minimum 20px for YouTube readability |
| Direct remotion-bits sync import | remotion-bits | `from 'remotion-bits'` (AnimatedText, StaggeredMotion, Particles, CodeBlock) | Use wrappers from `../../shared/components/bits` |
| remotion-bits interpolate/random | remotion-bits | `interpolate\|random.*from 'remotion-bits'` | Use `from 'remotion'` |
| Wireframe diagram node | visual-diagrams | Diagram node with flat `${color}22` bg + no boxShadow | Use `DIAGRAM_STYLES.nodeGradient()` + `.nodeShadow()` |
| Thin diagram border (1px) | visual-diagrams | `border: '1px solid` on diagram containers | Minimum 2px: `DIAGRAM_STYLES.nodeBorder()` |
| Thin connection line | visual-diagrams | SVG `strokeWidth` < 2.5 on diagram connections | Minimum 2.5px + add glow layer |
| Undersized diagram node | visual-diagrams | Diagram node width < 160 or height < 100 | Minimum 160x100 (spokes), 180x120 (hubs) |

### Tier 2b — High (component pairing / SFX rules — cause silent or broken UX)

| Rule | Source | How to Detect | Fix |
|------|--------|--------------|-----|
| FloatingCallout missing SFX | scene-design | Find all `<FloatingCallout` in scenes → extract `triggerFrame` → check `Composition.tsx` for matching `pop.mp3` Audio at `SCENES.<scene>.start + localFrame` | Add `{ from: SCENES.X.start + localFrame, sfx: 'sfx/final/emphasis/pop.mp3', vol: 0.4 }` to Composition.tsx SFX array |
| FloatingCallout missing `scale={1.25}` | scene-design | `<FloatingCallout` without `scale={1.25}` prop | Add `scale={1.25}` — default size too small for YouTube |
| SubscribeBanner missing SFX | composition-structure | `<SubscribeBanner` without `spring-pop.mp3` + `bell-notification.mp3` nearby | Add spring-pop at banner frame + bell at +150 frames |
| SFX volume exceeds 0.25 | agent-pitfalls, audio-design | `volume={0\.[3-9]}` or `volume={0\.2[6-9]}` or `volume={[1-9]}` or `vol:\s*0\.(?:[3-9]\|2[6-9])` | Hard cap 0.25 (≈ -12 dB below narration). Per-sound targets: bell→0.10, whoosh→0.15, shake→0.15, glitch→0.12, spring-pop/pop→0.15, slam→0.20, transition→0.12, default→0.15 |
| ScreenShake/GlitchInterrupt missing SFX | scene-design | `<ScreenShake` or `<GlitchInterrupt` in scene → check Composition.tsx for `screen-shake.mp3`/`glitch-zap.mp3` at matching absolute frame | Add retention SFX entry in Composition.tsx |
| Phase fade-out missing at scene end | agent-pitfalls, scene-design | Find last `isPhase` block per scene → check its opacity interpolation → if only 2 input keyframes `[X, X+N], [0, 1]` it's a bug. Grep: `isPhase` blocks whose opacity uses `interpolate(frame, [CONST, CONST + 20], [0, 1]` without a matching 4-keyframe version | Add fade-out: `[start, start+20, dur-24, dur], [0, 1, 1, 0]` |
| Minimum reading time violated | agent-pitfalls, scene-design | For each phase, find last `wordToFrame` trigger → calculate gap to phase boundary → if gap < 75 frames (2.5s), content flashes too fast | Push PHASE_END later to give 75+ frames after last trigger |
| KineticCaption in long-form | scene-design, agent-pitfalls | `KineticCaption` import or usage in non-Shorts composition | Delete — banned in all long-form videos |
| CameraZoom usage | scene-design, agent-pitfalls | `CameraZoom` import or usage anywhere | Delete — causes visible text drift, banned |

### Tier 3 — Medium (composition-level structural checks)

These require reading `Composition.tsx` files — do NOT fix these if context is getting long.

| Rule | Source | What to Check | Fix |
|------|--------|--------------|-----|
| Missing `OutroSequence` | composition-structure | `Composition.tsx` without `OutroSequence` import/usage | Add as final TransitionSeries.Sequence (240 frames) |
| Missing `BrandWatermark` | composition-structure | `Composition.tsx` without `BrandWatermark` | Add after audio layers |
| Missing `NoiseOverlay` | composition-structure | `Composition.tsx` without `NoiseOverlay` | Add after TransitionSeries, before audio |
| Missing `DynamousMidroll` | composition-structure, midroll-integration | `Composition.tsx` without `DynamousMidroll` | Add as Sequence overlay at 50-65% of video |
| Missing `DynamousBanner`+`DynamousCourse` | composition-structure | `Composition.tsx` without both | 2 combos per video — add at 1/3 and 2/3 marks |
| Missing `MidVideoReHook` | agent-pitfalls, scene-design | `Composition.tsx` without `MidVideoReHook` | Add as AbsoluteFill overlay at `TOTAL_FRAMES * 0.55` |
| Midroll in TransitionSeries | midroll-integration | `TransitionSeries.Sequence` wrapping `DynamousMidroll` | Use `<Sequence>` overlay with `opacity: 0.98` instead |
| Missing midroll narration audio | midroll-integration | Midroll present but no `Audio` for `dynamous-midroll.mp3` | Add `<Sequence from={midroll.start + 10}><Audio .../></Sequence>` |
| Opacity-only phases | scene-design, scene-validation | `phase1Opacity`/`phase2Opacity` siblings without `{isPhase && ...}` | Wrap in conditional mount `{isPhase1 && <div>...}` |
| Missing `ColorShift` | scene-design | Scene file without `ColorShift` import/usage | Wrap inner content div in `<ColorShift interval={600}>` |
| Missing backgroundColor | visual-qa | Root `<AbsoluteFill>` without `backgroundColor` | Add `backgroundColor: COLORS.background` |
| Scene3D in standard composition | remotion-bits | `Scene3D\|Element3D\|StepResponsive` in non-3D compositions | Remove — reserved for dedicated 3D mode only |
| Logos visible during midroll | composition-structure | Persistent overlay logos (VersionBranding, sponsor logos) not split around midroll | Split into before/after `<Sequence>` blocks to hide during midroll |
| BG music missing `loop` | hookify.bg-music-loop | `Binary Horizons` Audio without `loop` prop in Composition.tsx | Add `loop` prop — without it music stops after one playthrough |

### Tier 4 — Low (note for backlog if context is tight)

| Rule | What to Check |
|------|---------------|
| Missing `STAGGER` export | `constants/timing.ts` without `export const STAGGER = 8` |
| Hardcoded list stagger | `delay: 0, 80, 160` pattern (vs `triggerFrame + index * STAGGER`) |
| FitHeadline font shorthand | `fontFamily: 'Inter, sans-serif'` (should be exact `FONTS.primary` value) |
| ColorShift wraps AbsoluteFill | `<ColorShift>` wrapping outermost `AbsoluteFill` instead of inner content div |
| MidVideoReHook in TransitionSeries | MidVideoReHook as a `TransitionSeries.Sequence` — must be composition-level overlay |
| Duplicate shared components | New component file that replicates something in `src/shared/components/` |

## What NOT to Check

Already enforced by tooling — don't waste scan budget:
- ESLint rules (return types, unused vars) — `pnpm lint` catches these
- TypeScript strict mode — `pnpm exec tsc --noEmit` catches these
- Formatting (quotes, commas) — Prettier handles this
- Python files (`*.py`) — out of scope, covered by `python-pipeline.md`
- Script/description files (`*.md`, `*.txt`) — out of scope
