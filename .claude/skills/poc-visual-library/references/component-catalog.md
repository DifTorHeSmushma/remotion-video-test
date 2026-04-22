# POC Component Catalog

Complete catalog of 176+ reusable Remotion components across 30 POC categories. All components are deterministic, GPU-accelerated, and designed for 1920x1080 at 30fps.

**Stack**: Remotion 4.0 / React 19 / TypeScript 5.9

**Location**: `src/pocs/<NN>-<category>/`

---

## 01 - Cinematic Camera Effects (5 components)

Pure CSS transform-based camera simulations. No WebGL required.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| **KenBurnsImage** | Slow zoom/pan on images with spring physics | `preset`: zoom-in, zoom-out, pan-left, pan-right, diagonal-drift |
| **ParallaxLayers** | Multi-depth layer scrolling (3D depth illusion) | Layer count, speed multipliers |
| **CameraRig** | 3D perspective keyframe animation (orbit, dolly, pan, tilt, roll) | CSS `perspective` + `transform3d` |
| **ZoomReveal** | Netflix-style fly-in (scaled down + blurred to focus) | Spring overshoot, blur amount |
| **FocusPull** | Rack focus between foreground/background planes | Animated blur filters, spring transitions |

**Demo**: `CinematicCameraDemo.tsx` - 10s (300 frames)

---

## 02 - Data Visualizations (6 components)

SVG-based animated charts with spring physics and staggered entrances.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| **AnimatedBarChart** | Horizontal/vertical bars with spring entrance | Comparison mode, value counters |
| **AnimatedLineGraph** | Self-drawing SVG line with bezier curves | Data points, area fill, glow trail |
| **AnimatedCounter** | Rolling digit counter with formatting | `format`: number, percentage, currency, abbreviated; threshold color changes |
| **AnimatedPieChart** | Sequential segment sweeps, donut mode | Center text, pull-out highlight, label pop-ins |
| **NetworkGraph** | Node-and-edge with spring physics pop-ins | Animated SVG edges, pulse on active nodes |
| **ComparisonTable** | Rows slide from alternating sides | Check/cross icon pop-ins, highlight glow |

**Demo**: `DataVizDemo.tsx` - 15s (450 frames)

---

## 03 - Particle & Visual Effects (7 components)

Composable `AbsoluteFill` overlays for backgrounds, transitions, emphasis.

| Component | Description | Presets/Types |
|-----------|-------------|---------------|
| **ParticleField** | Configurable particle system | `floating-dots`, `rising-sparks`, `snow`, `confetti`, `matrix-rain`, `fireflies` |
| **GradientMesh** | Animated gradient mesh with Lissajous movement | `aurora`, `lava-lamp`, `ocean`, `sunset`, `nebula` |
| **MorphingBlob** | SVG blob morphing (Catmull-Rom to Bezier) | Gradient fill, glow option |
| **GlitchEffect** | RGB splitting, slice displacement, scanlines | `continuous` or `triggered` mode |
| **EnergyBeam** | Animated light beams with SVG glow | `spotlight`, `sunburst`, `laser-grid`, `light-leak` |
| **WaveBackground** | Layered SVG sine waves | `ocean-waves`, `sound-waves`, `mountain-range` |
| **AnimatedGrid** | Grid with ripple/glow and perspective tilt | Types: `lines`, `dots` |

**Performance**: Keep `ParticleField` count under 200. Matrix-rain and confetti are heavier.

**Demo**: `ParticleEffectsDemo.tsx` - 20s (600 frames)

---

## 04 - Code Animations (7 components + 1 utility)

Developer-oriented visuals for coding tutorials and tech explainers.

| Component | Description | Key Features |
|-----------|-------------|--------------|
| **TypewriterCode** | Character-by-character typing | Variable speed, blinking cursor, syntax highlighting, backspace/corrections |
| **AnimatedDiff** | Git diff visualization | Unified/side-by-side, red slides out, green slides in, animated +/- markers |
| **TerminalEmulator** | macOS terminal (red/yellow/green dots) | Command typing, output delays, ANSI colors, spinners, progress bars |
| **CodeHighlight** | Spotlight effect on code regions | Sequential walkthrough, bracket annotations, rest dims to 30% |
| **FileTree** | VS Code-style file explorer | Animated expand/collapse, file icons by extension, sequential expansion |
| **BrowserMockup** | Chrome browser window | Tab, URL typing, loading bar, content area |
| **APIFlow** | Client-to-server request/response | Method badges (GET/POST/PUT/DELETE), JSON cards, status codes |

