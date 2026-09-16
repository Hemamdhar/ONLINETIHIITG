# Day 19 - Controlled Experiment Strategy

## Objective

Tune the Day 18 shortlisted enhancement candidate, `clahe_v1`, while preserving `raw_v1` as the fixed reference. The experiment selects parameters using DIAT validation data only. The final test split is not read or evaluated by the Day 19 sweep.

## Search space

| Experiment      | Condition | Clip limit | Grid size | Role                        |
| --------------- | --------- | ---------: | --------: | --------------------------- |
| D19-raw-control | raw_v1    |        n/a |       n/a | Fixed reference             |
| D19-clahe-1p5x8 | clahe_v1  |        1.5 |       8x8 | Lower enhancement strength  |
| D19-clahe-2x8   | clahe_v1  |        2.0 |       8x8 | Day 13/Day 17 baseline      |
| D19-clahe-3x8   | clahe_v1  |        3.0 |       8x8 | Higher enhancement strength |

Only one meaningful parameter, CLAHE clip limit, is varied in this first controlled search. Grid size is held at the approved 8x8 setting so the experiment does not confound multiple changes. Gamma is not tuned because Day 18 identified the current gamma candidate as an identity transform and deferred it.

## Fixed controls

- Dataset: `DIATAquarium.v4i.yolov8`.
- Split: `val` only, deterministic first 256 records after sorting by source image path. The full validation split contains 2,222 images across 294 groups; this bounded subset keeps the CPU experiment reproducible and executable locally.
- Model: frozen Day 16 `best.pt` checkpoint.
- Image size: 320.
- Confidence threshold: 0.25.
- IoU threshold: 0.50.
- Batch: 16.
- Device: CPU.
- Same validation records and source order for every candidate.
- No test records are loaded by `run_validation_sweep.py`.

## Selection rule

The preferred candidate maximizes validation detections on the deterministic 256-image subset. Ties are broken by lower detector inference time per image. This rule is a smoke-check selection rule, not a claim of accuracy superiority, because the abbreviated Day 16 checkpoint does not provide a meaningful trained-model basis for precision, recall, or mAP selection. A production selection must replace this with full-validation mAP50-95, rare-class recall, failure-case review, and runtime budget.

## Reproducibility and logging

`run_validation_sweep.py` regenerates validation-only derived images, runs the same frozen checkpoint for all candidates, writes every candidate to `experiment_log_v1.csv`, and saves the selected configuration to `best_validated_config.json`. Derived files are under `validation_derivatives_v1/`; raw and test data are not modified.

## Interpretation boundary

A candidate marked best here is the best configuration under this controlled smoke sweep. It must not be evaluated on the final test split until the parameter is frozen and the detector is retrained or otherwise approved for a meaningful final comparison.
