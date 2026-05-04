#!/usr/bin/env python3
"""Step 4: Merge video + audio into final output."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.merge import merge

if __name__ == "__main__":
    print("Merging video and audio...")
    merge()
