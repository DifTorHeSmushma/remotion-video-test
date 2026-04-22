# Animation Patterns & Techniques

Comprehensive reference for animation approaches, timing, easing, and implementation patterns for Remotion video production.

---

## Core Animation Primitives

### Remotion Fundamentals

All animations MUST be deterministic. Use these Remotion APIs:

```tsx
import { useCurrentFrame, interpolate, spring, random } from 'remotion';

const frame = useCurrentFrame();

// Linear interpolation (most common)
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Spring physics (bouncy, organic)
const scale = spring({
  frame,
  fps: 30,
  config: { damping: 12, stiffness: 200 },
});

// Deterministic randomness
const offset = random('unique-seed') * 10;
```

### CRITICAL RULES
- **Always clamp**: `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'`
- **No Math.random()**: Use `random('seed')` from Remotion
- **No Date.now()**: Everything frame-based
- **GPU-only properties**: Only animate `transform`, `filter`, `opacity`
- **Add willChange**: Include `willChange: 'transform'` or `willChange: 'opacity'` for GPU promotion

---

## Entrance Animations

### Fade In
```tsx
const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
```

### Slide Up + Fade
```tsx
const opacity = interpolate(frame, [start, start + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const translateY = interpolate(frame, [start, start + 20], [30, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
// style: { opacity, transform: `translateY(${translateY}px)` }
```

### Spring Pop-In
```tsx
const scale = spring({ frame: frame - startFrame, fps: 30, config: { damping: 12 } });
// style: { transform: `scale(${scale})` }
```

### Slam-In (KineticText style)
```tsx
const scale = spring({ frame: frame - startFrame, fps: 30, config: { damping: 8, stiffness: 300 } });
// Overshoots past 1.0 then settles - very dramatic
```

### Staggered Entrance (multiple items)
```tsx
items.map((item, i) => {
  const delay = i * 5; // 5 frames between each
  const opacity = interpolate(frame, [start + delay, start + delay + 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const translateY = interpolate(frame, [start + delay, start + delay + 15], [20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <div style={{ opacity, transform: `translateY(${translateY}px)` }}>{item}</div>;
});
```

### Wipe Reveal (left to right)
```tsx
const clipX = interpolate(frame, [start, start + 30], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
// style: { clipPath: `inset(0 ${100 - clipX}% 0 0)` }
```

---

## Text Animations

### Character-by-Character Reveal
```tsx
const text = "Hello World";
const charsVisible = Math.floor(interpolate(frame, [start, start + text.length * 2], [0, text.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
const displayText = text.slice(0, charsVisible);
```

### Word-by-Word Highlight (AnimatedCaption style)
```tsx
words.map((word, i) => {
  const isActive = frame >= word.startFrame && frame < word.endFrame;
  const scale = isActive ? spring({ frame: frame - word.startFrame, fps: 30, config: { damping: 15 } }) * 0.1 + 1 : 1;
  return <span style={{ color: isActive ? accent : dimmed, transform: `scale(${scale})` }}>{word.text} </span>;
});
```

### Gradient Text Shimmer
```tsx
const shimmerOffset = interpolate(frame, [0, 60], [-100, 200], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
// style: { backgroundImage: `linear-gradient(90deg, #a855f7, #ec4899, #a855f7)`,
//   backgroundSize: '200% 100%', backgroundPosition: `${shimmerOffset}% 0`,
//   WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }
```

### Rolling Number Counter
```tsx
const value = interpolate(frame, [start, start + 60], [0, targetNumber], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  easing: (t) => 1 - Math.pow(1 - t, 3), // cubic ease-out
});
```

---

## Background Effects

### Gradient Mesh (3-layer)
```tsx
// Layer 1: Radial gradient at 20,30% position
// Layer 2: Radial gradient at 80,70% position
// Layer 3: Radial gradient at 50,50% position
// Animate positions with Lissajous: x = sin(frame * speed), y = cos(frame * speed * 1.3)
```

### Floating Particles
```tsx
particles.map((p, i) => {
  const x = p.startX + Math.sin(frame * 0.02 + p.phase) * 50;
  const y = p.startY - frame * p.speed * 0.5; // drift upward
  const opacity = 0.3 + Math.sin(frame * 0.05 + i) * 0.2;
  return <div style={{ position: 'absolute', left: x, top: y % height, opacity, width: p.size, height: p.size, borderRadius: '50%', background: accent }} />;
});
```

### Perspective Grid
```tsx
// style: {
//   perspective: '800px',
//   backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
//   backgroundSize: '60px 60px',
//   transform: `rotateX(60deg) translateY(${frame * 2}px)` // scrolling grid
// }
```

---

## Transition Patterns

### Scene-to-Scene (using TransitionSeries)
```tsx
import { TransitionSeries } from '@remotion/transitions';
import { fade, slide, wipe } from '@remotion/transitions/presentations';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={sceneADuration}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()} // or slide(), wipe(), custom
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={sceneBDuration}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### Custom Transition Implementation
```tsx
const customTransition = (props: CustomTransitionProps): TransitionPresentation<{}> => ({
  component: ({ children, presentationProgress, presentationDirection }) => {
    const opacity = presentationDirection === 'entering'
      ? presentationProgress
      : 1 - presentationProgress;
    return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
  },
});
```

