#!/usr/bin/env python3
"""Step 2: Generate TTS audio from content/script.yml."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.tts import generate

if __name__ == "__main__":
    print("Generating TTS audio...")
    generate()
