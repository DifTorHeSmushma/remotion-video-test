---
name: youtube-thumbnail
description: Use when the user asks to create thumbnails, generate thumbnail concepts, design thumbnail manifests, make thumbnail variants, or says "thumbnails for [composition]". Generates 3 Nano Banana Pro-optimized manifest JSON files with psychology-driven concepts and ready-to-paste Gemini prompts. Reads content-brief, full-script, and colors.ts to select optimal concepts. Outputs manifests that paste directly into Google Gemini with Nano Banana Pro for generation. Does NOT render PNG images.
metadata:
  author: diysmartcode
  version: '2.0'
---

# YouTube Thumbnail Generator — Nano Banana Pro Edition

Generate 3 distinct thumbnail concepts as `manifest.json` files. Each contains a psychology-driven concept, a **ready-to-paste Nano Banana Pro prompt**, and all metadata needed to produce the final image in Google Gemini.

**This skill creates manifest files ONLY. Do NOT run any Python scripts or generate PNG images.**

---

## Philosophy: Honest Thumbnails That Win Clicks

This channel earns trust by being straight with the audience. Every thumbnail must follow the **Honest Hook Principle**:

> Make people click because the content is genuinely worth their time — not because you tricked them into expecting something else.

### What This Means in Practice

**DO:**
- Use real stats, real results, real claims from the video
- Show the actual tool, product, or concept being discussed
- Create curiosity about something the video genuinely delivers
- Use emotions that match the creator's actual reaction to the content
- Frame the real value in the most compelling way possible

**NEVER:**
- Superlatives not backed by the video ("The BEST...", "INSANE...", "GAME CHANGER...")
- Facial expressions that don't match the video's actual tone
- Promise a reveal or payoff the video doesn't deliver
- Use fear/alarm tactics when the content is educational
- Manufacture controversy or drama that isn't in the content

### The Trust-CTR Framework

High CTR without retention destroys channels. The goal is:

| Metric | Target | How Thumbnails Help |
|---|---|---|
| CTR | 5-10% | Honest curiosity hooks matched to audience interest |
| Retention | 50-70%+ | Thumbnail promise aligns with video delivery |
| Satisfaction | High | Viewer feels respected, not tricked |

Misleading thumbnails can boost CTR 40-60% short-term but reduce recommendation traffic by 80%+ within weeks as algorithmic penalties accumulate. Honest thumbnails compound trust over time, increasing subscriber CTR 15-20%.

---

## Golden Rules

### 1. Represent, Don't Screenshot

The thumbnail symbolically represents the video's core value. It is NOT a literal frame from the video. A symbolic visual communicates the concept more powerfully. If someone could pause the video and find this exact frame, it's too literal.

### 2. Clarity + Curiosity, Never Confusion

Every thumbnail must pass this test:
- **Clarity** = "I instantly know what's happening in this image" (REQUIRED)
- **Curiosity** = "I want to know what happens next / what the result is" (DESIRED)
- **Confusion** = "I don't understand what I'm looking at" (FATAL)

At postage-stamp size (150px wide), a viewer must understand the situation in under 1 second.

### 3. Sell the ONE Most Honest Hook

A multi-topic video picks the ONE claim, stat, or insight that is:
1. Genuinely the most interesting part of the video
2. Broadly appealing to the target audience
3. Something the video fully delivers on

The thumbnail sells ONLY that one thing.

### 4. Thumbnail Intrigues Before the Title

Viewers see the thumbnail first. The visual hook must be compelling standalone. Test: "Would someone want to learn more from this image without reading any text?"

### 5. Thumbnail + Title = A Pair, Not a Copy

Thumbnail text must NEVER repeat the video title. They work as complementary curiosity vectors:
- **Thumbnail visual + text** → emotional hook, sets up the question
- **Video title** → context, frames the answer

Example: Title = "Claude Code Just Changed Everything" → Thumbnail text = "WAIT WHAT?" (not "Claude Code Update")

### 6. Under 4 Words, Under 12 Characters

Thumbnail text: 1-3 words maximum, under 12 total characters. Research shows thumbnails with fewer than 12 text characters significantly outperform text-heavy designs. Every character must earn its place.

