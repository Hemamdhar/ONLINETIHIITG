"""
Unified Surveillance Pipeline Module.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from PIL import Image

from .preprocessing import PhotometricPreprocessor
from .detector import ObjectDetector, BoundingBox
from .tracker import SpatialIoUTracker, Tracklet


class SurveillancePipeline:
    """End-to-End AI-Based Underwater Surveillance Pipeline."""

    def __init__(
        self,
        enhancement_method: str = "clahe",
        clip_limit: float = 1.5,
        grid_size: int = 8,
        weights_path: Optional[Union[str, Path]] = None,
        image_size: int = 320,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.50,
        device: str = "cpu"
    ):
        self.preprocessor = PhotometricPreprocessor(
            method=enhancement_method,
            clip_limit=clip_limit,
            grid_size=grid_size
        )
        self.detector = ObjectDetector(
            weights_path=weights_path,
            image_size=image_size,
            conf_threshold=conf_threshold,
            iou_threshold=iou_threshold,
            device=device
        )
        self.tracker = SpatialIoUTracker(
            iou_threshold=iou_threshold,
            max_age=5,
            min_hits=3
        )

    def process_frame(
        self,
        image_input: Union[Image.Image, np.ndarray, str, Path]
    ) -> Dict[str, Any]:
        """
        Execute full pipeline: Preprocess -> Detect -> Track.
        """
        # Step 1: Preprocessing
        enhanced_image, prep_ms = self.preprocessor.process(image_input)

        # Step 2: Detection
        detections, inf_ms = self.detector.detect(enhanced_image)

        # Step 3: Tracking
        active_tracks, track_ms = self.tracker.update(detections)

        total_ms = prep_ms + inf_ms + track_ms
        fps = 1000.0 / max(total_ms, 1e-6)

        return {
            "status": "success",
            "enhanced_image": enhanced_image,
            "latency": {
                "preprocessing_ms": round(prep_ms, 3),
                "inference_ms": round(inf_ms, 3),
                "tracking_ms": round(track_ms, 3),
                "total_ms": round(total_ms, 3),
                "throughput_fps": round(fps, 2)
            },
            "detections": [d.to_dict() for d in detections],
            "tracks": [t.to_dict() for t in active_tracks]
        }

    def process_sequence(
        self,
        image_paths: List[Union[str, Path]]
    ) -> List[Dict[str, Any]]:
        """
        Execute pipeline sequentially across a list of frame paths.
        """
        sequence_results = []
        for path in image_paths:
            res = self.process_frame(path)
            res["source_path"] = str(path)
            sequence_results.append(res)
        return sequence_results
