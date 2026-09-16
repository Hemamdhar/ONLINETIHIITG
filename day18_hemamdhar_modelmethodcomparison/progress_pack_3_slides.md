# Day 18 Progress Pack - 3 Slides

## Slide 1 - What has been built and compared

**Title:** Model and Method Comparison: Current Evidence

- Three matched conditions are defined: `raw_v1`, `clahe_v1`, and `gamma_v1`.
- The same frozen Day 16 YOLOv8n checkpoint, manifest, image size, confidence threshold, and IoU threshold were used for all conditions.
- The DIAT smoke evaluation processed 954 paired test images per condition.
- Detector metrics from the smoke checkpoint:
  - raw: precision 0.0, recall 0.0, mAP50 0.0, mAP50-95 0.0
  - CLAHE: precision 0.0, recall 0.0, mAP50 0.0, mAP50-95 0.0
  - gamma: precision 0.0, recall 0.0, mAP50 0.0, mAP50-95 0.0
- Interpretation: these are smoke-run outputs from 1 epoch and 2% training data, not final model conclusions.

## Slide 2 - Efficiency, limitations, and failure risks

**Title:** Runtime and Evidence Gaps

| Condition | ms/image |     FPS | Current reading                        |
| --------- | -------: | ------: | -------------------------------------- |
| raw_v1    |  42.9064 | 23.3065 | Fastest reference                      |
| clahe_v1  |  50.0835 | 19.9667 | Moderate overhead                      |
| gamma_v1  |  63.8674 | 15.6574 | Slowest; current transform is identity |

- UIQM, PSNR, and SSIM were not measured; PSNR/SSIM require valid reference pairs.
- Sequence groups exist, but persistent object IDs do not; formal tracking consistency metrics are unavailable.
- The tracker function exists but has not yet produced track assignments or rendered tracking output.
- Main risks: underfitting, blocked leakage-safe splits for some datasets, small/dark/turbid/blurred/occluded scenes, annotation ambiguity, and tracker instability after missed detections.
- No enhancement winner can be claimed from the present smoke run.

## Slide 3 - Shortlist and mentor decisions

**Title:** Recommended Next Experiment

**Shortlist**

1. `clahe_v1` with a properly trained comparable detector: strongest enhancement candidate because it is non-identity, deterministic, and has lower overhead than gamma.
2. `raw_v1` control: mandatory reference and operational fallback because it is fastest.
3. `gamma_v1`: diagnostic only until validation selects non-identity parameters and demonstrates benefit.

**Before final selection**

- Complete a group-safe, longer detector run.
- Select enhancement and parameters on validation only.
- Compare per-class AP, rare-class recall, difficult-scene failures, and runtime.
- Execute the IoU tracker on non-empty ordered predictions and save tracking output.
- Obtain persistent IDs before reporting IDF1, MOTA, MOTP, or identity switches.
- Freeze the method, then evaluate the untouched test split once.

**Mentor approvals requested**

- CLAHE as the next enhancement candidate.
- Detector model, epochs, seeds, and runtime/accuracy thresholds.
- Separate-dataset reporting and tracking scope.
