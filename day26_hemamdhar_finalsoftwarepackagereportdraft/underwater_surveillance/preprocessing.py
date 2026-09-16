"""
Photometric Preprocessing Module for Underwater Visual Data.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Tuple, Union

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


def CIELAB_CLAHE(
    image: np.ndarray,
    clip_limit: float = 1.5,
    grid_size: int = 8
) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization exclusively to the
    Lightness (L*) channel in CIELAB color space, preserving a* and b* chromaticity.

    Parameters:
        image (np.ndarray): Input RGB image array [H, W, 3], uint8.
        clip_limit (float): Threshold for contrast limiting. Default is 1.5.
        grid_size (int): Tile grid size for local equalization. Default is 8 (8x8).

    Returns:
        np.ndarray: Enhanced RGB image array [H, W, 3], uint8.
    """
    if cv2 is None:
        raise RuntimeError("OpenCV (cv2) is required for CIELAB CLAHE enhancement.")

    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    lightness, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(int(grid_size), int(grid_size)))
    enhanced_l = clahe.apply(lightness)

    merged = cv2.merge((enhanced_l, a_channel, b_channel))
    enhanced_rgb = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
    return enhanced_rgb


class PhotometricPreprocessor:
    """High-performance preprocessor for underwater imagery."""

    def __init__(
        self,
        method: str = "clahe",
        clip_limit: float = 1.5,
        grid_size: int = 8
    ):
        self.method = method.lower()
        self.clip_limit = float(clip_limit)
        self.grid_size = int(grid_size)

        if self.method == "clahe" and cv2 is not None:
            self._clahe_op = cv2.createCLAHE(
                clipLimit=self.clip_limit,
                tileGridSize=(self.grid_size, self.grid_size)
            )
        else:
            self._clahe_op = None

    def process(
        self,
        image_input: Union[Image.Image, np.ndarray, str, Path]
    ) -> Tuple[np.ndarray, float]:
        """
        Process an input image and return the enhanced RGB array and latency in ms.
        """
        start = time.perf_counter()

        if isinstance(image_input, (str, Path)):
            pil_img = Image.open(image_input).convert("RGB")
            arr = np.asarray(pil_img)
        elif isinstance(image_input, Image.Image):
            arr = np.asarray(image_input.convert("RGB"))
        elif isinstance(image_input, np.ndarray):
            arr = image_input if image_input.ndim == 3 else np.repeat(image_input[:, :, None], 3, axis=2)
        else:
            raise TypeError(f"Unsupported image input type: {type(image_input)}")

        if self.method in ["raw", "raw_v1", "identity"]:
            latency_ms = (time.perf_counter() - start) * 1000.0
            return arr, latency_ms

        if self.method == "clahe":
            if cv2 is None:
                raise RuntimeError("OpenCV is required for CLAHE.")
            lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            enhanced_l = self._clahe_op.apply(l)
            enhanced_rgb = cv2.cvtColor(cv2.merge((enhanced_l, a, b)), cv2.COLOR_LAB2RGB)
            latency_ms = (time.perf_counter() - start) * 1000.0
            return enhanced_rgb, latency_ms

        raise ValueError(f"Unknown preprocessing method: {self.method}")
