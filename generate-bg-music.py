#!/usr/bin/env python3
"""
Generate custom background music for a Remotion video composition.

Usage:
    python generate-bg-music.py <AnimationName>
    python generate-bg-music.py <AnimationName> --prompt "lo-fi ambient, soft piano"
    python generate-bg-music.py <AnimationName> --duration 180
    python generate-bg-music.py <AnimationName> --no-update
    python generate-bg-music.py <AnimationName> --dry-run

Prerequisites:
    ELEVENLABS_API_KEY set in environment (or .env)

Output:
    public/audio/<animationname>/bg-music.mp3
    Optionally patches Composition.tsx to use the new track.
"""

import argparse
import os
import re
import sys
from pathlib import Path

from generate_bg_music_lib import generate_background_music

FPS = 30

# Suffix appended to ALL music prompts to keep tracks unobtrusive
_BG_SUFFIX = ", very minimal and sparse, no melody, no vocals, extremely quiet and ambient, designed to sit far behind spoken narration"

# Map script tone (from content-brief.md) to music style prompt
TONE_MUSIC_MAP = {
    "tech-influencer-edgy": "dark ambient pad, slow evolving texture, deep sub-bass drone, sparse glitch accents" + _BG_SUFFIX,
    "professional-corporate": "soft ambient pad, gentle piano notes with long reverb, minimal strings" + _BG_SUFFIX,
    "friendly-educational": "warm lo-fi ambient texture, soft filtered chords, slow gentle pulse" + _BG_SUFFIX,
    "dramatic-cinematic": "low cinematic drone, slow strings swell, dark atmospheric texture" + _BG_SUFFIX,
    "casual-conversational": "light acoustic ambient, soft muted guitar harmonics, airy pad" + _BG_SUFFIX,
    "hype-energetic": "subtle electronic pulse, soft filtered synth pad, gentle rhythmic texture" + _BG_SUFFIX,
}

# Default prompt when tone mapping fails
DEFAULT_MUSIC_PROMPT = "ambient atmospheric pad, slow evolving texture, no melody, no beat, extremely minimal background for spoken narration"


def extract_duration_from_timing(animation_name: str) -> float | None:
    """Extract video duration in seconds from timing.ts by parsing TOTAL_FRAMES.

    Handles three common patterns:
      TOTAL_FRAMES = 10349;                              -> 10349
      TOTAL_FRAMES = SCENES.outro.start + ...; // 13117  -> 13117
      TOTAL_FRAMES = OUTRO_START + OUTRO_GAP; // ... = 23480 -> 23480
    """
    timing_path = Path("src") / animation_name / "constants" / "timing.ts"
    if not timing_path.exists():
        return None

    content = timing_path.read_text(encoding="utf-8")

    # Pattern 1: Direct numeric assignment
    match = re.search(r'TOTAL_FRAMES\s*=\s*(\d+)\s*;', content)
    if match:
        return int(match.group(1)) / FPS

    # Pattern 2: Expression with numeric value in trailing comment
    # e.g. "TOTAL_FRAMES = SCENES.outro.start + ...; // 13117"
    # e.g. "TOTAL_FRAMES = OUTRO_START + OUTRO_GAP;  // 23240 + 240 = 23480"
    match = re.search(r'TOTAL_FRAMES\s*=\s*[^;]+;\s*//.*?(\d{3,})\s*$', content, re.MULTILINE)
    if match:
        # Take the last number in the comment (most likely the final value)
        line_match = re.search(r'TOTAL_FRAMES\s*=\s*[^;]+;\s*//(.*)', content, re.MULTILINE)
        if line_match:
            comment = line_match.group(1)
            numbers = re.findall(r'\d{3,}', comment)
            if numbers:
                return int(numbers[-1]) / FPS

    return None


