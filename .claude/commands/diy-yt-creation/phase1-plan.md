---
description: "Phase 1: Plan a new video — define scenes, durations, visuals, and component architecture"
argument-hint: <topic/concept description or brief>
---

<objective>
Execute Phase 1 of the DIY YouTube Video Creation Workflow.
Take "$ARGUMENTS" and produce a complete Remotion animation production plan.

**Goal**: Transform the content brief (from Phase 0) into a structured animation plan with scene breakdowns, visual design language, and file architecture.
**Input**: `src/<AnimationName>/research/content-brief.md` (from Phase 0: Research)
**Output**: `.agents/plans/$ARGUMENTS.plan.md`
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

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 0 (Research) is `done`.
  - If not: STOP and report "Phase 0 (Research) has not been completed. Run `/diy-yt-creation:phase0-research $ARGUMENTS` first."
- **Re-run check**: If Phase 1 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

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

### Story Lock Placement

For each scene, note where Story Locks should appear (see `.claude/references/story-locks.md`):
- **Term Branding**: Which scene introduces a coined term? (usually Scene 2–3)
- **Loop Openers**: Between which scenes? (every 60–90s for long-form, every 20–30s for Shorts)
- **Negative Frame**: Which feature/point benefits from negative framing?
- **Thought Narration**: After which major reveal? (usually post-hook or mid-video)

This is lightweight planning guidance — the actual Story Lock application happens in Phase 2 (Step 4b).

**Hook Scope Rule**: Negative Frames and Loop Openers belong in Scene 02+ (post-click retention), NOT in the hook. The hook's job is to validate the click — not shame, manipulate, or create artificial tension. Save "stop doing X wrong" for mid-video where it serves retention without wasting hook seconds.

## Step 2b: Open Loop Architecture (MANDATORY)

Every long-form video (60s+) needs an open loop architecture planned before script writing begins. This creates the curiosity backbone that keeps viewers watching.

### Primary Open Loop

Define ONE primary open loop — a question, tension, or promise raised early and resolved late:

```yaml
open_loop_architecture:
  primary_loop:
    setup_scene: "Scene 01 (Hook)"
    setup_line: "<The specific sentence that opens the loop>"
    resolution_scene: "Scene 07 (Framework)"
    resolution_line: "<The specific sentence that closes the loop>"
    type: "<question | tension | promise | mystery>"
```

### Loop Opener Placement

Plan where loop openers (attention resets) appear throughout the video:

| Video Length | Minimum Count | Suggested Placement |
|-------------|---------------|---------------------|
| < 60s | 2 | Every 20-30s |
| 60-180s | 2-3 | Every 60-90s |
| 180-420s | 3-5 | Every 60-90s |
| 420s+ | 5+ | Every 60-90s |

```yaml
  loop_openers:
    - scene: "Scene 02"
      position: "opening"
      phrase: "<e.g., 'But that is just the beginning.'>"
    - scene: "Scene 04"
      position: "transition"
      phrase: "<e.g., 'Here is where it gets interesting.'>"
```

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

### Optional: Visual Enhancement Components

Include in the plan if the video benefits from cinematic polish:

```yaml
visual_enhancements:
  light_leaks:
    - position: "hook-entrance"     # TransitionSeries.Overlay at Scene00→Scene01 cut
      seed: 3
      hueShift: 0                   # warm amber (0), cool blue (240), green (120)
      durationInFrames: 20
    - position: "cta-entrance"      # TransitionSeries.Overlay at last-scene→CTA cut
      seed: 7
      hueShift: 240                 # cool blue for emotional close
      durationInFrames: 20
  starburst:
    - scene: "Scene00Preview"       # Behind hero stat
      rays: 12
      colors: ["<primary>", "<secondary>"]
      opacity: 0.12
      rotationSpeed: 0.2
    - scene: "SceneCTA"             # Energy burst behind CTA
      rays: 24
      colors: ["#ffffff", "#ffe066"]
      opacity: 0.15
```

**Guidelines**: Use light leaks at 2–4 cut points max (less is more). Starburst backgrounds work best behind large stat displays and CTAs. Keep starburst opacity at 0.10–0.20 to avoid competing with text.

### Optional: Advanced Visual Effects

Specify in the plan if the video benefits from these advanced packages:

