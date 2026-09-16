# Enhancement Baseline Results + Mentor Review

## 1. Current decision

**Enhancement baseline:** Protocol ready; measured results pending Dataset V1.  
**Detector training:** Plan defined for raw and enhanced paired runs.  
**Mentor feedback:** Awaiting review.  
**Release state:** BLOCKED until the raw archive, prepared manifest, and quality gates are complete.

## 2. Conditions under comparison

| Condition  | Input               | Parameters                                             | Role                            |
| ---------- | ------------------- | ------------------------------------------------------ | ------------------------------- |
| `raw_v1`   | Prepared Dataset V1 | None                                                   | Reference condition             |
| `clahe_v1` | Same V1 images      | clip limit `2.0`, tile grid `8x8`                      | Classical enhancement baseline  |
| `gamma_v1` | Same V1 images      | gamma `1.0`, contrast `1.0` until validation selection | Lightweight diagnostic baseline |

All conditions use the same labels, source checksums, groups, splits, detector input size, and evaluation protocol. Enhancement outputs are derivatives and never replace raw or prepared inputs.

## 3. Data-quality status

| Quality item                   | Status  | Required evidence                                  |
| ------------------------------ | ------- | -------------------------------------------------- |
| Archive inventory/checksums    | BLOCKED | Day 7 inventory and checksum manifest              |
| Image-label pairs              | BLOCKED | Complete pair manifest and dispositions            |
| YOLO validity                  | BLOCKED | Parser output and corrected-label review           |
| Resolution/visibility EDA      | BLOCKED | Day 10 statistics and representative grids         |
| Class support                  | BLOCKED | Per-dataset/per-class counts and rare-class review |
| Duplicate/source-group overlap | BLOCKED | Exact/near duplicate and sequence report           |
| Prepared Dataset V1            | BLOCKED | Day 11 manifest and post-transform validation      |

## 4. Results table

Populate only from frozen validation/test runs. Keep test values hidden until the final condition is selected.

| Dataset | Split | Condition               | Precision | Recall | mAP50 | mAP50-95 | Rare-class recall | Preprocess ms/img | Inference ms/img | FPS | Status  |
| ------- | ----- | ----------------------- | --------: | -----: | ----: | -------: | ----------------: | ----------------: | ---------------: | --: | ------- |
| Pending | val   | raw_v1                  |           |        |       |          |                   |                   |                  |     | pending |
| Pending | val   | clahe_v1                |           |        |       |          |                   |                   |                  |     | pending |
| Pending | val   | gamma_v1                |           |        |       |          |                   |                   |                  |     | pending |
| Pending | test  | selected condition only |           |        |       |          |                   |                   |                  |     | blocked |

## 5. Interpretation rules

- Select enhancement using validation performance, rare-class behavior, visual failure cases, and processing cost together.
- Report per-class AP and recall; aggregate mAP alone cannot hide rare-class regressions.
- Compare paired source records so raw and enhanced results use identical evidence.
- Treat UIQM as descriptive, not as a detector-success criterion.
- Do not report PSNR/SSIM without valid reference image pairs.
- Evaluate the untouched test split once after the condition and parameters are frozen.
- Keep the raw condition as the primary reference even if enhancement is selected.

## 6. Mentor review prompts

1. Is the raw-vs-CLAHE-vs-gamma comparison sufficient for the first baseline?
2. Should gamma remain identity until validation selects a non-identity value?
3. Are the fixed detector model, checkpoint, epoch budget, and seed schedule approved?
4. Are per-class recall and runtime acceptable decision criteria?
5. Are any difficult classes or visibility strata missing from the review set?
6. Should a learned enhancement be added after the classical baseline, or remain out of scope?

## 7. Release decision

**Current decision:** Do not claim an enhancement winner or detector result until Dataset V1 passes its evidence gates and the mentor feedback below is completed.