**Utility**: `syntaxHighlight.ts` - Token-based highlighter: JS/TS, Python, Bash, JSON, HTML/JSX, CSS (Monokai-inspired)

**Demo**: `CodeAnimationsDemo.tsx` - 20s (600 frames)

---

## 05 - Typography & Motion Graphics (8 components)

Text animations for titles, captions, callouts, stats.

| Component | Description | Presets/Variants |
|-----------|-------------|------------------|
| **KineticText** | Words flying in from directions | `slam-in`, `cascade`, `wave`, `typewriter`, `scatter` |
| **AnimatedLowerThird** | News-style lower third | `news`, `tech`, `minimal`, `gradient` |
| **TextReveal** | Text through masking effects | `wipe-horizontal`, `wipe-vertical`, `character-by-character`, `blur-to-sharp`, `scale-from-nothing` |
| **SplitText** | Per-character animations | `bounce-in`, `spin-in`, `flip-in`, `elastic`, `wave-motion` |
| **AnimatedCallout** | Popup annotation with arrows | `tooltip`, `speech-bubble`, `badge`, `alert` |
| **GradientText** | Animated gradient shimmer | Directions: `horizontal`, `vertical`, `diagonal` |
| **NumberReveal** | Dramatic stat count-up | Scale bump + glow, comparison "FROM -> TO" mode |
| **AnimatedCaption** | CapCut-style word-by-word sync | Active word highlights with spring bounce, sliding window |

**Demo**: `TypographyDemo.tsx` - 20s (600 frames)

---

## 06 - Custom Transitions (8 transitions)

`TransitionPresentation` for `@remotion/transitions` `TransitionSeries`.

| Transition | Description | Duration | Impact |
|-----------|-------------|----------|--------|
| **Liquid Morph** | Organic fluid distortion (SVG turbulence) | 30 frames | High |
| **Cube Rotate** | 3D cube face rotation | 20 frames | Medium |
| **Circle Wipe** | Expanding circle with ripple ring | 25 frames | Medium |
| **Glitch Cut** | RGB split + slice displacement | 12 frames | Very High |
| **Zoom Through** | Camera zoom through white flash | 25 frames | High |
| **Page Flip** | 3D page turn with fold shadow | 25 frames | Medium |
| **Disintegrate** | Thanos-snap grid particle fly-away | 30 frames | Very High |
| **Morph Shape** | Expanding shape clip (circle/hex/diamond/star) | 25 frames | Medium |

**Best Pairs**: Liquid Morph (primary) + Glitch Cut (accent) = highest impact combo

---

## 07 - Audio-Reactive Visualizations (5 components)

Simulated audio-reactive effects (frame-based sine waves, no actual audio input).

| Component | Styles |
|-----------|--------|
| **WaveformVisualizer** | `bars`, `mirror`, `circular` |
| **SpectrumAnalyzer** | `gradient`, `neon`, `fire` + peak hold |
| **PulsingBackground** | `radial`, `rings`, `grid` |
| **ReactiveParticles** | Trail effects, spectrum colors |
| **BeatCounter** | `dots`, `bars`, `pulse` (BPM sync) |

---

## 08 - Scroll & Progress (6 components)

| Component | Styles |
|-----------|--------|
| **ProgressBar** | `linear`, `gradient`, `neon`, `striped` |
| **CircularProgress** | `solid`, `gradient`, `dashed` + counter |
| **StepProgress** | `dots`, `bars`, `card` (H/V layout) |
| **ScrollTimeline** | `classic`, `alternating`, `minimal` |
| **NumberTicker** | Airport departure board slot machine |
| **InfiniteScroll** | 4 directions, seamless loop, fade edges |

---

## 09 - 3D & Spatial Effects (6 components)

CSS 3D transforms only, no WebGL.

| Component | Description |
|-----------|-------------|
| **CardFlip3D** | Front/back flip with spring physics |
| **Carousel3D** | Rotating circle carousel with reflection |
| **FloatingCard** | Organic 3D tilt with multi-frequency sine |
| **PerspectiveGrid** | `floor`, `ceiling`, `tunnel` styles |
| **StackedCards** | `fan`, `deal`, `cascade`, `spread` |
| **IsometricGrid** | 2.5D blocks with staggered wave growth |

