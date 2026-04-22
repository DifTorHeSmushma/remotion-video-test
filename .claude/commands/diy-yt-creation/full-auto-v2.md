---
description: "Full auto v2: Orchestrate all phases (0-6) by invoking individual phase workflows"
argument-hint: <topic, product URL, or concept description> [--upload]
---

<objective>
Execute the ENTIRE DIY YouTube Video Creation Workflow by orchestrating individual phase workflows.
This version calls each phase command sequentially, ensuring consistency with the standalone phase workflows.

**Goal**: Go from concept to render-ready composition autonomously, then STOP for user approval before rendering.
**Output**: `out/<AnimationName>/final.mp4` + all intermediate artifacts

IMPORTANT: Do NOT ask questions during execution EXCEPT before rendering. Gather all parameters upfront, then run autonomously through Phases 0-4b. Phase 5 MUST stop and wait for explicit user approval before starting any render.

**CRITICAL**: NEVER start `remotion render` without explicit user confirmation. This is a hard gate, not a suggestion.
</objective>

<initial-setup>

## Step 1: Parse Input and Detect Parameters

Parse "$ARGUMENTS" to extract parameters:

**If structured brief** (contains "**Topic**:", "**Duration**:", etc.):
- Extract all fields directly from the brief
- Store as `PARAMS` object for passing to phases

**If freeform text**:
- Look for duration patterns: "15s", "30s", "45s", "60s", "90s", "2min", "3min"
- Extract topic/URL from the text

## Step 2: Set Parameters (Use Defaults for Missing Values)

Collect these parameters ONCE at the start. Do NOT ask questions later.

```yaml
PARAMS:
  topic: "<extracted from $ARGUMENTS>"
  duration: "<detected or default: 5min>"
  tone: "<from brief or default: tech-influencer-edgy>"
  resolution: "<from brief or default: 1920x1080>"
  target_audience: "<from brief or infer from topic>"
  key_angle: "<from brief or determine in Phase 0>"
  links: "<URLs from brief or empty>"
  must_mention: "<from brief or empty>"
  technical_terms: "<from brief or empty>"
  upload_requested: "<true if --upload in $ARGUMENTS>"
```

### Duration-to-Structure Quick Reference

| Duration | Scenes | Words | Structure |
|----------|--------|-------|-----------|
| 15s | 3 | ~37 | Hook → Core → CTA |
| 30s | 4-5 | ~75 | Hook → Solution → Feature → CTA |
| 45s | 5-6 | ~112 | Hook → Solution → 2-3 Features → CTA |
| 60s | 6-7 | ~150 | Hook → Solution → 3-4 Features → Trust → CTA |
| 90s | 7-8 | ~225 | Hook → Solution → 4-5 Features → Trust → CTA |
| 3min | 9-10 | ~450 | Hook → Solution → 5-7 Features → Ecosystem → Security → CTA |
| 5min | 10-12 | ~750 | Preview → Hook → Problem → Solution → 4-6 Deep Features → Example → Framework → Trust → CTA |
| 7min | 12-14 | ~1050 | Preview → Hook → Problem → Solution → 5-8 Deep Features → Real Examples → Framework → Trust → CTA |
| 8min | 14-16 | ~1200 | Preview → Hook → Problem → Solution → 6-10 Deep Features → Multiple Examples → Comparisons → Framework → Trust → CTA |

## Step 3: Derive AnimationName

Convert topic to PascalCase for folder name:
- "docker sandboxes" → "DockerSandboxes"
- "Claude Code v2.1.20" → "ClaudeCodeV2120"
- "remote agentic coding" → "RemoteAgenticCoding"

Store as `ANIMATION_NAME` for all phases.

## Step 4: Initialize Phase Status File

Create `src/{ANIMATION_NAME}/phase-status.md` with all phases as `pending`:

```markdown
# Phase Status: {ANIMATION_NAME}

| Phase | Status | Completed |
|-------|--------|-----------|
| 0 - Research | pending | |
| 1 - Plan | pending | |
| 2 - Script | pending | |
| 2.5 - Critique | pending | |
| 2a - TTS Script | pending | |
| 2b - Fact Check | pending | |
| 3 - Audio | pending | |
| 3.5 - Retention | pending | |
| 4 - Sync | pending | |
| 4b - Visual QA | pending | |
| 5 - Render | pending | |
| 6 - Shorts | pending | |
| 6 - Upload | pending | |
```

