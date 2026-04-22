# Visual Design Reference — YouTube Shorts Hooks (9:16)

> Adapted from the youtube-hooks cinematic visual design system (Part 5), compressed for vertical format.  
> All pixel values assume 1080×1920 at 30fps.

---

## 9:16 Safe Zone Map

```
┌─────────────────────────────────────┐  y=0
│  ░░░░░░░░░  TOP DEAD ZONE  ░░░░░░░  │  y=0–384px    (0–20%)
│  Channel name · Subscribe button    │
│  Title overlay (platform-injected)  │
├─────────────────────────────────────┤  y=384px
│                                     │
│                                     │
│         ╔═══════════════╗           │
│         ║               ║           │
│         ║  SAFE ZONE    ║  ← 100%  │  y=384–1440px (20–75%)
│         ║  1080×1056px  ║  live     │
│         ║               ║  area     │
│         ║  All text,    ║           │
│         ║  faces,       ║           │
│         ║  key action   ║           │
│         ╚═══════════════╝           │
│                                     │
├─────────────────────────────────────┤  y=1440px
│  ░░░░░░░  BOTTOM DEAD ZONE  ░░░░░  │  y=1440–1920px (75–100%)
│  Like · Comment · Share · Subscribe │
│  Video title text (platform UI)     │
└─────────────────────────────────────┘  y=1920
```

**Precise pixel values:**

| Zone | Y start | Y end | Height | Notes |
|---|---|---|---|---|
| Top dead zone | 0px | 384px | 384px | Platform UI; never place critical content |
| Safe zone (top half) | 384px | 912px | 528px | Best for hook text, hero visuals |
| Safe zone (center) | 672px | 1248px | 576px | Eye-tracking sweet spot; highest attention |
| Safe zone (bottom half) | 912px | 1440px | 528px | Supporting text, lower-thirds |
| Bottom dead zone | 1440px | 1920px | 480px | Like/comment/share buttons; never use |
| **Total safe zone** | **384px** | **1440px** | **1056px** | **55% of frame height** |

**Vertical-specific rules:**
- Eye-tracking research confirms gaze concentrates on the **center third** of the vertical frame — position the single most important element at y=672–1248px, x=270–810px
- The narrow 1080px width means anything placed near x=0 or x=1080 risks the platform edge chrome on some devices; maintain a 60px horizontal margin minimum
- Light leaks and atmosphere effects may extend into dead zones — only content (text, faces, key visuals) must stay in the safe zone

---

## The Shorts Visual Timeline (Frame-by-Frame)

At 30fps, a 30-second Short = **900 frames**. Every section must have visual activity on at least 3 of the 7 layer stack simultaneously (background atmosphere → midground particles → main subject → foreground elements → text & graphics → lighting FX → lens simulation).

