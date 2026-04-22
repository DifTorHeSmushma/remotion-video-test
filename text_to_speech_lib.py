"""
Core ElevenLabs TTS generation with word-level sync timestamps.
Shared by text-to-speech.py (single scene) and generate-all-audio.py (batch).
"""

import os
import re
import json
import base64
import hashlib
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Voice settings from .env (with API defaults as fallbacks)
VOICE_STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.5"))
VOICE_SIMILARITY_BOOST = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75"))
VOICE_STYLE = float(os.getenv("ELEVENLABS_STYLE", "0.0"))
VOICE_SPEED = float(os.getenv("ELEVENLABS_SPEED", "1.0"))
VOICE_SPEED_SHORTS = float(os.getenv("ELEVENLABS_SPEED_SHORTS", "1.15"))
VOICE_SPEED_PREVIEW = float(os.getenv("ELEVENLABS_SPEED_PREVIEW", "1.15"))
VOICE_USE_SPEAKER_BOOST = os.getenv("ELEVENLABS_USE_SPEAKER_BOOST", "true").lower() == "true"


def clean_sync_data(words_data: list) -> list:
    """
    Clean ElevenLabs sync data by removing SSML tag artifacts.

    Fixes three problems:
    1. Ghost Words: Entries like "<break" or 'time="0.4s"/>' that are SSML fragments
    2. Combined Leakage: Words like "choices:<break" that merge text with SSML
    3. Timing Tightening: Ensures no word's end exceeds next word's start
    """
    cleaned = []

    for entry in words_data:
        word = entry["word"]
        start = entry["start"]
        end = entry["end"]

        # 1. Clean SSML tags from word text
        clean_word = re.sub(r'<break[^>]*>?', '', word)           # Remove <break...>
        clean_word = re.sub(r'time="[^"]*"\s*/?>', '', clean_word) # Remove time="..."/>
        clean_word = re.sub(r'/>', '', clean_word)                  # Remove stray />
        clean_word = clean_word.strip().strip('\n')

        # 2. Skip entries that are empty after cleaning (pure SSML fragments)
        if not clean_word:
            continue

        cleaned.append({
            "word": clean_word,
            "start": start,
            "end": end,
        })

    # 4. Tighten timing: ensure no word's end exceeds next word's start
    for i in range(len(cleaned) - 1):
        if cleaned[i]["end"] > cleaned[i + 1]["start"]:
            cleaned[i]["end"] = cleaned[i + 1]["start"]

    return cleaned


# ---------------------------------------------------------------------------
# Chunked generation (sentence-level) + delta-regen support
# ---------------------------------------------------------------------------

# Abbreviations whose trailing '.' does NOT end a sentence.
# Kept as a set of the exact surface form we expect to find in scripts.
_ABBREVIATIONS = {
    "Dr.", "Mr.", "Mrs.", "Ms.", "Jr.", "Sr.", "St.",
    "e.g.", "i.e.", "etc.", "vs.", "viz.", "cf.",
    "U.S.", "U.K.", "E.U.", "A.I.", "N.B.",
    "a.m.", "p.m.", "A.M.", "P.M.",
    "Inc.", "Ltd.", "Co.", "Corp.",
    "No.", "Vol.", "Ch.", "pp.", "ed.", "approx.",
}

# Sentence boundary: a terminator followed by whitespace followed by a capital
# letter, digit, or opening quote. The whitespace group is captured so we can
# rebuild the original spacing if needed.
_SENTENCE_BOUNDARY = re.compile(r'(?<=[.!?])(\s+)(?=[A-Z0-9"\'])')

# Secondary split points for oversized sentences (semicolons, colons).
_SECONDARY_BOUNDARY = re.compile(r'(?<=[;:])\s+')


