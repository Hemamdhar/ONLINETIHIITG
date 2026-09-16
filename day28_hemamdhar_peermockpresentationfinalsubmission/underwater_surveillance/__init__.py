"""
Underwater Surveillance Package (underwater_surveillance)
Version 1.0.0
Author: Hemamdhar Dakarapu

A real-time, edge-optimized visual surveillance package designed for underwater robotics.
Features CIELAB CLAHE enhancement, YOLOv8n object detection, and greedy IoU multi-object tracking.
"""

from .preprocessing import ContrastEnhancer, CIELABCLAHEEnhancer, get_enhancer
from .detector import ObjectDetector, DetectionResult
from .tracker import GreedyIoUTracker, TrackedObject
from .pipeline import SurveillancePipeline, PipelineConfig

__version__ = "1.0.0"
__author__ = "Hemamdhar Dakarapu"
__all__ = [
    "ContrastEnhancer",
    "CIELABCLAHEEnhancer",
    "get_enhancer",
    "ObjectDetector",
    "DetectionResult",
    "GreedyIoUTracker",
    "TrackedObject",
    "SurveillancePipeline",
    "PipelineConfig",
    "__version__",
]
