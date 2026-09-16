# Enhancement and Detection Comparison Protocol

## Conditions

- `raw_v1`: prepared Dataset V1 with no enhancement.
- `clahe_v1`: CLAHE-derived images using fixed clip limit and tile grid.
- `gamma_v1`: fixed gamma/contrast diagnostic baseline.

Enhancement outputs are derivatives linked to the same source path, checksum, label, group, and split. Labels do not change because these baselines are photometric transformations only.

## Fair comparison controls

1. Use the same frozen Dataset V1 manifest and dataset-specific class map.
2. Use the same train/validation/test group assignments, model architecture, checkpoint initialization, image size, optimizer, epochs, augmentation, confidence threshold, IoU threshold, and seed schedule.
3. Select enhancement parameters using training/validation evidence only. The test split is evaluated once after the condition is frozen.
4. Report precision, recall, mAP@50, mAP@50-95, per-class AP, rare-class behavior, false-negative examples, preprocessing time, inference time, and FPS.
5. Compare raw and enhanced conditions on paired source records so changes are attributable to the enhancement.
6. Retain visual grids of representative improvements and failures, including dark, turbid, blurred, color-cast, and occluded scenes.

## Enhancement defaults

- CLAHE: grayscale luminance/equalization implementation; default clip limit `2.0`, tile grid `8x8`.
- Gamma: default gamma `1.0` and contrast `1.0`, which is identity until a validation-selected value is supplied.
- No vertical flip, random color jitter, or test-time augmentation in this baseline package.

## Tracking and sequence metadata

The prepared manifest's source `group` is a sequence proxy for leakage control. It is not an object identity. Run `prepare_sequence_metadata.py` to export group IDs and detect cross-split group overlap. Do not report formal tracking metrics without persistent object IDs or approved tracking ground truth.

## Decision rule

Prefer an enhanced condition only if it improves or preserves detector performance, rare-class recall, and failure-case behavior within the approved processing budget. A higher UIQM alone is insufficient, and PSNR/SSIM are not claimed without valid reference image pairs.
