"""
Spatial Multi-Object Tracking Module for Underwater Video Sequences.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
from .detector import BoundingBox


@dataclass
class Tracklet:
    """Active object track across sequential video frames."""
    track_id: int
    box: Tuple[float, float, float, float]
    class_id: int
    class_name: str = ""
    hits: int = 1
    age: int = 1
    time_since_update: int = 0
    confirmed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "bbox": [round(c, 2) for c in self.box],
            "class_id": self.class_id,
            "class_name": self.class_name,
            "hits": self.hits,
            "age": self.age,
            "confirmed": self.confirmed
        }


class SpatialIoUTracker:
    """Deterministic spatial IoU tracker."""

    def __init__(
        self,
        iou_threshold: float = 0.50,
        max_age: int = 5,
        min_hits: int = 3
    ):
        self.iou_threshold = float(iou_threshold)
        self.max_age = int(max_age)
        self.min_hits = int(min_hits)
        self.next_id = 1
        self.tracks: List[Tracklet] = []

    @staticmethod
    def _compute_iou(box_a: Tuple[float, float, float, float], box_b: Tuple[float, float, float, float]) -> float:
        xa1, ya1, xa2, ya2 = box_a
        xb1, yb1, xb2, yb2 = box_b

        xi1 = max(xa1, xb1)
        yi1 = max(ya1, yb1)
        xi2 = min(xa2, xb2)
        yi2 = min(ya2, yb2)

        inter_w = max(0.0, xi2 - xi1)
        inter_h = max(0.0, yi2 - yi1)
        inter_area = inter_w * inter_h

        area_a = max(0.0, xa2 - xa1) * max(0.0, ya2 - ya1)
        area_b = max(0.0, xb2 - xb1) * max(0.0, yb2 - yb1)
        union_area = area_a + area_b - inter_area

        if union_area <= 0.0:
            return 0.0
        return inter_area / union_area

    def update(
        self,
        detections: List[BoundingBox]
    ) -> Tuple[List[Tracklet], float]:
        """
        Associate detections with active tracks and return updated tracklets and latency.
        """
        start = time.perf_counter()

        for track in self.tracks:
            track.age += 1
            track.time_since_update += 1

        matched_detections = set()
        matched_tracks = set()

        if self.tracks and detections:
            iou_matrix = np.zeros((len(self.tracks), len(detections)), dtype=np.float32)
            for t_idx, track in enumerate(self.tracks):
                for d_idx, det in enumerate(detections):
                    if track.class_id == det.class_id:
                        iou_matrix[t_idx, d_idx] = self._compute_iou(track.box, det.box_coords)

            while True:
                max_iou = np.max(iou_matrix) if iou_matrix.size > 0 else 0.0
                if max_iou < self.iou_threshold:
                    break
                t_idx, d_idx = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
                if t_idx in matched_tracks or d_idx in matched_detections:
                    iou_matrix[t_idx, d_idx] = -1.0
                    continue

                track = self.tracks[t_idx]
                det = detections[d_idx]
                track.box = det.box_coords
                track.hits += 1
                track.time_since_update = 0
                if track.hits >= self.min_hits:
                    track.confirmed = True

                matched_tracks.add(t_idx)
                matched_detections.add(d_idx)
                iou_matrix[t_idx, :] = -1.0
                iou_matrix[:, d_idx] = -1.0

        for d_idx, det in enumerate(detections):
            if d_idx not in matched_detections:
                new_track = Tracklet(
                    track_id=self.next_id,
                    box=det.box_coords,
                    class_id=det.class_id,
                    class_name=det.class_name,
                    hits=1,
                    age=1,
                    time_since_update=0,
                    confirmed=(self.min_hits <= 1)
                )
                self.next_id += 1
                self.tracks.append(new_track)

        self.tracks = [
            t for t in self.tracks
            if t.time_since_update <= self.max_age
        ]

        latency_ms = (time.perf_counter() - start) * 1000.0
        active = [t for t in self.tracks if t.confirmed or t.hits >= 1]
        return active, latency_ms
