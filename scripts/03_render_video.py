#!/usr/bin/env python3
"""Step 3: Render Manim video."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == "__main__":
    cmd = ["manim", "-pqh", "scenes/vcr.py", "VCR"]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
