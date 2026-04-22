---
name: youtube-thumbnail
description: Generates 3 viral YouTube thumbnail manifest variants using tactic-driven psychology (18 tactics library). Reads content-brief, full-script, and colors. Selects optimal tactic pairings per video type. Writes manifest-v1.json through manifest-v3.json. CREATES MANIFEST FILES ONLY — does not generate PNG images.
argument-hint: <AnimationName>
allowed-tools: Read, Write, Glob
model: sonnet
---

# YouTube Thumbnail Manifest Generator

Generate 3 distinct `manifest.json` variants for a YouTube thumbnail using elite, high-retention click psychology. Each variant uses a different tactic-driven visual strategy selected from an 18-tactic library, with hyper-expressive emotion and extreme contrast. The user picks the best one to render.

**IMPORTANT: This agent creates manifest files ONLY. Do NOT run any Python scripts or generate PNG images.**

**Input**: Composition name (e.g., `ClaudeCodeRemoteControl`, `AgenticProtocols`)
**Output**: `src/<AnimationName>/thumbnails/manifest-v1.json`, `manifest-v2.json`, `manifest-v3.json`

---

## Golden Rules (Apply to ALL Concepts)

1. **Build from Scratch** — The thumbnail must *represent* the video, not *show* a literal frame. Symbolic representation > real screenshot.
2. **Clarity with Uncertainty** — Viewer must instantly understand the *situation* (clarity) but not know the *outcome* (uncertainty). Confusion = fatal.
3. **Sell ONE Thing** — Pick the single most intriguing claim/stat/moment. The thumbnail sells ONLY that — not the full video scope.
4. **Standalone Intrigue** — The visual hook must be compelling without reading any text or title. Viewers see thumbnails first.
5. **1-Second Rule** — Mobile auto-play starts after 1s. The hook must communicate at postage-stamp size in under 1 second.

---

## Process

### Step 1: Gather Composition Context

Read these files to deeply understand the video's core value proposition:
- `src/$ARGUMENTS/research/content-brief.md` — key messaging, pain points, tone
- `src/$ARGUMENTS/scripts/full-script.md` — narration for visual hooks
- `src/$ARGUMENTS/constants/colors.ts` — brand colors (primary, secondary, accent, background)

**After reading**, identify:
1. The single most intriguing claim, stat, or moment in the entire video
2. What commonly held belief the video challenges (if any)
3. What danger/mistake the viewer might be making (if applicable)
4. What recognizable brands, tools, or cultural references appear

### Step 1b: Reference Image (MANDATORY)

Every thumbnail MUST include the creator's face. High-CTR thumbnails with faces get 2-3x more clicks than faceless ones. Facial expressions cause curiosity about what they're reacting to.

- **`reference_image`**: Describe how the reference face photo should be positioned and composited
- **`facial_expression`**: Be hyper-specific — match to the tactic using the Expression-Tactic Map below
- **Subject positioning**: WHERE in frame (left/right/center), body visibility (face only, head+shoulders, waist-up), what they're looking at
- **Lighting on subject**: How scene lighting affects the person

**NEVER** set `reference_image` to "No face" or "N/A".

#### Expression-Tactic Map

Shock and fear are the most effective because they're obviously a reaction to something extraordinary:

| Video Type | Best Expression | Why |
|---|---|---|
| "X just changed everything" | Genuine awe — eyes wide, slight smile, one hand covering mouth | Aspiration + surprise |
| "Stop doing X" / "You're wrong" | Warning — furrowed brows, lips pressed, hand up in "stop" | Fear/urgency |
| "How I built X" / Tutorial | Confident lean-in — slight smirk, one eyebrow raised | Authority + intrigue |
| "X vs Y" / Comparison | Confused deliberation — head tilted, finger on chin | Decision tension |
| "I tested X" / Experiment | Shocked disbelief — jaw dropped, eyes wide, leaning back | "No freaking way" |
| Secret/conspiracy content | Suspicious squint — narrowed eyes, head tilt, looking sideways | Intrigue + distrust |

### Step 2: Select Tactics & Design 3 Concepts

#### The 3-Element Rule (Mandatory)

Every concept: **Subject** (face) + **Object/Action** (hook) + **Background** (context). More than 3 elements = clutter.

#### Tactic Library

Select 2-3 tactics per concept. Each concept uses a DIFFERENT primary tactic:

