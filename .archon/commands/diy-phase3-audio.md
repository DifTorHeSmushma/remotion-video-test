---
description: "Phase 3: Generate per-scene audio files with word-level sync timestamps"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 3 of the DIY YouTube Video Creation Workflow.
Generate ElevenLabs TTS audio for all scenes of "$ARGUMENTS" with word-level sync JSON for frame-accurate animation alignment.

**Goal**: Produce .mp3 audio clips and .json word timestamps for each scene.
**Input**: `src/$ARGUMENTS/scripts/scene-NN-<name>.txt` (from Phase 2)
**Output**:
  - `public/audio/<lowercase-name>/sceneNN.mp3` (merged audio, what the composition plays)
  - `public/audio/<lowercase-name>/sceneNN-chunks/chunk-NN.mp3` (per-sentence chunks for delta regen)
  - `src/$ARGUMENTS/scripts/sceneNN-sync.json` (word timestamps — scenes import this)
  - `src/$ARGUMENTS/scripts/sceneNN-history.json` (chunk metadata + checksums for `regen-changed.py`)
  - Updated `src/$ARGUMENTS/constants/timing.ts` (scene durations from audio)
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 3)
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 2b (Fact Check) is `done`. If Phase 2b does not exist in phase-status.md (older compositions), verify Phase 2a (TTS Script) is `done` instead.
  - If Phase 2b is `blocked`: STOP and report "Phase 2b (Fact Check) is blocked. Fix the failing claims and re-run `/diy-yt-creation:phase2b-factcheck $ARGUMENTS` first."
  - If Phase 2b is `pending`: STOP and report "Phase 2b (Fact Check) has not been completed. Run `/diy-yt-creation:phase2b-factcheck $ARGUMENTS` first."
- **Re-run check**: If Phase 3 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Verify Prerequisites

Check that:
1. `.env` file exists with `ELEVENLABS_API_KEY` and `VOICE_ID`
2. Python packages installed: `elevenlabs`, `python-dotenv`
3. Script files exist in `src/$ARGUMENTS/scripts/scene-*.txt`
4. At least one script file is non-empty
5. **Preview script exists**: `src/$ARGUMENTS/scripts/scene-00-preview.txt` (MANDATORY)

If missing, instruct the user on what to set up.

## Step 1b: Generate Preview Hook Audio (MANDATORY - Run First)

Generate preview audio BEFORE main scene audio. The preview uses energetic pacing:

```bash
python text-to-speech.py \
  --input src/$ARGUMENTS/scripts/scene-00-preview.txt \
  --output-dir public/audio/<animation-name>/ \
  --sync-dir src/$ARGUMENTS/scripts/ \
  --name scene00 \
  --preview \
  --chunk sentence
```

The `--preview` flag uses `ELEVENLABS_SPEED_PREVIEW` from .env (default 1.15) for faster, more energetic delivery. This pacing matches the rapid visual changes in preview hooks.

The `--chunk sentence` flag splits the script into sentence-sized chunks before generation. This writes per-sentence MP3s to `sceneNN-chunks/` and a `sceneNN-history.json` alongside the sync file. Later script edits can be re-rendered via `regen-changed.py` at ~5-10% of the cost of a full re-generation. See Step 7 below.

**Preview Audio Guidelines:**
- Target duration: 10-15 seconds (~300-450 frames at 30fps)
- Listen for energy level — should sound excited, not rushed
- Verify word timestamps in `scene00-sync.json` for rapid visual sync

## Step 2: Generate Audio (Batch)

Run the batch generation script with chunked mode and parallel API calls:
```bash
python generate-all-audio.py $ARGUMENTS --parallel 5 --chunk sentence
```

- `--chunk sentence` splits each scene into sentence-sized chunks before generation. Writes per-sentence MP3s to `public/audio/<name>/sceneNN-chunks/` and a `sceneNN-history.json` sync-directory alongside `sceneNN-sync.json`. Required for Step 7 (delta regen).
- `--parallel 5` runs 5 concurrent ElevenLabs API calls (Pro tier supports up to 10; 5 is safe default). Inside each scene, chunks still run sequentially — total concurrent API calls equal `--parallel`, regardless of chunk count. Free/Starter tiers should use `--parallel 1`.

This processes each `scene-NN-<name>.txt` and produces:
- `public/audio/<animation-name>/sceneNN.mp3` (merged audio, what scenes play)
- `public/audio/<animation-name>/sceneNN-chunks/chunk-NN.mp3` (per-sentence chunks)
- `src/$ARGUMENTS/scripts/sceneNN-sync.json` (merged word timestamps)
- `src/$ARGUMENTS/scripts/sceneNN-history.json` (chunk checksums for delta regen)

