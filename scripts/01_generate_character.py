#!/usr/bin/env python3
"""Step 1: Generate SVG character poses from content/character.yml."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.character_builder import generate_all_poses

if __name__ == "__main__":
    print("Generating character SVGs...")
    generate_all_poses()