def extract_prompt_from_brief(animation_name: str) -> str:
    """Build a music prompt from the content-brief.md topic and tone."""
    brief_path = Path("src") / animation_name / "research" / "content-brief.md"
    if not brief_path.exists():
        print(f"  No content-brief.md found, using default music prompt.")
        return DEFAULT_MUSIC_PROMPT

    content = brief_path.read_text(encoding="utf-8")

    # Extract tone — handles: **Tone:** value, Tone: value, `tone` value
    tone = None
    tone_patterns = [
        r'\*\*[Tt]one:?\*\*:?\s*[`"]*([A-Za-z\-]+)',   # **Tone:** tech-influencer-edgy
        r'[Tt]one\s*:\s*[`"]*([a-z\-]+)[`"]*',          # Tone: tech-influencer-edgy
        r'[Tt]one\s+direction:?\s*["\']([^"\']+)',       # Tone direction: "neutral..."
    ]
    for pattern in tone_patterns:
        tone_match = re.search(pattern, content)
        if tone_match:
            tone = tone_match.group(1).strip().lower()
            break

    # Extract topic/title — strip "Content Brief:" prefix if present
    topic = None
    topic_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if topic_match:
        topic = topic_match.group(1).strip()
        topic = re.sub(r'^Content\s+Brief:\s*', '', topic, flags=re.IGNORECASE).strip()

    # Build prompt from tone mapping
    if tone and tone in TONE_MUSIC_MAP:
        base_prompt = TONE_MUSIC_MAP[tone]
        print(f"  Tone detected: {tone}")
    else:
        base_prompt = DEFAULT_MUSIC_PROMPT
        if tone:
            print(f"  Tone '{tone}' not in mapping, using default.")
        else:
            print(f"  No tone detected, using default music prompt.")

    # Add topic context if available
    if topic:
        return f"{base_prompt}, background for a video about {topic}"
    return base_prompt


