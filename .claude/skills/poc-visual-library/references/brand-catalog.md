# Brand Style Catalog

Complete reference for all 19 brand styles. Each brand includes color palette, typography, visual effects, animation principles, and recommended use cases.

---

## 1. AI-Neural

**Aesthetic**: Cutting-edge AI and machine learning. Neural networks, data flows, computational processes. Intelligent, connected, alive with data.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Deep Dark | `#0a0a0f` | Primary background |
| Dark Layer | `#1a1a2e` | Secondary background, cards |
| Electric Cyan | `#00d4ff` | Primary accent, titles, borders |
| Neural Purple | `#a855f7` | Secondary accent, highlights |
| Data Green | `#22c55e` | Success/active states |
| Node Gray | `#4b5563` | Connections, borders |

**Gradients**:
- Hero: `linear-gradient(135deg, #00d4ff 0%, #a855f7 100%)`
- Mesh BG: Layered radial gradients of cyan (20%), purple (15%), green (10%)

**Typography**:
- Headlines: Inter 80-120px, weight 900, cyan/purple gradient text
- Subtitles: Inter 48-64px, weight 700, solid cyan
- Body: Inter 28-36px, weight 400-600, white 90% opacity
- Code/Data: JetBrains Mono 24-32px, cyan or green

**Visual Effects**:
- Neural network nodes: 12px cyan circles with `box-shadow: 0 0 20px rgba(0, 212, 255, 0.8)`, pulsing scale 1.0-1.5 over 2s
- Data flow particles: 4x40px gradient streaks flowing left-to-right over 4s
- Gradient mesh: Rotating radial gradient overlay with hue-rotate animation
- Connection lines: Gradient from transparent to cyan, scaleX from 0 to 1

**Animation Principles**:
- Data flows left-to-right, 3-5s linear, gradient trails
- Nodes pulse with staggered delays for network effect
- Elements fade in with 20px upward movement, 0.6s ease-out
- Child elements stagger 0.1s for cascading reveals

**Best For**: AI tutorials, ML explainers, data science, neural network demos

---

## 2. Cyberpunk Neon

**Aesthetic**: Dark, immersive futuristic hacker aesthetic. Neon-lit alleyways, digital rain, terminal screens at 3 AM. Harsh, high-contrast. NOT friendly or approachable - for experts and hackers.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Deep Dark | `#0a0a0f` | Primary background |
| Dark Slate | `#1a1a2e` | Card backgrounds |
| Neon Cyan | `#00ffff` | Primary accent, titles, borders |
| Magenta | `#ff00ff` | Secondary, highlights, hover |
| Electric Blue | `#00d4ff` | Code, links, interactive |
| Warning Red | `#ff0055` | Errors, alerts |
| Success Green | `#00ff88` | Success states |

**Typography**:
- Headlines: Orbitron 60-80px, weight 900, cyan neon glow (`text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff`)
- Sections: Orbitron 42-52px, weight 700, magenta glow
- Body: JetBrains Mono 18-20px, weight 400, color `#b8c6db`
- Code: JetBrains Mono 16-18px, weight 500, syntax colored

**Visual Effects**:
- Neon glow: `box-shadow: 0 0 30px cyan, 0 0 60px cyan, inset 0 0 30px cyan`
- Scanlines: `repeating-linear-gradient(0deg, rgba(0,0,0,0.1) 0-1px, transparent 1-2px)`, animate translateY 8-10s
- Corner accents: 20-30px `::before/::after` L-shaped borders in magenta
- RGB glitch: Quick bursts (0.1s) every 2-3s, offset text-shadow cyan/magenta
- Pulse glow: box-shadow 20px to 60px blur, 2s ease-in-out infinite

**Animation Principles**:
- Pulsing glows: 2s ease-in-out, shadow 20px to 60px
- RGB split: 0.1s bursts every 2-3s with translate + shadow
- Typing cursor: 1s step-end blink
- Reveals: opacity + transform (translateY or scale) over 0.5-1s

**Best For**: Developer tools, security content, hacking tutorials, CLI tools, terminal demos

---

## 3. Modern Gradient

