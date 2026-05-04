# Customization Guide

This guide walks you through replacing the example content with your own to produce a personalized video resume.

## Step 1: Write Your Script

Edit `content/script.yml`. Each segment needs:

```yaml
segments:
  - id: s01              # unique identifier, used to match audio files
    en: "Your text."     # English narration (also the TTS input)
    cn: "你的文字。"       # Chinese subtitle (displayed below English)
    rate: "-10%"         # TTS speed: -20% to +20%
    video_start: 0.30    # seconds into the video when this subtitle appears
```

**Tips:**
- Keep each segment under 15 words for readability
- `video_start` should be slightly before the narration starts (allow ~0.3s lead)
- Use negative rates (`-5%` to `-15%`) for clearer, slower speech

## Step 2: Customize Your Character

Edit `content/character.yml`:

```yaml
skin: "#FCDEC0"         # base skin color (hex)
skin_shadow: "#EABC98"  # shadow areas
hair: "#1C1C1C"         # hair color
glasses_frame: "#C09898" # glasses color (remove glasses by setting to "none")
shirt: "#A8D0E0"        # shirt/top color
```

Regenerate SVGs after changes:
```bash
make character
```

## Step 3: Add Background Music (Optional)

Place your BGM file at `audio/bgm_trimmed.mp3`. The merge pipeline will:
- Apply `bgm_volume_db` attenuation from `config/video.yml`
- Fade in/out automatically
- Loop or truncate to match video length

## Step 4: Adjust Video Parameters

Edit `config/video.yml`:

```yaml
video:
  total_duration_s: 62   # adjust to match your script length
  fps: 60                # 30 or 60

audio:
  tts_voice: "en-US-AndrewNeural"  # any edge-tts voice
  bgm_volume_db: -11               # negative = quieter BGM
```

Available edge-tts voices: run `edge-tts --list-voices` to see all options.

## Step 5: Customize Animations

The scene logic lives in `scenes/vcr.py`. Each `scene_0N_*` method corresponds to a segment range.

To add a new scene or modify animations:
1. Add your segment IDs to `content/script.yml`
2. Add a corresponding `scene_0N_myname` method to `VCR` in `scenes/vcr.py`
3. Call it from `construct()`

## Step 6: Run the Full Pipeline

```bash
make all
```

Or run stages individually for faster iteration:
```bash
make character   # only if you changed character.yml
make tts         # only if you changed script text
make render      # only if you changed scenes/vcr.py
make merge       # always re-run after render
```

## Timing Workflow

If you change the script text, the TTS durations will change and timing may drift. After `make tts`, check `audio/timing.json` to see the actual durations, then adjust `video_start` values in `content/script.yml` accordingly.