Each phase command updates its own row when it completes. In crash recovery, read this file to determine where to resume.

</initial-setup>

<orchestration>

### Context Isolation Mandate (CRITICAL)

**All phases MUST run as isolated subagents via the Task tool.** Never invoke phase commands as slash commands from this orchestrator — slash commands load their full `.md` contents plus all runtime artifacts (web searches, briefs, sync JSONs, render logs) into the main context and cause 500K+ token bloat by Phase 4.

Dispatch rules:
- Phases 0, 1, 2, 2.5, 2a, 2b, 3, 5 → `subagent_type: "diy-phase-runner"` (generic runner)
- Phase 3.5 → `subagent_type: "retention-strategy-agent"` (existing)
- Phase 4 → `subagent_type: "phase4-scene-builder"` (existing)
- Phase 4b → `subagent_type: "remotion-qa-agent"` (existing)

After each Task returns, record ONLY the <200-word summary in the orchestration log (`src/{ANIMATION_NAME}/orchestration-log.md`). Do NOT re-read research briefs, plans, scripts, or sync JSONs in this orchestrator — every subsequent subagent reads inputs from disk autonomously.

### Phase Status Tracking

Each runner agent updates `src/{ANIMATION_NAME}/phase-status.md` when it completes (mark row as `done` + date). The orchestrator just checks the latest row and moves on.

**Crash recovery**: If full-auto-v2 is interrupted, read `phase-status.md` to see which phases completed. Resume from the first `pending` phase.

## Phase 0: Research

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase0-research {PARAMS.topic}

Context:
- AnimationName: {ANIMATION_NAME}
- Duration: {PARAMS.duration}
- Links to fetch: {PARAMS.links}
- Key angle hint: {PARAMS.key_angle}
- Target audience: {PARAMS.target_audience}"
```

**Expected output** (written to disk by agent):
- `src/{ANIMATION_NAME}/research/content-brief.md`

Proceed immediately after agent returns `Status: done`.

---

## Phase 1: Plan

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase1-plan {ANIMATION_NAME}

Context:
- Duration: {PARAMS.duration}
- Tone: {PARAMS.tone}
- Resolution: {PARAMS.resolution}
- Target audience: {PARAMS.target_audience}"
```

**Expected output** (written to disk by agent):
- `.agents/plans/{ANIMATION_NAME}.plan.md`

Proceed immediately after agent returns `Status: done`.

---

## Phase 2: Script (Raw + Preview Hook)

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase2-script {ANIMATION_NAME}

Context:
- Tone: {PARAMS.tone}
- Technical terms: {PARAMS.technical_terms}
- Must-mention: {PARAMS.must_mention}
- Word count target: matches {PARAMS.duration} from plan
- MANDATORY: include Scene 00 Preview hook (10-15s teaser)"
```

**Expected output** (written to disk by agent):
- `src/{ANIMATION_NAME}/scripts/full-script.md` (includes Scene 00 Preview section)

The runner verifies the Scene 00 Preview exists before returning `Status: done`.

**AUTO-APPROVE**: In full-auto mode, skip the review checkpoint. Proceed immediately to Phase 2.5.

---

## Phase 2.5: Script Quality Gate (MANDATORY)

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase2-5-critique {ANIMATION_NAME}"
```

The runner reads plan.md (including Hook Variants) + full-script.md from disk and runs the gate autonomously.

**Quality Gate Logic** (enforced inside the runner):
- PASS if all four gates pass (hook_score >= 7.0 AND story_arc_score >= 7.0 AND loop_opener_count >= required AND banned_phrase_count == 0) → runner returns `Status: done` → PROCEED to Phase 2a immediately
- FAIL on any gate → runner returns `Status: gate-blocked` with failing gate names → STOP orchestration, report to user, await revision to `full-script.md`, then re-dispatch Phase 2.5

**Expected output**:
- `src/{ANIMATION_NAME}/scripts/critique-report.md`

**STOP on FAIL**: Do NOT proceed to Phase 2a under any circumstance until the runner returns `Status: done`.

---

## Phase 2a: Script (TTS Optimized)

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase2a-script {ANIMATION_NAME}

