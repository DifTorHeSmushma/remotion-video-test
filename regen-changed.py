"""Regenerate ONLY the chunks whose text has changed, using checksums.

Workflow:
  1. Phase 2a (or a prior `generate-all-audio.py --chunk sentence`) produced
     sceneNN.mp3, sceneNN-sync.json, sceneNN-history.json, and per-chunk
     MP3s in public/audio/<comp>/sceneNN-chunks/.
  2. User edits src/<Name>/scripts/scene-NN-*.txt (changes a sentence or two).
  3. `python regen-changed.py <AnimationName>` re-splits the script with the
     same chunker, computes checksums, and compares them against the old
     history. Only chunks whose checksum changed or that are new get sent to
     ElevenLabs. Unchanged chunks are reused verbatim.

Matching is content-based, not index-based: inserting a new sentence in the
middle causes only that new sentence to be generated — chunks before AND
after it are recognized by their checksums and reused.

Usage:
  python regen-changed.py <AnimationName>
  python regen-changed.py <AnimationName> --scene 02
  python regen-changed.py <AnimationName> --dry-run
  python regen-changed.py <AnimationName> --force     # regen everything

If a scene has no sceneNN-history.json (generated with --chunk none originally),
it is skipped with a warning. Run `generate-all-audio.py --chunk sentence`
first to migrate such scenes into the chunked format.
"""

import argparse
import glob
import json
import os
import re
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

from text_to_speech_lib import (
    DEFAULT_INTER_CHUNK_SILENCE_MS,
    compute_checksum,
    concat_mp3s,
    generate_chunk,
    get_mp3_duration,
    merge_chunk_syncs,
    split_into_chunks,
)

load_dotenv()
VOICE_ID = os.getenv("VOICE_ID") or "JBFqnCBsd6RMkjVDRZzb"


def _scene_num(filename: str) -> int:
    m = re.search(r"scene-(\d+)", filename)
    return int(m.group(1)) if m else -1


def _find_script(scripts_dir: Path, scene_num: int) -> Path | None:
    matches = sorted(scripts_dir.glob(f"scene-{scene_num:02d}-*.txt"))
    return matches[0] if matches else None


def plan_scene(
    scripts_dir: Path,
    audio_dir: Path,
    scene_num: int,
    force: bool,
) -> dict | None:
    """Build a regen plan for one scene without touching any files.

    Returns a dict with:
      scene_name, script_file, history_path, chunks_dir,
      new_chunks (list of {index, text, checksum, action, old_index}),
      reuse_count, regen_count, chars_billed, total_chars, speed, voice_id,
      inter_chunk_silence_ms
    or None if the scene should be skipped.
    """
    scene_name = f"scene{scene_num:02d}"
    script_file = _find_script(scripts_dir, scene_num)
    if not script_file:
        return None
    history_path = scripts_dir / f"{scene_name}-history.json"
    chunks_dir = audio_dir / f"{scene_name}-chunks"

    if not history_path.exists():
        print(f"  {scene_name}: no history.json — skipped (run generate-all-audio.py --chunk sentence first)")
        return None
    if not chunks_dir.exists():
        print(f"  {scene_name}: chunks dir missing at {chunks_dir} — skipped")
        return None

    with open(script_file, "r", encoding="utf-8") as f:
        new_text = f.read().strip()
    with open(history_path, "r", encoding="utf-8") as f:
        history = json.load(f)

    new_chunks = split_into_chunks(new_text)
    old_by_checksum: dict[str, dict] = {}
    for entry in history["chunks"]:
        # First checksum wins if duplicates exist (rare — only if script had
        # two identical sentences). Subsequent duplicates will force-regen.
        old_by_checksum.setdefault(entry["checksum"], entry)

    plan_entries: list[dict] = []
    reused_old_indices: set[int] = set()
    for i, txt in enumerate(new_chunks):
        cs = compute_checksum(txt)
        if not force and cs in old_by_checksum and old_by_checksum[cs]["index"] not in reused_old_indices:
            plan_entries.append({
                "index": i,
                "text": txt,
                "checksum": cs,
                "action": "reuse",
                "old_index": old_by_checksum[cs]["index"],
            })
            reused_old_indices.add(old_by_checksum[cs]["index"])
        else:
            plan_entries.append({
                "index": i,
                "text": txt,
                "checksum": cs,
                "action": "regen",
                "old_index": None,
            })

    reuse_count = sum(1 for e in plan_entries if e["action"] == "reuse")
    regen_count = sum(1 for e in plan_entries if e["action"] == "regen")
    chars_billed = sum(len(e["text"]) for e in plan_entries if e["action"] == "regen")
    total_chars = sum(len(e["text"]) for e in plan_entries)

    return {
        "scene_name": scene_name,
        "script_file": script_file,
        "history_path": history_path,
        "chunks_dir": chunks_dir,
        "audio_dir": audio_dir,
        "scripts_dir": scripts_dir,
        "new_chunks": plan_entries,
        "reuse_count": reuse_count,
        "regen_count": regen_count,
        "chars_billed": chars_billed,
        "total_chars": total_chars,
        "speed": history.get("speed", 1.0),
        "voice_id": history.get("voice_id", VOICE_ID),
        "inter_chunk_silence_ms": history.get("inter_chunk_silence_ms", DEFAULT_INTER_CHUNK_SILENCE_MS),
        "model": history.get("model", "eleven_multilingual_v2"),
    }


