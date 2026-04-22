# Remotion Implementation Reference — YouTube Shorts Hooks (9:16)

Adapted from the youtube-hooks SKILL.md Part 7 for the compressed Shorts timeline and vertical 9:16 format.

---

## Shorts Composition Config

```tsx
import { Composition } from 'remotion';
import { ShortsHookComposition } from './ShortsHookComposition';

// 1080×1920 (9:16), 30fps
// Duration: 900-1800 frames (30-60 seconds)
// Default hook: 900 frames (30s)

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ShortsHook"
        component={ShortsHookComposition}
        durationInFrames={900}   // 30 seconds at 30fps — extend to 1800 for 60s
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          hookScript: {
            scrollStop: 'You\'re writing AI prompts wrong.',
            promise: 'One change made my code accuracy jump from 60% to 90%.',
            delivery: 'Write prompts like API specs, not instructions. Here\'s exactly how.',
            payoff: 'This works on any LLM. Switch today.',
            keyNumber: 90,
          },
          visuals: {
            primary: staticFile('visuals/hero.jpg'),
            proof: staticFile('visuals/proof-screenshot.jpg'),
          },
          voiceover: staticFile('vo/hook.mp3'),
          palette: {
            accent: '#FFAA00',
            danger: '#FF4444',
            success: '#44FF88',
            data: '#44AAFF',
          },
        }}
      />
    </>
  );
};
```

---

## Shorts Hook Composition Structure

The Shorts timeline collapses the 5-layer hook from 30s of long-form into the same 30s but with a compressed,
higher-energy arc. Music bed starts at **frame 0** (not deferred like in long-form hooks).

### Scene Map

| Scene | Name | Time | Frames | Purpose |
|---|---|---|---|---|
| 1 | Scroll-Stop | 0–1.5s | 0–45 | Pattern-break that halts the scroll |
| 2 | Promise | 1.5–5s | 45–150 | Single bold claim, curiosity gap opens |
| 3 | Delivery | 5–25s | 150–750 | Core value — visual changes every 60-90 frames |
| 4 | Payoff | 25–29s | 750–870 | Result/transformation, CTA seed |
| 5 | Loop Bridge | 29–30s | 870–900 | Seamless return to frame 0 for auto-replay |

### Layer Architecture

```
Layer 0  (Audio)  — Music bed (frame 0, volume ramps up)
Layer 0  (Audio)  — Ambient texture (loops entire composition)
Layer 0  (Audio)  — Voiceover (full composition)
Layer 1           — BackgroundAtmosphere (vertical gradient, always running)
Layer 2           — FloatingParticles (reduced count for narrow frame)
Layer 3           — Scene content (Sequences per scene)
Layer 4           — LightLeak (top/bottom positions, transition moments)
Layer 5           — DynamicVignette (always on top of content)
Layer 6           — FilmGrain (topmost, always running)
Layer 7           — ChromaticAberration (impact moments only, ≤8 frames)
```

### Full Composition

