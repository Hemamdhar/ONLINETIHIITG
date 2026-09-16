"""
Object Detection Engine for Underwater Surveillance.
Wraps YOLOv8n object detection with fast inference and confidence filtering.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np


@dataclass
class DetectionResult:
    """Represents an individual detected bounding box."""
    bbox: List[float]  # [x1, y1, x2, y2]
    confidence: float
    class_id: int
    class_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ObjectDetector:
    """
    Underwater Object Detector utilizing lightweight YOLOv8n.
    Supports edge compute inference with configurable confidence and IoU thresholds.
    """

    def __init__(
        self,
        weights_path: Optional[str] = None,
        imgsz: int = 320,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.50,
        device: str = "cpu"
    ):
        self.imgsz = imgsz
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.device = device
        self.model = None

        # Resolve weights path
        if weights_path is not None and Path(weights_path).exists():
            self._load_model(weights_path)
        else:
            # Check default workspace weights
            default_weights = Path(__file__).resolve().parent.parent.parent / "yolov8n.pt"
            if default_weights.exists():
                self._load_model(str(default_weights))
            else:
                self.model = None

    def _load_model(self, path: str):
        try:
            from ultralytics import YOLO
            self.model = YOLO(path)
        except Exception as e:
            print(f"[Detector Warning] Ultralytics YOLO loading failed: {e}. Operating in mock/test mode.")
            self.model = None

    def detect(self, image: np.ndarray) -> List[DetectionResult]:
        """
        Run inference on preprocessed frame.
        :param image: BGR image numpy array
        :return: List of DetectionResult objects
        """
        if image is None or image.size == 0:
            return []

        if self.model is None:
            # Fallback mock detector for isolated unit tests / environments
            return []

        try:
            results = self.model.predict(
                source=image,
                imgsz=self.imgsz,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                device=self.device,
                verbose=False
            )
            
            detections: List[DetectionResult] = []
            for r in results:
                boxes = r.boxes
                if boxes is None:
                    continue
                for box in boxes:
                    xyxy = box.xyxy[0].tolist()
                    conf = float(box.conf[0].item())
                    cls_id = int(box.cls[0].item())
                    cls_name = r.names.get(cls_id, f"class_{cls_id}")
                    detections.append(DetectionResult(
                        bbox=[round(coord, 2) for coord in xyxy],
                        confidence=round(conf, 4),
                        class_id=cls_id,
                        class_name=cls_name
                    ))
            return detections
        except Exception as e:
            print(f"[Detector Error] Inference failed: {e}")
            return []
