# Day 16 Completion Status

## Requirement audit

| Requirement | Status | Evidence |
|---|---|---|
| Transfer-learning detector on raw data | PARTIAL | DIAT raw_v1 trained from `yolov8n.pt` |
| Precision, recall, mAP | COMPLETE FOR DIAT SMOKE RUN | `DIATAquarium.v4i.yolov8/raw_v1/metrics.json` |
| Class-wise errors | COMPLETE FOR DIAT SMOKE RUN | Per-class AP and confusion-matrix plots |
| Model size/software/inference time | COMPLETE FOR DIAT SMOKE RUN | Metrics JSON records parameters, checkpoint size, speed, Python, platform |
| Predictions/checkpoints | COMPLETE FOR DIAT SMOKE RUN | `train/weights/best.pt`, `last.pt`, and `predictions/` |
| Aquatic Plant baseline | BLOCKED | Only two source groups; no leakage-safe three-way split |
| Well baseline | BLOCKED | One source group; no leakage-safe three-way split |
| Full planned 50-epoch baseline | NOT COMPLETE | CPU environment; only accelerated 1-epoch smoke run completed |

## DIAT smoke-run result

- Dataset: `DIATAquarium.v4i.yolov8`
- Condition: `raw_v1`
- Model: `yolov8n.pt`
- Parameters: 3,007,793
- Checkpoint size: 5.9199 MB
- Local run controls: 1 epoch, 320px input, 2% training fraction
- Precision: 0.0
- Recall: 0.0
- mAP@50: 0.0
- mAP@50-95: 0.0
- Inference speed: approximately 41.04 ms/image
- Platform: Python 3.13.6 on macOS ARM64

These zero metrics are valid outputs of the intentionally abbreviated smoke run and must not be presented as a trained-model conclusion.

## Final decision

**Day 16 implementation and one DIAT smoke baseline are complete. The full multi-dataset detection baseline is not complete.**

Do not create random test splits for Aquatic Plant or Well. To complete those runs, obtain additional independent source sequences or approve an evaluation design that does not claim a three-way sequence-safe split. To obtain the planned baseline, run the configured 50 epochs on suitable hardware and preserve the current manifest version with the results.