def execute_plan(plan: dict) -> None:
    """Apply a regen plan: stage old chunks, regenerate changed, re-merge."""
    scene_name = plan["scene_name"]
    chunks_dir: Path = plan["chunks_dir"]
    audio_dir: Path = plan["audio_dir"]
    scripts_dir: Path = plan["scripts_dir"]
    voice_id: str = plan["voice_id"]
    speed: float = plan["speed"]
    silence_ms: int = plan["inter_chunk_silence_ms"]

    # Atomic-ish swap: move old chunks aside, rebuild fresh, delete backup on success.
    bak_dir = chunks_dir.parent / f"{chunks_dir.name}.bak"
    if bak_dir.exists():
        shutil.rmtree(bak_dir)
    chunks_dir.rename(bak_dir)
    chunks_dir.mkdir()

    try:
        new_history_entries: list[dict] = []
        chunks_data: list[dict] = []

        for entry in plan["new_chunks"]:
            new_idx = entry["index"]
            dest_mp3 = chunks_dir / f"chunk-{new_idx:02d}.mp3"
            dest_sync = chunks_dir / f"chunk-{new_idx:02d}-sync.json"

            if entry["action"] == "reuse":
                old_idx = entry["old_index"]
                src_mp3 = bak_dir / f"chunk-{old_idx:02d}.mp3"
                src_sync = bak_dir / f"chunk-{old_idx:02d}-sync.json"
                shutil.copy(src_mp3, dest_mp3)
                shutil.copy(src_sync, dest_sync)
                with open(src_sync, "r", encoding="utf-8") as f:
                    words = json.load(f)["words"]
                duration = get_mp3_duration(str(dest_mp3))
                print(f"  [{new_idx:02d}] reuse <- old chunk {old_idx:02d} ({len(entry['text'])} chars)")
            else:
                print(f"  [{new_idx:02d}] regen ({len(entry['text'])} chars)")
                is_preview = scene_name == "scene00"
                mp3_bytes, words = generate_chunk(
                    entry["text"], voice_id, speed=speed, is_preview=is_preview,
                )
                dest_mp3.write_bytes(mp3_bytes)
                with open(dest_sync, "w", encoding="utf-8") as f:
                    json.dump({"words": words}, f, indent=2)
                duration = get_mp3_duration(str(dest_mp3))

            new_history_entries.append({
                "index": new_idx,
                "text": entry["text"],
                "checksum": entry["checksum"],
                "mp3": f"chunk-{new_idx:02d}.mp3",
                "duration": duration,
                "word_count": len(words),
            })
            chunks_data.append({"words": words, "duration": duration})

        cursor = 0
        for e in new_history_entries:
            e["words_offset"] = cursor
            cursor += e["word_count"]

        merged_mp3 = audio_dir / f"{scene_name}.mp3"
        merged_sync = scripts_dir / f"{scene_name}-sync.json"
        history_path = plan["history_path"]

        concat_mp3s(
            [str(chunks_dir / f"chunk-{e['index']:02d}.mp3") for e in new_history_entries],
            str(merged_mp3),
            inter_chunk_silence_ms=silence_ms,
        )
        merged_words = merge_chunk_syncs(chunks_data, inter_chunk_silence_ms=silence_ms)
        with open(merged_sync, "w", encoding="utf-8") as f:
            json.dump({"words": merged_words}, f, indent=4)

        bundle = {
            "voice_id": voice_id,
            "speed": speed,
            "model": plan["model"],
            "inter_chunk_silence_ms": silence_ms,
            "chunks": new_history_entries,
        }
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)

        total_duration = get_mp3_duration(str(merged_mp3))
        print(f"  {scene_name}: merged {total_duration:.2f}s ({len(merged_words)} words)")

    except Exception:
        # Roll back to old chunks so user isn't left with a broken scene.
        if chunks_dir.exists():
            shutil.rmtree(chunks_dir)
        bak_dir.rename(chunks_dir)
        raise
    else:
        shutil.rmtree(bak_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate only chunks whose text changed")
    parser.add_argument("animation_name", help="AnimationName (folder name under src/)")
    parser.add_argument("--scene", type=int, default=None, help="Only process this scene number")
    parser.add_argument("--dry-run", action="store_true", help="Print plan but do not call the API")
    parser.add_argument("--force", action="store_true", help="Regenerate all chunks even if unchanged")
    args = parser.parse_args()

    scripts_dir = Path("src") / args.animation_name / "scripts"
    audio_dir = Path("public") / "audio" / args.animation_name.lower()
    if not scripts_dir.is_dir():
        print(f"Error: {scripts_dir} not found")
        sys.exit(1)

    all_scripts = sorted(scripts_dir.glob("scene-*.txt"), key=lambda p: _scene_num(p.name))
    scene_nums = (
        [args.scene] if args.scene is not None
        else [_scene_num(p.name) for p in all_scripts if _scene_num(p.name) >= 0]
    )

    plans: list[dict] = []
    for n in scene_nums:
        p = plan_scene(scripts_dir, audio_dir, n, args.force)
        if p:
            plans.append(p)

    if not plans:
        print("Nothing to do.")
        return

    print("=" * 60)
    print(f"Regen plan for {args.animation_name}:\n")
    total_chars = 0
    total_billed = 0
    for p in plans:
        pct = 100 * p["chars_billed"] // max(p["total_chars"], 1)
        print(f"  {p['scene_name']}: {p['reuse_count']} reuse, {p['regen_count']} regen "
              f"-> {p['chars_billed']}/{p['total_chars']} chars ({pct}%)")
        total_chars += p["total_chars"]
        total_billed += p["chars_billed"]
    saved = total_chars - total_billed
    pct_billed = 100 * total_billed // max(total_chars, 1)
    pct_saved = 100 - pct_billed
    print(f"\n  TOTAL: {total_billed}/{total_chars} chars ({pct_billed}% billed, {pct_saved}% saved = {saved} chars)")
    print("=" * 60)

    if args.dry_run:
        print("\nDry run — no files touched.")
        return

    if total_billed == 0:
        print("\nAll chunks unchanged — nothing to regenerate.")
        return

    for p in plans:
        if p["regen_count"] == 0:
            print(f"\n--- {p['scene_name']}: all chunks unchanged, skipping ---")
            continue
        print(f"\n--- {p['scene_name']} ---")
        execute_plan(p)

    print("\nDone.")


if __name__ == "__main__":
    main()
