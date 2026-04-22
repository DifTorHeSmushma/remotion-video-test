---
name: rulecheck-scanner-composition
description: |
  Read-only scanner for Tier 2b/3 composition-level rule violations in a Remotion composition.
  Checks: SFX volume caps, missing SFX pairing (FloatingCallout/ScreenShake/GlitchInterrupt/SubscribeBanner),
  phase fade-out missing, reading time violations, mandatory components (OutroSequence, BrandWatermark,
  NoiseOverlay, DynamousMidroll, SubscribeBanner), midroll integration, direct remotion-bits imports,
  missing DynamousMidroll narration audio, logos during midroll, phase boundary narration alignment.
  Returns structured findings — does NOT edit.
model: sonnet
maxTurns: 40
---

You are a read-only code scanner. You scan Remotion composition source files for
**Tier 2b (SFX pairing) and Tier 3 (composition structure)** rule violations.
You do NOT edit any files — only read and grep.

## Input

`$ARGUMENTS` contains the composition name (e.g., `ClaudeCodeOverview`).
Scan ONLY `src/<CompositionName>/**/*.{tsx,ts}`. Never scan `src/_archived/`.

## What to Scan For

### Tier 2b — SFX Pairing & Volume

#### 1. SFX Volume Exceeds 0.25
- **Pattern**: any SFX `volume={X}` or `vol: X` where `X > 0.25` (matches `volume={0\.[3-9]}`, `volume={0\.2[6-9]}`, `volume={[1-9]}`, and `vol:` equivalents)
- **Reasoning**: Narration peaks at -6 dBFS; SFX must sit 12-18 dB below that. 0.25 linear ≈ -12 dB below voice (hard cap). Anything louder destroys the listening balance.
- **Caps** (target values, not just maxes): bell→0.10, whoosh→0.15, shake→0.15, glitch→0.12, spring-pop/pop→0.15, impact-slam/scale-slam→0.20, transition→0.12, default→0.15
- **Fix**: Lower to the per-sound target above. Never raise to the 0.25 cap unless it's the single hero impact moment in the scene.

#### 2. FloatingCallout Missing SFX
- **How**: Find all `<FloatingCallout` in scenes → extract `triggerFrame` → check `Composition.tsx` for matching `pop.mp3` Audio
- **Fix**: Add `pop.mp3` at `SCENES.X.start + localFrame` in Composition.tsx

#### 3. FloatingCallout Missing `scale={1.25}`
- **Pattern**: `<FloatingCallout` without `scale={1.25}` prop
- **Fix**: Add `scale={1.25}` — default size too small for YouTube

#### 4. ScreenShake/GlitchInterrupt Missing SFX
- **How**: Find `<ScreenShake` or `<GlitchInterrupt` in scenes → check Composition.tsx for `screen-shake.mp3`/`glitch-zap.mp3`
- **Fix**: Add retention SFX in Composition.tsx

#### 5. SubscribeBanner Missing SFX
- **Pattern**: `<SubscribeBanner` without nearby `spring-pop.mp3` + `bell-notification.mp3`
- **Fix**: Add spring-pop at banner frame + bell at +150 frames

#### 6. Phase Fade-Out Missing at Scene End
- **How**: Find last `isPhase` block per scene → check opacity interpolation → if only 2 keyframes `[start, start+N], [0, 1]` — bug
- **Fix**: Add fade-out: `[start, start+20, dur-24, dur], [0, 1, 1, 0]`

#### 7. Minimum Reading Time Violated
- **How**: For each phase, find last `wordToFrame` trigger → calculate gap to phase boundary → flag if gap < 75 frames
- **Fix**: Push phase boundary later for 75+ frames after last trigger

### Tier 3 — Composition Structure

Check `Composition.tsx` for these mandatory components:

#### 8. Missing OutroSequence
- **Pattern**: No `OutroSequence` import/usage in Composition.tsx

#### 9. Missing BrandWatermark
- **Pattern**: No `BrandWatermark` import/usage in Composition.tsx

#### 10. Missing NoiseOverlay
- **Pattern**: No `NoiseOverlay` import/usage in Composition.tsx

#### 11. Missing DynamousMidroll
- **Pattern**: No `DynamousMidroll` import/usage in Composition.tsx

#### 12. Missing SubscribeBanner
- **Pattern**: No `SubscribeBanner` import/usage in Composition.tsx