```tsx
import {
  AbsoluteFill, Audio, Sequence, useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing, staticFile, Img,
} from 'remotion';
import { TransitionSeries, linearTiming, springTiming } from '@remotion/transitions';
import { slide } from '@remotion/transitions/slide';
import { fade } from '@remotion/transitions/fade';
import { useMemo } from 'react';

interface ShortsHookProps {
  hookScript: {
    scrollStop: string;
    promise: string;
    delivery: string;
    payoff: string;
    keyNumber?: number;
  };
  visuals: {
    primary: string;
    proof?: string;
  };
  voiceover: string;
  palette: {
    accent: string;
    danger: string;
    success: string;
    data: string;
  };
}

export const ShortsHookComposition: React.FC<ShortsHookProps> = ({
  hookScript,
  visuals,
  voiceover,
  palette,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Color temperature: warm at Scroll-Stop, neutral for Delivery, warm again at Payoff
  const colorTemp = interpolate(
    frame,
    [0, 45, 150, 600, 750, 870, 900],
    [8, 12, 0, 0, 14, 8, 8],
    { extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0a0a1a',
      filter: `hue-rotate(${colorTemp}deg)`,
    }}>

      {/* ═══ LAYER 1: BACKGROUND ATMOSPHERE (vertical, always running) ═══ */}
      <BackgroundAtmosphere frame={frame} fps={fps} />

      {/* ═══ LAYER 2: FLOATING PARTICLES (narrow spread for 9:16) ═══ */}
      <FloatingParticles count={12} color={`${palette.accent}33`} />

      {/* ═══ AUDIO: Music bed — starts at frame 0, ramps in over 2s ═══ */}
      {/* KEY DIFFERENCE FROM LONG-FORM: music starts immediately, not deferred */}
      <Audio
        src={staticFile('music/background.mp3')}
        volume={(f) =>
          interpolate(f, [0, 60], [0, 0.12], { extrapolateRight: 'clamp' })
        }
      />

      {/* ═══ AUDIO: Ambient texture ═══ */}
      <Audio src={staticFile('sfx/ambient-digital.wav')} volume={0.10} loop />

      {/* ═══ AUDIO: Voiceover ═══ */}
      <Audio src={voiceover} volume={1} />

      {/* ═══ SCENE 1: Scroll-Stop (0–1.5s = frames 0–45) ═══ */}
      <Sequence durationInFrames={45}>
        <ScrollStopScene
          text={hookScript.scrollStop}
          visual={visuals.primary}
          palette={palette}
        />
        <LightLeak position="top" color={palette.accent} intensity={0.10} />
        {/* SFX: impact on visual appear (frame 3) */}
        <Sequence from={3}>
          <Audio src={staticFile('sfx/impact-light.wav')} volume={0.30} />
        </Sequence>
      </Sequence>

      {/* ═══ SCENE 2: Promise (1.5–5s = frames 45–150) ═══ */}
      <Sequence from={45} durationInFrames={105}>
        <Audio src={staticFile('sfx/whoosh-light.wav')} volume={0.25} />
        <PromiseScene
          text={hookScript.promise}
          keyNumber={hookScript.keyNumber}
          palette={palette}
        />
        <LightLeak position="top" color={palette.data} intensity={0.08} />
        {/* SFX: snare impact when number locks in (~frame 30) */}
        <Sequence from={30}>
          <Audio src={staticFile('sfx/impact-snare.wav')} volume={0.30} />
        </Sequence>
      </Sequence>

      {/* ═══ SCENE 3: Delivery (5–25s = frames 150–750) ═══ */}
      {/* Internal visual refreshes every 60-90 frames keep eyes engaged */}
      <Sequence from={150} durationInFrames={600}>
        {/* Riser pre-empts the hard cut to Delivery */}
        <Sequence from={-20}>
          <Audio src={staticFile('sfx/riser-shimmer.wav')} volume={0.35} />
        </Sequence>
        <Audio src={staticFile('sfx/impact-bass.wav')} volume={0.35} />
        <DeliveryScene
          text={hookScript.delivery}
          proofVisual={visuals.proof}
          palette={palette}
        />
        <ImpactSequence />
        {/* Internal transition whooshes at visual change points */}
        <Sequence from={75}>
          <Audio src={staticFile('sfx/whoosh-light.wav')} volume={0.18} />
        </Sequence>
        <Sequence from={165}>
          <Audio src={staticFile('sfx/whoosh-light.wav')} volume={0.18} />
        </Sequence>
        <Sequence from={300}>
          <Audio src={staticFile('sfx/whoosh-light.wav')} volume={0.18} />
        </Sequence>
        <Sequence from={450}>
          <Audio src={staticFile('sfx/whoosh-light.wav')} volume={0.15} />
        </Sequence>
        <LightLeak position="bottom" color={palette.accent} intensity={0.06} />
      </Sequence>

      {/* ═══ SCENE 4: Payoff (25–29s = frames 750–870) ═══ */}
      <Sequence from={750} durationInFrames={120}>
        <Audio src={staticFile('sfx/whoosh-heavy.wav')} volume={0.25} />
        <Sequence from={15}>
          <Audio src={staticFile('sfx/impact-light.wav')} volume={0.25} />
        </Sequence>
        <PayoffScene
          text={hookScript.payoff}
          palette={palette}
        />
        <LightLeak position="top" color={palette.success} intensity={0.08} />
      </Sequence>

      {/* ═══ SCENE 5: Loop Bridge (29–30s = frames 870–900) ═══ */}
      <Sequence from={870} durationInFrames={30}>
        <LoopBridge
          primaryVisual={visuals.primary}
          palette={palette}
          bridgeToFrame={0}
        />
      </Sequence>

      {/* ═══ LAYER 5: DYNAMIC VIGNETTE (always on top of content) ═══ */}
      <DynamicVignette
        intensity={
          (frame >= 140 && frame <= 155) ? 0.35
          : (frame >= 740 && frame <= 755) ? 0.30
          : 0.18
        }
      />

      {/* ═══ LAYER 6: FILM GRAIN (topmost, always) ═══ */}
      <FilmGrain />

      {/* ═══ LAYER 7: CHROMATIC ABERRATION (Scene 3 impact cut only) ═══ */}
      <Sequence from={150} durationInFrames={8}>
        <ChromaticAberration
          intensity={interpolate(
            spring({ frame: frame - 150, fps, config: { damping: 300 } }),
            [0, 1], [1, 0]
          )}
        />
      </Sequence>

      {/* Light leak flash at Scene 1 → 2 transition */}
      <Sequence from={40} durationInFrames={15}>
        <LightLeak position="top" color={palette.accent} intensity={0.15} />
      </Sequence>

    </AbsoluteFill>
  );
};
```

