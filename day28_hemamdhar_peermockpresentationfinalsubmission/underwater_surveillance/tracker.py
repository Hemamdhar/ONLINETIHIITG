"""
Greedy IoU Multi-Object Tracking Module.
Provides lightweight, zero-parameter tracking suitable for real-time edge micro-controllers.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class TrackedObject:
    """Represents a continuous track trajectory across video frames."""
    track_id: int
    bbox: List[float]  # [x1, y1, x2, y2]
    class_id: int
    class_name: str
    confidence: float
    age: int
    hits: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_iou(box1: List[float], box2: List[float]) -> float:
    """Compute Intersection over Union between two [x1, y1, x2, y2] bounding boxes."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)
    inter_area = inter_w * inter_h

    area1 = max(0.0, box1[2] - box1[0]) * max(0.0, box1[3] - box1[1])
    area2 = max(0.0, box2[2] - box2[0]) * max(0.0, box2[3] - box2[1])
    union_area = area1 + area2 - inter_area

    if union_area <= 0:
        return 0.0
    return inter_area / union_area


class GreedyIoUTracker:
    """
    Greedy Intersection-over-Union (IoU) Multi-Object Tracker.
    Associates newly detected bounding boxes with existing active tracks
    based on spatial overlap without heavy feature extraction or Kalman filtering.
    """

    def __init__(self, iou_threshold: float = 0.50, max_age: int = 5):
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self.next_id = 1
        self.tracks: List[TrackedObject] = []

    def update(self, detections: List[Any]) -> List[TrackedObject]:
        """
        Update active tracks with new frame detections.
        :param detections: List of DetectionResult objects
        :return: List of currently active TrackedObject instances
        """
        # Age existing tracks
        for t in self.tracks:
            t.age += 1

        matched_track_indices = set()
        matched_detection_indices = set()

        # Perform greedy bipartite matching
        if len(self.tracks) > 0 and len(detections) > 0:
            iou_matrix = np.zeros((len(self.tracks), len(detections)), dtype=np.float32)
            for t_idx, track in enumerate(self.tracks):
                for d_idx, det in enumerate(detections):
                    # Check class consistency
                    if track.class_id == det.class_id:
                        iou_matrix[t_idx, d_idx] = calculate_iou(track.bbox, det.bbox)
                    else:
                        iou_matrix[t_idx, d_idx] = 0.0

            # Match greedily highest IoU first
            while True:
                max_iou = np.max(iou_matrix)
                if max_iou < self.iou_threshold:
                    break
                t_idx, d_idx = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
                if t_idx in matched_track_indices or d_idx in matched_detection_indices:
                    iou_matrix[t_idx, d_idx] = -1.0
                    continue

                # Update matched track
                matched_track_indices.add(t_idx)
                matched_detection_indices.add(d_idx)
                iou_matrix[t_idx, :] = -1.0
                iou_matrix[:, d_idx] = -1.0

                track = self.tracks[t_idx]
                det = detections[d_idx]
                track.bbox = det.bbox
                track.confidence = det.confidence
                track.age = 0
                track.hits += 1

        # Instantiate new tracks for unmatched detections
        for d_idx, det in enumerate(detections):
            if d_idx not in matched_detection_indices:
                new_track = TrackedObject(
                    track_id=self.next_id,
                    bbox=det.bbox,
                    class_id=det.class_id,
                    class_name=det.class_name,
                    confidence=det.confidence,
                    age=0,
                    hits=1
                )
                self.next_id += 1
                self.tracks.append(new_track)

        # Remove dead tracks that exceeded max_age
        self.tracks = [t for t in self.tracks if t.age <= self.max_age]
        return self.tracks

    def reset(self):
        """Reset tracker state and active track database."""
        self.next_id = 1
        self.tracks = []
