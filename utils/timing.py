import json
from dataclasses import dataclass
from typing import Dict

TIMING_PATH = "/Users/fuy/Desktop/VCR/audio/timing.json"


@dataclass(frozen=True)
class SegmentTiming:
    id: str
    text: str
    duration: float
    video_start: float


class TimingData:
    def __init__(self, path: str = TIMING_PATH):
        with open(path) as f:
            data = json.load(f)
        self._segs: Dict[str, SegmentTiming] = {}
        for s in data["segments"]:
            self._segs[s["id"]] = SegmentTiming(
                id=s["id"],
                text=s["text"],
                duration=s["duration"],
                video_start=s["video_start"],
            )

    def start(self, seg_id: str) -> float:
        return self._segs[seg_id].video_start

    def end(self, seg_id: str) -> float:
        s = self._segs[seg_id]
        return s.video_start + s.duration

    def dur(self, seg_id: str) -> float:
        return self._segs[seg_id].duration
