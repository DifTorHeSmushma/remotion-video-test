# Nano Banana Pro — Prompt Construction Guide

Complete reference for writing prompts that paste directly into Google Gemini with Nano Banana Pro for YouTube thumbnail generation.

---

## Model Capabilities

- **Identity locking**: Up to 14 reference images (6 with high fidelity). Always lock the creator's face.
- **Text rendering**: Sharp, legible text in multiple languages. Put text in quotes for exact rendering.
- **Aspect ratios**: Supports 16:9 natively (specify explicitly).
- **Resolution**: Generate at 1K, 2K, or 4K. Request "4K" for thumbnail work.
- **Reference images**: Upload creator face photos as reference. Use "Keep the person's facial features exactly the same as Image 1/the reference image."

---

## The 6-Component Prompt Formula

Based on official Google prompting guidelines. Every thumbnail prompt follows this structure:

```
[Subject] + [Action/Expression] + [Environment/Background] + [Composition] + [Art Style/Lighting] + [Text + Technical Details]
```

### Component Breakdown

#### 1. Subject (with Identity Lock)
```
Keep the person's facial features exactly the same as the reference image.
A [gender descriptor] with [expression description — be specific about eyes, mouth, posture].
Position the person on the [right third / center-right] of the frame,
[head and shoulders / waist-up] visible, [gaze direction].
```

**Expression specificity examples:**
- WEAK: "happy expression" → generic, unpredictable
- STRONG: "calm confidence — steady direct eye contact, slight knowing smile that reaches the eyes, relaxed shoulders, slight forward lean"
- STRONG: "authentic curiosity — one eyebrow raised, slight head tilt to the right, eyes engaged and focused on the object to the left"

#### 2. Action / Object (The Hook)
```
[What the object is, with specific visual details].
Position it [where in frame].
[Size, color, material, glow, text on the object].
```

**Object specificity examples:**
- WEAK: "a terminal window" → generic
- STRONG: "a dark terminal window with brushed aluminum frame, traffic-light dots (red #FF5F56, yellow #FFBD2E, green #27C93F), showing green monospace text on a #0D1117 background. The terminal displays '$ claude' as a command prompt with a blinking cyan cursor"

#### 3. Environment / Background
```
[Color/gradient description with hex codes].
[Atmospheric elements — subtle, not distracting].
[Depth cues if any].
```

**Background examples:**
- "Clean gradient background from deep navy (#0D1117) at top to slightly lighter (#161B22) at bottom"
- "Solid dark background (#0D1117) with a subtle radial glow of cyan (#58A6FF) at 10% opacity behind the subject"

#### 4. Composition
```
[Layout description — what goes where].
Clean negative space at [position] for text overlay.
Only 3 elements: the person, the [object], and the background.
Medium shot, eye-level camera angle.
```

#### 5. Art Style / Lighting
```
[Lighting setup — be specific about direction, color, intensity].
[Overall aesthetic].
```

**Lighting examples:**
- "Three-point lighting: warm key light from the right, cool cyan fill (#58A6FF) from the left creating a subtle rim on the subject's face, soft ambient fill"
- "Dramatic side lighting from the left, creating defined shadows on the right side of the face, with a subtle cyan backlight creating a rim glow on the subject's hair and shoulders"

#### 6. Text + Technical Specs
```
Render the text "[EXACT TEXT]" in bold, [color] sans-serif font
with [2px black outline / dark drop shadow] at the [position] of the frame.
The text must be large, sharp, and readable at small sizes.

Professional YouTube thumbnail. 16:9 aspect ratio.
Cinematic lighting. High contrast. High saturation.
Ultra-sharp, 4K quality. Clean, modern design.
```

---

## Complete Prompt Examples

### Example 1: Tech Tool Review (Brand Trust + Recognition)

```
Keep the person's facial features exactly the same as the reference image. Calm confident expression — steady direct eye contact, slight professional smile, relaxed shoulders. Position the person on the right third of the frame, head and shoulders visible, looking directly at camera. Warm key light from the right, cool cyan fill light (#58A6FF) from the left creating a subtle rim on the face.

On the left side of the frame, a large, crisp Claude Code terminal window with brushed aluminum frame and traffic-light dots. The terminal shows green and cyan monospace text on a dark #0D1117 background: "$ claude" as a prompt with a few lines of colorful output. The terminal is sharp, realistic, and dominant in size. A small Anthropic logo sits subtly in the corner of the terminal.

Clean gradient background from deep navy (#0D1117) at top to #161B22 at bottom. No other elements.

Clean, minimal composition. Only 3 elements: the person on the right, the terminal on the left, and the dark gradient background. Generous negative space at the top-left for text. Medium shot, eye-level framing.

Render the text "FULL GUIDE" in bold, white (#FFFFFF) sans-serif font with a 2px dark drop shadow at the top-left area of the frame. Text must be large, sharp, and readable at small sizes.

Professional YouTube thumbnail. 16:9 aspect ratio. Cinematic lighting. High contrast. High saturation. Ultra-sharp, 4K quality. Clean, modern, premium design.
```