**Aesthetic**: Instagram/Stripe-inspired. Rich gradients, glass morphism, modern typography. Digital sophistication with vibrant color transitions.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Deep Night | `#1a1a2e` | Primary background |
| Dark Space | `#16213e` | Secondary background |
| Midnight | `#0f172a` | Deepest background |
| Purple | `#a855f7` | Primary gradient color |
| Pink | `#ec4899` | Primary gradient color |
| Indigo | `#6366f1` | Secondary gradient |
| Violet | `#8b5cf6` | Secondary gradient |
| Cyan | `#06b6d4` | Accent |
| Soft Pink | `#f472b6` | Tertiary |

**Signature Gradients**:
- Purple-Pink Hero: `linear-gradient(135deg, #a855f7 0%, #ec4899 100%)`
- Indigo-Purple: `linear-gradient(90deg, #6366f1 0%, #a855f7 100%)`
- Pink Sunrise: `linear-gradient(135deg, #ec4899 0%, #f472b6 50%, #a855f7 100%)`
- Cool Spectrum: `linear-gradient(135deg, #06b6d4 0%, #6366f1 50%, #a855f7 100%)`
- Radial Glow: `radial-gradient(circle at top right, #a855f7 0%, #1a1a2e 70%)`

**Typography**: Inter only
- Hero: 64px/800, gradient text
- Heading: 48px/700
- Section: 36px/600
- Body Large: 18px/500
- Body: 16px/400

**Visual Effects**:
- Glass morphism: `background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1)`
- Gradient borders: Pseudo-element with mask-composite trick
- Gradient text: `background-clip: text; -webkit-text-fill-color: transparent`
- Glow: `text-shadow: 0 0 40px rgba(168, 85, 247, 0.8), 0 0 80px rgba(168, 85, 247, 0.4)`
- Animated gradient: `background-size: 200% 200%; animation: gradient-shift 3s ease infinite`

**Animation Principles**:
- Gradient shifts via background-position, background-size 200% 200%
- Smooth reveals: opacity + scale (0.95 to 1.0) together
- Blur reveals: filter blur + opacity transitions
- Never instant color changes - always ease

**Best For**: SaaS products, social media, modern web apps, trend-focused content

---

## 4. Corporate Modern

**Aesthetic**: Professional yet contemporary. Clean lines with sophisticated color use. Balanced between approachable and authoritative.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Navy Dark | `#0f172a` | Primary background |
| Slate Dark | `#1e293b` | Card backgrounds |
| Blue Primary | `#3b82f6` | Primary accent |
| Blue Light | `#60a5fa` | Secondary accent |
| Emerald | `#10b981` | Success, positive |
| Amber | `#f59e0b` | Warning, attention |
| Slate Text | `#e2e8f0` | Body text |

**Typography**: Inter
- Headlines: 56-72px, weight 800, blue or white
- Body: 18-24px, weight 400, slate text

**Visual Effects**:
- Subtle card shadows: `box-shadow: 0 4px 20px rgba(0,0,0,0.3)`
- Clean borders: `1px solid rgba(255,255,255,0.1)`
- Minimal gradients: Subtle top-to-bottom or left-to-right
- Icon containers: Rounded squares with blue background at 10% opacity

**Best For**: Enterprise SaaS, B2B content, product demos, corporate training

---

## 5. Clean Corporate

**Aesthetic**: Crisp, minimal, trustworthy. Maximum clarity and readability. Professional without being stuffy.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| White | `#ffffff` | Primary background |
| Light Gray | `#f8fafc` | Card backgrounds |
| Dark Text | `#1e293b` | Primary text |
| Blue | `#2563eb` | Primary accent |
| Green | `#16a34a` | Success |
| Red | `#dc2626` | Error |

**Typography**: Inter
- Headlines: 48-64px, weight 700-800, dark text or blue
- Body: 16-20px, weight 400, dark text

**Visual Effects**: Minimal - clean lines, subtle shadows, crisp borders
**Best For**: Documentation, tutorials, professional presentations

---

## 6. Brutalist

**Aesthetic**: Raw, bold, unapologetic. High contrast, harsh geometry, intentionally rough. Makes a statement.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Black | `#000000` | Primary background |
| White | `#ffffff` | Text, borders |
| Red | `#ff0000` | Accent |
| Yellow | `#ffff00` | Highlight |

