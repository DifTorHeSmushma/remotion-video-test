# Scene Templates Reference

Every brand includes 20 scene templates as HTML files. These templates demonstrate the visual design for specific scene types and include Remotion porting notes.

**Location**: `public/poc-styles/brands/<brand-name>/<template>.html`

---

## Template Categories

### Title Scenes (3 templates)

#### title-hook
**Purpose**: Opening hook that grabs attention in first 3 seconds.
**Structure**: Full-screen centered text with dramatic background effects.
**Key Elements**:
- Oversized text (80-120px) with gradient or glow
- Animated background (gradient wave, particles, or neural network)
- Gradient-highlighted keyword with animated underline
- Subtitle with lighter weight beneath
- Optional "shocking stat" or number overlay

**Remotion Pattern**:
```tsx
// Phase 1: Background builds (frames 0-15)
// Phase 2: Main text slams in (frames 15-30) - use KineticText slam-in
// Phase 3: Gradient word highlights (frames 30-45) - use GradientText
// Phase 4: Subtitle fades up (frames 45-60)
```

#### title-intro
**Purpose**: Topic introduction after hook. Establishes "what this video covers."
**Structure**: Balanced layout with topic name, subtitle, and visual context.
**Key Elements**:
- Topic name in gradient text
- "In this video..." subtitle
- Category/tech badges or pill labels
- Subtle background (grid, mesh, or particles at low opacity)

#### title-question
**Purpose**: Pose a provocative question to drive curiosity.
**Structure**: Large question text centered, possibly with ? emphasis animation.
**Key Elements**:
- Question in oversized gradient text
- Animated question mark (bounce, glow, or scale)
- Dark background for focus on text
- Optional floating context elements around question

---

### Stats Scenes (3 templates)

#### stats-counter
**Purpose**: Display a single dramatic statistic with count-up animation.
**Structure**: Centered giant number with label and optional comparison.
**Key Elements**:
- Giant number (120-180px) with `AnimatedCounter`
- Label text below (24-36px)
- Optional delta indicator (+/- change)
- Background glow or particle burst on completion
- Threshold color changes (green at goal)

**Remotion Pattern**:
```tsx
// Use AnimatedCounter with format="percentage" or "number"
// Add NumberReveal for scale bump + glow on completion
// Background: GradientMesh at 20% opacity
// Optional: ParticleField confetti burst at counter completion
```

#### stats-comparison
**Purpose**: Compare two or more metrics side by side.
**Structure**: Two-column or row layout with competing numbers.
**Key Elements**:
- Two large numbers with labels
- VS badge or separator between them
- Winner highlight (glow, scale, or color)
- Animated bars showing relative magnitude
- Sequential reveal (left first, then right)

#### stats-growth
**Purpose**: Show trend/growth over time with before/after.
**Structure**: Number with upward arrow, optional sparkline/graph.
**Key Elements**:
- Before value (small, dimmed, strikethrough)
- After value (large, bright, glowing)
- Arrow indicator between them
- Mini chart or progress bar
- Percentage change badge

---

### Code Scenes (3 templates)

#### code-terminal
**Purpose**: Show command execution in a terminal.
**Structure**: macOS-style terminal window with typing animation.
**Key Elements**:
- Terminal chrome (red/yellow/green dots, title bar)
- Command prompt ($ or >) with blinking cursor
- Command types out character by character
- Output appears line by line with delays
- Optional colored output (green success, red error)
- Loading spinner or progress bar

**Remotion Pattern**:
```tsx
// Use TerminalEmulator component
// Configure commands array with output and delays
// Add syntaxHighlight for colored output
// Background: dark (brand background color)
```

#### code-diff
**Purpose**: Show code changes (before/after).
**Structure**: Unified diff or side-by-side with red/green highlighting.
**Key Elements**:
- File header with path
- Red lines (removed) slide out left
- Green lines (added) slide in from right
- Line number column
- +/- markers with animation

**Remotion Pattern**: Use `AnimatedDiff` component with unified or side-by-side mode.

#### code-typing
**Purpose**: Live code writing demonstration.
**Structure**: Code editor with syntax highlighting and line numbers.
**Key Elements**:
- Editor chrome (tab, file name)
- Character-by-character typing with variable speed
- Syntax highlighting applies in real-time
- Line highlighting for focus areas
- Optional cursor blink

**Remotion Pattern**: Use `TypewriterCode` with `syntaxHighlight.ts` utility.

---

### List Scenes (3 templates)

