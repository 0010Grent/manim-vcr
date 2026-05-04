import json
import os
import subprocess
from pathlib import Path
from typing import Optional

import yaml
from pydub import AudioSegment

from core import AUDIO_DIR, CONFIG_DIR, MEDIA_DIR, OUTPUT_DIR


def load_config(path: Optional[Path] = None) -> dict:
    if path is None:
        path = CONFIG_DIR / "video.yml"
    with open(path) as f:
        return yaml.safe_load(f)


def find_rendered_video(media_dir: Path) -> Optional[Path]:
    """在 media/ 目录树中查找渲染出的 mp4 文件（取最新）。"""
    candidates = sorted(media_dir.rglob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def merge(config_path: Optional[Path] = None) -> None:
    cfg = load_config(config_path)
    audio_cfg = cfg["audio"]

    bgm_volume_db: float = audio_cfg["bgm_volume_db"]
    narration_volume_db: float = audio_cfg["narration_volume_db"]
    bgm_fade_in_ms: int = audio_cfg["bgm_fade_in_ms"]
    bgm_fade_out_ms: int = audio_cfg["bgm_fade_out_ms"]
    total_duration_ms: int = int(cfg["video"]["total_duration_s"] * 1000)

    timing_path = AUDIO_DIR / "timing.json"
    with open(timing_path) as f:
        timing = json.load(f)

    # Stage 1: place narration segments on a silence track
    print("Stage 1: Timeline-aligned narration")
    silence = AudioSegment.silent(duration=total_duration_ms)
    for seg in timing["segments"]:
        mp3 = AUDIO_DIR / f"{seg['id']}.mp3"
        audio = AudioSegment.from_mp3(str(mp3))
        pos = int(seg["video_start"] * 1000)
        silence = silence.overlay(audio, position=pos)
        print(f"  {seg['id']}: placed at {seg['video_start']}s (dur {seg['duration']}s)")

    narration_path = AUDIO_DIR / "narration_aligned.mp3"
    silence.export(str(narration_path), format="mp3", bitrate="192k")
    print(f"  -> {narration_path}")

    # Stage 2: mix narration + BGM
    print("\nStage 2: Mixing narration + BGM")
    narration = AudioSegment.from_mp3(str(narration_path)) + narration_volume_db

    bgm_candidates = [
        AUDIO_DIR / "bgm_trimmed.mp3",
        AUDIO_DIR / "bgm.mp3",
    ]
    bgm_path = next((p for p in bgm_candidates if p.exists()), None)

    if bgm_path:
        bgm = AudioSegment.from_mp3(str(bgm_path)) + bgm_volume_db
        if len(bgm) < total_duration_ms:
            bgm = bgm + AudioSegment.silent(duration=total_duration_ms - len(bgm))
        else:
            bgm = bgm[:total_duration_ms]
        bgm = bgm.fade_in(bgm_fade_in_ms).fade_out(bgm_fade_out_ms)
        mixed = narration.overlay(bgm)
        print(f"  BGM mixed ({bgm_volume_db}dB, fade-in {bgm_fade_in_ms}ms, fade-out {bgm_fade_out_ms}ms)")
    else:
        mixed = narration
        print("  No BGM found, using narration only")

    mixed_path = AUDIO_DIR / "mixed_audio.mp3"
    mixed.export(str(mixed_path), format="mp3", bitrate="192k")
    print(f"  -> {mixed_path}")

    # Stage 3: merge video + audio
    print("\nStage 3: Merging video + audio")
    video_path = find_rendered_video(MEDIA_DIR)
    if video_path is None:
        raise FileNotFoundError(f"No rendered video found in {MEDIA_DIR}. Run 'make render' first.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "VCR_Final.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(mixed_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_path),
    ]
    print(f"  {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"\n  -> {output_path}")
