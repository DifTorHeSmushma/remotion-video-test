"""
Core ElevenLabs Music API generation for background music tracks.
Shared by generate-bg-music.py (CLI) and available for programmatic use.
"""

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# API limits
MIN_DURATION_MS = 3_000      # 3 seconds
MAX_DURATION_MS = 600_000    # 10 minutes
LOOP_WARN_MS = 600_000       # Warn if video > 10 min (suggest loop prop)


def generate_background_music(
    prompt: str,
    duration_seconds: float,
    output_path: str,
    force_instrumental: bool = True,
) -> dict:
    """
    Generate a background music track using ElevenLabs Music API.

    Args:
        prompt: Text description of desired music style/mood.
        duration_seconds: Target duration in seconds.
        output_path: Path to write the output .mp3 file.
        force_instrumental: If True, guarantees no vocals (default True).

    Returns:
        dict with keys: success (bool), path (str), duration_ms (int),
        warn_loop (bool — True if video > 10 min, suggest Remotion loop prop).
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing ELEVENLABS_API_KEY in .env file!")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    duration_ms = int(duration_seconds * 1000)
    warn_loop = duration_ms > LOOP_WARN_MS

    # Clamp to API limits
    clamped_ms = max(MIN_DURATION_MS, min(duration_ms, MAX_DURATION_MS))
    if clamped_ms != duration_ms:
        print(f"  Duration clamped: {duration_ms}ms -> {clamped_ms}ms (API range: {MIN_DURATION_MS}-{MAX_DURATION_MS}ms)")

    print(f"  Generating background music...")
    print(f"  Prompt: {prompt}")
    print(f"  Duration: {clamped_ms / 1000:.1f}s ({clamped_ms}ms)")
    print(f"  Instrumental: {force_instrumental}")

    audio = client.music.compose(
        prompt=prompt,
        music_length_ms=clamped_ms,
        force_instrumental=force_instrumental,
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write streaming chunks to file
    total_bytes = 0
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
            total_bytes += len(chunk)

    print(f"  Saved: {output_path} ({total_bytes / 1024:.0f} KB)")

    if warn_loop:
        print(f"  WARNING: Video is longer than 10 minutes. Music track is capped at 10 min.")
        print(f"           Use <Audio loop /> in Remotion to loop the track.")

    return {
        "success": True,
        "path": output_path,
        "duration_ms": clamped_ms,
        "warn_loop": warn_loop,
    }