def split_into_chunks(text: str, min_chars: int = 40, max_chars: int = 400) -> list[str]:
    """Split text into sentence-sized chunks for per-chunk TTS generation.

    Sentences shorter than ``min_chars`` are merged forward so TTS prosody
    doesn't degrade on tiny fragments. Sentences longer than ``max_chars`` are
    split on secondary boundaries (``;`` / ``:``) to keep per-chunk regen cheap.
    Abbreviations from ``_ABBREVIATIONS`` are protected from false splits.
    """
    sentinel = "\x00"
    protected = text
    for abbrev in _ABBREVIATIONS:
        protected = protected.replace(abbrev, abbrev.replace(".", sentinel))

    parts = _SENTENCE_BOUNDARY.split(protected)
    sentences: list[str] = []
    i = 0
    while i < len(parts):
        s = parts[i].replace(sentinel, ".").strip()
        if s:
            sentences.append(s)
        # The split captures the whitespace group at odd indices — skip it.
        i += 2

    merged: list[str] = []
    buffer = ""
    for s in sentences:
        if not buffer:
            buffer = s
            continue
        if len(buffer) < min_chars:
            buffer = buffer + " " + s
        else:
            merged.append(buffer)
            buffer = s
    if buffer:
        merged.append(buffer)

    final: list[str] = []
    for s in merged:
        if len(s) <= max_chars:
            final.append(s)
            continue
        sub_parts = _SECONDARY_BOUNDARY.split(s)
        running = ""
        for sub in sub_parts:
            sub = sub.strip()
            if not sub:
                continue
            candidate = (running + " " + sub).strip() if running else sub
            if len(candidate) <= max_chars or not running:
                running = candidate
            else:
                final.append(running)
                running = sub
        if running:
            final.append(running)

    return final


def compute_checksum(text: str) -> str:
    """SHA-256 of whitespace-normalized text. Used as the delta-regen key."""
    normalized = " ".join(text.split())
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_mp3_duration(mp3_path: str) -> float:
    """Read exact MP3 duration in seconds via ffprobe.

    We read the container duration rather than ``words[-1]['end']`` because
    ElevenLabs often appends trailing silence that sync data does not cover.
    When concatenating chunks, using the sync end time causes cumulative drift.
    """
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            mp3_path,
        ],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


# Inter-chunk silence restores the natural sentence-boundary pauses that
# ElevenLabs inserts when processing longer text in a single call. Measured
# empirically on a 1204-char / 11-chunk scene: 650ms lands within 200ms of
# the reference single-call duration (79.595s reference vs 79.778s merged).
DEFAULT_INTER_CHUNK_SILENCE_MS = 650


def _get_silence_mp3(duration_ms: int) -> str:
    """Return a path to a cached silent MP3 of the given duration.

    Uses the same codec params as ElevenLabs output (mp3, 44100 Hz, 128 kbps,
    mono->stereo-compatible) so the concat demuxer's ``-c copy`` mode accepts
    the file without re-encoding. Cached in the OS temp dir to avoid
    regenerating across invocations.
    """
    cache_dir = Path(tempfile.gettempdir()) / "diy-tts-silence"
    cache_dir.mkdir(exist_ok=True)
    silence_path = cache_dir / f"silence-{duration_ms}ms.mp3"
    if silence_path.exists() and silence_path.stat().st_size > 0:
        return str(silence_path)

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi",
            "-i", f"anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", f"{duration_ms / 1000.0:.3f}",
            "-c:a", "libmp3lame", "-b:a", "128k",
            str(silence_path),
        ],
        check=True,
    )
    return str(silence_path)