### Transition + SFX Timing
- SFX starts **5 frames before** transition begins
- SFX duration: **30 frames** (1 second)
- SFX volume: **0.7** (70%)

---

## Timing & Easing Reference

### Standard Durations
| Animation | Frames | Seconds |
|-----------|--------|---------|
| Quick fade | 10-15 | 0.3-0.5s |
| Standard entrance | 15-20 | 0.5-0.7s |
| Dramatic reveal | 20-30 | 0.7-1.0s |
| Counter count-up | 30-60 | 1.0-2.0s |
| Scene transition | 12-30 | 0.4-1.0s |
| Stagger delay | 3-8 | 0.1-0.3s per item |

### Spring Configs
| Feel | damping | stiffness | mass |
|------|---------|-----------|------|
| Snappy | 15-20 | 200 | 1 |
| Bouncy | 8-12 | 200 | 1 |
| Gentle | 20-30 | 100 | 1 |
| Heavy | 12-15 | 100 | 2 |
| Elastic | 5-8 | 300 | 1 |

### Easing Functions (for interpolate)
```tsx
import { Easing } from 'remotion';
// Easing.ease - standard
// Easing.bezier(0.25, 0.1, 0.25, 1) - custom
// Easing.inOut(Easing.cubic) - smooth in/out
// Easing.out(Easing.cubic) - fast start, slow end (most common for entrances)
```

---

## Phase-Based Rendering (CRITICAL)

### The Pattern
```tsx
// Define mutually exclusive phases
const PHASE1_END = 65;
const PHASE2_END = 125;

const isPhase1 = audioFrame < PHASE1_END;
const isPhase2 = audioFrame >= PHASE1_END && audioFrame < PHASE2_END;

// Conditional mount - elements UNMOUNT when not in phase
{isPhase1 && (
  <div style={{ opacity: phase1Opacity }}>
    <ContentA />
  </div>
)}
{isPhase2 && (
  <div style={{ opacity: phase2Opacity }}>
    <ContentB />
  </div>
)}
```

### Rules
1. **No gaps**: PHASE2_START === PHASE1_END (same constant)
2. **No overlaps**: Use `>=` for start, `<` for end
3. **ALL elements gated**: Even titles and backgrounds
4. **Opacity for animation only**: Not for visibility control between phases

---

## Performance Guidelines

| Effect | Limit | Notes |
|--------|-------|-------|
| Blur filters | < 15px | Avoid stacking multiple blurs |
| Particle count | < 200 | matrix-rain/confetti heavier |
| SVG grid spacing | 60px+ | Lower density for smooth render |
| Simultaneous springs | < 5 | Negligible at 30fps per component |
| Gradient stops | < 5 | More stops = more computation |
| Box shadow layers | < 3 | Each layer is a render pass |

---

## Common Combinations

### "Living Background" Stack
1. Base: Solid dark color (#0f172a)
2. Layer 1: `AnimatedGrid` perspective grid at 15% opacity
3. Layer 2: `GradientMesh` nebula at 20-30% opacity
4. Layer 3: `ParticleField` floating-dots at 30-40% opacity

### "Dramatic Stat Reveal"
1. Background builds (10 frames)
2. Number counts up via `AnimatedCounter` (45 frames)
3. Scale bump + glow pulse at completion (10 frames)
4. Delta indicator slides in (10 frames)

### "Code Demo Sequence"
1. Terminal chrome appears (10 frames)
2. Command types out via `TypewriterCode` (30+ frames)
3. Output lines stagger in (15 frames)
4. Spotlight highlights key output via `CodeHighlight` (20 frames)

### "Architecture Build"
1. Grid background draws in (15 frames)
2. Nodes pop in with staggered springs (30 frames)
3. Connection lines draw between nodes (20 frames)
4. Data flow particles animate along paths (continuous)
5. Labels fade in on nodes (15 frames)

### "Comparison Reveal"
1. "Before" column slides in from left (15 frames)
2. VS badge pops in center with spring (10 frames)
3. "After" column slides in from right (15 frames)
4. Winner highlight glows (10 frames)
5. Check/cross icons pop in per row (staggered 5 frames each)
