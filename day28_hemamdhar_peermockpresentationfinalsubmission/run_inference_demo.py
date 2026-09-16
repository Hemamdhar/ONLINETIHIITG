#!/usr/bin/env python3
"""
Stand-alone Inference and Pipeline Verification Demo Script for Day 28 Submission.
Runs the complete CIELAB CLAHE + YOLOv8n + Greedy IoU Tracker pipeline on sample underwater imagery.
"""

import sys
import json
from pathlib import Path
import cv2
import numpy as np

# Add parent directory to path so underwater_surveillance can be imported directly
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from underwater_surveillance import SurveillancePipeline, PipelineConfig


def main():
    print("=== Underwater Visual Surveillance: Live Submission Inference Demo ===")
    
    # Locate dataset frame or sample
    sample_candidates = [
        CURRENT_DIR.parent / "day11_hemamdhar_visionpreprocessing/prepared_dataset_v1/val/DIATAquarium.v4i.yolov8/images/av0_0_20231228_102111_mp4-0_jpg.rf.7aa4fa3149688bd7abd114bfa46704b4.jpg",
        CURRENT_DIR.parent / "day10_hemamdhar_visualeda/dataset/val/images/av0_0_20231228_102111_mp4-0_jpg.rf.7aa4fa3149688bd7abd114bfa46704b4.jpg",
    ]

    target_image = None
    for cand in sample_candidates:
        if cand.exists():
            target_image = cand
            break

    if target_image is None or not target_image.exists():
        print("[Demo] Creating synthetic underwater frame for verification...")
        frame = np.full((640, 640, 3), (120, 80, 20), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 80, (200, 160, 50), -1)
    else:
        print(f"Target Input Frame: {target_image}")
        frame = cv2.imread(str(target_image))

    # Initialize frozen production pipeline
    config = PipelineConfig(
        enhancement_method="clahe",
        clip_limit=1.5,
        tile_grid_size=(8, 8),
        weights_path=str(CURRENT_DIR.parent / "yolov8n.pt"),
        imgsz=320,
        confidence_threshold=0.25,
        iou_threshold=0.50,
        tracking_max_age=5,
        device="cpu"
    )
    pipeline = SurveillancePipeline(config)

    # Execute end-to-end pipeline
    result = pipeline.process_frame(frame)

    # Render visual output
    annotated = pipeline.draw_overlay(frame, result)
    output_path = CURRENT_DIR / "demo_submission_inference_output.png"
    cv2.imwrite(str(output_path), annotated)
    print(f"Saved visual demo output to: {output_path}")

    # Output structured payload
    print("\n--- Structured Output Payload ---")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
