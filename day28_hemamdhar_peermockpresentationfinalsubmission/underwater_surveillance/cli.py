"""
Command-Line Interface (CLI) for underwater_surveillance package.
Allows running single-frame or batch video inference from the terminal.
"""

import argparse
import json
import sys
from pathlib import Path
import cv2

from .pipeline import SurveillancePipeline, PipelineConfig


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI-Based Underwater Visual Surveillance CLI (v1.0.0)"
    )
    parser.add_argument(
        "--input", "-i", required=True, type=str,
        help="Path to input image file or directory"
    )
    parser.add_argument(
        "--output", "-o", default=None, type=str,
        help="Path to save annotated output image or JSON summary"
    )
    parser.add_argument(
        "--method", "-m", default="clahe", choices=["clahe", "raw", "raw_v1", "gamma"],
        help="Enhancement method to apply"
    )
    parser.add_argument(
        "--clip-limit", type=float, default=1.5,
        help="CLAHE clip limit (default: 1.5)"
    )
    parser.add_argument(
        "--grid-size", type=int, default=8,
        help="CLAHE grid tile size (default: 8 for 8x8)"
    )
    parser.add_argument(
        "--weights", "-w", default=None, type=str,
        help="Path to YOLOv8n detector weights"
    )
    parser.add_argument(
        "--imgsz", type=int, default=320,
        help="Inference resolution (default: 320)"
    )
    parser.add_argument(
        "--conf", type=float, default=0.25,
        help="Confidence threshold (default: 0.25)"
    )
    parser.add_argument(
        "--iou", type=float, default=0.50,
        help="IoU NMS threshold (default: 0.50)"
    )
    parser.add_argument(
        "--json-only", action="store_true",
        help="Print structured JSON result only without saving image"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[Error] Input path '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Initialize Pipeline
    config = PipelineConfig(
        enhancement_method=args.method,
        clip_limit=args.clip_limit,
        tile_grid_size=(args.grid_size, args.grid_size),
        weights_path=args.weights,
        imgsz=args.imgsz,
        confidence_threshold=args.conf,
        iou_threshold=args.iou
    )
    pipeline = SurveillancePipeline(config)

    # Load image
    image = cv2.imread(str(input_path))
    if image is None:
        print(f"[Error] Failed to decode image '{args.input}'.", file=sys.stderr)
        sys.exit(1)

    # Process frame
    result = pipeline.process_frame(image)

    # Output JSON payload
    print(json.dumps(result, indent=2))

    # Save visual output if requested
    if args.output and not args.json_only:
        annotated = pipeline.draw_overlay(image, result)
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_path), annotated)
        print(f"Saved annotated image to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
