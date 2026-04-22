"""
Generate ElevenLabs TTS audio with word-level sync timestamps for a single scene.

Usage:
  python text-to-speech.py --input <script.txt> --output-dir <audio-dir> --sync-dir <json-dir> --name <sceneNN>

Example:
  python text-to-speech.py \
    --input src/DockerSandboxes3Min/scripts/scene-01-hook.txt \
    --output-dir public/audio/docker-sandboxes/ \
    --sync-dir src/DockerSandboxes3Min/scripts/ \
    --name scene01
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from text_to_speech_lib import generate_synced_audio

load_dotenv()

VOICE_ID = os.getenv("VOICE_ID")


def main():
    parser = argparse.ArgumentParser(description="Generate ElevenLabs TTS with word-level sync timestamps")
    parser.add_argument("--input", "-i", required=True, help="Path to text file containing the narration script")
    parser.add_argument("--output-dir", "-o", required=True, help="Directory for the .mp3 output")
    parser.add_argument("--sync-dir", "-s", required=True, help="Directory for the .json sync output")
    parser.add_argument("--name", "-n", required=True, help="Output filename prefix (e.g., scene01)")
    parser.add_argument("--voice-id", "-v", default=None, help="ElevenLabs voice ID (overrides .env VOICE_ID)")
    parser.add_argument("--shorts", action="store_true", help="Use faster speed setting for Shorts (ELEVENLABS_SPEED_SHORTS)")
    parser.add_argument("--preview", action="store_true", help="Use faster speed setting for Preview hooks (ELEVENLABS_SPEED_PREVIEW)")
    parser.add_argument("--speed", type=float, default=None, help="Override TTS speed (e.g., 1.15 for Spanish)")
    parser.add_argument("--chunk", choices=["none", "sentence"], default="none",
                        help="'sentence' splits the script into sentence-sized chunks for cheap per-sentence regeneration (writes {name}-chunks/ and {name}-history.json). Default: 'none' (single API call).")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"Error: Input file {args.input} is empty!", file=sys.stderr)
        sys.exit(1)

    voice_id = args.voice_id or VOICE_ID or "JBFqnCBsd6RMkjVDRZzb"

    output_mp3 = os.path.join(args.output_dir, f"{args.name}.mp3")
    output_json = os.path.join(args.sync_dir, f"{args.name}-sync.json")
    history_path = os.path.join(args.sync_dir, f"{args.name}-history.json")

    generate_synced_audio(
        text, output_mp3, output_json, voice_id,
        is_short=args.shorts, is_preview=args.preview, speed_override=args.speed,
        chunk_mode=args.chunk, history_path=history_path,
    )


if __name__ == "__main__":
    main()
