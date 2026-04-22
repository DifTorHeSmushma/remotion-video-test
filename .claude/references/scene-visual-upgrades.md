---
name: Scene Visual Upgrade Patterns (Glass Morphism + Spring Animations)
description: Proven visual patterns from ArchonOverview — glass cards, SVG diagrams, word highlighting, platform icons, parallax screenshots
type: feedback
---

## Glass Morphism Card Style (use everywhere)
```tsx
background: 'rgba(30,41,59,0.6)',
backdropFilter: 'blur(12px)',
border: '1px solid rgba(255,255,255,0.08)',
borderRadius: 14,
boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
```
Active/highlighted variant: add colored border + glow (`boxShadow: 0 0 40px ${color}44`).

## Word-by-Word Highlighting (for narration text > 10 words)
Extract timestamps from sync JSON, render as `<span>` array:
- Inactive: `COLORS.secondaryText`, fontWeight 400
- Active: `COLORS.primaryText`, fontWeight 600
- Accent words (tool names, key terms): specific accent color + fontWeight 800 + textShadow glow

## SVG Fan-Out Diagrams
- Use gradient `<linearGradient>` per line (hub color → node color)
- Line draw animation: interpolate endpoint position over 20 frames
- Shorten lines from hub/node edges (HUB_MARGIN=44, CARD_MARGIN=50) to avoid bleeding through
- Glow filter: `<feGaussianBlur stdDeviation="3">` on lines
- strokeWidth: 4px minimum for YouTube visibility

## Platform Icons (inline SVG)
Use inline SVG paths for recognizable platforms (GitHub Octocat, Slack hash, Telegram plane, Discord mark). Safer than emoji in headless Chromium. Each icon 40px with accent color fill.

## Browser Chrome Simulator (standardized)
- Width: 94%, centered with `alignSelf: 'center'`
- Title bar: height 36px, dark bg, 3 colored dots (12px)
- `objectFit: 'contain'`, NO maxHeight constraints
- Screenshots/videos display at their natural aspect ratio

## "OBSOLETE" / Status Badge Pattern
- Glass card with gradient border + accent color glow
- Spring scale entrance with ScreenShake + scale-slam SFX
- Trigger at the exact word timestamp when status is spoken
- Red for negative (OBSOLETE), green for positive (LAUNCHING), purple for events (LIVE STREAM)

## Comparison Tables (Grid Layout)
- CSS Grid with fixed column widths (`gridTemplateColumns: '240px 1fr 1fr 1fr 1fr'`)
- Archon column highlighted with gradient bg + glow border
- Green checkmarks / red X marks at 26px
- Glass morphism per row

**Why:** Plain text and basic opacity fades look "boring" and "basic" per user feedback. Every element needs spring entrance, glass styling, and proper SFX pairing.

**How to apply:** When building any new scene, start with glass morphism containers, spring entrances for every element, word highlighting for narration text, and SVG gradients for diagrams.
