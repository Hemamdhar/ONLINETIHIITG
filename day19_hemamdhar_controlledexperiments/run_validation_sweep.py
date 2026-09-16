"""Run a validation-only CLAHE parameter sweep with the frozen Day 16 detector."""
from __future__ import annotations

import csv
import json
import platform
import shutil
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
MANIFEST = REPO / "day11_hemamdhar_visionpreprocessing" / "prepared_dataset_v1" / "manifest_v1.json"
CHECKPOINT = REPO / "day16_hemamdhar_objectdetectionbaseline" / "outputs" / "DIATAquarium.v4i.yolov8" / "raw_v1" / "train" / "weights" / "best.pt"
DERIVED = ROOT / "validation_derivatives_v1"
OUTPUTS = ROOT / "validation_outputs_v1"
LOG = ROOT / "experiment_log_v1.csv"
BEST = ROOT / "best_validated_config.json"

sys.path.insert(0, str(REPO / "day13_hemamdhar_enhancementdetectionpreparation"))
from enhance_baselines import enhance

from ultralytics import YOLO

CANDIDATES = [
    {"experiment_id": "D19-raw-control", "condition": "raw_v1", "clip_limit": "", "grid_size": ""},
    {"experiment_id": "D19-clahe-1p5x8", "condition": "clahe_v1", "clip_limit": 1.5, "grid_size": 8},
    {"experiment_id": "D19-clahe-2x8", "condition": "clahe_v1", "clip_limit": 2.0, "grid_size": 8},
    {"experiment_id": "D19-clahe-3x8", "condition": "clahe_v1", "clip_limit": 3.0, "grid_size": 8},
]


def main() -> None:
    records = [
        record for record in json.loads(MANIFEST.read_text(encoding="utf-8"))
        if record.get("dataset") == "DIATAquarium.v4i.yolov8" and record.get("split") == "val"
    ]
    records = sorted(records, key=lambda record: record["image"])[:256]
    if not records:
        raise RuntimeError("No DIAT validation records found")
    if not CHECKPOINT.exists():
        raise FileNotFoundError(CHECKPOINT)

    DERIVED.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    model = YOLO(str(CHECKPOINT))
    rows = []
    for candidate in CANDIDATES:
        condition_dir = DERIVED / candidate["experiment_id"]
        if condition_dir.exists():
            shutil.rmtree(condition_dir)
        condition_dir.mkdir(parents=True)
        sources = []
        generation_start = time.perf_counter()
        for record in records:
            source = Path(record["image"])
            destination = condition_dir / source.name
            with Image.open(source) as image:
                if candidate["condition"] == "raw_v1":
                    transformed = image.convert("RGB")
                else:
                    transformed = enhance(
                        image,
                        "clahe",
                        gamma=1.0,
                        contrast=1.0,
                        clip_limit=float(candidate["clip_limit"]),
                        grid_size=int(candidate["grid_size"]),
                    )
                transformed.save(destination, quality=95)
            sources.append(str(destination))
        preprocessing_seconds = time.perf_counter() - generation_start

        inference_start = time.perf_counter()
        result_stream = model.predict(
            source=sources,
            imgsz=320,
            conf=0.25,
            iou=0.50,
            batch=16,
            device="cpu",
            verbose=False,
            save=False,
            stream=True,
        )
        image_count = 0
        detections = 0
        for result in result_stream:
            image_count += 1
            detections += len(result.boxes)
        inference_seconds = time.perf_counter() - inference_start
        rows.append(
            {
                "experiment_id": candidate["experiment_id"],
                "split": "val",
                "dataset": "DIATAquarium.v4i.yolov8",
                "condition": candidate["condition"],
                "clip_limit": candidate["clip_limit"],
                "grid_size": candidate["grid_size"],
                "images": image_count,
                "detections": detections,
                "precision": "not_computed",
                "recall": "not_computed",
                "mAP50": "not_computed",
                "mAP50_95": "not_computed",
                "preprocess_ms_per_image": preprocessing_seconds * 1000 / len(records),
                "inference_ms_per_image": inference_seconds * 1000 / image_count,
                "fps": image_count / max(inference_seconds, 1e-9),
                "selection_metric": "detections_then_lower_inference_time",
                "status": "complete_validation_sweep",
                "notes": "Frozen Day 16 smoke checkpoint; accuracy metrics not computed by this inference-only sweep.",
            }
        )

    fieldnames = list(rows[0])
    with LOG.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    best = max(rows, key=lambda row: (int(row["detections"]), -float(row["inference_ms_per_image"])))
    best_config = {
        "status": "best_validated_configuration_for_smoke_sweep",
        "experiment_id": best["experiment_id"],
        "dataset": best["dataset"],
        "split_used_for_selection": best["split"],
        "condition": best["condition"],
        "clip_limit": float(best["clip_limit"]) if best["clip_limit"] else None,
        "grid_size": int(best["grid_size"]) if best["grid_size"] else None,
        "model_checkpoint": str(CHECKPOINT),
        "image_size": 320,
        "confidence_threshold": 0.25,
        "iou_threshold": 0.50,
        "batch": 16,
        "device": "cpu",
        "test_touched": False,
        "selection_rule": "maximize validation detections; break ties with lower inference time",
        "caveat": "This is not an accuracy winner: the abbreviated checkpoint produced no validated precision/recall/mAP calculation in this sweep.",
    }
    BEST.write_text(json.dumps(best_config, indent=2), encoding="utf-8")
    print(json.dumps({"log": str(LOG), "best": best_config}, indent=2))


if __name__ == "__main__":
    main()