### Example 2: Benchmark Result (Proof + One Intriguing Part)

```
Keep the person's facial features exactly the same as the reference image. Genuine enthusiasm — real smile reaching the eyes, slight forward lean, one eyebrow subtly raised, engaged and energized expression. Position the person on the right third of the frame, head and shoulders visible, looking toward the bold stat on the left with engaged interest.

On the left-center of the frame, the text "3.9X" rendered extremely large and bold in glowing cyan (#58A6FF) with a subtle outer glow effect. Below it in smaller white text: "FASTER". The numbers are the dominant visual element, taking up roughly 30% of the frame.

Solid dark background (#0D1117) with a subtle radial cyan glow at 8% opacity behind the large "3.9X" text, adding depth.

Clean composition. Only 3 elements: the person on the right, the bold stat on the left, and the dark background. Negative space at the top for any additional text overlay. Medium shot, eye-level.

Professional YouTube thumbnail. 16:9 aspect ratio. Cinematic lighting with dramatic side light. High contrast. High saturation. Ultra-sharp, 4K quality.
```

### Example 3: Before/After (Transformation + Unknown Before/After)

```
Keep the person's facial features exactly the same as the reference image. Thoughtful evaluation — hand near chin, focused but approachable eyes, slight analytical expression. Position the person on the right third of the frame, head and shoulders visible, looking between the two comparison elements.

Split composition on the left two-thirds. LEFT: a dark card labeled "Before" in muted gray, showing a few lines of messy, cluttered code in desaturated tones with red warning indicators. RIGHT: a brighter card labeled "After" in cyan (#58A6FF), showing clean organized code in vibrant colors with green success indicators (#3FB950). A bold cyan arrow points from the left card to the right card.

Dark background (#0D1117). The "Before" card has a slightly darker treatment, the "After" card has a subtle bright glow around its edges.

Clean composition. Only 3 elements: the person on the right, the split comparison on the left, and the dark background. Negative space at the top for text. Medium shot, eye-level.

Render the text "FIXED" in bold, cyan (#58A6FF) sans-serif font with a 2px black outline at the top-center of the frame.

Professional YouTube thumbnail. 16:9 aspect ratio. High contrast between the before and after states. Ultra-sharp, 4K quality.
```

---

## Prompt Quality Checklist

Before finalizing a prompt, verify:

- [ ] **Identity lock present** — starts with "Keep the person's facial features exactly the same as the reference image"
- [ ] **Aspect ratio specified** — "16:9 aspect ratio" is in the prompt
- [ ] **Resolution specified** — "4K quality" or "ultra-sharp" is in the prompt
- [ ] **Colors are specific** — hex codes or vivid color names, not vague descriptions
- [ ] **Spatial layout is clear** — "right third", "left side", "top-left" — precise positions
- [ ] **Only 3 elements** — person + object + background, nothing else
- [ ] **Expression is specific** — describes eyes, mouth, posture, not just "happy"
- [ ] **Lighting is directional** — "from the left", "key light from right", not just "well-lit"
- [ ] **Text is in quotes** — exact characters enclosed in quotation marks
- [ ] **Text style is specified** — font weight, color, outline/shadow, position
- [ ] **No negative instructions** — describes what IS there, not what ISN'T
- [ ] **No AI clichés** — no "ethereal", "majestic", "breathtaking", "stunning"
- [ ] **Bottom-right is empty** — no elements placed where YouTube timestamp goes

---

## Common Fixes

| Problem | Solution |
|---------|----------|
| Face doesn't match reference | Add "Keep the person's facial features exactly the same as the reference image" at the very start. Upload 3-5 reference photos with varied angles. |
| Text is blurry or wrong | Put exact text in quotes. Specify font weight, color, and outline. Add "sharp, legible text" |
| Too many elements / cluttered | Remove everything except person + object + background. Simplify. |
| Colors are muddy | Use hex codes. Add "high saturation" and "high contrast" |
| Generic AI look | Add specific material/texture descriptions. Use camera/lens language. Avoid cliché art direction words. |
| Wrong aspect ratio | Explicitly state "16:9 aspect ratio" early in the prompt |
| Object too small at thumbnail size | Make the object "large and dominant" — specify it takes up 30%+ of frame |
| Expression is generic | Describe specific muscle movements: "eyes wide", "one eyebrow raised", "slight smirk with left corner of mouth raised" |
