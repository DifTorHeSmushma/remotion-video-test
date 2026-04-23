---
description: Implement a Remotion composition for the `remotion-from-hn` workflow. Slug-based composition ID, conditional voice/music/sfx wiring, optional diagram components, optional brand overlay from .archon/brand.yaml.
argument-hint: (no direct arguments — consumes artifacts at $ARTIFACTS_DIR/ and repo-local .archon/brand.yaml)
---

# Remotion — Build Composition

**Workflow ID**: $WORKFLOW_ID
**Artifacts dir**: $ARTIFACTS_DIR

You are the Remotion builder node of the `remotion-from-hn` workflow. Plan,
narration, diagram decision, and (opt-in) audio files are already on disk.
Your job: implement the composition inside the pre-scaffolded project at
`$ARTIFACTS_DIR/project`. You have two skills loaded:

- `remotion-best-practices` — always consult
- `visual-diagrams` — consult ONLY if the plan flagged diagrams

---

## Phase 1: LOAD

Read these in order:

1. `$ARTIFACTS_DIR/slug.json` — authoritative `composition_id` and `fs_slug`.
   **The composition ID MUST be the exact `composition_id` string from this
   file.** Do not invent one.
2. `$ARTIFACTS_DIR/video-plan.md` — scene structure.
3. `$ARTIFACTS_DIR/narration.json` — spoken script per scene.
4. `$ARTIFACTS_DIR/article.json` + `$ARTIFACTS_DIR/article-body.md` — source
   material. Consult `article-body.md` if a scene needs a concrete detail.
5. `$ARTIFACTS_DIR/diagram-flag.json` — `{uses_diagrams, scenes[]}`.
6. **Probe which audio layers exist** (read each if present):
   - `$ARTIFACTS_DIR/audio/voice-manifest.json`
   - `$ARTIFACTS_DIR/audio/music-manifest.json`
   - `$ARTIFACTS_DIR/audio/sfx-manifest.json`
7. `.archon/brand.yaml` (repo-local, optional) — if present, apply the
   `colors`, `font_family`, `logo_url`, `watermark_position` /
   `watermark_opacity`. If absent, use neutral defaults:

       bg: #0B1120
       primary: #7C3AED
       secondary: #06B6D4
       accent: #F59E0B
       text_primary: #FFFFFF
       text_muted: #94A3B8
       font: Inter (via @remotion/google-fonts)
       no watermark

8. `$ARTIFACTS_DIR/project/src/Root.tsx` and `package.json`.

Then from the skills, always read:
- `rules/compositions.md`
- `rules/timing.md`
- `rules/sequencing.md`
- `rules/text-animations.md`
- `rules/animations.md`
- `rules/fonts.md`

If **voice-manifest exists**, additionally read:
- `rules/voiceover.md`
- `rules/calculate-metadata.md`
- `rules/get-audio-duration.md`
- `rules/audio.md`

If **diagram-flag.uses_diagrams == true**, additionally read:
- `visual-diagrams` SKILL.md
- `references/component-patterns.md`
- `references/animation-choreography.md`

### PHASE_1_CHECKPOINT
- [ ] `composition_id` + `fs_slug` captured from slug.json (will use verbatim)
- [ ] Plan + narration + diagram-flag read
- [ ] Each audio manifest probed; modes noted (voiced / music / sfx)
- [ ] Brand config loaded OR defaults selected
- [ ] Relevant rule files consulted

## Phase 2: IMPLEMENT

Layout inside `$ARTIFACTS_DIR/project/src/<composition_id>/`:

    src/<COMPOSITION_ID>/
      <COMPOSITION_ID>.tsx      — top-level composition, <Sequence>s, audio
      calculateMetadata.ts      — only when voice-manifest exists
      constants.ts              — fps, palette, typography, layout
      scenes/Scene1.tsx         — per-scene component
      scenes/SceneN.tsx

### Shared rules (always)

- Composition ID = exact `composition_id` from slug.json
- 1920×1080 @ 30fps
- Scene IDs stable: `scene1`, `scene2`, …
- **No TailwindCSS** — scaffold was `--no-tailwind`. Inline styles or style objects.
- All `interpolate()` calls set `extrapolateLeft` and `extrapolateRight`.
- Text ≥ 48px body / ≥ 96px headlines for 1080p legibility.
- **Do NOT delete the scaffold's `MyComp`**. Append the new composition.
- **Hook (scene1)**: narration and on-screen text must NOT echo the article
  title, must NOT reference HN/points/comments, must NOT open with "Welcome"
  / "Today" / "In this video". On-screen text ≤ 10 words. Entrance motion
  is dynamic, not a static fade-in headline.
- **Content**: nothing anywhere in the composition (on-screen text,
  narration, chart labels, etc.) may reference Hacker News or its metadata.

### Brand overlay

