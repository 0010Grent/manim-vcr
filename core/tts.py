import json
import subprocess
from pathlib import Path
from typing import Optional

import yaml

from core import AUDIO_DIR, CONTENT_DIR


def load_script(path: Optional[Path] = None) -> dict:
    if path is None:
        path = CONTENT_DIR / "script.yml"
    with open(path) as f:
        return yaml.safe_load(f)


def generate(script_path: Optional[Path] = None, output_dir: Optional[Path] = None, voice: str = "en-US-AndrewNeural") -> None:
    if output_dir is None:
        output_dir = AUDIO_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    script = load_script(script_path)
    timing_data = []

    for seg in script["segments"]:
        mp3_path = output_dir / f"{seg['id']}.mp3"
        vtt_path = output_dir / f"{seg['id']}.vtt"
        rate = seg["rate"]
        cmd = [
            "edge-tts",
            "--voice", voice,
            f"--rate={rate}",
            "--text", seg["en"],
            "--write-media", str(mp3_path),
            "--write-subtitles", str(vtt_path),
        ]
        subprocess.run(cmd, check=True)

        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        timing_data.append({
            "id": seg["id"],
            "text": seg["en"],
            "rate": rate,
            "duration": round(duration, 3),
            "video_start": seg["video_start"],
        })
        print(f"  {seg['id']}: {duration:.3f}s @ {seg['video_start']}s [{rate}]")

    total_narration = sum(t["duration"] for t in timing_data)
    scenes = script.get("scenes", [])

    with open(output_dir / "timing.json", "w") as f:
        json.dump({
            "segments": timing_data,
            "scenes": scenes,
            "total_narration": round(total_narration, 3),
        }, f, indent=2)

    print(f"\nTotal narration: {total_narration:.3f}s")
    print(f"Timing data saved to {output_dir / 'timing.json'}")