---

## Process

### Step 1: Gather Context

Read these files to deeply understand the video:
- `src/<Composition>/research/content-brief.md` — key messaging, pain points, tone
- `src/<Composition>/scripts/full-script.md` — narration, claims, stats, proof points
- `src/<Composition>/constants/colors.ts` — brand colors

**After reading, identify:**
1. The single most interesting factual claim or result in the video
2. What concrete problem the video solves for the viewer
3. What recognizable brands, tools, or stats appear
4. The honest emotional tone — what would the creator genuinely feel about this content?
5. What commonly held belief the video challenges (if any)

**Honesty check:** For each potential hook, ask: "Does the video fully deliver on this promise within the first 2 minutes?" If not, pick a different hook.

### Step 2: Select Concepts & Tactics

#### The 3-Element Rule (Mandatory)

Every concept has exactly 3 visual elements:
1. **Subject** — the person/face (40%+ of frame)
2. **Object** — the hook element (tool, stat, visual metaphor)
3. **Background** — context (gradient, environment, negative space)

More than 3 elements = clutter = confusion = lower CTR.

#### Tactic Library

Select 1-2 tactics per concept. Each concept uses a DIFFERENT primary tactic:

| Tactic | What It Does | Best For | Honesty Check |
|---|---|---|---|
| **Recognition Bias** | Feature recognizable brands, logos, tools | Tool reviews, brand content | Is this tool actually in the video? |
| **Proof/Evidence** | Show concrete stats, numbers, results | Results-based, benchmarks | Is this stat real and from the video? |
| **Missing Puzzle** | Show a result but hide the cause/method | How-to, tutorials | Does the video reveal the method? |
| **Challenge Beliefs** | Present a counterintuitive claim | Myth-busting, surprising facts | Does the video back this claim? |
| **Unknown Before/After** | Show one side of a transformation | Upgrades, improvements | Is the transformation real? |
| **Wonder/Mystery** | Develop a thought-provoking question | Deep dives, exploration | Does the video explore this fully? |
| **One Intriguing Part** | Sell the single most clickable element | Multi-topic videos | Is this actually in the video? |
| **Novelty** | Unique visual style = unique info | Crowded niches | Does the style match the content quality? |
| **Brand Trust** | Leverage known brand for credibility | Reviews, official content | Is the brand association accurate? |
| **Brightness Contrast** | High light/dark contrast for pop | All thumbnails (foundational) | Always appropriate |
| **Color Contrast** | Complementary color pairs for standout | All thumbnails (foundational) | Always appropriate |

**Tactics removed from v1 (too clickbaity for honest content):**
- ~~Alarm~~ — implies danger that may not exist
- ~~Secret~~ — implies conspiracy/hidden knowledge
- ~~Mistake Fear~~ — manufactures anxiety
- ~~Spectacle/FOMO~~ — overpromises excitement
- ~~No Freaking Way~~ — forces fake disbelief
- ~~Extraordinary Framing~~ — inflates ordinary into spectacular

These can be used ONLY when the video content genuinely warrants them (e.g., a real security vulnerability discovery justifies Alarm).

#### Concept Generation

For each of the 3 manifests, pick a **primary tactic** and 0-1 **supporting tactics**:

**Recommended pairings by video type:**

| Video Type | Concept 1 | Concept 2 | Concept 3 |
|---|---|---|---|
| Tutorial/How-To | Missing Puzzle + Proof | Before/After + Recognition | One Intriguing Part + Brand Trust |
| Tool Review | Recognition + Brand Trust | Proof/Evidence + Color Contrast | Before/After + Novelty |
| News/Update | Recognition + Proof | Challenge Beliefs + Wonder | One Intriguing Part + Brand Trust |
| Deep Dive | Wonder + Missing Puzzle | Challenge Beliefs + Novelty | Proof + Recognition |
| Benchmark/Test | Proof + Color Contrast | Before/After + Recognition | One Intriguing Part + Wonder |

### Step 3: Design Expression & Subject

Every thumbnail MUST include the creator's face. Thumbnails with faces get 25-50% higher CTR.

