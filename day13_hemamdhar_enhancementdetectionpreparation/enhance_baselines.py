"""Generate read-only photometric enhancement baselines from Dataset V1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image, ImageEnhance
except ImportError:
    Image = ImageEnhance = None


def enhance(image: "Image.Image", method: str, gamma: float, contrast: float, clip_limit: float, grid_size: int):
    if method == "raw":
        return image.convert("RGB")
    if method == "gamma":
        if ImageEnhance is None:
            raise RuntimeError("Pillow is required for gamma baseline")
        enhanced = ImageEnhance.Contrast(image.convert("RGB")).enhance(contrast)
        if gamma == 1.0:
            return enhanced
        lookup = [min(255, max(0, int(((value / 255.0) ** gamma) * 255.0))) for value in range(256)]
        return enhanced.point(lookup * 3)
    if method == "clahe":
        if cv2 is None:
            raise RuntimeError("OpenCV is required for CLAHE baseline")
        import numpy as np
        array = np.asarray(image.convert("RGB"))
        lab = cv2.cvtColor(array, cv2.COLOR_RGB2LAB)
        lightness, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        result = cv2.cvtColor(cv2.merge((clahe.apply(lightness), a_channel, b_channel)), cv2.COLOR_LAB2RGB)
        return Image.fromarray(result)
    raise ValueError(f"unknown enhancement method: {method}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--methods", nargs="+", default=["raw", "clahe", "gamma"], choices=["raw", "clahe", "gamma"])
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--contrast", type=float, default=1.0)
    parser.add_argument("--clip-limit", type=float, default=2.0)
    parser.add_argument("--grid-size", type=int, default=8)
    args = parser.parse_args()
    if not args.manifest.exists():
        report = {"status": "blocked", "reason": f"manifest_not_found:{args.manifest}"}
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "enhancement_status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2
    if Image is None:
        raise RuntimeError("Pillow is required to generate enhancement baselines")
    records = json.loads(args.manifest.read_text(encoding="utf-8"))
    generated = []
    for method in args.methods:
        for record in records:
            source = Path(record["image"])
            if not source.exists():
                raise FileNotFoundError(source)
            destination = args.output / method / record["split"] / record["dataset"] / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source) as image:
                enhance(image, method, args.gamma, args.contrast, args.clip_limit, args.grid_size).save(destination, quality=95)
            generated.append({"method": method, "source": str(source), "output": str(destination), "split": record["split"], "dataset": record["dataset"], "group": record["group"], "source_sha256": record["source_sha256"]})
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "enhancement_manifest_v1.json").write_text(json.dumps(generated, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ready", "records": len(generated), "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
