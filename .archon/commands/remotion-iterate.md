---
description: Apply QA findings to the Remotion composition built by `remotion-build-composition`. Fixes CRITICAL + HIGH issues (voice/music/sfx/diagrams/hook/content), re-runs tsc. Defers MED/LOW.
argument-hint: (no direct arguments — consumes $ARTIFACTS_DIR/qa-findings.md)
---

# Remotion — Iterate on QA Findings

**Workflow ID**: $WORKFLOW_ID
**Artifacts dir**: $ARTIFACTS_DIR

You are the only node in the workflow allowed to edit scene code after the
build step. Two skills loaded: `remotion-best-practices` and `visual-diagrams`
(consult when relevant).

The **repo root is the project root**. All edits happen inside
`src/<composition_id>/` — do not touch `src/Root.tsx` (it auto-registers
via `import.meta.glob`) and do not modify other compositions.

---

## Phase 1: LOAD

1. `$ARTIFACTS_DIR/qa-findings.md` — findings, severity-tagged
2. `$ARTIFACTS_DIR/slug.json` — composition_id + fs_slug (authoritative)
3. `$ARTIFACTS_DIR/video-plan.md` — structural source of truth
4. `$ARTIFACTS_DIR/diagram-flag.json` — whether diagram scenes are expected
5. Audio manifests (if present):
   - `$ARTIFACTS_DIR/audio/voice-manifest.json`
   - `$ARTIFACTS_DIR/audio/music-manifest.json`
   - `$ARTIFACTS_DIR/audio/sfx-manifest.json`
6. `.archon/brand.yaml` (if present)
7. Everything under `src/<composition_id>/` in the repo root. DO NOT read or
   modify `src/Root.tsx` — it's stable and auto-registers.

Then pull the relevant rule files based on what the findings flag —
timing, sequencing, voiceover, calculate-metadata, audio for voice issues;
visual-diagrams component-patterns for diagram issues; etc.

### PHASE_1_CHECKPOINT
- [ ] Findings sorted by severity
- [ ] Plan + slug + diagram-flag + audio manifests read
- [ ] Current code state understood

## Phase 2: PLAN FIXES

Write `$ARTIFACTS_DIR/iterate-plan.md`:

    # Iterate Plan

    ## Fixing
    - [CRITICAL] <issue> — <file> — <one-line fix intent>
    - [HIGH]     <issue> — <file> — <one-line fix intent>

    ## Deferring
    - [MED]  <issue> — <why skipped for this pass>
    - [LOW]  <issue> — <why skipped for this pass>

**Scope rule**: fix every CRITICAL and every HIGH. Defer MED and LOW unless
trivial while you're already editing the same file. Do not add new features.

Common HIGH/CRITICAL issue shapes in this workflow:

- Hardcoded `SCENE_AUDIO_FRAMES` instead of dynamic `getAudioDuration()` in
  `calculateMetadata.ts` — fix by replacing constants with dynamic measurement
  per `rules/voiceover.md`.
- Unducked music (no `volume` on the music `<Audio>`, or `volume` near 1.0
  while voice plays) — set `volume` to the manifest's value (default 0.2).
- On-screen text or narration referencing Hacker News / points / comments —
  rewrite to article-focused copy.
- Hook scene opening with "Welcome", "Today", the article title as a card,
  or with no dynamic motion — rewrite per the hook rules from the plan.
- Diagram-flagged scenes built with plain typography — swap to the correct
  `visual-diagrams` component.
- Plan-specified transitions absent — implement them.

### PHASE_2_CHECKPOINT
- [ ] `iterate-plan.md` written
- [ ] Every CRITICAL and HIGH has a line in "Fixing"

## Phase 3: APPLY FIXES

Edit the files in your plan, scoped strictly to `src/<composition_id>/`.
Rules:

- Do not change the `composition_id` (from `slug.json`).
- Do not rename files unless a finding requires it.
- Do not change fps/width/height.
- Do not touch `src/Root.tsx` or any other composition's directory.
- If a fix changes per-scene timing, keep `calculateMetadata` and
  `<Sequence>` offsets consistent.
- If fixing audio wiring, keep manifest paths exact — they live under the
  repo's `public/` and are read via `staticFile()` with the verbatim
  manifest path.
- Keep edits minimal — one fix per finding, not a rewrite.

## Phase 4: VERIFY

```bash
npx --yes tsc --noEmit
```

Retry once on failure. If still failing, stop and report.

### PHASE_4_CHECKPOINT
- [ ] `tsc --noEmit` exits 0
- [ ] All CRITICAL + HIGH findings addressed or explicitly documented as
      "not fixable in one pass — see notes"

## Phase 5: REPORT

Write `$ARTIFACTS_DIR/iterate-report.md`:

    # Iterate Report

    ## Fixed
    - [CRITICAL] <finding> — <file:line> — <what changed>
    - [HIGH]     <finding> — <file:line> — <what changed>

    ## Deferred
    - [MED] <finding> — <reason>

    ## Outcome
    - tsc --noEmit: PASS | FAIL (with error digest)

Final message to the workflow: plain-text summary under 100 words listing
count CRITICAL+HIGH fixed, count deferred, tsc result, files touched.
