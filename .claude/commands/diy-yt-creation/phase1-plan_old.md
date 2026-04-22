---
description: "Phase 1: Plan a new video — define scenes, durations, visuals, and component architecture"
argument-hint: <topic/concept description or brief>
---

<objective>
Execute Phase 1 of the DIY YouTube Video Creation Workflow.
Take "$ARGUMENTS" and produce a complete Remotion animation production plan.

**Goal**: Transform the content brief (from Phase 0) into a structured animation plan with scene breakdowns, visual design language, and file architecture.
**Input**: `src/<AnimationName>/research/content-brief.md` (from Phase 0: Research)
**Output**: `.agents/plans/<topic>-explainer.plan.md`
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 1)
</objective>

<autonomous-mode>
## When Called from full-auto-v2

If this phase is invoked as part of the full-auto-v2 orchestration, parameters will be passed in context.
**DO NOT ask questions** — use the provided values:

- **Duration**: Use PARAMS.duration (default: 60s)
- **Tone**: Use PARAMS.tone (default: tech-influencer-edgy)
- **Resolution**: Use PARAMS.resolution (default: 1920x1080)

Proceed autonomously through all steps.
</autonomous-mode>

<process>

## Step 1: Read Research & Gather Requirements

First, read the content brief from Phase 0:
- `src/$ARGUMENTS/research/content-brief.md`

Extract: value proposition, pain points, key features, messaging hierarchy, and suggested narrative arc.

**Interactive mode** (standalone execution) — Ask the user (one question at a time, prefer multiple choice):
1. **Video duration**: How long? (45s / 60s / 90s / 3min)
2. **Tone**: What feel? (professional-corporate / tech-influencer-edgy / friendly-educational / dramatic-cinematic)
3. **Resolution**: Output size? (1280x720 / 1920x1080)

**Autonomous mode** (from full-auto-v2) — Use context values, do not ask.

Note: Target audience and key angle are already defined in the content brief.

## Step 2: Scene Architecture

Based on duration, determine scene count and average length:
- 45s → 5-6 scenes, 8-10s each
- 60s → 6-7 scenes, 9-10s each
- 90s → 7-8 scenes, 11-13s each
- 3min → 8-10 scenes, 15-22s each

Structure the narrative arc using the **Kallaway Formula**:
1. **Hook — Context Lean-In** (10-15% of duration) — establish topic clarity, create common ground via mind-blowing fact or shared pain point. Viewer must "self-select" within 4 seconds.
2. **Scroll-Stop Interjection** (integrated into Hook/Solution) — use "But," "However," or "Yet" to halt momentum and create the stun gun effect
3. **Contrarian Snapback** — reveal unexpected path, the "Uno Reverse" that snaps viewers onto a new trajectory
4. **Solution** (15-20%) — introduce the product/concept with benefit-first framing
5. **Deep Dive** (40-50%) — 3-5 feature scenes, each BENEFIT-LED not feature-led
6. **Social Proof / Security** (10-15%) — trust signals, cult hopping references
7. **CTA** (10%) — call to action, closing

### The Explosion Timer
- **Short-form (< 60s)**: Must deliver unique value before 4-second mark
- **YouTube (60s+)**: Must deliver value hit within first 1-2 minutes
- Front-load the "Value Loop" — give immediate payoff to earn the right to continue

## Step 3: Visual Design Language

### Theme Selection