```yaml
advanced_effects:
  motion_blur:
    - scene: "Scene01Hook"        # Hero stat entrance
      layers: 8
      lagInFrames: 0.5
    - scene: "Scene00Preview"     # Fast preview cuts
      layers: 6
      lagInFrames: 0.4
  procedural_noise:
    - scene: "Scene03"            # Organic ambient background
      color: "<primary>"
      count: 15
      opacity: 0.12
      speed: 0.006
  animated_shapes:
    - scene: "Scene04"            # Diagram accent shapes
      shape: "circle"
      stroke: "<accent>"
      triggerFrame: "synced"
  rounded_text_boxes:
    - scene: "Shorts captions"    # TikTok-style caption boxes
      boxColor: "rgba(139,92,246,0.85)"
      fontSize: 48
  lottie_animations:
    - scene: "Scene05"            # Loading spinner, checkmark, etc.
      asset: "loading-spinner.json"
      source: "lottiefiles.com"
  gif_embeds:
    - scene: "Scene02"            # Demo GIF from product
      asset: "demo-preview.gif"
```

**When to use each**:
- **MotionBlurTrail**: Fast spring entrances, hero stat reveals, scale pops — anything that moves quickly
- **ProceduralNoise**: Replace static gradient backgrounds with organic flowing particles
- **AnimatedShape**: Draw-on SVG shapes for diagrams, accents, visual metaphors
- **RoundedTextBox**: Shorts captions, callout labels, any multi-line highlighted text
- **Lottie**: High-quality vector animations from lottiefiles.com (loading, checkmarks, icons)
- **Gif**: Embed product demo GIFs or reaction GIFs (frame-synced playback)

**Diagram & Visual Components** (from `src/shared/components/diagrams/`, uses `lucide-react` icons):
Whenever a scene needs architecture diagrams, process flows, stat displays, feature grids, or quotes, use these instead of building custom boxes. All support `mode="light"` and `mode="dark"`.

| Component | Use When | Example |
|---|---|---|
| **InfographicFlow** | Multi-stage process, how-it-works, pipeline | "How Agent Skills Work" (7-stage pastel bands) |
| **Timeline** | Chronological events, roadmap, history | "OpenClaw: Rise and Fall" (6 milestones) |
| **StatCardRow** | Big numbers, metrics, KPIs | "335K Stars, 2M Users, $5K Cost" |
| **FeatureGrid** | Feature lists, capability overview | "Platform Capabilities" (3x2 grid) |
| **ProcessCycle** | Iterative loops, feedback cycles | "AI Agent Loop" (5-step circle) |
| **QuoteCard** | Tweets, announcements, key quotes | Boris Cherny announcement card |
| **HubAndSpoke** | Central service + connected nodes | Tech stack, API ecosystem |
| **FlowDiagram** | Simple sequential pipeline (3-5 nodes) | Build > Test > Deploy |
| **LayeredArchitecture** | Stacked layers (UI > API > DB) | Software architecture |
| **ComparisonDiagram** | Before/After, side-by-side | Old vs New approach |