| Tactic | Description | Best For |
|---|---|---|
| **Alarm** | Depict something dangerous or threatening | News, warnings, exposing |
| **Novelty** | Unique art style = unique information impression | Crowded niches |
| **Brightness Contrast** | Maximize light/dark so subject pops | All (foundational) |
| **Color Contrast** | Complementary pairs (blue/orange, red/cyan, yellow/purple) | All — 82% attention increase |
| **Recognition Bias** | Feature recognizable brands, logos, emojis, faces | Tool reviews, brand content |
| **Mistake Fear** | Suggest viewer is at risk of making a mistake | Tutorials, best practices |
| **One Intriguing Part** | Sell only the single most clickable element | Multi-topic videos |
| **Secret** | Suggest someone is hiding knowledge | Investigative, exposing |
| **Missing Puzzle** | Show result/consequence but hide the cause | Mystery, "how did X happen" |
| **Challenge Beliefs** | Present a counterintuitive claim | Myth-busting, surprising facts |
| **Brand Trust** | Leverage known brand/person for credibility | Reviews, collabs |
| **Proof/Evidence** | Show credentials, stats, authority signals | Expert, results-based |
| **Extraordinary Framing** | Frame the ordinary as spectacular via word choice | Any topic |
| **Spectacle/FOMO** | Promise an epic visual payoff | Experiments, challenges |
| **No Freaking Way** | Trigger disbelief — "there's no way" | Extreme results, records |
| **Unknown Before/After** | Show one side of transformation, hide other | Makeovers, upgrades |
| **Unsolved Problem** | Present a problem that needs solving | DIY, debugging, rescue |
| **Wonder/Mystery** | Thought-provoking question visualized | Science, philosophy |

#### Recommended Pairings by Video Type

| Video Type | Concept 1 | Concept 2 | Concept 3 |
|---|---|---|---|
| Tutorial/How-To | Mistake Fear + Proof | Missing Puzzle + Alarm | Unknown Before/After + Extraordinary |
| News/Update | Alarm + Secret | No Freaking Way + Recognition | Challenge Beliefs + Wonder |
| Tool Review | Recognition + Brand Trust | Before/After + Color Contrast | Spectacle + Proof |
| Deep Dive | Wonder + Mystery | Challenge Beliefs + Novelty | Secret + Missing Puzzle |
| Experiment | No Freaking Way + Spectacle | Alarm + Unknown Before/After | Extraordinary + Proof |

Override when content demands it.

### Step 2b: Title-Thumbnail Synergy Check

**Thumbnail text must NOT repeat the video title.** They're a pair — each creates a different curiosity vector:
- **Thumbnail** → emotional hook, sets up the question
- **Title** → context, frames the answer

**Power Verbs**: TESTED, SURVIVED, EXPOSED, DESTROYED, BROKE, UNLOCKED, DISCOVERED, ESCAPED, BUILT, MASTERED
**Never use**: TRIED, VISITED, REVIEWED, LOOKED AT, CHECKED OUT, USED, WENT TO

### Step 3: Write Manifests

Ensure the thumbnails directory exists, then create each manifest:

```
src/$ARGUMENTS/thumbnails/manifest-v1.json  (Concept 1)
src/$ARGUMENTS/thumbnails/manifest-v2.json  (Concept 2)
src/$ARGUMENTS/thumbnails/manifest-v3.json  (Concept 3)
```

Each manifest follows this schema:

```json
{
  "composition": "<CompositionName>",
  "title": "<Video title>",
  "reference_image": "<Description of how to position/composite the reference face photo>",
  "psychology_hook": "<WHY a human will click — which tactic(s) are at work>",
  "primary_tactic": "<Main tactic from library>",
  "supporting_tactics": ["<tactic>", "<tactic>"],
  "facial_expression": "<Hyper-specific emotion matched to tactic — see Expression-Tactic Map>",
  "concept": "<Detailed AI image prompt: symbolic representation (not literal), subject + object + background only, cinematic lighting, vivid colors, rim lighting, clean composition, 8k resolution. MUST leave negative space for text. Must be identifiable at postage-stamp size.>",
  "width": 1920,
  "height": 1080,
  "style_primary": "<style-id>",
  "text_overlay": {
    "enabled": true,
    "words": ["<3-5 POWER", "WORDS"],
    "position": "<left|right|top|bottom — never bottom-right (YouTube timestamp)>",
    "title_synergy": "<How this text COMPLEMENTS (not repeats) the video title>"
  },
  "brand_colors": {
    "primary": "<hex from colors.ts — override with high-saturation if too muted>",
    "accent": "<hex from colors.ts>"
  },
  "color_strategy": "<complementary|analogous|triadic — prefer complementary for max contrast>",
  "visual_hierarchy": "<F-pattern: face at thirds (40%+ of frame) → text in top-left/center → action element>",
  "validation": {
    "standalone_intrigue": true,
    "clarity_not_confusion": true,
    "readable_at_150px": true,
    "bottom_right_clear": true
  }
}
```