#### list-features
**Purpose**: Showcase product features or capabilities.
**Structure**: Feature items with icons, staggered entrance.
**Key Elements**:
- Feature items with icon + title + description
- Staggered slide-in from left or right
- Icon containers with brand accent background
- Optional check marks or numbered badges
- Hover-like glow on active item

#### list-steps
**Purpose**: Step-by-step process or workflow.
**Structure**: Numbered steps with connecting lines.
**Key Elements**:
- Numbered circles with brand accent
- Step title + description
- Connecting lines or arrows between steps
- Sequential reveal (each step appears after previous)
- Active step highlight

**Remotion Pattern**: Use `StepProgress` for step indicators + sequential reveal with `interpolate` stagger.

#### list-benefits
**Purpose**: Highlight key benefits or advantages.
**Structure**: Benefit cards or list items with emphasis.
**Key Elements**:
- Benefit items with accent-colored bullet/icon
- Short, punchy text (3-5 words per benefit)
- Staggered entrance with spring physics
- Optional gradient highlight on key words

---

### Compare Scenes (2 templates)

#### compare-before-after
**Purpose**: Show transformation or improvement.
**Structure**: Two panels - "Before" (dimmed, red-tinted) and "After" (bright, green-tinted).
**Key Elements**:
- Split screen or sequential reveal
- "Before" label with red/warning styling
- "After" label with green/success styling
- Arrow or transition between states
- Clear visual contrast

#### compare-side-by-side
**Purpose**: Feature-by-feature comparison of two options.
**Structure**: Two columns with comparison rows.
**Key Elements**:
- Column headers (Option A vs Option B)
- VS badge in center
- Feature rows with check/cross indicators
- Winner highlighting
- `ComparisonTable` component recommended

---

### CTA Scenes (2 templates)

#### cta-subscribe
**Purpose**: YouTube subscribe call-to-action.
**Structure**: Subscribe button with bell icon and count.
**Key Elements**:
- YouTube-style subscribe button
- Bell icon animation
- Subscriber count increment
- Cursor animation clicking subscribe
- "Hit subscribe" text prompt
- `SubscribeButton` component

#### cta-download
**Purpose**: Download or action call-to-action.
**Structure**: Large button with download icon and supporting text.
**Key Elements**:
- Prominent download button with gradient
- File/tool name and version
- Supporting benefit text
- Arrow or pointer guiding attention
- Pulsing glow on button

---

### Outro (1 template)

#### outro-summary
**Purpose**: Closing summary of key points.
**Structure**: Key takeaways listed with brand styling.
**Key Elements**:
- "Key Takeaways" or "Summary" header
- 3-5 bullet points of main points
- Brand logo/watermark
- "Thanks for watching" text
- Social links or next video suggestion

---

### Transitions (3 templates)

#### transition-fade
**Purpose**: Smooth crossfade between scenes.
**Implementation**: Opacity interpolation over 15-30 frames.

#### transition-slide
**Purpose**: Directional slide between scenes.
**Implementation**: TranslateX/Y with ease timing over 20-30 frames.

#### transition-zoom
**Purpose**: Zoom-through effect for emphasis.
**Implementation**: Scale from 1.0 to 2.0 (outgoing) while incoming scales 0.5 to 1.0.

---

## Template File Pattern

Every brand has the same 20 template files:
```
brands/<brand-name>/
├── _style-guide.html      # Full style guide reference
├── title-hook.html
├── title-intro.html
├── title-question.html
├── stats-counter.html
├── stats-comparison.html
├── stats-growth.html
├── code-terminal.html
├── code-diff.html
├── code-typing.html
├── list-features.html
├── list-steps.html
├── list-benefits.html
├── compare-before-after.html
├── compare-side-by-side.html
├── cta-subscribe.html
├── cta-download.html
├── outro-summary.html
├── transition-fade.html
├── transition-slide.html
└── transition-zoom.html
```

## Scene-to-Brand Combinations

Best brand choices per scene type:

| Scene Type | Top Brands | Why |
|---|---|---|
| Stats/Counters | modern-gradient, fintech, cyberpunk-neon | Strong number presentation |
| Code/Terminal | cyberpunk-neon, ai-neural, retro-tech | Developer aesthetic |
| Comparisons | clean-corporate, saas-dashboard, modern-gradient | Clear hierarchy |
| Architecture | ai-neural, enterprise-dark, scifi-space | Technical depth |
| CTAs | modern-gradient, playful-colorful, tech-startup | Energy + action |
| Tutorials | nature-organic, clean-corporate, minimalist-dark | Approachable + clear |
| Lists/Features | corporate-modern, saas-dashboard, tech-startup | Structured info |
| Cinematic Titles | cyberpunk-neon, scifi-space, luxury-premium | Maximum drama |
