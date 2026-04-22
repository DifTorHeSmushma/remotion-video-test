# Thumbnail Evaluation Framework

10-criteria checklist for evaluating thumbnail manifests before generation. Run this check on every manifest.

---

## Mandatory Criteria (Must Pass ALL 7)

### 1. Honesty Check
**Does the thumbnail promise something the video delivers?**

- The hook (stat, claim, visual) appears in the video with full context
- The expression matches the video's actual emotional tone
- No implied claim the video doesn't back up
- A viewer who clicks will feel their expectations were met

**Fail triggers:** Superlative text, exaggerated expressions for educational content, implied controversy where none exists.

### 2. Clarity at Thumbnail Size
**Is the concept instantly understandable at 150px wide?**

- The visual situation is clear in under 1 second
- No ambiguous imagery that requires zooming to understand
- The 3-element composition reads cleanly at any size

**Test:** Describe what you see in one sentence. If it takes more than one sentence, it's too complex.

### 3. Three-Element Rule
**Does the composition have exactly 3 visual elements?**

- Subject (face/person) — 40%+ of frame
- Object (hook element) — clear and identifiable
- Background — not competing for attention

**Fail triggers:** 4+ distinct visual elements, busy backgrounds that compete with the object, multiple text blocks.

### 4. Text Effectiveness
**Is the text overlay working hard?**

- Under 12 characters / 1-3 words
- Does NOT repeat the video title
- Readable at 150px with bold sans-serif + stroke/shadow
- Positioned away from bottom-right (timestamp zone)

### 5. Face & Expression
**Is the face compelling and appropriate?**

- Face takes up 40%+ of frame
- Expression is hyper-specific (not "happy" but "calm confidence with slight knowing smile")
- Expression matches the video's actual tone (see honest-hooks.md)
- Eyes are clearly visible and convey emotion

### 6. Color & Contrast
**Will this stand out in the YouTube feed?**

- High contrast between foreground and background
- Colors are saturated enough to pop on YouTube's neutral gray feed
- Complementary or analogous color strategy applied
- No more than 3 dominant colors

### 7. Safe Zones
**Are important elements in safe areas?**

- Nothing important in bottom-right (YouTube timestamp: ~10% of frame)
- Core content within center 60% safe zone (mobile cropping)
- No important elements at extreme edges

---

## Optimization Criteria (Score 1-5 Each)

### 8. Curiosity Generation
**How strongly does this create an information gap?**

- 5: "I need to click this right now to find out"
- 4: "That's interesting, I want to know more"
- 3: "Seems worth checking out"
- 2: "I can probably guess what this is about"
- 1: "I already know everything from the thumbnail"

### 9. Title Synergy
**How well do thumbnail and title work as a pair?**

- 5: Thumbnail and title create complementary curiosity vectors — each adds something the other doesn't
- 4: Good pairing, each contributes unique information
- 3: Decent pairing but some redundancy
- 2: Thumbnail mostly repeats what the title says
- 1: Thumbnail and title say the same thing

### 10. Feed Differentiation
**Would this stand out against competing thumbnails for the same topic?**

- 5: Completely unique approach — no one else has this angle
- 4: Fresh take that stands out from the standard approach
- 3: Some unique elements but follows common patterns
- 2: Similar to what most channels would create
- 1: Generic, interchangeable with any competing thumbnail

---

## Scoring

| Score | Rating | Action |
|-------|--------|--------|
| 7/7 mandatory + 13-15 optimization | Ready to generate | Paste prompt into Gemini |
| 7/7 mandatory + 10-12 optimization | Good | Generate, consider small tweaks |
| 7/7 mandatory + <10 optimization | Needs iteration | Revise concept before generating |
| <7/7 mandatory | Fail | Must fix mandatory criteria first |

---

## Quick Validation Sequence

For each manifest, run through these yes/no gates:

```
1. HONEST? → Does the video deliver what this thumbnail promises?
2. CLEAR?  → Can I understand this in 1 second at 150px?
3. SIMPLE? → Exactly 3 elements? (person + object + background)
4. TEXT?   → Under 12 chars? Not repeating title? Readable?
5. FACE?   → 40%+ of frame? Expression matches content tone?
6. POP?    → High contrast? Saturated colors? Stands out?
7. SAFE?   → Nothing in bottom-right or extreme edges?
```

If any gate is "no" → fix before generating.