When planning scenes, specify the diagram component in the visual plan:
```yaml
  visual_plan:
    - scene: "Scene03"
      component: "InfographicFlow"
      mode: "light"
      stages: 5
      description: "How the token spoofing pipeline works"
    - scene: "Scene04"
      component: "StatCardRow"
      mode: "dark"
      stats: ["335K Stars", "2M Users", "$5K Cost"]
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

## Step 3c.5: Hook Variant Generation (MANDATORY)

Before the script is written, Phase 1 generates three hook variants. This ensures the strongest possible opening line is selected before committing to the full script.

### Hook Formula Selection

| Topic Type | Best Formula | Rationale |
|------------|-------------|-----------|
| New tool / product release | Stakes | Urgency + FOMO |
| Technical concept / tutorial | Counterintuitive | Contrast creates curiosity |
| Comparison / versus | Number | Benchmarks anchor credibility |
| Case study / story | Counterintuitive + narrative | Surprise flip earns investment |
| Workflow / productivity | Stakes | Pain-first, solution-second |
| AI / emerging tech | Number + Counterintuitive | Stats fight skepticism; contrarian fights hype fatigue |

### Hook Type Selection by Video Purpose

Select the hook type based on what the video IS, not what scores highest on drama:

| Video Type | Preferred Hook | Why |
|-----------|---------------|-----|
| Feature announcement / tutorial | **Direct Signal** — name the feature in sentence 1 | Audience clicked for THIS feature; validate immediately |
| Problem-solution / workflow fix | **Question or Input Bias** — open with the pain | Pain earns the right to present the solution |
| Deep dive / architecture | **Expert Secret** — "Senior engineers never..." | Positions viewer as insider |
| Comparison / benchmark | **Contrast** — "[impressive thing], but get this..." | Sets up the comparison frame |

**CRITICAL for feature videos**: Do NOT default to shame hooks ("Most developers don't know..."). Your audience already uses the tool. Lead with what they'll learn, not what they're doing wrong.

### Three Variants

Generate exactly three hook variants:

- **Variant A — Counterintuitive**: Contradicts common belief about the topic. Opens with a claim that makes the viewer say "Wait, what?"
- **Variant B — Stakes**: Quantifies cost of inaction. Opens with what the viewer stands to lose or waste by not watching.
- **Variant C — Number**: Opens with a surprising stat, benchmark, or data point that anchors credibility.

Each variant must attempt the 5-Layer Hook Stack:

| Layer | Name | Function |
|-------|------|----------|
| 1 | **Counterintuitive Claim** | Breaks the expected frame |
| 2 | **Stakes Establishment** | Why this matters NOW |
| 3 | **Number/Specificity Anchor** | Makes the abstract concrete |
| 4 | **Scroll-Stop Interjection** | The stun gun (But/However/Yet) |
| 5 | **Promise of Resolution** | Earns the right to continue |

Short-form (< 60s) needs minimum layers 1+4. Long-form (60s+) needs all five.

### Advisory Scoring Rubric

Score each variant on three dimensions (1-10 each):

| Dimension | 9-10 | 7-8 | 5-6 | 3-4 |
|-----------|------|-----|-----|-----|
| Curiosity Gap | Single sentence creates immediate, unambiguous gap | Gap present but takes 2-3 sentences | Some curiosity but could be dismissed | Informational, no gap |
| Stakes Clarity | Specific, quantified stakes | Clear but general stakes | Implied stakes, viewer must infer | Benefits mentioned but no stakes |
| Specificity | Specific stat or number in opening line | Named tools/examples within 30s | Some specificity | Generic language |

### Dimension 4 — Value Alignment (0 or 1)
Does the hook opening line directly name or preview the video's main feature/concept?
- 1: Hook names the feature, capability, or outcome within the first sentence
- 0: Hook creates curiosity through problem/pain/stat without previewing the solution

For feature announcements/tutorials, this dimension is CRITICAL — the audience clicked because they want to learn about the specific topic, not be told they're doing something wrong.

Stun Gun bonus: +2 if But/However/Yet present, +0 if absent.
Promise bonus: +1 if explicit promise of resolution, +0 if absent.

```
base = (curiosity + stakes + specificity) / 3
stun_bonus = stun_gun_score / 20    # 0.0 or 0.1 (reduced — drama shouldn't dominate)
alignment_bonus = value_alignment * 0.5  # 0.0 or 0.5
hook_score = min(10, round(base + stun_bonus + alignment_bonus + promise, 1))
```

### Plan Output Format

Include in the plan file:
```yaml
hook_variants:
  variant_a:
    type: "counterintuitive"
    opening_line: "<exact first sentence>"
    layers_present: [1, 4, 5]
    advisory_score: X.X
  variant_b:
    type: "stakes"
    opening_line: "<exact first sentence>"
    layers_present: [2, 3, 4, 5]
    advisory_score: X.X
  variant_c:
    type: "number"
    opening_line: "<exact first sentence>"
    layers_present: [3, 4, 5]
    advisory_score: X.X
  recommended: "variant_b"
