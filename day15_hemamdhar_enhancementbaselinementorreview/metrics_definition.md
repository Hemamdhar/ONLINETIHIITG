# Raw-vs-Enhanced Metrics Definition

## Detection metrics

- **Precision:** predicted positives that are correct under the fixed IoU and confidence rules.
- **Recall:** ground-truth objects detected under the same rules.
- **mAP@50:** mean AP at IoU 0.50.
- **mAP@50-95:** mean AP over IoU thresholds 0.50 through 0.95.
- **Per-class AP:** AP reported separately for every dataset-specific class.
- **Rare-class recall:** recall for classes below the predeclared support threshold; record that threshold with the run.

## Operational metrics

- **Preprocessing time:** enhancement plus image preparation time per image, measured separately from detector inference.
- **Inference time:** detector time per image under a stated batch size and hardware.
- **FPS:** images per second under the stated end-to-end or inference-only definition.

## Image-quality metrics

- **UIQM:** optional descriptive underwater quality score; never the sole selection criterion.
- **PSNR/SSIM:** report only where a valid reference image pair exists. They are not valid for arbitrary enhanced/raw pairs when no clean reference is available.

## Comparison requirements

Use identical source records, labels, class maps, splits, detector controls, and seed schedule. Report validation results for selection and hold out the test split until the final condition is frozen. Include confidence intervals or seed variation when multiple runs are available.
