---
description: "Generate custom background music for a video using ElevenLabs Music API"
argument-hint: <AnimationName> [--prompt "..."] [--no-update] [--dry-run]
---

<objective>
Generate a unique, topic-appropriate instrumental background music track for "$ARGUMENTS" using the ElevenLabs Music API.

This is a **standalone optional skill** — not part of the full-auto pipeline. Run it after Phase 3 (audio) or Phase 4 (sync) to replace the generic shared background track with a custom one.

**Output**: `public/audio/<animationname>/bg-music.mp3` + optional Composition.tsx patch
</objective>

<process>

## Step 1: Verify Prerequisites

Check that:
1. `ELEVENLABS_API_KEY` is set in `.env`
2. `src/$ARGUMENTS/` exists (composition directory)
3. `src/$ARGUMENTS/constants/timing.ts` exists (for auto-detecting duration)

If timing.ts is missing, inform the user they need to provide `--duration <seconds>`.

## Step 2: Preview with Dry Run

Run a dry run first to verify auto-detected settings:

```bash
python generate-bg-music.py $ARGUMENTS --dry-run
```

This shows:
- Auto-detected duration from timing.ts
- Auto-generated music prompt from content-brief.md tone mapping
- Output file path

Review the prompt. If the auto-generated prompt doesn't match the video's mood, suggest a `--prompt` override.

## Step 3: Generate Background Music

Run the generation:

```bash
python generate-bg-music.py $ARGUMENTS
```

Or with custom options:
```bash
python generate-bg-music.py $ARGUMENTS --prompt "lo-fi ambient, soft piano, warm and educational"
python generate-bg-music.py $ARGUMENTS --duration 180
python generate-bg-music.py $ARGUMENTS --no-update  # skip Composition.tsx patch
```

## Step 4: Verify Output

1. Confirm `public/audio/<animationname>/bg-music.mp3` was created
2. If Composition.tsx was patched, verify the audio path was updated correctly
3. If the video is longer than 10 minutes, remind the user to add `loop` prop:
   ```tsx
   <Audio src={staticFile('audio/<name>/bg-music.mp3')} volume={0.08} loop />
   ```

## Step 5: Volume Tuning Guidance

Inform the user about volume adjustment:
- Default: `volume={0.04}` (subtle background)
- Range: `0.02` (barely perceptible) to `0.06` (clearly audible)
- Preview in Remotion Studio (`pnpm dev`) and adjust to taste
- Music must NEVER compete with narration — start low (0.03-0.04) and increase only if needed
- If the track still feels distracting at 0.03, regenerate with `--prompt` adding "extremely sparse, no rhythm, no melody"

</process>

<output>
**Files created/updated**:
- `public/audio/<animationname>/bg-music.mp3` (generated music track)
- `src/$ARGUMENTS/Composition.tsx` (patched audio path, unless `--no-update`)

**Report to user**:
1. Music generation summary (duration, prompt used)
2. Composition.tsx patch status
3. Volume tuning guidance
4. Loop prop reminder if video > 10 min
</output>
