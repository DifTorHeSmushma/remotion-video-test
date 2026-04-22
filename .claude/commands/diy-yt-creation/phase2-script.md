---
description: "Phase 2: Write narration script for user review (raw, no TTS markup)"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 2 of the DIY YouTube Video Creation Workflow.
Write a high-retention narration script using the Kallaway Formula and present it for user review.

**Goal**: Write viral-quality narration using proven hook techniques and linguistic precision, then STOP for user review before any TTS optimization.
**Input**: Plan file from Phase 1 (see Plan File Discovery below)
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

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 1 (Plan) is `done`.
  - If not: STOP and report "Phase 1 (Plan) has not been completed. Run `/diy-yt-creation:phase1-plan $ARGUMENTS` first."
- **Re-run check**: If Phase 2 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Read the Plan & Research

### Plan File Discovery

Locate the plan file using this priority:
1. `.agents/plans/$ARGUMENTS.plan.md` (direct match by AnimationName)
2. If not found, glob `.agents/plans/*.plan.md` and find the file whose kebab-case name
   best matches $ARGUMENTS split on PascalCase boundaries
   (e.g., `ClaudeCodeDesktop` -> look for a file containing `claude-code-desktop`)
3. If still not found, STOP and ask the user for the plan file path. Do NOT proceed without a plan.

Store the resolved path as `PLAN_FILE` for all subsequent references.

Read `PLAN_FILE` and the content brief from `src/$ARGUMENTS/research/`.
Extract: scene list, durations, key messaging, tone, visual beats, hook architecture, and cult hopping references.

### Selected Hook Variant

Before writing, confirm which hook variant was selected in Phase 1:
- Read `PLAN_FILE` -> Hook Variants section
- In **interactive mode**: If the user has not selected a variant, show all three variants and ask them to choose before proceeding
- In **autonomous mode** (full-auto-v2): Use the highest-scoring variant automatically

The selected hook variant's opening line becomes the **mandatory first sentence** of Scene 01.
Do not improvise a different hook — the variant was scored and selected for a reason.

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
- For feature/tutorial videos: **Name the feature and its benefit immediately**
- For problem/analysis videos: Use a **mind-blowing fact** OR a **shared pain point**
- Create common ground with the target audience
- DO NOT default to shame framing ("Most developers don't know...") — your audience already uses the tool
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

1. **Attention Grab (2-3 words, ~1s):** Bold opening that validates the click
   - For feature/tutorial videos: **Name the feature** — "Skills system.", "Print mode.", "Worktrees."
   - For analysis/problem videos: Bold stat or shocking statement — "85% of developers..."
   - DO NOT default to stats for feature videos — your audience clicked for the feature, show it

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

## Step 3c: Consult the Scriptwriting Playbook

Before writing the full script, review the banned phrases and voice guidelines in:
`.claude/research/faceless-tech-scriptwriting-playbook.md`

Key sections to reference during writing:
- **§4 (Writing Voice for TTS)**: Gary Provost rhythm, Golf Buddy tone, TTS-specific rules
- **§5 (Transitions)**: Use these instead of defaulting to "But here's the thing" or "Let me show you"
- **§11 (Banned Patterns)**: Critical/High phrases that will cause QG-5 failure in Phase 2.5
- **§2 (Script Structure)**: Use But/Therefore chains, not "And then" sequences

Do NOT use any phrase from the §11 Critical list. QG-5 will block the script if found.

## Step 3d: Scars Mining (Credibility Signal)

Before writing, identify **1-2 experience signals** for this topic — specific friction points, failure modes, or time traps that a practitioner would know but ChatGPT cannot replicate.

Run the **Commodity Test**: "Can a viewer get the core answer from ChatGPT in 10 seconds?" If YES, the script needs repositioning to the experience layer before writing begins.

For each major scene, ask:
- What is the most common mistake a developer makes when first encountering this?
- What does the documentation skip that causes real failures in practice?
- What took days to figure out that can be compressed into one sentence here?

Write the answers as 1-2 sentences each. These become the **scar inserts** — woven into scene narration to replace purely informational passages.

**Scar insert patterns:**
- "The docs skip this — if you [X] before [Y], it silently fails."
- "Took me three weeks to realize: [specific technical gotcha]."
- "Almost every team makes this mistake on first setup: [specific error]."