def patch_composition(animation_name: str, audio_rel_path: str) -> bool:
    """
    Patch Composition.tsx to use the per-video background music track
    instead of the shared default.
    """
    comp_path = Path("src") / animation_name / "Composition.tsx"
    if not comp_path.exists():
        print(f"  Composition.tsx not found at {comp_path} — skipping patch.")
        return False

    content = comp_path.read_text(encoding="utf-8")
    original = content

    # Match common shared bg-music patterns
    patterns = [
        r"staticFile\(['\"]audio/shared/bg-music\.wav['\"]\)",
        r"staticFile\(['\"]audio/shared/bg-music\.mp3['\"]\)",
        r"staticFile\(['\"]audio/shared/Binary Horizons\.wav['\"]\)",
        r"staticFile\(['\"]audio/shared/Binary Horizons\.mp3['\"]\)",
    ]

    replacement = f"staticFile('{audio_rel_path}')"
    patched = False

    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            patched = True

    if patched:
        comp_path.write_text(content, encoding="utf-8")
        print(f"  Patched Composition.tsx: bg-music -> {audio_rel_path}")
        return True
    elif replacement in content:
        print(f"  Composition.tsx already uses {audio_rel_path} — no patch needed.")
        return True
    else:
        print(f"  No shared bg-music reference found in Composition.tsx — skipping patch.")
        print(f"  You may need to manually add: <Audio src={{staticFile('{audio_rel_path}')}} volume={{0.08}} />")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate custom background music for a Remotion video composition."
    )
    parser.add_argument("animation_name", help="Name of the animation (e.g., CareerLadder)")
    parser.add_argument("--prompt", help="Custom music prompt (overrides auto-detection)")
    parser.add_argument("--duration", type=float, help="Duration in seconds (overrides auto-detection from timing.ts)")
    parser.add_argument("--no-update", action="store_true", help="Skip patching Composition.tsx")
    parser.add_argument("--dry-run", action="store_true", help="Preview settings without calling the API")
    parser.add_argument("--vocals", action="store_true", help="Allow vocals (default: instrumental only)")
    parser.add_argument("--multi-segment", action="store_true",
                        help="Generate 3 tracks: bg-music-hook.mp3, bg-music-body.mp3, bg-music-cta.mp3")
    parser.add_argument("--no-metadata", action="store_true",
                        help="Skip writing bg-music-metadata.json (written by default in --multi-segment)")
    parser.add_argument("--hook-bpm", type=str, default="100-110",
                        help="BPM range for hook segment (default: 100-110)")
    parser.add_argument("--body-bpm", type=str, default="75-90",
                        help="BPM range for body segment (default: 75-90)")
    parser.add_argument("--cta-bpm", type=str, default="110-120",
                        help="BPM range for CTA segment (default: 110-120)")
    parser.add_argument("--hook-mood", type=str, default=None,
                        help="Music mood for hook segment (overrides auto-detection from tone)")
    args = parser.parse_args()

    animation_name = args.animation_name
    audio_dir_name = animation_name.lower()
    output_path = os.path.join("public", "audio", audio_dir_name, "bg-music.mp3")
    audio_rel_path = f"audio/{audio_dir_name}/bg-music.mp3"

    # Check animation exists
    src_dir = Path("src") / animation_name
    if not src_dir.exists():
        print(f"Error: {src_dir} not found!")
        sys.exit(1)

    # Resolve duration
    if args.duration:
        duration = args.duration
        print(f"  Duration: {duration:.1f}s (from --duration flag)")
    else:
        duration = extract_duration_from_timing(animation_name)
        if duration:
            print(f"  Duration: {duration:.1f}s (auto-detected from timing.ts)")
        else:
            print("Error: Could not auto-detect duration from timing.ts.")
            print("       Provide --duration <seconds> or ensure timing.ts has TOTAL_FRAMES.")
            sys.exit(1)

    # Resolve prompt
    if args.prompt:
        prompt = args.prompt
        print(f"  Prompt: {prompt} (from --prompt flag)")
    else:
        prompt = extract_prompt_from_brief(animation_name)
        print(f"  Prompt: {prompt}")

    force_instrumental = not args.vocals

    # Summary
    print(f"\n{'='*60}")
    print(f"Background Music Generation: {animation_name}")
    print(f"{'='*60}")
    print(f"  Output:       {output_path}")
    print(f"  Duration:     {duration:.1f}s")
    print(f"  Instrumental: {force_instrumental}")
    print(f"  Prompt:       {prompt}")
    print(f"  Patch Comp:   {'no (--no-update)' if args.no_update else 'yes'}")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("DRY RUN — No API call will be made.\n")
        if args.multi_segment:
            for suffix in ("hook", "body", "cta"):
                seg_path = os.path.join("public", "audio", audio_dir_name, f"bg-music-{suffix}.mp3")
                print(f"  [{'EXISTS' if os.path.exists(seg_path) else 'NEW':6s}] {seg_path}")
        else:
            if os.path.exists(output_path):
                print(f"  [EXISTS] {output_path}")
            else:
                print(f"  [NEW]    {output_path}")
        return

    # Multi-segment mode: generate 3 tracks for hook / body / CTA
    if args.multi_segment:
        # Resolve hook mood: --hook-mood flag > auto-detected from tone
        hook_mood = args.hook_mood
        if not hook_mood:
            # Try to extract tone from brief and map it
            brief_path = Path("src") / animation_name / "research" / "content-brief.md"
            if brief_path.exists():
                brief_content = brief_path.read_text(encoding="utf-8")
                for pattern in [r'\*\*[Tt]one:?\*\*:?\s*[`"]*([A-Za-z\-]+)', r'[Tt]one\s*:\s*[`"]*([a-z\-]+)[`"]*']:
                    m = re.search(pattern, brief_content)
                    if m:
                        hook_mood = m.group(1).strip().lower()
                        break
            if not hook_mood:
                hook_mood = "dramatic-cinematic"

        # Build per-segment prompts with BPM from args
        hook_prompt_base = TONE_MUSIC_MAP.get(hook_mood, TONE_MUSIC_MAP.get("dramatic-cinematic", DEFAULT_MUSIC_PROMPT))
        segments = [
            ("hook", f"{hook_prompt_base}, {args.hook_bpm} BPM, energetic, for hook section"),
            ("body", f"{prompt}, {args.body_bpm} BPM, ambient minimal, for explanation section"),
            ("cta",  f"{prompt}, {args.cta_bpm} BPM, upbeat, for call-to-action section"),
        ]

        # Parse BPM midpoints for metadata
        def parse_bpm_mid(bpm_str: str) -> int:
            parts = bpm_str.split("-")
            return int((int(parts[0]) + int(parts[-1])) / 2) if len(parts) == 2 else int(parts[0])

        segment_meta = {}
        for suffix, seg_prompt in segments:
            seg_path = os.path.join("public", "audio", audio_dir_name, f"bg-music-{suffix}.mp3")
            print(f"\nGenerating {suffix} segment: {seg_path}")
            print(f"  Prompt: {seg_prompt}")

            if not args.dry_run:
                try:
                    generate_background_music(
                        prompt=seg_prompt,
                        duration_seconds=duration / 3,
                        output_path=seg_path,
                        force_instrumental=force_instrumental,
                    )
                except Exception as e:
                    print(f"\nError generating {suffix} segment: {e}")
                    sys.exit(1)

            bpm_arg = {"hook": args.hook_bpm, "body": args.body_bpm, "cta": args.cta_bpm}[suffix]
            segment_meta[suffix] = {
                "file": f"bg-music-{suffix}.mp3",
                "bpm": parse_bpm_mid(bpm_arg),
                "bpm_range": bpm_arg,
                "prompt": seg_prompt,
            }

        # Write metadata JSON (unless --no-metadata)
        if not args.no_metadata:
            import json
            metadata_path = os.path.join("public", "audio", audio_dir_name, "bg-music-metadata.json")
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(segment_meta, f, indent=2)
            print(f"\n  Metadata written: {metadata_path}")

        print(f"\n{'='*60}")
        print(f"Multi-segment music saved to public/audio/{audio_dir_name}/")
        print(f"\nAdd to Composition.tsx:")
        print(f"  {{/* Hook music: energetic, {args.hook_bpm} BPM */}}")
        print(f"  <Sequence from={{0}} durationInFrames={{SCENES.hook.duration}}>")
        print(f"    <Audio src={{staticFile('audio/{audio_dir_name}/bg-music-hook.mp3')}} volume={{(f) =>")
        print(f"      interpolate(f, [0, 15, SCENES.hook.duration - 45, SCENES.hook.duration], [0, 0.12, 0.12, 0],")
        print(f"        {{ extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }})}} />")
        print(f"  </Sequence>")
        print(f"  {{/* Body music: ambient, {args.body_bpm} BPM */}}")
        print(f"  <Sequence from={{SCENES.hook.duration}} durationInFrames={{MIDROLL_START - SCENES.hook.duration}}>")
        print(f"    <Audio src={{staticFile('audio/{audio_dir_name}/bg-music-body.mp3')}} volume={{0.07}} />")
        print(f"  </Sequence>")
        print(f"  {{/* CTA music: upbeat, {args.cta_bpm} BPM */}}")
        print(f"  <Sequence from={{CTA_START}} durationInFrames={{OUTRO_START - CTA_START}}>")
        print(f"    <Audio src={{staticFile('audio/{audio_dir_name}/bg-music-cta.mp3')}} volume={{(f) =>")
        print(f"      interpolate(f, [0, 30, (OUTRO_START - CTA_START) - 60, OUTRO_START - CTA_START], [0, 0.12, 0.12, 0],")
        print(f"        {{ extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }})}} />")
        print(f"  </Sequence>")
        print(f"{'='*60}")
        return

    # Check for existing file
    if os.path.exists(output_path):
        print(f"  Overwriting existing: {output_path}")

    # Generate
    try:
        result = generate_background_music(
            prompt=prompt,
            duration_seconds=duration,
            output_path=output_path,
            force_instrumental=force_instrumental,
        )
    except Exception as e:
        print(f"\nError generating music: {e}")
        sys.exit(1)

    # Patch Composition.tsx
    if not args.no_update:
        print()
        patch_composition(animation_name, audio_rel_path)

    # Final summary
    print(f"\n{'='*60}")
    print(f"Done! Background music saved to {output_path}")
    if result.get("warn_loop"):
        print(f"  TIP: Video is >10 min. Add `loop` prop to <Audio> in Composition.tsx:")
        print(f"       <Audio src={{staticFile('{audio_rel_path}')}} volume={{0.08}} loop />")
    print(f"\n  Volume tuning: Adjust `volume={{0.04}}` in Composition.tsx if needed.")
    print(f"  Typical range: 0.02 (barely perceptible) to 0.06 (clearly audible).")
    print(f"  IMPORTANT: Music must never compete with narration. Start low (0.03-0.04).")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