**Expression must match the video's actual tone:**

| Video Tone | Expression | Description |
|---|---|---|
| Genuinely impressive result | Calm confidence | Steady gaze, slight knowing smile, "this is worth your time" |
| Educational / walkthrough | Approachable instructor | Warm smile, relaxed posture, slight lean forward |
| Surprising discovery | Authentic curiosity | Raised eyebrow, slight head tilt, engaged eyes |
| Critical analysis | Thoughtful evaluation | Hand near chin, focused but fair expression |
| Exciting capability | Genuine enthusiasm | Real smile reaching the eyes, energized but not manic |
| Problem solved | Satisfied expert | Slight smirk, confident posture, "figured it out" energy |

**NEVER:** Jaw-dropped shock for educational content. Exaggerated fear for tutorials. Fake surprise for news updates.

**Subject positioning rules:**
- Face occupies 40%+ of frame
- Position at right third (standard) or center-right
- Head and shoulders visible minimum
- Describe WHERE they look: at camera (trust), at object (directs attention), slightly off-camera (contemplation)
- Describe lighting on subject: how the scene lighting affects them

### Step 4: Write Manifests

For each variant, create `src/<Composition>/thumbnails/manifest-v1.json`, `manifest-v2.json`, `manifest-v3.json`.

```json
{
  "composition": "<CompositionName>",
  "title": "<Video title>",
  "concept_summary": "<One sentence: what the viewer sees and why they click>",
  "honesty_check": "<What specific video content backs this thumbnail's promise>",
  "primary_tactic": "<Main tactic from library>",
  "supporting_tactics": ["<tactic>"],
  "reference_image": "<How to position the creator's face — position, body visible, gaze direction, lighting>",
  "facial_expression": "<Specific emotion matched to the video's actual tone — see Expression table>",
  "subject_position": "right-third | center-right",
  "object_description": "<The hook element — what it is, where it goes, how it looks>",
  "background_description": "<Background treatment — color, gradient, atmosphere>",
  "text_overlay": {
    "enabled": true,
    "text": "<1-3 words, under 12 characters total>",
    "position": "top-left | top-center | left-center",
    "font_style": "bold sans-serif, white with dark stroke/shadow for readability",
    "title_synergy": "<How this text complements (not repeats) the video title>"
  },
  "brand_colors": {
    "primary": "<hex — override muted colors with high-saturation version>",
    "accent": "<hex>"
  },
  "color_strategy": "complementary | analogous",
  "nano_banana_prompt": "<FULL READY-TO-PASTE PROMPT — see Prompt Construction below>",
  "validation": {
    "honest_promise": true,
    "clarity_not_confusion": true,
    "readable_at_150px": true,
    "three_elements_only": true,
    "bottom_right_clear": true,
    "text_under_12_chars": true
  }
}
```

### Step 5: Construct the Nano Banana Pro Prompt

This is the most critical step. The `nano_banana_prompt` field must be a **complete, ready-to-paste prompt** for Google Gemini with Nano Banana Pro.

#### Prompt Formula

Use this exact structure (based on the official Google prompting guide):

```
[Identity Lock] + [Subject + Expression + Position] + [Object + Action] + [Background + Lighting] + [Composition + Style] + [Text Rendering] + [Technical Specs]
```

#### Prompt Template

```
IDENTITY & SUBJECT:
Keep the person's facial features exactly the same as the reference image. [Expression description]. Position the person on the [position] of the frame, [body parts visible], [gaze direction]. [Lighting on subject].

OBJECT/HOOK:
[Detailed description of the hook element — what it is, its visual treatment, position in frame, colors, any text ON the object].

BACKGROUND:
[Background description — gradient, color, atmosphere, depth].

COMPOSITION:
[Layout description]. Clean negative space at [position] for text overlay. Only 3 elements in frame: the person, the [object], and the background. No clutter.

TEXT:
Render the text "[THUMBNAIL TEXT]" in bold, [color] sans-serif font with [outline/shadow treatment] at the [position] of the frame. Text must be large, sharp, and readable even at small sizes.

STYLE:
Professional YouTube thumbnail. 16:9 aspect ratio. Cinematic lighting. High contrast. High saturation. Ultra-sharp, 4K quality. Clean, modern design.
```

