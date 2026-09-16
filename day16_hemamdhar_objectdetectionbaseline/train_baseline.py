"""Train and evaluate a raw transfer-learning detector baseline."""

from __future__ import annotations

import argparse
import csv
import json
import platform
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path


def load_simple_config(path: Path) -> dict:
    config = {}
    current_section = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":") and not line.startswith("  "):
            current_section = line[:-1]
            config[current_section] = {}
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value in {"null", "None"}:
            parsed = None
        elif value.lower() in {"true", "false"}:
            parsed = value.lower() == "true"
        else:
            try:
                parsed = int(value)
            except ValueError:
                try:
                    parsed = float(value)
                except ValueError:
                    parsed = value.strip("'\"")
        if current_section and raw_line.startswith("  "):
            config[current_section][key] = parsed
        else:
            config[key] = parsed
    return config


def blocked(output: Path, reason: str) -> int:
    output.mkdir(parents=True, exist_ok=True)
    report = {"status": "blocked", "reason": reason, "date": date.today().isoformat()}
    (output / "baseline_status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 2


def dataset_records(manifest_path: Path, dataset_name: str) -> list[dict]:
    records = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [record for record in records if record.get("dataset") == dataset_name]


def write_detector_yaml(records: list[dict], dataset_name: str, output: Path) -> Path:
    split_paths = {}
    for split in ("train", "val", "test"):
        split_records = [record for record in records if record.get("split") == split]
        if not split_records:
            raise ValueError(f"missing split records: {split}")
        split_paths[split] = Path(split_records[0]["image"]).parent
    prepared_root = split_paths["train"].parents[2]
    yaml_path = output / "dataset.yaml"
    class_names = records[0].get("class_names", {})
    names = [class_names[key] for key in sorted(class_names, key=lambda value: int(value))]
    yaml_path.write_text(
        "\n".join([
            f"path: {prepared_root}",
            f"train: {split_paths['train'].relative_to(prepared_root)}",
            f"val: {split_paths['val'].relative_to(prepared_root)}",
            f"test: {split_paths['test'].relative_to(prepared_root)}",
            f"nc: {len(names)}",
            "names: [" + ", ".join(json.dumps(name) for name in names) + "]",
            f"dataset_name: {dataset_name}",
            ""]), encoding="utf-8")
    return yaml_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("detector_config.yaml"))
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    parser.add_argument("--epochs", type=int, default=None, help="Optional local-run override; record it in metrics.")
    parser.add_argument("--imgsz", type=int, default=None, help="Optional local-run image-size override; record it in metrics.")
    parser.add_argument("--fraction", type=float, default=1.0, help="Fraction of training data for an accelerated run.")
    args = parser.parse_args()
    config = load_simple_config(args.config)
    manifest = Path(config["manifest"])
    if not manifest.is_absolute():
        manifest = (args.config.parent / manifest).resolve()
    if not manifest.exists():
        return blocked(args.output / args.dataset_name / config["condition"], f"manifest_not_found:{manifest}")
    try:
        from ultralytics import YOLO
    except ImportError:
        return blocked(args.output / args.dataset_name / config["condition"], "ultralytics_not_installed")
    records = dataset_records(manifest, args.dataset_name)
    if not records:
        return blocked(args.output / args.dataset_name / config["condition"], f"dataset_not_found_in_manifest:{args.dataset_name}")
    run_output = args.output / args.dataset_name / config["condition"]
    run_output.mkdir(parents=True, exist_ok=True)
    try:
        dataset_yaml = write_detector_yaml(records, args.dataset_name, run_output)
        model = YOLO(config["model"])
        train_start = time.perf_counter()
        epochs = args.epochs if args.epochs is not None else int(config["epochs"])
        image_size = args.imgsz if args.imgsz is not None else int(config["image_size"])
        model.train(data=str(dataset_yaml), imgsz=image_size, epochs=epochs, batch=int(config["batch"]), workers=int(config["workers"]), seed=int(config["seed"]), fraction=args.fraction, project=str(run_output), name="train", exist_ok=True, augment=False)
        train_seconds = time.perf_counter() - train_start
        best_checkpoint = run_output / "train" / "weights" / "best.pt"
        if not best_checkpoint.exists():
            return blocked(run_output, "training_completed_without_best_checkpoint")
        evaluator = YOLO(str(best_checkpoint))
        validation_start = time.perf_counter()
        metrics = evaluator.val(data=str(dataset_yaml), split="test", imgsz=image_size, conf=float(config["confidence_threshold"]), iou=float(config["iou_threshold"]), plots=True, project=str(run_output), name="test", exist_ok=True)
        elapsed = time.perf_counter() - validation_start
        results = getattr(metrics, "results_dict", {})
        prediction_dir = run_output / "predictions"
        test_source = Path(next(record["image"] for record in records if record.get("split") == "test")).parent
        evaluator.predict(source=str(test_source), imgsz=image_size, conf=float(config["confidence_threshold"]), iou=float(config["iou_threshold"]), save=True, save_txt=True, save_conf=True, project=str(run_output), name="predictions", exist_ok=True)
        per_class_ap = {}
        if hasattr(metrics, "box") and hasattr(metrics.box, "ap_class_index") and hasattr(metrics.box, "ap"):
            per_class_ap = {
                str(int(class_id)): (float(value) if getattr(value, "ndim", 0) == 0 else [float(item) for item in value])
                for class_id, value in zip(metrics.box.ap_class_index, metrics.box.ap)
            }
        speed = getattr(metrics, "speed", {})
        parameter_count = sum(parameter.numel() for parameter in evaluator.model.parameters()) if hasattr(evaluator, "model") else None
        checkpoint_size_mb = best_checkpoint.stat().st_size / (1024 * 1024)
        metric_record = {
            "run_id": f"D16-{args.dataset_name}-{config['condition']}", "date": date.today().isoformat(), "dataset": args.dataset_name,
            "condition": config["condition"], "dataset_version": "prepared_dataset_v1", "manifest": str(manifest), "split": "test",
            "model": config["model"], "seed": config["seed"], "image_size": image_size, "epochs": epochs, "fraction": args.fraction,
            "precision": results.get("metrics/precision(B)"), "recall": results.get("metrics/recall(B)"),
            "map50": results.get("metrics/mAP50(B)"), "map50_95": results.get("metrics/mAP50-95(B)"),
            "per_class_ap": per_class_ap, "speed": speed,
            "parameter_count": parameter_count, "model_size_mb": round(checkpoint_size_mb, 4),
            "evaluation_seconds": round(elapsed, 4), "train_seconds": round(train_seconds, 4),
            "checkpoint_path": str(best_checkpoint), "prediction_path": str(prediction_dir), "status": "complete",
            "software": f"python={sys.version.split()[0]}, platform={platform.platform()}",
        }
        (run_output / "metrics.json").write_text(json.dumps(metric_record, indent=2), encoding="utf-8")
        with (run_output / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=metric_record.keys())
            writer.writeheader()
            writer.writerow(metric_record)
        print(json.dumps(metric_record, indent=2))
        return 0
    except Exception as exc:
        return blocked(run_output, f"baseline_error:{type(exc).__name__}:{exc}")


if __name__ == "__main__":
    raise SystemExit(main())
