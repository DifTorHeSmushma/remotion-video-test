"""
Batch audio generation for all scenes of a video composition.

Usage:
  python generate-all-audio.py <AnimationName> [--parallel N]

Example:
  python generate-all-audio.py DockerSandboxes3Min              # sequential (default)
  python generate-all-audio.py DockerSandboxes3Min --parallel 5  # 5 concurrent API calls

This reads all scene-*.txt files from src/<AnimationName>/scripts/,
generates audio + sync JSON for each, and prints a timing.ts update.

Parallel mode uses ThreadPoolExecutor for concurrent ElevenLabs API calls.
ElevenLabs Pro tier supports up to 10 concurrent requests; default is 5 for safety.
Free/Starter tiers should use --parallel 1 (sequential).
"""

import os
import sys
import glob
import math
import re
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from text_to_speech_lib import generate_synced_audio
from dotenv import load_dotenv

load_dotenv()

VOICE_ID = os.getenv("VOICE_ID") or "JBFqnCBsd6RMkjVDRZzb"
FPS = 30
AUDIO_OFFSET_PREVIEW = 10 # frames before audio starts in scene 0 (preview)
AUDIO_OFFSET_FIRST = 15  # frames before audio starts in scene 1
AUDIO_OFFSET_REST = 10   # frames before audio starts in scenes 2+
BUFFER_FRAMES = 15       # padding after audio ends
TRANSITION_DURATION = 15 # TransitionSeries overlap between scenes


def get_scene_number(filename: str) -> int:
    match = re.search(r'scene-(\d+)', filename)
    return int(match.group(1)) if match else 0


def process_scene(script_file: str, audio_dir: str, scripts_dir: str, chunk_mode: str = "none") -> dict | None:
    """Process a single scene: read script, call TTS API, return timing info."""
    basename = os.path.basename(script_file)
    scene_num = get_scene_number(basename)
    scene_name = f"scene{scene_num:02d}"

    with open(script_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"  Skipping {basename} (empty)")
        return None

    output_mp3 = os.path.join(audio_dir, f"{scene_name}.mp3")
    output_json = os.path.join(scripts_dir, f"{scene_name}-sync.json")
    history_path = os.path.join(scripts_dir, f"{scene_name}-history.json")

    print(f"--- Scene {scene_num:02d} ---")
    is_preview = scene_num == 0
    words_data = generate_synced_audio(
        text, output_mp3, output_json, VOICE_ID,
        is_preview=is_preview,
        chunk_mode=chunk_mode,
        history_path=history_path,
    )

    audio_duration = words_data[-1]["end"] if words_data else 0
    if scene_num == 0:
        audio_offset = AUDIO_OFFSET_PREVIEW
    elif scene_num == 1:
        audio_offset = AUDIO_OFFSET_FIRST
    else:
        audio_offset = AUDIO_OFFSET_REST
    scene_duration = audio_offset + math.ceil(audio_duration * FPS) + BUFFER_FRAMES

    name_part = basename.replace("scene-", "").replace(".txt", "")
    return {
        "num": scene_num,
        "name": name_part.split("-", 1)[-1] if "-" in name_part else name_part,
        "duration": scene_duration,
        "audio_seconds": audio_duration,
    }


def main():
    parser = argparse.ArgumentParser(description="Batch audio generation for video compositions")
    parser.add_argument("animation_name", help="AnimationName (folder name under src/)")
    parser.add_argument("--parallel", type=int, default=1, metavar="N",
                        help="Number of concurrent API calls (default: 1, max recommended: 5 for Pro tier)")
    parser.add_argument("--chunk", choices=["none", "sentence"], default="none",
                        help="'sentence' splits each scene into chunks for cheap per-sentence regeneration via regen-changed.py. Default: 'none' (single API call per scene).")
    args = parser.parse_args()

    animation_name = args.animation_name
    max_workers = max(1, min(args.parallel, 10))  # clamp to 1-10
    scripts_dir = os.path.join("src", animation_name, "scripts")
    audio_dir = os.path.join("public", "audio", animation_name.lower())

    if not os.path.isdir(scripts_dir):
        print(f"Error: {scripts_dir} not found!")
        sys.exit(1)

    # Find all scene script files
    script_files = sorted(
        glob.glob(os.path.join(scripts_dir, "scene-*.txt")),
        key=lambda f: get_scene_number(os.path.basename(f))
    )

    if not script_files:
        print(f"No scene-*.txt files found in {scripts_dir}")
        sys.exit(1)

    print(f"Found {len(script_files)} scene scripts in {scripts_dir}")
    if max_workers > 1:
        print(f"Parallel mode: {max_workers} concurrent API calls\n")
    else:
        print(f"Sequential mode (use --parallel N for concurrent generation)\n")

    start_time = time.time()
    scenes_timing = []
    errors = []

    if max_workers > 1:
        # Parallel: submit all scenes to thread pool
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_scene, sf, audio_dir, scripts_dir, args.chunk): sf
                for sf in script_files
            }
            for future in as_completed(future_to_file):
                sf = future_to_file[future]
                try:
                    result = future.result()
                    if result is not None:
                        scenes_timing.append(result)
                except Exception as e:
                    errors.append((os.path.basename(sf), str(e)))
                    print(f"  ERROR generating {os.path.basename(sf)}: {e}")
    else:
        # Sequential: original behavior
        for script_file in script_files:
            try:
                result = process_scene(script_file, audio_dir, scripts_dir, args.chunk)
                if result is not None:
                    scenes_timing.append(result)
            except Exception as e:
                errors.append((os.path.basename(script_file), str(e)))
                print(f"  ERROR generating {os.path.basename(script_file)}: {e}")
            print()

    # Sort by scene number (parallel mode returns in completion order)
    scenes_timing.sort(key=lambda s: s["num"])

    elapsed = time.time() - start_time

    if errors:
        print(f"\n{'!' * 60}")
        print(f"WARNING: {len(errors)} scene(s) failed:")
        for name, err in errors:
            print(f"  - {name}: {err}")
        print(f"{'!' * 60}")

    # Print timing.ts content
    print("\n" + "=" * 60)
    print("Update your constants/timing.ts with:\n")

    current_start = 0
    scene_names = []
    for s in scenes_timing:
        # Extract a clean key name from the filename
        key = re.sub(r'^\d+-', '', s["name"]).replace("-", "")
        scene_names.append(key)
        print(f"  {key}: {{ start: {current_start}, duration: {s['duration']} }},  // {s['audio_seconds']:.1f}s audio")
        current_start += s["duration"] - TRANSITION_DURATION

    total = sum(s["duration"] for s in scenes_timing)
    print(f"\nTOTAL_FRAMES = {total}  ({total / FPS:.1f}s)")
    print(f"\nGenerated {len(scenes_timing)} scenes in {elapsed:.1f}s", end="")
    if max_workers > 1:
        print(f" ({max_workers} parallel workers)")
    else:
        print(" (sequential)")
    print("=" * 60)


if __name__ == "__main__":
    main()
