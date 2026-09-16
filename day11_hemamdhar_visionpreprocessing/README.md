# Day 11 - Vision Preprocessing

This folder implements Prepared Dataset V1. The pipeline keeps the Day 7 raw archive read-only and writes versioned manifests and processed records under `prepared_dataset_v1/`.

## Files

- `preprocessing_config.json` - frozen V1 dimensions, split ratios, normalization, and augmentation policy.
- `preprocess_dataset.py` - inventory, YOLO validation, leakage-safe group splitting, deterministic letterboxing, and a PyTorch-compatible loader.

## Run

From this folder:

```bash
python3 preprocess_dataset.py --config preprocessing_config.json
```

The default archive is `../day7_hemamdhar_initialinspection/raw_data_archive`. Override it with `--archive` if needed.

## V1 policy

- Raw files are never overwritten.
- Dataset exports retain separate class spaces.
- Source sequence and duplicate groups are assigned to one split only.
- Images are letterboxed to `640x640`; boxes receive the same transform and are revalidated.
- Images are normalized to `[0, 1]` only when loaded by `YoloDataset`.
- Training augmentation is limited to deterministic horizontal flip when enabled; validation and test are unchanged.
- No preprocessing output is produced until the archive contains readable image-label pairs.

The current workspace does not contain the downloaded raw archive, so execution will report a blocked preparation state rather than create fabricated data.
