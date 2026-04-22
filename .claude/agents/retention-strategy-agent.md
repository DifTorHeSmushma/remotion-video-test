---
name: retention-strategy-agent
description: Analyzes script content and sync data for a composition, then produces a per-scene retention strategy document mapping each scene to specific retention components with exact props and triggerFrames. Runs before phase4-scene-builder so the scene agent has concrete, content-aware decisions rather than generic rules.
argument-hint: <AnimationName>
allowed-tools: Bash, Read, Write, Glob, Grep
model: sonnet
---

# Retention Strategy Agent

Analyze `$ARGUMENTS` and produce `src/$ARGUMENTS/retention-strategy.md` — a per-scene component prescription that the `phase4-scene-builder` reads before writing any TSX.

**Self-Contained Inputs** (read from disk — do NOT assume main context):
1. `.agents/plans/$ARGUMENTS.plan.md` — visual design + scene descriptions + midReHookPhrase
2. `src/$ARGUMENTS/scripts/full-script.md` — raw script with scene headers and narration text
3. `src/$ARGUMENTS/scripts/scene-*.txt` — TTS scripts (for [PAUSE] and reveal word detection)
4. `src/$ARGUMENTS/scripts/sceneNN-sync.json` — word timestamps (ALL scenes)
5. `src/$ARGUMENTS/constants/timing.ts` — TOTAL_FRAMES, SCENE_STARTS, AUDIO_OFFSET

**Output**:
- `src/$ARGUMENTS/retention-strategy.md`
- Update `src/$ARGUMENTS/phase-status.md`: set `3.5 - Retention` row to `done`

---

## Step 1: Load Inputs

Read all inputs. Extract:
- `TOTAL_FRAMES` from timing.ts (numeric parse — see generate-bg-music.py pattern)
- `AUDIO_OFFSET` from timing.ts (look for `AUDIO_OFFSET = N` or `audioOffset: N`)
- `FPS` from timing.ts (default 30)
- Scene list from timing.ts SCENES constant (keys, starts, durations)
- `midReHookPhrase` from plan.md (look for `midReHookPhrase:` field)
- All scene descriptions from plan.md (visual elements, diagram counts, code presence)
- Word timestamps from every `sceneNN-sync.json`

---

## Step 2: Run Dead Zone Audit

```bash
python3 scripts/audit-pattern-interrupts.py $ARGUMENTS 2>&1
```

Parse the output. For each dead zone found, note:
- Scene key (from "in 'sceneKey'")
- Frame range (start–end)
- Gap in frames
- Suggested component from the audit output

---

## Step 3: Classify Each Scene

For each scene in SCENES (skip scene00/preview), classify using this decision tree:

### Classification Rules

**Check plan.md description for this scene:**

| If plan mentions... | Scene type |
|---|---|
| diagram / flowchart / architecture / layers / flow / nodes | `diagram` |
| code block / terminal / syntax / command / snippet | `code` |
| single stat / percentage / number as hero content | `stats` |
| bullet list / steps / features (3+ items staggered) | `list` |
| CTA / subscribe / call to action / final scene (last in SCENES) | `cta` |
| everything else | `narration-primary` |

**Secondary signals from full-script.md section for this scene:**
- Word count < 80 and plan has a dominant visual → `stats` or `diagram`
- Scene has numbered list items (1. 2. 3.) → `list`
- Script mentions specific timestamps where new elements are introduced → diagram timing

### Diagram Element Detection

For `diagram` scenes: count distinct diagram elements in plan.md description.
If 3+ elements: mark `spotlightFocus: true` and identify the spoken word that introduces each element.
Cross-reference with sceneNN-sync.json to find triggerFrame for each element introduction.

Example: if plan says "Three layers: Data Layer, Logic Layer, UI Layer" and script says
"Starting with the data layer [sync:2.1s]... then the logic layer [sync:4.8s]... finally the UI [sync:7.2s]"
→ SpotlightFocus transitions at wordToFrame(2.1, AUDIO_OFFSET), wordToFrame(4.8, AUDIO_OFFSET), wordToFrame(7.2, AUDIO_OFFSET)

To find these timestamps: scan sync JSON for the exact word from the plan element name.
Pick the word with highest confidence match. If not found, use even thirds of the scene duration.

---

## Step 4: Assign Components Per Scene

For each classified scene, apply this assignment matrix:

### narration-primary
- **KineticCaption**: YES
  - `combineMs`: default 800. If scene WPM > 170 (fast speaker): use 600. If WPM < 130: use 1000.
  - `accentColor`: use `COLORS.accent` (read from the colors.ts if it exists, else '#FFD700')
  - `audioOffset`: use AUDIO_OFFSET from timing.ts