---

## 10 - Social Media & UI (6 components)

| Component | Description |
|-----------|-------------|
| **TweetCard** | Animated X post with typing + engagement counters |
| **ChatBubble** | iMessage/WhatsApp/Slack with typing indicator |
| **NotificationStack** | iOS/Android/macOS notification slide-in |
| **LikeButton** | Heart/like with particle burst (Twitter/IG/YT) |
| **SubscribeButton** | YouTube subscribe + bell + cursor animation |
| **PhoneMockup** | iPhone/Android bezel with status bar |

---

## 11 - Diagrams & Flowcharts (5 components)

| Component | Styles |
|-----------|--------|
| **AnimatedFlowchart** | `tech`, `blueprint`, `neon` |
| **SequenceDiagram** | UML with animated message passing |
| **MindMap** | `organic`, `structured`, `colorful` |
| **ArchitectureDiagram** | AWS/Azure/generic with animated data flow |
| **TimelineDiagram** | H/V with milestones + progressive fill |

---

## 12 - Cinematic Title Sequences (5 components)

| Component | Style |
|-----------|-------|
| **NetflixTitle** | Red glow, lens flare, spring overshoot |
| **MarvelTitle** | Rapid panel flashes, character build |
| **GlitchTitle** | Decode/scramble/static + RGB split |
| **TypewriterTitle** | Cream paper, ink stamps, typo correction |
| **ParticleTitle** | `dust`, `sparks`, `stars` assembly |

---

## 13 - Liquid Metal & Morphing (5 components)

| Component | Description |
|-----------|-------------|
| **MetaballField** | SVG metaballs: chrome/gold/neon/lava |
| **LiquidText** | `melt`, `solidify`, `shatter`, `ripple` |
| **MorphingShape** | Circle/star/hexagon/blob/heart morphing |
| **ChromeDroplet** | Physics-based fall, splash, ripples |
| **LavaLamp** | Convection dynamics, heat coloring, merge |

---

## 14 - Comic Book Panels (6 components)

| Component | Description |
|-----------|-------------|
| **PanelLayout** | `single`, `split-vertical/horizontal`, `grid-2x2`, `manga-3`, `action-diagonal` |
| **SpeechBubble** | `speech`, `thought`, `shout`, `whisper`, `narrator` |
| **ActionLines** | Radial/horizontal speed lines |
| **ImpactFrame** | `manga`, `western`, `pop-art` with screen shake |
| **HalftoneOverlay** | `mono`, `duotone`, `classic` CMYK |
| **MangaTransition** | `page-turn`, `panel-shatter`, `ink-wash`, `zip-reveal` |

---

## 15 - Holographic HUD / Sci-Fi (6 components)

| Component | Description |
|-----------|-------------|
| **HoloPanel** | Floating translucent panel with scan line + boot-up |
| **CircularHUD** | Rotating rings with percentage, crosshair |
| **DataStream** | Matrix rain: hex/binary/katakana/symbols |
| **WireframeObject** | Rotating cube/sphere/torus/DNA/pyramid |
| **ScannerEffect** | H/V/radial sweep with data labels |
| **HolographicText** | RGB aberration, flicker, projection beam |

---

## 16 - Generative Art (5 components)

| Component | Styles |
|-----------|--------|
| **FractalTree** | `oak`, `pine`, `cherry-blossom`, `lightning` |
| **CellularAutomaton** | `life`, `seeds`, `highlife`, `day-and-night` |
| **SacredGeometry** | Seed of Life, Flower of Life, Metatron's Cube, Sri Yantra, Golden Spiral |
| **RecursivePattern** | Sierpinski, Koch, Dragon Curve, Hilbert |
| **ParticleConstellation** | Golden angle particles with connections |

---

## 17 - Handwriting & Sketch (6 components)

| Component | Description |
|-----------|-------------|
| **HandDrawnLine** | `pen`, `pencil`, `chalk`, `marker` instruments |
| **HandDrawnShape** | rect, circle, arrow, underline, bracket, star, checkmark, cross |
| **WhiteboardText** | Character-by-character with highlights |
| **ChalkboardScene** | Full board with frame, tray, dust, eraser |
| **SketchDiagram** | `whiteboard`, `notebook`, `napkin` themes |
| **NotebookPage** | Ruled paper with blue lines, red margin |

---

