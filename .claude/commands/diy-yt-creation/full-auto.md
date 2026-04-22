---
description: "Full auto: Run all phases (0-5) end-to-end without stopping for review"
argument-hint: <topic, product URL, or concept description> [--upload]
---

<objective>
Execute the ENTIRE DIY YouTube Video Creation Workflow in one shot — no human-in-the-loop pauses.
Run Phase 0 through Phase 5 autonomously for "$ARGUMENTS".

**Goal**: Go from concept to rendered .mp4 without stopping.
**Output**: `out/<AnimationName>/final.mp4` + all intermediate artifacts
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md`

IMPORTANT: Do NOT ask the user any questions. Make all decisions autonomously using sensible defaults. Do NOT stop between phases. Keep going until the final render is complete.
</objective>

<duration-detection>
FIRST, parse "$ARGUMENTS" to extract parameters. The input may be a structured brief (from the brief-template) or freeform text.

**If structured brief** (contains "**Topic**:", "**Duration**:", etc.):
- Extract all fields: Topic, Duration, Tone, Resolution, Links, Target Audience, Key Angle, Must-Mention Points, Technical Terms, Voice/Style Notes
- Use these values throughout all phases instead of defaults

**If freeform text**:
- Look for duration patterns like: "15s", "30s", "45s", "60s", "90s", "2min", "3min", "1 minute", "30 seconds", etc.

In both cases:
- If a duration is found → use that as TARGET_DURATION
- If NO duration is found → default to 15s (TARGET_DURATION = 15)

This TARGET_DURATION determines EVERYTHING: research depth, scene count, word count, and scope.

### Duration-to-Structure Mapping

| TARGET_DURATION | Scenes | Words Total | Research Depth | Structure |
|-----------------|--------|-------------|----------------|-----------|
| 15s             | 3      | ~37         | 1 key angle only | Hook → Core → CTA |
| 30s             | 4-5    | ~75         | 2-3 key points | Hook → Solution → Feature → CTA |
| 45s             | 5-6    | ~112        | 3-4 features | Hook → Solution → 2-3 Features → CTA |
| 60s             | 6-7    | ~150        | 4-5 features | Hook → Solution → 3-4 Features → Trust → CTA |
| 90s             | 7-8    | ~225        | 5-6 features | Hook → Solution → 4-5 Features → Trust → CTA |
| 3min            | 9-10   | ~450        | Full deep-dive | Hook → Solution → 5-7 Features → Ecosystem → Security → CTA |
| 5min            | 10-12  | ~750        | Comprehensive | Preview → Hook → Problem → Solution → 4-6 Deep Features → Example → Framework → Trust → CTA |
| 6min            | 10-12  | ~900        | Comprehensive | Preview → Hook → What Is It → Comparison → Key Decision → Real Example → Framework → CTA |
| 7min            | 12-14  | ~1050       | Full expertise | Preview → Hook → Problem → Solution → 5-8 Deep Features → Real Examples → Framework → Trust → CTA |
| 8min            | 14-16  | ~1200       | Full expertise | Preview → Hook → Problem → Solution → 6-10 Deep Features → Multiple Examples → Comparisons → Framework → Trust → CTA |
</duration-detection>

<defaults>
When decisions are needed, use these defaults (do NOT ask the user).
**Brief values OVERRIDE these defaults** — if the brief specifies Tone, Resolution, etc., use those instead:
- **Duration**: 6min (10-12 scenes) unless specified in brief or $ARGUMENTS
- **Tone**: tech-influencer-edgy (short punchy sentences, confident, rhetorical questions)
- **Resolution**: 1920x1080
- **FPS**: 30
- **Transitions**: Alternate between slide, fade, and wipe
- **Spring style**: Mix of snappy (UI elements) and smooth (text)
- **Audio offset**: 30 frames for scene 1, 20 frames for scenes 2+
- **Buffer**: 30 frames after audio ends
- **Outro**: 240 frames (8 seconds) — OutroSequence is MANDATORY
- **Background music**: audio/shared/bg-music.wav at volume 0.08 — MANDATORY
- **Voice**: Use VOICE_ID from .env or default "JBFqnCBsd6RMkjVDRZzb"
- **Codec**: h264, CRF 18
</defaults>

<process>

## Phase 0: Research (AUTO)

Research depth is proportional to TARGET_DURATION:

**15s (minimal)**: Find the ONE most compelling angle. Single value prop, single pain point. No feature deep-dive needed.
**30-45s (focused)**: Value prop + 2-3 supporting points. Brief competitive context.
**60s+ (standard)**: Full research — features, pain points, differentiators, proof points, competitors.

Steps:
1. If structured brief provided: fetch all **Links** URLs first, then supplement with web search if needed. If freeform: research "$ARGUMENTS" using web search and URL fetching.
2. Extract content proportional to TARGET_DURATION (see above)
3. Use **Key Angle** from brief if provided, otherwise determine the single best narrative angle
4. Include **Must-Mention Points** and **Technical Terms** from brief in the content-brief
5. **Hook Architecture Research** (for Kallaway Formula):
   - Identify cult hopping opportunities (known brands/celebrities that can anchor the topic)
   - Define common ground for target audience (shared pain points, relatable metaphors)
   - Find contrarian angles (counterintuitive insights, "Uno Reverse" opportunities)
   - Collect mind-blowing facts (shocking statistics for scroll-stop effect)
6. Create `src/<AnimationName>/research/content-brief.md`
7. Derive `<AnimationName>` from the topic using PascalCase (e.g., "docker sandboxes" → "DockerSandboxes")
8. **Create phase status file**: Write `src/<AnimationName>/phase-status.md` with all phases as `pending` (see template below)

**Phase status template:**
```markdown
# Phase Status: <AnimationName>

