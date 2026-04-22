---
name: Cinematic Hook Patterns (Film Trailer Style)
description: Proven hook techniques from ArchonOverview — Film Trailer variant with spring animations, smash cuts, team avatars, and layered SFX
type: feedback
---

## Film Trailer Hook Structure (HookVariant7 — proven winner)

### Visual Beats
1. **Title cards on black** (frames 0-60): "LAST MONTH" springs up from below with radial glow behind it. Hold for 1.3s minimum.
2. **Themed background** (frames 60-250): Dark themed bg (e.g., GitHub #0d1117) with subtle Octocat/logo at 6-8% opacity. Ken Burns zoom (1.0→1.15) + slow pan on the background icon. Dynamic vignette tightening from 55%→40% as tension builds.
3. **Text spring entrances**: Each phrase springs in from a different direction — "LAUNCHED" from below, "Agentic Workflows" from right, "It's a big deal" slam with scale overshoot (1.3→1.0).
4. **"But" smash cut**: White flash (60% opacity, 1 frame peak, 4 frame decay) + GlitchInterrupt (4 frames) + ScreenShake (intensity 5, 5 frames). Keep subtle — too much feels laggy.
5. **Team avatars**: Two-tier layout — Core Team (larger, cyan borders) + Contributors (smaller, grey borders). Each with name label. Spring stagger 3-4 frames apart.
6. **Logo video**: Use `<Sequence from={startFrame} durationInFrames={duration}>` for proper playback timing. WebM with alpha + `transparent` prop on OffthreadVideo.
7. **Feature rapid-fire cards**: 96px bold text, each card springs in with scale (1.4→1.0), different accent colors.
8. **Launch badges**: Glass morphism pills stacked — "Launching on GitHub" (green) + "Live Stream on Cole's Channel" (purple dot indicator).

### SFX Layering (per impact moment)
- **Smash cut**: `impact-slam.mp3` (0.35-0.45) — the main punch
- **Pivot "But"**: Triple stack: `impact-slam` (0.45) + `screen-shake` (0.35) + `glitch-zap` (0.28)
- **Reveal**: `scale-slam.mp3` (0.40) — for hero text/logo
- **Feature cards**: `pop.mp3` (0.28-0.32) — rapid-fire, one per card
- **Transitions**: `cinematic-whoosh.mp3` (0.3) — at every LightLeakOverlay cut
- **BG music**: Generate 40s hook-specific track via ElevenLabs, prompt must say "immediate from first second" to avoid silent intro

### Key Learnings
- Title cards need 1.3s+ hold time regardless of narration speed — decouple from word timestamps
- ScreenShake intensity above 8 feels laggy, keep at 5-6
- GlitchInterrupt duration above 6 frames feels stuttery, keep at 4
- White flash above 60% opacity is blinding, keep at 40-60%
- Background logo/icon videos: use `<Sequence>` for playback timing, NOT conditional mount
- Team photos at 100-130px for core, 80px for contributors in split layouts

**Why:** User confirmed this as the winning hook style after testing 10 variants. The Film Trailer approach (sequential title cards → themed background → smash cut pivot → portrait + team → rapid features) consistently outperformed other approaches.

**How to apply:** Use this structure as the starting template for future video hooks. Adapt the themed background and colors per video topic.