**Alternative** (single scene at a time):
```bash
python text-to-speech.py \
  --input src/$ARGUMENTS/scripts/scene-NN-<name>.txt \
  --output-dir public/audio/<animation-name>/ \
  --sync-dir src/$ARGUMENTS/scripts/ \
  --name sceneNN \
  --chunk sentence
```

**Opt-out** (legacy single-call mode): omit `--chunk sentence` to generate as one API call per scene. This is faster (1 call vs ~10 per scene) but loses the ability to do delta regen on edits.

## Step 3: Calculate Timing

For each scene, compute duration from the generated audio:

```
audio_offset = 30 frames (scene 1) or 20 frames (scenes 2+)
audio_duration_frames = ceil(last_word.end * 30)
scene_duration = audio_offset + audio_duration_frames + 30 (buffer)
```

Each scene's start frame = previous scene's start + previous scene's duration.

## Step 4: Update timing.ts

Write/update `src/$ARGUMENTS/constants/timing.ts`:

```typescript
export const FPS = 30;

export const AUDIO_OFFSET_FIRST = 30; // frames before scene 1 audio
export const AUDIO_OFFSET_REST = 20;  // frames before scenes 2+ audio
export const BUFFER_FRAMES = 30;      // padding after audio ends

export const SCENES = {
  <name1>: { start: 0, duration: <calculated> },
  <name2>: { start: <prev_end>, duration: <calculated> },
  // ...
} as const;

export const TRANSITION_DURATION = 15; // frames

// MANDATORY: Outro sequence (from shared component)
export const OUTRO_DURATION = 240; // 8 seconds at 30fps

// Total frames MUST include outro
export const TOTAL_FRAMES = <sum_of_content_durations> + OUTRO_DURATION;
export const TOTAL_DURATION_SECONDS = TOTAL_FRAMES / FPS;
```

## Step 5: Update Composition Duration

Update the composition in `src/Root.tsx` to use the new `TOTAL_FRAMES` value:
```typescript
<Composition
  id="$ARGUMENTS"
  component={...}
  durationInFrames={TOTAL_FRAMES}
  ...
/>
```

## Step 6: Verify Sync JSON Structure

Each `sceneNN-sync.json` should contain:
```json
{
  "words": [
    { "word": "First", "start": 0.0, "end": 0.35 },
    { "word": "word", "start": 0.4, "end": 0.72 },
    ...
  ]
}
```

Check that:
- No words have `start: 0, end: 0` (indicates API issue)
- Words are in chronological order
- Last word's `end` time matches expected audio duration

## Step 7: Re-generating After Script Edits (Delta Regen)

When the user edits a `scene-NN-*.txt` file AFTER Phase 3 has run with `--chunk sentence`, only re-generate the chunks whose text actually changed — never re-run `generate-all-audio.py` for a one-sentence fix.

```bash
# Preview the plan (no API calls, no file changes)
python regen-changed.py $ARGUMENTS --dry-run

# Execute — only changed chunks hit ElevenLabs
python regen-changed.py $ARGUMENTS

# Single scene only
python regen-changed.py $ARGUMENTS --scene 02

# Force full regen of every chunk (rarely needed — voice param change, model upgrade)
python regen-changed.py $ARGUMENTS --force
```

Matching is content-based (SHA-256 of whitespace-normalized chunk text), not index-based. That means inserting a new sentence in the middle of a scene causes only the new sentence to be generated — chunks BEFORE and AFTER it are recognized by checksum and reused verbatim. Typical edit cost: **~5-10% of a full scene regen**.

**When regen-changed.py is NOT usable:**
- Scene has no `sceneNN-history.json` (generated with `--chunk none`, or before chunked mode existed) → run `generate-all-audio.py $ARGUMENTS --chunk sentence` once to migrate.
- Voice or model params changed → use `--force` to re-generate everything at the new params.

After regen, `sceneNN.mp3` and `sceneNN-sync.json` are rewritten in place. Scene components and `Composition.tsx` need no changes — they import the same filenames.

**If narration duration changed significantly** (e.g., you added two sentences), re-run the Phase 3 timing step: the scene's total frames, subsequent scene starts, and `TOTAL_FRAMES` must be recomputed in `timing.ts` and `Root.tsx`. For small word-level edits within the same number of sentences, timing is usually unchanged enough to skip.

</process>

<output>
**Files created/updated**:
- `public/audio/<name>/scene01.mp3` through `sceneNN.mp3`
- `src/$ARGUMENTS/scripts/scene01-sync.json` through `sceneNN-sync.json`
- `src/$ARGUMENTS/constants/timing.ts`
- `src/Root.tsx` (composition duration)

**Report to user**:
1. Table: Scene | Audio Duration | Scene Frames | Word Count
2. Total video duration in seconds
3. Any audio generation errors or warnings
4. Instruction: Listen to each .mp3 to verify pronunciation and pacing
5. Next step: After audio approval, run `/diy-yt-creation/phase4-sync $ARGUMENTS`

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `3 - Audio` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>