**Typography**: Monospace or heavy sans-serif
- Headlines: 80-120px, weight 900, uppercase, tight letter-spacing
- Body: 16-20px, monospace

**Visual Effects**:
- Thick borders: 4-8px solid white or red
- No rounded corners - all sharp edges
- Harsh shadows or no shadows
- Glitch effects, noise overlays

**Best For**: Bold statements, contrarian content, punk-tech, manifestos

---

## 7. Enterprise Dark

**Aesthetic**: Serious, powerful, data-heavy. Command center feel. Authority and sophistication.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Deep Dark | `#0a0a12` | Primary background |
| Dark Blue | `#111827` | Card backgrounds |
| Electric Blue | `#3b82f6` | Primary accent |
| Cyan | `#06b6d4` | Data highlights |
| Gray | `#6b7280` | Secondary text |

**Typography**: Inter or system sans-serif
**Best For**: Enterprise tools, security dashboards, DevOps, infrastructure

---

## 8. Fintech

**Aesthetic**: Precision, trust, data visualization. Clean with accent greens. Bloomberg/Robinhood inspired.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Dark BG | `#0f172a` | Background |
| Green | `#22c55e` | Positive/up |
| Red | `#ef4444` | Negative/down |
| Blue | `#3b82f6` | Neutral data |
| Gold | `#eab308` | Premium |

**Typography**: Inter for text, JetBrains Mono for numbers
**Best For**: Finance, crypto, trading, analytics

---

## 9. High Contrast

**Aesthetic**: Maximum accessibility and readability. Bold, clear, no ambiguity.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Black | `#000000` | Background |
| White | `#ffffff` | Text |
| Yellow | `#fbbf24` | Primary accent |
| Blue | `#3b82f6` | Links, interactive |

**Typography**: Large sizes, heavy weights, clear hierarchy
**Best For**: Accessibility-focused content, presentations, education

---

## 10. Luxury Premium

**Aesthetic**: Elegant, refined, exclusive. Gold accents, dark backgrounds, serif typography.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Rich Black | `#0a0a0a` | Background |
| Dark Charcoal | `#1a1a1a` | Cards |
| Gold | `#d4a853` | Primary accent |
| Champagne | `#f5e6c8` | Secondary |
| Platinum | `#e5e5e5` | Text |

**Typography**: Serif for headlines (Playfair Display or similar), sans-serif for body
**Best For**: Premium products, luxury brand content, high-end tutorials

---

## 11. Minimalist Dark

**Aesthetic**: Less is more. Content-first, clean, focused. Maximum breathing room.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Near Black | `#111111` | Background |
| Dark Gray | `#1a1a1a` | Cards |
| White | `#ffffff` | Primary text |
| Gray | `#888888` | Secondary text |
| Accent | `#a855f7` | Single accent color |

**Typography**: Inter, generous spacing, limited weight range (400, 600, 700)
**Best For**: Clean tutorials, minimal presentations, content-focused videos

---

## 12. Nature Organic

**Aesthetic**: Warm, approachable, educational. Earth tones, organic shapes, natural gradients.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Forest Dark | `#1a2e1a` | Background |
| Earth Brown | `#4a3728` | Secondary |
| Leaf Green | `#22c55e` | Primary accent |
| Sky Blue | `#38bdf8` | Secondary accent |
| Warm Sand | `#fde68a` | Highlights |

**Typography**: Rounded sans-serif, warm weights
**Best For**: Science, education, environmental, health topics

---

## 13. Playful Colorful

**Aesthetic**: Vibrant, energetic, fun. Rainbow accents, bouncy animations, friendly.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Dark Base | `#1a1a2e` | Background |
| Electric Pink | `#ec4899` | Primary |
| Bright Yellow | `#fbbf24` | Accent |
| Lime Green | `#84cc16` | Success |
| Cyan | `#06b6d4` | Info |
| Purple | `#a855f7` | Highlight |

**Typography**: Rounded sans-serif, playful weights
**Best For**: Fun tutorials, creative content, community-focused videos

---

## 14. Retro Tech

**Aesthetic**: Vintage computing, CRT warmth, phosphor green, amber terminals. Nostalgic.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| CRT Dark | `#0a0a0a` | Background |
| Phosphor Green | `#00ff41` | Primary text |
| Amber | `#ff9500` | Secondary |
| CRT Blue | `#4fc3f7` | Accent |
| Scanline Dark | `#1a1a1a` | Overlays |

