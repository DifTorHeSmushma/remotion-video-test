---
description: "Phase 2a: Apply TTS optimization and split approved script into scene files"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 2a of the DIY YouTube Video Creation Workflow.
Take the user-approved raw script and apply ElevenLabs TTS optimization, then split into per-scene files.

**Goal**: Transform the reviewed raw script into TTS-optimized scene files ready for audio generation.
**Input**: `src/$ARGUMENTS/scripts/full-script.md` (user-reviewed raw script from Phase 2)
**Output**: `src/$ARGUMENTS/scripts/scene-NN-<name>.txt` (TTS-optimized per-scene files)
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 2a)
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 2.5 (Critique) is `done` (not `blocked` or `pending`).
  - If `blocked`: STOP and report "Phase 2.5 (Critique) is blocked. Fix the script issues and re-run `/diy-yt-creation:phase2-5-critique $ARGUMENTS` first."
  - If `pending`: STOP and report "Phase 2.5 (Critique) has not been completed. Run `/diy-yt-creation:phase2-5-critique $ARGUMENTS` first."
- **Re-run check**: If Phase 2a is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Read the Approved Script

Read the user-reviewed script from `src/$ARGUMENTS/scripts/full-script.md`.
Confirm with user: "I see the script in full-script.md. Has it been reviewed and approved for TTS processing?"

If user has not reviewed it yet, tell them to run `/diy-yt-creation:phase2-script $ARGUMENTS` first.

## Step 2: Apply ElevenLabs Optimization via Skill

**MANDATORY**: Invoke the `elevenlabs-tts-optimizer` skill using the Skill tool to optimize the script.

**How to invoke**: Use the Skill tool with `skill: "elevenlabs-tts-optimizer"` and pass the approved script content.

**If the skill fails**, fall back to these manual rules and inform the user:

### Pronunciation Fixes
- **Acronyms** (letter-by-letter): `API` → `A P I`, `CLI` → `C L I`, `SSH` → `S S H`, `IDE` → `I D E`, `CI/CD` → `C I C D`
- **DO NOT spell out**: `AI` (ElevenLabs pronounces it naturally), `OK` → `okay`
- **Technical terms**: `nginx` → `engine-x`, `kubectl` → `cube-C T L`, `jq` → `jay-queue`, `cgroups` → `see-groups`, `npm` → `N P M`
- **Brands**: Keep as-is unless commonly mispronounced

### Pause Control
- Use `<break time="0.5s" />` between major ideas (sparingly — max 2-3 per scene)
- Use ellipses `...` for dramatic pauses
- Use em-dashes `—` for natural mid-sentence pauses
- Period + new sentence for full stops

### Quality Rules
- Keep each scene script under 800 characters
- No curly braces `{}`, angle brackets `<>` (except break tags), or square brackets `[]`
- Write numbers as words: `100` → `one hundred`
- Expand symbols: `$` → `dollars`, `%` → `percent`, `@` → `at`

## Step 3: Split to Scene Files

Create individual scene files in `src/$ARGUMENTS/scripts/`:

```
src/$ARGUMENTS/scripts/
├── full-script.md          (kept for reference — original reviewed version)
├── scene-01-<name>.txt     (TTS-optimized)
├── scene-02-<name>.txt     (TTS-optimized)
└── scene-NN-<name>.txt     (TTS-optimized)
```

Use kebab-case names matching the scene purpose (hook, solution, features, cta, etc.)

## Step 4: Final Verification

For each scene script, verify:
- Word count within ±10% of target
- No sentence exceeds 20 words (hard to follow in audio)
- Technical terms are pronunciation-safe
- Break tags used sparingly (max 2-3 per scene)
- Each scene under 800 characters

</process>

<output>
**Files created**: `src/$ARGUMENTS/scripts/scene-NN-<name>.txt`

**Report to user**:
1. Confirm that `elevenlabs-tts-optimizer` skill was invoked (or note if fallback was used)
2. Table: Scene | Name | Word Count | Target | Duration
3. List of TTS transformations applied (pronunciation fixes, pause insertions)
4. Any concerns flagged (long sentences, missing pause points)
5. Next step: Run `/diy-yt-creation:phase3-audio $ARGUMENTS`

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `2a - TTS Script` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>