## 18 - Morphing Data Narratives (6 components)

| Component | Description |
|-----------|-------------|
| **MorphChart** | Interpolate between bar/pie/line/scatter/donut/area |
| **DataParticles** | Points explode and reform ("data big bang") |
| **AnimatedAxis** | Animated scale transitions |
| **DataAnnotation** | `callout`, `spotlight`, `comparison` |
| **NumberMorph** | Odometer digits, sparkline, trend arrows |
| **StorySequence** | Director for multi-state data narratives |

---

## 19 - Isometric World Builder (5 components)

| Component | Description |
|-----------|-------------|
| **IsometricBlock** | `solid`, `glass`, `glow`, `striped` cubes |
| **IsometricGrid** | Floor grid with staggered line draw-in |
| **IsometricStack** | Vertical column (tech stack viz) |
| **IsometricConnector** | `solid`, `dashed`, `dotted`, `flow` lines |
| **IsometricScene** | 2D layout array → 3D scene with labels |

---

## 20 - Optical Illusions (6 components)

| Component | Types |
|-----------|-------|
| **MoirePattern** | `lines`, `circles`, `radial`, `grid` |
| **ImpossibleShape** | Penrose Triangle, Stairs, Cube, Blivet |
| **OpArtGrid** | `bulge`, `wave`, `vortex`, `checkerboard` |
| **HypnoticSpiral** | `archimedean`, `logarithmic`, `fibonacci` |
| **Zoetrope** | `bouncing`, `walking`, `morphing`, `rotating-cube` |
| **AnamorphicText** | Extreme CSS perspective with viewpoint sweep |

---

## 21 - Neon Signs & LED (5 components)

| Component | Description |
|-----------|-------------|
| **NeonText** | Triple-layer glow with sequential letter flicker |
| **NeonShape** | SVG shapes: border, underline, arrow, circle, star, heart, lightning |
| **LEDMatrix** | 5x7 pixel font: static/scroll/typewriter + rainbow |
| **PixelArtCanvas** | Self-drawing from 2D arrays: scanline/random/spiral/outline |
| **RetroDisplay** | Split-flap/flip-clock with 3D flip animation |

---

## 22 - Paper Craft & Origami (5 components)

| Component | Description |
|-----------|-------------|
| **PaperFold** | Fold along axis with two-sided rendering |
| **PopUpCard** | Pop-up book with staggered 3D unfolding |
| **OrigamiFold** | `crane`, `boat`, `airplane`, `box`, `heart` |
| **PaperTexture** | `white`, `craft`, `cardboard`, `watercolor`, `newspaper` |
| **CutOutAnimation** | Paper puppet theater with brass brad joints |

---

## 23 - Glitch Art & Databending (6 components)

| Component | Modes |
|-----------|-------|
| **RGBShift** | `static`, `pulse`, `shake`, `wave` |
| **ScanLineGlitch** | Burst timing, color bleed, block artifacts |
| **VHSEffect** | Scan lines, jitter, color bleeding, tracking, noise, REC |
| **PixelSort** | Sweeping sort zone with streaks |
| **DataMosh** | Frozen blocks, horizontal smear, ghost trails |
| **GlitchText** | Substitution, displacement, flicker, corruption |

---

## 24 - Particle Physics Text (6 components)

| Component | Description |
|-----------|-------------|
| **TextParticleMap** | Generates particle targets from 8x12 bitmap font |
| **ParticleRenderer** | `dot`, `glow`, `spark`, `square` + blend modes |
| **PhysicsEngine** | Euler integration: gravity, wind, attractors, noise |
| **TextFormation** | `converge`, `swirl`, `rain`, `explosion-reverse` |
| **TextDisintegration** | `dust`, `explode`, `dissolve`, `gravity`, `vortex` |
| **ParticleWave** | Sine displacement through formed text |

---

## 25a - DNA & Bioluminescence (5 components)

| Component | Description |
|-----------|-------------|
| **DNAHelix** | Rotating double helix with color-coded base pairs |
| **CellDivision** | Full mitosis: elongation, split, cleavage |
| **NeuralSynapse** | Signal propagation, neurotransmitter burst |
| **Bioluminescence** | Jellyfish with pulsing glow, tentacles |
| **ProteinFold** | `ribbon`, `spacefill`, `wireframe` rendering |

---

## 25b - Bio-Organic Simulations (5 components)