Choose a base theme from `src/shared/themes/` or specify custom colors:
- **dark-tech** (default) — Dark backgrounds (#0D1117), cyan/purple accents. Best for: technical explainers, coding tutorials.
- **corporate** — Professional slate tones, blue primary. Best for: business presentations, B2B content.
- **vibrant** — High contrast, electric cyan/purple/coral. Best for: attention-grabbing, social media.
- **educational** — Warm, friendly, higher contrast. Best for: tutorials, courses, educational content.
- **custom** — Specify primary/secondary/accent colors to override base theme.

Define for the plan:
- **Base theme**: `dark-tech` | `corporate` | `vibrant` | `educational` | `custom`
- **Color overrides** (if customizing): Primary, secondary, accent hex values
- **Extended colors** (optional): Composition-specific colors (e.g., brand colors, component-specific)
- **Typography**: Heading font + mono/code font (from @remotion/google-fonts, default: Inter + JetBrains Mono)
- **Motion style**: Spring emphasis (`snappy` = responsive, `smooth` = flowing, `bouncy` = playful)
- **Background**: Gradient direction, particle effects, scene transitions

### Multi-Sensory Hook Design

Visual hooks are 100x more powerful than spoken words. Plan lockstep between script and screen:

**Text-on-Screen Protocol (3-5 Word Rule)**:
- Distill hook context into max 5 words displayed on screen
- Use bold, high-contrast fonts
- Text should accelerate "lean-in" before audio registers
- Example: Instead of narrating "life-size floor plans," display "Future of Home Design"

**Motion & The "Deer" Effect**:
- Plan strategic motion to trigger biological "stop and stare" reflex
- Balance: Too much overwhelms, too little bores
- Consider rapid transitions (POV-to-mirror, zoom-snap) for hook scenes
- Reserve aggressive motion for the first 4 seconds

**Visual Hook Matrix for Each Scene**:
| Scene | On-Screen Text (3-5 words) | Motion Type | Visual Trust Signal |
|-------|---------------------------|-------------|---------------------|
| Hook  | <distilled hook>          | Rapid/Attention | Dark, professional |
| Solution | <product name>         | Smooth reveal | Brand colors |
| Features | <benefit word>         | Deliberate | Icons/diagrams |
| CTA   | <action verb>             | Urgent pulse | Clear focal point |

## Step 3b: Transition & SFX Selection (MANDATORY)

Every video uses exactly **2 scene transitions** for visual consistency:
- **Primary**: Used for most scene changes (~80%)
- **Accent**: Used for hook entrance, CTA, key reveals (~20%)

### Transition Selection Process

Based on the **tone** and **topic**, select transitions from `src/shared/transitions/presets.ts`:

#### Available Scene Transitions
| ID | Name | Best For |
|----|------|----------|
| wipe-left | Wipe Left | technical, professional, tutorials |
| wipe-right | Wipe Right | technical, professional, flowing-content |
| wipe-diagonal | Wipe Diagonal | energetic, action, dramatic |
| slide-up | Slide Up | building, progression, technical-deep-dive |
| cross-dissolve | Cross Dissolve | conceptual, philosophical, smooth |
| zoom-through | Zoom Through | deep-dive, focus, technical-details |
| circle-reveal | Circle Reveal | reveals, surprises, features |
| split-horizontal | Split Horizontal | comparisons, before-after |

#### Available Intro/Outro Transitions (for hooks and CTAs)
| ID | Name | Best For |
|----|------|----------|
| burst-in | Burst In | hooks, intros, attention-grab |
| impact-slam | Impact Slam | cta, conclusions, emphasis |
| explode-in | Explode In | dramatic reveals, important-points |
| glitch-in | Glitch In | tech, digital, modern, coding |
| shatter-out | Shatter Out | exits, endings, dramatic-close |

#### Recommended Pairings by Content Type

| Content Type | Primary | Accent |
|--------------|---------|--------|
| Technical/Coding | wipe-left | slide-up or glitch-in |
| Tutorial | wipe-right | cross-dissolve |
| Professional/Business | cross-dissolve | wipe-right |
| Energetic/Action | wipe-diagonal | burst-in or impact-slam |
| Educational/Explainer | slide-up | zoom-through |

### Plan Format

Include in the plan file:

```yaml
transitions:
  primary:
    id: <transition-id>
    usage: "Most scene transitions"
  accent:
    id: <transition-id>
    usage: "Hook entrance, CTA, key reveals"
  reasoning: "<1 sentence why these match the content>"
```

**Example for a Claude Code release video:**
```yaml
transitions:
  primary:
    id: wipe-left
    usage: "Clean scene changes for technical content"
  accent:
    id: glitch-in
    usage: "Digital feel for coding/AI topic, used at hook and CTA"
  reasoning: "Technical content with modern coding feel benefits from clean wipes + digital glitch accent"
```

## Step 3c: Preview Hook Strategy (MANDATORY)

Every video MUST include a preview hook scene (Scene00Preview) that:
- Runs 10-15 seconds (300-450 frames at 30fps)
- Shows 4-6 quick clips/teasers from upcoming content
- Changes visuals every 10-15 frames (0.3-0.5 seconds)
- Creates "open loops" that demand resolution

Research shows:
- 50-60% of viewers drop off in the first 3 seconds
- Preview hooks create "open loops" → +32% watch time
- Pattern interrupts → +23% retention rate

### Preview Hook Template

| Phase | Frames | Duration | Content |
|-------|--------|----------|---------|
| Attention Grab | 0-30 | 1s | Bold stat or shocking statement |
| Teaser 1 | 30-90 | 2s | Quick clip from Scene 03-04 |
| Teaser 2 | 90-150 | 2s | Quick clip from Scene 05-06 |
| Teaser 3 | 150-210 | 2s | Quick clip from final feature |
| Promise | 210-300 | 3s | "In this video..." value proposition |

### Preview Types (Choose Based on Content)

1. **Montage Preview** — Quick cuts of upcoming visual moments
   - Best for: Feature-rich products, transformations, demos
   - Visuals: Rapid scene cuts, each lasting 1-2 seconds

2. **Stats Cascade** — Rapid-fire statistics that will be explained
   - Best for: Data-driven content, comparisons, research results
   - Visuals: Large numbers animate in sequence with glowing effects

3. **Before/After Tease** — Show transformation without explanation
   - Best for: Tutorials, productivity tools, improvements
   - Visuals: Split screen or sequential reveal

4. **Question Barrage** — "What if... But how... And why..."
   - Best for: Educational content, problem-solution narratives
   - Visuals: Text questions fly in, creating curiosity gaps

### Preview Hook Plan Format

Include this in the plan file:
```markdown
### Scene 00 Preview (MANDATORY)
- **Type**: <Montage/Stats/Before-After/Question>
- **Duration**: <10-15>s (<300-450> frames)
- **Phases**:
  1. [0-30f] Attention Grab: <bold statement or stat>
  2. [30-90f] Teaser 1: <preview of Scene X content>
  3. [90-150f] Teaser 2: <preview of Scene Y content>
  4. [150-210f] Teaser 3: <preview of Scene Z content>
  5. [210-300f] Promise: "In this video, <value proposition>"
- **"Upcoming" Badge**: Top-left corner, fades out before final CTA
```

## Step 3d: AI Image Prompts (OPTIONAL)

If the video requires custom AI-generated images (not text/diagrams/code), define prompts for each scene that needs one.

### When to Use AI Images
- **YES**: Hero shots, abstract backgrounds, conceptual visualizations
- **NO**: Text layouts, code demos, architecture diagrams, UI mockups

### Image Prompt Planning

For each scene requiring a generated image:
```yaml
images:
  - scene: hook
    name: scene01-hero
    prompt: "[Detailed description with style, lighting, composition]"
    aspect_ratio: "16:9"  # or "9:16" for Shorts
    usage: "Background image for hook scene"
```

### Prompt Guidelines

1. **Be Specific**: Include lighting, style, mood, and technical details
2. **Match Video Theme**: Use consistent visual language
3. **Dark Backgrounds**: Work best with text overlays
4. **Avoid Text in Images**: Imagen doesn't reliably render text

### Template
```
[Subject]. [Style/mood]. [Lighting details].
Dark environment with [primary color] and [accent color] accents.
[Quality modifiers: Ultra-detailed, cinematic, 8K, etc.]
```

### Example for Tech Video
```yaml
images:
  - scene: hook
    name: scene01-hero
    prompt: "Dramatic explosion of glowing neural network nodes connected by electric blue data streams. Deep space black background with purple nebula hints. Cinematic volumetric lighting, hyper-detailed, 8K quality."
    aspect_ratio: "16:9"
    usage: "Attention-grabbing hook background"
```

Generated images will be created in Phase 4 before building scenes.

## Step 4: Component Inventory

List reusable components needed:
- Scene wrapper (background + gradient)
- Text elements (headings, body, code blocks)
- Visual elements (terminal windows, diagrams, icons, avatars)
- Animation elements (particles, flow arrows, glowing badges)

### remotion-bits Component Selection

Evaluate whether `remotion-bits` wrappers can replace manual animation code. Always prefer wrappers for supported use cases:

| Visual Need | remotion-bits Option | When to Prefer |
|---|---|---|
| Text entrance | `SyncedAnimatedText` (character/word/line split) | Titles, stats, labels — saves 20+ lines vs manual interpolate |
| Code/terminal | `SyncedCodeBlock` (syntax highlight + line stagger) | Code demos, CLI output |
| Feature lists | `SyncedStaggeredMotion` (auto-staggered children) | Bullet lists, feature grids |
| Typing effect | `TypeWriter` (direct import OK, no sync needed) | Preview hooks, CTAs |
| Stat counters | `AnimatedCounter` (direct import OK) | Number reveals |
| Background particles | `SyncedParticles` | Scene backgrounds |
| Gradient backgrounds | `GradientTransition` (direct import OK) | Scene backgrounds |

Add `remotion_bits_components_used: [list]` to the plan output when using any of these.

### CRITICAL: Layout Rules to Prevent Overlapping Elements

**Screen Zone Allocation:**
For 1920x1080, define clear zones that elements can occupy:
```
┌──────────────────────────────────────────────────────┐
│ TOP ZONE (y: 0-200)                                  │
│ - Titles, scene labels, badges                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│ MAIN CONTENT ZONE (y: 200-900)                       │
│ - Primary visuals, diagrams, terminals              │
│ - Split: Left (x: 0-960) | Right (x: 960-1920)      │
│                                                      │
├──────────────────────────────────────────────────────┤
│ BOTTOM ZONE (y: 900-1080)                            │
│ - Captions, callouts, progress indicators            │
└──────────────────────────────────────────────────────┘
```

**Phase-Based Content Strategy:**
When a scene has multiple content sections that would compete for space:
1. Divide scene duration into phases
2. Each phase gets exclusive use of the main content zone
3. Only the current phase's elements are visible
4. Transitions between phases use fade/slide animations

Example scene breakdown:
```
Scene 05 (25 seconds / 750 frames):
├── Phase 1 (frame 0-250): Terminal demo
├── Phase 2 (frame 250-500): Code comparison
└── Phase 3 (frame 500-750): Feature summary
```

### Architecture Diagrams: Box + Arrow Layout Planning

When a scene includes connected elements (flowcharts, architecture diagrams, data flow):

**1. Define Grid Layout in Plan:**
```
Scene 03 Architecture - Grid Layout:
┌─────────────────────────────────────────────────────────┐
│  ┌─────────┐           ┌─────────┐           ┌────────┐ │
│  │Platform │──────────▶│Orchestr.│──────────▶│Database│ │
│  │Adapters │           │         │           │        │ │
│  └─────────┘           └────┬────┘           └────────┘ │
│       ▲                     │                           │
│       │                     ▼                           │
│  ┌─────────┐           ┌─────────┐                      │
│  │ Slack   │           │Workflow │                      │
│  │ GitHub  │           │ Engine  │                      │
│  └─────────┘           └─────────┘                      │
└─────────────────────────────────────────────────────────┘
```

**2. Specify Box Positions (absolute coordinates):**
```markdown
| Box ID      | Position (x, y) | Size (w × h) | Animation Start |
|-------------|-----------------|--------------|-----------------|
| platforms   | (100, 250)      | 280 × 100    | frame 0         |
| orchestrator| (520, 350)      | 280 × 100    | frame 30        |
| database    | (940, 250)      | 280 × 100    | frame 60        |
| workflow    | (520, 550)      | 280 × 100    | frame 90        |
```

**3. Specify Connections:**
```markdown
| From → To              | Path Type    | Animation After |
|------------------------|--------------|-----------------|
| platforms → orchestrator | horizontal  | frame 20        |
| orchestrator → database  | horizontal  | frame 50        |
| orchestrator → workflow  | vertical    | frame 80        |
```

**4. Animation Sequence (layered):**
- Frame 0-30: Background + grid lines fade in
- Frame 30-60: First box animates in
- Frame 60-90: First arrow draws, second box animates in
- Continue pattern: Arrow → Box → Arrow → Box

**5. Z-Index Layering:**
```
Layer 0 (bottom): Background gradient, grid lines
Layer 1: Arrows/connections (render first)
Layer 2: Box shadows
Layer 3: Boxes (render last, on top of arrows)
Layer 4: Labels/badges
```

## Step 5: File Structure

Plan the file layout per project conventions:
```
src/<AnimationName>/
├── Composition.tsx
├── constants/ (colors.ts, fonts.ts, springs.ts, timing.ts)
├── components/ (reusable visual elements)
└── scenes/ (Scene01*.tsx through SceneNN*.tsx)
```

## Step 6: Use Remotion Best Practices

**MANDATORY**: Invoke the `remotion-best-practices` skill using the Skill tool (`skill: "remotion-best-practices"`) to inform animation patterns and constraints. Do NOT skip this step. Apply its guidance to the plan's motion design and component architecture.

If the skill fails, fall back to these manual rules and note the failure in the report:
- Use `spring()` for organic motion, `interpolate()` for linear
- Keep springs deterministic (pass `fps` explicitly)
- Use `extrapolateLeft/Right: 'clamp'` on all interpolations
- Plan for `TransitionSeries` orchestration with transition types per scene

</process>

<output>
**Save to**: `.agents/plans/<kebab-case-topic>-explainer.plan.md`

**Report to user**:
1. Director's Summary (2-3 sentences on the vision)
2. Master Timeline table (Scene | Duration | Visual Goal | Key Elements)
3. Color palette preview
4. Component count and complexity rating (LOW/MED/HIGH)
5. Next step: Run `/diy-yt-creation/phase2-script <AnimationName>`
</output>