def concat_mp3s(
    chunk_paths: list[str],
    output_path: str,
    inter_chunk_silence_ms: int = 0,
) -> None:
    """Concatenate MP3 chunks losslessly via ffmpeg's concat demuxer.

    All ElevenLabs output is ``mp3_44100_128`` CBR, so ``-c copy`` produces a
    click-free merge with no re-encoding. When ``inter_chunk_silence_ms > 0``,
    a cached silent MP3 of that duration is inserted between chunks to restore
    the natural sentence-boundary pauses lost when the text is split across
    multiple API calls. Requires ffmpeg in PATH.
    """
    silence_path = (
        _get_silence_mp3(inter_chunk_silence_ms)
        if inter_chunk_silence_ms > 0
        else None
    )

    list_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            list_path = f.name
            for i, p in enumerate(chunk_paths):
                if i > 0 and silence_path is not None:
                    sp = os.path.abspath(silence_path).replace("\\", "/")
                    f.write(f"file '{sp}'\n")
                abs_path = os.path.abspath(p).replace("\\", "/")
                f.write(f"file '{abs_path}'\n")

        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-f", "concat", "-safe", "0",
                "-i", list_path,
                "-c", "copy",
                output_path,
            ],
            check=True,
        )
    finally:
        if list_path and os.path.exists(list_path):
            os.unlink(list_path)


def merge_chunk_syncs(
    chunks_data: list[dict],
    inter_chunk_silence_ms: int = 0,
) -> list[dict]:
    """Merge per-chunk word lists into a single continuous timeline.

    Each entry in ``chunks_data`` must supply:
      - ``words``: list of {word, start, end} from the per-chunk TTS call
      - ``duration``: actual MP3 duration in seconds (from ``get_mp3_duration``)

    ``inter_chunk_silence_ms`` MUST match the value passed to ``concat_mp3s``
    for the same generation — otherwise word timestamps will drift out of sync
    with the merged audio. Returns a flat word list with absolute timestamps,
    tightened so no word's end exceeds the next word's start.
    """
    silence_seconds = inter_chunk_silence_ms / 1000.0
    merged: list[dict] = []
    cursor = 0.0
    for idx, ch in enumerate(chunks_data):
        if idx > 0:
            cursor += silence_seconds
        for w in ch["words"]:
            merged.append({
                "word": w["word"],
                "start": w["start"] + cursor,
                "end": w["end"] + cursor,
            })
        cursor += ch["duration"]

    for i in range(len(merged) - 1):
        if merged[i]["end"] > merged[i + 1]["start"]:
            merged[i]["end"] = merged[i + 1]["start"]

    return merged


