"""
Preprocessing and Enhancement Kernels for Underwater Imagery.
Provides optimized CIELAB CLAHE, Gamma correction, and Identity enhancement modules.
"""

from typing import Tuple, Optional
import cv2
import numpy as np


class ContrastEnhancer:
    """Base class for image contrast enhancers."""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance input BGR or RGB image.
        :param image: Input numpy array (H, W, 3)
        :return: Enhanced numpy array (H, W, 3)
        """
        raise NotImplementedError


class CIELABCLAHEEnhancer(ContrastEnhancer):
    """
    Contrast Limited Adaptive Histogram Equalization applied strictly
    to the L* (Lightness) channel of the CIELAB color space.
    Preserves chromaticity (a*, b*) to prevent artificial color distortion.
    """

    def __init__(self, clip_limit: float = 1.5, tile_grid_size: Tuple[int, int] = (8, 8)):
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def enhance(self, image: np.ndarray) -> np.ndarray:
        if image is None or image.size == 0:
            raise ValueError("Input image cannot be None or empty.")
        
        # Convert BGR to CIELAB
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Equalize only the Lightness (L*) channel
        l_eq = self.clahe.apply(l)
        
        # Merge back and convert to BGR
        enhanced_lab = cv2.merge((l_eq, a, b))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        return enhanced_bgr


class GammaCorrectionEnhancer(ContrastEnhancer):
    """Non-linear gamma correction baseline for ablation and diagnostics."""

    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
        inv_gamma = 1.0 / max(gamma, 1e-6)
        self.table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    def enhance(self, image: np.ndarray) -> np.ndarray:
        if image is None or image.size == 0:
            raise ValueError("Input image cannot be None or empty.")
        return cv2.LUT(image, self.table)


class IdentityEnhancer(ContrastEnhancer):
    """Pass-through enhancer representing raw, unenhanced input."""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        return image.copy()


def get_enhancer(method: str = "clahe", clip_limit: float = 1.5, tile_grid_size: Tuple[int, int] = (8, 8), gamma: float = 1.0) -> ContrastEnhancer:
    """Factory function to instantiate contrast enhancers."""
    method_clean = method.lower().strip()
    if method_clean in ["clahe", "clahe_v2", "clahe_v1", "clahe_v3"]:
        return CIELABCLAHEEnhancer(clip_limit=clip_limit, tile_grid_size=tile_grid_size)
    elif method_clean in ["gamma", "gamma_v1"]:
        return GammaCorrectionEnhancer(gamma=gamma)
    elif method_clean in ["raw", "raw_v1", "none", "identity"]:
        return IdentityEnhancer()
    else:
        raise ValueError(f"Unknown enhancement method: {method}. Supported: 'clahe', 'gamma', 'raw'.")