| Phase | Status | Completed |
|-------|--------|-----------|
| 0 - Research | pending | |
| 1 - Plan | pending | |
| 2 - Script | pending | |
| 2.5 - Critique | pending | |
| 2a - TTS Script | pending | |
| 3 - Audio | pending | |
| 4 - Sync | pending | |
| 4b - Visual QA | pending | |
| 5 - Render | pending | |
| 6 - Shorts | pending | |
| 6 - Upload | pending | |
```

**Update phase status**: After EACH phase completes below, update `src/<AnimationName>/phase-status.md` — set that phase's row to `done` with today's date. If a phase fails, set to `blocked (<reason>)`.

Proceed immediately to Phase 1.

## Phase 1: Plan (AUTO)

1. Read the content brief just created
2. **MANDATORY**: Invoke the `remotion-best-practices` skill using the Skill tool (`skill: "remotion-best-practices"`) for animation patterns and constraints. Do NOT skip this.
3. Use the Duration-to-Structure Mapping table to determine scene count and structure:
   - 15s → 3 scenes: Hook (5s) → Core Message (6s) → CTA (4s)
   - 30s → 4-5 scenes: Hook (7s) → Solution (8s) → Feature (8s) → CTA (7s)
   - 45s → 5-6 scenes: Hook (8s) → Solution (10s) → 2-3 Features (8s each) → CTA (7s)
   - 60s → 6-7 scenes: Hook (10s) → Solution (12s) → 3-4 Features (9s each) → Trust (8s) → CTA (7s)
   - 90s+ → Use content density to determine (see duration table)
4. Structure scenes according to TARGET_DURATION pattern
5. Define color palette based on the product/topic branding
6. Define component inventory (fewer components for shorter videos)
7. Write plan to `.agents/plans/<AnimationName>.plan.md`

Proceed immediately to Phase 2.

## Phase 2: Script (AUTO)

1. Read the plan and content brief. If a structured brief was provided, also apply **Tone**, **Voice/Style Notes**, **Target Audience**, and **Technical Terms** (pronunciation) from it.

2. **Write the Hook using Kallaway Formula** (critical for retention):
   - **Context Lean-In**: Establish topic clarity in first 4 seconds with mind-blowing fact OR shared pain point
   - **Scroll-Stop Interjection**: Use "But," "However," or "Yet" as a stun gun mid-sentence
   - **Contrarian Snapback**: The "Uno Reverse" that snaps viewers onto unexpected path

3. **Apply High-Retention Scripting Techniques**:
   - **Benefit-Led**: Lead with problem solved, not feature described ("If you want X, you need Y")
   - **Cult Hopping**: Reference known brands/celebrities to anchor unknown concepts
   - **Distillation**: "Say it twice" — Expert line + 5-year-old metaphor for complex concepts
   - **Boxer's Rhythm**: 3 jabs (short sentences) + 1 overhand (longer context)
   - **Jagged Edge**: Vary sentence lengths (no monotonous straight right margin)

4. Write per-scene narration at ~2.5 words/second per scene duration:
   - 15s total → ~37 words across 3 scenes (~12 words each)
   - 30s total → ~75 words across 4-5 scenes
   - 60s total → ~150 words across 6-7 scenes
   - For short videos (15-30s): Every word must earn its place. Be punchy and direct.
   - For longer videos (60s+): Allow breathing room and explanatory detail.

5. **MANDATORY**: Invoke the `elevenlabs-tts-optimizer` skill using the Skill tool to optimize all scripts for eleven_multilingual_v2. Do NOT skip this — use `skill: "elevenlabs-tts-optimizer"` and apply its output. If the skill fails, fall back to manual rules and note the failure in the final report:
   - Acronyms letter-by-letter: API → A P I, CLI → C L I (but NOT "AI" — ElevenLabs handles it naturally)
   - Technical terms phonetically: nginx → engine-x, kubectl → cube-C T L
   - Numbers as words
   - Ellipses for dramatic pauses, em-dashes for mid-sentence pauses

6. Save full script to `src/<AnimationName>/scripts/full-script.md` for reference
7. Save per-scene to `src/<AnimationName>/scripts/scene-NN-<name>.txt`

Proceed immediately to Phase 3.

## Phase 3: Audio (AUTO)

1. Verify `.env` has ELEVENLABS_API_KEY
2. Run batch generation:
   ```bash
   python generate-all-audio.py <AnimationName> --parallel 5
   ```
3. If batch script fails, fall back to per-scene:
   ```bash
   python text-to-speech.py -i <script> -o <audio-dir> -s <sync-dir> -n <name>
   ```
   Run for each scene sequentially.
4. Read all generated sync JSON files
5. Calculate scene durations:
   ```
   scene_duration = audio_offset + ceil(last_word.end * 30) + 30
   ```
6. Write `src/<AnimationName>/constants/timing.ts` with calculated values:
   - Include `OUTRO_DURATION = 240` (8 seconds at 30fps)
   - `TOTAL_FRAMES` must include outro: `content_frames + OUTRO_DURATION`

Proceed immediately to Phase 3.2.

## Phase 3.2: Background Music (AUTO)

Generate multi-segment background music matched to the hook's cinematic pattern.

1. Read `cinematic_hook_blueprint.music_profile` from the plan file
2. Run: `python generate-bg-music.py <AnimationName> --multi-segment --hook-mood <mood> --hook-bpm <range> --body-bpm 75-90 --cta-bpm 110-120`
3. Outputs: `bg-music-hook.mp3`, `bg-music-body.mp3`, `bg-music-cta.mp3`, `bg-music-metadata.json`

If no blueprint exists, use defaults: `--hook-mood dramatic-cinematic --hook-bpm 100-110`

Proceed immediately to Phase 4.

## Phase 4: Sync (AUTO)

1. Create constants: colors.ts, fonts.ts, springs.ts (timing.ts already done — ensure it includes `OUTRO_DURATION = 240`)
2. Create reusable components based on the plan
3. For each scene, read its sync JSON and build the scene component:
   - Map key visual moments to word timestamps
   - Use formula: `frame = word.start * 30 + audio_offset`
   - Comment sync sources at top of each scene
   - Use spring() for entrances, interpolate() for opacity/progress
   - Clamp all interpolations

   **CRITICAL - NO OVERLAPPING ELEMENTS**:
   - Use phase-based rendering when scene has multiple content sections
   - Elements that share screen space must animate sequentially (A exits → B enters)
   - Never render two elements in the same zone simultaneously

   **ARCHITECTURE DIAGRAMS** (boxes with arrows/lines):
   - Position boxes on a grid system (consistent spacing)
   - Calculate arrow endpoints from box positions dynamically
   - Render arrows BEFORE boxes in component tree (lower z-index)
   - Use orthogonal (right-angle) paths for clarity
   - Animate: Background → Arrow draws → Target box appears

4. Build Composition.tsx with TransitionSeries + Audio layer. **MANDATORY ELEMENTS**:
   - **OutroSequence**: Add as final sequence after CTA scene (8s / 240 frames, fades in)
     ```tsx
     import { BrandWatermark, OutroSequence } from '../shared/components';
     // ... in TransitionSeries, as LAST scene:
     <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: t })} />
     <TransitionSeries.Sequence durationInFrames={240}>
       <OutroSequence />
     </TransitionSeries.Sequence>
     ```
   - **Background music**: `<Audio src={staticFile('audio/shared/bg-music.wav')} volume={0.08} />`
   - **BrandWatermark**: `<BrandWatermark />` after audio layer
5. Register in Root.tsx (use `TOTAL_FRAMES` which includes outro)
6. **MANDATORY**: Invoke the `remotion-best-practices` skill using the Skill tool (`skill: "remotion-best-practices"`) to verify the implementation. Fix any violations before proceeding.

**VERIFICATION GATE** (ALL must pass before Phase 5):
- [ ] `Composition.tsx` contains `<OutroSequence` — brand outro video is REQUIRED
- [ ] `Composition.tsx` contains `<BrandWatermark` — watermark is REQUIRED
- [ ] `timing.ts` includes `outro: { start: X, duration: 240 }` — 8s outro duration
- If any check fails: STOP and add the missing mandatory element

Proceed immediately to Phase 5.

## Phase 5: Render (ASK the User before start rendering. Only do the Validation/Lint AUTO!)

1. Run lint check:
   ```bash
   npm run lint
   ```
   Fix any errors found (TypeScript or ESLint).

2. Render the final video:
   ```bash
   npx remotion render <CompositionId> out/<AnimationName>/final.mp4 --codec h264 --crf 18
   ```

3. Report completion with file path and size.

## Phase 6: YouTube Description (AUTO - MANDATORY)

**This phase is REQUIRED for every video. Do NOT skip.**

1. Read source content for context:
   - `src/<AnimationName>/research/content-brief.md` - Topic context and key points
   - `src/<AnimationName>/scripts/full-script.md` - Full narration content
   - `src/<AnimationName>/constants/timing.ts` - Scene timing for chapters

2. Generate chapter timestamps from timing.ts:
   - Formula: `start_frame / 30 fps = seconds → M:SS`
   - First chapter MUST start at `0:00`

3. Create `src/<AnimationName>/youtube-description.md` with this structure:

```markdown
[Hook paragraph 1 - KEYWORD-RICH opener: Include topic name, version, key features in first 200 chars. YouTube SEO depends on this. Lead with keywords, not questions.]