#### Prompt Writing Rules

1. **Identity lock is mandatory**: Always start with "Keep the person's facial features exactly the same as the reference image"
2. **Be specific, not vague**: "Dark navy to black gradient" not "dark background"
3. **Describe spatially**: Use "left third", "right third", "center", "top area" — be precise about where each element goes
4. **Name colors explicitly**: Use hex codes or vivid color names, never "nice color"
5. **Limit to 3 visual elements**: Person + object + background. That's it. If you're describing a 4th element, remove one
6. **Text rendering**: Always put text in quotes, specify exact font style, color, outline, and position
7. **No AI-art clichés**: Never use "ethereal", "whimsical", "majestic", "breathtaking" — these produce generic results
8. **Camera/lens language**: Use "medium shot", "eye-level", "shallow depth of field" for better composition control
9. **Material specificity**: "Brushed aluminum terminal frame" not "a terminal window"
10. **Positive framing**: Describe what you want, not what you don't want ("empty background" not "no clutter")

---

## Style Presets

| ID | Use For | Key Visual Elements |
|----|---------|-------------------|
| `tech-clean` | Coding, AI, tools — professional dark mode | Dark bg, clean UI elements, subtle accent glow |
| `proof-stat` | Benchmarks, results, data-driven | Bold number dominates, evidence-forward |
| `before-after` | Transformations, improvements | Split composition, muted vs vibrant |
| `brand-authority` | Official content, trusted sources | Logo + clean layout, premium minimal feel |
| `minimalist` | Professional, clean, authority | Single focal point, generous negative space |
| `curiosity-gap` | Teasers, partial reveals | Strategic concealment, shadows, partial view |

---

## Color Strategy

Brand colors from `colors.ts` may be too muted for thumbnails. YouTube's feed demands high saturation.

**Override rules:**
- If primary is dark/neutral → substitute with high-saturation version
- Use **complementary pairs** for maximum feed standout: blue/orange, red/cyan, yellow/purple
- High saturation is essential — but avoid all-neon (nothing stands out if everything glows)

**Proven combinations:** Yellow text on dark blue | White text on dark gradient | Cyan accents on dark bg | Orange/red accents on dark bg

**Avoid:** Light on light | Similar hues without contrast | More than 3 colors | Pastels without contrast anchor | YouTube's own red (#FF0000) — blends with the UI

---

## Visual Hierarchy

Viewers scan thumbnails in an F-pattern:

1. **Face** — at right third, 40%+ of frame, draws the eye first
2. **Text** — in negative space (top-left or top-center), bold sans-serif, stroke/shadow
3. **Object** — the hook element the subject is reacting to or presenting
4. **Never** — place anything important in bottom-right (YouTube timestamp) or frame edges (device cropping)

Keep the core content inside the center 60% safe zone for mobile cropping.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|---|---|
| Superlative text ("BEST", "INSANE", "GAME CHANGER") | Reads as clickbait, erodes trust with honest audience |
| Exaggerated expressions that don't match content | Viewers feel deceived → low retention → algorithmic penalty |
| Text overlay repeats the video title | Wasted real estate — thumbnail + title are a pair |
| More than 3 visual elements | Cognitive overload at thumbnail size |
| Content in bottom-right corner | YouTube timestamp overlay covers it |
| Generic AI aesthetic | Stock-photo feel signals generic content |
| Vague prompt language | "Beautiful scene" → unpredictable AI output |
| Fear/alarm for educational content | Mismatched tone destroys trust |
| Muted colors without override | Gets lost in YouTube's neutral feed |
| More than 3 words or 12 characters in text | Unreadable at mobile size, cluttered |

---

## References

- `references/nano-banana-prompting.md` — Full Nano Banana Pro prompt construction guide with examples
- `references/honest-hooks.md` — Honest thumbnail philosophy, trust-CTR framework, and hook formulas
- `references/evaluation-framework.md` — 10-criteria evaluation checklist
- `references/quick-reference.md` — One-page cheat sheet