```
FRAMES 0-45 (0–1.5s) — SCROLL-STOP
│
├── Frame 0: NEVER black. Atmosphere pre-loaded:
│   - Background gradient alive (subtle pulse, 2% scale breath)
│   - Particles already drifting downward (top→bottom direction)
│   - Subtle light leak bleeding from TOP edge (not left/right — vertical grammar)
│
├── Frame 0–6: Micro-ramp — atmosphere at 80% brightness, no subject yet.
│   Creates 0.2s of charged anticipation without emptiness.
│
├── Frame 6–18: PRIMARY VISUAL ERUPTS from center vertical axis:
│   - Spring pop: scale 0→108%→100% over 12 frames (stiffness 400, damping 200)
│   - Simultaneous bloom pulse behind subject: glow radius 0→200%→100%
│   - Entry direction: from center Z-axis (zoom in), NOT from left/right
│   - For text-only hooks: words fall from top edge with stagger
│
├── Frame 18–45: VISUAL HOLDS with LIVING MOTION:
│   - Ken Burns: slow Z-axis push (+2% scale over 1.5s) — no lateral drift
│   - Particles drift downward over the subject (foreground layer)
│   - Subtle vignette at base intensity (12% edge darkening)
│   - Hook text begins word-by-word spring reveal (40ms stagger per word)
│   - Accent word: +10% scale, channel accent color, 0.3s glow pulse
│
FRAMES 45-150 (1.5–5s) — PROMISE VISUAL
│
├── Frame 42–45: PRE-TRANSITION — light leak swells from bottom edge (0.3s)
│
├── Frame 45–51: VERTICAL CUT with compound transition:
│   - Main content slides upward (not sideways — vertical grammar)
│   - Background shifts color temperature (cool→warm or warm→cool)
│   - Particle layer micro-pauses 2 frames then resumes
│   - Whoosh SFX (upward pitch sweep)
│
├── Frame 51–120: PROMISE CONTENT — the "why you should keep watching" visual:
│   - Number/result/claim enters with slot-machine digit scramble
│   - Behind the number: radial glow pulse synced to impact SFX
│   - Screen shake on lock-in: 3px diagonal, 3 frames, spring-dampened
│   - For comparison promises: vertical split (top/bottom) begins forming
│   - Device frame (phone mockup) slides down into frame from top edge
│
└── Frame 120–150: Energy build — Z-zoom rate +0.5%, particles accelerate 15%
    Vignette tightens 3% (subconscious pressure signal)

FRAMES 150-750 (5–25s) — DELIVERY
│  Visual change every 60–90 frames (2–3s). Faster than long-form (3–5s).
│  Each segment follows: pre-transition (3 frames) → cut → new content → hold → repeat.
│
├── DELIVERY SEGMENT PATTERN (repeat every 60–90 frames):
│   ┌── [F-3 to F-0]:  Light leak swells from entry direction of next shot
│   ├── [F+0]:          Hard cut — new section, shifted color temperature
│   ├── [F+0 to F+6]:   New content enters — spring overshoot from top or Z-axis
│   ├── [F+6 to F-6]:   HOLD with living motion (Ken Burns Z-push, particles, text)
│   └── [F-6 to F+0]:   Outgoing element slides UP (not to side) as next builds
│
├── IMPACT MOMENTS (at major reveals within Delivery, max 2):
│   - Frame N+0: Flash (white, 20% opacity, full screen, 1 frame)
│   - Frame N+1: Chromatic aberration spike (RGB split 6px, 1 frame)
│   - Frame N+2: Screen shake (5px diagonal, spring-damped, 3 frames)
│   - Frame N+3: HARD CUT to contrasting visual with opposite color temp
│
├── EVIDENCE SEGMENTS — Screen recording/UI shown with depth treatment:
│   - Recording in device frame (phone chrome) — not raw fullscreen
│   - Drop shadow under device frame (depth signal)
│   - Background: blurred, desaturated duplicate at 40% opacity
│   - Callouts: glassmorphism style (backdrop-blur 12px + thin bright border)
│   - Zoom into detail: smooth 150% Z-push, vignette following focal point
│
└── VISUAL CRESCENDO — highest layer count of the entire Short occurs here:
    Main subject + particle system + text overlay + device frame + glow FX
    This is the visual peak. All 7 layers active simultaneously.

FRAMES 750-870 (25–29s) — PAYOFF
│
├── Frame 747–750: Elegant transition — smooth dissolve (NOT hard cut here).
│   The contrast with the hard Delivery cuts signals "we're landing."
│
├── Frame 750–810: RESULT/ANSWER delivery:
│   - Clean, centered composition — reduce active layer count to 4
│   - Before/After: VERTICAL split (top = before, bottom = after)
│     · Top half: slightly desaturated, cool grade, slow downward drift
│     · Bottom half: full saturation, warm grade, slow upward drift (visual tension)
│     · Divider: 1px solid + 20px glow (energy line), slides in from center
│   - OR: Single full-frame result with maximum saturation boost (+15%)
│   - Key result text: centered in safe zone, maximum size (128px+)
│
├── Frame 810–855: VISUAL EXHALE — brief rest before loop:
│   - Particles slow to 50% speed
│   - Vignette softens to 8% (least tight in entire Short)
│   - Clean backgrounds: breathing room signals completion
│   - Takeaway text holds, no new elements entering
│
└── Frame 855–870: Begin warm-up for loop bridge
    Color temperature starts shifting back toward Frame 0's palette

FRAMES 870-900 (29–30s) — LOOP BRIDGE
│
├── Frame 870–885: VISUAL CALLBACK — echo of Frame 0's composition:
│   - Same color temperature as opening
│   - Same particle density as opening
│   - Subtle suggestion of the opening visual (blurred or partial)
│
├── Frame 885–897: LOOP TENSION — one unresolved visual element:
│   - A detail from the payoff that "leads" back to the opening question
│   - OR: The opening hook text fades back in (ghost at 30% opacity)
│   - This is why viewers rewatch: the brain seeks resolution of the loop
│
└── Frame 897–900: SEAMLESS HAND-OFF:
    Atmosphere, particle positions, and color temperature match Frame 0 exactly.
    The Short loops invisibly. Every rewatch = another engagement signal.
```

