# Day 16 - Object Detection Baseline

This folder prepares the raw-data transfer-learning detector baseline, evaluation metrics, timing/model-size records, prediction outputs, and checkpoints.

## Files

- `train_baseline.py` - validates Dataset V1, trains one dataset-specific Ultralytics YOLO baseline, evaluates it, and records artifacts.
- `detector_config.yaml` - baseline training configuration.
- `baseline_metrics.csv` - metric/output schema.
- `evaluation_protocol.md` - baseline evaluation and class-error review rules.

## Run

Install the approved detector dependency in the selected environment, then run:

```bash
python3 train_baseline.py --config detector_config.yaml --dataset-name DIATAquarium.v4i.yolov8
```

The script expects `prepared_dataset_v1/manifest_v1.json` from Day 11 and a dataset-specific class map. It writes checkpoints under `outputs/<dataset>/raw_v1/weights/`, predictions under `outputs/<dataset>/raw_v1/predictions/`, and metrics under `outputs/<dataset>/raw_v1/`.

The current workspace has no prepared records, so execution reports a blocked status and does not create fabricated metrics or checkpoints.