Context:
- Technical terms: {PARAMS.technical_terms}"
```

**Expected output** (written to disk by agent):
- `src/{ANIMATION_NAME}/scripts/scene-00-preview.txt` (MANDATORY preview hook, 25-37 words)
- `src/{ANIMATION_NAME}/scripts/scene-NN-<name>.txt` (per-scene files)

Proceed immediately after agent returns `Status: done`.

---

## Phase 2b: Fact Check (MANDATORY GATE)

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase2b-factcheck {ANIMATION_NAME}"
```

The runner performs all WebSearch/WebFetch and Perplexity verification **in its own context**. Main orchestrator never sees the raw search results — only the summary count.

**Quality Gate Logic** (enforced inside the runner):
- PASS: all Tier 1 claims VERIFIED or auto-corrected (minor) → `Status: done` → PROCEED to Phase 3
- FAIL: any Tier 1 claim FAILED/UNVERIFIED, or major correction needed → `Status: gate-blocked` → STOP orchestration, report to user

**Expected output**:
- `src/{ANIMATION_NAME}/scripts/fact-check-report.md`
- `src/{ANIMATION_NAME}/scripts/perplexity-results.json` (if `PERPLEXITY_API_KEY` set)

**STOP on FAIL**: Do NOT proceed to Phase 3 until the runner returns `Status: done`.

---

## Phase 3: Audio Generation

**Dispatch** via Task tool:
```
subagent_type: "diy-phase-runner"
prompt: "phase3-audio {ANIMATION_NAME}

Context:
- Voice ID: from .env or default
- Speed: normal (long-form)
- Generation order: preview audio FIRST (python text-to-speech.py ... --name scene00 --preview), then python generate-all-audio.py {ANIMATION_NAME} --parallel 5
- Summarize TTS logs — do NOT echo full Python output"
```

**Expected output** (written to disk by agent):
- `public/audio/{name}/scene00.mp3` + `public/audio/{name}/sceneNN.mp3`
- `src/{ANIMATION_NAME}/scripts/sceneNN-sync.json`
- `src/{ANIMATION_NAME}/constants/timing.ts`

Proceed immediately after agent returns `Status: done`.

---

## Phase 3.2: Background Music Generation (AUTO)

Generate multi-segment background music that matches the hook's cinematic pattern.

**Read** the cinematic hook blueprint from `.agents/plans/{ANIMATION_NAME}.plan.md` to extract:
- `music_profile.hook_mood` → `--hook-mood` flag
- `music_profile.hook_bpm` → `--hook-bpm` flag (e.g., "95-105")
- `music_profile.body_bpm` → `--body-bpm` flag (e.g., "75-90")
- `music_profile.cta_bpm` → `--cta-bpm` flag (e.g., "110-120")

If no cinematic hook blueprint exists in the plan, use defaults (hook-mood: dramatic-cinematic, hook-bpm: 100-110).

**Run**:
```bash
python generate-bg-music.py {ANIMATION_NAME} --multi-segment \
  --hook-mood {hook_mood} \
  --hook-bpm {hook_bpm} \
  --body-bpm {body_bpm} \
  --cta-bpm {cta_bpm}
```

**Expected output**:
- `public/audio/{name}/bg-music-hook.mp3` (energetic, hook BPM)
- `public/audio/{name}/bg-music-body.mp3` (ambient, body BPM)
- `public/audio/{name}/bg-music-cta.mp3` (upbeat, CTA BPM)
- `public/audio/{name}/bg-music-metadata.json` (BPM values for beat alignment in Phase 4)

**Proceed immediately** — this is non-blocking.

---

## Phase 3.5: Retention Strategy (SUBAGENT)

**Spawn `retention-strategy-agent` as an isolated subagent** to analyze script content and produce a per-scene component prescription.

Use the **Task tool**:
```
Task tool:
  subagent_type: "retention-strategy-agent"
  prompt: "{ANIMATION_NAME}"
```

The agent reads all inputs from disk (plan, full-script.md, all sync JSONs, timing.ts) and writes:
- `src/{ANIMATION_NAME}/retention-strategy.md` (per-scene component decisions)

**Wait for Task tool result.** Confirm `retention-strategy.md` exists before proceeding.

**Expected output** (written to disk by agent):
- `src/{ANIMATION_NAME}/retention-strategy.md`

---

## Phase 3.5b: Screenshot Capture (OPTIONAL)

**Check**: Does the plan file (`.agents/plans/{ANIMATION_NAME}.plan.md`) contain a `screenshots:` section?

