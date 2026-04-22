---
name: poc-visual-library
description: Comprehensive visual style, theme, and component reference library for video production. Contains 19 brand style guides, 30 POC component categories (176+ components), 8 custom transitions, scene template patterns, and animation techniques. Use when planning visual design for new videos, selecting brand styles, choosing POC components for scenes, or getting implementation ideas for Remotion animations. Triggers on requests like "what style should I use", "which components fit this scene", "visual ideas for...", "how to animate...", "brand style reference", or any visual design decision during video creation.
---

# POC Visual Library

The definitive reference for all visual styles, brand themes, animation components, and scene templates available in the diy-yt-creator platform. This skill provides everything needed to make visual design decisions for video production.

## When to Use This Skill

- **Brand Selection**: Choosing a visual style/theme for a new video
- **Scene Design**: Deciding which POC components fit a specific scene type
- **Animation Ideas**: Finding the right animation technique for content
- **Style Reference**: Getting exact colors, fonts, gradients, and effects for a brand
- **Template Selection**: Picking the right scene template pattern
- **Visual Planning**: Phase 1 and Phase 4 visual design decisions
- **Component Discovery**: Finding reusable components across 30 POC categories

## Quick Start: Brand Selection Guide

Choose a brand based on content type and audience:

| Content Type | Recommended Brand | Why |
|---|---|---|
| AI/ML Tutorials | **ai-neural** | Neural network visuals, data flow effects, computational feel |
| Developer Tools | **cyberpunk-neon** | Hacker aesthetic, terminal vibes, high-energy |
| SaaS/Product | **modern-gradient** | Instagram/Stripe-inspired, gradient-rich, trendy |
| Enterprise/B2B | **corporate-modern** or **clean-corporate** | Professional, trustworthy, structured |
| Startup/Launch | **tech-startup** | Energetic, bold, forward-looking |
| Finance/Crypto | **fintech** | Data-focused, precision, trust indicators |
| Science/Education | **nature-organic** | Approachable, warm, educational |
| Gaming/Creative | **vaporwave** | Retro-futuristic, nostalgic, eye-catching |
| Security/Hacking | **cyberpunk-neon** | Dark, dangerous, electric |
| Luxury/Premium | **luxury-premium** | Elegant, gold accents, refined |
| High-Accessibility | **high-contrast** | Maximum readability, bold contrasts |
| Space/Future | **scifi-space** | Cosmic, expansive, wonder-inspiring |
| Data/Analytics | **saas-dashboard** | Dashboard-native, metric-focused |
| Retro/Nostalgia | **retro-tech** | Vintage computing, warm CRT feel |
| Bold/Statement | **brutalist** | Raw, impactful, unapologetic |
| Playful/Fun | **playful-colorful** | Vibrant, energetic, friendly |
| Dark/Minimal | **minimalist-dark** | Clean, focused, content-first |
| Dark Enterprise | **enterprise-dark** | Serious, powerful, data-heavy |
| Dynamous Brand | **dynamous** | Brand-specific style for Dynamous content |

## Reference Files

Detailed information is organized into reference files:

- [references/brand-catalog.md](references/brand-catalog.md) - All 19 brand style guides with colors, fonts, effects, and usage
- [references/component-catalog.md](references/component-catalog.md) - All 30 POC categories with 176+ components
- [references/scene-templates.md](references/scene-templates.md) - 20 scene template types with implementation patterns
- [references/animation-patterns.md](references/animation-patterns.md) - Animation techniques, transitions, and timing
- [references/design-system.md](references/design-system.md) - Shared design principles, performance guidelines, and integration

## Scene-to-Component Quick Map

When building a specific scene type, use these components:

### Hook / Title Scenes
- `KineticText` (slam-in, cascade, wave presets) for dramatic text entrance
- `GradientText` for shimmer on key phrases
- `NetflixTitle` / `GlitchTitle` / `ParticleTitle` for cinematic intros
- `ZoomReveal` for Netflix-style fly-in
- `GlitchEffect` overlay for energy

### Stats / Numbers Scenes
- `AnimatedCounter` for counting up big numbers
- `NumberReveal` for dramatic stat reveals with glow pulse
- `AnimatedBarChart` for comparative data
- `AnimatedPieChart` for distribution data
- `NumberMorph` for odometer-style rolling digits

### Code / Technical Scenes
- `TypewriterCode` for realistic code typing
- `TerminalEmulator` for macOS terminal chrome
- `AnimatedDiff` for git diff visualization
- `CodeHighlight` for spotlight walkthroughs
- `BrowserMockup` for web page demonstrations
- `APIFlow` for client-server request/response

### Comparison Scenes
- `ComparisonTable` with animated check/cross icons
- `AnimatedBarChart` in comparison mode
- Side-by-side layout with phase-based reveal

### List / Features Scenes
- `StepProgress` for step-by-step flows
- `ScrollTimeline` for timeline reveals
- `AnimatedCallout` for annotation boxes
- `AnimatedLowerThird` for labels

### Architecture / Diagram Scenes
- `AnimatedFlowchart` for process flows
- `ArchitectureDiagram` for system architecture
- `SequenceDiagram` for UML sequence diagrams
- `MindMap` for branching concepts
- `NetworkGraph` for node-and-edge graphs
- `IsometricScene` for 2.5D tech stack visuals

### Background Atmosphere (layerable)
- `ParticleField` (floating-dots at 40% opacity)
- `GradientMesh` (nebula at 30% opacity)
- `AnimatedGrid` (perspective grid)
- `WaveBackground` for layered waves
- `StarField` for cosmic themes

### Transitions Between Scenes
- **Primary (most cuts)**: Liquid Morph, Circle Wipe, Zoom Through
- **Accent (key reveals)**: Glitch Cut, Disintegrate
- **Elegant**: Page Flip, Cube Rotate
- **Shape-based**: Morph Shape (circle, hexagon, diamond, star)

### Social Media / UI Scenes
- `TweetCard` for animated X/Twitter posts
- `ChatBubble` for messaging UIs
- `PhoneMockup` for mobile demos
- `SubscribeButton` for YouTube CTAs
- `NotificationStack` for notification UIs

### Cinematic Title Sequences
- `NetflixTitle` - dramatic zoom with red glow
- `MarvelTitle` - rapid panel flashes
- `GlitchTitle` - cyberpunk decode/scramble
- `TypewriterTitle` - vintage typewriter
- `ParticleTitle` - particles assembling into text

## Component Integration Priority

Ranked by immediate impact on video quality:

### Tier 1 - High Impact, Low Effort (use first)
1. **AnimatedCounter** - Every tech video has stats
2. **TypewriterCode** - Instantly improves code scenes
3. **TerminalEmulator** - macOS terminal chrome
4. **KineticText** - Drop-in title replacement
5. **GradientText** - Shimmer on key phrases

### Tier 2 - High Impact, Medium Effort
6. **AnimatedBarChart** - Framework comparisons
7. **ComparisonTable** - Tool A vs Tool B
8. **KenBurnsImage** - Cinematic B-roll
9. **GlitchEffect** - Energy for transitions
10. **AnimatedCaption** - CapCut-style word sync

### Tier 3 - Medium Impact, Unique Value
11. **AnimatedDiff** - Git diff visualization
12. **APIFlow** - Architecture scenes
13. **NetworkGraph** - Self-building diagrams
14. **ZoomReveal** - Dramatic reveals
15. **ParticleField** - Background atmosphere

### Tier 4 - Transitions (batch integrate)
16. All 8 custom transitions - Liquid Morph + Glitch Cut highest impact pair
