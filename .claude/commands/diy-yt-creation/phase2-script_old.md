---
description: "Phase 2: Write narration script for user review (raw, no TTS markup)"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 2 of the DIY YouTube Video Creation Workflow.
Write a high-retention narration script using the Kallaway Formula and present it for user review.

**Goal**: Write viral-quality narration using proven hook techniques and linguistic precision, then STOP for user review before any TTS optimization.
**Input**: `.agents/plans/<topic>-explainer.plan.md` (the plan from Phase 1)
**Output**: `src/$ARGUMENTS/scripts/full-script.md` (complete raw script for review)
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 2)
</objective>

<autonomous-mode>
## When Called from full-auto-v2

If this phase is invoked as part of the full-auto-v2 orchestration:
- **DO NOT STOP for user review** — proceed directly to Phase 2a
- Use PARAMS.tone for writing style
- Use PARAMS.technical_terms for pronunciation planning
- Use PARAMS.must_mention to ensure required points are covered

The script review checkpoint is skipped in autonomous mode.
</autonomous-mode>

<process>

## Step 1: Read the Plan & Research

Read the plan file from `.agents/plans/` and the content brief from `src/$ARGUMENTS/research/`.
Extract: scene list, durations, key messaging, tone, visual beats, hook architecture, and cult hopping references.

## Step 2: Calculate Word Targets

For each scene, calculate target word count at ~2.5 words/second:
- 10s scene → ~25 words
- 15s scene → ~37 words
- 20s scene → ~50 words
- 25s scene → ~62 words
- 30s scene → ~75 words

Leave ~2-3s of silence buffer per scene (audio starts after scene transition).

## Step 3: Write the Hook (Kallaway Formula)

The hook is the most critical part. Apply the **Three-Step Hook Formula**:

### Step 3a: Context Lean-In (First 4 Seconds)
Establish topic clarity immediately. The viewer must "self-select."
- Use a **mind-blowing fact** OR a **shared pain point**
- Create common ground with the target audience
- Example (Tech): "You're juggling scattered websites and messy documents."
- Example (General): "Finding a fact in a PDF feels like finding one grain of sand on a beach."

### Step 3b: Scroll-Stop Interjection (The Stun Gun)
Insert a contrasting transition word to halt momentum mid-thought:
- **Primary Stun Guns**: "But," "However," "Yet," "Although"
- This is a stop sign in the middle of a sentence
- Example: "...scattered documents. **But** imagine if..."

### Step 3c: Contrarian Snapback (The Uno Reverse)
Snap the viewer onto an unexpected path:
- If you started praising something, reveal it's actually the least impressive part
- Create the "Hook, Line, and Sinker" effect
- Example: "...But this isn't just another search engine — it's an automated knowledge base that reads everything for you."

## Step 3b: Write the Preview Hook Script (MANDATORY)

Before writing Scene01 (main hook), write the Scene00Preview script. This "In this video..." preview is proven to increase watch time by 32%.

### Preview Hook Formula

**Duration:** 10-15 seconds (~25-37 words at 2.5 words/sec)
**Pacing:** 1.15x normal speed (use `--preview` flag for TTS)
**Energy:** HIGH — this is the attention grab that earns the right to continue

### Structure (Mandatory Elements)

1. **Attention Grab (2-3 words, ~1s):** Bold opening statement — a mind-blowing fact or pattern interrupt
   - "85% of developers..."
   - "One command..."
   - "Three minutes..."
   - Large number, shocking stat, or counterintuitive claim

2. **Teaser Phrases (3-4 phrases, 4-6 words each, ~6-8s):**
   - Quick mentions of key features/outcomes from upcoming scenes
   - NO explanation, just intrigue — create "open loops"
   - Each teaser should reference a specific visual that will appear later
   - Example: "Automated testing. Real-time suggestions. Zero config."

3. **Promise Statement (8-12 words, ~3s):**
   - "In this video, I'll show you exactly how..."
   - "Let me show you the [X] that changed everything..."
   - "Here's what nobody tells you about..."
   - Specific value proposition that ties the teasers together

### Example Preview Script (10 seconds, ~25 words)

```
55% faster — that's the difference.
Copilot. Claude. Gemini. Which AI actually delivers?
Real-world testing secrets. The future of coding.
Let's dive in.
```

### Preview Script Template

```markdown
## Scene 00 Preview

[Bold stat or statement — 2-4 words]
[Teaser 1 — 4-6 words referencing Scene 03-04 visual]
[Teaser 2 — 4-6 words referencing Scene 05-06 visual]
[Teaser 3 — 4-6 words referencing final feature visual]
[Promise statement — 8-12 words]
```