**Typography**: VT323, Courier New, or similar monospace
- Scanline overlays on everything
- CRT curvature effect on containers
- Phosphor glow on text

**Best For**: Retro computing, history of tech, terminal-focused content

---

## 15. SaaS Dashboard

**Aesthetic**: Dashboard-native, metric-focused, data-dense. Clean information hierarchy.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Dashboard Dark | `#0f172a` | Background |
| Card Dark | `#1e293b` | Card backgrounds |
| Blue | `#3b82f6` | Primary data |
| Green | `#22c55e` | Positive |
| Red | `#ef4444` | Negative |
| Purple | `#8b5cf6` | Secondary data |

**Typography**: Inter for all, JetBrains Mono for metrics
**Best For**: Product analytics, SaaS reviews, dashboard walkthroughs

---

## 16. Sci-Fi Space

**Aesthetic**: Cosmic, expansive, wonder-inspiring. Deep space backgrounds, stellar effects.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Space Black | `#050510` | Background |
| Nebula Blue | `#1e3a5f` | Secondary |
| Star White | `#f0f0ff` | Text |
| Plasma Blue | `#00b4d8` | Primary accent |
| Nebula Purple | `#7c3aed` | Secondary accent |
| Solar Gold | `#f59e0b` | Highlights |

**Typography**: Orbitron or similar for headlines, Inter for body
**Best For**: Space/astronomy content, futuristic tech, sci-fi themed videos

---

## 17. Tech Startup

**Aesthetic**: Energetic, bold, forward-looking. Gradient-heavy, modern, Silicon Valley.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Dark | `#0f172a` | Background |
| Blue | `#2563eb` | Primary |
| Violet | `#7c3aed` | Secondary |
| Emerald | `#059669` | Success |
| Orange | `#f97316` | CTA/Attention |

**Typography**: Inter, bold weights for headlines
**Best For**: Startup launches, product announcements, funding news

---

## 18. Vaporwave

**Aesthetic**: Retro-futuristic, 80s/90s nostalgia, pastel neons, Japanese characters, grid backgrounds.

**Color Palette**:
| Name | Hex | Usage |
|------|-----|-------|
| Dark Purple | `#1a0a2e` | Background |
| Hot Pink | `#ff6b9d` | Primary |
| Cyan | `#00ffff` | Secondary |
| Lavender | `#c084fc` | Accent |
| Peach | `#fb923c` | Warm accent |

**Typography**: Pixel fonts or stylized sans-serif for headlines, clean sans for body
- Chrome text effects, sunset gradients
- Grid perspective backgrounds
- Palm tree / sunset silhouettes

**Best For**: Nostalgic content, aesthetic videos, creative/art topics

---

## 19. Dynamous

**Aesthetic**: Brand-specific style for Dynamous AI content. Professional yet approachable.

**Note**: Use this brand specifically for Dynamous-branded content. Check brand assets for specific guidelines.

---

## Brand Selection Matrix

| Brand | Energy | Formality | Tech Level | Accessibility |
|-------|--------|-----------|------------|---------------|
| ai-neural | Medium | Medium | High | Medium |
| cyberpunk-neon | High | Low | High | Medium |
| modern-gradient | High | Low | Medium | High |
| corporate-modern | Medium | High | Medium | High |
| clean-corporate | Low | High | Low | Very High |
| brutalist | Very High | Low | Medium | Medium |
| enterprise-dark | Medium | Very High | High | Medium |
| fintech | Medium | High | High | Medium |
| high-contrast | Medium | Medium | Low | Very High |
| luxury-premium | Low | Very High | Low | High |
| minimalist-dark | Low | Medium | Medium | High |
| nature-organic | Low | Low | Low | High |
| playful-colorful | Very High | Low | Low | High |
| retro-tech | Medium | Low | High | Medium |
| saas-dashboard | Medium | High | High | High |
| scifi-space | High | Medium | Medium | Medium |
| tech-startup | High | Medium | Medium | High |
| vaporwave | High | Low | Low | Medium |
| dynamous | Medium | Medium | Medium | High |
