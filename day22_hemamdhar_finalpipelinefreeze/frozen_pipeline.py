"""
Day 22 — Frozen Final Model & Pipeline Module
AI-Based Underwater Visual Surveillance Pipeline

This module encapsulates the final, frozen, immutable computer vision pipeline:
1. Photometric Preprocessing: CLAHE (CIELAB L-channel, clip_limit=1.5, grid=8x8) or raw control.
2. Object Detection: YOLOv8n (imgsz=320, conf=0.25, iou=0.50).
3. Multi-Object Tracking: Deterministic greedy IoU tracker (iou_thresh=0.50, max_age=5, min_hits=3).
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


@dataclass
class Detection:
    """Bounding box detection proposal."""
    box: Tuple[float, float, float, float]  # [x1, y1, x2, y2]
    confidence: float
    class_id: int
    class_name: str = ""


@dataclass
class Tracklet:
    """Tracked object across sequential frames."""
    track_id: int
    box: Tuple[float, float, float, float]
    class_id: int
    hits: int = 1
    age: int = 1
    time_since_update: int = 0
    confirmed: bool = False


class FrozenPreprocessor:
    """Deterministic photometric preprocessing engine."""

    def __init__(self, method: str = "clahe", clip_limit: float = 1.5, grid_size: int = 8):
        self.method = method.lower()
        self.clip_limit = float(clip_limit)
        self.grid_size = int(grid_size)

        if self.method == "clahe" and cv2 is not None:
            self.clahe = cv2.createCLAHE(
                clipLimit=self.clip_limit,
                tileGridSize=(self.grid_size, self.grid_size)
            )
        else:
            self.clahe = None

    def transform(self, image: Union[Image.Image, np.ndarray, Path, str]) -> Tuple[Image.Image, float]:
        """Apply frozen transformation and record preprocessing latency."""
        start_time = time.perf_counter()

        if isinstance(image, (str, Path)):
            pil_img = Image.open(image).convert("RGB")
        elif isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image).convert("RGB")
        else:
            pil_img = image.convert("RGB")

        if self.method == "raw" or self.method == "raw_v1":
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return pil_img, latency_ms

        if self.method == "clahe":
            if cv2 is None:
                raise RuntimeError("OpenCV (cv2) is required for CLAHE enhancement.")
            arr = np.asarray(pil_img)
            lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
            lightness, a_channel, b_channel = cv2.split(lab)
            enhanced_l = self.clahe.apply(lightness)
            merged = cv2.merge((enhanced_l, a_channel, b_channel))
            result_rgb = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
            result_img = Image.fromarray(result_rgb)
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return result_img, latency_ms

        raise ValueError(f"Unsupported enhancement method: {self.method}")


class FrozenIoUTracker:
    """Greedy spatial IoU association tracker for underwater video frames."""

    def __init__(self, iou_threshold: float = 0.50, max_age: int = 5, min_hits: int = 3):
        self.iou_threshold = float(iou_threshold)
        self.max_age = int(max_age)
        self.min_hits = int(min_hits)
        self.next_id = 1
        self.tracks: List[Tracklet] = []

    @staticmethod
    def compute_iou(box_a: Tuple[float, float, float, float], box_b: Tuple[float, float, float, float]) -> float:
        """Calculate Intersection over Union (IoU) between two bounding boxes [x1, y1, x2, y2]."""
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

    def update(self, detections: List[Detection]) -> List[Tracklet]:
        """Update tracker state with new detections from the current frame."""
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
                        iou_matrix[t_idx, d_idx] = self.compute_iou(track.box, det.box)

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
                track.box = det.box
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
                    box=det.box,
                    class_id=det.class_id,
                    hits=1,
                    age=1,
                    time_since_update=0,
                    confirmed=(self.min_hits <= 1)
                )
                self.next_id += 1
                self.tracks.append(new_track)

        self.tracks = [
            track for track in self.tracks
            if track.time_since_update <= self.max_age
        ]

        return [track for track in self.tracks if track.confirmed or track.hits >= 1]


class FrozenPipeline:
    """End-to-End Frozen Underwater Computer Vision Pipeline."""

    def __init__(
        self,
        enhancement_method: str = "clahe",
        clip_limit: float = 1.5,
        grid_size: int = 8,
        detector_weights: Optional[str] = None,
        image_size: int = 320,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.50,
    ):
        self.preprocessor = FrozenPreprocessor(
            method=enhancement_method,
            clip_limit=clip_limit,
            grid_size=grid_size
        )
        self.tracker = FrozenIoUTracker(iou_threshold=0.50, max_age=5, min_hits=3)
        self.image_size = int(image_size)
        self.conf_threshold = float(conf_threshold)
        self.iou_threshold = float(iou_threshold)
        self.detector_weights = detector_weights
        self._model = None

    def _get_model(self):
        if self._model is None and self.detector_weights:
            try:
                from ultralytics import YOLO
                self._model = YOLO(self.detector_weights)
            except Exception as e:
                self._model = None
        return self._model

    def process_frame(
        self,
        image_input: Union[Image.Image, np.ndarray, Path, str]
    ) -> Dict[str, Any]:
        """Execute frozen pipeline on a single frame."""
        # Step 1: Preprocessing
        enhanced_image, prep_ms = self.preprocessor.transform(image_input)

        # Step 2: Object Detection
        inf_start = time.perf_counter()
        detections: List[Detection] = []
        model = self._get_model()

        if model is not None:
            results = model.predict(
                source=enhanced_image,
                imgsz=self.image_size,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=False,
                device="cpu"
            )
            for res in results:
                for box in res.boxes:
                    coords = box.xyxy[0].cpu().numpy().tolist()
                    conf = float(box.conf[0].cpu().numpy())
                    cls_id = int(box.cls[0].cpu().numpy())
                    cls_name = model.names.get(cls_id, str(cls_id)) if hasattr(model, "names") else str(cls_id)
                    detections.append(Detection(
                        box=(coords[0], coords[1], coords[2], coords[3]),
                        confidence=conf,
                        class_id=cls_id,
                        class_name=cls_name
                    ))
        inf_ms = (time.perf_counter() - inf_start) * 1000.0

        # Step 3: Tracking
        track_start = time.perf_counter()
        active_tracks = self.tracker.update(detections)
        track_ms = (time.perf_counter() - track_start) * 1000.0

        total_ms = prep_ms + inf_ms + track_ms
        fps = 1000.0 / max(total_ms, 1e-6)

        return {
            "status": "success",
            "preprocessing_ms": prep_ms,
            "inference_ms": inf_ms,
            "tracking_ms": track_ms,
            "total_latency_ms": total_ms,
            "throughput_fps": fps,
            "detection_count": len(detections),
            "detections": [
                {
                    "box": d.box,
                    "confidence": d.confidence,
                    "class_id": d.class_id,
                    "class_name": d.class_name
                }
                for d in detections
            ],
            "active_track_count": len(active_tracks),
            "tracks": [
                {
                    "track_id": t.track_id,
                    "box": t.box,
                    "class_id": t.class_id,
                    "hits": t.hits,
                    "age": t.age,
                    "confirmed": t.confirmed
                }
                for t in active_tracks
            ]
        }


def main():
    parser = argparse.ArgumentParser(description="Day 22 Frozen Final Pipeline CLI")
    parser.add_argument("--method", default="clahe", choices=["clahe", "raw", "raw_v1"])
    parser.add_argument("--clip-limit", type=float, default=1.5)
    parser.add_argument("--grid-size", type=int, default=8)
    parser.add_argument("--weights", type=str, default=None)
    parser.add_argument("--imgsz", type=int, default=320)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.50)
    args = parser.parse_args()

    pipeline = FrozenPipeline(
        enhancement_method=args.method,
        clip_limit=args.clip_limit,
        grid_size=args.grid_size,
        detector_weights=args.weights,
        image_size=args.imgsz,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )
    print(json.dumps({
        "status": "frozen_pipeline_initialized",
        "method": args.method,
        "clip_limit": args.clip_limit,
        "grid_size": args.grid_size,
        "image_size": args.imgsz,
        "conf_threshold": args.conf
    }, indent=2))


if __name__ == "__main__":
    main()