### TTS Optimization for Preview

- Use faster speed (1.15x via `--preview` flag) for energetic pacing
- Minimal pauses between phrases — keep momentum high
- Energy should be HIGH — this is the attention grab
- Short sentences only — no complex clauses
- Write the file as `scene-00-preview.txt` (follows naming convention)

## Step 4: Write the Full Script

Write the complete narration as one flowing document, applying these techniques:

### Benefit-Led Scripting
Viewers care about their problems, not your features:
- **Mediocre (Feature-led)**: "Magnesium is a core mineral."
- **Viral (Benefit-led)**: "If you want better sleep, you need magnesium."

For each feature scene, ask: "What problem does this solve for the viewer?"

### Cult Hopping Strategy
Wrap unknown ideas in known layers:
- Reference established brands or celebrities for subconscious comfort
- Example: "Like Taylor Swift's financial advisor..." makes tax planning feel familiar
- Draft off existing credibility to accelerate trust

### The Distillation Technique ("Say It Twice")
Maximize comprehension by providing two "cracks" at the point:
1. **The Expert Line**: Use technical language. ("SpaceX caught the Starship in the Mechazilla.")
2. **The 5-Year-Old Line**: Use a metaphor. ("It's like metal chopsticks catching a 23-story building.")

### Linguistic Precision (Rhythm & Cadence)

**The Staccato Rule**: Short, punchy sentences for hooks. High value density per word.

**The Boxer's Rhythm**: Vary your "punches."
- Three "Jabs" (short sentences) → One "Overhand" (longer contextual sentence)
- Example: "It's fast. It's precise. It never forgets. And it integrates with everything you already use."

**Pop-Pop-B Pattern (Three-Item Lists)**:
- Two short "Pops" + One longer contextual "B"
- Example: "The energy you bring, the charisma you show, and the rhythm of how you speak."

**The Jagged Edge Test**:
- Audit the script visually — if the right margin is a straight line, it's monotonous
- You need variety in sentence length creating a "jagged edge"

**Down-Energy Syllables**:
- End sentences on hard "down" notes to signal completion
- Avoid upspeak patterns that sound uncertain

### Tone Guidelines (from plan)
- **tech-influencer**: Short punchy sentences. Rhetorical questions. Confident swagger.
- **professional-corporate**: Clear, authoritative. No slang. Trust through precision.
- **friendly-educational**: Conversational. "Let me show you..." Warm and approachable.
- **dramatic-cinematic**: Building tension. Strategic pauses. Cinematic reveals.

## Step 5: Create Full Script for Review

Save the complete script to `src/$ARGUMENTS/scripts/full-script.md` as **plain narration text only**.

```markdown
# [Video Title]

## Scene 1: [Name]

[Plain narration text for this scene. No word counts, no annotations, no TTS markup. Just the words the narrator will speak.]

## Scene 2: [Name]

[Plain narration text...]

## Scene 3: [Name]

[Plain narration text...]
```

**IMPORTANT**:
- Write ONLY the narration text — no metadata, no word counts, no checklists
- Plain, human-readable form — no TTS optimizations yet (no pronunciation fixes, no break tags)
- Keep scene headers simple: just `## Scene N: [Name]`
- This is what the user will review and edit directly

</process>

<output>
**File created**: `src/$ARGUMENTS/scripts/full-script.md`

**STOP HERE — User Review Required**

Tell the user:
> "Script created: `src/$ARGUMENTS/scripts/full-script.md`
>
> Please review and edit the script directly in that file. When you're satisfied, run:
> `/diy-yt-creation:phase2a-script $ARGUMENTS`
>
> Phase 2a will apply TTS optimization and split into scene files for audio generation."

Do NOT:
- Proceed to TTS optimization
- Create scene files
- Present detailed quality assessments or checklists

Just create the plain script file and stop.
</output>

<quality-checklist>
## Immediate Authority Checklist (from viral hook research)

Before presenting the script, verify:

1. [ ] **Benefit First**: Did I lead with a pain point solve?
2. [ ] **Cult Hop**: Did I anchor the niche in a known reference?
3. [ ] **Value Compression**: Is there a unique "value hit" before the 4-second mark?
4. [ ] **Clarity Check**: Is the message distilled to its atomic unit?
5. [ ] **Stun Gun**: Does the hook contain a "But/However/Yet" interjection?
6. [ ] **Uno Reverse**: Does the hook snap to an unexpected path?
7. [ ] **Jagged Edge**: Do sentence lengths vary visibly?
8. [ ] **Say It Twice**: Are complex concepts explained both technically and simply?
</quality-checklist>
