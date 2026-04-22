---
name: crownpeak-brand
description: Applies Crownpeak's official brand colors and typography to artifacts, presentations, documents, and web components. Use when creating content that should follow Crownpeak/e-Spirit brand guidelines, visual formatting, or company design standards.
---

# Crownpeak Brand Styling

## Colors

**Primary Colors:**
- Dark Navy: `#0E2841` - Primary backgrounds, dark text
- White: `#FFFFFF` - Light backgrounds, text on dark
- Light Gray: `#E8E8E8` - Subtle backgrounds, borders

**Gradient (signature brand element):**
- Cyan to Purple: `#00E2CE` → `#6600CC`
- Use for accent bars, decorative elements, CTAs

**Accent Colors:**
- Blue: `#156082` - Accent 1
- Orange: `#E97132` - Accent 2
- Green: `#196B24` - Accent 3
- Cyan: `#0F9ED5` - Accent 4
- Purple: `#A02B93` - Accent 5 (primary brand accent)
- Lime: `#4EA72E` - Accent 6

## Typography

- **Font Family**: Open Sans (with Arial/sans-serif fallback)
- **Headings**: Open Sans, 18pt+
- **Body Text**: Open Sans, 12-16pt

## Visual Elements

**Signature Elements:**
- Cyan-to-purple gradient bars (horizontal accents)
- Purple chevron arrows (>>>) as directional indicators
- Diagonal geometric shapes with gradient fills

**Icon Style:**
- Solid fill icons in Purple (`#A02B93`) or gradient
- Simple, modern iconography

## Application Guidelines

### For HTML/React Artifacts
```css
:root {
  --cp-navy: #0E2841;
  --cp-cyan: #00E2CE;
  --cp-purple: #6600CC;
  --cp-accent-purple: #A02B93;
  --cp-light: #E8E8E8;
}

/* Gradient accent */
.brand-gradient {
  background: linear-gradient(90deg, #00E2CE 0%, #6600CC 100%);
}
```

### For Documents/Presentations
- Dark slides: Navy background (`#0E2841`) with white text
- Light slides: White background with navy text
- Accent elements: Use gradient bar at top or bottom
- Headings: Open Sans, larger sizes

### Color Combinations
- **Dark theme**: Navy bg + white text + gradient accents
- **Light theme**: White bg + navy text + purple accents
- **CTA buttons**: Gradient fill or solid purple