**If YES**:
1. Create `src/{ANIMATION_NAME}/images/screenshots.json` from the plan's `screenshots:` section
2. Run: `python capture-screenshots.py {ANIMATION_NAME}`
3. Verify output summary — all captures should be >10KB
4. Log any failures (auth wall, CAPTCHA) — Phase 4 will use placeholder cards for missing screenshots

**If NO**: Skip this step entirely.

This step can run **in parallel with Phase 3.5** (retention strategy) since they have no dependencies on each other. Both must complete before Phase 4 begins.

**Expected output**:
- `src/{ANIMATION_NAME}/images/screenshots.json` (manifest)
- `public/images/{name}/*.png` (captured screenshots)

**Proceed to Phase 4** after both Phase 3.5 and Phase 3.5b complete (or are skipped).

---

## Phase 4: Sync (Build Scenes — SUBAGENT)

**Spawn `phase4-scene-builder` as an isolated subagent** to prevent ~9,000 lines of generated TSX from bloating the main context.

Use the **Task tool**:
```
Task tool:
  subagent_type: "phase4-scene-builder"
  prompt: "{ANIMATION_NAME}"
```

The agent reads all its inputs from disk autonomously:
- `.agents/plans/{ANIMATION_NAME}.plan.md` — visual design (falls back to glob `*.plan.md` for legacy kebab-case names)
- `src/{ANIMATION_NAME}/scripts/sceneNN-sync.json` — word timestamps
- `src/{ANIMATION_NAME}/constants/timing.ts` — scene durations
- `src/{ANIMATION_NAME}/scripts/full-script.md` — scene names

**Wait for Task tool result.** Review the returned scene inventory.

**Expected output** (written to disk by agent):
- `src/{ANIMATION_NAME}/constants/` (colors, fonts, springs, timing)
- `src/{ANIMATION_NAME}/components/`
- `src/{ANIMATION_NAME}/scenes/Scene00Preview.tsx` (MANDATORY)
- `src/{ANIMATION_NAME}/scenes/Scene01*.tsx` through `SceneNN*.tsx`
- `src/{ANIMATION_NAME}/Composition.tsx` (MUST include OutroSequence + BrandWatermark)
- `src/Root.tsx` (updated)
- `src/{ANIMATION_NAME}/qa-frames.json` (MANDATORY)
- `out/{ANIMATION_NAME}/validate-*.md` (per-scene validation reports)

**Verify from agent's returned inventory** (ALL must pass):
- [ ] `qa-frames.json` exists
- [ ] No scene reported as ❌ FAIL in inventory
- [ ] `Composition.tsx` contains `<OutroSequence` (agent confirms)
- [ ] `Composition.tsx` contains `<BrandWatermark` (agent confirms)

**If agent reports FAIL** on any scene: Read the specific report at
`out/{ANIMATION_NAME}/validate-<SceneNN>.md` and fix before proceeding.

**Proceed directly to Phase 5** after agent returns success. Skip Phase 4b unless the user explicitly requests QA.

---

## Phase 4b: Visual QA (SKIPPED BY DEFAULT)

**Do NOT run this phase automatically.** QA is opt-in — only spawn `remotion-qa-agent` if the user explicitly asks ("run QA", "do visual QA", "check frames", etc.).

Mark the Phase 4b row in `phase-status.md` as `skipped (user can run /remotion-qa manually)` and continue to Phase 5.

If the user explicitly requests QA, spawn the agent via Task tool with `subagent_type: "remotion-qa-agent"` and `prompt: "{ANIMATION_NAME}"`. The agent writes its report to `out/{ANIMATION_NAME}/qa-report.md`. Apply the standard gate: pass -> proceed, warnings -> note, failures -> stop and fix.

---

## Phase 5: Render (PRE-RENDER PREP)

**Dispatch pre-render prep** via Task tool. The runner executes steps 1-4 of `phase5-render.md` only (validation, lint, YouTube description generation, summary build) and STOPS at the render gate — it does NOT run `remotion render`.

```
subagent_type: "diy-phase-runner"
prompt: "phase5-render {ANIMATION_NAME}

Context:
- Resolution: {PARAMS.resolution}
- Codec: h264, CRF 18
- QA: skipped by default (user runs /remotion-qa manually if needed)
- HARD GATE: do NOT run `remotion render` or full-video `remotion still`. Stop at the render gate and return gate-blocked with the composition summary.
- Return the full summary (scene count, duration, warnings) in the Notes field so the orchestrator can present it to the user."
```