```

In **interactive mode**: Present all three variants and ask the user to select one.
In **autonomous mode**: Use the variant with the highest advisory score.

## Step 3c.6: Cinematic Hook Blueprint (MANDATORY)

After selecting the hook variant, generate a **cinematic hook blueprint** that tells Phase 4 exactly how to build the hook visually. This is the key to producing film-trailer quality hooks automatically.

### Hook Pattern Selection

Choose a hook pattern based on content type and hook variant style. Reference: `src/shared/constants/hookSprings.ts` for pattern definitions.

| Pattern | Best For | Key Visual Technique |
|---------|----------|---------------------|
| **FilmTrailer** | Product launches, announcements, team reveals | Title cards → pivot → portrait/logo reveal → rapid-fire features |
| **ContrastPivot** | Comparisons, myth-busting, contrarian takes | Build context → smash cut → contrarian reveal → evidence |
| **StatCascade** | Data-driven content, benchmarks, research | Rapid stat slams with scale springs → context → deep stat |
| **RackFocusReveal** | Tool demos, screenshot-heavy intros | Blurred screenshot → snap focus → callouts appear on product |
| **TerminalHacker** | Technical/coding content, CLI tools | Typewriter terminal → shatter reveal → product behind |
| **SplitScreenDuel** | Head-to-head comparisons, X vs Y | 50/50 split → checks vs crosses → winner expands to 100% |

**Pattern Selection Rules:**
- Product/team announcement + Stakes/Counterintuitive hook → **FilmTrailer**
- Technical concept + Counterintuitive hook → **ContrastPivot** or **TerminalHacker**
- Comparison/versus + Number hook → **SplitScreenDuel** or **StatCascade**
- Tool demo + any hook → **RackFocusReveal**
- Data/benchmark + Number hook → **StatCascade**

### Visual Beats Specification

Define each visual beat with timing targets, spring type, and SFX. Spring types reference `HOOK_SPRINGS` from `src/shared/constants/hookSprings.ts`:

| Spring Preset | Feel | Use For |
|---------------|------|---------|
| `heavy` | Grounded, no bounce | Title cards, context-setting text |
| `gentle` | Soft rise | Body text, descriptions |
| `snappy` | Fast, controlled | Feature names, brand text |
| `slam` | Aggressive overshoot | Pivot words, "BUT.", stat reveals |
| `reveal` | Quick pop with settle | Brand name, logo entrance |
| `stagger` | Light bounce | Avatar pop-ins, badge reveals |

### SFX Map

Assign SFX to visual beats. Reference `HOOK_SFX` from `src/shared/constants/hookSprings.ts`:

| SFX Preset | When | Sound |
|------------|------|-------|
| `smashCut` | Context entrance, smash cut transitions | Single impact-slam (0.35) |
| `pivot` | "But" / pivot moment — TRIPLE layered | impact-slam (0.45) + screen-shake (0.35) + glitch-zap (0.28) |
| `brandReveal` | Product/brand name appears | scale-slam (0.40) |
| `featureCard` | Each feature card entrance | spring-pop (0.35) |
| `announcement` | Key announcement badges | screen-shake (0.35) |

### Music Profile

Based on the selected pattern, specify the hook music characteristics:

| Pattern | Hook BPM | Body BPM | CTA BPM | Hook Mood |
|---------|----------|----------|---------|-----------|
| FilmTrailer | 95-105 | 75-90 | 110-120 | dramatic-cinematic |
| ContrastPivot | 90-100 | 75-90 | 110-120 | dramatic-cinematic |
| StatCascade | 100-110 | 75-90 | 110-120 | hype-energetic |
| RackFocusReveal | 90-100 | 75-90 | 110-120 | tech-influencer-edgy |
| TerminalHacker | 95-105 | 75-90 | 110-120 | tech-influencer-edgy |
| SplitScreenDuel | 90-100 | 75-90 | 110-120 | dramatic-cinematic |

### Blueprint Plan Output Format

Include this in the plan file:

```yaml
cinematic_hook_blueprint:
  pattern: "<FilmTrailer | ContrastPivot | StatCascade | RackFocusReveal | TerminalHacker | SplitScreenDuel>"
  selected_variant: "<variant_a | variant_b | variant_c>"

  visual_beats:
    - beat: "Cold Open"
      timing: "0-2s"
      visual: "<description: e.g., Pure black → title card spring-in>"
      spring: "heavy"
      sfx: null
    - beat: "Context"
      timing: "2-8s"
      visual: "<description: e.g., GitHub gradient bg + sequential text springs>"
      spring: "snappy"
      sfx: "smashCut"
    - beat: "PIVOT"
      timing: "~8s"
      visual: "<description: e.g., White flash + 'BUT' 240px red + glitch + shake>"
      spring: "slam"
      sfx: "pivot"
      retention_effects: ["GlitchInterrupt", "ScreenShake"]
    - beat: "Reveal"
      timing: "8-16s"
      visual: "<description: e.g., Portrait + staggered team avatars + brand name>"
      spring: "reveal"
      sfx: "brandReveal"
      retention_effects: ["ScreenShake"]
    - beat: "Rapid-Fire"
      timing: "16-35s"
      visual: "<description: e.g., Feature cards cycling every ~100 frames>"
      spring: "slam"
      sfx: "featureCard"
    - beat: "CTA"
      timing: "35-40s"
      visual: "<description: e.g., Badges + final line fade to black>"
      spring: "gentle"
      sfx: null

  pivot_word: "<the exact word in the script that triggers the pivot, e.g., 'But'>"
  brand_reveal_word: "<the word where the brand/product name appears, e.g., 'Archon'>"

  assets_needed:
    - type: "<portrait | logo | screenshot | video>"
      description: "<what it shows>"
      source: "<URL or file path if known>"

  music_profile:
    hook_mood: "<dramatic-cinematic | tech-influencer-edgy | hype-energetic>"
    hook_bpm: [<min>, <max>]
    body_bpm: [75, 90]
    cta_bpm: [110, 120]