| Component | Description |
|-----------|-------------|
| **DNAHelix** | `classic`, `neon`, `monochrome` variants |
| **CellDivision** | Stage-driven with wobbly membrane |
| **NeuralSynapse** | Fractal dendrites, BFS chain-reaction |
| **Bioluminescence** | Bezier tentacles, caustic rays, depth fog |
| **MicroscopeView** | Focus rack, stain modes, reticle grid |

---

## 26 - Cosmic & Astronomy (5 components)

| Component | Description |
|-----------|-------------|
| **StarField** | Parallax stars with twinkle, diffraction spikes |
| **Nebula** | Orion/Eagle/Crab/Rosette/Pillars palettes |
| **BlackHole** | Accretion disk, Doppler shift, lensing, jets |
| **GravityLens** | SVG displacement + Einstein ring |
| **SolarSystem** | Kepler mechanics, depth sorting, orbital trails |

---

## 27 - Mathematical Beauty (5 components)

| Component | Description |
|-----------|-------------|
| **MandelbrotZoom** | Smooth coloring, exponential zoom |
| **LorenzAttractor** | RK4 integration, 3D projection |
| **FourierCircles** | Epicycles: square/sawtooth/circle targets |
| **VoronoiDiagram** | Drifting seeds + Delaunay triangulation |
| **GoldenSpiral** | Fibonacci rectangles, quarter arcs, phi |

---

## 28 - Swarm Intelligence (5 components)

| Component | Description |
|-----------|-------------|
| **Boids** | 150 agents: separation/alignment/cohesion + predator |
| **FishSchool** | Depth sizing, shimmer, caustics, bubbles |
| **AntColony** | Pheromone pathfinding with decay |
| **ParticleLife** | `symbiosis`, `predator-prey`, `ecosystem`, `chaos` |
| **EmergentText** | Swarm self-organizes to form text |

---

## 29 - Quantum & Wave Physics (5 components)

| Component | Description |
|-----------|-------------|
| **WaveInterference** | Two-source superposition with intensity map |
| **FieldLines** | EM field via Euler integration + equipotential |
| **DoubleSlit** | wave/particle/both modes + intensity distribution |
| **ProbabilityCloud** | 1s/2s/2p/3d orbitals via Monte Carlo |
| **WaveEquation** | `standing`, `traveling`, `superposition`, `beats` |

---

## 30 - Blueprint & Technical Drawing (5 components)

| Component | Description |
|-----------|-------------|
| **BlueprintBackground** | Blue paper, grid, border, title block, fold marks |
| **DimensionLine** | ISO 128: linear, angular, radius, diameter |
| **ExplodedView** | Exploded assembly with guide lines |
| **CrossSection** | Material hatching: diagonal/crosshatch/dots |
| **TechnicalCallout** | `balloon`, `leader`, `detail-view`, `section-cut` |

---

## Summary

| POC | Category | Components |
|-----|----------|-----------|
| 01 | Cinematic Camera | 5 |
| 02 | Data Visualizations | 6 |
| 03 | Particle Effects | 7 |
| 04 | Code Animations | 7 + 1 utility |
| 05 | Typography Motion | 8 |
| 06 | Custom Transitions | 8 transitions |
| 07 | Audio-Reactive | 5 |
| 08 | Scroll & Progress | 6 |
| 09 | 3D & Spatial | 6 |
| 10 | Social Media UI | 6 |
| 11 | Diagrams & Flowcharts | 5 |
| 12 | Cinematic Titles | 5 |
| 13 | Liquid Metal | 5 |
| 14 | Comic Panels | 6 |
| 15 | Holographic HUD | 6 |
| 16 | Generative Art | 5 |
| 17 | Handwriting & Sketch | 6 |
| 18 | Morphing Data | 6 |
| 19 | Isometric World | 5 |
| 20 | Optical Illusions | 6 |
| 21 | Neon & LED | 5 |
| 22 | Paper Craft | 5 |
| 23 | Glitch Art | 6 |
| 24 | Particle Text | 6 |
| 25a | DNA & Bio | 5 |
| 25b | Bio-Organic | 5 |
| 26 | Cosmic | 5 |
| 27 | Math Beauty | 5 |
| 28 | Swarm Intelligence | 5 |
| 29 | Quantum & Waves | 5 |
| 30 | Blueprint | 5 |
| **Total** | | **176 components + 8 transitions** |
