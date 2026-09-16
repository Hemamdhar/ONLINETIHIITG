"""
Command-Line Interface for the Underwater Surveillance Pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from PIL import Image

from .pipeline import SurveillancePipeline


def main():
    parser = argparse.ArgumentParser(description="AI-Based Underwater Visual Surveillance CLI")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to input image or sequence directory")
    parser.add_argument("--output", "-o", type=str, default=None, help="Path to save output JSON or enhanced image")
    parser.add_argument("--method", "-m", type=str, default="clahe", choices=["clahe", "raw", "raw_v1"], help="Enhancement method")
    parser.add_argument("--clip-limit", type=float, default=1.5, help="CLAHE clip limit")
    parser.add_argument("--grid-size", type=int, default=8, help="CLAHE grid tile size")
    parser.add_argument("--weights", "-w", type=str, default=None, help="Path to YOLOv8n detector weights")
    parser.add_argument("--imgsz", type=int, default=320, help="Inference resolution")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--iou", type=float, default=0.50, help="IoU NMS threshold")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    pipeline = SurveillancePipeline(
        enhancement_method=args.method,
        clip_limit=args.clip_limit,
        grid_size=args.grid_size,
        weights_path=args.weights,
        image_size=args.imgsz,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )

    if input_path.is_file():
        result = pipeline.process_frame(input_path)
        enhanced = result.pop("enhanced_image")
        
        output_str = json.dumps(result, indent=2)
        print(output_str)

        if args.output:
            out_p = Path(args.output)
            if out_p.suffix.lower() in [".jpg", ".png", ".jpeg"]:
                Image.fromarray(enhanced).save(out_p)
                print(f"Saved enhanced image to {out_p}")
            else:
                out_p.write_text(output_str, encoding="utf-8")
                print(f"Saved output JSON to {out_p}")
    else:
        # Directory of sequence frames
        image_files = sorted(list(input_path.glob("*.jpg")) + list(input_path.glob("*.png")))
        print(f"Processing sequence of {len(image_files)} frames...")
        seq_results = pipeline.process_sequence(image_files)
        for r in seq_results:
            r.pop("enhanced_image", None)
        
        summary = {
            "total_frames": len(seq_results),
            "results": seq_results
        }
        output_str = json.dumps(summary, indent=2)
        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"Saved sequence results to {args.output}")
        else:
            print(output_str)


if __name__ == "__main__":
    main()
