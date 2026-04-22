"""Retry only missing scenes across multiple compositions.

Caps concurrency at 8 to stay safely under ElevenLabs' 10 concurrent limit.
"""
import glob
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from text_to_speech_lib import generate_synced_audio

load_dotenv()
VOICE_ID = os.getenv("VOICE_ID")


def get_scene_number(filename: str) -> int:
    m = re.search(r"scene-(\d+)", filename)
    return int(m.group(1)) if m else -1


def enumerate_missing(compositions):
    jobs = []
    for comp in compositions:
        scripts_dir = os.path.join("src", comp, "scripts")
        audio_dir = os.path.join("public", "audio", comp.lower())
        os.makedirs(audio_dir, exist_ok=True)
        for script in sorted(glob.glob(os.path.join(scripts_dir, "scene-*.txt"))):
            num = get_scene_number(os.path.basename(script))
            if num < 0:
                continue
            mp3 = os.path.join(audio_dir, f"scene{num:02d}.mp3")
            if os.path.exists(mp3) and os.path.getsize(mp3) > 1000:
                continue
            jobs.append({
                "comp": comp,
                "script": script,
                "mp3": mp3,
                "json": os.path.join(scripts_dir, f"scene{num:02d}-sync.json"),
                "is_preview": num == 0,
                "label": f"{comp}/scene{num:02d}",
            })
    return jobs


def run_one(job):
    with open(job["script"], "r", encoding="utf-8") as f:
        text = f.read().strip()
    generate_synced_audio(text, job["mp3"], job["json"], VOICE_ID, is_preview=job["is_preview"])
    return job["label"]


def main():
    comps = sys.argv[1:]
    if not comps:
        print("Usage: python retry-missing-audio.py <Comp1> <Comp2> ...")
        sys.exit(1)
    jobs = enumerate_missing(comps)
    print(f"Missing scenes: {len(jobs)}")
    for j in jobs:
        print(f"  - {j['label']}")
    if not jobs:
        return

    done, failed = [], []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(run_one, j): j for j in jobs}
        for fut in as_completed(futs):
            j = futs[fut]
            try:
                fut.result()
                done.append(j["label"])
                print(f"  OK {j['label']} ({len(done)}/{len(jobs)})")
            except Exception as e:
                failed.append((j["label"], str(e)[:300]))
                print(f"  FAIL {j['label']}: {str(e)[:150]}")

    print(f"\nDone: {len(done)} | Failed: {len(failed)}")
    for name, err in failed:
        print(f"  FAIL {name}: {err}")
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
