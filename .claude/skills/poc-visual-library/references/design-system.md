# Design System & Integration Guide

Shared design principles, integration patterns, and best practices that apply across all brands and components.

---

## Design Principles (All POCs)

1. **Deterministic**: All animations use `useCurrentFrame()`, `interpolate()`, `spring()`. No `Math.random()` or `Date.now()`. Use `random('seed')` for randomness.
2. **Clamped Interpolations**: Every `interpolate()` call uses `extrapolateLeft: 'clamp'` and `extrapolateRight: 'clamp'`.
3. **Phase-Based Rendering**: Demo compositions use conditional mounting (not just opacity) to prevent overlapping elements.
4. **GPU-Accelerated**: Animate only `transform`, `filter`, and `opacity` - no layout properties.
5. **`willChange` Hints**: Include `willChange` for GPU layer promotion.

---

## Standard Video Dimensions

| Format | Width | Height | FPS | Aspect |
|--------|-------|--------|-----|--------|
| Standard (YouTube) | 1920 | 1080 | 30 | 16:9 |
| Shorts (Vertical) | 1080 | 1920 | 30 | 9:16 |

---

## Color System Architecture

### Base Pattern (colors.ts)
```typescript
export const COLORS = {
  background: '#0f172a',
  backgroundAlt: '#1e293b',
  text: '#ffffff',
  textSecondary: '#e2e8f0',
  textMuted: '#94a3b8',
  primary: '#a855f7',      // Brand primary accent
  secondary: '#ec4899',     // Brand secondary accent
  accent: '#06b6d4',        // Tertiary accent
  success: '#22c55e',
  warning: '#f59e0b',
  danger: '#ef4444',
} as const;
```

### Brand Application
When applying a brand style, map the brand's palette into this standard structure:
- **Background colors**: Brand's dark backgrounds
- **Text colors**: White/light with varying opacity
- **Primary/Secondary**: Brand's accent colors
- **Success/Warning/Danger**: Standard semantic colors (green/amber/red)

---

## Typography System

### Font Loading (fonts.ts)
```typescript
import { loadFont } from '@remotion/google-fonts/Inter';
const { fontFamily: interFamily } = loadFont();

// For monospace (code scenes)
import { loadFont as loadJBMono } from '@remotion/google-fonts/JetBrainsMono';
const { fontFamily: monoFamily } = loadJBMono();
```

### Type Scale
| Role | Size | Weight | Usage |
|------|------|--------|-------|
| Hero Title | 80-120px | 900 | Hook text, main title |
| Section Title | 48-64px | 700-800 | Scene headers |
| Subtitle | 32-42px | 600 | Section subtitles |
| Body Large | 24-32px | 500-600 | Important body text |
| Body | 18-24px | 400 | Regular body text |
| Caption | 14-16px | 400 | Labels, annotations |
| Code | 18-24px | 400-500 | Code blocks, terminal |

### Video-Specific Sizing Rules
- **Minimum readable size**: 18px at 1920x1080
- **Stats/numbers**: 120-180px for dramatic impact
- **Code**: 20-28px for readability
- **Captions**: 24-36px with shadow/outline for visibility

---

## Glass Morphism Pattern

Standard glass card used across multiple brands:

```tsx
const glassStyle: React.CSSProperties = {
  background: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: 20,
};
```

Variants:
- **Light glass**: `rgba(255, 255, 255, 0.08)` + blur(15px)
- **Heavy glass**: `rgba(255, 255, 255, 0.03)` + blur(30px)
- **Colored glass**: `rgba(accent, 0.1)` + blur(20px)

---

## Gradient Text Pattern

Used across multiple brands:

```tsx
const gradientTextStyle: React.CSSProperties = {
  background: 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
};
```

---

## Neon Glow Pattern

Common across cyberpunk-neon, ai-neural, scifi-space:

```tsx
// Text glow
const neonTextStyle: React.CSSProperties = {
  textShadow: '0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.4)',
};

// Box glow
const neonBoxStyle: React.CSSProperties = {
  boxShadow: '0 0 20px rgba(0, 255, 255, 0.4), 0 0 40px rgba(0, 255, 255, 0.2)',
  border: '2px solid #00ffff',
};
```

---

## Component Integration Path

### Promoting POC to Shared Component

1. Copy `.tsx` file to `src/shared/components/`
2. Copy associated `types.ts` if shared types exist
3. Add exports to barrel file `src/shared/components/index.ts`
4. Import from `'../shared/components'` in scene code

