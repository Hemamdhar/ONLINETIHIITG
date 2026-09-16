"""
Unified Surveillance Pipeline for Underwater Video Ingestion, Enhancement, Detection, and Tracking.
"""

from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass, asdict
import time
import cv2
import numpy as np

from .preprocessing import ContrastEnhancer, get_enhancer
from .detector import ObjectDetector, DetectionResult
from .tracker import GreedyIoUTracker, TrackedObject


@dataclass
class PipelineConfig:
    """Configuration container for the end-to-end surveillance pipeline."""
    enhancement_method: str = "clahe"
    clip_limit: float = 1.5
    tile_grid_size: Tuple[int, int] = (8, 8)
    gamma: float = 1.0
    weights_path: Optional[str] = None
    imgsz: int = 320
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.50
    tracking_max_age: int = 5
    device: str = "cpu"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SurveillancePipeline:
    """
    End-to-End Production Pipeline for Real-Time Underwater Visual Surveillance.
    Orchestrates:
    1. Preprocessing / CIELAB CLAHE Contrast Equalization
    2. YOLOv8n Object Detection
    3. Greedy IoU Multi-Object Tracking
    4. Hardware Latency Benchmarking and Telemetry
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        
        # 1. Initialize Enhancer
        self.enhancer = get_enhancer(
            method=self.config.enhancement_method,
            clip_limit=self.config.clip_limit,
            tile_grid_size=self.config.tile_grid_size,
            gamma=self.config.gamma
        )

        # 2. Initialize Detector
        self.detector = ObjectDetector(
            weights_path=self.config.weights_path,
            imgsz=self.config.imgsz,
            conf_threshold=self.config.confidence_threshold,
            iou_threshold=self.config.iou_threshold,
            device=self.config.device
        )

        # 3. Initialize Tracker
        self.tracker = GreedyIoUTracker(
            iou_threshold=self.config.iou_threshold,
            max_age=self.config.tracking_max_age
        )

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single image frame end-to-end.
        :param frame: Input BGR image numpy array (H, W, 3)
        :return: Structured dictionary containing metrics, detections, and tracks
        """
        if frame is None or frame.size == 0:
            return {"error": "Invalid or empty image frame", "status": "failed"}

        t_total_start = time.perf_counter()

        # Step 1: Contrast Enhancement
        t_pre_start = time.perf_counter()
        enhanced_frame = self.enhancer.enhance(frame)
        t_pre_end = time.perf_counter()
        pre_ms = (t_pre_end - t_pre_start) * 1000.0

        # Step 2: Object Detection
        t_det_start = time.perf_counter()
        detections = self.detector.detect(enhanced_frame)
        t_det_end = time.perf_counter()
        det_ms = (t_det_end - t_det_start) * 1000.0

        # Step 3: Multi-Object Tracking
        t_trk_start = time.perf_counter()
        tracks = self.tracker.update(detections)
        t_trk_end = time.perf_counter()
        trk_ms = (t_trk_end - t_trk_start) * 1000.0

        t_total_end = time.perf_counter()
        total_ms = (t_total_end - t_total_start) * 1000.0
        fps = 1000.0 / max(total_ms, 1e-6)

        return {
            "status": "success",
            "latency": {
                "preprocessing_ms": round(pre_ms, 3),
                "inference_ms": round(det_ms, 3),
                "tracking_ms": round(trk_ms, 3),
                "total_ms": round(total_ms, 3),
                "throughput_fps": round(fps, 2)
            },
            "detections": [d.to_dict() for d in detections],
            "tracks": [t.to_dict() for t in tracks]
        }

    def draw_overlay(self, frame: np.ndarray, result: Dict[str, Any]) -> np.ndarray:
        """
        Render visual overlays, bounding boxes, track IDs, and telemetry HUD on frame.
        :param frame: Original or enhanced BGR image
        :param result: Dictionary returned by process_frame
        :return: Annotated BGR image
        """
        annotated = frame.copy()
        tracks = result.get("tracks", [])
        latency = result.get("latency", {})

        # Draw Bounding Boxes and Track Labels
        for t in tracks:
            bbox = t.get("bbox", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, bbox)
            track_id = t.get("track_id", 0)
            cls_name = t.get("class_name", "object")
            conf = t.get("confidence", 0.0)

            # Draw Box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Label banner
            label = f"ID:{track_id} {cls_name} {conf:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated, (x1, max(0, y1 - 20)), (x1 + w + 6, max(20, y1)), (0, 255, 0), -1)
            cv2.putText(annotated, label, (x1 + 3, max(15, y1 - 4)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        # Draw Telemetry HUD Header
        total_ms = latency.get("total_ms", 0.0)
        fps = latency.get("throughput_fps", 0.0)
        hud_text = f"FPS: {fps:.1f} | Latency: {total_ms:.1f}ms | Method: {self.config.enhancement_method.upper()}"
        cv2.rectangle(annotated, (10, 10), (450, 45), (15, 23, 42), -1)
        cv2.rectangle(annotated, (10, 10), (450, 45), (59, 130, 246), 1)
        cv2.putText(annotated, hud_text, (20, 33),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

        return annotated