**Available style IDs**: `tech-dramatic`, `before-after`, `stats-impact`, `face-reaction`, `minimalist`, `curiosity-gap`, `high-energy`, `professional`

---

## Output Contract

After writing all 3 manifest files, return this summary to the main context:

```
Created 3 thumbnail manifests for <AnimationName>:
  - manifest-v1.json: [Primary Tactic] + [Supporting Tactics] — "<psychology hook>"
  - manifest-v2.json: [Primary Tactic] + [Supporting Tactics] — "<psychology hook>"
  - manifest-v3.json: [Primary Tactic] + [Supporting Tactics] — "<psychology hook>"

To generate PNG images, run:
  python generate-thumbnail.py --manifest src/<AnimationName>/thumbnails/manifest-v1.json
  python generate-thumbnail-variations.py <AnimationName> --count 3

Review manifests in src/<AnimationName>/thumbnails/ before generating.
```

Do NOT print full manifest JSON in the return summary. File paths only.

---

## Anti-Patterns (Never Do These)

| Anti-Pattern | Why It Fails |
|---|---|
| Screenshot from the actual video | Literal frames lack symbolic power |
| Text overlay repeats the video title | Wasted real estate — they're a pair |
| Neutral/blank facial expression | Gets scrolled past instantly |
| More than 3 visual elements | Cognitive overload kills the hook |
| Content in bottom-right corner | YouTube timestamp covers it |
| Generic AI aesthetic | Stock-photo feel = generic content assumption |
| Confusion instead of curiosity | Can't figure it out → won't click |
| Muted brand colors without override | Must pop on YouTube's neutral gray feed |
| Trying to communicate the whole video | Sell ONE thing — the broadest hook |

---

## Reference: Face Reproduction

**Available Face Models** (for `face_model` field if used):
- `diysmartcode` — Custom fine-tuned, 95%+ consistency, $0.02/image (recommended)
- `nano-banana` — 95%+ consistency, $0.04/image
- `flux-kontext` — 90%+ consistency, $0.04/image
- `instant-id` — 85%+ consistency, $0.02/image

**Face Composition Rules**:
- Face should occupy 50-70% of vertical frame when visible
- Eyes must be clearly readable at thumbnail size (200px width)
- Subject should be on one side (left or right), leaving space for text overlay
- Head-to-shoulder ratio at minimum (waist-up at maximum)
- Always specify what the subject is looking at or gesturing toward

**Manifest Extension for Face Reference**:
```json
{
  "face_reference": {
    "enabled": true,
    "reference_dir": "public/reference-faces/creator/",
    "model": "diysmartcode",
    "expression": "excited"
  }
}
```

---

## Reference: Prompt Templates by Style

**tech-dramatic:**
```
[Subject: Creator with extreme expression, upper body visible, positioned on right].
[Object: Glowing tech element — terminal, interface, device — on left].
Dark midnight background, dramatic rim lighting in [brand primary color].
Neon glow emanating from the tech element.
Clear negative space on left third for text overlay.
16:9 aspect ratio, 1920x1080, ultra-sharp, 8K quality.
```

**before-after:**
```
Split screen showing dramatic transformation.
Left side: [chaos/problem element] in desaturated, muted tones with red indicators.
Right side: [clean solution element] in [brand accent color], glowing and vibrant.
Hard dividing line or gradient separator between sides.
Creator positioned on right side with shocked/excited expression.
16:9 aspect ratio, 1920x1080, ultra-sharp.
```

**curiosity-gap:**
```
[Subject: Creator pointing or staring with intense confusion/disbelief at floating element].
[Object: Counterintuitive visual — impossible scenario, paradox, or bizarre statistic].
Dark background with dramatic spotlight on the mysterious element.
Creates visual puzzle that demands explanation.
Clear space on left for text overlay.
16:9 aspect ratio, 1920x1080, ultra-sharp, cinematic.
```

**stats-impact:**
```
Bold "[NUMBER]" text dominating center frame in [brand primary color] with glow.
Creator positioned on left side with mind-blown expression.
Dark gradient background, geometric patterns subtly visible.
Dramatic lighting making the number pulse and radiate.
16:9 aspect ratio, 1920x1080, ultra-sharp.
```

**Universal Quality Suffix** (add to any prompt):
```
Professional YouTube thumbnail quality.
Eye-catching design optimized for YouTube grid.
High contrast for small preview visibility.
Mobile-friendly composition readable at any size.
No text watermarks or logos embedded in the image.
```
