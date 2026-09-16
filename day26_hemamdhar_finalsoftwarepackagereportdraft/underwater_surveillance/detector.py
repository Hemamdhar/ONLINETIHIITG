"""
Object Detection Module for Underwater Organisms.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np


@dataclass
class BoundingBox:
    """Bounding box detection representation."""
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
    class_name: str = ""

    @property
    def box_coords(self) -> Tuple[float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2)

    @property
    def area(self) -> float:
        return max(0.0, self.x2 - self.x1) * max(0.0, self.y2 - self.y1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bbox": [round(self.x1, 2), round(self.y1, 2), round(self.x2, 2), round(self.y2, 2)],
            "confidence": round(self.confidence, 4),
            "class_id": self.class_id,
            "class_name": self.class_name
        }


class ObjectDetector:
    """Deep learning detector engine based on YOLOv8n architecture."""

    def __init__(
        self,
        weights_path: Optional[Union[str, Path]] = None,
        image_size: int = 320,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.50,
        device: str = "cpu"
    ):
        self.weights_path = str(weights_path) if weights_path else None
        self.image_size = int(image_size)
        self.conf_threshold = float(conf_threshold)
        self.iou_threshold = float(iou_threshold)
        self.device = device
        self._model = None

    def _load_model(self):
        if self._model is None and self.weights_path:
            try:
                from ultralytics import YOLO
                self._model = YOLO(self.weights_path)
            except Exception as e:
                self._model = None
        return self._model

    def detect(
        self,
        image: np.ndarray
    ) -> Tuple[List[BoundingBox], float]:
        """
        Execute forward pass on image and return detected bounding boxes and latency.
        """
        start = time.perf_counter()
        detections: List[BoundingBox] = []
        model = self._load_model()

        if model is not None:
            results = model.predict(
                source=image,
                imgsz=self.image_size,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=False,
                device=self.device
            )
            for res in results:
                for box in res.boxes:
                    coords = box.xyxy[0].cpu().numpy().tolist()
                    conf = float(box.conf[0].cpu().numpy())
                    cls_id = int(box.cls[0].cpu().numpy())
                    cls_name = model.names.get(cls_id, str(cls_id)) if hasattr(model, "names") else str(cls_id)
                    detections.append(BoundingBox(
                        x1=coords[0],
                        y1=coords[1],
                        x2=coords[2],
                        y2=coords[3],
                        confidence=conf,
                        class_id=cls_id,
                        class_name=cls_name
                    ))

        latency_ms = (time.perf_counter() - start) * 1000.0
        return detections, latency_ms