If `.archon/brand.yaml` exists:
- Apply `colors` to the palette object in `constants.ts`.
- Use `font_family` via `@remotion/google-fonts/<FamilyName>` (fall back to
  Inter if the name is unrecognized).
- If `logo_url` is a URL, download it to
  `$ARTIFACTS_DIR/project/public/brand/logo.<ext>` during build and render a
  watermark `<Img>` at `watermark_position` with `watermark_opacity`. Clamp
  logo width to 120px.
- If `logo_url` is a relative path starting with `.archon/brand/`, copy that
  file into `public/brand/` instead.
- Missing brand.yaml ⇒ use the neutral defaults listed in Phase 1.

### Silent mode (no voice-manifest)

- Static `durationInFrames` on `<Composition>` derived from plan nominal total.
- No `calculateMetadata`.
- No `<Audio>` for voice.
- (Music/SFX rules below still apply independently.)

### Voiced mode (voice-manifest exists)

Implement the canonical pattern from `rules/voiceover.md`:

1. `calculateMetadata.ts` uses `getAudioDuration(staticFile(scene.path))`
   per scene (**dynamic**, not hardcoded frame constants). Sum + optional
   small per-scene tail → `durationInFrames`. Pass `sceneDurations` into
   composition props.
2. In `<COMPOSITION_ID>.tsx`, each scene renders inside a `<Sequence from=
   {offsetFrames} durationInFrames={sceneFrames}>` with its scene
   component and its `<Audio src={staticFile(scene.path)} />`.
3. Register the composition in `Root.tsx` with `calculateMetadata` wired.
4. On-screen text complements — never duplicates — the narration.

### Music layer (music-manifest exists)

Single composition-level `<Audio>`:

```tsx
<Audio
  src={staticFile(musicManifest.path)}
  volume={musicManifest.volume}   // default ~0.2; ducks under voice
/>
```

Placed at composition root (not inside a Sequence) so it spans everything.
If music is shorter than the composition, accept silence at the tail rather
than looping — looping BGM under narration is distracting. If music is
longer, Remotion will trim automatically at render.

### SFX layer (sfx-manifest exists)

For each cue in `sfx-manifest.cues`:

- `intro_whoosh` → `<Audio src={staticFile(cue.path_rel)} />` inside a
  `<Sequence from={0} durationInFrames={cue.duration_frames}>`
- `outro_stinger` → at `compositionDuration - cue.duration_frames`
- `transition_N` → at each scene boundary (offset = end-frame of `from_scene`
  minus ~3 frames so it leads the cut)

Do NOT place SFX mid-scene unless the plan explicitly requested it.

### Diagram scenes (diagram-flag.uses_diagrams == true)

For each scene listed in `diagram-flag.scenes`, use the matching
`visual-diagrams` component:

- `flow` → `FlowDiagram`
- `hub-and-spoke` → `HubAndSpoke`
- `layered` → `LayeredArchitecture`
- `comparison` → `ComparisonDiagram`
- `infographic` → `InfographicFlow`

Follow the skill's rules: gradient fills, 2-layer shadows, ≥2.5px connection
strokes, Lucide icons (via `lucide-react`) or downloaded brand logos, never
Unicode emoji as icons. Background atmosphere (`ProceduralNoise` + radial
gradient) is encouraged for diagram scenes.

If `visual-diagrams` skill is NOT installed (SKILL.md missing), treat any
diagram-flagged scene as typography-only. Print a WARNING to stdout and
proceed.

### PHASE_2_CHECKPOINT
- [ ] `src/<composition_id>/` populated
- [ ] Composition registered in `Root.tsx` (MyComp still present)
- [ ] If voiced: `calculateMetadata.ts` uses dynamic `getAudioDuration`
- [ ] If music: single composition-level `<Audio volume>` set
- [ ] If SFX: cues wired at correct Sequence offsets
- [ ] If diagrams: flagged scenes use the correct component with full
      visual-diagrams treatment
- [ ] Brand overlay applied where relevant
- [ ] No Tailwind, no missing `extrapolate*`, no HN references

## Phase 3: SELF-CHECK

```bash
cd "$ARTIFACTS_DIR/project"
npx --yes tsc --noEmit
```

Fix errors. Retry up to two times. If still failing, stop and report.

### PHASE_3_CHECKPOINT
- [ ] `tsc --noEmit` exits 0
- [ ] Composition files present at `src/<composition_id>/`
- [ ] `Root.tsx` imports and registers `<composition_id>`

## Phase 4: REPORT

Final message (plain text, no code fences, no file dumps):

- Composition ID
- Modes: voiced=<bool> music=<bool> sfx=<bool> diagrams=<bool>
- Duration source (plan | audio-dynamic)
- Scenes implemented (one line each: `sceneN — name — start..end frames`)
- Files written (paths relative to `$ARTIFACTS_DIR/project/`)
- `tsc --noEmit` result (PASS or error summary)

No other text.