Runner returns `Status: gate-blocked` with the summary. The orchestrator surfaces it to the user verbatim.

**⛔ MANDATORY RENDER GATE — DO NOT SKIP ⛔**

**STOP HERE.** Present the runner's summary to the user and explicitly ask for render approval.
Do NOT run `remotion render` or `remotion still` for the full video under any circumstance until the user explicitly confirms.
Wait for the user to say "render", "go ahead", "yes", or similar before proceeding.

**After explicit user approval**, the orchestrator itself runs the single `pnpm exec remotion render ...` command from `CLAUDE.md` (Render Quality Settings) — no subagent needed for a single shell command, and keeping render logs out of context matters less once the workflow is effectively done.

**Expected output**:
- `out/{ANIMATION_NAME}/final.mp4` (only after user approval)
- `src/{ANIMATION_NAME}/youtube-description.md` (generated during pre-render prep)

---

## Phase 6: YouTube Description (AUTO)

**This phase runs automatically after render completes.**

**Invoke**: `/diy-yt-creation:phase6-upload {ANIMATION_NAME}` with `--description-only`

Or manually generate:
- Read timing.ts for chapter timestamps
- Read full-script.md for content
- Generate `src/{ANIMATION_NAME}/youtube-description.md`

**Expected output**:
- `src/{ANIMATION_NAME}/youtube-description.md`

---

## Phase 7: YouTube Upload (CONDITIONAL)

**Only runs if**: `{PARAMS.upload_requested}` is true

**Invoke**: `/diy-yt-creation:phase6-upload {ANIMATION_NAME}`

**Actions**:
1. Generate thumbnail prompts
2. Show dry-run preview
3. **ASK USER** for privacy setting
4. Upload

**Expected output**:
- Video URL
- `src/{ANIMATION_NAME}/thumbnail-prompts.md`

</orchestration>

<error-handling>

## If a Phase Fails

1. **Read the error message** carefully
2. **Attempt auto-fix** if possible (lint errors, missing imports)
3. **Report to user** with:
   - Which phase failed
   - Error details
   - Suggested fix
4. **Do NOT proceed** to next phase until current phase succeeds

## Common Issues and Fixes

| Issue | Phase | Auto-Fix |
|-------|-------|----------|
| Missing directory | 0 | Create `src/{ANIMATION_NAME}/research/` |
| Lint errors | 4, 5 | Run `npm run lint -- --fix` |
| Missing audio | 3 | Re-run TTS generation |
| TypeScript errors | 4 | Fix imports, add types |
| Render crash | 5 | Check for non-deterministic code |

</error-handling>

<output>

## Final Report

After all phases complete, report to user:

```markdown
## Video Creation Complete

**Composition**: {ANIMATION_NAME}
**Duration**: {duration} seconds ({frames} frames at 30fps)
**Resolution**: {PARAMS.resolution}
**Scenes**: {scene_count} scenes

### Files Created
- Video: `out/{ANIMATION_NAME}/final.mp4`
- YouTube Description: `src/{ANIMATION_NAME}/youtube-description.md`
- Composition: `src/{ANIMATION_NAME}/Composition.tsx`

### Preview
Run `npm run dev` and select "{ANIMATION_NAME}" in Remotion Studio.

### Upload (if requested)
Video URL: {url}
Privacy: {privacy_setting}
```

</output>

<comparison-to-v1>

## Why v2?

| Aspect | full-auto (v1) | full-auto-v2 |
|--------|----------------|--------------|
| Phase logic | Duplicated inline | References phase workflows |
| Phase execution | Inline in main context | Isolated subagents (Task tool) |
| Main context size | Accumulates everything (~500K+) | <100K even for long videos |
| Maintenance | Update in 2+ places | Update phase workflow once |
| Consistency | Can drift from phases | Always in sync |
| Flexibility | Monolithic | Modular, can run phases individually |
| Error handling | Basic | Phase-specific with auto-fix |

**v2 is the recommended approach** for maintainability, consistency, and context efficiency.

## Context Budget (after isolation refactor)

- Main orchestrator: ~30K tokens (PARAMS, phase-status, Task summaries)
- Each phase subagent: isolated — discarded when Task returns
- User only sees: Task summaries (1-10 lines each) + final report
- End-state main context (after 9 phases): <100K tokens vs 500K+ previously

</comparison-to-v2>