- **ColorShift**: YES — `interval={600}`
- **FitHeadline**: YES only if scene opens with a short punchy stat (word count of opening phrase < 8 words)
- **FloatingCallout**: CONSIDER if script has a technical term being defined for first time

### diagram
- **Diagram Library**: ALWAYS recommend a shared diagram component from `src/shared/components/diagrams/`:
  - Multi-stage process/pipeline → `InfographicFlow` (preferred, enterprise-grade)
  - Chronological events → `Timeline`
  - Big numbers/KPIs → `StatCardRow`
  - Feature/capability grid → `FeatureGrid`
  - Iterative loops → `ProcessCycle`
  - Tweets/announcements → `QuoteCard`
  - Hub + connected nodes → `HubAndSpoke` (from `src/shared/components/`)
  - Simple pipeline → `FlowDiagram` (from `src/shared/components/`)
  - Stacked layers → `LayeredArchitecture` (from `src/shared/components/`)
  - Before/after → `ComparisonDiagram` (from `src/shared/components/`)
  All use `lucide-react` icons and support `mode="light"` / `mode="dark"`.
- **KineticCaption**: NO (diagram drives visual, not word-by-word captions)
- **ColorShift**: YES — `interval={600}` (skip if using light-mode diagram component)
- **SpotlightFocus**: YES if 3+ elements (with frame ranges as computed in Step 3)
- **BlurReveal**: CONSIDER if plan mentions "reveal" or diagram appears all at once
- **FloatingCallout**: CONSIDER for the first element (definition variant)

### code
- **KineticCaption**: NO
- **ColorShift**: YES — `interval={600}`
- **REMINDER**: `whiteSpace: 'pre'` on all code containers
- **FitHeadline**: MAYBE for scene title if standalone

### stats
- **StatCardRow**: CONSIDER if 3-4 stats displayed together (from `src/shared/components/diagrams/`)
- **FitHeadline**: YES — for single hero number/stat
- **KineticCaption**: MAYBE for surrounding narration
- **ColorShift**: YES — `interval={600}`
- **ScreenShake**: CONSIDER at the frame the stat is revealed (for emphasis)

### list
- **KineticCaption**: MAYBE (depends on whether narration drives each item)
- **ColorShift**: YES — `interval={600}`
- **REMINDER**: Use `STAGGER = 8` from timing.ts for list item reveals
- **FitHeadline**: MAYBE for list title

### cta
- **KineticCaption**: NO
- **ColorShift**: NO (final scene should be clean)
- **FitHeadline**: YES for main CTA headline
- **REMINDER**: No open loop — ends with direct CTA

---

## Step 5: Compute Global Composition Elements

**MidVideoReHook:**
- `triggerFrame = Math.floor(TOTAL_FRAMES * 0.55)`
- `hookPhrase`: read from plan.md `midReHookPhrase` field. If not found, derive from script: find the scene at ~50-55% of total word count and extract its most impactful sentence.

**SlimProgressBar:**
- `startFrame`: first non-preview scene start (SCENE_STARTS.scene01 or equivalent)
- `color`: COLORS.accent if available

**ProgressDots:**
- `totalDots`: number of scenes excluding scene00preview
- `activeDotIndex`: computed in Composition.tsx from current frame vs SCENE_STARTS

---

## Step 6: Map Dead Zones to Scenes

For each dead zone from Step 2:
- Identify which scene it falls in (compare frame range to SCENE_STARTS)
- Add to that scene's strategy: "Dead zone at frames X–Y: add [component] at frame Z"
- Prefer ColorShift for body zones, GlitchInterrupt for fatigue zones

---

## Step 7: Write retention-strategy.md

Write `src/$ARGUMENTS/retention-strategy.md` using this exact structure:

```markdown
# Retention Strategy: {AnimationName}
<!-- Generated by retention-strategy-agent — DO NOT EDIT MANUALLY -->
<!-- Re-generate: spawn retention-strategy-agent {AnimationName} -->

## Global: Composition.tsx Elements

Add these to Composition.tsx as AbsoluteFill overlays (NOT in TransitionSeries):

```tsx
{/* Slim progress bar — starts after preview scene */}
<SlimProgressBar totalFrames={TOTAL_FRAMES} startFrame={SCENE_STARTS.scene01} color={COLORS.accent} />

{/* Progress dots — N scenes excluding preview */}
{/* Compute activeDot = Object.keys(SCENES).findIndex(k => frame < SCENE_STARTS[k] + SCENES[k].duration) */}
<ProgressDots totalDots={N} activeDotIndex={activeDot} dotColor={COLORS.accent} />

