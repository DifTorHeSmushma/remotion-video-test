# /sixty-seconds — 60-Second Explainer Video

**ARGUMENT HINT**: `<TopicName (PascalCase, e.g. TokenMisconceptions)>`

<objective>
Create a complete 60-second (1800-frame) explainer video from a 3-bullet content brief.
Structure: hook (10s, 300 frames) + explanation (35s, 1050 frames) + CTA (15s, 450 frames).
</objective>

<process>
## Step 1: Parse Content Brief

Ask the user for three bullets:
- **hook**: One provocative sentence (the "wait, what?" moment)
- **core**: The explanation in 1-3 key points (each gets ~12 seconds)
- **cta**: The call-to-action and next video tease

## Step 2: Write TTS Scripts

Target word counts at 2.5 words per second:
- Hook (10s): ~25 words → `src/SixtySeconds/$ARGUMENTS/scripts/scene-01-hook.txt`
- Explain (35s): ~87 words → `src/SixtySeconds/$ARGUMENTS/scripts/scene-02-explain.txt`
- CTA (15s): ~37 words → `src/SixtySeconds/$ARGUMENTS/scripts/scene-03-cta.txt`

Also write `src/SixtySeconds/$ARGUMENTS/scripts/full-script.md` combining all three.

## Step 3: Generate Audio

```bash
python text-to-speech.py -i src/SixtySeconds/$ARGUMENTS/scripts/scene-01-hook.txt -o public/audio/sixty-seconds/${ARGUMENTS_LOWER}/ -s src/SixtySeconds/$ARGUMENTS/scripts/ -n scene01
python text-to-speech.py -i src/SixtySeconds/$ARGUMENTS/scripts/scene-02-explain.txt -o public/audio/sixty-seconds/${ARGUMENTS_LOWER}/ -s src/SixtySeconds/$ARGUMENTS/scripts/ -n scene02
python text-to-speech.py -i src/SixtySeconds/$ARGUMENTS/scripts/scene-03-cta.txt -o public/audio/sixty-seconds/${ARGUMENTS_LOWER}/ -s src/SixtySeconds/$ARGUMENTS/scripts/ -n scene03
```

## Step 4: Scaffold Composition

Create `src/SixtySeconds/$ARGUMENTS/` with:
- `Composition.tsx` — Uses TransitionSeries with SixtySecondsHook, SixtySecondsExplain, SixtySecondsCTA
- `constants/timing.ts` — SCENES with durations, AUDIO_OFFSETs, TRANSITION_DURATION=15, TOTAL_FRAMES=1800

**Duration enforcement**: `calculateMetadata` returns exactly `{ durationInFrames: 1800 }`.
If total audio duration exceeds 60s, warn the user to trim the script.

**IMPORTANT**: `durationInFrames` uses `SCENES.X.duration` with NO `+ TRANSITION_DURATION` (scene durations already include the transition overlap).

## Step 5: Register in Root.tsx

Add the new composition to `src/Root.tsx`.

## Step 6: QA and Render

1. Run `pnpm lint` to verify no TypeScript errors
2. Render QA still at phase boundary frames:
   ```bash
   pnpm exec remotion still SixtySeconds-$ARGUMENTS out/sixty-seconds/qa-frame30.png --frame=30
   ```
3. Only render full video when user explicitly requests it
</process>

<output>
- `src/SixtySeconds/$ARGUMENTS/` — Complete composition
- `public/audio/sixty-seconds/${ARGUMENTS_LOWER}/` — Audio files with sync JSON
- Composition registered in `src/Root.tsx`
</output>
