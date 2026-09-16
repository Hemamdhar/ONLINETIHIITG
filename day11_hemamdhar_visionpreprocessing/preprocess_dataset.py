"""Build Prepared Dataset V1 without modifying the raw archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image
except ImportError:
    Image = None

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_class_names(dataset_root: Path) -> Dict[int, str]:
    for config_path in list(dataset_root.rglob("data.yaml")) + list(dataset_root.rglob("data.yml")):
        names = {}
        text = config_path.read_text(encoding="utf-8", errors="replace")
        names_match = re.search(r"^names:\s*\[(.*?)\]", text, flags=re.MULTILINE | re.DOTALL)
        if names_match:
            values = re.findall(r"['\"]([^'\"]+)['\"]", names_match.group(1))
            return {index: value for index, value in enumerate(values)}
        for line in text.splitlines():
            match = re.match(r"\s*(\d+)\s*:\s*['\"]?(.+?)['\"]?\s*$", line)
            if match:
                names[int(match.group(1))] = match.group(2).strip(" \\\"'")
        if names:
            return names
    return {}


def image_for_label(label_path: Path) -> Optional[Path]:
    for candidate in label_path.parent.parent.glob(f"{label_path.stem}.*"):
        if candidate.suffix.lower() in IMAGE_EXTENSIONS:
            return candidate
    return None


def source_group(image_path: Path, dataset_root: Path, pattern: str) -> str:
    stem = image_path.stem
    match = re.match(pattern, stem, flags=re.IGNORECASE)
    if match:
        return f"{dataset_root.name}:{match.group(1)}"
    return f"{dataset_root.name}:{image_path.parent.name}:{stem.rsplit('_', 1)[0]}"


def parse_label(label_path: Path, class_names: Dict[int, str]) -> Tuple[List[List[float]], List[str]]:
    rows, errors = [], []
    for line_number, line in enumerate(label_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        fields = line.split()
        if not fields:
            continue
        if len(fields) != 5:
            errors.append(f"line_{line_number}:expected_5_fields")
            continue
        try:
            values = [float(value) for value in fields]
            class_id = int(fields[0])
        except ValueError:
            errors.append(f"line_{line_number}:non_numeric")
            continue
        if class_names and class_id not in class_names:
            errors.append(f"line_{line_number}:unknown_class_{class_id}")
        if any(value < 0 or value > 1 for value in values[1:]):
            errors.append(f"line_{line_number}:coordinate_out_of_range")
        if values[3] <= 0 or values[4] <= 0:
            errors.append(f"line_{line_number}:non_positive_box_size")
        rows.append([class_id, *values[1:]])
    return rows, errors


def build_records(archive: Path, config: dict) -> Tuple[List[dict], List[str]]:
    records, errors = [], []
    if not archive.exists():
        return records, [f"archive_not_found:{archive}"]
    for dataset_root in sorted(path for path in archive.iterdir() if path.is_dir() and path.name != "inspection_outputs"):
        class_names = read_class_names(dataset_root)
        for image_path in sorted(dataset_root.rglob("*")):
            if not image_path.is_file() or image_path.suffix.lower() not in set(config["image_extensions"]):
                continue
            relative = image_path.relative_to(dataset_root)
            label_path = next((candidate for candidate in dataset_root.rglob(f"{image_path.stem}.txt") if candidate.parent.name == "labels"), None)
            if label_path is None:
                errors.append(f"missing_label:{image_path}")
                continue
            if Image is None:
                errors.append("pillow_required_for_preprocessing")
                return records, errors
            try:
                with Image.open(image_path) as image:
                    image.verify()
                with Image.open(image_path) as image:
                    width, height = image.size
            except Exception as exc:
                errors.append(f"unreadable_image:{image_path}:{type(exc).__name__}")
                continue
            labels, label_errors = parse_label(label_path, class_names)
            if label_errors:
                errors.extend(f"{image_path}:{item}" for item in label_errors)
                continue
            records.append({
                "dataset": dataset_root.name,
                "source_path": str(image_path),
                "relative_path": str(relative),
                "label_path": str(label_path),
                "source_sha256": sha256(image_path),
                "width": width,
                "height": height,
                "labels": labels,
                "class_names": class_names,
                "group": source_group(image_path, dataset_root, config["grouping"]["filename_sequence_regex"]),
            })
    return records, errors


def assign_splits(records: List[dict], config: dict) -> Dict[str, str]:
    groups = defaultdict(list)
    for record in records:
        groups[(record["dataset"], record["group"])].append(record)
    counts = {"train": 0, "val": 0, "test": 0}
    assignments = {}
    datasets = sorted({record["dataset"] for record in records})
    for dataset in datasets:
        dataset_groups = {key: value for key, value in groups.items() if key[0] == dataset}
        ordered_groups = sorted(dataset_groups, key=lambda item: hashlib.sha256(f"{config['split_seed']}:{item}".encode()).hexdigest())
        total = sum(len(value) for value in dataset_groups.values())
        targets = {"train": total * config["split_ratios"]["train"], "val": total * config["split_ratios"]["val"], "test": total * config["split_ratios"]["test"]}
        dataset_counts = {"train": 0, "val": 0, "test": 0}
        for group_key in ordered_groups:
            group_size = len(dataset_groups[group_key])
            split = min(("train", "val", "test"), key=lambda name: dataset_counts[name] - targets[name])
            for record in dataset_groups[group_key]:
                assignments[record["source_path"]] = split
            dataset_counts[split] += group_size
            counts[split] += group_size
    return assignments


def letterbox(image: "Image.Image", labels: List[List[float]], target_size: Tuple[int, int]):
    target_width, target_height = target_size
    original_width, original_height = image.size
    scale = min(target_width / original_width, target_height / original_height)
    resized_width = max(1, round(original_width * scale))
    resized_height = max(1, round(original_height * scale))
    resized = image.convert("RGB").resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_width, target_height), (114, 114, 114))
    pad_x = (target_width - resized_width) / 2
    pad_y = (target_height - resized_height) / 2
    canvas.paste(resized, (round(pad_x), round(pad_y)))
    transformed = []
    for class_id, x_center, y_center, width, height in labels:
        x_center = (x_center * original_width * scale + pad_x) / target_width
        y_center = (y_center * original_height * scale + pad_y) / target_height
        width = width * original_width * scale / target_width
        height = height * original_height * scale / target_height
        transformed.append([class_id, x_center, y_center, width, height])
    return canvas, transformed


def write_label(path: Path, labels: List[List[float]]) -> None:
    path.write_text("".join(f"{int(row[0])} {row[1]:.8f} {row[2]:.8f} {row[3]:.8f} {row[4]:.8f}\n" for row in labels), encoding="utf-8")


def prepare(records: List[dict], assignments: Dict[str, str], output: Path, config: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    target_size = tuple(config["target_size"])
    for record in records:
        split = assignments[record["source_path"]]
        destination_root = output / split / record["dataset"]
        source_name = Path(record["source_path"]).name
        image_destination = destination_root / "images" / Path(source_name).with_suffix(".jpg")
        label_destination = destination_root / "labels" / Path(source_name).with_suffix(".txt")
        image_destination.parent.mkdir(parents=True, exist_ok=True)
        label_destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(record["source_path"]) as image:
            processed, labels = letterbox(image, record["labels"], target_size)
            processed.save(image_destination, quality=95)
        write_label(label_destination, labels)
        manifest.append({"split": split, "dataset": record["dataset"], "source_path": record["source_path"], "source_sha256": record["source_sha256"], "group": record["group"], "class_names": record["class_names"], "image": str(image_destination), "label": str(label_destination), "labels": labels, "objects": len(labels)})
    (output / "manifest_v1.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (output / "split_summary.json").write_text(json.dumps({split: sum(item["split"] == split for item in manifest) for split in ("train", "val", "test")}, indent=2), encoding="utf-8")


class YoloDataset:
    """Minimal loader returning normalized RGB image arrays and YOLO targets."""

    def __init__(self, manifest_path: Path, split: str, augment: bool = False, flip_probability: float = 0.0):
        self.records = [item for item in json.loads(manifest_path.read_text(encoding="utf-8")) if item["split"] == split]
        self.augment = augment and split == "train"
        self.flip_probability = flip_probability

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index: int):
        if Image is None:
            raise RuntimeError("Pillow is required to load Prepared Dataset V1")
        record = self.records[index]
        try:
            import numpy as np
        except ImportError as exc:
            raise RuntimeError("NumPy is required to load Prepared Dataset V1") from exc
        with Image.open(record["image"]) as image:
            image_array = np.asarray(image.convert("RGB"), dtype="float32") / 255.0
        labels = json.loads(json.dumps(record.get("labels", [])))
        if self.augment and random.random() < self.flip_probability:
            image_array = image_array[:, ::-1, :].copy()
            labels = [[row[0], 1.0 - row[1], row[2], row[3], row[4]] for row in labels]
        return image_array, labels, record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("preprocessing_config.json"))
    parser.add_argument("--archive", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    base = args.config.parent
    archive = args.archive or (base / config["archive_relative_path"]).resolve()
    output = args.output or (base / config["output_directory"]).resolve()
    records, errors = build_records(archive, config)
    if not records:
        report = {"status": "blocked", "archive": str(archive), "records": 0, "errors": errors[:100]}
        output.mkdir(parents=True, exist_ok=True)
        (output / "preparation_status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2
    assignments = assign_splits(records, config)
    prepare(records, assignments, output, config)
    (output / "exclusions_v1.json").write_text(json.dumps({"status": "prepared_with_exclusions", "excluded_records": len(errors), "errors": errors[:1000]}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "prepared", "records": len(records), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
