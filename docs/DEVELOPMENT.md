# Development Guide

## Environment Setup

### Option A: Local (macOS/Linux)

```bash
# 1. Clone
git clone https://github.com/0010Grent/manim-vcr.git
cd manim-vcr

# 2. Install Python deps
pip install -r requirements.txt

# 3. Install system deps (macOS)
brew install ffmpeg cairo pango
# For TeX (required by Manim):
brew install --cask mactex

# 4. Verify
python -c "import manim; print(manim.__version__)"
ffmpeg -version | head -1
```

### Option B: Docker (Recommended for reproducibility)

```bash
# Build image (first time: ~30-60 min, downloads texlive-full)
docker compose build

# Or pull pre-built image:
docker pull 0010grent/manim-vcr:latest

# Run any command inside the container:
docker compose run --rm manim make all
docker compose run --rm manim python scripts/01_generate_character.py
```

## Running Individual Steps

```bash
make character   # → character/*.svg
make tts         # → audio/*.mp3, audio/timing.json
make render      # → media/videos/vcr/1080p60/VCR.mp4
make merge       # → output/VCR_Final.mp4
```

## Debugging

### Manim rendering issues

```bash
# Preview at lower quality for faster iteration
manim -pql scenes/vcr.py VCR   # low quality
manim -pqm scenes/vcr.py VCR   # medium quality
manim -pqh scenes/vcr.py VCR   # high quality (production)
```

### TTS issues

```bash
# Test a single segment
edge-tts --voice "en-US-AndrewNeural" --rate="-10%" \
  --text "Hello world" --write-media /tmp/test.mp3
```

### Verify final output

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,bit_rate,r_frame_rate \
  -of default=noprint_wrappers=1 output/VCR_Final.mp4
# Expected: width=1920, height=1080, r_frame_rate=60/1
```

## Project Architecture

```
core/                 # Framework engine (reusable)
  __init__.py         # Path constants (PROJECT_ROOT, AUDIO_DIR, ...)
  theme.py            # Visual constants (colors, fonts, sizes)
  timing.py           # TimingData — reads audio/timing.json
  subtitle.py         # BilingualSubtitle Manim component
  tts.py              # TTS generation from script.yml
  merge.py            # Audio/video merge pipeline
  character_builder.py # SVG generation from character.yml

scenes/
  vcr.py              # Main VCR scene (calls core/)

scripts/              # CLI entry points for each pipeline stage
content/              # User-editable content (script, character config)
config/               # Video/audio parameters
showcase/             # Demo assets committed to repo
```

## Adding a New Character Pose

1. Add a new generation call in `core/character_builder.py`:
   ```python
   poses = [
       ...
       ("fu_yao_happy.svg", "front", "smile_bright", "right"),
   ]
   ```
2. If needed, add the expression to `_front()` or `_side()` in the same file.
3. Add the expression name to `content/character.yml` under `expressions:`.
4. Reference it in `scenes/vcr.py`:
   ```python
   char_happy = SVGMobject(str(CHARACTER_DIR / "fu_yao_happy.svg"))
   ```

## Contributing

1. Fork the repo and create a feature branch
2. Follow the existing code style (type annotations, no hardcoded paths)
3. Test with `make all` before submitting a PR
4. Update `content/example/` if you add new config fields
