"""
AI-Based Underwater Visual Surveillance Package
Author: Hemamdhar Dakarapu
Version: 1.0.0
"""

from .preprocessing import PhotometricPreprocessor, CIELAB_CLAHE
from .detector import ObjectDetector, BoundingBox
from .tracker import SpatialIoUTracker, Tracklet
from .pipeline import SurveillancePipeline

__version__ = "1.0.0"
__all__ = [
    "PhotometricPreprocessor",
    "CIELAB_CLAHE",
    "ObjectDetector",
    "BoundingBox",
    "SpatialIoUTracker",
    "Tracklet",
    "SurveillancePipeline",
]