---

## 9:16 Atmosphere Components

All atmosphere components are adapted for the vertical 1080×1920 frame.

### BackgroundAtmosphere (vertical gradient direction)

The gradient flows **top-to-bottom** (not diagonal) to suit the tall vertical frame. The radial key light
is positioned in the upper-center safe zone, where text and faces typically appear.

```tsx
const BackgroundAtmosphere: React.FC<{
  frame: number; fps: number;
}> = ({ frame, fps }) => {
  // Slow gradient vertical drift
  const shift = interpolate(frame, [0, 900], [0, 8]);
  // Subtle hue oscillation
  const hue = interpolate(Math.sin(frame * 0.008), [-1, 1], [220, 242]);

  return (
    <AbsoluteFill style={{
      // Vertical gradient — top dark, mid slightly lighter, bottom darkest
      background: `linear-gradient(180deg,
        hsl(${hue}, 16%, ${4 + shift * 0.05}%) 0%,
        hsl(${hue + 8}, 12%, ${6 + shift * 0.03}%) 40%,
        hsl(${hue - 3}, 20%, 3%) 100%)`,
    }}>
      {/* Key light: upper-center (above text safe zone) */}
      <div style={{
        position: 'absolute',
        top: '10%',
        left: '25%',
        width: '50%',
        height: '35%',
        background: `radial-gradient(ellipse, rgba(255,255,255,0.025), transparent 70%)`,
        filter: 'blur(60px)',
      }} />
      {/* Accent glow: lower center (below text safe zone) */}
      <div style={{
        position: 'absolute',
        bottom: '15%',
        left: '30%',
        width: '40%',
        height: '20%',
        background: `radial-gradient(ellipse, rgba(100,120,255,0.015), transparent 70%)`,
        filter: 'blur(80px)',
      }} />
    </AbsoluteFill>
  );
};
```

### DynamicVignette (vertical ellipse)

The ellipse is **taller than it is wide** to match the 9:16 aspect ratio. This prevents over-darkening
the left/right edges (which are narrow) and concentrates the vignette on top/bottom instead.

```tsx
const DynamicVignette: React.FC<{
  intensity?: number;
}> = ({ intensity = 0.18 }) => {
  const frame = useCurrentFrame();
  // Slow breathing — 0.8× to 1.2× intensity
  const breathe = interpolate(
    Math.sin(frame * 0.025), [-1, 1], [intensity * 0.8, intensity * 1.2]
  );
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        // Vertical ellipse: 70% wide, 55% tall center clear zone
        background: `radial-gradient(
          ellipse 70% 55% at center,
          transparent 50%,
          rgba(0,0,0,${breathe * 0.55}) 78%,
          rgba(0,0,0,${breathe}) 100%
        )`,
      }}
    />
  );
};
```

### FloatingParticles (fewer count, narrower spread)

Particle count is reduced from 20 (16:9) to 12 (9:16), and horizontal spread is constrained so particles
don't bunch on the narrow left/right edges. Vertical drift speed is increased slightly to suit the tall frame.

```tsx
const FloatingParticles: React.FC<{
  count?: number; color?: string;
}> = ({ count = 12, color = 'rgba(255,255,255,0.15)' }) => {
  const frame = useCurrentFrame();
  const particles = useMemo(() =>
    Array.from({ length: count }, (_, i) => ({
      // Narrower horizontal spread: 10%-90% (not 0%-100%)
      x: 10 + (i * 137.508) % 80,
      y: (i * 57.2958) % 100,
      size: 1 + (i % 3),          // max 3px (vs 4px in 16:9)
      speedY: 0.25 + (i % 5) * 0.12, // slightly faster vertical drift
      speedX: 0.05 + (i % 3) * 0.03,
      blur: i < 2 ? 4 : 0,        // 2 bokeh particles (vs 3 in 16:9)
      opacity: i < 2 ? 0.07 : 0.10 + (i % 3) * 0.05,
    }))
  , [count]);

  return (
    <AbsoluteFill style={{ pointerEvents: 'none', overflow: 'hidden' }}>
      {particles.map((p, i) => (
        <div key={i} style={{
          position: 'absolute',
          left: `${(p.x + frame * p.speedX * 0.04) % 105 - 3}%`,
          top: `${(p.y + Math.sin(frame * 0.018 + i) * 2 + frame * p.speedY * 0.025) % 108 - 4}%`,
          width: p.size,
          height: p.size,
          borderRadius: '50%',
          backgroundColor: color,
          opacity: p.opacity,
          filter: p.blur ? `blur(${p.blur}px)` : undefined,
          boxShadow: `0 0 ${p.size * 3}px ${color}`,
        }} />
      ))}
    </AbsoluteFill>
  );
};
```