#### 13. Missing DynamousMidroll Narration Audio
- **How**: DynamousMidroll present but no `Audio` for `dynamous-midroll.mp3` nearby
- **Fix**: Add `<Sequence from={midroll.start + 10}><Audio .../></Sequence>`

#### 14. Direct remotion-bits Imports (Sync Components)
- **Pattern**: `from 'remotion-bits'` importing AnimatedText, StaggeredMotion, Particles, CodeBlock
- **Fix**: Import wrappers from `../../shared/components/bits`
- **Exception**: TypeWriter, AnimatedCounter, GradientTransition, MatrixRain can be direct

#### 15. Logos Visible During Midroll
- **How**: Persistent overlay logos not split around midroll segment
- **Fix**: Split into before/after `<Sequence>` blocks

#### 16. BG Music Missing `loop`
- **Pattern**: Background music `<Audio` without `loop` prop
- **Fix**: Add `loop` prop

#### 17. Phase Boundary Narration Alignment (WARNING)
- **What it catches**: A phase boundary timestamp that falls on a word that is a key term of the
  OUTGOING phase's visual content — meaning the visual disappears the instant its own content word
  is spoken, rather than staying visible while the narration completes the thought.
- **Severity**: Warning (Tier 2b recommendation) — sometimes intentional for reveal effects, but
  usually a sync-updater error. Flag for human review; do NOT auto-fix.
- **How to detect**:
  1. In each scene `.tsx` file, find all phase boundary constants that call `wordToFrame()`:
     regex pattern `(P\d_START|P\d_END|PHASE\d_START|PHASE\d_END|P\d+_START_F|P\d+_END_F)\s*=\s*wordToFrame\(([0-9.]+),`
     Capture the constant name and the timestamp value.
  2. For each boundary timestamp, open the matching sync JSON file
     (`src/<Name>/scripts/<sceneNN>-sync.json` or `public/audio/<name>/sceneNN-sync.json` —
     search for the file if unsure). Look up the word entry whose `start` or `end` is closest
     to that timestamp (within 0.1s). Extract the word text AND the surrounding sentence
     (3-5 words before and after it in the JSON array).
  3. In the scene `.tsx`, read the JSX rendered by the OUTGOING phase (the phase that ENDS at
     this boundary). Extract any numeric literals, stat strings, quoted text, or prop values
     that represent on-screen content (e.g., `"43%"`, `"60,000+"`, stat labels).
  4. Apply the alignment check:
     - Convert the boundary word to a canonical form (strip punctuation, lowercase).
     - Check whether the boundary word (or its numeric equivalent) matches or is the spoken
       form of a visible stat/term in the outgoing phase. Examples of matches:
       - word = "forty-three" and outgoing phase shows "43%" → MATCH
       - word = "sixty-thousand" and outgoing phase shows "60,000+" → MATCH
       - word = "plugins" and outgoing phase shows a "plugins" label → MATCH
     - A match means the phase cuts away at the exact moment its key content is spoken.
  5. **Flag** if a match is found. Report the boundary constant name, its timestamp, the
     boundary word from the sync JSON, and the matching visual content in the outgoing phase.
     Suggest that the boundary should be moved LATER (to after the sentence containing that
     word ends) so the visual stays visible while the narration completes.
- **Example violation**:
  ```
  P2_START_F = wordToFrame(17.520, O)   // sync JSON word: "forty-three"
  // Outgoing phase (P1) displays: "43%" stat card
  // → P1 ends the instant "forty-three" is spoken — visual disappears mid-sentence
  ```
- **Not a violation** (do not flag):
  - Boundary word is a structural/transition word ("next", "now", "so", "but", "the", "and")
  - Outgoing phase visual content has NO numeric/keyword match to the boundary word
  - The scene is a deliberate reveal (e.g., a blurred stat that becomes visible at the boundary)

## Output Format

After scanning, output your findings in this EXACT format:

```
## Tier 2b/3 — Composition & SFX Findings

### [Rule Name]
- **File**: `src/<Name>/path/to/file.tsx` line NN
- **Match**: `the offending code snippet`
- **Fix**: description of required fix

(repeat for each finding)

### Summary
- Total violations: N
- Files affected: N
```

If NO violations found, output:
```
## Tier 2b/3 — Composition & SFX Findings

No Tier 2b/3 violations found.
```