---

## 8 Visual Patterns for Shorts

### Pattern 1 — Result Flash

**What it is:** Show the end result for 1 second, then hard-cut back to the beginning state. The viewer has seen the destination; now they want the path.

**How it differs in 9:16:** In 16:9, the result is shown wide across the full horizontal frame. In 9:16, the result fills the entire vertical frame — face-filling close-up or full-screen result screenshot in a device frame. The narrow format makes this MORE impactful because there is nowhere to look except at the result. Show it desaturated/blown-out (as if "remembered"), then snap to full-color present.

**Cinematic execution:**
- Frame 0–30: Result visual, desaturated (filter: saturate(0.6)), slight bloom overlay, film grain at 5%
- Frame 30–33: Flash (white, 30% opacity) + chromatic aberration 4px, 2 frames
- Frame 33+: Hard cut to beginning state, full color, Z-axis pop

**Best hook formula pairing:** Transformation Preview, Problem-Solution, Before/After Reveal

---

### Pattern 2 — Split Comparison

**What it is:** Two tools, results, or approaches shown simultaneously for direct contrast.

**How it differs in 9:16:** The split is **top/bottom** (horizontal divider), NOT left/right. A vertical split in 9:16 gives each side only 540px of width — too narrow for legible UI or text. A horizontal split gives each side 960px of height and the full 1080px width. Top = the inferior/baseline option (cooler color grade, slightly desaturated). Bottom = the superior/result option (warmer, fully saturated). The divider is an energy line (1px solid + 20px glow) that slides in from the left edge over 12 frames.

**Cinematic execution:**
- Both halves have independent Ken Burns: top drifts downward 1%, bottom drifts upward 1% (visual tension)
- Color temperature difference: top = `hue-rotate(-10deg) saturate(0.8)`, bottom = `hue-rotate(+5deg) saturate(1.1)`
- Label text: top-left corner of each half, glassmorphism pill (backdrop-blur + border)

**Best hook formula pairing:** Comparison Verdict, Honest Evaluation, Better Alternative

---

### Pattern 3 — Data Counter

**What it is:** A key number animates from zero (or a bad number) to the final impressive value.

**How it differs in 9:16:** In 16:9, a counter can be placed off-center for composition. In 9:16, center the number on the vertical axis at the safe-zone midpoint (y≈912px). Make it larger — 180px+ font size — because mobile screens shrink everything. The impact moment (number lock-in) benefits from a full-screen radial glow burst that works dramatically in vertical because the narrow frame concentrates the explosion effect.

**Cinematic execution:**
- Slot-machine style: random digits flash at 2-frame intervals for 0.5s (not smooth interpolation)
- Lock-in: impact SFX + radial glow burst (0→300px radius, 0.3s) + screen shake (4px, 3 frames)
- Number color: accent color + layered text-shadow for volumetric depth (5 shadows, 1–5px offset)
- Supporting unit text (%, K, hrs) enters 3 frames after the number locks

**Best hook formula pairing:** Stakes Escalation, Comparison Verdict, Data-Driven Claims

---

### Pattern 4 — UI Reveal

**What it is:** A tool's interface slides into view with key elements highlighted, showing the product in action.

**How it differs in 9:16:** Use a **phone mockup frame** rather than a browser/desktop frame — it matches the viewer's context and triggers processing fluency (same device type). The phone frame slides DOWN from the top edge of the safe zone (top→bottom entry, vertical grammar). Behind the device: gaussian-blurred, enlarged, desaturated duplicate of the same UI (depth-of-field simulation). Callouts must be larger than in 16:9 — minimum 48px — and positioned above/below the highlighted element rather than to the side (no horizontal space).