[Hook paragraph 2 - Solution introduction: How does this video help?]

[Hook paragraph 3 - Call to watch: What will they gain by watching?]

What You'll Learn
✅ [Key takeaway 1 - extracted from script]
✅ [Key takeaway 2]
✅ [Key takeaway 3]
✅ [Key takeaway 4]
✅ [Key takeaway 5]
✅ [Key takeaway 6]

Why [Topic] Matters
[1 paragraph explaining the broader significance and relevance of this topic]

Chapters
0:00 [Scene 1 title - humanized from timing.ts scene names]
0:XX [Scene 2 title]
...
[Generate from SCENES object in timing.ts, use M:SS format]

Featured Concepts
[1 paragraph summarizing the main technical concepts explored in the video]

Resources
📝 [Primary documentation or tool]: [URL if known, otherwise placeholder]
[Additional relevant resources based on topic]

🚀 Want to learn agentic coding with live daily events and workshops?
Check out Dynamous AI: https://dynamous.ai/?code=646a60
Get 10% off here 👉 https://shorturl.smartcode.diy/dynamous_ai_10_percent_discount

Affiliate Partners
⚙️ n8n Cloud Automation: https://n8n.partnerlinks.io/diysmartcode
📈 vidIQ (grow your YouTube channel): https://vidiq.com/DIYSmartCode