def generate_chunk(
    text: str,
    voice_id: str,
    speed: float | None = None,
    is_short: bool = False,
    is_preview: bool = False,
) -> tuple[bytes, list[dict]]:
    """Generate audio for a single chunk and return raw bytes + cleaned words.

    Unlike ``generate_synced_audio``, this does not write any files — the
    caller is responsible for persisting the MP3 and sync data. This keeps
    the function usable both for first-time full generation and for
    selective re-generation of individual chunks.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing ELEVENLABS_API_KEY in .env file!")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    if speed is None:
        if is_preview:
            speed = VOICE_SPEED_PREVIEW
        elif is_short:
            speed = VOICE_SPEED_SHORTS
        else:
            speed = VOICE_SPEED

    voice_settings = VoiceSettings(
        stability=VOICE_STABILITY,
        similarity_boost=VOICE_SIMILARITY_BOOST,
        style=VOICE_STYLE,
        speed=speed,
        use_speaker_boost=VOICE_USE_SPEAKER_BOOST,
    )

    response = client.text_to_speech.stream_with_timestamps(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings=voice_settings,
    )

    audio_chunks: list[bytes] = []
    characters: list[str] = []
    starts: list[float] = []
    ends: list[float] = []

    for chunk in response:
        if hasattr(chunk, "audio_base_64") and chunk.audio_base_64:
            audio_chunks.append(base64.b64decode(chunk.audio_base_64))
        if hasattr(chunk, "alignment") and chunk.alignment:
            characters.extend(chunk.alignment.characters)
            starts.extend(chunk.alignment.character_start_times_seconds)
            ends.extend(chunk.alignment.character_end_times_seconds)

    words_data: list[dict] = []
    current_word = ""
    word_start = 0.0
    for i, char in enumerate(characters):
        if current_word == "":
            word_start = starts[i]
        current_word += char
        if char == " " or i == len(characters) - 1:
            words_data.append({
                "word": current_word.strip(),
                "start": word_start,
                "end": ends[i],
            })
            current_word = ""

    words_data = clean_sync_data(words_data)
    return b"".join(audio_chunks), words_data


def generate_synced_audio_chunked(
    text: str,
    output_mp3: str,
    output_json: str,
    voice_id: str,
    history_path: str,
    chunks_dir: str | None = None,
    inter_chunk_silence_ms: int = DEFAULT_INTER_CHUNK_SILENCE_MS,
    is_short: bool = False,
    is_preview: bool = False,
    speed_override: float | None = None,
) -> list[dict]:
    """Full sentence-chunked generation. No delta logic — this is the
    first-time/fresh-regen path. For selective regeneration on script edits,
    use ``regen-changed.py`` which diffs checksums against an existing
    ``history.json`` and only re-hits the API for changed chunks.

    Writes:
      {chunks_dir}/chunk-NN.mp3            — individual chunk audio
      {chunks_dir}/chunk-NN-sync.json      — per-chunk word timestamps (local)
      {output_mp3}                         — merged audio (the file scenes play)
      {output_json}                        — merged sync (the file scenes import)
      {history_path}                       — chunk metadata + checksums

    Returns the merged words list.
    """
    if chunks_dir is None:
        base = Path(output_mp3)
        chunks_dir = str(base.parent / f"{base.stem}-chunks")
    chunks_dir_p = Path(chunks_dir)
    chunks_dir_p.mkdir(parents=True, exist_ok=True)

    if speed_override is not None:
        speed = speed_override
    elif is_preview:
        speed = VOICE_SPEED_PREVIEW
    elif is_short:
        speed = VOICE_SPEED_SHORTS
    else:
        speed = VOICE_SPEED

    chunks = split_into_chunks(text)
    print(f"  Generating: {os.path.basename(output_mp3)} [chunked]")
    print(f"  Text: {len(text)} chars, ~{len(text.split())} words, {len(chunks)} chunks")

    history_entries: list[dict] = []
    chunks_data: list[dict] = []

    for i, chunk_text in enumerate(chunks):
        chunk_mp3 = chunks_dir_p / f"chunk-{i:02d}.mp3"
        chunk_sync = chunks_dir_p / f"chunk-{i:02d}-sync.json"
        mp3_bytes, words = generate_chunk(
            chunk_text, voice_id, speed=speed,
            is_short=is_short, is_preview=is_preview,
        )
        chunk_mp3.write_bytes(mp3_bytes)
        with open(chunk_sync, "w", encoding="utf-8") as f:
            json.dump({"words": words}, f, indent=2)

        duration = get_mp3_duration(str(chunk_mp3))
        history_entries.append({
            "index": i,
            "text": chunk_text,
            "checksum": compute_checksum(chunk_text),
            "mp3": f"chunk-{i:02d}.mp3",
            "duration": duration,
            "word_count": len(words),
        })
        chunks_data.append({"words": words, "duration": duration})

    # words_offset lets regen-changed.py splice per-chunk word slices into the
    # merged array without re-running all syncs.
    cursor = 0
    for entry in history_entries:
        entry["words_offset"] = cursor
        cursor += entry["word_count"]

    os.makedirs(os.path.dirname(output_mp3), exist_ok=True)
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    os.makedirs(os.path.dirname(history_path), exist_ok=True)

    concat_mp3s(
        [str(chunks_dir_p / f"chunk-{i:02d}.mp3") for i in range(len(chunks))],
        output_mp3,
        inter_chunk_silence_ms=inter_chunk_silence_ms,
    )

    merged_words = merge_chunk_syncs(chunks_data, inter_chunk_silence_ms=inter_chunk_silence_ms)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"words": merged_words}, f, indent=4)

    bundle = {
        "voice_id": voice_id,
        "speed": speed,
        "model": "eleven_multilingual_v2",
        "inter_chunk_silence_ms": inter_chunk_silence_ms,
        "chunks": history_entries,
    }
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)

    total_duration = get_mp3_duration(output_mp3)
    print(f"  Duration: {total_duration:.2f}s ({int(total_duration * 30)} frames at 30fps), {len(merged_words)} words")

    return merged_words


def generate_synced_audio(text: str, output_mp3: str, output_json: str, voice_id: str, is_short: bool = False, is_preview: bool = False, speed_override: float = None, chunk_mode: str = "none", history_path: str | None = None, inter_chunk_silence_ms: int = DEFAULT_INTER_CHUNK_SILENCE_MS) -> list:
    if chunk_mode == "sentence":
        if history_path is None:
            # Default: alongside the sync JSON, named {scene}-history.json
            hp = Path(output_json)
            history_path = str(hp.parent / hp.name.replace("-sync.json", "-history.json"))
        return generate_synced_audio_chunked(
            text, output_mp3, output_json, voice_id,
            history_path=history_path,
            inter_chunk_silence_ms=inter_chunk_silence_ms,
            is_short=is_short, is_preview=is_preview, speed_override=speed_override,
        )
    elif chunk_mode != "none":
        raise ValueError(f"chunk_mode must be 'none' or 'sentence', got {chunk_mode!r}")

    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing ELEVENLABS_API_KEY in .env file!")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Use appropriate speed based on mode or override
    if speed_override is not None:
        speed = speed_override
    elif is_preview:
        speed = VOICE_SPEED_PREVIEW
    elif is_short:
        speed = VOICE_SPEED_SHORTS
    else:
        speed = VOICE_SPEED

    print(f"  Generating: {os.path.basename(output_mp3)}")
    print(f"  Text: {len(text)} chars, ~{len(text.split())} words")
    if speed_override is not None:
        print(f"  Mode: CUSTOM SPEED (speed={speed})")
    elif is_preview:
        print(f"  Mode: PREVIEW (speed={speed})")
    elif is_short:
        print(f"  Mode: SHORT (speed={speed})")

    voice_settings = VoiceSettings(
        stability=VOICE_STABILITY,
        similarity_boost=VOICE_SIMILARITY_BOOST,
        style=VOICE_STYLE,
        speed=speed,
        use_speaker_boost=VOICE_USE_SPEAKER_BOOST,
    )

    response = client.text_to_speech.stream_with_timestamps(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings=voice_settings,
    )

    audio_chunks = []
    characters = []
    starts = []
    ends = []

    for chunk in response:
        if hasattr(chunk, 'audio_base_64') and chunk.audio_base_64:
            audio_chunks.append(base64.b64decode(chunk.audio_base_64))

        if hasattr(chunk, 'alignment') and chunk.alignment:
            characters.extend(chunk.alignment.characters)
            starts.extend(chunk.alignment.character_start_times_seconds)
            ends.extend(chunk.alignment.character_end_times_seconds)

    # Group characters into words
    words_data = []
    current_word = ""
    word_start = 0

    for i, char in enumerate(characters):
        if current_word == "":
            word_start = starts[i]
        current_word += char
        if char == " " or i == len(characters) - 1:
            words_data.append({
                "word": current_word.strip(),
                "start": word_start,
                "end": ends[i]
            })
            current_word = ""

    # Clean SSML artifacts from sync data
    raw_count = len(words_data)
    words_data = clean_sync_data(words_data)
    if raw_count != len(words_data):
        print(f"  Cleaned sync data: {raw_count} -> {len(words_data)} entries ({raw_count - len(words_data)} SSML artifacts removed)")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_mp3), exist_ok=True)
    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    with open(output_mp3, "wb") as f:
        f.write(b"".join(audio_chunks))

    with open(output_json, "w") as f:
        json.dump({"words": words_data}, f, indent=4)

    audio_duration = words_data[-1]["end"] if words_data else 0
    print(f"  Duration: {audio_duration:.2f}s ({int(audio_duration * 30)} frames at 30fps)")

    return words_data