```

### Example: FilmTrailer Blueprint (based on ArchonOverview)

```yaml
cinematic_hook_blueprint:
  pattern: "FilmTrailer"
  selected_variant: "variant_c"

  visual_beats:
    - beat: "Cold Open"
      timing: "0-2s"
      visual: "Pure black silence → 'LAST MONTH' title card rises from below"
      spring: "heavy"
      sfx: null
    - beat: "Context"
      timing: "2-8s"
      visual: "GitHub dark gradient bg + Octocat watermark + sequential text springs: 'GITHUB LAUNCHED', 'Agentic Workflows', 'AI agents running...', 'It's a big deal' slam"
      spring: "snappy"
      sfx: "smashCut"
    - beat: "PIVOT"
      timing: "~8s"
      visual: "White flash smash cut + 'BUT.' in 240px red holds 6 frames + vignette snap"
      spring: "slam"
      sfx: "pivot"
      retention_effects: ["GlitchInterrupt", "ScreenShake"]
    - beat: "Reveal"
      timing: "8-16s"
      visual: "Cole portrait fills left half + team avatars stagger right + 'ARCHON' 100px cyan with scale spring"
      spring: "reveal"
      sfx: "brandReveal"
      retention_effects: ["ScreenShake"]
    - beat: "Rapid-Fire"
      timing: "16-35s"
      visual: "4 feature cards slam in sequentially: REPEATABLE WORKFLOWS → PARALLEL EXECUTION → SEVEN PLATFORMS → CLAUDE CODE + CODEX"
      spring: "slam"
      sfx: "featureCard"
    - beat: "CTA"
      timing: "35-40s"
      visual: "'Launching on GitHub' green badge + 'Live Stream' purple badge → 'Watch what happens.' fade"
      spring: "gentle"
      sfx: null

  pivot_word: "But"
  brand_reveal_word: "Archon"

  assets_needed:
    - type: portrait
      description: "Cole Medin headshot"
      source: "public/images/dynamous/cole-medin.webp"
    - type: video
      description: "Archon logo transparent WebM"
      source: "public/video/archon-logo-transparent.webm"
    - type: screenshot
      description: "DAG builder screenshot"
      source: "public/images/archon-overview/new-dag-builder.png"

  music_profile:
    hook_mood: "dramatic-cinematic"
    hook_bpm: [95, 105]
    body_bpm: [75, 90]
    cta_bpm: [110, 120]
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

## Step 3e: Screenshot Capture Inventory (RECOMMENDED)

If the video requires real website/app screenshots (identified in the content brief's Demo Opportunity Inventory), plan the captures here. Screenshots are captured automatically in Phase 4 via `capture-screenshots.py`.

### When to Use Real Screenshots
- **YES**: Product homepages, GitHub repos, documentation pages, dashboards, blog posts, web app UIs
- **NO**: Internal/private tools (use mockups), content behind auth walls (use recreations), abstract concepts (use AI images)

### Screenshot Inventory

For each screenshot needed, add to the plan output:

```yaml
screenshots:
  - name: github-repo-hero
    url: "https://github.com/org/repo"
    scene: scene03
    color_scheme: dark
    usage: "Product intro background"
  - name: docs-quickstart
    url: "https://docs.example.com/quickstart"
    scene: scene05
    color_scheme: dark
    usage: "Documentation walkthrough background"
    scroll_to_selector: "#getting-started"
  - name: blog-announcement
    url: "https://blog.example.com/launch"
    scene: scene02
    color_scheme: light
    full_page: false
    usage: "Blog post hero for credibility"
```

### Guidelines
- Default to `dark` color scheme for tech tools (matches video dark backgrounds)
- Use `light` only when the product's light mode is its canonical appearance
- Set `scroll_to_selector` when you need a specific section (not the top of the page)
- Set `full_page: true` only for pages where the full scroll is needed (rare)
- Add `eval_before` for pages that need interaction before capture (e.g., expanding a section)

Screenshots will be captured in Phase 4 Step 1c before building scenes.

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
**Save to**: `.agents/plans/$ARGUMENTS.plan.md`

**Report to user**:
1. Director's Summary (2-3 sentences on the vision)
2. Master Timeline table (Scene | Duration | Visual Goal | Key Elements)
3. Color palette preview
4. Component count and complexity rating (LOW/MED/HIGH)
5. Next step: Run `/diy-yt-creation/phase2-script <AnimationName>`

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `1 - Plan` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>