Support the Channel
☕ Buy me a coffee: https://buymeacoffee.com/diy_smartcode

Target Audience
[Comma-separated list: developers, tech enthusiasts, etc. based on content]

Hashtags
#[Tag1] #[Tag2] #[Tag3] #[Tag4] #[Tag5] #DIYSmartCode #TechTutorial
```

4. Save to `src/<AnimationName>/youtube-description.md`

## Phase 7: YouTube Upload (OPTIONAL)

**This phase ONLY runs if:**
- `$ARGUMENTS` contains `--upload`, `upload`, or `publish`
- OR the structured brief contains `YouTube Upload: yes`

**If YouTube upload is NOT requested, SKIP this phase entirely.**

If upload is requested:

1. Check prerequisites:
   - `client_secrets.json` must exist (OAuth credentials)
   - If missing, display setup instructions and STOP

2. Generate thumbnail prompts:
   ```bash
   python youtube_upload.py <AnimationName> --gen-thumbs --dry-run
   ```
   This creates `src/<AnimationName>/thumbnail-prompts.md` for manual thumbnail creation.

3. Run dry-run preview:
   ```bash
   python youtube_upload.py <AnimationName> --dry-run
   ```
   Show the user what will be uploaded.

4. **ASK USER** before actual upload:
   - Confirm they want to proceed
   - Ask for privacy setting (default: private)

5. Upload with selected privacy:
   ```bash
   python youtube_upload.py <AnimationName> --privacy <selected>
   ```

6. Report video URL and next steps.

**IMPORTANT**: Even in full-auto mode, YouTube upload:
- Defaults to PRIVATE for safety
- Requires user confirmation before actual upload
- Can be scheduled with `--schedule "2026-01-28T15:00:00Z"`

</process>

<output>
**All files created**:
```
src/<AnimationName>/
├── research/content-brief.md
├── constants/ (colors, fonts, springs, timing)
├── components/ (scene background + visual elements)
├── scenes/ (Scene01*.tsx through SceneNN*.tsx)
├── scripts/ (scene-NN-*.txt + sceneNN-sync.json)
├── youtube-description.md  <-- MANDATORY
├── thumbnail-prompts.md    <-- If --upload requested
└── Composition.tsx

.agents/plans/<AnimationName>.plan.md
public/audio/<name>/scene01.mp3 through sceneNN.mp3
out/<AnimationName>/final.mp4
src/Root.tsx (updated)
```

**Final report to user**:
1. Video rendered: `out/<AnimationName>/final.mp4`
2. Duration: X seconds (Y frames at 30fps)
3. Scenes: N scenes with audio sync
4. File size
5. YouTube description generated: `src/<AnimationName>/youtube-description.md`
6. If uploaded: Video URL + thumbnail prompts location
7. Suggest: Run `npm run dev` to preview, or play the .mp4 directly
</output>