{/* Mid-video re-hook — at 55% mark */}
<MidVideoReHook
  hookPhrase="{midReHookPhrase}"
  triggerFrame={Math.floor(TOTAL_FRAMES * 0.55)}  {/* = {computed_frame} */}
/>
```

---

## Scene-by-Scene Prescriptions

### Scene00 (Preview) — TYPE: narration-primary
**SKIP ColorShift** — preview scenes use minimal styling.
**SKIP KineticCaption** — preview is short (~300 frames), use simple word highlighting.
**SKIP SlimProgressBar** — bar starts at scene01.

---

### SceneNN ({SceneName}) — TYPE: {type}

**Classification rationale**: {1-2 sentences explaining WHY this type was chosen based on plan content}

**Components to use:**

| Component | Use? | Props |
|---|---|---|
| KineticCaption | YES/NO | combineMs={N}, accentColor={COLORS.accent}, audioOffset={AUDIO_OFFSET} |
| ColorShift | YES/NO | interval={600} — wrap inner content div only |
| FitHeadline | YES/NO | text="{opening phrase}", maxWidth=1600, maxFontSize=96 |
| SpotlightFocus | YES/NO | active={frame >= triggerFrame && frame < nextTrigger} |
| BlurReveal | YES/NO | triggerFrame={N} |
| FloatingCallout | YES/NO | text="{term}", triggerFrame={N}, variant="definition" |
| ScreenShake | YES/NO | triggerFrame={N} |
| STAGGER | YES/NO | export const STAGGER = 8 in timing.ts |

**SpotlightFocus timing** (if applicable):
```tsx
// Element 1 active: wordToFrame({ts1}, AUDIO_OFFSET) → wordToFrame({ts2}, AUDIO_OFFSET)
// Element 2 active: wordToFrame({ts2}, AUDIO_OFFSET) → wordToFrame({ts3}, AUDIO_OFFSET)
// Element 3 active: wordToFrame({ts3}, AUDIO_OFFSET) → end of scene
const isEl1Active = frame >= wordToFrame({ts1}, AUDIO_OFFSET) && frame < wordToFrame({ts2}, AUDIO_OFFSET);
const isEl2Active = frame >= wordToFrame({ts2}, AUDIO_OFFSET) && frame < wordToFrame({ts3}, AUDIO_OFFSET);
const isEl3Active = frame >= wordToFrame({ts3}, AUDIO_OFFSET);
```

**Dead zone remediation** (if applicable):
- Frame {X}–{Y} ({gap}s gap): Add `<ColorShift interval={450}>` wrapper — this is shorter interval than scene default to act as the interrupt
  OR: Add `<GlitchInterrupt triggerFrame={midpoint} duration={12} />` at frame {midpoint}

**KineticCaption setup** (if applicable):
```tsx
import syncData from '../scripts/sceneNN-sync.json';
<KineticCaption
  syncData={syncData}
  audioOffset={AUDIO_OFFSET}
  accentColor={COLORS.accent}
  combineMs={N}
/>
```

---

## Summary Table

| Scene | Type | KineticCaption | SpotlightFocus | FitHeadline | Dead Zone Fix |
|---|---|---|---|---|---|
| Scene00 | preview | NO | NO | NO | — |
| SceneNN | {type} | YES/NO | YES/NO | YES/NO | {component or —} |

## Validation Checklist for phase4-scene-builder

After building each scene, verify:
- [ ] KineticCaption: present if type=narration-primary
- [ ] ColorShift: present on every non-preview scene
- [ ] FitHeadline: present if prescribed above
- [ ] SpotlightFocus: present with correct active conditions if prescribed
- [ ] Dead zone fix: applied if prescribed
- [ ] Global composition elements added to Composition.tsx
```

Fill in ALL placeholders with concrete values. Leave NO "{placeholder}" strings in the output.

---

## Step 8: Update Phase Status

Update `src/$ARGUMENTS/phase-status.md`:
- Set the `3.5 - Retention` row to `done {today's date}`
- If the row doesn't exist, add it between `3 - Audio` and `4 - Sync`

---

## Output to Caller

Return a brief summary:
```
Retention Strategy: {AnimationName}
Scenes analyzed: N
Scene types: X narration-primary, Y diagram, Z code, W stats, V list, U cta
Dead zones found: N (from audit)
Global elements: SlimProgressBar + ProgressDots + MidVideoReHook at frame {F}
Strategy written to: src/{AnimationName}/retention-strategy.md
```