At least 1 scar must appear somewhere in the final script. Phase 2.5 will check for its presence.

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

## Step 4b: Apply Story Locks (Enhancement Pass)

After writing the full script, review it through the lens of the **6 Story Locks** (see `.claude/references/story-locks.md` for full details). This is an enhancement pass — the core script should already be solid.

1. **Term Branding**: Identify 1–2 core concepts → give them a memorable name (short, vivid, 2–3 words)
2. **Embedded Truths**: Search for hedging words (`if`, `maybe`, `might`, `could`, `probably`) → replace with certainty framing (`when`, `the reason`, `once you`, `this is how`)
3. **Thought Narration**: Add 1–2 moments where you narrate the viewer's likely thought, at major transition points ("You're probably thinking: *'...'*")
4. **Negative Frames**: Consider negative-framing at least one key point — flip "here's how to do X" into "stop doing X wrong" (the Negative Flip)
5. **Loop Openers**: Add re-engagement phrases between major sections ("But that's not even the most interesting part", "Here's where it gets crazy")
6. **Contrast Words**: Ensure key pivot sentences use A→but→B structure — vary the contrast word (but, actually, instead, turns out, except)

**Note**: Don't force every lock into every script. Short scripts (15–30s) may only use Embedded Truths + Contrast Words. The goal is natural integration, not a checklist quota.

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
> Please review and edit the script directly in that file. When you are satisfied with the content, run the quality gate:
> `/diy-yt-creation:phase2-5-critique $ARGUMENTS`
>
> Phase 2.5 runs a four-pass LLM critique (Hook Strength, Retention Curve, TTS Readability, Story Arc) and gates access to Phase 2a. Only scripts that score >= 7/10 on Hook Strength and Story Arc will proceed to audio generation."

Do NOT:
- Proceed to TTS optimization
- Create scene files
- Present detailed quality assessments or checklists

Just create the plain script file and stop.

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `2 - Script` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>

<quality-checklist>
## Immediate Authority Checklist (from viral hook research)

Before presenting the script, verify:

0a. [ ] **Hook Variant Used**: Did I use the selected hook variant's opening line as written in the plan?
0b. [ ] **Open Loop Established**: Is the primary open loop (from plan's open_loop_architecture section) raised within the first 60 seconds?
0c. [ ] **Value Alignment**: Does the hook name the video's main feature/concept within the first sentence? For feature videos: "Print mode turns Claude into a Unix pipe" NOT "Most developers don't know about this hidden feature"
1. [ ] **Benefit First**: Did I lead with a pain point solve?
2. [ ] **Cult Hop**: Did I anchor the niche in a known reference?
3. [ ] **Value Compression**: Is there a unique "value hit" before the 4-second mark?
4. [ ] **Clarity Check**: Is the message distilled to its atomic unit?
5. [ ] **Stun Gun**: Does the hook contain a "But/However/Yet" interjection?
6. [ ] **Uno Reverse**: Does the hook snap to an unexpected path?
7. [ ] **Jagged Edge**: Do sentence lengths vary visibly?
8. [ ] **Say It Twice**: Are complex concepts explained both technically and simply?
9. [ ] **Term Branded**: Did I coin at least 1 named framework/concept?
10. [ ] **No Hedging**: Are "if/maybe/might/could" replaced with "when/the reason/once you"?
11. [ ] **Thought Narration**: Did I narrate the viewer's likely thought at least once?
12. [ ] **Negative Frame**: Is at least one point framed as a warning/mistake to avoid?
13. [ ] **Loop Openers**: Are there re-engagement phrases between major sections?
14. [ ] **Contrast Words**: Do key points use A→but→B structure?
</quality-checklist>

### Retention Structure Requirements (MANDATORY)

Every script must satisfy all of the following before proceeding to Phase 2a:

1. **Open Loop per Scene**: Each scene (except final CTA) ends with an open loop phrase
2. **Chapter Names as Curiosity Gaps**: Scene headers in full-script.md are curiosity gaps, not topic labels
3. **WPM in Range**: Each scene's word count ÷ duration = 150-165 WPM (mark deviations in header comments)
4. **Silence Cues**: High-impact reveal words preceded by `[PAUSE]` on its own line in .txt files