### LightLeak (top/bottom positions)

Vertical format replaces the four corner positions with **top** and **bottom** positions. The ellipse is
wider than it is tall to spread across the full 1080px width from either edge.

```tsx
const LightLeak: React.FC<{
  position: 'top' | 'bottom';
  color?: string; intensity?: number;
}> = ({ position, color = '#ff8844', intensity = 0.08 }) => {
  const frame = useCurrentFrame();
  const pulse = interpolate(Math.sin(frame * 0.035), [-1, 1], [0.65, 1]);
  const posMap = {
    'top':    { top: '-25%', left: '-10%' },
    'bottom': { bottom: '-25%', left: '-10%' },
  };
  return (
    <div style={{
      position: 'absolute',
      ...posMap[position],
      // Wide and short: spans full width, minimal vertical intrusion
      width: '120%',
      height: '55%',
      background: `radial-gradient(ellipse 80% 50%, ${color}, transparent 70%)`,
      opacity: intensity * pulse,
      pointerEvents: 'none',
      mixBlendMode: 'screen',
    }} />
  );
};
```

### FilmGrain (identical to 16:9)

Film grain operates at the pixel level and is aspect-ratio agnostic. Use the same implementation.

```tsx
const FilmGrain: React.FC = () => {
  const frame = useCurrentFrame();
  // Pseudo-random seed per frame produces static grain flicker
  const seed = (frame * 9301 + 49297) % 233280;
  const grainOpacity = 0.035;

  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        opacity: grainOpacity,
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200'
          xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence
          type='fractalNoise' baseFrequency='0.75' numOctaves='4'
          seed='${seed % 100}' stitchTiles='stitch'/%3E%3C/filter%3E
          %3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E")`,
        backgroundSize: 'cover',
        mixBlendMode: 'overlay',
      }}
    />
  );
};
```

### ChromaticAberration (identical to 16:9, impact moments only)

Channel separation is measured in pixels (not percentages), so it has no aspect-ratio dependency.
**Only ever active for 2–8 frames at impact cuts. Never run continuously.**

```tsx
const ChromaticAberration: React.FC<{
  intensity: number; // 0–1, pass an animated spring value
}> = ({ intensity }) => {
  const offset = intensity * 8; // max 8px shift at full intensity
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* Red channel: shifts left */}
      <AbsoluteFill style={{
        mixBlendMode: 'screen',
        backgroundColor: 'rgba(255,0,0,0.06)',
        transform: `translateX(${-offset}px)`,
        opacity: intensity,
      }} />
      {/* Blue channel: shifts right */}
      <AbsoluteFill style={{
        mixBlendMode: 'screen',
        backgroundColor: 'rgba(0,0,255,0.06)',
        transform: `translateX(${offset}px)`,
        opacity: intensity,
      }} />
    </AbsoluteFill>
  );
};
```

### ImpactSequence (same principles, adapted shake amplitude)

The shake amplitude is the same as 16:9 (6px max). In a narrow 1080px frame, 6px of horizontal shake
is proportionally slightly larger — acceptable because Shorts audiences expect more energy.

```tsx
const ImpactSequence: React.FC = () => {
  const frame = useCurrentFrame();

  const flashOpacity = interpolate(frame, [0, 4], [0.28, 0], {
    extrapolateRight: 'clamp',
  });

  const shakeIntensity = interpolate(frame, [0, 6], [6, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const shakeX = Math.sin(frame * 3) * shakeIntensity;
  const shakeY = Math.cos(frame * 2.5) * shakeIntensity;

  const chromaOffset = interpolate(frame, [0, 6], [8, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{
      transform: `translate(${shakeX}px, ${shakeY}px)`,
      pointerEvents: 'none',
    }}>
      {/* White flash */}
      <AbsoluteFill style={{
        backgroundColor: '#FFFFFF',
        opacity: flashOpacity,
      }} />
      {/* RGB split */}
      <AbsoluteFill style={{
        mixBlendMode: 'screen',
        opacity: chromaOffset > 0.5 ? 0.09 : 0,
      }}>
        <div style={{
          position: 'absolute', inset: 0,
          backgroundColor: 'rgba(255,0,0,0.5)',
          transform: `translateX(${-chromaOffset}px)`,
        }} />
        <div style={{
          position: 'absolute', inset: 0,
          backgroundColor: 'rgba(0,0,255,0.5)',
          transform: `translateX(${chromaOffset}px)`,
        }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## Core Animation Patterns for Shorts

### Spring Pop-In with Glow Burst (same as youtube-hooks)

```tsx
const popIn = (frame: number, fps: number, delay: number = 0) => {
  const s = spring({
    frame: frame - delay, fps,
    config: { damping: 200, stiffness: 300 },
  });
  return {
    scale: interpolate(s, [0, 1], [0.5, 1]),
    opacity: interpolate(s, [0, 1], [0, 1]),
    // Glow peaks at 50% spring progress, settles to 30% of peak
    glowIntensity: interpolate(s, [0, 0.5, 1], [0, 1, 0.3]),
  };
};

// Usage inside a component:
const { scale, opacity, glowIntensity } = popIn(frame, fps, 5);
// Apply to element:
// style={{ transform: `scale(${scale})`, opacity, filter: `brightness(${1 + glowIntensity * 0.4})` }}
```

### Word-by-Word Stagger (center-positioned for vertical safe zone)

Center alignment is mandatory in 9:16. All text is constrained to the horizontal safe zone (54–1026px).
`textAlign: 'center'` and `justifyContent: 'center'` are set on the container.

```tsx
const StaggeredText: React.FC<{
  text: string;
  accentWord?: string;
  accentColor?: string;
  fontSize?: number;
}> = ({ text, accentWord, accentColor = '#FFAA00', fontSize = 76 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(' ');
  const staggerDelay = 3; // frames between each word

  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',    // always centered in 9:16
      alignItems: 'center',
      gap: '0 14px',
      // Safe zone: left 54px, right 1026px → width 972px
      width: 972,
      margin: '0 auto',
      textAlign: 'center',
    }}>
      {words.map((word, i) => {
        const s = spring({
          frame: frame - i * staggerDelay, fps,
          config: { damping: 200, stiffness: 300 },
        });
        const isAccent = accentWord &&
          word.toLowerCase().includes(accentWord.toLowerCase());
        return (
          <span key={i} style={{
            display: 'inline-block',
            opacity: interpolate(s, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(s, [0, 1], [24, 0])}px)
                        scale(${interpolate(s, [0, 1], [0.8, isAccent ? 1.05 : 1])})`,
            fontSize,
            fontWeight: 900,
            fontFamily: 'Inter, sans-serif',
            color: isAccent ? accentColor : '#F0F0F0',
            textShadow: isAccent
              ? `0 0 24px ${accentColor}66, 0 0 48px ${accentColor}33,
                 0 2px 0 ${accentColor}44, 0 4px 0 ${accentColor}22`
              : '0 0 20px rgba(255,255,255,0.2), 0 2px 8px rgba(0,0,0,0.5)',
            lineHeight: 1.15,
          }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

### Slot Machine Data Counter (same as youtube-hooks)

No adaptation needed — the component is fully self-contained and works at any resolution.

```tsx
const SlotMachineCounter: React.FC<{
  target: number; suffix?: string; lockFrame?: number; color?: string;
}> = ({ target, suffix = '', lockFrame = 20, color = '#FFAA00' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const isLocked = frame >= lockFrame;

  const displayValue = isLocked
    ? target
    : Math.floor(Math.random() * target * 2);

  const lockSpring = spring({
    frame: frame - lockFrame, fps,
    config: { damping: 100, stiffness: 500 },
  });
  const glowRadius = isLocked
    ? interpolate(lockSpring, [0, 1], [60, 20])
    : 10;
  const glowOpacity = isLocked
    ? interpolate(lockSpring, [0, 0.3, 1], [0.8, 0.5, 0.2])
    : 0.1;

  const shakeOffset = (isLocked && frame - lockFrame < 3)
    ? Math.sin(frame * 5) * 2 : 0;

  return (
    <div style={{
      transform: `translateX(${shakeOffset}px)`,
      textAlign: 'center',
    }}>
      <div style={{
        fontSize: 148,        // slightly larger — fills vertical safe zone well
        fontWeight: 900,
        fontFamily: 'Inter, sans-serif',
        color,
        textShadow: `0 0 ${glowRadius}px ${color}${Math.round(glowOpacity * 255).toString(16).padStart(2, '0')},
                      0 0 ${glowRadius * 2}px ${color}33,
                      0 4px 0 ${color}44, 0 8px 0 ${color}22`,
        letterSpacing: isLocked ? '0' : '2px',
      }}>
        {displayValue}{suffix}
      </div>
    </div>
  );
};
```

### Cinematic Ken Burns (vertical pan for 9:16)

In the horizontal format, pan direction is left/right. For vertical 9:16, prefer **vertical pan**
(up/down) because the tall frame has more room to travel vertically. Zoom scale is the same.

```tsx
const CinematicKenBurns: React.FC<{
  src: string;
  durationFrames: number;
  direction?: 'in' | 'out';
  panDirection?: 'up' | 'down' | 'left' | 'right';
}> = ({ src, durationFrames, direction = 'in', panDirection = 'up' }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, durationFrames], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  });

  const scale = direction === 'in'
    ? interpolate(progress, [0, 1], [1, 1.08])
    : interpolate(progress, [0, 1], [1.08, 1]);

  // Vertical pan: preferred for 9:16 (more visual travel room)
  const panY = panDirection === 'up'
    ? interpolate(progress, [0, 1], [0, -2])
    : panDirection === 'down'
    ? interpolate(progress, [0, 1], [0, 2])
    : 0;
  // Horizontal pan: still available but narrower range
  const panX = panDirection === 'left'
    ? interpolate(progress, [0, 1], [0, -1.2])
    : panDirection === 'right'
    ? interpolate(progress, [0, 1], [0, 1.2])
    : 0;

  return (
    <div style={{ overflow: 'hidden', width: '100%', height: '100%' }}>
      <Img src={src} style={{
        width: '100%', height: '100%', objectFit: 'cover',
        transform: `scale(${scale}) translateX(${panX}%) translateY(${panY}%)`,
      }} />
    </div>
  );
};
```

### Device Frame (phone-style for 9:16)

The 16:9 youtube-hooks skill uses a browser or IDE frame. Shorts content is natively consumed on
a phone, so the device frame becomes a **phone shell** — appropriate for showing app UIs, TikTok
screenshots, or any mobile-first content. Positioned in the vertical safe zone.

```tsx
const DeviceFrame: React.FC<{
  children: React.ReactNode;
  showNotch?: boolean;
  showHomeBar?: boolean;
}> = ({ children, showNotch = true, showHomeBar = true }) => {
  return (
    <div style={{
      position: 'relative',
      // 78% of 1080px wide = 842px, maintains 9:16 proportions for inner content
      width: '78%',
      margin: '0 auto',
      borderRadius: 44,
      overflow: 'hidden',
      border: '3px solid rgba(255,255,255,0.12)',
      boxShadow: [
        '0 0 0 6px rgba(255,255,255,0.05)',
        '0 30px 100px rgba(0,0,0,0.7)',
        '0 10px 40px rgba(0,0,0,0.5)',
        'inset 0 1px 0 rgba(255,255,255,0.15)',
      ].join(', '),
    }}>
      {/* Status bar (notch area) */}
      {showNotch && (
        <div style={{
          height: 44,
          backgroundColor: 'rgba(10,10,10,0.95)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          {/* Dynamic Island / notch pill */}
          <div style={{
            width: 120, height: 32,
            backgroundColor: '#000',
            borderRadius: 20,
          }} />
        </div>
      )}

      {/* Screen content */}
      <div style={{ position: 'relative', backgroundColor: '#000' }}>
        {children}
      </div>

      {/* Home bar */}
      {showHomeBar && (
        <div style={{
          height: 32,
          backgroundColor: 'rgba(10,10,10,0.95)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <div style={{
            width: 130, height: 5,
            backgroundColor: 'rgba(255,255,255,0.35)',
            borderRadius: 3,
          }} />
        </div>
      )}
    </div>
  );
};
```

### Glass Callout (safe zone positioned)

The callout is positioned using pixel values clamped to the Shorts safe zone (see constants below).
Width is constrained to `972px` (safe zone width) max. Font size is slightly larger than the 16:9
version because the viewer is holding the phone 20–30cm away.

```tsx
const GlassCallout: React.FC<{
  text: string;
  // Pixel Y position within frame — keep between SHORTS_SAFE_ZONE.top and .bottom
  yPx?: number;
  color?: string;
}> = ({ text, yPx = 1200, color = '#FFAA00' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 200, stiffness: 250 } });

  return (
    <div style={{
      position: 'absolute',
      // Horizontally centered, safe zone aligned
      left: 54,
      right: 54,
      top: yPx,
      transform: `scale(${interpolate(s, [0, 1], [0.85, 1])})`,
      opacity: interpolate(s, [0, 1], [0, 1]),
      padding: '14px 24px',
      borderRadius: 14,
      backgroundColor: 'rgba(20,20,40,0.65)',
      backdropFilter: 'blur(16px)',
      border: `1px solid ${color}44`,
      boxShadow: `0 0 24px ${color}22, 0 6px 20px rgba(0,0,0,0.35)`,
      fontSize: 28,         // larger than 16:9 (was 20px)
      fontWeight: 600,
      fontFamily: 'Inter, sans-serif',
      color: '#F0F0F0',
      textAlign: 'center',
    }}>
      {text}
    </div>
  );
};
```

---

## Safe Zone Constants

Use these constants everywhere in the composition. Never position text or interactive elements
outside the safe zone — platform UI (TikTok-style comments/likes, subscribe button) overlaps
the bottom 25% and the top 20% of the frame.

```tsx
const SHORTS_SAFE_ZONE = {
  top: 384,       // 20% of 1920 — above this: YouTube Shorts UI overlaps
  bottom: 1440,   // 75% of 1920 — below this: like/comment/share buttons
  left: 54,       // 5% of 1080
  right: 1026,    // 95% of 1080

  // Text center zone — most comfortable reading area
  textTop: 576,   // 30% of 1920
  textBottom: 1344, // 70% of 1920

  // Derived convenience values
  safeWidth: 972,   // right - left = 1026 - 54
  safeHeight: 1056, // bottom - top = 1440 - 384
  centerX: 540,     // 1080 / 2
  centerY: 912,     // safe zone vertical center = (384 + 1440) / 2
};

// Helper: vertically centered within safe zone
const safeCenterY = (elementHeightPx: number) =>
  SHORTS_SAFE_ZONE.centerY - elementHeightPx / 2;

// Helper: position in lower safe zone (callouts, subtitles)
const lowerThirdY = (elementHeightPx: number) =>
  SHORTS_SAFE_ZONE.bottom - 200 - elementHeightPx;
```

---

## SFX File Structure for Shorts

The file layout mirrors youtube-hooks exactly. The single key difference is that `music/background.mp3`
starts playing at **frame 0** with a short fade-in ramp, not at frame 660 like in the long-form hook.

```
public/
├── sfx/
│   ├── whoosh-heavy.wav      # Scene 3 entry, Payoff transition
│   ├── whoosh-light.wav      # Text animations, internal Delivery refreshes
│   ├── whoosh-whip.wav       # Rapid visual cuts inside Delivery scene
│   ├── riser-low.wav         # Not used in base Shorts hook (too slow for 30s)
│   ├── riser-shimmer.wav     # 1s build before Scene 3 hard cut
│   ├── riser-combo.wav       # Optional: use if hook > 45s
│   ├── impact-bass.wav       # Scene 3 entry (pattern interrupt equivalent)
│   ├── impact-snare.wav      # Promise scene number lock-in
│   ├── impact-light.wav      # Scroll-Stop visual appear, Payoff accent
│   ├── impact-boom.wav       # Reserve for highest-energy Shorts only
│   ├── ambient-digital.wav   # Background texture (loopable, 30s+)
│   └── click-ui.wav          # Optional: UI interaction moments in Delivery
└── music/
    └── background.mp3        # ← Starts at FRAME 0 (key difference from long-form)
                              #   Ramps from 0 → 0.12 volume over frames 0–60
                              #   Stays at 0.12 for the entire composition
```

**Music timing rationale:** Long-form hooks defer music to avoid signalling "intro" to the brain. In
Shorts, the entire video IS the hook — music from frame 0 creates energy and distinguishes the video
from adjacent silent content in the feed. Keep it low (≤0.12 relative volume) so VO stays king.

**All SFX rules apply equally:**
- WAV format for SFX (precise timing, no MP3 decode latency)
- Normalized to -3dB peak
- Maximum 3 SFX simultaneously (ambient + transition + accent)
- No SFX on the very first word of the hook — first SFX hits on the first visual change (~frame 3)

---

## Loop Bridge Component

The Loop Bridge occupies the final 30 frames (29–30s, frames 870–900). Its purpose is to make
the auto-replay invisible: when the video loops back to frame 0, the viewer's brain registers
continuity rather than a hard restart.

**Three matching conditions for seamless loop:**
1. **Background gradient** matches frame 0 color state
2. **Particle positions** are mathematically consistent (frame 0 positions reused)
3. **Atmosphere opacity** cross-fades back to frame 0 values

```tsx
const LoopBridge: React.FC<{
  primaryVisual: string;
  palette: { accent: string; [key: string]: string };
  bridgeToFrame: number; // always 0
}> = ({ primaryVisual, palette, bridgeToFrame }) => {
  const frame = useCurrentFrame(); // local frame within this Sequence (0–29)
  const { fps } = useVideoConfig();

  // Progress: 0 at frame 870 (start of bridge), 1 at frame 900 (= frame 0)
  const progress = interpolate(frame, [0, 29], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.4, 0, 0.6, 1), // smooth S-curve
  });

  // ── 1. Background gradient: match frame 0 color state ──────────────────
  // Frame 0 hue = 220 (from BackgroundAtmosphere at frame=0, sin(0)=0 → lerp midpoint)
  // Frame 870 hue drifts to ~228. Cross-fade back to 220.
  const hue870 = interpolate(Math.sin(870 * 0.008), [-1, 1], [220, 242]); // ~228
  const hue0 = interpolate(Math.sin(0 * 0.008), [-1, 1], [220, 242]);     // ~231 (sin=0 → midpoint)
  const bridgeHue = interpolate(progress, [0, 1], [hue870, hue0]);

  // ── 2. Primary visual: fade out the current scene, fade in the first scene ──
  const overlayOpacity = interpolate(progress, [0, 0.5, 1], [0, 0.6, 1], {
    easing: Easing.out(Easing.quad),
  });

  // ── 3. Particle continuity: particles are deterministic by frame number,
  //       so frame 900 % 900 = 0 — the particle math naturally wraps.
  //       No extra work needed for FloatingParticles (it uses frame directly).
  // ── 4. Vignette: fades back to frame 0 intensity (0.18) ──────────────────
  const bridgeVignetteIntensity = interpolate(progress, [0, 1], [0.22, 0.18]);

  // ── 5. Light leak: brief top flash signals the "start" is near ───────────
  const leakIntensity = interpolate(
    progress,
    [0, 0.3, 0.7, 1],
    [0, 0.12, 0.10, 0.08]
  );

  return (
    <AbsoluteFill>

      {/* Gradient cross-fade back to frame 0 atmosphere */}
      <AbsoluteFill style={{
        background: `linear-gradient(180deg,
          hsl(${bridgeHue}, 16%, 4%) 0%,
          hsl(${bridgeHue + 8}, 12%, 6%) 40%,
          hsl(${bridgeHue - 3}, 20%, 3%) 100%)`,
        opacity: progress,
      }} />

      {/* Primary visual fade: current scene out → hero image in */}
      <AbsoluteFill style={{ opacity: overlayOpacity }}>
        <Img
          src={primaryVisual}
          style={{
            width: '100%', height: '100%', objectFit: 'cover',
            filter: 'brightness(0.4) saturate(0.8)',
          }}
        />
      </AbsoluteFill>

      {/* Gradient overlay matching frame 0 composition look */}
      <AbsoluteFill style={{
        background: `linear-gradient(
          180deg,
          rgba(10,10,26,0.55) 0%,
          rgba(10,10,26,0.25) 45%,
          rgba(10,10,26,0.75) 100%
        )`,
        opacity: interpolate(progress, [0, 1], [0, 1]),
      }} />

      {/* Scroll-Stop text ghost: fades in at the very end (primes frame 0) */}
      <AbsoluteFill style={{
        opacity: interpolate(progress, [0.7, 1], [0, 0.3]),
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        {/* Intentionally very faint — just enough to prime recognition */}
      </AbsoluteFill>

      {/* Bridge vignette */}
      <AbsoluteFill style={{
        pointerEvents: 'none',
        background: `radial-gradient(
          ellipse 70% 55% at center,
          transparent 50%,
          rgba(0,0,0,${bridgeVignetteIntensity * 0.55}) 78%,
          rgba(0,0,0,${bridgeVignetteIntensity}) 100%
        )`,
      }} />

      {/* Top light leak priming frame 0 atmosphere */}
      <div style={{
        position: 'absolute',
        top: '-25%', left: '-10%',
        width: '120%', height: '55%',
        background: `radial-gradient(ellipse 80% 50%, ${palette.accent}, transparent 70%)`,
        opacity: leakIntensity,
        mixBlendMode: 'screen',
        pointerEvents: 'none',
      }} />

    </AbsoluteFill>
  );
};
```

**Loop Bridge audio:** No SFX fires during the Loop Bridge — the ambient texture and music bed
continue uninterrupted, creating an audio through-line across the loop point. The last word of
the voiceover (if it ends before frame 870) leaves 1–2s of music-only before the bridge begins.

---

## TransitionSeries for Shorts Scenes

```tsx
<TransitionSeries>
  {/* Scene 1: Scroll-Stop */}
  <TransitionSeries.Sequence durationInFrames={45}>
    <ScrollStopScene ... />
  </TransitionSeries.Sequence>

  {/* Spring slide → Promise */}
  <TransitionSeries.Transition
    presentation={slide({ direction: 'from-bottom' })}   // vertical slide for 9:16
    timing={springTiming({ config: { damping: 220, stiffness: 320 } })}
  />

  {/* Scene 2: Promise */}
  <TransitionSeries.Sequence durationInFrames={105}>
    <PromiseScene ... />
  </TransitionSeries.Sequence>

  {/* Hard cut + ImpactSequence overlay → Delivery */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 3 })}       // near-instant — feels like a hard cut
  />

  {/* Scene 3: Delivery */}
  <TransitionSeries.Sequence durationInFrames={600}>
    <DeliveryScene ... />
  </TransitionSeries.Sequence>

  {/* Smooth fade → Payoff */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 18 })}
  />

  {/* Scene 4: Payoff */}
  <TransitionSeries.Sequence durationInFrames={120}>
    <PayoffScene ... />
  </TransitionSeries.Sequence>

  {/* Dissolve → Loop Bridge (no hard cut — continuity is the goal) */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 12 })}
  />

  {/* Scene 5: Loop Bridge */}
  <TransitionSeries.Sequence durationInFrames={30}>
    <LoopBridge ... />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

**Transition direction note:** Use `from-bottom` (vertical slide) for Shorts scene transitions
instead of `from-right` used in the 16:9 hook. Vertical movement matches the native swipe gesture
of the Shorts feed, creating subconscious format coherence.
