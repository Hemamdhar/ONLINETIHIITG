# Day 17 - Enhanced Detection / Tracking

## Completed notebook

- `enhanced_detection_tracking.ipynb` - generates matched CLAHE/gamma derivatives, applies the frozen Day 16 detector to raw and enhanced DIAT test images, records runtime/detection behavior, and reports exploratory sequence tracking status.

## Generated outputs

- `enhancement_outputs_v1/` - 17,788 DIAT CLAHE/gamma derivative records.
- `day17_outputs/enhanced_inference_summary.json` - raw/CLAHE/gamma inference counts and timing.
- `day17_outputs/raw_v1/`, `clahe_v1/`, `gamma_v1/` - saved detector predictions and images.
- `day17_outputs/tracking_status.json` - sequence-group and tracking-ground-truth status.

## Observed smoke-run result

All three conditions processed 954 DIAT test images with the frozen Day 16 smoke checkpoint. The checkpoint produced zero detections in this abbreviated run, so no precision/recall/mAP improvement claim is made. Runtime was approximately 46.9 ms/image for raw, 45.3 ms/image for CLAHE, and 56.4 ms/image for gamma.

The tracker is exploratory only. The manifest contains sequence proxies but no persistent object IDs or approved tracking ground truth, so IDF1, MOTA, and identity-switch metrics are intentionally not reported.

## Reproducibility

The comparison uses the same checkpoint, test records, image size (`320`), confidence (`0.25`), IoU (`0.50`), and source manifest for all conditions. The Day 16 checkpoint was trained with only 1 epoch and 2% of the training data, so these are pipeline smoke outputs rather than final scientific detector results.