### Using in Production Scenes
```tsx
import { useCurrentFrame, AbsoluteFill } from 'remotion';
import { AnimatedCounter } from '../shared/components/AnimatedCounter';
import { ParticleField } from '../shared/components/ParticleField';
import { AUDIO_OFFSET_FIRST } from '../constants/timing';

const StatsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const audioFrame = frame - AUDIO_OFFSET_FIRST;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a' }}>
      <ParticleField preset="floating-dots" count={40} layerOpacity={0.3} />
      <AnimatedCounter
        to={98.7}
        format="percentage"
        decimals={1}
        fontSize={140}
        startFrame={audioFrame}
      />
    </AbsoluteFill>
  );
};
```

---

## Mandatory Video Components

Every video MUST include:

1. **Scene00Preview**: 10-15s "In this video..." teaser
2. **OutroSequence**: 8s brand outro (final scene)
3. **BrandWatermark**: Logo with corner cycling
4. **DynamousBanner**: 2 appearances (1/3 and 2/3 into video)

---

## Before/After Examples

### Static Text → AnimatedCounter
- Before: `<div style={{ fontSize: 120 }}>98.7%</div>` (boring fade-in)
- After: `AnimatedCounter` counting 0→98.7% with threshold colors + `ParticleField` + `ZoomReveal` wrapping

### Static Code → TypewriterCode
- Before: Static code screenshot with highlight box
- After: `TypewriterCode` typing + `CodeHighlight` spotlight + `TerminalEmulator` running

### Static Diagram → NetworkGraph
- Before: Static boxes-and-arrows fading in
- After: `NetworkGraph` nodes popping in via spring + edges drawing + `AnimatedGrid` background + `GradientMesh` overlay

### Static Comparison → ComparisonTable
- Before: Static side-by-side text
- After: `ComparisonTable` rows sliding alternating sides + check/cross pop-ins + winner glow + `AnimatedBarChart` for numbers

### Flat Background → Living Background
- Before: Solid `#0f172a`
- After: `AnimatedGrid` perspective + `GradientMesh` nebula at 30% + `ParticleField` dots at 40%

### Stock Fade → Custom Transition
- Before: `fade()` between every scene
- After: `Liquid Morph` primary + `Glitch Cut` accent for hooks/reveals

---

## Scene Composition Checklist

When building any scene:

1. **Background layer**: Never flat solid - use at least one atmospheric effect (grid, mesh, particles)
2. **Content layer**: Main scene content with phase-based conditional rendering
3. **Overlay layer**: Optional effects (scanlines, glitch, particles) at low opacity
4. **Audio sync**: Use `wordToFrame()` for all timestamp-to-frame conversions
5. **Phase boundaries**: All content gated by mutually exclusive phase conditions
6. **Entry animations**: Every element has an entrance (fade, slide, spring, wipe)
7. **Exit animations**: Elements exit before next phase begins (fade out, slide out)
8. **GPU optimization**: Only animate transform, opacity, filter
9. **Clamped interpolations**: Every `interpolate()` call is clamped

---

## Recommended Brand + POC Pairings

| Video Topic | Brand | Key POC Components |
|---|---|---|
| AI Tool Review | ai-neural | TypewriterCode, AnimatedCounter, NetworkGraph, TerminalEmulator |
| Framework Comparison | modern-gradient | ComparisonTable, AnimatedBarChart, GradientText, KineticText |
| Code Tutorial | cyberpunk-neon | TypewriterCode, TerminalEmulator, CodeHighlight, AnimatedDiff |
| Product Launch | tech-startup | KineticText, AnimatedCounter, SubscribeButton, ParticleField |
| Data Analysis | fintech | AnimatedBarChart, AnimatedPieChart, AnimatedLineGraph, NumberMorph |
| Architecture Explainer | enterprise-dark | ArchitectureDiagram, AnimatedFlowchart, SequenceDiagram, IsometricScene |
| Science Education | nature-organic | DNAHelix, SolarSystem, WaveInterference, HandDrawnShape |
| Gaming/Fun | vaporwave/playful | NeonText, ParticleTitle, GlitchTitle, ComicPanels |
| Enterprise Demo | corporate-modern | StepProgress, ComparisonTable, BrowserMockup, APIFlow |
| Creative/Design | luxury-premium | LiquidText, MorphingShape, GradientText, FractalTree |

---

## Quick Reference: Font Pairings by Brand

| Brand | Headlines | Body | Code |
|---|---|---|---|
| ai-neural | Inter (900) | Inter (400) | JetBrains Mono |
| cyberpunk-neon | Orbitron (900) | JetBrains Mono (400) | JetBrains Mono |
| modern-gradient | Inter (800-900) | Inter (400-500) | - |
| corporate-modern | Inter (700-800) | Inter (400) | - |
| retro-tech | VT323 / Courier | VT323 / Courier | VT323 |
| luxury-premium | Playfair Display | Inter (300-400) | - |
| scifi-space | Orbitron (700) | Inter (400) | JetBrains Mono |
| brutalist | Monospace (900) | Monospace (400) | Monospace |
