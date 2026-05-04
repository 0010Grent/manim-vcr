import subprocess
import json

VOICE = "en-US-AndrewNeural"

SEGMENT_RATES = {
    "s01":  "-10%",
    "s02":  "-5%",
    "s02b": "-5%",
    "s03":  "+0%",
    "s04a": "+0%",
    "s04b": "+0%",
    "s05":  "-15%",
    "s05b": "-15%",
    "s06a": "-10%",
    "s06b": "-10%",
    "s07":  "-5%",
    "s07b": "-5%",
    "s08":  "-5%",
    "s09":  "-10%",
}

VIDEO_START = {
    "s01":  0.30,
    "s02":  3.50,
    "s02b": 5.50,
    "s03":  9.20,
    "s04a": 15.20,
    "s04b": 17.00,
    "s05":  20.50,
    "s05b": 25.40,
    "s06a": 29.00,
    "s06b": 34.00,
    "s07":  38.30,
    "s07b": 43.50,
    "s08":  49.00,
    "s09":  51.50,
}

segments = [
    {"id": "s01",  "text": "She teaches AI to think."},
    {"id": "s02",  "text": "This is Yao Fu."},
    {"id": "s02b", "text": "Most engineers write answers. She writes the questions."},
    {"id": "s03",  "text": "Every day, she tests where AI fails — on earnings, on risk, on reasoning."},
    {"id": "s04a", "text": "Faster than her."},
    {"id": "s04b", "text": "In some ways, smarter."},
    {"id": "s05",  "text": "But one day, the AI asked her something she couldn't answer."},
    {"id": "s05b", "text": "It asked: Why does beauty matter to you?"},
    {"id": "s06a", "text": "She showed it a sunset. It described the wavelengths perfectly."},
    {"id": "s06b", "text": "But it couldn't tell her why it was beautiful."},
    {"id": "s07",  "text": "That's when she understood. What makes us human isn't what we know."},
    {"id": "s07b", "text": "The AI could calculate. It could optimize. It could predict."},
    {"id": "s08",  "text": "It's what we choose to care about."},
    {"id": "s09",  "text": "She teaches AI to think. And it's teaching her what it means to be human."},
]

output_dir = "/Users/fuy/Desktop/VCR/audio"
timing_data = []

for seg in segments:
    mp3_path = f"{output_dir}/{seg['id']}.mp3"
    vtt_path = f"{output_dir}/{seg['id']}.vtt"
    rate = SEGMENT_RATES[seg["id"]]
    cmd = [
        "edge-tts",
        "--voice", VOICE,
        f"--rate={rate}",
        "--text", seg["text"],
        "--write-media", mp3_path,
        "--write-subtitles", vtt_path,
    ]
    subprocess.run(cmd, check=True)

    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", mp3_path],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    timing_data.append({
        "id": seg["id"],
        "text": seg["text"],
        "rate": rate,
        "duration": round(duration, 3),
        "video_start": VIDEO_START[seg["id"]],
    })
    print(f"  {seg['id']}: {duration:.3f}s @ {VIDEO_START[seg['id']]}s [{rate}] - {seg['text']}")

total_narration = sum(t["duration"] for t in timing_data)
print(f"\nTotal narration duration: {total_narration:.3f}s")

scenes = [
    {"id": 1, "name": "opening",    "start": 0.0,  "end": 3.0},
    {"id": 2, "name": "intro",      "start": 3.0,  "end": 8.0},
    {"id": 3, "name": "montage",    "start": 8.0,  "end": 20.0},
    {"id": 4, "name": "turning",    "start": 20.0, "end": 28.0},
    {"id": 5, "name": "sunset",     "start": 28.0, "end": 38.0},
    {"id": 6, "name": "understand", "start": 38.0, "end": 50.0},
    {"id": 7, "name": "closing",    "start": 50.0, "end": 60.0},
]

with open(f"{output_dir}/timing.json", "w") as f:
    json.dump({
        "segments": timing_data,
        "scenes": scenes,
        "total_narration": round(total_narration, 3),
    }, f, indent=2)

print(f"Timing data saved to {output_dir}/timing.json")