**Cinematic execution:**
- Device frame enters from y=-600 with spring (stiffness 300, damping 180) — overshoots 20px then settles
- Callout arrows point upward or downward (not sideways)
- Glassmorphism callout: `backdrop-filter: blur(12px)`, `border: 1px solid rgba(255,255,255,0.25)`, corner radius 12px
- Zoom to detail: Z-axis push into phone screen (scale 1.0 → 1.4 over 30 frames), vignette follows focal point

**Best hook formula pairing:** Hidden Discovery, Tool Demonstration, Transformation Preview

---

### Pattern 5 — Code Typewriter

**What it is:** Code appears character by character in real-time, as if being written now.

**How it differs in 9:16:** A 16:9 code block can span 80+ characters per line. 9:16 safe zone is ~1080px wide, allowing roughly 32–40 monospace characters per line at readable size. Use **larger font (28–32px)**, **fewer lines visible (5–8 max)**, and let the code scroll upward as new lines are typed (vertical scroll mirrors the platform's own scroll mechanic — subliminal familiarity). The narrow frame makes the glowing cursor more prominent and dramatic.

**Cinematic execution:**
- IDE background: deep dark with 3% opacity horizontal scan lines (CRT aesthetic)
- Each new character: faint glow for 5 frames after appearing (`text-shadow: 0 0 8px currentColor`)
- Cursor: soft halo (`box-shadow: 0 0 12px accent_color`), not just blinking block
- Syntax highlighting: comments in muted green, strings in amber, keywords in accent blue
- Code scrolls upward at 1 line per 18 frames when block exceeds 8 lines

**Best hook formula pairing:** Tutorial Hook, Problem-Solution, Transformation (technical)

---

### Pattern 6 — Before/After Flip

**What it is:** Two states separated by a dramatic transition — the transformation made visceral.

**How it differs in 9:16:** Use a **vertical wipe** (top-to-bottom reveal of the After state) rather than a left/right split — this follows the natural scroll direction and feels native. Alternatively: the top half shows Before, the bottom half shows After, with the divider sliding from above. The Before state uses cool color grade + desaturation. The After state snaps to full saturation + warm grade. In 16:9 this contrast spans the horizontal width; in 9:16 the full-height contrast is more striking because the color shift occupies the entire peripheral vision.

**Cinematic execution:**
- Before: `filter: saturate(0.65) hue-rotate(-12deg) brightness(0.9)`
- Transition: 3-frame impact sequence (flash + chromatic aberration 6px + shake 5px)
- After: `filter: saturate(1.15) hue-rotate(+5deg) brightness(1.05)` — overcorrect slightly
- Wipe direction: top-to-bottom over 12 frames (clip-path `polygon(0 0, 100% 0, 100% N%, 0 N%)`)
- Label pills: "BEFORE" anchored top-center, "AFTER" anchored bottom-center of safe zone

**Best hook formula pairing:** Transformation Preview, Problem-Solution, Honest Evaluation

---

### Pattern 7 — Rapid Montage

**What it is:** 3–5 quick shots in the first 5 seconds (45–60 frames each) that establish context, credibility, or stakes.

**How it differs in 9:16:** In 16:9, shots can enter from left or right using lateral motion. In 9:16, alternate entry directions top-to-bottom and Z-axis: shot 1 = Z-push in, shot 2 = slides down from top, shot 3 = Z-push in, shot 4 = slides up from bottom. Between each shot: a **2-frame flutter cut** (alternating outgoing and incoming at 2-frame intervals for 4 total frames) — the blockbuster trailer technique. Each shot must be a tight, vertically-composed close-up (no wide establishing shots that waste the narrow frame).

**Cinematic execution:**
- Shot duration: 15–30 frames (0.5–1s) each
- Flutter cut between each: `opacity` oscillation + `scale` micro-pulse (0.97→1.0) at each alternation
- Color temperature: vary each shot (cool, warm, neutral, cool) for visual variety
- At least 1 shot is extreme close-up (face, hands, screen detail) for intimacy
- Text overlay: single bold word per shot, center frame, spring-pops in at frame 3 of each shot

**Best hook formula pairing:** Stakes Escalation, Curated Countdown, Social Proof

---

### Pattern 8 — Focused Zoom

**What it is:** Start wide (full screen/interface), then smooth Z-axis zoom into one specific detail — the hidden thing the hook promises to reveal.

**How it differs in 9:16:** In 16:9, a zoom might pan laterally to reach the detail. In 9:16, the zoom is **pure Z-axis** (no lateral pan — the narrow frame means any pan quickly loses the subject). The blur treatment outside the focal area is stronger in 9:16 because there is less peripheral space; the vignette can darken aggressively without losing content. The reveal callout (glassmorphism label) appears above or below the zoomed detail, never to the side.

**Cinematic execution:**
- Wide: `scale(1.0)` over frames 0–6 (establish the full frame)
- Zoom: `scale(1.0 → 1.8)` over 30 frames with `ease-in-out` timing
- Rack focus simulation: `filter: blur(0 → 6px)` on background as zoom progresses
- Vignette: tightens from 12% to 30% edge darkening in sync with zoom
- Callout springs in at zoom peak: glassmorphism, positioned above zoomed element
- SFX: subtle whoosh + final "click" at zoom endpoint

**Best hook formula pairing:** Hidden Discovery, Honest Evaluation, Tutorial Hook

---

## Atmosphere Toolkit for Shorts

These effects are composited on top of all content on every frame. Individually subtle; together they create the perceived production quality gap between amateur and professional.

### Film Grain

Apply as an SVG `feTurbulence` overlay. **Seed must change every frame** — static grain is a dead giveaway of cheap production.

- Opacity: **3–6%** (same as long-form — phones have sharp OLED screens, grain is visible at lower values)
- Grain size: fine (baseFrequency: 0.65, 1–2px effective size)
- Blend mode: `overlay`
- Slightly more visible in dark areas (natural film behavior)
- Do not reduce below 3% — invisible grain defeats its purpose

```tsx
<filter id={`grain-${frame}`}>
  <feTurbulence type="fractalNoise" baseFrequency="0.65"
    numOctaves="3" seed={frame} stitchTiles="stitch" />
</filter>
<rect width="100%" height="100%" filter={`url(#grain-${frame})`} opacity={0.04} />
```

### Dynamic Vignette

The 9:16 vignette uses a **tall vertical ellipse** (not circular) to match the frame shape. A circular vignette on a 9:16 frame creates dark corners that obscure safe-zone content.

- Shape: `ellipse 60% 45% at 50% 50%` (wider than tall to counteract frame proportions)
- Base intensity: **15%** edge darkening
- Impact moments (counter lock-in, before/after transition): **28–32%**
- Visual rest (payoff exhale): **8–10%**
- Breathing animation: `sin(frame × 0.03)` ±20% of base intensity

```tsx
background: `radial-gradient(ellipse 60% 45% at 50% 50%,
  transparent 48%,
  rgba(0,0,0,${breathe * 0.5}) 72%,
  rgba(0,0,0,${breathe}) 100%)`
```

### Floating Particles

The narrow 9:16 frame means fewer particles are needed — too many feel claustrophobic. Particles drift **top-to-bottom** (not random direction) to reinforce the vertical scroll grammar and avoid particles exiting the frame horizontally.

- Count: **10–15** (vs. 15–30 in 16:9)
- Movement: top→bottom primary drift, + sinusoidal lateral oscillation (±2% x-axis)
- Size: 1–3px core dots; 2–3 foreground bokeh blobs at 4–6px with `blur(4px)`
- Opacity: 10–25% (slightly lower than 16:9 due to smaller phone screen — saturation is higher)
- Color: match accent color or `rgba(255,255,255,0.12)`
- Golden-ratio y-distribution to prevent clustering

### Light Leaks

In 9:16, light leaks enter from **top and bottom edges** — NOT from left/right corners. Left/right leaks in a narrow frame are visually disruptive and unnatural. Top light leaks feel like overhead illumination; bottom leaks feel like reflected floor light or lens contamination during movement.

- Top leak: warm amber/gold (`#ffaa44`), 6–10% opacity, appears during upward transitions
- Bottom leak: cooler teal/white (`#88ccff`), 4–8% opacity, appears during downward transitions
- Trigger: always at cut transitions (frames -3 to +6 around each cut)
- Radial gradient: `ellipse 80% 30% at 50% 0%` for top, `ellipse 80% 30% at 50% 100%` for bottom
- Blend mode: `screen`
- Never have top and bottom leaks simultaneously — choose one per transition

### Chromatic Aberration

Identical principle to long-form: **impact moments only**, never continuous.

- Trigger events: counter lock-in, before/after flip impact, Pattern Interrupt cut
- Duration: **2–4 frames** (slightly shorter than 16:9's 3–6 because mobile attention is faster)
- Shift distance: **4–6px** (slightly less than 16:9's 3–8px — OLED screens exaggerate the effect)
- Always accompanied by impact SFX
- Spring-decay: effect dissolves by frame +3 — no lingering aberration

### Screen Shake

Same core principle as long-form: activates vestibular response, adds physical weight to impact.

- Trigger: same events as chromatic aberration (always paired)
- Displacement: **3–6px** (slightly less than 16:9 — phone-held viewing means the shake competes with real device movement)
- Duration: **3–4 frames**, spring-dampened
- Direction: diagonal (maximize perceived force with minimum displacement)
- Never use more than twice in a 30-second Short

---

## Text Animation for Shorts

### Word-by-Word Reveal Synced to Voiceover

Each word is an independent animated element with a spring pop. Words appear **0.1–0.2s before** the corresponding audio — this "leads" the viewer's eye and makes captions feel natural rather than lagging.

- Stagger interval: **40ms per word** (same as long-form)
- Spring config: `stiffness: 400, damping: 200` (snappy, minimal overshoot)
- Entry direction: words drop down from y-8px (follows vertical grammar)
- Exit: `opacity` fade over 10–12 frames, or slide upward as a block

### Pop + Scale for Hook Text

The hook text (first 1.5s) is the largest, boldest text in the entire Short.

- Entry animation: scale `0 → 1.08 → 1.0` over 10 frames (spring pop with 8% overshoot)
- Simultaneously: glow bloom `0 → 150% → 100%` behind text
- Font: Inter Black, Montserrat Black, or equivalent — minimum 96px at 1080×1920
- Never more than 2 lines; never more than 6–7 words total in the hook text block
- Position: center of safe zone (y≈720–960px), horizontally centered

### Kinetic Typography for Emphasis Words

The single most important word in each sentence gets kinetic treatment — all others are static.

- Scale pulse: `1.0 → 1.08 → 1.0` over 18 frames on entry
- Color: channel accent color (never more than 1 colored word per sentence)
- Glow: `text-shadow: 0 0 16px accent_color, 0 0 32px accent_color_30%`
- Volumetric depth: 4 layered text-shadows at 1–4px offsets with decreasing opacity
- One-time underline draw: SVG line animates from 0%→100% width under the word (12 frames)

### Safe Zone Positioning

| Text type | Vertical position | Notes |
|---|---|---|
| Hook text (hero) | y=620–960px (center third) | Maximum size, spring pop, glow |
| Supporting sentence | y=960–1280px | 72–80px, word-by-word reveal |
| Lower-third caption | y=1200–1380px | 48–56px, semi-transparent bg box |
| Counter/number | y=780–1060px (centered) | 160–200px, slot-machine reveal |
| Label pills | y=430–520px (top) or y=1340–1400px (bottom) | Glassmorphism, 36–42px |

**Hard rules:**
- No text above y=420px (top dead zone begins at y=384px — give 36px buffer)
- No text below y=1400px (bottom dead zone begins at y=1440px — give 40px buffer)
- Never center text horizontally with x offset — all text centered on x=540px unless intentional label
- Minimum contrast ratio: 7:1 (WCAG AAA) — phone screens in sunlight require this; 4.5:1 is insufficient outdoors

---

## Color & Contrast for 9:16

The youtube-hooks color system applies in full, with one mandatory adjustment: **boost saturation +15% across all palette values** for Shorts. Mobile OLED screens have higher color volume, and outdoor viewing in sunlight requires extra punch. What looks saturated on a monitor looks correct on a phone.

### Color Temperature by Section

| Section | Frames | Color temp | Background | Accent | Saturation boost |
|---|---|---|---|---|---|
| Scroll-Stop | 0–45 | Neutral-cool | `#080818` | Channel blue/cyan | +15% |
| Promise | 45–150 | Warming | `#0e0c14` | Amber gold `#f0a030` | +15% |
| Delivery (evidence) | 150–750 | Varies per beat | Desaturated duplicate | Clean white | +10% |
| Impact moments | At cuts | Sharp contrast shift | Opposite temp | Electric `#00ffcc` | +20% |
| Payoff | 750–870 | Warm, inviting | `#120c08` | Warm gold | +15% |
| Loop Bridge | 870–900 | Return to opening | Match Frame 0 | Match Frame 0 | +15% |

### Phone-Screen Contrast Rules

- All text on dark backgrounds: white + glow (`text-shadow: 0 0 20px rgba(255,255,255,0.35), 0 0 40px rgba(255,255,255,0.12)`)
- Accent colors: bump HSL saturation to 85–95% (vs 70–80% in long-form)
- Background gradients: keep dark base (`#080818` to `#0e0c14`) — phone screens have near-infinite contrast ratio; a dark background makes every foreground element pop harder than on a monitor
- Numbers and data: use `#f0a030` (amber) rather than pure white — warm colors appear more saturated on OLED and are easier to read in motion
- Color shift at Pattern Interrupt (impact cut): cool-to-warm OR warm-to-electric. The COLOR shift IS the pattern interrupt — the brain registers it as a separate neural event

### Palette Construction

```
BASE (background atmosphere):     #080818  → #0e0c14  (cool dark to neutral dark)
PRIMARY TEXT:                      #FFFFFF  with bloom glow
ACCENT (channel color):            HSL(200, 90%, 60%) boosted +15% saturation vs desktop
IMPACT / NUMBERS:                  #f0a030  (amber, OLED-optimized warm)
CONTRAST ELEMENT (interrupt):      #00e5ff  (electric teal) OR #ff4400 (electric red)
GLASSMORPHISM:                     rgba(255,255,255,0.08) bg + rgba(255,255,255,0.20) border
```

---

## Motion Rules for Vertical

### Direction Grammar

Long-form video uses left-to-right as its primary axis — matching reading direction and horizontal cinematic grammar. Shorts use a different spatial language, derived from the scroll mechanic itself:

| Motion type | Long-form (16:9) | Shorts (9:16) | Why |
|---|---|---|---|
| New information enters | From right | From top | Matches scroll-down direction |
| Completed information exits | To left | To top (upward) | Feels like "scrolled past" |
| Emphasis/drama | Lateral pan | Z-axis zoom in | Narrow frame; lateral pan loses subject |
| Transition between sections | Horizontal wipe | Vertical wipe OR Z-cut | Native to format |
| Background drift | Subtle horizontal | Subtle vertical | Reinforces scroll grammar |
| Before/After split | Left/Right | Top/Bottom | Each half has full width |

### Z-Axis Priority

In 9:16, **Z-axis movement (zoom in/out) is the primary cinematic tool**. The narrow frame means lateral camera moves either lose the subject or run out of frame in less than a second. Z-axis zooms:
- Feel more dramatic in a tall frame (more vertical distance to travel visually)
- Simulate the "approach" feeling that triggers the brain's approach-avoidance system
- Are native to how phones are held (screen faces the viewer — z-axis = toward you)

Use `scale()` transforms for Z simulation. Ken Burns: always Z-push (scale 1.0→1.05 over 30s) — never lateral drift.

### Visual Change Rate

| Format | Visual change frequency | Basis |
|---|---|---|
| Long-form YouTube hook | Every 3–5 seconds | High tolerance for setup |
| YouTube Shorts | Every 2–3 seconds | Zero tolerance for static frames |
| Shorts impact moments | Every 1–1.5 seconds | During Delivery section peaks |

A "visual change" counts as: a cut, a new text element entering, a zoom threshold crossed, a new layer activating, or a color temperature shift. The goal is that every time a viewer's attention begins to waver (≈every 2s), a new stimulus resets the loop.

### Spring Physics Defaults (Vertical Format)

Higher stiffness and damping than long-form for snappier, more energetic motion — matching the aggressive pacing of the format:

```
ENTRY springs:     stiffness: 400,  damping: 200  (snappy pop, minimal overshoot)
TEXT springs:      stiffness: 500,  damping: 250  (almost no overshoot — clean legibility)
DEVICE FRAME:      stiffness: 300,  damping: 180  (slight overshoot — physical weight)
IMPACT elements:   stiffness: 600,  damping: 150  (maximum snap, brief overshoot)
SLOW reveals:      stiffness: 120,  damping: 160  (smooth, weighted entry)
```

All exit animations: `opacity` fade over 8–12 frames. Exits are never springs — exits should be invisible, not felt.
